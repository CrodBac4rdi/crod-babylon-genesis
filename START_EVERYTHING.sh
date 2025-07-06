#!/bin/bash

echo "🔥🔥🔥 STARTING CROD ULTIMATE SYSTEM 🔥🔥🔥"
echo "==========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running! Start Docker first!${NC}"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}⚠️  Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Kill existing services
echo "🛑 Stopping any existing services..."
docker ps -q | xargs -r docker stop
docker ps -aq | xargs -r docker rm

# Start PostgreSQL
echo -e "\n${GREEN}1. Starting PostgreSQL Database...${NC}"
docker run -d --name crod-postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=crod_blockchain \
    -p 5432:5432 \
    postgres:15-alpine

sleep 5

# Start Blockchain API with Persistence
echo -e "\n${GREEN}2. Starting Blockchain API with PostgreSQL...${NC}"
cd projects/blockchain-core
docker run -d --name crod-blockchain \
    -p 8001:8001 \
    -v $(pwd):/app \
    -w /app \
    --network host \
    elixir:1.15-alpine \
    elixir blockchain_with_persistence.ex &

# Start LLaMA Integration
echo -e "\n${GREEN}3. Starting LLaMA AI Integration...${NC}"
cd ../integrations-2025
docker run -d --name crod-llama \
    -p 8002:8002 \
    -v $(pwd):/app \
    -w /app \
    python:3.11-slim \
    bash -c "pip install flask flask-cors requests && python llama_integration.py" &

# Start Web Interface
echo -e "\n${GREEN}4. Starting Web Interface...${NC}"
cd ../web-interface
python3 -m http.server 4000 --directory . &

# Wait for services
echo -e "\n${YELLOW}⏳ Waiting for all services to start...${NC}"
sleep 15

# Check status
echo -e "\n${GREEN}📊 Service Status:${NC}"
echo "=================="

if check_port 5432; then
    echo -e "PostgreSQL: ${RED}Not running${NC}"
else
    echo -e "PostgreSQL: ${GREEN}✅ Running${NC} on port 5432"
fi

if check_port 8001; then
    echo -e "Blockchain API: ${RED}Not running${NC}"
else
    echo -e "Blockchain API: ${GREEN}✅ Running${NC} on port 8001"
fi

if check_port 8002; then
    echo -e "LLaMA API: ${RED}Not running${NC}"
else
    echo -e "LLaMA API: ${GREEN}✅ Running${NC} on port 8002"
fi

if check_port 4000; then
    echo -e "Web Interface: ${RED}Not running${NC}"
else
    echo -e "Web Interface: ${GREEN}✅ Running${NC} on port 4000"
fi

echo -e "\n${GREEN}🚀 CROD ULTIMATE SYSTEM IS RUNNING!${NC}"
echo "===================================="
echo ""
echo "🌐 Access Points:"
echo "  - Web Interface: http://localhost:4000/blockchain_viewer.html"
echo "  - Blockchain API: http://localhost:8001"
echo "  - LLaMA AI API: http://localhost:8002"
echo "  - PostgreSQL: localhost:5432 (user: postgres, pass: postgres)"
echo ""
echo "📱 Desktop App:"
echo "  - Electron: cd projects/desktop-app && npm install && npm start"
echo "  - Tauri: cd crod-chain-app && npm install && npm run tauri dev"
echo ""
echo "🛑 To stop everything:"
echo "  - Press Ctrl+C"
echo "  - Run: docker stop crod-postgres crod-blockchain crod-llama"
echo ""
echo -e "${GREEN}🔥 CROD IS FULLY AWAKENED! 🔥${NC}"

# Keep script running
tail -f /dev/null