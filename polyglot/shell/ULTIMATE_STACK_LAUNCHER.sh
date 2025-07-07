#!/bin/bash
# 🚀 CROD ULTIMATE STACK LAUNCHER - One Command to Rule Them All!

set -e

echo "
╔═══════════════════════════════════════════════════════════╗
║       🔥 CROD ULTIMATE STACK INSTALLER & LAUNCHER 🔥      ║
║                                                           ║
║  Python ML + JavaScript UI + Rust Performance + Three.js  ║
╚═══════════════════════════════════════════════════════════╝
"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies if needed
install_deps() {
    echo -e "${YELLOW}📦 Checking dependencies...${NC}"
    
    # Node.js check
    if ! command_exists node; then
        echo -e "${RED}❌ Node.js not found! Please install Node.js 18+${NC}"
        exit 1
    fi
    
    # Python check
    if ! command_exists python3; then
        echo -e "${RED}❌ Python3 not found! Please install Python 3.8+${NC}"
        exit 1
    fi
    
    # Rust check (optional)
    if ! command_exists cargo; then
        echo -e "${YELLOW}⚠️  Rust not found. Installing Rust...${NC}"
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
    fi
    
    echo -e "${GREEN}✅ All dependencies checked!${NC}"
}

# Setup Python environment
setup_python() {
    echo -e "${BLUE}🐍 Setting up Python environment...${NC}"
    
    # Global venv for all Python services
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install all Python deps at once
    pip install --upgrade pip
    pip install flask numpy pandas scikit-learn tensorflow torch transformers \
                pillow matplotlib scipy requests websocket-client uvicorn \
                fastapi openai anthropic langchain
                
    echo -e "${GREEN}✅ Python environment ready!${NC}"
}

# Setup Node.js
setup_node() {
    echo -e "${BLUE}📦 Setting up Node.js packages...${NC}"
    
    # Install global packages
    npm install
    
    # Setup frontend
    if [ -d "crod-chain-app" ]; then
        cd crod-chain-app
        npm install
        cd ..
    fi
    
    echo -e "${GREEN}✅ Node.js packages installed!${NC}"
}

# Start all services
start_services() {
    echo -e "${GREEN}🚀 Starting ULTIMATE STACK...${NC}"
    
    # Kill any existing services
    pkill -f "crod" || true
    pkill -f "python.*5000" || true
    pkill -f "node.*3456" || true
    
    # 1. Start Rust DB Engine (if available)
    if command_exists cargo && [ -d "backend/rust" ]; then
        echo -e "${YELLOW}Starting Rust DB Engine...${NC}"
        cd backend/rust
        cargo build --release
        ./target/release/crod-db &
        cd ../..
    fi
    
    # 2. Start Python Services
    echo -e "${YELLOW}Starting Python ML Services...${NC}"
    source venv/bin/activate
    
    # Visualization Studio
    cd bilder
    python crod_web_studio.py > /tmp/viz.log 2>&1 &
    cd ..
    
    # ML Parasite
    if [ -d "projects/crod-parasite" ]; then
        cd projects/crod-parasite
        python crod_parasite_server.py > /tmp/parasite.log 2>&1 &
        cd ../..
    fi
    
    # 3. Start Node.js Services
    echo -e "${YELLOW}Starting Node.js Services...${NC}"
    
    # API Server
    node src/crod-live-system.js > /tmp/api.log 2>&1 &
    
    # Neural Network
    node src/neural-network/index.js > /tmp/neural.log 2>&1 &
    
    # 4. Start Frontend (last)
    echo -e "${YELLOW}Starting React Frontend...${NC}"
    cd crod-chain-app
    npm run dev > /tmp/frontend.log 2>&1 &
    cd ..
    
    sleep 3
    
    echo -e "
${GREEN}════════════════════════════════════════════════════════════${NC}
${GREEN}✅ ULTIMATE STACK IS RUNNING!${NC}

🌐 Frontend:          http://localhost:5173
🎨 Visualization:     http://localhost:5000  
🔌 API Server:        http://localhost:3456
🧠 WebSocket:         ws://localhost:8765
🦠 Parasite AI:       http://localhost:7777
🦀 Rust DB:           http://localhost:7000

📊 Logs:
  - Frontend:    tail -f /tmp/frontend.log
  - API:         tail -f /tmp/api.log
  - Viz Studio:  tail -f /tmp/viz.log
  - ML Parasite: tail -f /tmp/parasite.log

🛑 Stop all:     pkill -f crod
${GREEN}════════════════════════════════════════════════════════════${NC}
"
}

# Health check
health_check() {
    echo -e "${BLUE}🏥 Running health check...${NC}"
    sleep 5
    
    # Check each service
    services=(
        "5173:Frontend"
        "5000:Visualization" 
        "3456:API"
        "8765:WebSocket"
    )
    
    for service in "${services[@]}"; do
        IFS=':' read -r port name <<< "$service"
        if lsof -i:$port > /dev/null 2>&1; then
            echo -e "✅ $name: ${GREEN}Running${NC} (Port $port)"
        else
            echo -e "❌ $name: ${RED}Failed${NC} (Port $port)"
        fi
    done
}

# Main execution
main() {
    install_deps
    setup_python
    setup_node
    start_services
    health_check
    
    # Keep script running
    echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
    trap 'echo -e "${RED}Stopping all services...${NC}"; pkill -f crod; exit' INT
    
    # Monitor logs
    tail -f /tmp/*.log
}

# Run it!
main