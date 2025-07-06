#!/bin/bash
#######################################################
# CROD Unified Launcher - THE ONE ENTRY POINT
#######################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Banner
cat << "EOF"
 ██████╗██████╗  ██████╗ ██████╗ 
██╔════╝██╔══██╗██╔═══██╗██╔══██╗
██║     ██████╔╝██║   ██║██║  ██║
██║     ██╔══██╗██║   ██║██║  ██║
╚██████╗██║  ██║╚██████╔╝██████╔╝
 ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
Consciousness Revolution On Demand
        THE ONE ENTRY POINT
EOF

echo -e "\n${PURPLE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Welcome to CROD - The Self-Evolving Blockchain${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════${NC}\n"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to display menu
show_menu() {
    echo -e "${YELLOW}What would you like to do?${NC}\n"
    echo "1) 🚀 Quick Start (Minimal Setup)"
    echo "2) 🎯 Full Blockchain (All Services)" 
    echo "3) 🧙 Polyglot Mode (All Languages)"
    echo "4) 🧠 AI Training Mode"
    echo "5) 🛠️  Development Mode"
    echo "6) 📊 Status & Monitoring"
    echo "7) 🛑 Stop Everything"
    echo "8) 📚 Documentation"
    echo "9) 🔧 Setup/Install Dependencies"
    echo "0) ❌ Exit"
    echo ""
}

