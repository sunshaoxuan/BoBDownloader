# PowerShell Script to Package BoB YouTube Video Downloader
# This script uses PyInstaller to create an executable for Windows.
# Ensure that Python and PyInstaller are installed on your system.

# Check if PyInstaller is installed
try {
    pip show pyinstaller | Out-Null
} catch {
    Write-Output "PyInstaller not found. Installing PyInstaller..."
    pip install pyinstaller
}

# Create dist directory if it doesn't exist
if (-not (Test-Path -Path "dist")) {
    New-Item -ItemType Directory -Path "dist"
}

# Package the Python script into a Windows executable
Write-Output "Building Windows executable..."
pyinstaller --onefile --name "BoBDownloader_win" BoBDownloader.py

if ($LASTEXITCODE -eq 0) {
    Write-Output "Windows executable created successfully."
    Move-Item -Path ".\dist\BoBDownloader_win.exe" -Destination ".\dist\"
} else {
    Write-Output "Failed to build Windows executable."
}

Write-Output "Packaging complete."
