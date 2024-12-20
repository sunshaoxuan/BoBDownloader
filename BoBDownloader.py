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
import logging
import signal

# SECRET KEY
secret_key = b'GIgwb1iHbTv8WNH6lewJD2Xl_wukBT8eH9ApXV5NyWs='

# ENCRYPTED CONFIG
encrypted_config = b'gAAAAABnTlZM5RWhy_zIlX_8rfXtFWQOjtMsj_ipJzY355li_ibOWokSb0JLLvCUOj5Dz_fp5MOA3GfGZGAhXlWGkZXZZ9u72pDIqN2DapbeNYeFPXaJOKftFLYbz09Hmy9XS_5mY-3P22PuP4SaX3NCo0lRWB85OQja2KrsvHi_Ir5VGDD-hlNkN64a8h7T4rUO6vRpMdXmyTw8fBkeaIMnqtkI0JEmw7btPJdIwe7VGBZzgw2O2F8='

# LOG DIRECTORY AND FILE
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "BoBDownloader.log")

# ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Global variable to track if the process should terminate
terminate_flag = False

def signal_handler(signum, frame):
    global terminate_flag
    logger.warning("Received termination signal. Preparing to exit...")
    terminate_flag = True

# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)

def load_encrypted_data(data_type):
    try:
        cipher_suite = Fernet(secret_key)
        decrypted_data = cipher_suite.decrypt(encrypted_config).decode()
        data_dict = json.loads(decrypted_data)
        return data_dict.get(data_type)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

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
        if terminate_flag:
            logger.warning("Download URL retrieval interrupted by termination signal.")
            return None

        try:
            download_host_url = load_encrypted_url() + download_info['id']
            logger.info(f"Attempt {attempt + 1}/{max_retries}: Requesting download URL...")

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
                logger.info("Success: Download URL retrieved.")
                return response_data.get("downloadUrlX")
            elif status == "convert_ready":
                logger.info("Conversion is not ready. Waiting for conversion to complete...")
                for _ in range(conversion_wait_time):
                    if terminate_flag:
                        logger.warning("Conversion wait interrupted by termination signal.")
                        return None
                    time.sleep(conversion_wait_time)
            elif status == "busy":
                logger.info("Server is busy. Retrying after a short wait...")
                for _ in range(wait_time):
                    if terminate_flag:
                        logger.warning("Busy wait interrupted by termination signal.")
                        return None
                    time.sleep(wait_time)
            else:
                logger.warning(f"Unexpected status: {status}. Retrying...")
                for _ in range(wait_time):
                    if terminate_flag:
                        logger.warning("Unexpected status wait interrupted by termination signal.")
                        return None
                    time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries}: Request failed with error: {e}")
            for _ in range(wait_time):
                if terminate_flag:
                    logger.warning("Request exception wait interrupted by termination signal.")
                    return None
                time.sleep(wait_time)

    logger.error("Failed to retrieve download URL after maximum retries.")
    return None

def parse_onclick_content(onclick_content):
    try:
        params_pattern = r"download\('([^']*)','([^']*)','([^']*)','([^']*)',(\d+),'([^']*)','([^']*)'\)"
        match = re.search(params_pattern, onclick_content)

        if not match:
            logger.error("Failed to match the correct onclick parameter format")
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
        logger.error(f"Error parsing onclick content: {e}")
        return None

