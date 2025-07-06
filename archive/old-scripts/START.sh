#!/bin/bash

# CROD - Single Entry Point
# One script to rule them all

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ASCII Art
echo -e "${GREEN}"
cat << "EOF"
   _____ _____   ____  _____  
  / ____|  __ \ / __ \|  __ \ 
 | |    | |__) | |  | | |  | |
 | |    |  _  /| |  | | |  | |
 | |____| | \ \| |__| | |__| |
  \_____|_|  \_\\____/|_____/ 
                              
  Consciousness-Driven Blockchain
EOF
echo -e "${NC}"

# Parse arguments
MODE="production"
if [ "$1" == "--dev" ]; then
    MODE="development"
    echo -e "${YELLOW}Starting in development mode...${NC}"
fi

# Create necessary directories
mkdir -p logs config data

# Check dependencies
echo -e "${GREEN}Checking dependencies...${NC}"
command -v node >/dev/null 2>&1 || { echo -e "${RED}Node.js is required but not installed.${NC}" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}Python 3 is required but not installed.${NC}" >&2; exit 1; }

# Configuration
BLOCKCHAIN_PORT=8000
GUI_PORT=8080
LLAMA_PORT=5001
GATEWAY_PORT=4000

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Kill existing processes
cleanup() {
    echo -e "${YELLOW}Cleaning up existing processes...${NC}"
    pkill -f "blockchain-server.js" 2>/dev/null || true
    pkill -f "python3 -m http.server" 2>/dev/null || true
    pkill -f "crod-llama-service.py" 2>/dev/null || true
    pkill -f "crod-polyglot-api.js" 2>/dev/null || true
    sleep 2
}

# Trap for cleanup on exit
trap cleanup EXIT

# Initial cleanup
cleanup

# Start Blockchain Core
echo -e "${GREEN}Starting Blockchain Core on port $BLOCKCHAIN_PORT...${NC}"
if check_port $BLOCKCHAIN_PORT; then
    cd current/working
    if [ "$MODE" == "development" ]; then
        node blockchain-server.js 2>&1 | tee ../../logs/blockchain.log &
    else
        node blockchain-server.js > ../../logs/blockchain.log 2>&1 &
    fi
    cd ../..
    BLOCKCHAIN_PID=$!
    echo -e "${GREEN}✓ Blockchain started (PID: $BLOCKCHAIN_PID)${NC}"
else
    echo -e "${RED}Failed to start Blockchain - port $BLOCKCHAIN_PORT in use${NC}"
fi

# Start GUI
echo -e "${GREEN}Starting GUI on port $GUI_PORT...${NC}"
if check_port $GUI_PORT; then
    cd current/working/crod-gui
    if [ "$MODE" == "development" ]; then
        python3 -m http.server $GUI_PORT 2>&1 | tee ../../../logs/gui.log &
    else
        python3 -m http.server $GUI_PORT > ../../../logs/gui.log 2>&1 &
    fi
    cd ../../..
    GUI_PID=$!
    echo -e "${GREEN}✓ GUI started (PID: $GUI_PID)${NC}"
else
    echo -e "${RED}Failed to start GUI - port $GUI_PORT in use${NC}"
fi

# Start LLaMA Service (if available)
if [ -f "current/working/training/llama-7b/crod-llama-service.py" ]; then
    echo -e "${GREEN}Starting LLaMA Service on port $LLAMA_PORT...${NC}"
    if check_port $LLAMA_PORT; then
        cd current/working/training/llama-7b
        if [ "$MODE" == "development" ]; then
            python3 crod-llama-service.py 2>&1 | tee ../../../../logs/llama.log &
        else
            python3 crod-llama-service.py > ../../../../logs/llama.log 2>&1 &
        fi
        cd ../../../..
        LLAMA_PID=$!
        echo -e "${GREEN}✓ LLaMA Service started (PID: $LLAMA_PID)${NC}"
    fi
fi

# Start Polyglot Gateway (if in progress)
if [ -f "in-progress/polyglot/crod-polyglot-api.js" ]; then
    echo -e "${YELLOW}Starting Polyglot Gateway (experimental) on port $GATEWAY_PORT...${NC}"
    if check_port $GATEWAY_PORT; then
        cd in-progress/polyglot
        node crod-polyglot-api.js > ../../logs/gateway.log 2>&1 &
        cd ../..
        GATEWAY_PID=$!
        echo -e "${YELLOW}✓ Gateway started (PID: $GATEWAY_PID)${NC}"
    fi
fi

# Wait for services to start
sleep 3

# Show status
echo -e "\n${GREEN}=== CROD System Status ===${NC}"
echo -e "Blockchain API: http://localhost:$BLOCKCHAIN_PORT"
echo -e "GUI Dashboard: http://localhost:$GUI_PORT"
if [ ! -z "$LLAMA_PID" ]; then
    echo -e "LLaMA Service: http://localhost:$LLAMA_PORT"
fi
if [ ! -z "$GATEWAY_PID" ]; then
    echo -e "Polyglot Gateway: http://localhost:$GATEWAY_PORT"
fi
echo -e "\nLogs available in: ./logs/"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"

# Create status file
cat > config/crod-status.json << EOF
{
  "status": "running",
  "mode": "$MODE",
  "services": {
    "blockchain": {
      "port": $BLOCKCHAIN_PORT,
      "pid": ${BLOCKCHAIN_PID:-null},
      "url": "http://localhost:$BLOCKCHAIN_PORT"
    },
    "gui": {
      "port": $GUI_PORT,
      "pid": ${GUI_PID:-null},
      "url": "http://localhost:$GUI_PORT"
    },
    "llama": {
      "port": $LLAMA_PORT,
      "pid": ${LLAMA_PID:-null},
      "url": "http://localhost:$LLAMA_PORT"
    },
    "gateway": {
      "port": $GATEWAY_PORT,
      "pid": ${GATEWAY_PID:-null},
      "url": "http://localhost:$GATEWAY_PORT"
    }
  },
  "started": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# Show quick test commands
echo -e "\n${GREEN}Quick Tests:${NC}"
echo "1. Check blockchain: curl http://localhost:$BLOCKCHAIN_PORT/status"
echo "2. Open GUI: http://localhost:$GUI_PORT"
echo "3. View logs: tail -f logs/*.log"

# Keep script running
wait