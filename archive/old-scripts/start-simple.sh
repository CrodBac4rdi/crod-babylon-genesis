#!/bin/bash

echo "🚀 Starting CROD Services..."

# Kill any existing processes
pkill -f "node blockchain-server.js" 2>/dev/null || true
pkill -f "python3 -m http.server" 2>/dev/null || true
pkill -f "crod-master-integration" 2>/dev/null || true

# Create logs directory
mkdir -p logs

# Start blockchain API
echo "Starting Blockchain API on port 4000..."
node blockchain-server.js > logs/blockchain.log 2>&1 &
API_PID=$!

# Start GUI
echo "Starting GUI on port 8080..."
cd crod-gui
python3 -m http.server 8080 > ../logs/gui.log 2>&1 &
GUI_PID=$!
cd ..

# Wait for services to start
sleep 3

# Test if API works
echo -e "\nTesting API..."
curl -s http://localhost:4000/status || echo "API still starting..."

echo -e "\n\n✅ Services Running:"
echo "📊 Dashboard: http://localhost:8080"
echo "🔌 API: http://localhost:4000"
echo ""
echo "Quick Commands:"
echo "- View API Status: curl http://localhost:4000/status"
echo "- Create Genesis: curl -X POST http://localhost:4000/genesis"
echo "- Mine Block: curl -X POST http://localhost:4000/mine -d '{\"data\":{\"msg\":\"test\"}}' -H 'Content-Type: application/json'"
echo ""
echo "Logs:"
echo "- tail -f logs/blockchain.log"
echo "- tail -f logs/gui.log"

echo -e "\n🎮 For GitHub Codespaces:"
echo "1. Go to PORTS tab in VS Code"
echo "2. Ports 4000 and 8080 should be listed"
echo "3. Click the globe icon to open in browser"

echo -e "\nPress Ctrl+C to stop all services"

# Cleanup on exit
cleanup() {
    echo -e "\n\nStopping services..."
    kill $API_PID 2>/dev/null || true
    kill $GUI_PID 2>/dev/null || true
    echo "✅ Services stopped"
}

trap cleanup EXIT

wait