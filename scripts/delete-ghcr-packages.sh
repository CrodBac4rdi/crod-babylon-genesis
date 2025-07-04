#!/bin/bash
# Delete all GHCR packages for crod-babylon-genesis

echo "🗑️ Deleting GitHub Container Registry packages..."

# List of packages to delete
PACKAGES=(
    "crod-babylon-genesis/pattern-district-rust"
    "crod-babylon-genesis/gateway-node"
    "crod-babylon-genesis/intelligence-hub-python"
    "crod-babylon-genesis/memory-quarter-go"
    "crod-babylon-genesis/meta-chain-elixir"
    "crod-babylon-genesis/llama-learning"
    "crod-babylon-genesis/blockchain-core"
    "crod-babylon-genesis/delta-quarter"
    "crod-babylon-genesis/crod-core"
)

for PACKAGE in "${PACKAGES[@]}"; do
    echo "Deleting $PACKAGE..."
    gh api -X DELETE "/user/packages/container/$(echo $PACKAGE | sed 's/\//%2F/g')" 2>/dev/null || echo "Failed to delete $PACKAGE"
done

echo "✅ Package cleanup complete!"