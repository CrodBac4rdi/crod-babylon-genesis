#!/bin/bash

echo "
╔═══════════════════════════════════════════════════════════════╗
║                    CROD BABYLON GENESIS                       ║
║                   MASTER CONTROL SCRIPT                       ║
╚═══════════════════════════════════════════════════════════════╝
"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

function show_menu() {
    echo -e "${BLUE}Was willst du starten?${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} 🚀 CROD Chain App (Web Version) - ${YELLOW}EMPFOHLEN!${NC}"
    echo -e "${GREEN}2)${NC} 🔗 Elixir Blockchain (Port 4000)"
    echo -e "${GREEN}3)${NC} 🎨 Python Visualizer (Port 5000)"
    echo -e "${GREEN}4)${NC} 📡 Mock Blockchain API (Port 3001)"
    echo -e "${GREEN}5)${NC} 🤖 CROD Parasite (Python)"
    echo -e "${GREEN}6)${NC} 🛠️  Go CLI Tools"
    echo -e "${GREEN}7)${NC} 📊 Alles auf einmal starten"
    echo -e "${GREEN}8)${NC} 📖 Projekt-Dokumentation anzeigen"
    echo -e "${GREEN}9)${NC} 🧹 Aufräumen (Kill all processes)"
    echo -e "${GREEN}0)${NC} ❌ Exit"
    echo ""
}

function start_crod_app() {
    echo -e "${YELLOW}Starting CROD Chain App...${NC}"
    cd crod-chain-app
    npm run dev:web &
    echo -e "${GREEN}✓ CROD App läuft auf http://localhost:5173${NC}"
    cd ..
}

function start_elixir_blockchain() {
    echo -e "${YELLOW}Starting Elixir Blockchain...${NC}"
    cd blockchain
    mix phx.server &
    echo -e "${GREEN}✓ Blockchain läuft auf http://localhost:4000${NC}"
    cd ..
}

function start_visualizer() {
    echo -e "${YELLOW}Starting Python Visualizer...${NC}"
    python3 crod_web_studio.py &
    echo -e "${GREEN}✓ Visualizer läuft auf http://localhost:5000${NC}"
}

function start_mock_api() {
    echo -e "${YELLOW}Starting Mock Blockchain API...${NC}"
    node blockchain-server.js &
    echo -e "${GREEN}✓ Mock API läuft auf http://localhost:3001${NC}"
}

function start_parasite() {
    echo -e "${YELLOW}Starting CROD Parasite...${NC}"
    python3 CROD_PARASITE_ULTIMATE.py &
    echo -e "${GREEN}✓ Parasite läuft im Hintergrund${NC}"
}

function start_go_tools() {
    echo -e "${YELLOW}Starting Go CLI Tools...${NC}"
    if [ -f "./crod-bin" ]; then
        ./crod-bin start &
        echo -e "${GREEN}✓ Go Tools gestartet${NC}"
    else
        echo -e "${RED}Go Tools nicht gefunden. Erst kompilieren mit: cd cmd/crod && go build -o ../../crod-bin${NC}"
    fi
}

function start_all() {
    echo -e "${PURPLE}Starting ALL THE THINGS! 🚀${NC}"
    start_crod_app
    sleep 2
    start_elixir_blockchain
    sleep 2
    start_visualizer
    sleep 1
    start_mock_api
    echo -e "${GREEN}✓ Alles läuft! Check die Ports.${NC}"
}

function show_docs() {
    echo -e "${BLUE}Projekt-Dokumentation:${NC}"
    cat PROJECT_STRUCTURE.md
}

function cleanup() {
    echo -e "${RED}Killing all CROD processes...${NC}"
    pkill -f "npm run dev"
    pkill -f "mix phx.server"
    pkill -f "python3 crod"
    pkill -f "node blockchain-server"
    pkill -f "crod-bin"
    echo -e "${GREEN}✓ Aufgeräumt!${NC}"
}

# Main loop
while true; do
    show_menu
    read -p "Deine Wahl: " choice
    
    case $choice in
        1) start_crod_app ;;
        2) start_elixir_blockchain ;;
        3) start_visualizer ;;
        4) start_mock_api ;;
        5) start_parasite ;;
        6) start_go_tools ;;
        7) start_all ;;
        8) show_docs ;;
        9) cleanup ;;
        0) echo "Bye!"; exit 0 ;;
        *) echo -e "${RED}Ungültige Wahl!${NC}" ;;
    esac
    
    echo ""
    read -p "Enter drücken für Menü..."
    clear
done