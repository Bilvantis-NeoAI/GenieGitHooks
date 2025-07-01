#!/usr/bin/env python3
"""
Genie GitHooks - Pre-commit Hook (Python Implementation)
Cross-platform compatible Git pre-commit hook for code review
"""

import os
import sys
import json
import subprocess
import tempfile
import platform
import requests
import webbrowser
from pathlib import Path

def show_message_box(message):
    """Display a message box using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Genie GitHooks", message)
    except ImportError:
        # Fallback to console if tkinter is not available
        print(f"GENIE GITHOOKS: {message}")

def detect_language(files):
    """Detect programming language from file extensions"""
    if not files:
        return 'unknown'
    
    # Check for special file patterns first
    special_files = {
        'requirements.txt': 'python',
        'pyproject.toml': 'python',
        'setup.py': 'python',
        'setup.cfg': 'python',
        'pipfile': 'python',
        'pipfile.lock': 'python',
        'poetry.lock': 'python',
        'conda.yaml': 'python',
        'environment.yml': 'python',
        'package.json': 'javascript',
        'package-lock.json': 'javascript',
        'yarn.lock': 'javascript',
        'bower.json': 'javascript',
        'webpack.config.js': 'javascript',
        'gulpfile.js': 'javascript',
        'gruntfile.js': 'javascript',
        'dockerfile': 'docker',
        'docker-compose.yml': 'docker',
        'docker-compose.yaml': 'docker',
        'makefile': 'makefile',
        'rakefile': 'ruby',
        'gemfile': 'ruby',
        'gemfile.lock': 'ruby',
        'cargo.toml': 'rust',
        'cargo.lock': 'rust',
        'pom.xml': 'java',
        'build.gradle': 'java',
        'composer.json': 'php',
        'composer.lock': 'php'
    }
    
    # Check if any files match special patterns
    for file in files:
        filename = os.path.basename(file).lower()
        if filename in special_files:
            return special_files[filename]
    
    # Extension-based detection
    extensions = {}
    for file in files:
        if '.' in file:
            ext = file.split('.')[-1].lower()
            extensions[ext] = extensions.get(ext, 0) + 1
    
    # Enhanced language mapping
    lang_map = {
        'py': 'python', 'pyx': 'python', 'pyi': 'python',
        'js': 'javascript', 'jsx': 'javascript',
        'ts': 'typescript', 'tsx': 'typescript',
        'java': 'java', 'class': 'java', 'jar': 'java',
        'cpp': 'cpp', 'cxx': 'cpp', 'cc': 'cpp',
        'c': 'c', 'h': 'c', 'hpp': 'cpp',
        'cs': 'csharp',
        'php': 'php', 'php3': 'php', 'php4': 'php', 'php5': 'php',
        'rb': 'ruby', 'ruby': 'ruby',
        'go': 'go', 'rs': 'rust',
        'kt': 'kotlin', 'kts': 'kotlin',
        'swift': 'swift',
        'html': 'html', 'htm': 'html',
        'css': 'css', 'scss': 'scss', 'sass': 'scss', 'less': 'css',
        'sql': 'sql', 'mysql': 'sql', 'postgresql': 'sql',
        'sh': 'bash', 'bash': 'bash', 'zsh': 'bash', 'fish': 'bash',
        'yml': 'yaml', 'yaml': 'yaml',
        'json': 'json', 'jsonc': 'json',
        'xml': 'xml', 'xsd': 'xml', 'xsl': 'xml',
        'md': 'markdown', 'markdown': 'markdown',
        'txt': 'text', 'text': 'text', 'log': 'text',
        'cfg': 'text', 'conf': 'text', 'config': 'text',
        'ini': 'text', 'properties': 'text', 'env': 'text',
        'toml': 'toml', 'dockerfile': 'docker',
        'makefile': 'makefile', 'mk': 'makefile'
    }
    
    if extensions:
        most_common_ext = max(extensions, key=extensions.get)
        return lang_map.get(most_common_ext, 'unknown')
    
    return 'unknown'

def open_html_in_browser(api_response):
    """Extract and open HTML from API response in browser"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
            # Try to parse as JSON first
            html_content = api_response
            try:
                parsed = json.loads(api_response)
                if isinstance(parsed, dict):
                    # Check for common HTML response keys
                    for key in ['html', 'content', 'response', 'data']:
                        if key in parsed:
                            html_content = parsed[key]
                            break
            except json.JSONDecodeError:
                pass
            
            # Write HTML to temp file
            temp_file.write(html_content)
            temp_file_path = temp_file.name
        
        # Open in browser
        webbrowser.open(f'file://{temp_file_path}')
        
    except Exception as e:
        print(f"Warning: Could not open review in browser: {e}")

