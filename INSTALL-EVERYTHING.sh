#!/bin/bash

# CROD MEGA INSTALLER - ALLES AUF EINMAL!
# Installiert ALLES was wir brauchen

set -e

echo "
╔═══════════════════════════════════════════╗
║       CROD MEGA INSTALLER v1.0            ║
║    Installing EVERYTHING you need!        ║
╚═══════════════════════════════════════════╝
"

# Check if running as sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run with sudo: sudo $0"
    exit 1
fi

echo "🔧 Updating package lists..."
apt update

echo ""
echo "📦 Installing development tools..."

# Core tools
apt install -y \
    curl \
    wget \
    git \
    build-essential \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common

# Programming languages
echo ""
echo "🦀 Installing Rust..."
if ! command -v cargo &> /dev/null; then
    apt install -y cargo rustc
else
    echo "   Rust already installed"
fi

# Go is already installed
echo ""
echo "🐹 Go already installed ✓"

# Python extras
echo ""
echo "🐍 Installing Python extras..."
apt install -y python3-pip python3-venv python3-dev

# Node.js (latest LTS)
echo ""
echo "📗 Installing Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
    apt install -y nodejs
else
    echo "   Node.js already installed"
fi

# Docker (if not installed)
echo ""
echo "🐳 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "   Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker daniel
else
    echo "   Docker already installed ✓"
fi

# Kubernetes tools
echo ""
echo "☸️  Installing Kubernetes tools..."

# kubectl
if ! command -v kubectl &> /dev/null; then
    echo "   Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
else
    echo "   kubectl already installed ✓"
fi

# k3s (lightweight Kubernetes)
if ! command -v k3s &> /dev/null; then
    echo "   Installing k3s..."
    curl -sfL https://get.k3s.io | sh -
    # Make kubectl use k3s
    mkdir -p /home/daniel/.kube
    cp /etc/rancher/k3s/k3s.yaml /home/daniel/.kube/config
    chown -R daniel:daniel /home/daniel/.kube
else
    echo "   k3s already installed ✓"
fi

# Helm (K8s package manager)
if ! command -v helm &> /dev/null; then
    echo "   Installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
else
    echo "   Helm already installed ✓"
fi

# Additional useful tools
echo ""
echo "🛠️  Installing additional tools..."
apt install -y \
    jq \
    htop \
    tmux \
    httpie \
    ripgrep \
    fzf \
    bat \
    ncdu \
    tldr

# VS Code extensions (if code CLI is available)
echo ""
if command -v code &> /dev/null; then
    echo "📝 Installing VS Code extensions..."
    
    # Install extensions as user daniel
    sudo -u daniel bash << 'EOF'
    # Kubernetes
    code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
    
    # Docker
    code --install-extension ms-azuretools.vscode-docker
    
    # Programming languages
    code --install-extension rust-lang.rust-analyzer
    code --install-extension golang.go
    code --install-extension ms-python.python
    code --install-extension JakeBecker.elixir-ls
    
    # Git
    code --install-extension eamodio.gitlens
    code --install-extension mhutchie.git-graph
    
    # AI/Copilot
    code --install-extension GitHub.copilot
    code --install-extension GitHub.copilot-chat
    
    # General productivity
    code --install-extension esbenp.prettier-vscode
    code --install-extension dbaeumer.vscode-eslint
    code --install-extension usernamehw.errorlens
    code --install-extension wayou.vscode-todo-highlight
    code --install-extension gruntfuggly.todo-tree
    
    # Themes
    code --install-extension PKief.material-icon-theme
    code --install-extension zhuangtongfa.material-theme
EOF
else
    echo "⚠️  VS Code not found, skipping extensions"
fi

# Fix permissions
echo ""
echo "🔐 Fixing permissions..."
chown -R daniel:daniel /home/daniel/Schreibtisch/Crod\ Programming/

# Docker post-install
if [ -S /var/run/docker.sock ]; then
    chmod 666 /var/run/docker.sock
fi

# Summary
echo ""
echo "
╔═══════════════════════════════════════════╗
║         INSTALLATION COMPLETE!            ║
╚═══════════════════════════════════════════╝

✅ Installed/Verified:
   - Rust & Cargo
   - Go
   - Node.js
   - Python extras
   - Docker
   - kubectl
   - k3s (Kubernetes)
   - Helm
   - VS Code extensions
   - Development tools

🚀 Next steps:
   1. Log out and back in (for docker group)
   2. Run: cd /home/daniel/Schreibtisch/Crod\\ Programming/CROD-Helper-Member-7
   3. Run: ./build-all-images.sh
   4. Run: ./deploy-to-k8s.sh

📝 Check k3s status:
   sudo systemctl status k3s
   kubectl get nodes
"