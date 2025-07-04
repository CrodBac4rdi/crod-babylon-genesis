#!/bin/bash

echo "🔥 STARTING COMPLETE CROD SYSTEM..."

# Kill old processes
pkill -f "crod_mirror_websocket_server" 2>/dev/null
pkill -f "crod_ultimate_gui" 2>/dev/null

# Start WebSocket Server in background
cd "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod"
nohup python3 crod_mirror_websocket_server.py > /tmp/crod_ws.log 2>&1 &
WS_PID=$!
echo "✅ WebSocket Server PID: $WS_PID"

# Wait a bit
sleep 2

# Start GUI in background with virtual display if needed
export DISPLAY=:0
nohup python3 crod_ultimate_gui.py > /tmp/crod_gui.log 2>&1 &
GUI_PID=$!
echo "✅ GUI PID: $GUI_PID"

echo ""
echo "🔥 CROD COMPLETE SYSTEM RUNNING!"
echo "   WebSocket: ws://localhost:8765"
echo "   GUI: Running in background"
echo ""
echo "Check logs:"
echo "   tail -f /tmp/crod_ws.log"
echo "   tail -f /tmp/crod_gui.log"
echo ""
echo "Stop with: pkill -f crod_"