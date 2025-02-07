import os,sys
import shutil
import requests
import subprocess
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QMessageBox
)
import traceback

# Now use HOOKS_DIR instead of "hooks/" in your installation logic

class BackendURLWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Enter Backend URL")
        self.setGeometry(100, 100, 400, 100)
        
        layout = QFormLayout()
        
        self.backend_url = QLineEdit()
        self.backend_url.setPlaceholderText("Enter backend URL")
        self.check_button = QPushButton("Check URL")
        self.check_button.clicked.connect(self.handle_check_url)
        
        layout.addRow(QLabel("Backend URL:"), self.backend_url)
        layout.addRow(self.check_button)
        
        self.setLayout(layout)

    def handle_check_url(self):
        backend_url = self.backend_url.text()
        
        if not backend_url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return
        
        # Make the GET request to the backend URL
        try:
            touch_api = f"{backend_url}/touch"
            response = requests.get(touch_api)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Backend is reachable. Proceeding to login.")
                self.login_window.set_backend_url(backend_url)  # Pass the backend URL to login window
                self.login_window.show()
                self.close()  # Close the backend URL window
            else:
                QMessageBox.critical(self, "Error", f"Failed to reach backend. Status Code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error connecting to the backend: {e}")

import os
import subprocess
import requests
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QFormLayout, QLabel, QMessageBox
import traceback
import logging

