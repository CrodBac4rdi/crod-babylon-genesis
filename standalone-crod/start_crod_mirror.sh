#!/bin/bash

echo "🔥 Starting CROD Mirror System..."
echo "================================"

# Kill any existing processes
pkill -f "crod_mirror_websocket_server.py" 2>/dev/null
pkill -f "crod_mirror_system.py" 2>/dev/null

# Start WebSocket server
echo "🌐 Starting WebSocket server..."
python3 crod_mirror_websocket_server.py &
WEBSOCKET_PID=$!

# Wait for server to start
sleep 2

# Start PyQt GUI
echo "🖥️  Starting CROD Mirror GUI..."
python3 crod_mirror_system.py &
GUI_PID=$!

# Start web interface
echo "🌍 Opening web interface..."
python3 -m http.server 8080 --directory . &
HTTP_PID=$!
sleep 1
xdg-open "http://localhost:8080/crod_mirror_interface.html" 2>/dev/null || open "http://localhost:8080/crod_mirror_interface.html" 2>/dev/null

echo ""
echo "✅ CROD Mirror System running!"
echo "   WebSocket: ws://localhost:8765"
echo "   Web UI: http://localhost:8080/crod_mirror_interface.html"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap to clean shutdown
trap "echo 'Shutting down...'; kill $WEBSOCKET_PID $GUI_PID $HTTP_PID 2>/dev/null; exit" INT TERM

# Wait
wait