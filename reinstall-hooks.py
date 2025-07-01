#!/usr/bin/env python3
"""
Quick script to reinstall Genie GitHooks and check their status
"""
import os
import sys
import platform
import shutil

def main():
    print("🔧 Genie GitHooks - Quick Reinstall")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ ERROR: Not in a Git repository")
        return 1
    
    # Check if hooks directory exists
    hooks_base = "hooks"
    if not os.path.exists(hooks_base):
        print(f"❌ ERROR: {hooks_base} directory not found")
        return 1
    
    # Determine platform-specific source files
    is_windows = platform.system().lower() == 'windows'
    
    if is_windows:
        pre_commit_source = os.path.join(hooks_base, "pre-commit-windows")
        post_commit_source = os.path.join(hooks_base, "post-commit-windows")
        print("🪟 Windows detected - using batch file hooks")
    else:
        pre_commit_source = os.path.join(hooks_base, "pre-commit")
        post_commit_source = os.path.join(hooks_base, "post-commit")
        print("🐧 Unix/Linux/Mac detected - using bash hooks")
    
    # Python implementation files
    pre_commit_py_source = os.path.join(hooks_base, "pre-commit.py")
    post_commit_py_source = os.path.join(hooks_base, "post-commit.py")
    
    # Check if source files exist
    missing_files = []
    for file in [pre_commit_source, post_commit_source, pre_commit_py_source, post_commit_py_source]:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ ERROR: Missing source files:")
        for file in missing_files:
            print(f"   - {file}")
        return 1
    
    # Create hooks directory and backup existing hooks
    git_hooks_dir = ".git/hooks"
    os.makedirs(git_hooks_dir, exist_ok=True)
    
    # Install hooks
    print("\n📁 Installing hooks...")
    
    # Pre-commit hook
    pre_commit_dest = os.path.join(git_hooks_dir, "pre-commit")
    shutil.copy2(pre_commit_source, pre_commit_dest)
    if not is_windows:
        os.chmod(pre_commit_dest, 0o755)
    print(f"✅ Installed: {pre_commit_dest}")
    
    # Pre-commit Python implementation
    pre_commit_py_dest = os.path.join(git_hooks_dir, "pre-commit.py")
    shutil.copy2(pre_commit_py_source, pre_commit_py_dest)
    print(f"✅ Installed: {pre_commit_py_dest}")
    
    # Post-commit hook
    post_commit_dest = os.path.join(git_hooks_dir, "post-commit")
    shutil.copy2(post_commit_source, post_commit_dest)
    if not is_windows:
        os.chmod(post_commit_dest, 0o755)
    print(f"✅ Installed: {post_commit_dest}")
    
    # Post-commit Python implementation
    post_commit_py_dest = os.path.join(git_hooks_dir, "post-commit.py")
    shutil.copy2(post_commit_py_source, post_commit_py_dest)
    print(f"✅ Installed: {post_commit_py_dest}")
    
    print("\n🔍 Checking installation...")
    
    # Check file sizes and types
    for hook_name, hook_path in [("pre-commit", pre_commit_dest), ("post-commit", post_commit_dest)]:
        if os.path.exists(hook_path):
            size = os.path.getsize(hook_path)
            with open(hook_path, 'r') as f:
                first_line = f.readline().strip()
            print(f"✅ {hook_name}: {size} bytes, starts with: {first_line}")
        else:
            print(f"❌ {hook_name}: Not found")
    
    # Check API configuration
    config_file = os.path.expanduser("~/.genie/config")
    token_file = os.path.expanduser("~/.genie/token")
    
    print(f"\n🔑 Configuration check...")
    if os.path.exists(config_file):
        print(f"✅ Config file exists: {config_file}")
    else:
        print(f"❌ Config file missing: {config_file}")
    
    if os.path.exists(token_file):
        print(f"✅ Token file exists: {token_file}")
    else:
        print(f"❌ Token file missing: {token_file}")
    
    print("\n🎉 Hook installation completed!")
    print("\n💡 Next steps:")
    print("   1. Make a test commit to verify hooks work")
    print("   2. If you get errors, check that Python 3 is installed")
    print("   3. If API errors occur, run the main app to re-login")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 