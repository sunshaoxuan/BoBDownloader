import re
import json
import requests
import argparse
from bs4 import BeautifulSoup

def sanitize_filename(filename):
    """
    Sanitize the filename by removing illegal characters
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_download_url(download_info):
    try:
        download_host_url = f"https://genyoutube.online/mates/en/convert?id={download_info['id']}"
        headers = {
            "x-note": download_info["note"]
        }
        data = {
            "platform": "youtube",
            "url": download_info["video_url"],
            "title": download_info["title"],
            "id": download_info["id"],
            "ext": download_info["ext"],
            "note": download_info["note"],
            "format": download_info["format"]
        }

        response = requests.post(download_host_url, headers=headers, data=data)
        response.raise_for_status()

        response_data = response.json()

        if response_data.get("status") == "success":
            download_url = response_data.get("downloadUrlX")
            return download_url
        elif response_data.get("status") == "convert_ready":
            print("The file is being prepared, please try again later.")
            return None
        else:
            print("Download request failed, server returned status:", response_data.get("status"))
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to request download URL: {e}")
        return None

def parse_onclick_content(onclick_content):
    try:
        params_pattern = r"download\('([^']*)','([^']*)','([^']*)','([^']*)',(\d+),'([^']*)','([^']*)'\)"
        match = re.search(params_pattern, onclick_content)

        if not match:
            print("Failed to match the correct onclick parameter format")
            return None

        video_url, title, id, ext, total_size, note, format_ = match.groups()

        return {
            "video_url": video_url,
            "title": title,
            "id": id,
            "ext": ext,
            "total_size": total_size,
            "note": note,
            "format": format_
        }
    except Exception as e:
        print(f"Error parsing onclick content: {e}")
        return None

def extract_outermost_div_and_script(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        outer_div = soup.find('div', recursive=False)
        if not outer_div:
            print("No resolution download information source found.")
            return None
        else:
            print("Found resolution download information source")

        return outer_div
    except Exception as e:
        print(f"Error extracting address: {e}")
        return None

def parse_div_section_ex(div_content):
    """
    Parse the <div> section to extract information for all available resolutions, and let the user choose
    """
    try:
        soup = BeautifulSoup(str(div_content), 'html.parser')
        table = soup.find('table', class_='table-bordered')

        if not table:
            print("No download information table found")
            return None

        rows = table.find_all('tr')
        if not rows:
            print("No rows found in the table")
            return None

        options = []

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                resolution = columns[0].text.strip()
                size = columns[1].text.strip()
                download_button = columns[2].find('button')
                if download_button and 'onclick' in download_button.attrs:
                    onclick_content = download_button['onclick']
                    download_info = parse_onclick_content(onclick_content)
                    if download_info:
                        download_info['resolution'] = resolution
                        download_info['size'] = size
                        options.append(download_info)

        if not options:
            print("No available resolution information found")
            return None

        # List all available resolutions and let the user choose
        print("\nAvailable Resolutions:")
        for index, option in enumerate(options, start=1):
            print(f"{index}. Resolution: {option['resolution']}, Size: {option['size']}")

        choice = input("Enter the number of the resolution you want to download: ")
        
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid input, please rerun the program and select a valid number.")
            return None

        return options[int(choice) - 1]

    except Exception as e:
        print(f"Error parsing <div> section: {e}")
        return None

def analyze_video(video_url):
    service_url = "https://genyoutube.online/mates/en/analyze/ajax"
    data = {
        "url": video_url,
        "ajax": 1,
        "lang": "en",
        "platform": "youtube"
    }

    try:
        response = requests.post(service_url, data=data)
        response.raise_for_status()

        response.encoding = 'utf-8'
        json_response = response.text
        json_data = json.loads(json_response)
        
        if json_data.get("status") == "success" and "result" in json_data:
            return json_data["result"]
        else:
            print("The returned JSON format is not as expected")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def download_video(download_url, title, resolution, file_type):
    try:
        # Sanitize the filename
        sanitized_title = sanitize_filename(title)

        output_file = f"{sanitized_title}_{resolution}.{file_type}"
        
        # Download the file using the provided link
        print(f"Starting download: {download_url}")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Download completed: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# Main program
if __name__ == "__main__":
    # Use argparse to get command line arguments
    parser = argparse.ArgumentParser(description="YouTube Video Downloader Script")
    parser.add_argument("video_url", help="URL of the YouTube video to download")
    args = parser.parse_args()

    # Get the video URL
    video_url = args.video_url
    html_fragment = analyze_video(video_url)
    
    print(f"Analyzing video URL: {video_url}...")
    div_section = extract_outermost_div_and_script(html_fragment)

    if div_section:
        print("Fetching download information...")
        download_info = parse_div_section_ex(div_section)

        if download_info:
            print("Parsing download URL...")
            download_url = get_download_url(download_info)

            if download_url:
                download_video(download_url, download_info["title"], download_info["note"], download_info["ext"])
