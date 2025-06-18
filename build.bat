@echo off
echo 🖥️ Building Genie- Commit Review for Windows...

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ app.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Install requirements if not already installed
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Generate the spec file using Python
echo Generating PyInstaller spec file...
python generate_spec.py

REM Build the executable
echo Building Windows executable...
pyinstaller --clean genie-commit-review.spec
if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build complete!
echo The executable can be found at dist\GenieCommitReview.exe
echo.
echo 🚀 To distribute:
echo    • Copy the entire dist folder for distribution
echo    • Or use the build_windows.py script for professional packaging
pause 