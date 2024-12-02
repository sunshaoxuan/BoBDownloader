# BoB YouTube Video Downloader

A Python script for downloading YouTube videos by extracting available resolutions and allowing the user to select the preferred resolution for download. The script uses web scraping techniques to interact with a third-party YouTube video analysis service and simulate download actions.

## Features

- Extract video metadata from a YouTube link, including available resolutions and file sizes.
- Allows the user to choose from available resolutions before downloading.
- Downloads the selected video resolution with proper filename sanitization to prevent issues with file saving.
- Command-line support for easy usage.

## Requirements

- Python 3.x
- `requests` library: for making HTTP requests to the analysis service.
- `beautifulsoup4` library: for parsing the HTML content.

## Installation

1. **Install Python**

   - Ensure that you have Python 3 installed on your system. You can check by running the following command in your terminal or command prompt:

     ```sh
     python3 --version
     ```

   - If Python 3 is not installed, you can download it from [Python's official website](https://www.python.org/downloads/).

2. **Install Dependencies**

   - You will need the `requests` and `beautifulsoup4` packages. You can install these packages via pip:
     ```sh
     pip3 install requests beautifulsoup4
     ```

## Usage

1. **Clone or Download the Repository**

   - Clone this repository or download it as a ZIP file, then navigate to the folder containing the script.

   ```sh
   git clone https://github.com/sunsx/youtube-video-downloader.git
   cd youtube-video-downloader
   ```

2. **Run the Script**

   - The script can be executed using the command line by passing the YouTube video URL as an argument:

     ```sh
     python3 down.py "https://www.youtube.com/watch?v=VIDEO_ID"
     ```

   - If you do not pass the video URL, the script will prompt you to provide a valid URL.

3. **Select Video Resolution**

   - After running the script, it will present you with a list of available resolutions and their respective file sizes. Enter the number corresponding to the desired resolution to start the download.

## Example

```sh
$ python3 down.py "https://www.youtube.com/watch?v=gV5rQFCgCjA"

Available Resolutions:
1. Resolution: 720p, Size: 22.62M
2. Resolution: 480p, Size: 15.43M
3. Resolution: 360p, Size: 10.12M

Enter the number corresponding to the resolution you wish to download: 1
Starting download: 720p...
Download completed: "video_title_720p.mp4"
```

## Script Overview

- **`analyze_video(video_url)`**: Sends a POST request to an external analysis service to extract information about available resolutions and formats for the provided video URL.
- **`extract_outermost_div_and_script(html_content)`**: Extracts the main `<div>` and `<script>` tags containing video information from the returned HTML content.
- **`parse_div_section(div_content)`**: Parses the `<div>` content to extract information on available resolutions and presents them for the user to choose from.
- **`get_download_url(download_info)`**: Sends a POST request to retrieve the actual download URL for the video.
- **`download_video(download_url, title, resolution, file_type)`**: Downloads the video from the generated download URL.
- **`sanitize_filename(filename)`**: Sanitizes filenames to remove illegal characters for cross-platform compatibility.

## Requirements and Notes

- **Network Access**: The script needs access to the internet as it relies on an external service to analyze and download videos.
- **Compatibility**: This script should work on macOS, Linux, and Windows, provided Python 3 and the necessary libraries are installed.
- **Disclaimer**: This script utilizes a third-party YouTube analysis service. Make sure to comply with YouTube's Terms of Service before using this tool.

## Troubleshooting

- **Missing Dependencies**: Ensure all required Python packages (`requests`, `beautifulsoup4`) are installed. Use the following command to install missing dependencies:

  ```sh
  pip3 install requests beautifulsoup4
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

