# BoB YouTube Video Downloader

A Python script for downloading YouTube videos by extracting available resolutions and allowing the user to select the preferred resolution for download. The script uses web scraping techniques to interact with a third-party YouTube video analysis service and simulate download actions.

<<<<<<< HEAD
=======
---

>>>>>>> master
## Features

- Extract video metadata from a YouTube link, including available resolutions and file sizes.
- Allows the user to choose from available resolutions before downloading or specify a preferred resolution as a command-line argument.
- Downloads the selected video resolution with proper filename sanitization to prevent issues with file saving.
- Command-line support for easy usage, with options for specifying a preferred resolution and output filename or directory.
<<<<<<< HEAD
- Encrypted URL management for enhanced security.
- Detailed download progress with human-readable file sizes, estimated download time remaining, and download speed.
- Cross-platform support for packaging into executables (Windows, macOS, and Linux).

## What's New in v1.0.2

- **Code Structure Simplification**: Removed the need for external `.config` and `secret.key` files by embedding the encrypted data directly in the script. This change reduces the complexity of file management and improves ease of deployment.
- **Estimated Download Time**: Added download speed calculation and estimated remaining time during the video download, providing a more informative download progress experience.
- **Enhanced Download Progress**: Improved download progress updates to include details such as download speed, percentage completion, and estimated time left.
- **Error Handling Improvements**: Added better error handling across various functions to enhance the robustness and reliability of the script.
=======
- **Encrypted URL management** for enhanced security.
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
>>>>>>> master

## Requirements

- Python 3.x
<<<<<<< HEAD
- `requests` library: for making HTTP requests to the analysis service.
- `beautifulsoup4` library: for parsing the HTML content.
- `cryptography` library: for handling encrypted URLs.

## Installation

1. **Install Python**

   - Ensure that you have Python 3 installed on your system. You can check by running the following command in your terminal or command prompt:

     ```sh
     python3 --version
     ```

   - If Python 3 is not installed, you can download it from [Python's official website](https://www.python.org/downloads/).

2. **Install Dependencies**

   - You will need the `requests`, `beautifulsoup4`, and `cryptography` packages. You can install these packages via pip:
     ```sh
     pip3 install requests beautifulsoup4 cryptography
     ```

## Usage

1. **Clone or Download the Repository**

   - Clone this repository or download it as a ZIP file, then navigate to the folder containing the script.

=======
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

>>>>>>> master
   ```sh
   git clone https://github.com/sunshaoxuan/BoBDownloader.git
   cd BoBDownloader
   ```

2. **Run the Script**

<<<<<<< HEAD
   - The script can be executed using the command line by passing the YouTube video URL as an argument. You can also specify a preferred resolution using the `--resolution` flag and an output path using the `--output` flag:

     ```sh
     python3 down.py "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p --output "path/to/output/file.mp4"
     ```

   - If you do not pass the video URL, the script will prompt you to provide a valid URL.

3. **Select Video Resolution**

   - After running the script, it will present you with a list of available resolutions and their respective file sizes if no preferred resolution is specified. Enter the number corresponding to the desired resolution to start the download.

## Example

```sh
$ python3 down.py "https://www.youtube.com/watch?v=gV5rQFCgCjA" --resolution 720p

Analyzing video URL: https://www.youtube.com/watch?v=gV5rQFCgCjA...
Fetching the resolution information...
Fetching download information...
Parsing download URL...
Downloading the video...
File name: video_title_720p.mp4
Downloaded 22.62 MB of 22.62 MB (100.00%) at 2.2 MB/s, ETA: 0.00s
Download completed: video_title_720p.mp4
```

## Packaging

To make the downloader available as an executable, you can use the provided packaging scripts.

### Windows Packaging

1. **Use PowerShell Script**

   - There is a PowerShell script (`build.ps1`) provided for packaging the downloader into a Windows executable.
   - Run the following command in PowerShell:

     ```powershell
     .\build.ps1
     ```

   - This will create an executable file named `BoBDownloader_win.exe` in the `release` folder.

### macOS and Linux Packaging

1. **Use Bash Script**

   - There is a bash script (`build.sh`) provided for packaging the downloader into executables for Windows, macOS, or Linux.
   - Run the following command in your terminal:

     ```sh
     ./build.sh [windows|macos|linux]
     ```

   - Replace `[windows|macos|linux]` with your desired target platform.
   - The executable will be created in the `release` folder with the appropriate name for the platform.

## Script Overview

- **`analyze_video(video_url)`**: Sends a POST request to an external analysis service to extract information about available resolutions and formats for the provided video URL.
- **`extract_outermost_div_and_script(html_content)`**: Extracts the main `<div>` tag containing video information from the returned HTML content.
- **`parse_div_section_ex(div_content, preferred_resolution)`**: Parses the `<div>` content to extract information on available resolutions, presents them for the user to choose from, or selects the preferred resolution if specified.
- **`get_download_url(download_info)`**: Sends a POST request to retrieve the actual download URL for the video.
- **`download_video(download_url, title, resolution, file_type, output_path)`**: Downloads the video from the generated download URL and provides real-time progress updates.
- **`sanitize_filename(filename)`**: Sanitizes filenames to remove illegal characters for cross-platform compatibility.
- **`load_encrypted_url()`** and **`load_encrypted_service_url()`**: Load and decrypt the base URLs for requesting download information and service analysis.

## Requirements and Notes

- **Network Access**: The script needs access to the internet as it relies on an external service to analyze and download videos.
- **Compatibility**: This script should work on macOS, Linux, and Windows, provided Python 3 and the necessary libraries are installed.
- **Disclaimer**: This script utilizes a third-party YouTube analysis service. Make sure to comply with YouTube's Terms of Service before using this tool.

## Troubleshooting

- **Missing Dependencies**: Ensure all required Python packages (`requests`, `beautifulsoup4`, `cryptography`) are installed. Use the following command to install missing dependencies:

  ```sh
  pip3 install requests beautifulsoup4 cryptography
  ```

- **FileNotFoundError**: When saving the video, if the script reports a `FileNotFoundError`, it could be due to illegal characters in the filename. The script sanitizes filenames, but if this issue persists, manually modify the video title to remove any unusual characters.

- **Connection Errors**: If you encounter connection errors, check your internet connection and ensure that the external service used for analyzing videos is reachable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! If you have any suggestions or improvements, feel free to fork the repository and submit a pull request.

## Contact

For any questions or issues, please open an issue on the GitHub repository, or contact me via [sunsx@sina.com](mailto:sunsx@sina.com).

---

**Disclaimer**: This script is for educational purposes only. Downloading videos from YouTube may violate YouTube's terms of service. Please ensure that you have permission to download any content and do not use this script for unauthorized purposes.
=======
   ```sh
   python down.py "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p --output "path/to/output/file.mp4"
   ```

3. **Packaging (Optional)**

   - Use the provided `build.ps1` or `build.sh` scripts to create executables for Windows, macOS, or Linux.

---

## Usage

```sh
python down.py "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p --auto-select --output "path/to/output/file.mp4"
```

### Command-Line Arguments

- `video_url` (Required): URL of the YouTube video.
- `--resolution` (Optional): Specify the preferred resolution (default: `720p`).
- `--auto-select` (Optional): Automatically choose an alternative resolution if the preferred one is unavailable.
- `--output` (Optional): Specify the output file path or directory. Defaults to the current directory.

### Example

```sh
$ python3 down.py "https://www.youtube.com/watch?v=gV5rQFCgCjA" --resolution 720p --auto-select

Fetching resolution information...
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
>>>>>>> master
