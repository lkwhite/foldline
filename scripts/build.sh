#!/bin/bash
# Build script for Foldline

set -e

echo "🏗️  Building Foldline..."

# Build frontend
echo ""
echo "📦 Building frontend..."
cd frontend
npm run build
cd ..
echo "✓ Frontend built"

# Build Python backend with PyInstaller
echo ""
echo "📦 Building Python backend..."
cd backend

# Install PyInstaller if not present
pip install pyinstaller

# Build standalone executable
pyinstaller --name python_backend \
    --onefile \
    --clean \
    --noconfirm \
    main.py

# Move binary to Tauri bin directory
echo "Moving backend binary to Tauri bin directory..."
mkdir -p ../src-tauri/bin

if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    cp dist/python_backend.exe ../src-tauri/bin/
    echo "✓ Windows binary copied"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    cp dist/python_backend ../src-tauri/bin/python_backend-aarch64-apple-darwin
    cp dist/python_backend ../src-tauri/bin/python_backend-x86_64-apple-darwin
    echo "✓ macOS binaries copied"
else
    cp dist/python_backend ../src-tauri/bin/python_backend-x86_64-unknown-linux-gnu
    echo "✓ Linux binary copied"
fi

cd ..
echo "✓ Backend built"

# Build Tauri app
echo ""
echo "📦 Building Tauri application..."
cd src-tauri
cargo tauri build
cd ..
echo "✓ Tauri app built"

echo ""
echo "✅ Build complete!"
echo ""
echo "Installers can be found in src-tauri/target/release/bundle/"
