#!/bin/bash

# This script helps in packaging the BoB YouTube Video Downloader as an executable.
<<<<<<< HEAD
# It uses PyInstaller to create executables for Windows and macOS.

# Ensure Python and PyInstaller are installed on your system.
# You can install PyInstaller using:
# pip install pyinstaller

# Create a directory for build output
mkdir -p dist

# Windows packaging (cross-compilation on Linux/macOS is not straightforward, better to use a Windows machine for this)
function build_windows_exe {
    echo "Building Windows executable..."
    pyinstaller --onefile --name "BoBDownloader_win" BoBDownloader.py
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
    pyinstaller --onefile --name "BoBDownloader_mac" BoBDownloader.py
    if [ $? -eq 0 ]; then
        echo "macOS executable created successfully."
        mv dist/BoBDownloader_mac dist/
=======
# It first creates/uses a clean virtual environment so that only necessary packages
# are installed, which helps reduce the final executable size.
#
# Usage: ./build.sh [macos|linux]

envName="clean_env"
distDir="dist"
scriptName="BoBDownloader.py"

if [ ! -d "$envName" ]; then
    echo "Creating a new virtual environment..."
    python3 -m venv "$envName"
fi

echo "Activating virtual environment..."
# 激活虚拟环境（Linux/macOS方式）
source "$envName/bin/activate"

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing required packages in the virtual environment..."
pip install pyinstaller requests beautifulsoup4 tqdm

mkdir -p "$distDir"

function build_macos_exec {
    echo "Building macOS executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_mac" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "macOS executable created successfully."
        mv -f "dist/BoBDownloader_mac" "$distDir/"
>>>>>>> master
    else
        echo "Failed to build macOS executable."
    fi
}

<<<<<<< HEAD
# Linux packaging
function build_linux_exec {
    echo "Building Linux executable..."
    pyinstaller --onefile --name "BoBDownloader_linux" BoBDownloader.py
    if [ $? -eq 0 ]; then
        echo "Linux executable created successfully."
        mv dist/BoBDownloader_linux dist/
=======
function build_linux_exec {
    echo "Building Linux executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_linux" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "Linux executable created successfully."
        mv -f "dist/BoBDownloader_linux" "$distDir/"
>>>>>>> master
    else
        echo "Failed to build Linux executable."
    fi
}

<<<<<<< HEAD
# Check arguments to decide the build target
if [ "$1" == "windows" ]; then
    build_windows_exe
elif [ "$1" == "macos" ]; then
=======
if [ "$1" == "macos" ]; then
>>>>>>> master
    build_macos_exec
elif [ "$1" == "linux" ]; then
    build_linux_exec
else
<<<<<<< HEAD
    echo "Usage: $0 [windows|macos|linux]"
    echo "Specify 'windows' to build for Windows, 'macos' to build for macOS, or 'linux' to build for Linux."
fi
=======
    echo "Usage: $0 [macos|linux]"
    echo "Specify build target for 'macos' for macOS, or 'linux' for Linux."
fi

echo "Packaging complete."

deactivate
>>>>>>> master
