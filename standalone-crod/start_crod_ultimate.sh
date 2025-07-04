#!/bin/bash

echo "🔥 Starting CROD ULTIMATE SYSTEM..."
echo "=================================="

# Kill any existing CROD processes
pkill -f "crod_mirror" 2>/dev/null
pkill -f "unified_crod_main" 2>/dev/null

# Start unified CROD if not running
if ! pgrep -f "unified_crod_main" > /dev/null; then
    echo "🧠 Starting Unified CROD..."
    cd /home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod
    nohup python3 unified_crod_main.py > /tmp/unified_crod.log 2>&1 &
    sleep 2
fi

# Start WebSocket server if not running  
if ! pgrep -f "crod_mirror_websocket_server" > /dev/null; then
    echo "🌐 Starting WebSocket Server..."
    cd /home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod
    nohup python3 crod_mirror_websocket_server.py > /tmp/crod_websocket.log 2>&1 &
    sleep 2
fi

# Start the ultimate GUI
echo "🖥️  Starting CROD Ultimate GUI..."
cd /home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod
python3 crod_ultimate_gui.py &

echo ""
echo "✅ CROD ULTIMATE SYSTEM RUNNING!"
echo "   - Unified CROD: Active"
echo "   - WebSocket Server: ws://localhost:8765"
echo "   - GUI: Opening..."
echo ""
echo "📡 To send chat messages:"
echo "   python3 crod_live_mirror.py"
echo ""
echo "🔥 EVERYTHING IS CONNECTED AND PROCESSING!"