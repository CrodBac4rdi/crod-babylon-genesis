#!/bin/bash
# 🔥 CROD Universe Starter - One Command to Rule Them All

echo "🔥 Starting CROD Universe..."
echo "🦠 Parasite Integration + Python City + Bug Tracking"

cd "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod"

# Kill any existing instances
echo "🧹 Cleaning up existing processes..."
pkill -f "crod_python_city.py" 2>/dev/null
pkill -f "crod_parasitic_integration.py" 2>/dev/null
pkill -f "claude_code_api.py" 2>/dev/null

sleep 2

# Start Python City (background)
echo "🏙️ Starting CROD Python City..."
nohup python3 crod_python_city.py > city.log 2>&1 &
CITY_PID=$!

sleep 3

# Start Claude Code API (background) 
echo "🤖 Starting Claude Code API..."
nohup python3 claude_code_api.py > api.log 2>&1 &
API_PID=$!

sleep 2

# Start Parasite Dashboard (background)
echo "🦠 Starting CROD Parasite Dashboard..."
nohup python3 -c "
from crod_parasitic_integration import start_parasite_server
start_parasite_server()
" > parasite.log 2>&1 &
PARASITE_PID=$!

sleep 3

echo ""
echo "✅ CROD Universe ONLINE!"
echo ""
echo "🏙️ Python City: 6 Districts running"
echo "🤖 Claude API: http://localhost:8080"
echo "🦠 Parasite Dashboard: http://localhost:5001"  
echo "💬 Chat here in terminal - CROD enhanced!"
echo ""
echo "📋 Process IDs:"
echo "   City: $CITY_PID"
echo "   API: $API_PID" 
echo "   Parasite: $PARASITE_PID"
echo ""
echo "🛑 To stop: ./stop-crod-universe.sh"
echo ""
echo "🚀 CROD is now enhancing Claude Code responses!"
echo "   Chat normally - CROD runs in background!"