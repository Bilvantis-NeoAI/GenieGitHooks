import os
import sys
import shutil
import requests
import subprocess
import traceback
import logging
import platform
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QFormLayout, QMessageBox, QProgressBar, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Helper function for subprocess calls to prevent terminal windows
def run_subprocess(cmd, **kwargs):
    """Run a subprocess command with appropriate flags to hide console window on Windows."""
    if platform.system().lower() == 'windows':
        # Add CREATE_NO_WINDOW flag on Windows to prevent console window from appearing
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
    
    return subprocess.run(cmd, **kwargs)

# Set up the logger for GUI application (no console output)
def setup_logging():
    """Configure logging for GUI application without console output"""
    try:
        # For GUI apps, log to file instead of console to avoid terminal window
        if platform.system() == "Windows":
            log_dir = os.path.join(os.path.expanduser("~"), ".genie")
        else:
            log_dir = os.path.expanduser("~/.genie")
        
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "genie-githooks.log")
        
        logging.basicConfig(
            level=logging.INFO,  # Reduced level for production
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                # Only add console handler in development (not in packaged app)
                # logging.StreamHandler()  # Commented out to prevent console window
            ]
        )
    except Exception:
        # If logging setup fails, use null handler to prevent console output
        logging.basicConfig(
            level=logging.CRITICAL,
            handlers=[logging.NullHandler()]
        )

setup_logging()

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setFixedWidth(300)
        
        self.status_label = QLabel("Connecting to server...")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        
    def set_status(self, text):
        self.status_label.setText(text)

class BackendURLWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Genie- Commit Review - Setup")
        self.setFixedSize(480, 420)
        self.center_window()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Brand header
        brand_label = QLabel("Genie")
        brand_font = QFont()
        brand_font.setPointSize(24)
        brand_font.setBold(True)
        brand_label.setFont(brand_font)
        brand_label.setAlignment(Qt.AlignCenter)
        
        # Feature header
        feature_label = QLabel("Commit Review")
        feature_font = QFont()
        feature_font.setPointSize(16)
        feature_label.setFont(feature_font)
        feature_label.setAlignment(Qt.AlignCenter)
        
        # Description
        desc_label = QLabel("Enter your backend server URL to get started")
        desc_label.setAlignment(Qt.AlignCenter)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Backend URL field
        url_label = QLabel("Backend URL:")
        url_label_font = QFont()
        url_label_font.setPointSize(10)
        url_label_font.setBold(True)
        url_label.setFont(url_label_font)
        
        self.backend_url = QLineEdit()
        # self.backend_url.setPlaceholderText("http://localhost:3000/genieapi")
        # self.backend_url.setText("http://localhost:3000/genieapi")
        self.backend_url.setMinimumHeight(35)
        self.backend_url.setMinimumWidth(300)
        
        # Set larger font for text input
        input_font = QFont()
        input_font.setPointSize(11)
        self.backend_url.setFont(input_font)
        
        form_layout.addWidget(url_label)
        form_layout.addWidget(self.backend_url)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.check_button = QPushButton("Check Connection")
        self.check_button.clicked.connect(self.handle_check_url)
        self.check_button.setMinimumHeight(40)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        cancel_button.setMinimumHeight(40)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.check_button)
        
        # Loading widget
        self.loading_widget = LoadingWidget()
        self.loading_widget.hide()
        
        # Assemble layout
        layout.addWidget(brand_label)
        layout.addWidget(feature_label)
        layout.addWidget(desc_label)
        layout.addSpacing(20)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addLayout(button_layout)
        layout.addWidget(self.loading_widget)
        
        self.setLayout(layout)
        
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def handle_check_url(self):
        backend_url = self.backend_url.text().strip()
        
        if not backend_url:
            QMessageBox.warning(self, "Input Error", "Please enter a backend URL")
            return
            
        # Show loading
        self.check_button.setEnabled(False)
        self.loading_widget.show()
        self.loading_widget.set_status("Checking connection...")
        
        # Use QTimer to prevent UI freezing
        QTimer.singleShot(100, lambda: self.check_connection(backend_url))
        
    def check_connection(self, backend_url):
        try:
            touch_api = f"{backend_url}/touch"
            response = requests.get(touch_api, timeout=10)
            
            if response.status_code == 200:
                self.loading_widget.hide()
                # Directly proceed to login without showing success dialog
                self.proceed_to_login(backend_url)
            else:
                self.loading_widget.hide()
                self.check_button.setEnabled(True)
                QMessageBox.critical(self, "Connection Error", f"Server responded with status: {response.status_code}")
                
        except requests.RequestException as e:
            self.loading_widget.hide()
            self.check_button.setEnabled(True)
            QMessageBox.critical(self, "Connection Error", f"Connection failed: {str(e)}")
            
    def proceed_to_login(self, backend_url):
        self.login_window.set_backend_url(backend_url)
        self.login_window.show()
        self.close()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.backend_url = None
        self.user_id = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Genie- Commit Review - Login")
        self.setFixedSize(450, 420)
        self.center_window()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel("Welcome Back")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        
        sub_header = QLabel("Sign in to your account")
        sub_header.setAlignment(Qt.AlignCenter)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)
        
        # Email field
        email_label = QLabel("Email:")
        email_label_font = QFont()
        email_label_font.setPointSize(10)
        email_label_font.setBold(True)
        email_label.setFont(email_label_font)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter your email")
        self.email.setMinimumHeight(35)
        self.email.setMinimumWidth(280)
        
        # Password field
        password_label = QLabel("Password:")
        password_label_font = QFont()
        password_label_font.setPointSize(10)
        password_label_font.setBold(True)
        password_label.setFont(password_label_font)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(35)
        self.password.setMinimumWidth(280)
        
        # Set larger font for text inputs
        input_font = QFont()
        input_font.setPointSize(11)
        self.email.setFont(input_font)
        self.password.setFont(input_font)
        
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email)
        form_layout.addSpacing(8)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password)
        
        # Buttons
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setMinimumHeight(40)
        
        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.open_register_window)
        self.register_button.setMinimumHeight(40)
        
        # Loading widget
        self.loading_widget = LoadingWidget()
        self.loading_widget.hide()
        
        # Assemble layout
        layout.addWidget(header_label)
        layout.addWidget(sub_header)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.loading_widget)
        
        self.setLayout(layout)
        
        # Connect Enter key
        self.password.returnPressed.connect(self.handle_login)
        
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def set_backend_url(self, backend_url):
        self.backend_url = backend_url
        
    def store_jwt_token(self, jwt_token):
        """Store JWT token in a secure location for hooks to use"""
        try:
            # Define Genie config path (platform-appropriate)
            if platform.system() == "Windows":
                genie_config_path = os.path.join(os.path.expanduser("~"), ".genie")
            else:
                genie_config_path = os.path.expanduser("~/.genie")
            
            # Create the .genie directory if it doesn't exist
            os.makedirs(genie_config_path, exist_ok=True)
            
            # Store token in a file
            token_file = os.path.join(genie_config_path, "token")
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(jwt_token)
            
            # Set file permissions to be readable only by the user (Unix-like systems)
            try:
                os.chmod(token_file, 0o600)
            except OSError:
                # Windows might not support chmod, but the file will still work
                pass
                
            logging.info(f"JWT token stored securely at: {token_file}")
            
        except Exception as e:
            logging.error(f"Failed to store JWT token: {e}")
            # Don't show error to user as this is not critical for hook installation
        
    def handle_login(self):
        username = self.email.text().strip()
        password = self.password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both email and password")
            return
            
        # Show loading
        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)
        self.loading_widget.show()
        self.loading_widget.set_status("Authenticating...")
        
        # Use QTimer to prevent UI freezing
        QTimer.singleShot(100, lambda: self.authenticate_user(username, password))
        
    def authenticate_user(self, username, password):
        try:
            payload = {'username': username, 'email': username, 'password': password}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            login_url = f"{self.backend_url}/auth/login"
            response = requests.post(login_url, data=payload, timeout=10)
            data = response.json()
            
            if "access_token" not in data:
                self.loading_widget.hide()
                self.login_button.setEnabled(True)
                self.register_button.setEnabled(True)
                QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")
                logging.warning(f"Failed login attempt for username: {username}")
                return
                
            jwt_token = data["access_token"]
            headers = {"Authorization": f"Bearer {jwt_token}"}
            
            user_url = f"{self.backend_url}/auth/users/me"
            user_response = requests.get(user_url, headers=headers, timeout=10)
            user_data = user_response.json()
            
            if "id" not in user_data:
                self.loading_widget.hide()
                self.login_button.setEnabled(True)
                self.register_button.setEnabled(True)
                QMessageBox.critical(self, "Error", "Failed to fetch user details")
                logging.error("Failed to fetch user details after authentication.")
                return
                
            self.user_id = str(user_data["id"])
            
            # Store JWT token for hooks to use
            self.store_jwt_token(jwt_token)
            
            self.loading_widget.set_status("Login successful! Setting up hooks...")
            
            # Proceed to hook management
            QTimer.singleShot(1000, self.manage_git_hooks)
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error during authentication: {e}")
            self.loading_widget.hide()
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)
            QMessageBox.critical(self, "Network Error", f"Network error: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error during authentication: {e}")
            self.loading_widget.hide()
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")
            
    def manage_git_hooks(self):
        try:
            GIT_HOOKS_DIR = self.get_or_set_global_git_hooks_dir()
            if not GIT_HOOKS_DIR:
                self.loading_widget.hide()
                self.login_button.setEnabled(True)
                self.register_button.setEnabled(True)
                QMessageBox.critical(self, "Error", "Git hooks directory not set. Aborting installation.")
                logging.error("Git hooks directory not set. Aborting installation.")
                return
                
            genie_hooks_installed = self.check_genie_hooks_installed(GIT_HOOKS_DIR)
            
            self.loading_widget.hide()
            
            if genie_hooks_installed:
                reply = QMessageBox.question(
                    self, "Genie Git Hooks Found", 
                    "Genie Git hooks for code review are already installed.\n\nDo you want to uninstall them?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.uninstall_genie_hooks_only(GIT_HOOKS_DIR)
            else:
                self.install_hooks_safely(GIT_HOOKS_DIR)
                
        except Exception as e:
            logging.error(f"Error managing Git hooks: {e}")
            # traceback.print_exc()  # Commented out to prevent console output
            self.loading_widget.hide()
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Error managing Git hooks: {str(e)}")

    def get_or_set_global_git_hooks_dir(self):
        """Get the Git hooks directory, using existing one or creating our own if none exists."""
        try:
            # Check if global git hooks path is already set by another application
            result = run_subprocess(['git', 'config', '--global', '--get', 'core.hooksPath'], 
                                    capture_output=True, text=True, check=False)
            hooks_path = result.stdout.strip()
            if hooks_path and os.path.exists(hooks_path):
                # Another application has set a hooks directory - use it
                logging.info(f"Using existing Git hooks directory from other application: {hooks_path}")
                return hooks_path
        except Exception as e:
            logging.error(f"Error checking existing git hooks path: {e}")
            
        # No existing hooks directory, check if we've set one before
        if platform.system() == "Windows":
            genie_hooks_path = os.path.join(os.path.expanduser("~"), ".genie", "hooks")
        else:
            genie_hooks_path = os.path.expanduser("~/.genie/hooks")
        
        # Check if we've already created our hooks directory
        if os.path.exists(genie_hooks_path):
            # Check if it's currently set as the global hooks path
            try:
                result = run_subprocess(['git', 'config', '--global', '--get', 'core.hooksPath'], 
                                        capture_output=True, text=True, check=False)
                current_path = result.stdout.strip()
                if current_path == genie_hooks_path:
                    logging.info(f"Using existing Genie hooks directory: {genie_hooks_path}")
                    return genie_hooks_path
            except Exception:
                pass
        
        # Create and set our hooks directory only if no other application is using Git hooks
        try:
            # Create the .genie/hooks directory
            os.makedirs(genie_hooks_path, exist_ok=True)
            
            # Only set as global hooks path if no other path is currently set
            result = run_subprocess(['git', 'config', '--global', '--get', 'core.hooksPath'], 
                                    capture_output=True, text=True, check=False)
            if not result.stdout.strip():
                # No global hooks path set, safe to set ours
                run_subprocess(['git', 'config', '--global', 'core.hooksPath', genie_hooks_path], 
                              check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logging.info(f"Created and set Genie hooks directory: {genie_hooks_path}")
            else:
                logging.info(f"Another application is using Git hooks, will install alongside: {genie_hooks_path}")
            
            return genie_hooks_path
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Git config error while setting up Genie hooks: {e}")
            QMessageBox.critical(self, "Error", f"Failed to configure Genie hooks directory: {str(e)}")
            return None
        except OSError as e:
            logging.error(f"Error creating Genie hooks directory: {e}")
            QMessageBox.critical(self, "Error", f"Failed to create .genie/hooks directory: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while setting up Genie hooks: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
            return None

    def check_genie_hooks_installed(self, hooks_dir):
        """Check if Genie-specific hooks are installed by looking for our signature."""
        try:
            genie_signature = "# GENIE_GITHOOKS_MARKER"
            
            # Check pre-commit hook
            pre_commit_path = os.path.join(hooks_dir, "pre-commit")
            pre_commit_installed = False
            if os.path.exists(pre_commit_path):
                with open(pre_commit_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if genie_signature in content:
                        pre_commit_installed = True
            
            # Check post-commit hook
            post_commit_path = os.path.join(hooks_dir, "post-commit")
            post_commit_installed = False
            if os.path.exists(post_commit_path):
                with open(post_commit_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if genie_signature in content:
                        post_commit_installed = True
            
            # Return True if either hook is installed
            return pre_commit_installed or post_commit_installed
            
        except Exception as e:
            logging.error(f"Error checking Genie hooks: {e}")
            return False

    def backup_existing_hooks(self, hooks_dir):
        """Backup existing hooks before modification."""
        try:
            backup_dir = os.path.join(hooks_dir, ".genie_backup")
            os.makedirs(backup_dir, exist_ok=True)
            
            hooks_to_backup = ["pre-commit", "post-commit"]
            
            for hook_name in hooks_to_backup:
                hook_path = os.path.join(hooks_dir, hook_name)
                backup_path = os.path.join(backup_dir, f"{hook_name}.original")
                
                if os.path.exists(hook_path) and not os.path.exists(backup_path):
                    shutil.copy2(hook_path, backup_path)
                    logging.info(f"Backed up existing {hook_name} hook")
                    
        except Exception as e:
            logging.error(f"Error backing up existing hooks: {e}")

    def install_hooks_safely(self, hooks_dir):
        """Install Genie hooks without overwriting other applications' hooks."""
        try:
            # Ensure the hooks directory exists
            os.makedirs(hooks_dir, exist_ok=True)
            
            # Backup existing hooks first
            self.backup_existing_hooks(hooks_dir)
            
            genie_signature = "# GENIE_GITHOOKS_MARKER"
            
            # Define source paths - handle both development and packaged app
            if getattr(sys, 'frozen', False):
                # Running as compiled executable - use PyInstaller's temp folder
                base_path = sys._MEIPASS
                hooks_base = os.path.join(base_path, 'hooks')
            else:
                # Running in development
                hooks_base = "hooks"
                
            pre_commit_source = os.path.join(hooks_base, "pre-commit")
            post_commit_source = os.path.join(hooks_base, "post-commit")
            
            logging.info(f"Looking for hooks in: {hooks_base}")
            logging.info(f"Pre-commit source exists: {os.path.exists(pre_commit_source)}")
            logging.info(f"Post-commit source exists: {os.path.exists(post_commit_source)}")
            
            # Check if hook files exist before installation
            if not os.path.exists(pre_commit_source) and not os.path.exists(post_commit_source):
                error_msg = f"Hook source files not found in {hooks_base}. Installation cannot proceed."
                logging.error(error_msg)
                QMessageBox.critical(self, "Error", error_msg)
                return
            
            # Install pre-commit hook
            if os.path.exists(pre_commit_source):
                pre_commit_path = os.path.join(hooks_dir, "pre-commit")
                
                # Read our hook content
                with open(pre_commit_source, "r", encoding="utf-8") as file:
                    genie_hook_content = file.read()
                
                # Add our signature
                genie_hook_content = f"{genie_signature}\n{genie_hook_content}"
                
                # Replace placeholders
                genie_hook_content = genie_hook_content.replace("${BASE_API}", self.backend_url).replace("${userId}", self.user_id)
                
                # Check if there's an existing hook
                existing_content = ""
                if os.path.exists(pre_commit_path):
                    with open(pre_commit_path, "r", encoding="utf-8") as f:
                        existing_content = f.read()
                        
                    # If existing hook doesn't contain our signature, chain it
                    if genie_signature not in existing_content:
                        # Create a chained hook that calls both
                        clean_genie_content = genie_hook_content.replace(genie_signature + '\n', '')
                        chained_content = f"""#!/bin/bash
{genie_signature}
# This hook chains multiple Git hook applications

# Call original hook first (if it exists and is not from Genie)
if [ -f "{hooks_dir}/.genie_backup/pre-commit.original" ]; then
    bash "{hooks_dir}/.genie_backup/pre-commit.original" "$@"
    original_exit_code=$?
    if [ $original_exit_code -ne 0 ]; then
        exit $original_exit_code
    fi
fi

# Call Genie hook
{clean_genie_content}
"""
                        genie_hook_content = chained_content
                
                # Write the hook
                with open(pre_commit_path, "w", encoding="utf-8") as f:
                    f.write(genie_hook_content)
                
                # Set executable permissions
                try:
                    os.chmod(pre_commit_path, 0o755)
                except OSError:
                    pass
                    
                logging.info("Pre-commit hook installed safely!")
            
            # Install post-commit hook (similar logic)
            if os.path.exists(post_commit_source):
                post_commit_path = os.path.join(hooks_dir, "post-commit")
                
                # Read our hook content
                with open(post_commit_source, "r", encoding="utf-8") as file:
                    genie_hook_content = file.read()
                
                # Add our signature
                genie_hook_content = f"{genie_signature}\n{genie_hook_content}"
                
                # Replace placeholders
                genie_hook_content = genie_hook_content.replace("${BASE_API}", self.backend_url).replace("${userId}", self.user_id)
                
                # Check if there's an existing hook
                existing_content = ""
                if os.path.exists(post_commit_path):
                    with open(post_commit_path, "r", encoding="utf-8") as f:
                        existing_content = f.read()
                        
                    # If existing hook doesn't contain our signature, chain it
                    if genie_signature not in existing_content:
                        # Create a chained hook that calls both
                        clean_genie_content = genie_hook_content.replace(genie_signature + '\n', '')
                        chained_content = f"""#!/bin/bash
{genie_signature}
# This hook chains multiple Git hook applications

# Call original hook first (if it exists and is not from Genie)
if [ -f "{hooks_dir}/.genie_backup/post-commit.original" ]; then
    bash "{hooks_dir}/.genie_backup/post-commit.original" "$@"
fi

# Call Genie hook
{clean_genie_content}
"""
                        genie_hook_content = chained_content
                
                # Write the hook
                with open(post_commit_path, "w", encoding="utf-8") as f:
                    f.write(genie_hook_content)
                
                # Set executable permissions
                try:
                    os.chmod(post_commit_path, 0o755)
                except OSError:
                    pass
                    
                logging.info("Post-commit hook installed safely!")
            
            QMessageBox.information(self, "Success", "Genie Git hooks installed successfully!\n\nCode review will now happen before each commit.\n\nExisting hooks from other applications have been preserved.")
            logging.info("Genie Git hooks installation completed successfully!")
            
            # Close after success
            QTimer.singleShot(2000, self.close)
            
        except Exception as e:
            logging.error(f"Error installing Genie hooks safely: {e}")
            QMessageBox.critical(self, "Error", f"Failed to install Genie hooks: {str(e)}")

    def uninstall_genie_hooks_only(self, hooks_dir):
        """Remove only Genie-specific hooks, preserve others."""
        try:
            genie_signature = "# GENIE_GITHOOKS_MARKER"
            hooks_to_process = ["pre-commit", "post-commit"]
            
            for hook_name in hooks_to_process:
                hook_path = os.path.join(hooks_dir, hook_name)
                backup_path = os.path.join(hooks_dir, ".genie_backup", f"{hook_name}.original")
                
                if os.path.exists(hook_path):
                    with open(hook_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # If this hook contains our signature
                    if genie_signature in content:
                        # Check if we have a backup of the original
                        if os.path.exists(backup_path):
                            # Restore the original hook
                            shutil.copy2(backup_path, hook_path)
                            logging.info(f"Restored original {hook_name} hook")
                        else:
                            # No original to restore, remove the hook entirely
                            os.remove(hook_path)
                            logging.info(f"Removed {hook_name} hook (no original to restore)")
            
            # Clean up backup directory if it's empty of relevant files
            backup_dir = os.path.join(hooks_dir, ".genie_backup")
            if os.path.exists(backup_dir):
                try:
                    # Remove backup files
                    for hook_name in hooks_to_process:
                        backup_file = os.path.join(backup_dir, f"{hook_name}.original")
                        if os.path.exists(backup_file):
                            os.remove(backup_file)
                    
                    # Remove backup directory if empty
                    if not os.listdir(backup_dir):
                        os.rmdir(backup_dir)
                except Exception as e:
                    logging.warning(f"Could not clean up backup directory: {e}")
            
            # Also remove the stored JWT token
            try:
                if platform.system() == "Windows":
                    token_file = os.path.join(os.path.expanduser("~"), ".genie", "token")
                else:
                    token_file = os.path.expanduser("~/.genie/token")
                    
                if os.path.exists(token_file):
                    os.remove(token_file)
                    logging.info("JWT token removed successfully")
                    
            except Exception as e:
                logging.warning(f"Failed to remove JWT token: {e}")
            
            QMessageBox.information(self, "Success", "Genie Git hooks uninstalled successfully!\n\nOriginal hooks from other applications have been preserved.")
            logging.info("Genie Git hooks uninstalled successfully!")
            
            # Close after success
            QTimer.singleShot(2000, self.close)
            
        except Exception as e:
            logging.error(f"Error uninstalling Genie hooks: {e}")
            QMessageBox.critical(self, "Error", f"Failed to uninstall Genie hooks: {str(e)}")
            
    def open_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.close()

class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.backend_url = self.login_window.backend_url
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Genie- Commit Review - Register")
        self.setFixedSize(500, 600)
        self.center_window()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel("Create Account")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        
        sub_header = QLabel("Join Genie- Commit Review today")
        sub_header.setAlignment(Qt.AlignCenter)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(6)
        
        # Create label font
        label_font = QFont()
        label_font.setPointSize(10)
        label_font.setBold(True)
        
        # Set larger font for all text inputs
        input_font = QFont()
        input_font.setPointSize(11)
        
        # Full Name field
        fullname_label = QLabel("Full Name:")
        fullname_label.setFont(label_font)
        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Enter your full name")
        self.fullname.setMinimumHeight(35)
        self.fullname.setMinimumWidth(280)
        self.fullname.setFont(input_font)
        
        # Email field
        email_label = QLabel("Email:")
        email_label.setFont(label_font)
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter your email")
        self.email.setMinimumHeight(35)
        self.email.setMinimumWidth(280)
        self.email.setFont(input_font)
        
        # Company field
        company_label = QLabel("Company:")
        company_label.setFont(label_font)
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Enter your company name")
        self.company_name.setMinimumHeight(35)
        self.company_name.setMinimumWidth(280)
        self.company_name.setFont(input_font)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setFont(label_font)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Create a password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(35)
        self.password.setMinimumWidth(280)
        self.password.setFont(input_font)
        
        # Confirm Password field
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFont(label_font)
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm your password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setMinimumHeight(35)
        self.confirm_password.setMinimumWidth(280)
        self.confirm_password.setFont(input_font)
        
        # Add all fields to layout
        form_layout.addWidget(fullname_label)
        form_layout.addWidget(self.fullname)
        form_layout.addSpacing(6)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email)
        form_layout.addSpacing(6)
        form_layout.addWidget(company_label)
        form_layout.addWidget(self.company_name)
        form_layout.addSpacing(6)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password)
        form_layout.addSpacing(6)
        form_layout.addWidget(confirm_label)
        form_layout.addWidget(self.confirm_password)
        
        # Buttons
        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setMinimumHeight(40)
        
        self.back_button = QPushButton("Back to Login")
        self.back_button.clicked.connect(self.go_back_to_login)
        self.back_button.setMinimumHeight(40)
        
        # Loading widget
        self.loading_widget = LoadingWidget()
        self.loading_widget.hide()
        
        # Assemble layout
        layout.addWidget(header_label)
        layout.addWidget(sub_header)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)
        layout.addWidget(self.loading_widget)
        
        self.setLayout(layout)
        
        # Connect Enter key
        self.confirm_password.returnPressed.connect(self.handle_register)
        
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def handle_register(self):
        fullname = self.fullname.text().strip()
        email = self.email.text().strip()
        company_name = self.company_name.text().strip()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if not all([fullname, email, company_name, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match!")
            return
            
        # Show loading
        self.register_button.setEnabled(False)
        self.back_button.setEnabled(False)
        self.loading_widget.show()
        self.loading_widget.set_status("Creating account...")
        
        # Use QTimer to prevent UI freezing
        QTimer.singleShot(100, lambda: self.create_account(fullname, email, company_name, password, confirm_password))
        
    def create_account(self, fullname, email, company_name, password, confirm_password):
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
            response = requests.post(f"{self.backend_url}/auth/register", json=payload, headers=headers, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                self.loading_widget.hide()
                QMessageBox.information(self, "Success", "Registration successful!\n\nPlease login with your new account.")
                QTimer.singleShot(2000, self.go_back_to_login)
            else:
                self.loading_widget.hide()
                self.register_button.setEnabled(True)
                self.back_button.setEnabled(True)
                error_msg = data.get('detail', 'Registration failed. Please try again.')
                QMessageBox.critical(self, "Registration Error", f"Registration failed:\n{error_msg}")
                
        except requests.exceptions.RequestException as e:
            self.loading_widget.hide()
            self.register_button.setEnabled(True)
            self.back_button.setEnabled(True)
            QMessageBox.critical(self, "Network Error", f"Network error: {str(e)}")
        except Exception as e:
            self.loading_widget.hide()
            self.register_button.setEnabled(True)
            self.back_button.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")
            
    def go_back_to_login(self):
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Genie- Commit Review")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Bilvantis")
    
    # Initialize and show windows
    login_window = LoginWindow()
    backend_window = BackendURLWindow(login_window)
    backend_window.show()
    
    sys.exit(app.exec())
