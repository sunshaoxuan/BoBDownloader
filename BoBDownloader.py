"""
YouTube Video Downloader

Exit Codes:
0  - Successful download
1  - User interruption (e.g., Ctrl+C)
2  - File size mismatch
3  - Download failure (request exception)
4  - Download URL not found
5  - Download info not found
6  - Div section extraction failed
7  - Video analysis failed
8  - Unexpected error
"""

import re
import json
import requests
import argparse
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
import os
import time
from tqdm import tqdm
import sys

# SECRET KEY
secret_key = b'GIgwb1iHbTv8WNH6lewJD2Xl_wukBT8eH9ApXV5NyWs='

# ENCRYPTED CONFIG
encrypted_config = b'gAAAAABnTlZM5RWhy_zIlX_8rfXtFWQOjtMsj_ipJzY355li_ibOWokSb0JLLvCUOj5Dz_fp5MOA3GfGZGAhXlWGkZXZZ9u72pDIqN2DapbeNYeFPXaJOKftFLYbz09Hmy9XS_5mY-3P22PuP4SaX3NCo0lRWB85OQja2KrsvHi_Ir5VGDD-hlNkN64a8h7T4rUO6vRpMdXmyTw8fBkeaIMnqtkI0JEmw7btPJdIwe7VGBZzgw2O2F8='

def load_encrypted_data(data_type):
    try:
        # Decrypt the data
        cipher_suite = Fernet(secret_key)
        decrypted_data = cipher_suite.decrypt(encrypted_config).decode()

        # Return the corresponding data
        data_dict = json.loads(decrypted_data)
        return data_dict.get(data_type)

    except Exception as e:
        print(f"Unexpected error: {e}")

def load_encrypted_url():
    return load_encrypted_data("url")

def load_encrypted_service_url():
    return load_encrypted_data("service_url")

