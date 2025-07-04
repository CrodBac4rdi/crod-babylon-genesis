#!/bin/bash

echo "🚀 Starting CROD Live Metrics Dashboard..."
echo "========================================="

cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/dashboard

# Check if ws module is installed
if ! npm list ws &>/dev/null; then
    echo "📦 Installing WebSocket module..."
    npm install ws
fi

# Kill any existing metrics server
pkill -f "node.*metrics-server.js" 2>/dev/null

# Start metrics server in background
echo "🔌 Starting metrics server on port 8889..."
node metrics-server.js &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Open dashboard in default browser
echo "🌐 Opening dashboard in browser..."
xdg-open "file://$(pwd)/crod-live-metrics.html" 2>/dev/null || \
    open "file://$(pwd)/crod-live-metrics.html" 2>/dev/null || \
    echo "⚠️  Please open manually: file://$(pwd)/crod-live-metrics.html"

echo ""
echo "✅ Dashboard running!"
echo "📊 Metrics server PID: $SERVER_PID"
echo ""
echo "To stop: kill $SERVER_PID"
echo ""

# Keep script running
wait $SERVER_PID