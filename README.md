# Genie GitHooks

## Overview
Genie GitHooks is a tool designed to streamline your Git workflow by providing automated code review before commits. The tool analyzes your code changes and provides comprehensive feedback in an easy-to-read HTML report that opens in your default browser. This guide provides step-by-step instructions to install and uninstall Genie GitHooks on both Windows and Ubuntu.

## Installation Guide

### Prerequisites
- **Python** Python 3.9 or later
- **Windows**: Windows OS (64-bit) 
- **Ubuntu**: Ubuntu 20.04 or later
- Internet connection
- Git installed on your system

### Steps to Install

#### **Windows Installation**
1. **Download the Application**  
   - [Download Genie-githooks_Win64_0.0.1.zip](./distribution/windows/Genie-githooks_Win64_0.0.1.zip)
   - Extract the contents of the ZIP file

2. **Navigate to the Application Directory**  
   - Open the extracted folder and go to the `app.dist` directory

3. **Run the Application**  
   - Open a terminal in the `app.dist` directory
   - Execute the following command:  
     ```sh
     app.exe
     ```

#### **Ubuntu Installation**
1. **Download the Application**  
   - [Download Genie-githooks_Ubuntu_0.0.1.zip](./distribution/ubuntu/Genie-githooks_Ubuntu_0.0.1.zip)
   - Extract the contents using the command:  
     ```sh
     unzip Genie-githooks_Ubuntu_0.0.1.zip
     ```

2. **Navigate to the Application Directory**  
   - Change directory to the extracted folder:  
     ```sh
     cd Genie-githooks_Ubuntu_0.0.1
     ```

3. **Run the Application**  
   - Grant execution permissions:  
     ```sh
     chmod +x app.bin
     ```
   - Execute the application:  
     ```sh
     ./app.bin
     ```

4. **Configure Backend URL**
    1. A popup will appear requesting the backend URL
    2. Enter: `http://localhost:3000/genieapi`
    3. Click the **Check URL** button

5. **Verify Backend Connection**

    If the connection is successful, you will see a message:  
      _"Backend is reachable. Proceeding to login."_
    - Click **OK**

6. **Login or Register**
  - A login popup will appear
  - Enter your credentials
  - If you do not have an account, click **Register** and follow the steps to create one

### Confirm Installation
  - After logging in, you will receive a confirmation message:  
    _"Git hooks installed successfully! Code review will now happen before each commit."_
  - Click **OK** to finish the installation

## How It Works
Once installed, Genie GitHooks will automatically:
1. **Intercept your commits**: When you run `git commit`, the tool will analyze your staged changes
2. **Send code for review**: Your git diff is sent to the backend for comprehensive analysis
3. **Generate review report**: A detailed HTML report is generated with:
   - Code quality assessment
   - Issue identification and explanations
   - Suggested fixes and improvements
   - Severity ratings for identified problems
4. **Open in browser**: The review report automatically opens in your default web browser
5. **Complete commit**: After review, your commit proceeds normally

The review happens in real-time and provides immediate feedback on your code quality before it's committed to your repository.

## Uninstallation Guide
To uninstall Genie GitHooks, follow steps 2–6 above. When the application detects an existing installation, a popup will appear stating:  
_"Git hooks for code review are already installed. Do you want to uninstall them?"_

- Click **Yes** to proceed with the uninstallation
- You will receive a confirmation message: _"Git code review hooks uninstalled successfully!"_

## Building Executables

### For Developers
To create platform-specific executables, use the build script:

#### Prerequisites
- Python 3.9 or later
- Git installed and in PATH

#### Build Commands

**For all platforms:**
```bash
# Install build dependencies
pip install pyinstaller

# Build executable for current platform
python build_executable.py
```

**For macOS specifically:**
```bash
# Quick build (recommended)
./build-mac.sh

# Or use the Python script directly
python3 build_mac.py
```

**For Windows specifically:**
```cmd
REM Quick build (recommended)
build-windows.bat

REM Or use the Python script directly
python build_windows.py
```

#### Supported Platforms
- **Windows**: Creates `.exe` executable with optional NSIS installer and shell hook scripts (via Git Bash)
- **macOS**: Creates `.app` bundle with DMG installer and shell hook scripts  
- **Linux**: Creates binary executable with shell hook scripts

#### Cross-Platform Features
- ✅ **Native UI**: PySide6 provides native look and feel on all platforms
- ✅ **Universal shell scripts**: Uses same shell scripts on all platforms (Git Bash handles Windows execution)
- ✅ **Automatic path handling**: Correctly handles file paths and directory structures
- ✅ **Git integration**: Works with Git installations on all platforms

#### Optional Build Tools

**For Windows builds:**
- [NSIS (Nullsoft Scriptable Install System)](https://nsis.sourceforge.io/) - Creates professional Windows installers with uninstall support
- Windows SDK - Provides SignTool for code signing executables
- Code signing certificate (.pfx file) - For distributing signed executables

**For macOS builds:**
- Xcode command line tools - For code signing: `xcode-select --install`
- Code signing certificate - Apple Developer certificate for distribution

## Support
For any issues or inquiries, please contact support at [support@bilvantis.in](mailto:support@bilvantis.in).

---
**Version:** 2.0.0  
**Developed by:** Bilvantis

# Test change
