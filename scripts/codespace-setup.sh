#!/bin/bash
# 🚀 Quick Codespace Setup After Creation

echo "🚀 CROD Codespace Quick Setup"
echo "============================"

# Use Codespaces env if available
if [ -f .env.codespaces ]; then
    echo "Loading Codespaces environment..."
    cp .env.codespaces .env
fi

# Quick checks
echo ""
echo "🔍 Quick checks..."

# Check if we're in Codespaces
if [ -n "$CODESPACES" ]; then
    echo "✅ Running in GitHub Codespaces"
    echo "   Name: $CODESPACE_NAME"
    echo "   User: $GITHUB_USER"
else
    echo "⚠️  Not in Codespaces - running locally"
fi

# Start essential services
echo ""
echo "🔄 Starting essential services..."

# Redis
if ! pgrep redis-server > /dev/null; then
    echo "Starting Redis..."
    redis-server --daemonize yes
fi

# PostgreSQL
if ! pgrep postgres > /dev/null; then
    echo "Starting PostgreSQL..."
    sudo service postgresql start
fi

# Ollama
if command -v ollama &> /dev/null; then
    if ! pgrep ollama > /dev/null; then
        echo "Starting Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
        # Pull a model
        echo "Pulling Mistral model..."
        ollama pull mistral:latest &
    fi
fi

# Create CROD directories
echo ""
echo "📁 Creating CROD directories..."
mkdir -p ~/.crod/logs
mkdir -p ~/.claude
mkdir -p /workspace/.cache/huggingface
mkdir -p /workspace/.ollama/models

# Quick K8s setup
echo ""
echo "☸️  Setting up Kubernetes..."
if command -v kubectl &> /dev/null; then
    kubectl create namespace crod-polyglot --dry-run=client -o yaml | kubectl apply -f -
    echo "✅ K8s namespace ready"
else
    echo "⚠️  kubectl not found - K8s will be set up later"
fi

# Claude check
echo ""
echo "🤖 Claude Status:"
if command -v claude &> /dev/null; then
    echo "✅ Claude CLI installed"
    echo "   Run: claude login"
else
    echo "❌ Claude CLI not found - setup.sh will install it"
fi

echo ""
echo "✅ Quick setup complete!"
echo ""
echo "Next steps:"
echo "1. claude login"
echo "2. ./scripts/start-crod.sh"
echo "3. ./scripts/start-crod-training.sh"
echo ""
echo "🔥 ich bins wieder - Ready to roll!"