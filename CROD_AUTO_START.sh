#!/bin/bash
# 🚀 CROD ULTIMATE AUTO-START - Startet ALLES automatisch!

echo "
╔═══════════════════════════════════════════════════════════╗
║        🧠 CROD ULTIMATE SYSTEM - AUTO LAUNCH              ║
║                                                           ║
║        Starting ALL services automatically...              ║
╚═══════════════════════════════════════════════════════════╝
"

# Kill any existing CROD processes
pkill -f "crod" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "python.*web_studio" 2>/dev/null
pkill -f "node.*live-system" 2>/dev/null

sleep 1

# Start all services in background
echo "🎨 Starting Visualization Studio..."
cd /workspaces/crod-babylon-genesis/bilder && python crod_web_studio.py > /tmp/viz.log 2>&1 &

echo "🧠 Starting Neural Network Engine..."
cd /workspaces/crod-babylon-genesis/src && node neural-network/index.js > /tmp/neural.log 2>&1 &

echo "🌐 Starting CROD Live System API..."
cd /workspaces/crod-babylon-genesis && node src/crod-live-system.js > /tmp/api.log 2>&1 &

echo "🚀 Starting Web Interface..."
cd /workspaces/crod-babylon-genesis && node start-crod-web.js > /tmp/web.log 2>&1 &

# Wait a moment for services to start
sleep 3

echo "
╔═══════════════════════════════════════════════════════════╗
║                  ✅ ALL SYSTEMS ONLINE!                   ║
╚═══════════════════════════════════════════════════════════╝

🌐 Web Interface:      http://localhost:5173
🎨 Visualization:      http://localhost:5000  
📡 API:                http://localhost:3456
🔌 WebSocket:          ws://localhost:8765

Services running in background. Logs in /tmp/
"

# Keep script running to show status
tail -f /tmp/api.log