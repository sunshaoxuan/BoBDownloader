# BoB YouTube Video Downloader

A Python script for downloading YouTube videos by extracting available resolutions and allowing the user to select the preferred resolution for download. The script uses encrypted URLs for secure communication and enhanced web scraping techniques for parsing video information.

---

## Features

- Extract video metadata from a YouTube link, including available resolutions and file sizes.
- Allows the user to choose from available resolutions before downloading or specify a preferred resolution as a command-line argument.
- Downloads the selected video resolution with proper filename sanitization to prevent issues with file saving.
- Command-line support for easy usage, with options for specifying a preferred resolution and output filename or directory.
- **Encrypted URL management** for secure communication.
- **Incomplete download resumption** with range header support.
- **Intelligent resolution selection:** Automatically selects an alternative resolution if the preferred one is unavailable.
- **Detailed error codes** for easier troubleshooting.
- Download progress bar with estimated time remaining and speed calculation.

---

## What's New in v1.1.0

### Download Enhancements

- **Resumable Downloads:** Downloads can now resume from incomplete files using range requests.
- **File Integrity Check:** Verifies downloaded file size against server-reported size to ensure completion.

### Video Analysis Improvements

- **Enhanced Resolution Selection:** Automatically selects the best available resolution if the preferred one is unavailable.
- **Improved Parsing:** Robust parsing for download options using updated web scraping logic.

### Error Handling and Debugging

- **Detailed Error Codes:** Improved exit codes for specific error scenarios (e.g., missing div section, file size mismatch).
- **Retry Logic:** Retries requests for unstable connections or temporary server issues.
- **Debugging Output:** Logs request details and server responses for troubleshooting.

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
- `--max-retries` (Optional): Maximum number of retries for download URL request (default: `5`).
- `--wait-time` (Optional): Wait time in seconds between retries (default: `10`).
- `--conversion-wait` (Optional): Wait time in seconds for 'convert_ready' status (default: `20`).

### Example

```sh
$ python3 BoBDownloader.py "https://www.youtube.com/watch?v=gV5rQFCgCjA" --resolution 720p --auto-select

Analyzing video URL: https://www.youtube.com/watch?v=gV5rQFCgCjA...
Analysis complete.
Fetching the resolution information...
Available resolutions:
1. MP3 (26.42 MB)
2. 720p (MP4) (294.65 MB)
3. 360p (MP4) (93.8 MB)
Select resolution by number: 2
Attempting to download from: https://example.com/download?id=example_download_id
[Video Title 720p]:  80%|███████████████████████████████     | 248M/309M [13:12<01:20, 1.25MB/s]
Download completed: video_title_720p.mp4
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
