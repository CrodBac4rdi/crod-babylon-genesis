#!/bin/bash
# CROD Complete Startup Script

set -e

echo "🔥 Starting CROD Universe..."
echo "Consciousness Level: 175"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo "Checking prerequisites..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${YELLOW}⚠️  kubectl not found, using docker-compose fallback${NC}"
    USE_COMPOSE=true
else
    USE_COMPOSE=false
fi

# Check if Ollama is available
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama found${NC}"
    # Start Ollama if not running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "Starting Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found - CROD will use built-in logic${NC}"
fi

# Start Redis if not running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "Starting Redis..."
    redis-server --daemonize yes > /dev/null 2>&1 || true
fi

# Start NATS if available
if command -v nats-server &> /dev/null; then
    if ! pgrep -x "nats-server" > /dev/null; then
        echo "Starting NATS..."
        nats-server -js > /dev/null 2>&1 &
    fi
fi

echo ""
echo "🏗️  Building CROD Districts..."

# Build all Docker images
./scripts/build-all.sh

echo ""
echo "🚀 Deploying CROD..."

if [ "$USE_COMPOSE" = true ]; then
    # Use docker-compose for local development
    echo "Using Docker Compose..."
    docker-compose up -d
else
    # Use Kubernetes
    echo "Using Kubernetes..."
    
    # Create namespace
    kubectl create namespace crod-polyglot --dry-run=client -o yaml | kubectl apply -f -
    
    # Deploy all services
    kubectl apply -f k8s/
    
    # Wait for pods to be ready
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app=redis -n crod-polyglot --timeout=60s
    kubectl wait --for=condition=ready pod -l app=meta-chain -n crod-polyglot --timeout=60s
fi

echo ""
echo -e "${GREEN}✅ CROD is starting!${NC}"
echo ""
echo "Available services:"
echo "  - Gateway: http://localhost:30889"
echo "  - Meta-Chain: http://localhost:8000"
echo "  - Redis: localhost:6379"

if command -v nats-server &> /dev/null; then
    echo "  - NATS: localhost:4222"
fi

echo ""
echo "Commands:"
echo "  - View logs: kubectl logs -n crod-polyglot -f deployment/meta-chain"
echo "  - Check status: kubectl get pods -n crod-polyglot"
echo "  - Stop CROD: ./scripts/stop-crod.sh"
echo ""
echo "🔥 ich bins wieder - CROD is online! 🔥"