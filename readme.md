# BoB YouTube Video Downloader

A Python script for downloading YouTube videos by extracting available resolutions and allowing the user to select the preferred resolution for download. The script uses web scraping techniques to interact with a third-party YouTube video analysis service and simulate download actions.

---

## Features

- Extract video metadata from a YouTube link, including available resolutions and file sizes.
- Allows the user to choose from available resolutions before downloading or specify a preferred resolution as a command-line argument.
- Downloads the selected video resolution with proper filename sanitization to prevent issues with file saving.
- Command-line support for easy usage, with options for specifying a preferred resolution and output filename or directory.
- **Encrypted URL management** for enhanced security.
- **Incomplete download resumption** with range header support.
- **Intelligent resolution selection:** Automatically selects an alternative resolution if the preferred one is unavailable.
- **Detailed error codes** for easier troubleshooting.
- **Signal handling for graceful termination**, ensuring clean exits when interrupted.
- **Advanced retry mechanisms** for download URL retrieval and conversions.
- Enhanced logging with both file and console outputs for better monitoring and debugging.

---

## What's New in v1.5.0

### Signal Handling and Graceful Exit

- Added signal handling to ensure the downloader exits gracefully when interrupted (e.g., `SIGTERM`, `Ctrl+C`).
- Improved robustness against interruptions during critical operations, such as downloading or waiting for conversion readiness.

### Enhanced Download Management

- Improved **resumable download** functionality with better error handling for incomplete files.
- Added verification for file size after download to ensure data integrity.

### Optimized Performance

- Improved retry logic for handling server-side conversion delays and busy statuses, ensuring a more reliable download process.
- Reduced redundant operations for faster execution and better resource usage.

### Expanded CLI Options

- New options for controlling retry behavior:
  - `--max-retries`: Set the maximum number of retries for download URL requests (default: 5).
  - `--wait-time`: Specify the wait time (in seconds) between retries (default: 10).
  - `--conversion-wait`: Set the wait time (in seconds) for `convert_ready` statuses (default: 20).

---

## Requirements

- Python 3.x
- Required Python libraries:
  - `requests`: for making HTTP requests to the analysis service.
  - `beautifulsoup4`: for parsing HTML content.
  - `cryptography`: for handling encrypted URLs.
  - `tqdm`: for showing download progress bars.

Install dependencies using pip:

```sh
pip install requests beautifulsoup4 cryptography tqdm
```

---

## Installation

1. **Clone or Download the Repository**

   ```sh
   git clone https://github.com/sunshaoxuan/BoBDownloader.git
   cd BoBDownloader
   ```

2. **Run the Script**

   ```sh
   python BoBDownloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p --output "path/to/output/file.mp4"
   ```

3. **Packaging (Optional)**

   - Use the provided `build.ps1` or `build.sh` scripts to create executables for Windows, macOS, or Linux.

---

## Usage

```sh
python BoBDownloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p --auto-select --output "path/to/output/file.mp4"
```

### Command-Line Arguments

- `video_url` (Required): URL of the YouTube video.
- `--resolution` (Optional): Specify the preferred resolution (default: `720p`).
- `--auto-select` (Optional): Automatically choose an alternative resolution if the preferred one is unavailable.
- `--output` (Optional): Specify the output file path or directory. Defaults to the current directory.
- `--max-retries` (Optional): Maximum retries for download URL request (default: 5).
- `--wait-time` (Optional): Wait time (in seconds) between retries (default: 10).
- `--conversion-wait` (Optional): Wait time (in seconds) for `convert_ready` status (default: 20).
- `--silent` (Optional): Suppress console output, logging only to a file.

### Example

```sh
$ python3 BoBDownloader.py "https://www.youtube.com/watch?v=gV5rQFCgCjA" --resolution 1080p --auto-select

Fetching resolution information...
Available resolutions:
1. MP3 (26.42 MB)
2. 1080p (MP4) (450.2 MB)
3. 720p (MP4) (294.65 MB)
4. 360p (MP4) (93.8 MB)
Select resolution by number: 2
Attempting to download from: https://example.com/download?id=example_download_id
[Video Title 1080p]:  80%|███████████████████████████████     | 360M/450M [13:12<01:20, 1.25MB/s]
Download completed: video_title_1080p.mp4
```

---

## Troubleshooting

- **Missing Dependencies:**

  ```sh
  pip install requests beautifulsoup4 cryptography tqdm
  ```

- **File Integrity Issues:**
  - Ensure the `tqdm` progress bar reaches 100%. If interrupted, rerun the script to resume the download.

- **Connection Errors:**
  - Check your network connection and retry.

- **Slow Download Speeds:**
  - Retry the script in a faster network environment.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Disclaimer:** This script is for educational purposes only. Ensure you have permission to download content and comply with YouTube's Terms of Service.

