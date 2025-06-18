#!/bin/bash
echo "🚀 Building Genie GitHooks..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install requirements if not already installed
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Install PyInstaller if not already installed
pip install pyinstaller

# Generate the spec file using Python
echo "Generating PyInstaller spec file..."
python generate_spec.py

# Build the executable
echo "Building executable..."
pyinstaller --clean genie-githooks.spec
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

# Platform-specific post-processing
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    echo "✅ Build complete!"
    echo "The application can be found at dist/GenieGitHooks.app"
    echo ""
    echo "🍎 For professional macOS distribution, use:"
    echo "   ./build-mac.sh"
    
    # Check if we need to sign the app
    if [ -n "$APPLE_DEVELOPER_ID" ]; then
        echo "🔐 Signing the application with Developer ID: $APPLE_DEVELOPER_ID"
        codesign --force --options runtime --sign "$APPLE_DEVELOPER_ID" "dist/GenieGitHooks.app"
    fi
    
elif [ "$(uname)" = "Linux" ]; then
    # Linux
    echo "✅ Build complete!"
    echo "The executable can be found at dist/GenieGitHooks"
    echo ""
    echo "🐧 To distribute:"
    echo "   • Copy the dist folder for portable distribution"
    echo "   • Create a .deb or .rpm package for system installation"
    
else
    # Other Unix-like systems
    echo "✅ Build complete!"
    echo "The executable can be found in the dist folder."
fi

echo ""
echo "🚀 For professional packaging with installers, use:"
echo "   • Windows: build-windows.bat or python build_windows.py"
echo "   • macOS: ./build-mac.sh or python build_mac.py" 