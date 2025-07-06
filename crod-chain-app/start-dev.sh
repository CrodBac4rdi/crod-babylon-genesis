#!/bin/bash

echo "🚀 CROD Chain App - Starting Development Server"
echo "============================================="

cd "$(dirname "$0")"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build Rust backend first
echo "🔨 Building Rust backend..."
cd src-tauri
cargo build
cd ..

# Start the dev server
echo "🌟 Starting Tauri development server..."
npm run tauri dev