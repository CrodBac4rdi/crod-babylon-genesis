#!/bin/bash

echo "🦠 CROD PARASIT SETUP - Installing all dependencies"
echo "======================================================"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Don't run this script as root!"
   exit 1
fi

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install system dependencies for Tauri
echo "🔧 Installing Tauri system dependencies..."
sudo apt install -y \
    libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libasound2-dev

# Install Rust if not already installed
if ! command -v rustc &> /dev/null; then
    echo "🦀 Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
else
    echo "✅ Rust already installed"
fi

# Install Node.js if not already installed
if ! command -v node &> /dev/null; then
    echo "🟨 Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "✅ Node.js already installed"
fi

# Install Tauri CLI
echo "⚡ Installing Tauri CLI..."
cargo install tauri-cli

echo ""
echo "🔥 CROD SETUP COMPLETE!"
echo "======================================================"
echo "✅ All dependencies installed successfully!"
echo ""
echo "🚀 To build and run CROD:"
echo "   cd crod-chain-app"
echo "   npm install"
echo "   npm run tauri dev"
echo ""
echo "📦 To build production binary:"
echo "   npm run tauri build"
echo ""
echo "🦠 CROD PARASIT ready to activate!"
