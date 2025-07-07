#!/bin/bash
# 🔥 CROD ULTIMATE SETUP SCRIPT
# Diese Datei installiert ALLES was du für die ultimative Live-Coding-Umgebung brauchst

set -e

echo "=================================================================="
echo "🦠 CROD PARASIT ULTIMATE SETUP"
echo "Installing EVERYTHING for the ultimate development experience!"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_info "Starting CROD Ultimate Setup..."

# Update system
print_info "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y
print_status "System updated"

# Install essential system dependencies
print_info "Installing essential system dependencies..."
sudo apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    cmake \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

print_status "Essential dependencies installed"

# Install Tauri system dependencies
print_info "Installing Tauri system dependencies..."
sudo apt-get install -y \
    libwebkit2gtk-4.0-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libsoup2.4-dev \
    libjavascriptcoregtk-4.0-dev \
    libglib2.0-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libatk1.0-dev \
    libgdk-pixbuf-2.0-dev \
    libxss1 \
    libasound2-dev

print_status "Tauri dependencies installed"

# Install database systems
print_info "Installing database systems..."
sudo apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    postgresql \
    postgresql-contrib \
    redis-server

print_status "Database systems installed"

# Install Python and scientific computing libraries
print_info "Installing Python and scientific libraries..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    python3-pandas

print_status "Python ecosystem installed"

# Install Node.js (latest LTS)
print_info "Installing Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
    print_status "Node.js installed"
else
    print_status "Node.js already installed"
fi

# Install Rust
print_info "Installing/Updating Rust..."
if ! command -v rustc &> /dev/null; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
    print_status "Rust installed"
else
    rustup update
    print_status "Rust updated"
fi

# Make sure cargo is in PATH
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.cargo/env 2>/dev/null || true

# Install Tauri CLI
print_info "Installing Tauri CLI..."
cargo install tauri-cli --locked
print_status "Tauri CLI installed"

# Install additional Rust tools
print_info "Installing Rust development tools..."
cargo install \
    cargo-watch \
    cargo-edit \
    cargo-expand \
    cargo-audit \
    cargo-outdated

print_status "Rust tools installed"

# Install Python ML/AI libraries
print_info "Installing Python ML/AI libraries..."
pip3 install --user --upgrade pip

# Core ML libraries
pip3 install --user \
    numpy \
    scipy \
    matplotlib \
    pandas \
    scikit-learn \
    jupyter \
    ipython

# Deep Learning
pip3 install --user \
    tensorflow \
    torch \
    torchvision \
    transformers

# Computer Vision
pip3 install --user \
    opencv-python \
    Pillow \
    plotly

# 3D Graphics
pip3 install --user \
    vtk \
    mayavi \
    open3d \
    trimesh

# Web frameworks
pip3 install --user \
    flask \
    fastapi \
    uvicorn \
    websockets \
    aiohttp

# Database connectors
pip3 install --user \
    sqlalchemy \
    psycopg2-binary \
    pymongo \
    redis

# Development tools
pip3 install --user \
    black \
    flake8 \
    pytest \
    mypy

print_status "Python libraries installed"

# Install additional JavaScript packages globally
print_info "Installing global JavaScript packages..."
npm install -g \
    typescript \
    ts-node \
    @types/node \
    prettier \
    eslint \
    nodemon \
    concurrently

print_status "Global JavaScript packages installed"

# Setup the CROD project
print_info "Setting up CROD project..."
cd "$(dirname "$0")"

if [ -d "crod-chain-app" ]; then
    cd crod-chain-app
    
    print_info "Installing npm dependencies..."
    npm install
    
    print_info "Installing additional npm dependencies..."
    npm install \
        @tauri-apps/api \
        @tauri-apps/plugin-updater \
        @tauri-apps/plugin-dialog \
        @tauri-apps/plugin-fs \
        @tauri-apps/plugin-sql \
        framer-motion \
        lucide-react \
        zustand \
        recharts
    
    print_status "NPM dependencies installed"
    
    # Build Rust backend
    print_info "Building Rust backend..."
    cd src-tauri
    cargo build
    cd ..
    
    print_status "Rust backend built"
else
    print_warning "crod-chain-app directory not found. Make sure you're in the right directory."
fi

# Create desktop entry
print_info "Creating desktop entry..."
cat > ~/.local/share/applications/crod-ultimate.desktop << EOF
[Desktop Entry]
Name=CROD Ultimate
Comment=Ultimate AI Development Environment
Exec=/workspaces/crod-babylon-genesis/crod-chain-app/src-tauri/target/debug/crod-chain-app
Icon=/workspaces/crod-babylon-genesis/crod-chain-app/src-tauri/icons/icon.png
Type=Application
Categories=Development;IDE;
Terminal=false
EOF

print_status "Desktop entry created"

# Create run script
cat > ~/run-crod.sh << 'EOF'
#!/bin/bash
cd /workspaces/crod-babylon-genesis/crod-chain-app
npm run tauri dev
EOF

chmod +x ~/run-crod.sh
print_status "Run script created at ~/run-crod.sh"

echo ""
echo "=================================================================="
echo -e "${GREEN}🎉 CROD ULTIMATE SETUP COMPLETE! 🎉${NC}"
echo "=================================================================="
echo ""
echo -e "${CYAN}What was installed:${NC}"
echo "✓ System dependencies and build tools"
echo "✓ Tauri with all required libraries"
echo "✓ Node.js with TypeScript ecosystem"
echo "✓ Rust with development tools"
echo "✓ Python with ML/AI libraries (TensorFlow, PyTorch, etc.)"
echo "✓ 3D graphics libraries (VTK, Open3D, etc.)"
echo "✓ Database systems (PostgreSQL, Redis, SQLite)"
echo "✓ Web frameworks (Flask, FastAPI)"
echo "✓ Development tools and linters"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. To start CROD: cd crod-chain-app && npm run tauri dev"
echo "3. Or use the run script: ~/run-crod.sh"
echo ""
echo -e "${PURPLE}🦠 CROD PARASIT is ready to enhance your development experience!${NC}"
echo "=================================================================="
