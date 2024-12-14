#!/bin/bash

# This script helps in packaging the BoB YouTube Video Downloader as an executable.
# It first creates/uses a clean virtual environment so that only necessary packages
# are installed, which helps reduce the final executable size.
#
# Usage: ./build.sh [windows|macos|linux]

envName="clean_env"
distDir="dist"
scriptName="BoBDownloader.py"

# 创建并激活虚拟环境
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

# 创建 dist 目录（如果不存在）
mkdir -p "$distDir"

function build_windows_exe {
    echo "Building Windows executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_win" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "Windows executable created successfully."
        mv "dist/BoBDownloader_win.exe" "$distDir/"
    else
        echo "Failed to build Windows executable."
    fi
}

function build_macos_exec {
    echo "Building macOS executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_mac" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "macOS executable created successfully."
        mv "dist/BoBDownloader_mac" "$distDir/"
    else
        echo "Failed to build macOS executable."
    fi
}

function build_linux_exec {
    echo "Building Linux executable..."
    pyinstaller --onefile --clean --name "BoBDownloader_linux" "$scriptName"
    if [ $? -eq 0 ]; then
        echo "Linux executable created successfully."
        mv "dist/BoBDownloader_linux" "$distDir/"
    else
        echo "Failed to build Linux executable."
    fi
}

# 根据参数决定打包目标
if [ "$1" == "windows" ]; then
    build_windows_exe
elif [ "$1" == "macos" ]; then
    build_macos_exec
elif [ "$1" == "linux" ]; then
    build_linux_exec
else
    echo "Usage: $0 [windows|macos|linux]"
    echo "Specify 'windows' to build for Windows, 'macos' for macOS, or 'linux' for Linux."
fi

echo "Packaging complete."

# 注销虚拟环境
deactivate
