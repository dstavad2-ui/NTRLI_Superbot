#!/bin/bash

# NTRLI Superbot - APK Build Script
# This script builds the Android APK for NTRLI Superbot

echo "=================================="
echo "NTRLI Superbot - APK Builder"
echo "=================================="
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer is not installed!"
    echo "Installing buildozer..."
    pip install buildozer
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found!"
    echo "Please run this script from the app1 directory"
    exit 1
fi

# Clean previous builds (optional)
read -p "Clean previous builds? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning previous builds..."
    rm -rf .buildozer
    rm -rf bin
fi

# Choose build type
echo ""
echo "Select build type:"
echo "1) Debug APK (faster, for testing)"
echo "2) Release APK (optimized, for distribution)"
read -p "Enter choice (1 or 2): " build_type

if [ "$build_type" == "2" ]; then
    echo "🔨 Building RELEASE APK..."
    buildozer android release
else
    echo "🔨 Building DEBUG APK..."
    buildozer android debug
fi

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ BUILD SUCCESSFUL!"
    echo ""
    echo "APK location: $(pwd)/bin/"
    ls -lh bin/*.apk
    echo ""
    echo "📱 Transfer the APK to your Android device and install"
    echo "⚠️  Enable 'Install from Unknown Sources' in Android settings"
else
    echo ""
    echo "❌ BUILD FAILED!"
    echo "Check the error messages above"
    exit 1
fi
