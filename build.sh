#!/bin/bash

# This script helps in packaging the BoB YouTube Video Downloader as an executable.
# It uses PyInstaller to create executables for Windows and macOS.

# Ensure Python and PyInstaller are installed on your system.
# You can install PyInstaller using:
# pip install pyinstaller

# Create a directory for build output
mkdir -p dist

# Windows packaging (cross-compilation on Linux/macOS is not straightforward, better to use a Windows machine for this)
function build_windows_exe {
    echo "Building Windows executable..."
    pyinstaller --onefile --name "BoBDownloader_win" down.py
    if [ $? -eq 0 ]; then
        echo "Windows executable created successfully."
        mv dist/BoBDownloader_win.exe dist/
    else
        echo "Failed to build Windows executable."
    fi
}

# macOS packaging
function build_macos_exec {
    echo "Building macOS executable..."
    pyinstaller --onefile --name "BoBDownloader_mac" down.py
    if [ $? -eq 0 ]; then
        echo "macOS executable created successfully."
        mv dist/BoBDownloader_mac dist/
    else
        echo "Failed to build macOS executable."
    fi
}

# Linux packaging
function build_linux_exec {
    echo "Building Linux executable..."
    pyinstaller --onefile --name "BoBDownloader_linux" down.py
    if [ $? -eq 0 ]; then
        echo "Linux executable created successfully."
        mv dist/BoBDownloader_linux dist/
    else
        echo "Failed to build Linux executable."
    fi
}

# Check arguments to decide the build target
if [ "$1" == "windows" ]; then
    build_windows_exe
elif [ "$1" == "macos" ]; then
    build_macos_exec
elif [ "$1" == "linux" ]; then
    build_linux_exec
else
    echo "Usage: $0 [windows|macos|linux]"
    echo "Specify 'windows' to build for Windows, 'macos' to build for macOS, or 'linux' to build for Linux."
fi
