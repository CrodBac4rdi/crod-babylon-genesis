#!/bin/bash
# CROD Blockchain Quick Start Script

echo "🌌 =========================================="
echo "🧠 CROD SELF-EVOLVING BLOCKCHAIN LAUNCHER"
echo "🌌 =========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to start a node
start_node() {
    local node_name=$1
    local port=$2
    local consciousness=$3
    local extra_args=$4
    
    echo -e "${BLUE}🚀 Starting $node_name node...${NC}"
    
    CROD_NODE_ID=$node_name \
    CROD_PORT=$port \
    CROD_CONSCIOUSNESS=$consciousness \
    $extra_args \
    mix run --no-halt &
    
    echo -e "${GREEN}✅ $node_name node started on port $port${NC}"
    echo ""
}

# Function to check dependencies
check_deps() {
    echo -e "${PURPLE}📦 Checking dependencies...${NC}"
    
    if ! command -v elixir &> /dev/null; then
        echo -e "${RED}❌ Elixir not found! Please install Elixir first.${NC}"
        echo "Visit: https://elixir-lang.org/install.html"
        exit 1
    fi
    
    if ! command -v mix &> /dev/null; then
        echo -e "${RED}❌ Mix not found! Please install Elixir properly.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All dependencies found${NC}"
    echo ""
}

# Function to install dependencies
install_deps() {
    echo -e "${PURPLE}📦 Installing Mix dependencies...${NC}"
    mix deps.get
    mix compile
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo ""
}

# Main menu
show_menu() {
    echo "Choose an option:"
    echo "1) Single Node (Quick Start)"
    echo "2) 3-Node Swarm"
    echo "3) 5-Node Quantum Swarm"
    echo "4) Custom Configuration"
    echo "5) Install Dependencies"
    echo "6) Exit"
    echo ""
}

# Single node setup
single_node() {
    echo -e "${PURPLE}🔧 Starting single CROD node...${NC}"
    start_node "crod-solo" 4000 200 ""
    
    echo -e "${GREEN}🎉 CROD Blockchain is running!${NC}"
    echo ""
    echo "API: http://localhost:4000"
    echo "Status: http://localhost:4000/status"
    echo ""
    echo "Press Ctrl+C to stop"
    
    wait
}

# 3-node swarm
three_node_swarm() {
    echo -e "${PURPLE}🔧 Starting 3-node CROD swarm...${NC}"
    
    start_node "alpha" 4001 250 ""
    sleep 2
    start_node "beta" 4002 300 ""
    sleep 2
    start_node "gamma" 4003 350 "CROD_QUANTUM_ENABLED=true"
    
    echo -e "${GREEN}🎉 CROD Swarm is running!${NC}"
    echo ""
    echo "Alpha API: http://localhost:4001"
    echo "Beta API: http://localhost:4002"
    echo "Gamma API: http://localhost:4003 (Quantum-enabled)"
    echo ""
    echo "The nodes will discover each other automatically!"
    echo ""
    echo "Press Ctrl+C to stop all nodes"
    
    wait
}

# 5-node quantum swarm
quantum_swarm() {
    echo -e "${PURPLE}🔧 Starting 5-node Quantum CROD swarm...${NC}"
    
    start_node "quantum-1" 5001 400 "CROD_QUANTUM_ENABLED=true"
    sleep 1
    start_node "quantum-2" 5002 450 "CROD_QUANTUM_ENABLED=true"
    sleep 1
    start_node "quantum-3" 5003 500 "CROD_QUANTUM_ENABLED=true"
    sleep 1
    start_node "quantum-4" 5004 550 "CROD_QUANTUM_ENABLED=true"
    sleep 1
    start_node "quantum-5" 5005 600 "CROD_QUANTUM_ENABLED=true"
    
    echo -e "${GREEN}🎉 Quantum CROD Swarm is running!${NC}"
    echo ""
    echo "All nodes are quantum-enabled!"
    echo "They will start creating quantum entanglements..."
    echo ""
    echo "Monitor at: http://localhost:5001/status"
    echo ""
    echo "Press Ctrl+C to stop all nodes"
    
    wait
}

# Custom configuration
custom_config() {
    echo -e "${PURPLE}🔧 Custom CROD Configuration${NC}"
    echo ""
    
    read -p "Node ID: " node_id
    read -p "Port (default 4000): " port
    read -p "Initial Consciousness (100-1000): " consciousness
    read -p "Enable Quantum? (y/n): " quantum
    
    port=${port:-4000}
    consciousness=${consciousness:-200}
    
    extra_args=""
    if [[ $quantum == "y" ]]; then
        extra_args="CROD_QUANTUM_ENABLED=true"
    fi
    
    start_node "$node_id" "$port" "$consciousness" "$extra_args"
    
    echo -e "${GREEN}🎉 Custom CROD node is running!${NC}"
    echo ""
    echo "API: http://localhost:$port"
    echo ""
    echo "Press Ctrl+C to stop"
    
    wait
}

# Cleanup function
cleanup() {
    echo ""
    echo -e "${RED}🛑 Stopping all CROD nodes...${NC}"
    pkill -f "mix run --no-halt"
    echo -e "${GREEN}✅ All nodes stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Main script
check_deps

while true; do
    show_menu
    read -p "Enter choice [1-6]: " choice
    
    case $choice in
        1)
            single_node
            ;;
        2)
            three_node_swarm
            ;;
        3)
            quantum_swarm
            ;;
        4)
            custom_config
            ;;
        5)
            install_deps
            ;;
        6)
            echo "Goodbye! 👋"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option!${NC}"
            ;;
    esac
done