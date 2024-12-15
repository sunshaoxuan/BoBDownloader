# PowerShell Script to Package BoB YouTube Video Downloader
# This script uses PyInstaller to create an executable for Windows.
# Ensure that Python and PyInstaller are installed on your system.
# Check if PyInstaller is installed
# PowerShell Script to Package BoB YouTube Video Downloader using a clean virtual environment

$envName = "clean_env"
$distDir = "dist"
$outputName = "BoBDownloader_win.exe"
$scriptName = "BoBDownloader.py"

if (-not (Test-Path -Path $envName)) {
    Write-Output "Creating a new virtual environment..."
    python -m venv $envName
}

Write-Output "Activating virtual environment..."
. ".\$envName\Scripts\Activate.ps1"

Write-Output "Upgrading pip..."
python -m pip install --upgrade pip

Write-Output "Installing required packages in the virtual environment..."
pip install pyinstaller requests beautifulsoup4 tqdm

if (-not (Test-Path -Path $distDir)) {
    New-Item -ItemType Directory -Path $distDir | Out-Null
}

Write-Output "Building Windows executable..."
pyinstaller --onefile --clean --name "BoBDownloader_win" $scriptName

if ($LASTEXITCODE -eq 0) {
    Write-Output "Windows executable created successfully."
    Move-Item -Path ".\dist\BoBDownloader_win.exe" -Destination ".\dist\$outputName" -Force
} else {
    Write-Output "Failed to build Windows executable."
}

Write-Output "Packaging complete."

Deactivate
