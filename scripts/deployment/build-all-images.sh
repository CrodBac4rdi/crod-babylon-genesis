#!/bin/bash

# CROD POLYGLOT CITY - Build All Docker Images
# No sudo needed for docker build!

set -e

echo "🏗️ CROD POLYGLOT CITY - Building all districts..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POD_SOURCES="$SCRIPT_DIR/pod-sources"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Build function
build_image() {
    local name=$1
    local path=$2
    
    echo "🔨 Building $name..."
    
    if [ -d "$path" ]; then
        cd "$path"
        
        # Special handling for each language
        case $name in
            "meta-chain")
                # Create empty mix.lock if not exists
                touch mix.lock
                ;;
            "memory-quarter")
                # Create go.sum if not exists
                go mod tidy 2>/dev/null || touch go.sum
                ;;
        esac
        
        # Build the image
        if docker build -t "crod/$name:latest" . ; then
            echo -e "${GREEN}✅ $name built successfully${NC}"
        else
            echo -e "${RED}❌ $name build failed${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ $name source not found at $path${NC}"
        return 1
    fi
    
    cd "$SCRIPT_DIR"
    echo ""
}

# Build all images
echo "📦 Building Docker images (no sudo needed)..."
echo ""

build_image "meta-chain" "$POD_SOURCES/meta-chain"
build_image "pattern-district" "$POD_SOURCES/pattern-district"
build_image "memory-quarter" "$POD_SOURCES/memory-quarter"
build_image "intelligence-hub" "$POD_SOURCES/intelligence-hub"
build_image "gateway" "$POD_SOURCES/gateway"
build_image "llama-learning" "$POD_SOURCES/llama-learning"
build_image "blockchain-core" "$POD_SOURCES/blockchain-core"
build_image "delta-quarter" "$POD_SOURCES/delta-quarter"

# Redis doesn't need building (using official image)
echo "📦 Redis will use official image: redis:7-alpine"
echo ""

# List built images
echo "📋 Built images:"
docker images | grep crod || echo "No CROD images found"

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Apply K8s configs: kubectl apply -f pod-configs/"
echo "   2. Check pods: kubectl get pods -n crod-polyglot"
echo "   3. Access gateway: http://localhost:30888"
echo ""
echo "🔑 For K8s deployment you'll need sudo for:"
echo "   - kubectl commands"
echo "   - If using kind/minikube setup"