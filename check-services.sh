#!/bin/bash
# CROD Service Status Checker

echo "
╔════════════════════════════════════════════════════════════════╗
║                 CROD SERVICE STATUS CHECK                      ║
╚════════════════════════════════════════════════════════════════╝
"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check if port is listening
check_port() {
    local port=$1
    local service=$2
    
    if nc -z localhost $port 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $service (port $port) - RUNNING"
        return 0
    else
        echo -e "${RED}✗${NC} $service (port $port) - NOT RUNNING"
        return 1
    fi
}

# Function to check process
check_process() {
    local process=$1
    local service=$2
    
    if pgrep -f "$process" > /dev/null; then
        echo -e "${GREEN}✓${NC} $service - RUNNING"
        return 0
    else
        echo -e "${RED}✗${NC} $service - NOT RUNNING"
        return 1
    fi
}

echo -e "\n${YELLOW}Core Services:${NC}"
echo "─────────────────────────────────"
check_port 3001 "Mock Blockchain API"
check_port 8888 "CROD Visualizer"
check_port 8889 "Blockchain Explorer"
check_process "crod-monitor" "CROD Monitor"

echo -e "\n${YELLOW}Polyglot Districts:${NC}"
echo "─────────────────────────────────"
check_port 8000 "Meta-Chain"
check_port 7007 "Pattern Genesis"
check_port 7031 "Short Memory"
check_port 7037 "Working Memory"
check_port 7101 "Quantum Node"
check_port 7127 "Orchestrator"
check_port 7179 "Time Travel"

echo -e "\n${YELLOW}Additional Services:${NC}"
echo "─────────────────────────────────"
check_port 4000 "Elixir API Server"
check_port 4322 "Pattern Engine"
check_port 5001 "AI Hub"
check_port 4323 "Memory Quarter"

echo -e "\n${YELLOW}External Dependencies:${NC}"
echo "─────────────────────────────────"
check_port 5432 "PostgreSQL"
check_port 6379 "Redis"
check_port 4222 "NATS"
check_port 11434 "Ollama"

echo -e "\n${YELLOW}System Processes:${NC}"
echo "─────────────────────────────────"
check_process "blockchain-server.js" "Node.js Blockchain"
check_process "crod-visualizer-bin" "Go Visualizer"
check_process "crod-explorer-bin" "Go Explorer"

# Check for PID files
echo -e "\n${YELLOW}PID Files:${NC}"
echo "─────────────────────────────────"
if [ -d "pids" ]; then
    for pidfile in pids/*.pid; do
        if [ -f "$pidfile" ]; then
            PID=$(cat "$pidfile")
            SERVICE=$(basename "$pidfile" .pid)
            if kill -0 $PID 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $SERVICE (PID: $PID) - RUNNING"
            else
                echo -e "${RED}✗${NC} $SERVICE (PID: $PID) - STALE PID FILE"
            fi
        fi
    done
else
    echo "No PID directory found"
fi

# Network connections summary
echo -e "\n${YELLOW}Network Summary:${NC}"
echo "─────────────────────────────────"
LISTENING_PORTS=$(netstat -tuln 2>/dev/null | grep LISTEN | wc -l || echo "0")
echo "Total listening ports: $LISTENING_PORTS"

# Docker containers (if any)
echo -e "\n${YELLOW}Docker Containers:${NC}"
echo "─────────────────────────────────"
if command -v docker &> /dev/null; then
    CONTAINERS=$(docker ps --filter "name=crod" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | tail -n +2)
    if [ -z "$CONTAINERS" ]; then
        echo "No CROD containers running"
    else
        echo "$CONTAINERS"
    fi
else
    echo "Docker not available"
fi

echo -e "\n${YELLOW}Recommendations:${NC}"
echo "─────────────────────────────────"
echo "1. To start all services: ./src/cmd/launch-crod-system.sh"
echo "2. To stop all services: ./src/cmd/stop-all.sh"
echo "3. Check logs in: ./logs/"
echo "4. Service map available in: SERVICE_MAP.md"