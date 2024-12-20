#!/bin/bash

# This script helps in packaging the BoB YouTube Video Downloader as an executable.
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
    else
        echo "Failed to build macOS executable."
    fi
}

function build_linux_exec {
    echo "Building Linux executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_linux" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "Linux executable created successfully."
        mv -f "dist/BoBDownloader_linux" "$distDir/"
    else
        echo "Failed to build Linux executable."
    fi
}

if [ "$1" == "macos" ]; then
    build_macos_exec
elif [ "$1" == "linux" ]; then
    build_linux_exec
else
    echo "Usage: $0 [macos|linux]"
    echo "Specify build target for 'macos' for macOS, or 'linux' for Linux."
fi

echo "Packaging complete."

deactivate
