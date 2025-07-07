#!/bin/bash

echo "🔨 Building CROD Blockchain..."

# Install dependencies
mix deps.get

# Build escript (single executable)
mix escript.build

# Make it executable
chmod +x crod_blockchain

echo "✅ Build complete!"
echo ""
echo "Run with:"
echo "  ./crod_blockchain start    # Start 3 nodes locally"
echo "  ./crod_blockchain help     # Show all options"