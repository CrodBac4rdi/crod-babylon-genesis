#!/bin/bash

# CROD ULTIMATIV CREATIVE SUITE - Build & Start
echo "🔥🔥🔥 CROD ULTIMATIV CREATIVE SUITE 🔥🔥🔥"
echo "==========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check GPU
echo "🎮 Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✅ NVIDIA GPU detected!${NC}"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    GPU_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  No NVIDIA GPU detected, using CPU mode${NC}"
    GPU_AVAILABLE=false
fi

# Install dependencies if needed
echo ""
echo "📦 Checking dependencies..."

# Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
fi

# Node.js for Tauri
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Rust for Tauri
if ! command -v cargo &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

# Tauri CLI
if ! command -v cargo-tauri &> /dev/null; then
    echo "Installing Tauri CLI..."
    cargo install tauri-cli
fi

# Build Tauri App
echo ""
echo "🔨 Building CROD Creative Suite..."
cd crod-creative-suite/tauri-app

# Install frontend dependencies
npm install

# Build Tauri app
cargo tauri build

# Copy executable to desktop
cp src-tauri/target/release/crod-ultimativ ~/Schreibtisch/CROD_ULTIMATIV

# Make it executable
chmod +x ~/Schreibtisch/CROD_ULTIMATIV

# Create desktop entry with icon
cat > ~/Schreibtisch/CROD_Creative_Suite.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=🔥 CROD Creative Suite
Comment=Create Everything, Mine Innovation
Exec=/home/daniel/Schreibtisch/CROD_ULTIMATIV
Icon=/home/daniel/Schreibtisch/crod-babylon-genesis-main/CROD_ULTIMATIV/crod-icon.png
Terminal=false
Categories=Development;Graphics;Game;
StartupNotify=true
Actions=Start;Stop;

[Desktop Action Start]
Name=Start All Services
Exec=bash -c "cd /home/daniel/Schreibtisch/crod-babylon-genesis-main/CROD_ULTIMATIV && docker-compose up -d"

[Desktop Action Stop]
Name=Stop All Services
Exec=bash -c "cd /home/daniel/Schreibtisch/crod-babylon-genesis-main/CROD_ULTIMATIV && docker-compose down"
EOF

chmod +x ~/Schreibtisch/CROD_Creative_Suite.desktop

# Start backend services
echo ""
echo "🚀 Starting backend services..."
cd ..
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 10

# Create startup script
cat > ~/Schreibtisch/START_CROD_CREATIVE.sh << 'EOF'
#!/bin/bash
echo "🔥 STARTING CROD CREATIVE SUITE 🔥"

# Start Docker services if not running
cd /home/daniel/Schreibtisch/crod-babylon-genesis-main/CROD_ULTIMATIV/crod-creative-suite
docker-compose up -d

# Wait a bit
sleep 5

# Start the app
/home/daniel/Schreibtisch/CROD_ULTIMATIV &

# Show logs
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🔥 CROD Creative Suite is running!"
echo ""
echo "Features:"
echo "  ✅ Game Creation with GPU acceleration"
echo "  ✅ 3D Modeling & Animation"
echo "  ✅ Story & Content Generation"
echo "  ✅ Media Processing (GIF, Video)"
echo "  ✅ Innovation Mining System"
echo "  ✅ Review & Learning Tracker"
echo ""
echo "Every creation is evaluated for innovation!"
echo "Only truly new creations mine blocks!"
EOF

chmod +x ~/Schreibtisch/START_CROD_CREATIVE.sh

# Final message
echo ""
echo -e "${GREEN}✅ BUILD COMPLETE!${NC}"
echo ""
echo "🎯 TO START CROD CREATIVE SUITE:"
echo "   1. Double-click 'CROD Creative Suite' on your desktop"
echo "   2. OR run: ~/Schreibtisch/START_CROD_CREATIVE.sh"
echo ""
echo "🔥 FEATURES:"
echo "   • Create games, 3D models, stories, media"
echo "   • GPU accelerated rendering"
echo "   • Innovation-based mining"
echo "   • Review & tag everything"
echo "   • Network learns from your creations"
echo ""
echo "💡 MINING RULES:"
echo "   • New blocks only for TRUE innovations"
echo "   • Efficiency = Network improvement"
echo "   • No duplicates = No blocks"
echo "   • Create something NEW to mine!"
echo ""
echo "🚀 Press Enter to start now..."
read

# Start immediately
~/Schreibtisch/START_CROD_CREATIVE.sh