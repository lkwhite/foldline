#!/bin/bash
# Development setup script for Foldline

set -e

echo "🔧 Setting up Foldline development environment..."

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

if ! command -v cargo &> /dev/null; then
    echo "❌ Rust is not installed. Please install Rust first: https://rustup.rs/"
    exit 1
fi

echo "✓ Prerequisites found"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..
echo "✓ Frontend dependencies installed"

# Install backend dependencies
echo ""
echo "📦 Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..
echo "✓ Backend dependencies installed"

# Create placeholder icons for Tauri
echo ""
echo "🎨 Creating placeholder icons..."
mkdir -p src-tauri/icons
# Note: You'll need to add actual icon files here
# For now, this just creates the directory

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  1. Start the backend: cd backend && python3 main.py"
echo "  2. In another terminal, start Tauri: cd src-tauri && cargo tauri dev"
echo ""
echo "Or use the shortcut: npm run tauri:dev"
