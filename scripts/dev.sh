#!/bin/bash
# Development script for Foldline
# This runs the backend in dev mode and starts Tauri dev

set -e

echo "🚀 Starting Foldline in development mode..."

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "Stopping backend..."
    kill $BACKEND_PID 2>/dev/null || true
    exit
}

trap cleanup EXIT INT TERM

# Start Python backend
echo "Starting Python backend..."
cd backend
python3 main.py --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 2

# Start Tauri dev (this will also start the frontend)
echo "Starting Tauri dev..."
cd src-tauri
cargo tauri dev

# Cleanup will be called automatically on exit
