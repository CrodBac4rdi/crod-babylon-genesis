#!/bin/bash
# Stop all CROD services cleanly

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}Stopping CROD services...${NC}"

# Kill by PID files if they exist
if [ -d "pids" ]; then
    for pidfile in pids/*.pid; do
        if [ -f "$pidfile" ]; then
            PID=$(cat "$pidfile")
            if kill -0 $PID 2>/dev/null; then
                kill $PID
                echo -e "${GREEN}✓ Stopped process $PID${NC}"
            fi
            rm "$pidfile"
        fi
    done
fi

# Fallback: Kill by name
pkill -f "blockchain-server.js"
pkill -f "crod-visualizer-bin"
pkill -f "crod-explorer-bin"
pkill -f "crod-monitor-bin"
pkill -f "npm run tauri"
pkill -f "cargo-tauri"

echo -e "${GREEN}✓ All CROD services stopped${NC}"