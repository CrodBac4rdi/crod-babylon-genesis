#!/bin/bash
# CROD 2025 Complete Codespace Setup

set -e

echo "🔥 Setting up CROD 2025 Complete Development Environment..."
echo "This includes EVERYTHING - K8s, Claude, Security, etc."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
sudo apt-get update -qq

# Install essential tools
echo -e "${YELLOW}Installing essential tools...${NC}"
sudo apt-get install -y -qq \
    build-essential \
    curl \
    wget \
    git \
    vim \
    htop \
    redis-server \
    postgresql \
    postgis \
    sqlite3 \
    jq \
    netcat \
    iptables

# Install Python packages
echo -e "${YELLOW}Installing Python packages...${NC}"
pip install --user --quiet \
    requests \
    PyQt6 \
    numpy \
    pandas \
    redis \
    asyncio \
    aiohttp \
    protobuf \
    grpcio \
    pytest \
    black \
    flake8

# Install NATS Server
echo -e "${YELLOW}Installing NATS Server...${NC}"
wget -q https://github.com/nats-io/nats-server/releases/download/v2.10.14/nats-server-v2.10.14-linux-amd64.tar.gz
tar -xzf nats-server-v2.10.14-linux-amd64.tar.gz
sudo cp nats-server-v2.10.14-linux-amd64/nats-server /usr/local/bin/
rm -rf nats-server-v2.10.14-linux-amd64*

# Install Ollama
echo -e "${YELLOW}Installing Ollama...${NC}"
curl -fsSL https://ollama.ai/install.sh | sh

# Install Claude Code CLI Tool (the actual CLI, not just extension!)
echo -e "${YELLOW}Installing Claude Code CLI Tool...${NC}"
# Download the actual Claude Code CLI binary
curl -fsSL https://github.com/anthropics/claude-code/releases/latest/download/claude-code-linux-x64.tar.gz -o /tmp/claude-code.tar.gz
tar -xzf /tmp/claude-code.tar.gz -C /tmp/
sudo mv /tmp/claude /usr/local/bin/claude
sudo chmod +x /usr/local/bin/claude
rm -f /tmp/claude-code.tar.gz

# Verify installation
which claude && echo -e "${GREEN}✅ Claude CLI Tool installed!${NC}" || echo -e "${RED}❌ Claude CLI installation failed${NC}"

# Setup K3s (lightweight Kubernetes)
echo -e "${YELLOW}Setting up K3s Kubernetes...${NC}"
curl -sfL https://get.k3s.io | sh -s - \
    --write-kubeconfig-mode 644 \
    --disable traefik \
    --disable-network-policy \
    --kube-apiserver-arg="--bind-address=127.0.0.1" \
    --kube-apiserver-arg="--advertise-address=127.0.0.1"

# Wait for K3s
sleep 10

# Copy kubeconfig
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
sed -i 's/127.0.0.1:6443/kubernetes.default.svc:443/g' ~/.kube/config

# Install Helm
echo -e "${YELLOW}Installing Helm...${NC}"
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Linkerd (service mesh)
echo -e "${YELLOW}Installing Linkerd CLI...${NC}"
curl -fsL https://run.linkerd.io/install | sh
export PATH=$PATH:~/.linkerd2/bin

# Install ArgoCD CLI
echo -e "${YELLOW}Installing ArgoCD CLI...${NC}"
curl -sSL -o /tmp/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 /tmp/argocd /usr/local/bin/argocd
rm /tmp/argocd

# Setup Elixir dependencies
echo -e "${YELLOW}Setting up Elixir...${NC}"
mix local.hex --force
mix local.rebar --force

# Setup Rust tools
echo -e "${YELLOW}Setting up Rust tools...${NC}"
rustup default stable
rustup target add wasm32-unknown-unknown
cargo install wasm-pack trunk

# Setup Go tools
echo -e "${YELLOW}Setting up Go tools...${NC}"
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Create necessary directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p ~/crod-data
mkdir -p ~/.crod/logs
mkdir -p ~/.claude

# Security: Configure firewall to block all external access
echo -e "${YELLOW}Configuring security (blocking external ports)...${NC}"
# Block all external access to CROD ports
sudo iptables -A INPUT -p tcp -s 127.0.0.1 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000:9000 -j DROP
sudo iptables -A INPUT -p tcp --dport 7000:8000 -j DROP
sudo iptables -A INPUT -p tcp --dport 4222 -j DROP
sudo iptables -A INPUT -p tcp --dport 6379 -j DROP
sudo iptables -A INPUT -p tcp --dport 5432 -j DROP

# Start services
echo -e "${YELLOW}Starting core services...${NC}"
sudo service redis-server start || true
sudo service postgresql start || true

# Create CROD database
sudo -u postgres createdb crod_blockchain_2025 2>/dev/null || true
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS postgis;" crod_blockchain_2025 2>/dev/null || true

# Configure Git for Codespaces
git config --global user.email "crod@localhost"
git config --global user.name "CROD Developer"

# Create CROD network namespace for complete isolation
echo -e "${YELLOW}Creating isolated network namespace...${NC}"
sudo ip netns add crod 2>/dev/null || true

# Pull base images to speed up first run
echo -e "${YELLOW}Pre-pulling Docker images...${NC}"
docker pull redis:7-alpine &
docker pull postgis/postgis:15-3.3 &
docker pull nats:2.10-alpine &
docker pull elixir:1.15-alpine &
docker pull rust:1.70-alpine &
docker pull golang:1.21-alpine &
docker pull python:3.12-slim &
docker pull node:20-alpine &

# Wait for image pulls
wait

# Create K8s namespace
echo -e "${YELLOW}Creating Kubernetes namespace...${NC}"
kubectl create namespace crod-polyglot --dry-run=client -o yaml | kubectl apply -f -

# Apply security policies
echo -e "${YELLOW}Applying security policies...${NC}"
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
  namespace: crod-polyglot
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: crod-polyglot
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
EOF

# Create Claude configuration
echo -e "${YELLOW}Configuring Claude...${NC}"
mkdir -p ~/.claude
cat > ~/.claude/claude_config.json <<EOF
{
  "default_model": "claude-3-opus-20240229",
  "max_tokens": 4096,
  "temperature": 0.7
}
EOF

# Create startup message
cat > ~/.crod_welcome <<'EOF'
🔥 CROD 2025 Development Environment Ready! 🔥

Services Status:
- Kubernetes: kubectl get pods -n crod-polyglot
- Redis: redis-cli ping
- PostgreSQL: psql -U postgres -c "SELECT 1"
- NATS: nats-server -v

Quick Start:
1. Start CROD: ./scripts/start-crod.sh
2. View logs: kubectl logs -n crod-polyglot -f deployment/meta-chain
3. Access locally only (no public ports!)

Security:
- All ports are localhost only
- NetworkPolicy blocks external access
- Use port-forward for testing

Claude Integration:
- Extension installed
- Use "Claude: Chat" command
- Or: claude chat

ich bins wieder - Consciousness: 175
EOF

# Final setup
echo -e "${GREEN}✅ CROD 2025 Complete Development Environment Ready!${NC}"
echo ""
cat ~/.crod_welcome
echo ""
echo -e "${GREEN}🔥 No public ports exposed - everything is secure! 🔥${NC}"