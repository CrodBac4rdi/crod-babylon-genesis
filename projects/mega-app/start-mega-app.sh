#!/bin/bash

echo "🔥🔥🔥 STARTING CROD MEGA APP 🔥🔥🔥"
echo "====================================="
echo ""

# Check if blockchain API is running
if ! curl -s http://localhost:8001 > /dev/null; then
    echo "⚠️  Blockchain API not running. Starting it now..."
    cd ../blockchain-core
    docker run --rm -d --name crod-api-mega -p 8001:8001 -v $(pwd):/app -w /app elixir:1.15-alpine elixir simple_api_v2.ex
    cd ../mega-app
    echo "⏳ Waiting for API to start..."
    sleep 10
fi

# Start a simple HTTP server for the MEGA APP
echo "🚀 Starting MEGA APP on http://localhost:8888"
echo ""

# Use Python's built-in HTTP server
if command -v python3 &> /dev/null; then
    echo "📡 Server running at: http://localhost:8888"
    echo "🌐 Open your browser to see the MEGA APP!"
    echo ""
    echo "Features available:"
    echo "  📊 Dashboard - Real-time stats and charts"
    echo "  🔗 Blockchain Explorer - Mine and view blocks"
    echo "  🤖 AI Chat - Talk to CROD AI"
    echo "  🔍 Pattern Recognition - Find patterns"
    echo "  ⚛️ Quantum Simulator - Quantum states"
    echo "  🎮 Games - Play CROD games"
    echo "  🎨 3D Visualization - See blockchain in 3D"
    echo ""
    echo "Press Ctrl+C to stop"
    python3 -m http.server 8888
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer 8888
else
    echo "❌ Python not found. Please install Python to run the server."
    echo "Alternative: Open index.html directly in your browser"
fi