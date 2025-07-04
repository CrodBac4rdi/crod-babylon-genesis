#!/bin/bash
# Development environment setup

set -e

echo "🔧 Setting up CROD development environment..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"

# Install dependencies based on OS
if [ "$OS" == "linux" ]; then
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "Installing Linux dependencies..."
        sudo apt-get update
        sudo apt-get install -y \
            build-essential \
            curl \
            wget \
            git \
            redis-server \
            postgresql \
            postgis \
            python3-pip \
            python3-venv
    fi
elif [ "$OS" == "macos" ]; then
    # macOS with Homebrew
    if command -v brew &> /dev/null; then
        echo "Installing macOS dependencies..."
        brew install \
            redis \
            postgresql \
            postgis \
            nats-server
    else
        echo "Please install Homebrew first"
        exit 1
    fi
fi

# Install language toolchains
echo ""
echo "Installing language toolchains..."

# Rust
if ! command -v rustc &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi
rustup target add wasm32-unknown-unknown
cargo install wasm-pack

# Go
if ! command -v go &> /dev/null; then
    echo "Installing Go..."
    wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    rm go1.21.5.linux-amd64.tar.gz
fi

# Node.js via nvm
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc
    nvm install 20
    nvm use 20
fi

# Elixir
if ! command -v elixir &> /dev/null; then
    echo "Installing Elixir..."
    wget https://packages.erlang-solutions.com/erlang-solutions_2.0_all.deb
    sudo dpkg -i erlang-solutions_2.0_all.deb
    sudo apt-get update
    sudo apt-get install -y esl-erlang elixir
    rm erlang-solutions_2.0_all.deb
fi

# Install NATS
if ! command -v nats-server &> /dev/null; then
    echo "Installing NATS Server..."
    wget https://github.com/nats-io/nats-server/releases/download/v2.10.14/nats-server-v2.10.14-${OS}-amd64.tar.gz
    tar -xzf nats-server-v2.10.14-${OS}-amd64.tar.gz
    sudo cp nats-server-v2.10.14-${OS}-amd64/nats-server /usr/local/bin/
    rm -rf nats-server-v2.10.14-${OS}-amd64*
fi

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Install K3s (lightweight Kubernetes)
if ! command -v kubectl &> /dev/null; then
    echo "Installing K3s..."
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    mkdir -p ~/.kube
    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
    sudo chown $(id -u):$(id -g) ~/.kube/config
fi

# Python packages
echo ""
echo "Installing Python packages..."
pip3 install --user \
    requests \
    numpy \
    pandas \
    redis \
    asyncio \
    aiohttp \
    protobuf \
    grpcio \
    pytest

# Node packages
echo ""
echo "Installing Node packages..."
npm install -g \
    typescript \
    ts-node \
    nodemon \
    jest

# Elixir packages
echo ""
echo "Setting up Elixir..."
mix local.hex --force
mix local.rebar --force

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p ~/crod-data
mkdir -p ~/.crod/logs

# Initialize databases
echo ""
echo "Initializing databases..."
sudo -u postgres createdb crod_blockchain 2>/dev/null || true
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS postgis;" crod_blockchain 2>/dev/null || true

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. Pull CROD model: ollama pull mistral:7b"
echo "3. Start development: ./scripts/start-crod.sh"
echo ""
echo "🔥 Ready to build CROD!"