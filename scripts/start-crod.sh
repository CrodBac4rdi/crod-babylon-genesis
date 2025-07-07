#!/bin/bash

echo "🧬 Starting CROD Polyglot System..."

# Check if Llama is installed
if command -v ollama &> /dev/null; then
    echo "🦙 Llama detected"
    # Pull llama2 if not exists
    ollama pull llama2 2>/dev/null || echo "Llama2 already downloaded"
else
    echo "⚠️  Llama not installed. Install with:"
    echo "   curl -fsSL https://ollama.com/install.sh | sh"
    echo "   ollama pull llama2"
fi

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start CROD
echo "🚀 Starting CROD..."
node CROD.js start