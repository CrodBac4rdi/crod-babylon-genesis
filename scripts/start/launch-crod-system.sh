#!/bin/bash
# CROD INTEGRATED LAUNCHER - Startet ALLES mit NATS Integration!

cd "$(dirname "$0")/../.."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}
╔════════════════════════════════════════════════════════════════╗
║                 CROD BABYLON GENESIS v4.0                      ║
║               FULLY INTEGRATED BLOCKCHAIN SYSTEM               ║
╚════════════════════════════════════════════════════════════════╝
${NC}"

# Create necessary directories
mkdir -p logs pids

# 1. Start NATS JetStream (Message Bus)
echo -e "${YELLOW}[1/7] Starting NATS JetStream Message Bus...${NC}"
if ! pgrep -f "nats-server" > /dev/null; then
    docker run -d --name crod-nats \
        -p 4222:4222 \
        -p 8222:8222 \
        nats:latest \
        -js \
        --store_dir /data \
        --cluster_name CROD
    echo -e "${GREEN}✓ NATS running on port 4222${NC}"
else
    echo -e "${GREEN}✓ NATS already running${NC}"
fi

# 2. Start Elixir Blockchain API
echo -e "${YELLOW}[2/7] Starting Elixir Blockchain Core...${NC}"
cd src/blockchain/elixir
if [ ! -d "_build" ]; then
    mix deps.get
    mix compile
fi
elixir --name crod@localhost -S mix run --no-halt > ../../../logs/elixir.log 2>&1 &
echo $! > ../../../pids/elixir.pid
cd ../../..
sleep 3
echo -e "${GREEN}✓ Blockchain API on port 4000${NC}"

# 3. Start Mock Blockchain (Fallback)
echo -e "${YELLOW}[3/7] Starting Mock Blockchain API...${NC}"
node src/blockchain-server.js > logs/blockchain.log 2>&1 &
echo $! > pids/blockchain.pid
echo -e "${GREEN}✓ Mock API on port 3001${NC}"

# 4. Start Neural Network with Blockchain Integration
echo -e "${YELLOW}[4/7] Starting CROD Neural Network...${NC}"
node src/index.js > logs/neural.log 2>&1 &
echo $! > pids/neural.pid
echo -e "${GREEN}✓ Neural Network active${NC}"

# 5. Start Go Visualizer
echo -e "${YELLOW}[5/7] Starting System Visualizer...${NC}"
./src/cmd/crod-visualizer-bin > logs/visualizer.log 2>&1 &
echo $! > pids/visualizer.pid
echo -e "${GREEN}✓ Visualizer on port 8888${NC}"

# 6. Start Blockchain Explorer
echo -e "${YELLOW}[6/7] Starting Blockchain Explorer...${NC}"
./src/cmd/crod-explorer-bin > logs/explorer.log 2>&1 &
echo $! > pids/explorer.pid
echo -e "${GREEN}✓ Explorer on port 8889${NC}"

# 7. Start CROD Chain App (Main UI)
echo -e "${YELLOW}[7/7] Starting CROD Chain App...${NC}"
cd crod-chain-app
npm run tauri dev > ../logs/tauri.log 2>&1 &
echo $! > ../pids/tauri.pid
cd ..

# Start Health Monitor in new terminal
gnome-terminal --title="CROD Health Monitor" -- bash -c "./src/cmd/crod-monitor-bin --interval 2"

echo -e "
${GREEN}════════════════════════════════════════════════════════════════${NC}
${GREEN}✓ CROD FULLY INTEGRATED SYSTEM OPERATIONAL!${NC}
${GREEN}════════════════════════════════════════════════════════════════${NC}

${PURPLE}Message Bus:${NC}
- NATS JetStream:         nats://localhost:4222
- Monitor:                http://localhost:8222

${PURPLE}Blockchain Services:${NC}
- Elixir Blockchain API:  http://localhost:4000/api/blockchain
- Mock Blockchain API:    http://localhost:3001
- Blockchain Explorer:    http://localhost:8889

${PURPLE}System Monitoring:${NC}
- System Visualizer:      http://localhost:8888
- Health Monitor:         Running in terminal

${PURPLE}Main Application:${NC}
- CROD Chain App:         Loading...

${YELLOW}Integration Active:${NC}
✓ Neural Network → Blockchain via Interface
✓ Real-time events via NATS
✓ Consciousness-driven mining
✓ Pattern discovery → Block creation

${GREEN}The Blockchain lives INSIDE the system! 🧠⛓️${NC}
"

# Monitor integration
watch -n 5 'echo "=== NATS Streams ===" && curl -s http://localhost:8222/jsz | jq .streams'