# Set up the logger to print logs to the console
logging.basicConfig(
    level=logging.DEBUG,  # Minimum level of logs to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[logging.StreamHandler()]  # This will print logs to the console
)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.backend_url = None  # Initialize the backend URL variable
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 100)
        
        layout = QFormLayout()
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter your email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        
        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.open_register_window)
        
        layout.addRow(QLabel("Email:"), self.email)
        layout.addRow(QLabel("Password:"), self.password)
        layout.addRow(self.login_button)
        layout.addRow(self.register_button)
        
        self.setLayout(layout)

    def set_backend_url(self, backend_url):
        """Sets the backend URL dynamically"""
        self.backend_url = backend_url
        
    def handle_login(self):
        username = self.email.text()
        password = self.password.text()
        
        user_id = self.authenticate_user(username, password)
        
        if user_id:
            self.user_id = user_id
            self.manage_git_hooks(user_id)
            self.close()  # Close the login window after successful login
        else:
            # Show retry option on login failure
            retry_reply = QMessageBox.question(self, "Login Failed", "Login failed. Do you want to retry?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if retry_reply == QMessageBox.StandardButton.No:
                self.close()  # Close the login window if the user chooses not to retry

    def authenticate_user(self, username, password):
        try:
            payload = {'username': username, 'email': username, 'password': password}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            login_url = f"{self.backend_url}/auth/login"  # Use the user-defined base URL here
            response = requests.post(login_url, data=payload)
            data = response.json()

            if "access_token" not in data:
                QMessageBox.warning(self, "Login Failed", "Invalid Credentials")
                logging.warning(f"Failed login attempt for username: {username}")
                return None  # Return None if authentication fails

            jwt_token = data["access_token"]
            headers = {"Authorization": f"Bearer {jwt_token}"}
            
            user_url = f"{self.backend_url}/auth/users/me"  # Use the user-defined base URL here
            user_response = requests.get(user_url, headers=headers)
            user_data = user_response.json()
            
            if "id" not in user_data:
                QMessageBox.critical(self, "Error", "Failed to fetch user details")
                logging.error("Failed to fetch user details after authentication.")
                return None  # Return None if unable to fetch user details

            return user_data["id"]  # Return the user ID if successful
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error during authentication: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Request error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during authentication: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
            return None

    def manage_git_hooks(self, user_id):
        try:
            GIT_HOOKS_DIR = self.get_or_set_global_git_hooks_dir()
            if not GIT_HOOKS_DIR:
                QMessageBox.critical(self, "Error", "Git hooks directory not set. Aborting installation.")
                logging.error("Git hooks directory not set. Aborting installation.")
                return

            hooks_exist = os.path.exists(os.path.join(GIT_HOOKS_DIR, "pre-commit"))
            
            if hooks_exist:
                reply = QMessageBox.question(self, "Git Hooks Found", "Git hooks are already installed. Do you want to uninstall them?", 
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.uninstall_hooks(GIT_HOOKS_DIR)
            else:
                self.install_hooks()
        except Exception as e:
            logging.error(f"Error managing Git hooks: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error managing Git hooks: {e}")

    def install_hooks(self):
        """ Installs Git Hooks after successful login """
        try:
            git_hooks_dir = self.get_or_set_global_git_hooks_dir()
            if not git_hooks_dir:
                self.show_error_message("Error", "Git hooks directory not set. Aborting installation.")
                return

            # Ensure the hooks directory exists
            os.makedirs(git_hooks_dir, exist_ok=True)

            # Set the paths for the pre-commit and post-commit hook files
            pre_commit_path = os.path.join(git_hooks_dir, "pre-commit")
            post_commit_path = os.path.join(git_hooks_dir, "post-commit")

            # Define the shell script file path
            pre_commit_source = "hooks/pre-commit"
            post_commit_source = "hooks/post-commit"

            # Replace BASE_URL dynamically in the shell script (if exists)
            if os.path.exists(pre_commit_source):
                with open(pre_commit_source, "r") as file:
                    pre_commit_content = file.read()
                with open(post_commit_source, "r") as file:
                    post_commit_content = file.read()

                # Replace $BASE_URL with a specific value
                pre_commit_content = pre_commit_content.replace("${BASE_API}",self.backend_url).replace("${userId}",self.user_id)
                post_commit_content = post_commit_content.replace("${BASE_API}",self.backend_url).replace("${userId}",self.user_id)
                
                # Write the modified script to the pre-commit hook
                with open(pre_commit_path, "w") as pre_commit_file:
                    pre_commit_file.write(pre_commit_content)

                with open(post_commit_path, "w") as post_commit_file:
                    post_commit_file.write(post_commit_content)

                # Ensure both hooks are executable
                os.chmod(pre_commit_path, 0o755)
                os.chmod(post_commit_path, 0o755)

                self.show_info_message("Success", "Git hooks installed successfully!")
                logging.info("Git hooks installed successfully!")

        except Exception as e:
            logging.error(f"Error installing Git hooks: {e}")
            traceback.print_exc()
            self.show_error_message("Error", f"Failed to install git hooks: {str(e)}")

    def show_info_message(self, title, message):
        """ Display an info message """
        QMessageBox.information(None, title, message)

    def show_error_message(self, title, message):
        """ Display an error message """
        QMessageBox.critical(None, title, message)

    def uninstall_hooks(self, hooks_dir):
        try:
            os.remove(os.path.join(hooks_dir, "pre-commit"))
            QMessageBox.information(self, "Success", "Git hooks uninstalled successfully!")
            logging.info("Git hooks uninstalled successfully!")
        except Exception as e:
            logging.error(f"Error uninstalling Git hooks: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to uninstall hooks: {e}")
    
    def get_or_set_global_git_hooks_dir(self):
        try:
            # Attempt to get the current global git hooks directory
            hooks_path = subprocess.check_output(['git', 'config', '--global', '--get', 'core.hooksPath']).strip()
            if hooks_path:
                return hooks_path.decode('utf-8')
        except subprocess.CalledProcessError:
            # If there is no global git hooks path set, we continue
            pass
        except Exception as e:
            logging.error(f"Error checking global git hooks path: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error while checking global Git hooks: {e}")
            return None

        # Define the default hooks path
        default_hooks_path = os.path.expanduser("~/.git_hooks")

        # Ask user if they want to set the global Git hooks path
        reply = QMessageBox.question(self, "Set Global Git Hooks", 
                                    f"Global Git hooks are not set. Set them to {default_hooks_path}?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Attempt to set the global git hooks path
                subprocess.run(['git', 'config', '--global', 'core.hooksPath', default_hooks_path], check=True)
                # Create the default hooks directory if it doesn't exist
                os.makedirs(default_hooks_path, exist_ok=True)
                return default_hooks_path
            except subprocess.CalledProcessError as e:
                logging.error(f"Git config error while setting global hooks: {e}")
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Failed to set global hooks: {e}")
                return None
            except PermissionError as e:
                logging.error(f"Permission error while setting global hooks: {e}")
                traceback.print_exc()
                QMessageBox.critical(self, "Permission Denied", f"Permission error while setting hooks path: {e}")
                return None
            except OSError as e:
                logging.error(f"OS error while setting global hooks: {e}")
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Error while creating the hooks directory: {e}")
                return None
            except Exception as e:
                logging.error(f"Unexpected error while setting global hooks: {e}")
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
                return None
        else:
            # User declined to set the global hooks path
            return None

    def open_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.close()

class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QFormLayout()
        
        self.fullname = QLineEdit()
        self.email = QLineEdit()
        self.username = QLineEdit()
        self.company_name = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)
        
        self.back_button = QPushButton("Back to Login")
        self.back_button.clicked.connect(self.go_back_to_login)

        layout.addRow(QLabel("Full Name:"), self.fullname)
        layout.addRow(QLabel("Email:"), self.email)
        layout.addRow(QLabel("Company Name:"), self.company_name)
        layout.addRow(QLabel("Password:"), self.password)
        layout.addRow(QLabel("Confirm Password:"), self.confirm_password)
        layout.addRow(self.register_button)
        layout.addRow(self.back_button)
        
        self.setLayout(layout)
    
    def handle_register(self):
        fullname = self.fullname.text()
        email = self.email.text()
        company_name = self.company_name.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if not all([fullname, email, company_name, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match!")
            return
        
        payload = {
            "email": email,
            "full_name": fullname,
            "password": password,
            "confirm_password": confirm_password,
            "username": email,
            "company_name": company_name
        }
        
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(REGISTER_API, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Registration successful! Please log in.")
                self.login_window.show()
                self.close()
            else:
                retry_reply = QMessageBox.question(self, "Registration Failed", f"Registration failed: {data.get('detail', 'Unknown error')}. Do you want to retry?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if retry_reply == QMessageBox.StandardButton.No:
                    self.close()  # Close the register window if user chooses not to retry
        except Exception as e:
            retry_reply = QMessageBox.question(self, "API Error", f"API Error: {e}. Do you want to retry?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if retry_reply == QMessageBox.StandardButton.No:
                self.close()  # Close the register window if user chooses not to retry

    def go_back_to_login(self):
        """Handles the Back button action."""
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize and show BackendURLWindow first
    login_window = LoginWindow()
    backend_window = BackendURLWindow(login_window)
    backend_window.show()

    sys.exit(app.exec())