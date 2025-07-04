#!/bin/bash
# 🛑 CROD Universe Stopper

echo "🛑 Stopping CROD Universe..."

cd "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod"

# Kill all CROD processes
echo "🧹 Terminating CROD processes..."
pkill -f "crod_python_city.py"
pkill -f "crod_parasitic_integration.py" 
pkill -f "claude_code_api.py"
pkill -f "complete_crod_system.py"

# Kill Flask servers
pkill -f "flask"

sleep 2

echo "✅ CROD Universe stopped!"
echo "💤 All districts offline"
echo "🦠 Parasite deactivated" 
echo "🤖 Claude API stopped"