def sanitize_filename(filename):
    """
    Sanitize the filename by removing illegal characters
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_download_url(download_info, max_retries, wait_time, conversion_wait_time):
    for attempt in range(max_retries):
        try:
            download_host_url = load_encrypted_url() + download_info['id']
            print(f"Attempt {attempt + 1}/{max_retries}: Requesting download URL...")

            headers = {"x-note": download_info["note"]}
            data = {
                "platform": "youtube",
                "url": download_info["video_url"],
                "title": download_info["title"],
                "id": download_info["id"],
                "ext": download_info["ext"],
                "note": download_info["note"],
                "format": download_info["format"]
            }

            response = requests.post(download_host_url, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            status = response_data.get("status")
            if status == "success":
                print("Success: Download URL retrieved.")
                return response_data.get("downloadUrlX")
            elif status == "convert_ready":
                print("Conversion is not ready. Waiting for conversion to complete...")
                time.sleep(conversion_wait_time)  # Wait before retrying
            elif status == "busy":
                print("Server is busy. Retrying after a short wait...")
                time.sleep(wait_time)
            else:
                print(f"Unexpected status: {status}. Retrying...")
                time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Request failed with error: {e}")
            time.sleep(wait_time)

    print("Failed to retrieve download URL after maximum retries.")
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

def parse_div_section_ex(div_content, preferred_resolution=None):
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

        # If the preferred resolution is specified, try to find it in the options
        if preferred_resolution:
            for option in options:
                if preferred_resolution in option['resolution']:
                    return option
            print(f"Preferred resolution {preferred_resolution} not found, please choose manually.")

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
    service_url = load_encrypted_service_url()
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

def download_video(download_url, title, resolution, file_type, output_path=None):
    try:
        # Sanitize the filename
        sanitized_title = sanitize_filename(title)

        # Determine the output file path
        if output_path:
            if os.path.isdir(output_path):
                output_file = os.path.join(output_path, f"{sanitized_title}_{resolution}.{file_type}")
            else:
                output_file = output_path
        else:
            output_file = f"{sanitized_title}_{resolution}.{file_type}"

        # Download the file using the provided link
        print(f"File name: {output_file}")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        start_time = time.time()  # Record the start time

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Calculate percentage
                    percentage = (downloaded_size / total_size) * 100 if total_size else 0
                    
                    # Calculate download speed
                    elapsed_time = time.time() - start_time
                    speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
                    
                    # Estimate time remaining
                    time_remaining = (total_size - downloaded_size) / speed if speed > 0 else float('inf')
                    
                    # Convert bytes to a human-readable format
                    def human_readable_size(size, decimal_places=2):
                        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                            if size < 1024.0:
                                return f"{size:.{decimal_places}f} {unit}"
                            size /= 1024.0
                        return f"{size:.{decimal_places}f} PB"

                    # Clear the line and display the download progress
                    print(f"\r{' ' * 80}\rDownloaded {human_readable_size(downloaded_size)} of {human_readable_size(total_size)} ({percentage:.2f}%) "
                          f"at {human_readable_size(speed)}/s, ETA: {time_remaining:.2f}s", end='', flush=True)

        print(f"\nDownload completed: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# Example of a master branch related comment or logic
# This logic is specific to the master branch
def some_master_branch_function():
    # Perform some operations specific to the master branch
    pass

# Main script
if __name__ == "__main__":
    # Ensure this script is running on the master branch
    current_branch = "master"  # This is a placeholder for actual branch checking logic
    if current_branch == "master":
        print("Running on the master branch")
        # Execute master branch specific logic
        some_master_branch_function()

    try:
        # Use argparse to get command line arguments
        parser = argparse.ArgumentParser(
            description="Download YouTube videos with specified resolution.\n\n"
                        "Usage:\n"
                        "  python BoBDownloader.py <video_url> [--resolution <resolution>] [--auto-select] [--output <path>]\n\n"
                        "Arguments:\n"
                        "  video_url            The URL of the YouTube video to download.\n"
                        "  --resolution         Preferred resolution (default: 720p).\n"
                        "  --auto-select        Automatically select alternative resolution if preferred is not available.\n"
                        "  --output             Output path for the downloaded video.\n"
                        "  --max-retries        Maximum number of retries for download URL request (default: 5).\n"
                        "  --wait-time          Wait time in seconds between retries (default: 10).\n"
                        "  --conversion-wait    Wait time in seconds for 'convert_ready' status (default: 20).\n\n"
                        "Exit Codes:\n"
                        "  0  - Successful download\n"
                        "  1  - User interruption (e.g., Ctrl+C)\n"
                        "  2  - File size mismatch\n"
                        "  3  - Download failure (request exception)\n"
                        "  4  - Download URL not found\n"
                        "  5  - Download info not found\n"
                        "  6  - Div section extraction failed\n"
                        "  7  - Video analysis failed\n"
                        "  8  - Unexpected error",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("video_url", help="The URL of the YouTube video to download.")
        parser.add_argument("--resolution", help="Preferred resolution (default: 720p)", default="720p")
        parser.add_argument("--auto-select", action="store_true", 
                          help="Automatically select alternative resolution if preferred is not available")
        parser.add_argument("--output", help="Output path for the downloaded video", default=None)
        parser.add_argument("--max-retries", type=int, default=5, help="Maximum number of retries for download URL request")
        parser.add_argument("--wait-time", type=int, default=10, help="Wait time in seconds between retries")
        parser.add_argument("--conversion-wait", type=int, default=20, help="Wait time in seconds for 'convert_ready' status")
        args = parser.parse_args()

        # Use the parsed arguments
        max_retries = args.max_retries
        wait_time = args.wait_time
        conversion_wait_time = args.conversion_wait

        # Get the video URL
        video_url = args.video_url
        preferred_resolution = args.resolution
        output_path = args.output
        print(f"\r{' ' * 80}\rAnalyzing video URL: {video_url}...", end='')
        html_fragment = analyze_video(video_url)
        print("Analysis complete.")

        print(f"\r{' ' * 80}\rFetching the resolution information...", end='')    
        div_section = extract_outermost_div_and_script(html_fragment)
        print("Resolution information fetched.")

        if div_section:
            print(f"\r{' ' * 80}\rFetching download information...", end='')
            download_info = parse_div_section_ex(div_section, preferred_resolution)
            print("Download information fetched.")

            if download_info:
                print(f"\r{' ' * 80}\rParsing download URL...", end='')
                download_url = get_download_url(download_info, max_retries, wait_time, conversion_wait_time)
                print("Download URL parsed.")

                if download_url:
                    print("Downloading the video...")
                    download_video(download_url, download_info["title"], download_info["note"], download_info["ext"], output_path)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
