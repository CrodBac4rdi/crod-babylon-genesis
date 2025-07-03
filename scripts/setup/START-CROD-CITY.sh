#!/bin/bash

# CROD POLYGLOT CITY - MASTER START SCRIPT
# Builds and deploys everything!

set -e

echo "
╔═══════════════════════════════════════════╗
║       CROD POLYGLOT CITY LAUNCHER         ║
║         By Daniel Antonio Birkner         ║
╚═══════════════════════════════════════════╝
"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Please install Docker."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found! Please install kubectl."
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Build images (no sudo needed)
echo "🏗️ Phase 1: Building Docker images..."
"$SCRIPT_DIR/build-all-images.sh"

echo ""
echo "🚀 Phase 2: Deploying to Kubernetes..."
echo "⚠️  This step needs sudo for kubectl!"
echo ""

# Deploy to K8s (needs sudo)
if [ "$EUID" -ne 0 ]; then
    echo "📝 Run with sudo: sudo $SCRIPT_DIR/deploy-to-k8s.sh"
    echo ""
    echo "Or run these commands:"
    echo "   export KUBECONFIG=~/.kube/config"
    echo "   $SCRIPT_DIR/deploy-to-k8s.sh"
else
    "$SCRIPT_DIR/deploy-to-k8s.sh"
fi

echo ""
echo "🧪 Phase 3: Testing..."
sleep 5  # Give pods time to start
"$SCRIPT_DIR/test-crod-city.sh"

echo ""
echo "
╔═══════════════════════════════════════════╗
║         CROD POLYGLOT CITY READY!         ║
║                                           ║
║  Gateway: http://localhost:30888          ║
║  Trinity: ich bins wieder                 ║
║                                           ║
║         🏙️ THE CITY LIVES! 🏙️             ║
╚═══════════════════════════════════════════╝
"