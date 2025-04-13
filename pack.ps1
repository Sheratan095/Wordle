# Define venv path
$venvPath = "kivy_env"
$venvPython = "$venvPath\Scripts\python.exe"

# Step 1: Create virtual environment if it doesn't exist
if (-Not (Test-Path $venvPath))
{
	Write-Host "📦 Creating virtual environment..."
	python -m venv $venvPath

	if (-Not (Test-Path $venvPython))
	{
		Write-Error "❌ Failed to create virtual environment!"
		exit 1
	}

	Write-Host "☁️ Installing Kivy and pyInstaller into virtual environment..."
	& $venvPython -m pip install --upgrade pip
	& $venvPython -m pip install kivy pyinstaller
}
else
{
	Write-Host "✅ Virtual environment already exists."
}

# Step 3: Run PyInstaller
Write-Host "🚀 Building project with PyInstaller..."
& $venvPython -m PyInstaller `
  --icon "assets/icon.ico" `
  --onedir `
  --noconfirm `
  --windowed `
  source/Wordle.py

# Step 4: Copy resources to output folder
$distPath = "dist/Wordle"

if (-Not (Test-Path $distPath))
{
	Write-Error "❌ Build failed: $distPath does not exist."
	exit 1
}

Write-Host "📁 Copying extra files..."
Copy-Item -Path "config.json" -Destination $distPath -Force
Copy-Item -Path "assets" -Destination $distPath -Recurse -Force
Copy-Item -Path "vocabularies" -Destination $distPath -Recurse -Force

Write-Host "`n✅ Build complete! Executable and files ready in $distPath"
