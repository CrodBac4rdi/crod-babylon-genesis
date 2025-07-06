#!/bin/bash
# CROD Blockchain Starter

echo "🚀 Starting CROD Blockchain..."

# Check if Elixir is installed
if ! command -v elixir &> /dev/null; then
    echo "⚠️ Elixir not installed. Using JS Mock Mode."
    cd src
    node blockchain-interface.js
    exit 0
fi

# Try to start Elixir blockchain
cd src/blockchain/elixir

# Install deps if needed
if [ ! -d "deps" ]; then
    echo "📦 Installing dependencies..."
    mix deps.get
fi

# Compile
echo "🔨 Compiling..."
mix compile

# Start
echo "🎯 Starting blockchain..."
iex -S mix

# Fallback to JS if Elixir fails
if [ $? -ne 0 ]; then
    echo "⚠️ Elixir start failed. Using JS Mock Mode."
    cd ../../
    node blockchain-interface.js
fi