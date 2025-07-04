#!/bin/bash
# Build all CROD Docker images

set -e

echo "🔨 Building all CROD districts..."

DISTRICTS=(
    "meta-chain"
    "pattern-district"
    "memory-quarter"
    "intelligence-hub"
    "gateway"
    "crod-core"
)

# Build blockchain core
echo "Building blockchain-core..."
docker build -t crod/blockchain-core:latest ./blockchain-core/

# Build neural network
echo "Building neural-network..."
docker build -t crod/neural-network:latest ./neural-network/

# Build all districts
for district in "${DISTRICTS[@]}"; do
    echo "Building $district..."
    docker build -t crod/$district:latest ./districts/$district/
done

echo ""
echo "✅ All districts built successfully!"
echo ""
echo "Images created:"
docker images | grep crod | grep latest