# Activate virtual environment path to python.exe
$venvPython = "kivy_env\Scripts\python.exe"  # Use \Scripts\ on Windows

# Check if pyinstaller is installed
$pyInstallerInstalled = & $venvPython -m pip show pyinstaller 2>$null

if (-Not $pyInstallerInstalled) {
	Write-Host "🔧 Installing PyInstaller in virtual environment..."
	& $venvPython -m pip install pyinstaller
}
else {
	Write-Host "✅ PyInstaller already installed."
}

# Run PyInstaller from the virtual environment
& $venvPython -m PyInstaller `
  --icon assets/icon.ico `
  --onedir `
  --noconfirm `
  --hide-console=hide-early `
  source/Wordle.py

# Define output path
$distPath = "dist/Wordle"

# Ensure destination exists
if (-Not (Test-Path $distPath))
{
	Write-Error "Build failed: $distPath does not exist."
	exit 1
}

# Copy config.json
Copy-Item -Path "config.json" -Destination $distPath -Force

# Copy assets/ folder
Copy-Item -Path "assets" -Destination $distPath -Recurse -Force

# Copy vocabularies/ folder
Copy-Item -Path "vocabularies" -Destination $distPath -Recurse -Force

Write-Host "✅ Build complete! Files copied to $distPath"
