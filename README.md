# Genie GitHooks

## Overview
Genie GitHooks is a tool designed to streamline your Git workflow by automating hook management. This guide provides step-by-step instructions to install and uninstall Genie GitHooks on both Windows and Ubuntu.

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
    2. Enter: `https://genie.bilvantis.in/fastapi`
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
    _"Git hooks installed successfully."_
  - Click **OK** to finish the installation

## Uninstallation Guide
To uninstall Genie GitHooks, follow steps 2–6 above. When the application detects an existing installation, a popup will appear stating:  
_"Git hooks are already installed. Would you like to uninstall them?"_

- Click **Yes** to proceed with the uninstallation
- You will receive a confirmation message once uninstallation is complete

## Support
For any issues or inquiries, please contact support at [support@bilvantis.in](mailto:support@bilvantis.in).

---
**Version:** 0.0.1  
**Developed by:** Bilvantis