def get_git_info():
    """Get Git repository information"""
    try:
        # Get staged files
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                              capture_output=True, text=True, check=True)
        staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # Get diff content
        result = subprocess.run(['git', 'diff', '--cached'], 
                              capture_output=True, text=True, check=True)
        diff_content = result.stdout
        
        # Get repo name
        try:
            result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], 
                                  capture_output=True, text=True, check=False)
            if result.stdout:
                repo_name = result.stdout.strip().split('/')[-1].replace('.git', '')
            else:
                repo_name = os.path.basename(os.getcwd())
        except:
            repo_name = os.path.basename(os.getcwd())
        
        # Get branch name
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        branch_name = result.stdout.strip()
        
        return staged_files, diff_content, repo_name, branch_name
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return [], "", "", ""

def get_jwt_token():
    """Get JWT token from stored location"""
    try:
        if platform.system() == "Windows":
            token_file = os.path.join(os.path.expanduser("~"), ".genie", "token")
        else:
            token_file = os.path.expanduser("~/.genie/token")
        
        if os.path.exists(token_file):
            with open(token_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception as e:
        print(f"Error reading token: {e}")
    
    return None

def send_for_review(diff_content, language, repo_name, branch_name, api_url, jwt_token):
    """Send code changes for review"""
    try:
        payload = {
            "code": diff_content,
            "language": language,
            "project_name": repo_name,
            "branch_name": branch_name,
            "html": True
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        }
        
        # print("DEBUG: Sending request to API...")
        # print(f"DEBUG: Payload size: {len(json.dumps(payload))} characters")
        
        response = requests.post(f"{api_url}/review/review", 
                               json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Error sending for review: {e}")
        return None

def get_api_url():
    """Get API URL from configuration file"""
    try:
        if platform.system() == "Windows":
            config_file = os.path.join(os.path.expanduser("~"), ".genie", "config")
        else:
            config_file = os.path.expanduser("~/.genie/config")
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return content
        
        # Fallback: try to read from environment variable (for backward compatibility)
        env_api = os.environ.get('GENIE_API_URL') or os.environ.get('BASE_API')
        if env_api:
            return env_api
            
        return None
        
    except Exception as e:
        print(f"Error reading API configuration: {e}")
        return None

def main():
    """Main pre-commit hook logic"""
    print("pre-commit")
    
    # Get API URL from configuration file
    api_url = get_api_url()
    if not api_url:
        print("ERROR: API URL not configured.")
        print("Please run the Genie GitHooks app to set up your backend URL.")
        print("The app will create a configuration file with your API settings.")
        return 1
    
    # Check Git configuration
    try:
        result = subprocess.run(['git', 'config', '--global', '--get', 'user.name'], 
                              capture_output=True, text=True, check=False)
        git_username = result.stdout.strip()
        
        result = subprocess.run(['git', 'config', '--global', '--get', 'user.email'], 
                              capture_output=True, text=True, check=False)
        git_email = result.stdout.strip()
        
        if not git_username or not git_email:
            show_message_box('Error: Git global username and/or email is not set.\n'
                           'Please configure them using:\n'
                           'git config --global user.name "Your Name"\n'
                           'git config --global user.email "you@example.com"')
            return 1
            
    except Exception as e:
        print(f"Error checking Git configuration: {e}")
        return 1
    
    # Get Git information
    staged_files, diff_content, repo_name, branch_name = get_git_info()
    
    if not staged_files:
        show_message_box("No files staged for commit.")
        return 0
    
    if not diff_content:
        show_message_box("No changes detected in staged files.")
        return 0
    
    # Detect programming language
    language = detect_language(staged_files)
    
    # Debug output
    # print(f"DEBUG: Staged files: {' '.join(staged_files)}")
    # print(f"DEBUG: Language detected: {language}")
    # print(f"DEBUG: Repo name: {repo_name}")
    # print(f"DEBUG: Branch name: {branch_name}")
    # print(f"DEBUG: Diff content length: {len(diff_content)}")
    # print("DEBUG: First 200 chars of diff:")
    print(diff_content[:200])
    print("")
    print("--- End diff preview ---")
    
    # Get JWT token
    jwt_token = get_jwt_token()
    if not jwt_token:
        show_message_box("ERROR: Authentication token not found. Please run the Genie GitHooks app to login again.")
        return 1
    
    # API URL is already set from command line argument above
    
    # Send for review
    response = send_for_review(diff_content, language, repo_name, branch_name, api_url, jwt_token)
    
    if response:
        # Check for authentication errors
        if '"detail":' in response and ('"Unauthorized"' in response or '"Invalid token"' in response):
            show_message_box("ERROR: Authentication failed. Your session may have expired.\n"
                           "Please run the Genie GitHooks app to login again.")
            return 1
        
        # Check for other errors
        if '"detail":' in response and '"Not Found"' in response:
            show_message_box("ERROR: API endpoint not found. Please check server configuration.")
            return 1
        
        # Open HTML response in browser
        open_html_in_browser(response)
    else:
        show_message_box("ERROR: Unable to communicate with the server. Check internet connection or server status.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 