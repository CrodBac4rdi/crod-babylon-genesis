#!/bin/bash

# Farben für Terminal-Ausgaben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}
╔═══════════════════════════════════════════════════════════════╗
║              CROD BABYLON GENESIS - DEV SERVER               ║
║                 POLYGLOT ARCHITECTURE STACK                  ║
╚═══════════════════════════════════════════════════════════════╝
${NC}"

# Stoppe alle laufenden Services bei CTRL+C
trap 'kill $(jobs -p) 2>/dev/null' EXIT

# Verzeichnisse erstellen falls sie nicht existieren
mkdir -p logs

# Mock-Services starten
start_mock_services() {
    echo -e "${YELLOW}Starte Mock-Services...${NC}"

    # Node.js Mock API Server (Port 3001)
    echo -e "${GREEN}Starte Node.js Mock API Server auf Port 3001...${NC}"
    node src/blockchain-server.js > logs/node-api.log 2>&1 &
    NODE_PID=$!
    echo -e "${GREEN}Node.js Mock API Server läuft mit PID $NODE_PID${NC}"

    # Python Visualizer (Port 5000)
    echo -e "${GREEN}Starte Python Visualizer auf Port 5000...${NC}"
    cd bilder && python3 crod_web_studio.py > ../logs/python-viz.log 2>&1 &
    PYTHON_PID=$!
    cd ..
    echo -e "${GREEN}Python Visualizer läuft mit PID $PYTHON_PID${NC}"

    # Frontend (Port 5173)
    echo -e "${GREEN}Starte Frontend auf Port 5173...${NC}"
    cd crod-chain-app && npm run dev:web > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}Frontend läuft mit PID $FRONTEND_PID${NC}"
    
    echo -e "${YELLOW}Alle Mock-Services wurden gestartet!${NC}"
}

# Dashboard für Service-Status
show_status_dashboard() {
    clear
    echo -e "${BLUE}
╔═══════════════════════════════════════════════════════════════╗
║                     SERVICE STATUS                           ║
╚═══════════════════════════════════════════════════════════════╝
${NC}"
    
    # Node.js API
    if ps -p $NODE_PID > /dev/null; then
        echo -e "${GREEN}[✓] Node.js API Server      (PID: $NODE_PID)   - http://localhost:3001${NC}"
    else
        echo -e "${RED}[✗] Node.js API Server      (GESTOPPT)${NC}"
    fi
    
    # Python Visualizer
    if ps -p $PYTHON_PID > /dev/null; then
        echo -e "${GREEN}[✓] Python Visualizer      (PID: $PYTHON_PID)   - http://localhost:5000${NC}"
    else
        echo -e "${RED}[✗] Python Visualizer      (GESTOPPT)${NC}"
    fi
    
    # Frontend
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}[✓] Frontend App           (PID: $FRONTEND_PID)   - http://localhost:5173${NC}"
    else
        echo -e "${RED}[✗] Frontend App           (GESTOPPT)${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Logs werden in logs/ gespeichert${NC}"
    echo -e "${YELLOW}Drücke CTRL+C um alle Services zu stoppen${NC}"
    echo ""
}

# Services starten
start_mock_services

# Status Dashboard aktualisieren (alle 5 Sekunden)
while true; do
    show_status_dashboard
    sleep 5
done