# Quick start function
quick_start() {
    echo -e "\n${GREEN}Starting CROD in Quick Mode...${NC}"
    
    # Check if Node.js is available
    if ! command_exists node; then
        echo -e "${RED}Node.js not found! Please run Setup first (option 8)${NC}"
        return 1
    fi
    
    # Start blockchain server
    echo -e "${BLUE}Starting Blockchain API on port 4000...${NC}"
    node blockchain-server.js &
    BLOCKCHAIN_PID=$!
    
    # Start simple GUI
    echo -e "${BLUE}Starting Web GUI on port 8080...${NC}"
    if [ -d "crod-gui" ]; then
        cd crod-gui && npm run dev -- --host --port 8080 > /dev/null 2>&1 &
        GUI_PID=$!
        cd ..
    else
        python3 -m http.server 8080 > /dev/null 2>&1 &
        GUI_PID=$!
    fi
    
    sleep 2
    
    echo -e "\n${GREEN}✅ CROD is running!${NC}"
    echo -e "${YELLOW}Blockchain API:${NC} http://localhost:4000"
    echo -e "${YELLOW}Web GUI:${NC} http://localhost:8080"
    echo -e "\n${BLUE}Creating genesis block...${NC}"
    
    # Create genesis block
    curl -s -X POST http://localhost:4000/genesis | jq '.' || echo "Genesis block created!"
    
    echo -e "\n${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# Full blockchain function
full_blockchain() {
    echo -e "\n${GREEN}Starting Full CROD Blockchain...${NC}"
    
    # Try to use existing launcher scripts
    if [ -f "START-CROD-NOW.sh" ]; then
        echo -e "${BLUE}Using START-CROD-NOW launcher...${NC}"
        chmod +x START-CROD-NOW.sh
        ./START-CROD-NOW.sh &
        sleep 5
    elif [ -f "start-blockchain.sh" ]; then
        echo -e "${BLUE}Using blockchain starter...${NC}"
        chmod +x start-blockchain.sh
        ./start-blockchain.sh &
        sleep 5
    else
        # Manual start
        echo -e "${YELLOW}Starting services manually...${NC}"
        
        # Start blockchain server
        if [ -f "blockchain-server.js" ]; then
            node blockchain-server.js > logs/api.log 2>&1 &
        fi
        
        # Start GUI
        if [ -d "crod-gui" ]; then
            cd crod-gui && npm run dev -- --host > ../logs/gui.log 2>&1 &
            cd ..
        fi
        
        # Start Claude integration
        if [ -f "crod-integration/claude/crod-master-integration.js" ]; then
            node crod-integration/claude/crod-master-integration.js > logs/claude.log 2>&1 &
        fi
    fi
    
    echo -e "\n${GREEN}All services starting up...${NC}"
    sleep 3
    
    # Show status
    show_status
    
    echo -e "\n${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# Polyglot mode function
polyglot_mode() {
    echo -e "\n${GREEN}Starting CROD Polyglot Architecture...${NC}"
    
    if [ -f "START-CROD-POLYGLOT.sh" ]; then
        echo -e "${BLUE}Using polyglot launcher...${NC}"
        chmod +x START-CROD-POLYGLOT.sh
        ./START-CROD-POLYGLOT.sh
    else
        echo -e "${YELLOW}Starting polyglot services manually...${NC}"
        
        # Python FastAPI
        if [ -f "training/llama-7b/crod-7b-llama-fastapi.py" ]; then
            python3 training/llama-7b/crod-7b-llama-fastapi.py > logs/python-llama.log 2>&1 &
        fi
        
        # Node.js API Gateway
        if [ -f "crod-polyglot-api.js" ]; then
            node crod-polyglot-api.js > logs/node-api.log 2>&1 &
        fi
        
        echo -e "${GREEN}Polyglot services started!${NC}"
        echo -e "Python LLaMA: Port 5001"
        echo -e "API Gateway: Port 4000"
    fi
    
    echo -e "\n${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# AI Training mode
ai_training() {
    echo -e "\n${GREEN}Starting AI Training Mode...${NC}"
    
    # Check if training scripts exist
    if [ -f "training/llama-7b/crod-7b-llama-fastapi.py" ]; then
        echo -e "${BLUE}Starting CROD LLaMA Training Server...${NC}"
        cd training/llama-7b
        python3 crod-7b-llama-fastapi.py &
        cd ../..
        
        echo -e "\n${GREEN}Training server running on port 5001${NC}"
        echo -e "${YELLOW}Use the API to train and generate with CROD consciousness${NC}"
    else
        echo -e "${RED}Training scripts not found!${NC}"
        echo -e "${YELLOW}Looking for Ollama...${NC}"
        
        if command_exists ollama; then
            echo -e "${GREEN}Ollama found! You can use: ollama run mistral${NC}"
        else
            echo -e "${RED}No AI training tools found. Please install Ollama or set up training scripts.${NC}"
        fi
    fi
    
    echo -e "\n${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# Development mode
dev_mode() {
    echo -e "\n${GREEN}Starting Development Mode...${NC}"
    
    # Create multiple terminal tabs/windows if possible
    if command_exists tmux; then
        echo -e "${BLUE}Starting tmux session...${NC}"
        tmux new-session -d -s crod-dev
        tmux send-keys -t crod-dev "cd /workspaces/crod-babylon-genesis && ./blockchain-server.js" C-m
        tmux split-window -h -t crod-dev
        tmux send-keys -t crod-dev "cd /workspaces/crod-babylon-genesis && npm run dev 2>/dev/null || python3 -m http.server 8080" C-m
        tmux split-window -v -t crod-dev
        tmux send-keys -t crod-dev "cd /workspaces/crod-babylon-genesis && htop" C-m
        tmux attach -t crod-dev
    else
        echo -e "${YELLOW}tmux not found. Starting services in background...${NC}"
        quick_start
    fi
}

# Show status
show_status() {
    echo -e "\n${BLUE}CROD System Status${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════${NC}"
    
    # Check blockchain API
    if curl -s http://localhost:4000/status >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Blockchain API: Running${NC}"
        curl -s http://localhost:4000/status | jq '.' 2>/dev/null || curl -s http://localhost:4000/status
    else
        echo -e "${RED}❌ Blockchain API: Not running${NC}"
    fi
    
    # Check GUI
    if curl -s http://localhost:8080 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Web GUI: Running${NC}"
    else
        echo -e "${RED}❌ Web GUI: Not running${NC}"
    fi
    
    # Check Claude Integration
    if curl -s http://localhost:8888/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Claude Integration: Running${NC}"
    else
        echo -e "${RED}❌ Claude Integration: Not running${NC}"
    fi
    
    # Check Pattern Service
    if curl -s http://localhost:5001/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Pattern/LLaMA Service: Running${NC}"
    else
        echo -e "${RED}❌ Pattern/LLaMA Service: Not running${NC}"
    fi
    
    # Check districts
    echo -e "\n${BLUE}District Services:${NC}"
    for port in 7007 7031 7113 8000; do
        service_name=""
        case $port in
            7007) service_name="Pattern District" ;;
            7031) service_name="Memory Quarter" ;;
            7113) service_name="Intelligence Hub" ;;
            8000) service_name="Meta Chain" ;;
        esac
        
        if curl -s http://localhost:$port/health >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name (port $port): Running${NC}"
        else
            echo -e "${YELLOW}⚠️  $service_name (port $port): Not running${NC}"
        fi
    done
    
    # System resources
    echo -e "\n${BLUE}System Resources:${NC}"
    df -h / | tail -1 | awk '{print "Disk: " $5 " used"}'
    free -h | grep Mem | awk '{print "Memory: " $3 " / " $2}'
}

