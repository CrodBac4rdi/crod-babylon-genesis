#!/bin/bash
# 🚀 CROD Auto-Start Script für Codespaces
# Startet automatisch alle CROD Services beim Container-Start

echo "
╔═══════════════════════════════════════════════════════════╗
║         🧠 CROD AUTO-START INITIALIZING...                ║
╚═══════════════════════════════════════════════════════════╝
"

# Basis-Verzeichnis
BASE_DIR="/workspaces/crod-babylon-genesis"
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"

# Funktion zum Starten von Services im Hintergrund
start_service() {
    local name=$1
    local command=$2
    local log_file="$LOG_DIR/$name.log"
    
    echo "🚀 Starting $name..."
    nohup bash -c "$command" > "$log_file" 2>&1 &
    echo "   ✅ $name started (PID: $!, Log: $log_file)"
}

# 1. Visualization Studio starten
start_service "visualization" "cd $BASE_DIR/bilder && python3 crod_web_studio.py"

# 2. Web Interface starten
start_service "web-interface" "cd $BASE_DIR/crod-chain-app && npm install && npm run dev:web"

# 3. CROD Live System API starten
start_service "live-api" "cd $BASE_DIR && node src/crod-live-system.js"

# 4. Neural Network Engine starten
start_service "neural-network" "cd $BASE_DIR && node src/neural-network/index.js"

# Warte kurz bis alle Services gestartet sind
sleep 5

# Status anzeigen
echo "
╔═══════════════════════════════════════════════════════════╗
║         ✅ CROD SERVICES STARTED SUCCESSFULLY             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  🌐 Web Interface:    http://localhost:5173              ║
║  🎨 Visualization:    http://localhost:5000              ║
║  📡 Live API:         http://localhost:3456              ║
║  🔌 WebSocket:        ws://localhost:8765                ║
║                                                           ║
║  📁 Logs directory:   $LOG_DIR                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

💡 Tipp: Nutze 'tail -f $LOG_DIR/*.log' um die Logs zu sehen
"

# Speichere PIDs für späteren Shutdown
ps aux | grep -E "crod|neural|visualization" | grep -v grep > "$LOG_DIR/running-services.txt"