def extract_outermost_div_and_script(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        outer_div = soup.find('div', recursive=False)
        if not outer_div:
            logger.error("No resolution download information source found.")
            return None
        else:
            logger.info("Found resolution download information source")
        return outer_div
    except Exception as e:
        logger.error(f"Error extracting address: {e}")
        return None

def parse_div_section_ex(div_content, preferred_resolution=None, auto_select=False):
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
            logger.error("No available resolution information found")
            return None
    
        # If the preferred resolution is specified, try to find it in the options
        if preferred_resolution:
            for option in options:
                if preferred_resolution in option['resolution']:
                    return option
            
            if auto_select:
                logger.info(f"Preferred resolution {preferred_resolution} not found, auto-selecting available option")
                return options[0]  # select the first option if auto-select is enabled
            else:
                logger.info(f"Preferred resolution {preferred_resolution} not found, please choose manually")

        # If only one option is available and auto-select is enabled
        if len(options) == 1 and auto_select:
            return options[0]

        # List all available resolutions and let the user choose
        if not auto_select:
            print("\nAvailable Resolutions:")
            for index, option in enumerate(options, start=1):
                print(f"{index}. Resolution: {option['resolution']}, Size: {option['size']}")

            choice = input("Enter the number of the resolution you want to download: ")
            
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
                logger.error("Invalid input, please rerun the program and select a valid number")
                return None

            return options[int(choice) - 1]
        else:
            return options[0]  # select the first option if auto-select is enabled

    except Exception as e:
        logger.error(f"Error parsing <div> section: {e}")
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
    sanitized_title = sanitize_filename(title)

    # Determine output file name
    if output_path and os.path.isfile(output_path):
        # If output_path is a file, use it directly
        output_file = output_path
    elif output_path and os.path.isdir(output_path):
        # If output_path is a directory, construct the file name
        output_file = os.path.join(output_path, f"{sanitized_title}_{resolution}.{file_type}")
    else:
        # Default to current directory with constructed file name
        output_file = f"{sanitized_title}_{resolution}.{file_type}"

    try:
        # Check the file size on the server
        with requests.head(download_url, timeout=10) as head_response:
            head_response.raise_for_status()
            total_size = int(head_response.headers.get('content-length', 0))
            logger.info(f"Server-reported size: {total_size} bytes")

        # Get already downloaded file size
        downloaded_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        # If the file already exists and is complete, skip downloading
        if downloaded_size == total_size:
            logger.info(f"File {output_file} already exists and is complete. Skipping download.")
            return 9  # specific exit code to indicate that the file already exists and is complete

        # Ensure the existing file size matches the expected range
        if downloaded_size > 0:
            headers = {"Range": f"bytes={downloaded_size}-"}
        else:
            headers = {}

        # Start downloading
        with requests.get(download_url, headers=headers, stream=True, timeout=10) as response:
            response.raise_for_status()

            # Validate server's response for Range request
            content_range = response.headers.get('Content-Range')
            if downloaded_size > 0 and not content_range:
                logger.warning("Server does not support resuming downloads. Restarting download...")
                os.remove(output_file)
                downloaded_size = 0

            with open(output_file, 'ab') as f, tqdm(
                total=total_size, 
                initial=downloaded_size, 
                unit='B', 
                unit_scale=True,
                unit_divisor=1024,
                desc=sanitized_title[:30] + "...",
                disable=args.silent  # disable progress bar if silent mode is enabled
            ) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
                    
                    # Check if termination signal was received
                    if terminate_flag:
                        logger.warning(f"Download interrupted by termination signal. Progress: {pbar.n}/{total_size} bytes.")
                        return 1  # user interruption

        logger.info(f"\nDownload completed: {output_file}")
        if os.path.getsize(output_file) != total_size:
            logger.error(f"Warning: File size mismatch. Expected: {total_size}, Got: {os.path.getsize(output_file)}")
            return 2  # file size mismatch
        return 0  # successful completion

    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed: {e}")
        return 3  # download failure

    except KeyboardInterrupt:
        logger.warning(f"\nDownload interrupted by user. Progress: {pbar.n}/{total_size} bytes.")
        return 1  # user interruption

def setup_logging(silent_mode):
    # ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    handlers = [logging.FileHandler(LOG_FILE, encoding='utf-8')]
    if not silent_mode:
        handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [Thread-%(thread)d] - %(levelname)s - %(message)s',
        handlers=handlers
    )
    return logging.getLogger(__name__)

# Main script
if __name__ == "__main__":
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
        parser.add_argument("--silent", action="store_true", help="Run in silent mode (log to file only)")
        args = parser.parse_args()

        # Set up logging
        logger = setup_logging(args.silent)
        
        # Use the parsed arguments
        max_retries = args.max_retries
        wait_time = args.wait_time
        conversion_wait_time = args.conversion_wait

        # Get the video URL
        video_url = args.video_url
        preferred_resolution = args.resolution
        output_path = args.output
        
        logger.info(f"Analyzing video URL: {video_url}")
        html_fragment = analyze_video(video_url)
        logger.info("Analysis complete")

        logger.info("Fetching the resolution information")    
        div_section = extract_outermost_div_and_script(html_fragment)
        logger.info("Resolution information fetched")

        if div_section:
            logger.info("Fetching download information")
            download_info = parse_div_section_ex(div_section, preferred_resolution, args.auto_select)
            logger.info("Download information fetched")

            if download_info:
                logger.info("Parsing download URL")
                download_url = get_download_url(download_info, max_retries, wait_time, conversion_wait_time)
                logger.info("Download URL parsed")

                if download_url:
                    logger.info("Downloading the video...")
                    success = download_video(download_url, download_info["title"], 
                                          download_info["note"], download_info["ext"], 
                                          output_path)
                    if success == 0:
                        sys.exit(0)  # successful completion
                    elif success == 2:
                        sys.exit(2)  # file size mismatch
                    else:
                        sys.exit(success)  # download failure
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
