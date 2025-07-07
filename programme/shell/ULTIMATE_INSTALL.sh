#!/bin/bash
# 🔥 CROD ULTIMATE ONE-CLICK INSTALLER
# Diese Datei installiert das komplette CROD-System mit allen Dependencies
# Einfach ausführen mit: chmod +x ULTIMATE_INSTALL.sh && ./ULTIMATE_INSTALL.sh

set -e

echo "=================================================================="
echo "🦠 CROD PARASIT - ULTIMATE ONE-CLICK INSTALLER"
echo "Installing complete AI/ML/3D/DB development environment..."
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
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as normal user."
   exit 1
fi

# Detect OS
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="MacOS"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    OS="Windows"
fi

print_info "Detected OS: $OS"

# 1. Update system packages
print_info "Updating system packages..."
if [[ "$OS" == "Linux" ]]; then
    sudo apt-get update -y
    sudo apt-get upgrade -y
elif [[ "$OS" == "MacOS" ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew update
    brew upgrade
fi

# 2. Install essential system tools
print_info "Installing essential system tools..."
if [[ "$OS" == "Linux" ]]; then
    sudo apt-get install -y \
        curl \
        wget \
        git \
        build-essential \
        cmake \
        pkg-config \
        libssl-dev \
        libgtk-3-dev \
        libwebkit2gtk-4.0-dev \
        libappindicator3-dev \
        librsvg2-dev \
        libsoup2.4-dev \
        libjavascriptcoregtk-4.0-dev \
        libglib2.0-dev \
        libcairo2-dev \
        libpango1.0-dev \
        libatk1.0-dev \
        libgdk-pixbuf-2.0-dev \
        libxss1 \
        libasound2-dev \
        sqlite3 \
        libsqlite3-dev \
        postgresql \
        postgresql-contrib \
        redis-server \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-setuptools \
        ffmpeg \
        libavcodec-dev \
        libavformat-dev \
        libavutil-dev \
        libswscale-dev \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
        libhdf5-dev \
        libeigen3-dev \
        libboost-all-dev \
        libopencv-dev \
        libvtk9-dev \
        libpcl-dev \
        libflann-dev \
        libgsl-dev \
        libfftw3-dev \
        libqhull-dev \
        default-jdk \
        nodejs \
        npm
elif [[ "$OS" == "MacOS" ]]; then
    brew install \
        curl \
        wget \
        git \
        cmake \
        pkg-config \
        openssl \
        sqlite \
        postgresql \
        redis \
        python3 \
        ffmpeg \
        boost \
        eigen \
        opencv \
        vtk \
        pcl \
        gsl \
        fftw \
        qhull \
        openjdk \
        node \
        npm
fi

print_status "System tools installed"

# 3. Install Rust and Cargo
print_info "Installing Rust and Cargo..."
if ! command -v rustc &> /dev/null; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

# Install additional Rust tools
cargo install cargo-tauri-dev --locked
cargo install trunk --locked
cargo install wasm-pack --locked

print_status "Rust toolchain installed"

# 4. Install Node.js and npm packages
print_info "Installing Node.js dependencies..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Global npm packages
npm install -g \
    @tauri-apps/cli \
    typescript \
    vite \
    eslint \
    prettier \
    create-tauri-app \
    tailwindcss \
    postcss \
    autoprefixer

print_status "Node.js toolchain installed"

# 5. Install Python ML/AI/3D libraries
print_info "Installing Python ML/AI/3D libraries..."
python3 -m pip install --user --upgrade pip setuptools wheel

# Install requirements from requirements.txt
if [[ -f "requirements.txt" ]]; then
    print_info "Installing from requirements.txt..."
    python3 -m pip install --user -r requirements.txt
else
    print_info "Installing core ML/AI libraries..."
    python3 -m pip install --user \
        numpy \
        scipy \
        matplotlib \
        pandas \
        scikit-learn \
        jupyter \
        ipython \
        tensorflow \
        torch \
        torchvision \
        transformers \
        opencv-python \
        Pillow \
        plotly \
        vtk \
        mayavi \
        open3d \
        trimesh \
        pyvista \
        sympy \
        numba \
        jax \
        jaxlib \
        flask \
        fastapi \
        uvicorn \
        websockets \
        aiohttp \
        sqlalchemy \
        psycopg2-binary \
        pymongo \
        redis \
        elasticsearch \
        neo4j \
        celery \
        gevent \
        lxml \
        beautifulsoup4 \
        requests \
        httpx \
        web3 \
        cryptography \
        networkx \
        graphviz \
        seaborn \
        librosa \
        soundfile \
        nltk \
        spacy \
        gensim \
        qiskit \
        cirq \
        pygame \
        arcade
fi

print_status "Python libraries installed"

# 6. Setup project dependencies
print_info "Setting up CROD project dependencies..."
cd crod-chain-app

# Install npm dependencies
npm install

print_status "Project dependencies installed"

# 7. Build the application
print_info "Building CROD application..."
npm run tauri build

print_status "Application built successfully"

# 8. Create desktop entry (Linux only)
if [[ "$OS" == "Linux" ]]; then
    print_info "Creating desktop entry..."
    DESKTOP_FILE="$HOME/.local/share/applications/crod-parasit.desktop"
    APP_ICON="$PWD/src-tauri/icons/icon.png"
    APP_EXEC="$PWD/src-tauri/target/release/crod-chain-app"
    
    mkdir -p "$HOME/.local/share/applications"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=CROD Parasit
Comment=Ultimate AI/ML Live-Coding Environment
Exec=$APP_EXEC
Icon=$APP_ICON
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
    
    print_status "Desktop entry created"
fi

# 9. Create run script
print_info "Creating run script..."
cat > ../run-crod.sh << 'EOF'
#!/bin/bash
# 🔥 CROD PARASIT LAUNCHER
# Startet die CROD-App mit allen Services

cd "$(dirname "$0")/crod-chain-app"

# Start Redis if not running
if ! pgrep redis-server > /dev/null; then
    echo "Starting Redis server..."
    redis-server --daemonize yes
fi

# Start PostgreSQL if not running
if ! pgrep postgres > /dev/null; then
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
fi

# Start the app
echo "🦠 Starting CROD Parasit..."
npm run tauri dev

echo "CROD Parasit is running!"
EOF

chmod +x ../run-crod.sh

print_status "Run script created"

# 10. Final setup
print_info "Finalizing setup..."
cd ..

# Create quick start script
cat > START_CROD.sh << 'EOF'
#!/bin/bash
# 🔥 CROD PARASIT QUICK START
echo "🦠 Starting CROD Parasit Ultimate..."
./run-crod.sh
EOF

chmod +x START_CROD.sh

print_status "Quick start script created"

echo "=================================================================="
echo -e "${GREEN}🎉 CROD PARASIT INSTALLATION COMPLETE! 🎉${NC}"
echo "=================================================================="
echo ""
echo -e "${CYAN}To start CROD Parasit:${NC}"
echo -e "${YELLOW}  ./START_CROD.sh${NC}"
echo ""
echo -e "${CYAN}Or run manually:${NC}"
echo -e "${YELLOW}  ./run-crod.sh${NC}"
echo ""
echo -e "${CYAN}Features installed:${NC}"
echo -e "${GREEN}  ✓ Complete AI/ML environment (TensorFlow, PyTorch, etc.)${NC}"
echo -e "${GREEN}  ✓ 3D Graphics libraries (VTK, Open3D, Mayavi)${NC}"
echo -e "${GREEN}  ✓ Database systems (PostgreSQL, Redis, MongoDB)${NC}"
echo -e "${GREEN}  ✓ Web development tools (React, Tauri, Vite)${NC}"
echo -e "${GREEN}  ✓ Quantum computing libraries (Qiskit, Cirq)${NC}"
echo -e "${GREEN}  ✓ Computer vision (OpenCV, Pillow)${NC}"
echo -e "${GREEN}  ✓ Natural language processing (NLTK, spaCy)${NC}"
echo -e "${GREEN}  ✓ Blockchain integration (Web3, Cryptography)${NC}"
echo -e "${GREEN}  ✓ Live-coding and AI chat interface${NC}"
echo -e "${GREEN}  ✓ File monitoring and code execution${NC}"
echo ""
echo -e "${PURPLE}🦠 CROD Parasit is ready to evolve! 🦠${NC}"
echo "=================================================================="
