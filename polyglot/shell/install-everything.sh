#!/bin/bash
# 🔥 CROD ULTIMATE DEPENDENCY INSTALLER
# Installiert ALLES was für die ultimative Live-Coding-Umgebung benötigt wird

echo "🦠 CROD PARASIT: Installing EVERYTHING you need!"
echo "=================================================================="

# System Dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    pkg-config \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libwebkit2gtk-4.0-dev \
    libsoup2.4-dev \
    libjavascriptcoregtk-4.0-dev \
    libglib2.0-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libatk1.0-dev \
    libgdk-pixbuf-2.0-dev \
    libxss1 \
    libasound2-dev \
    cmake \
    python3 \
    python3-pip \
    python3-dev \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    python3-pandas \
    sqlite3 \
    libsqlite3-dev \
    redis-server \
    postgresql \
    postgresql-contrib

# Rust
echo "🦀 Installing/Updating Rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env
rustup update

# Node.js (latest LTS)
echo "🟨 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python ML/AI Libraries
echo "🐍 Installing Python ML/AI libraries..."
pip3 install --user \
    numpy \
    scipy \
    matplotlib \
    pandas \
    scikit-learn \
    tensorflow \
    torch \
    torchvision \
    transformers \
    opencv-python \
    pillow \
    requests \
    flask \
    fastapi \
    uvicorn \
    websockets \
    asyncio \
    aiohttp \
    sqlalchemy \
    psycopg2-binary \
    redis \
    celery \
    jupyter \
    ipython

# 3D Libraries
echo "🎮 Installing 3D libraries..."
pip3 install --user \
    three \
    babylonjs \
    blender-bpy \
    vtk \
    mayavi \
    plotly \
    open3d

# Vector/Math Libraries
echo "🧮 Installing vector/math libraries..."
pip3 install --user \
    numpy \
    sympy \
    numba \
    cupy-cuda11x \
    jax \
    jaxlib

# Database Libraries
echo "🗄️ Installing database libraries..."
pip3 install --user \
    sqlite3 \
    pymongo \
    elasticsearch \
    neo4j \
    cassandra-driver \
    influxdb-client

# Tauri Dependencies
echo "🚀 Installing Tauri..."
cargo install tauri-cli

# Additional Rust tools
echo "🔧 Installing Rust tools..."
cargo install \
    cargo-watch \
    cargo-edit \
    cargo-expand \
    serde_json \
    tokio-tungstenite \
    warp \
    axum

echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo "=================================================================="
echo "🦠 CROD PARASIT: All dependencies installed!"
echo "🔥 You can now run: npm run tauri dev"
echo "=================================================================="
