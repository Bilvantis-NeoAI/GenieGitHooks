#!/usr/bin/env python3
"""
Genie GitHooks - Post-commit Hook (Python Implementation)
Cross-platform compatible Git post-commit hook
"""

import os
import sys
import subprocess
import platform

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

def get_commit_details():
    """Get details about the latest commit"""
    try:
        # Get commit ID
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        commit_id = result.stdout.strip()
        
        # Get commit message
        result = subprocess.run(['git', 'log', '--format=%B', '-n', '1', commit_id], 
                              capture_output=True, text=True, check=True)
        commit_message = result.stdout.strip()
        
        # Get branch name
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        branch = result.stdout.strip()
        
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
        
        return commit_id, commit_message, branch, repo_name
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return "", "", "", ""

def main():
    """Main post-commit hook logic"""
    # Get commit details
    commit_id, commit_message, branch, repo_name = get_commit_details()
    
    # Display commit information
    print("Commit completed successfully!")
    print(f"Commit ID: {commit_id}")
    print(f"Branch: {branch}")
    print(f"Repository: {repo_name}")
    print(f"Message: {commit_message}")
    
    # Optional: Show completion message
    # show_message_box(f"Commit completed successfully in branch: {branch}")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 