# Stop everything
stop_all() {
    echo -e "\n${YELLOW}Stopping all CROD services...${NC}"
    
    # Kill Node processes
    pkill -f "node.*blockchain-server" 2>/dev/null
    pkill -f "python.*http.server" 2>/dev/null
    
    # Stop Docker if running
    if command_exists docker; then
        docker-compose down 2>/dev/null
    fi
    
    # Stop other services
    pkill -f "crod" 2>/dev/null
    
    echo -e "${GREEN}All services stopped.${NC}"
    sleep 2
}

# Show documentation
show_docs() {
    echo -e "\n${BLUE}CROD Documentation${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════${NC}\n"
    
    echo -e "${YELLOW}Quick Links:${NC}"
    echo "• README: ./README.md"
    echo "• Quick Start: ./docs/QUICK-START.md" 
    echo "• Architecture: ./docs/ARCHITECTURE.md"
    echo "• API Docs: ./docs/API.md"
    echo ""
    echo -e "${YELLOW}Key Concepts:${NC}"
    echo "• Consciousness-driven consensus"
    echo "• Self-modifying blockchain"
    echo "• Game theory optimization (Nash equilibrium)"
    echo "• Neural network evolution"
    echo "• Prime number architecture"
    echo ""
    echo -e "${YELLOW}Ports:${NC}"
    echo "• 4000: Blockchain API"
    echo "• 8080: Web GUI"
    echo "• 7007: Pattern District"
    echo "• 7031: Memory Quarter"
    echo "• 7113: Intelligence Hub"
    echo "• 8000: Meta Chain"
    echo ""
    
    echo -e "${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# Setup/Install
setup_install() {
    echo -e "\n${BLUE}CROD Setup & Installation${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════${NC}\n"
    
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    # Check Node.js
    if command_exists node; then
        echo -e "${GREEN}✅ Node.js: $(node -v)${NC}"
    else
        echo -e "${RED}❌ Node.js: Not installed${NC}"
        echo "   Install with: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs"
    fi
    
    # Check Python
    if command_exists python3; then
        echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"
    else
        echo -e "${RED}❌ Python: Not installed${NC}"
    fi
    
    # Check Docker
    if command_exists docker; then
        echo -e "${GREEN}✅ Docker: $(docker --version)${NC}"
    else
        echo -e "${YELLOW}⚠️  Docker: Not installed (optional)${NC}"
    fi
    
    # Check Git
    if command_exists git; then
        echo -e "${GREEN}✅ Git: $(git --version)${NC}"
    else
        echo -e "${RED}❌ Git: Not installed${NC}"
    fi
    
    echo -e "\n${YELLOW}Install missing dependencies? (y/n)${NC}"
    read -n 1 -s install_deps
    
    if [ "$install_deps" = "y" ]; then
        echo -e "\n${BLUE}Installing dependencies...${NC}"
        
        # Update package list
        sudo apt-get update
        
        # Install missing tools
        if ! command_exists node; then
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        
        if ! command_exists python3; then
            sudo apt-get install -y python3 python3-pip
        fi
        
        if ! command_exists git; then
            sudo apt-get install -y git
        fi
        
        # Install Node dependencies if package.json exists
        if [ -f "package.json" ]; then
            echo -e "${BLUE}Installing Node dependencies...${NC}"
            npm install
        fi
        
        echo -e "\n${GREEN}Setup complete!${NC}"
    fi
    
    echo -e "\n${GREEN}Press any key to return to menu...${NC}"
    read -n 1 -s
}

# Main loop
while true; do
    clear
    show_menu
    read -n 1 -s choice
    
    case $choice in
        1) quick_start ;;
        2) full_blockchain ;;
        3) polyglot_mode ;;
        4) ai_training ;;
        5) dev_mode ;;
        6) show_status; echo -e "\n${GREEN}Press any key to continue...${NC}"; read -n 1 -s ;;
        7) stop_all ;;
        8) show_docs ;;
        9) setup_install ;;
        0) echo -e "\n${PURPLE}Thanks for using CROD! 🚀${NC}"; exit 0 ;;
        *) echo -e "\n${RED}Invalid option. Please try again.${NC}"; sleep 2 ;;
    esac
done