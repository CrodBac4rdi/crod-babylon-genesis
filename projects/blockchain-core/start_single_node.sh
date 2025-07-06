#!/bin/bash

echo "🚀 Starting CROD Blockchain Single Node"
echo "======================================"

# Check if Elixir is installed
if ! command -v elixir &> /dev/null; then
    echo "❌ Elixir is not installed. Installing..."
    echo "Please run: sudo apt-get install elixir"
    exit 1
fi

# Get dependencies
echo "📦 Getting dependencies..."
mix deps.get

# Compile
echo "🔨 Compiling..."
mix compile

# Start the blockchain
echo "🚀 Starting blockchain node..."
iex -S mix

echo "✅ Blockchain node started!"
echo ""
echo "In IEx, try:"
echo "  {:ok, blockchain} = CROD.Blockchain.start_link()"
echo "  CROD.Blockchain.get_chain()"
echo "  CROD.Blockchain.add_block(blockchain, %{data: \"Hello CROD!\"})"