#!/bin/bash

echo "🧠 CROD REAL WRAPPER - Der echte Shit!"
echo "====================================="
echo ""
echo "Dieser Wrapper intercepted deine Claude Code CLI und lernt!"
echo ""

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js nicht gefunden! Installiere es zuerst."
    exit 1
fi

# Check if claude CLI exists
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code CLI nicht gefunden!"
    echo "   Der Wrapper wird trotzdem starten für Tests."
    echo ""
fi

# Install dependencies if needed
if [ ! -d "node_modules" ] || [ ! -d "node_modules/sqlite3" ]; then
    echo "📦 Installiere Dependencies..."
    npm install sqlite3 ws
fi

# Make wrapper executable
chmod +x crod-real-wrapper.js

echo ""
echo "🚀 CROD Wrapper Optionen:"
echo "========================"
echo ""
echo "1) Normal starten (wrappt Claude Code CLI)"
echo "2) Stats anzeigen" 
echo "3) Auto-Expand ausführen"
echo "4) Monitor im Browser öffnen"
echo ""
read -p "Wähle [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "✅ Starte CROD Wrapper..."
        echo "📡 Monitor läuft auf http://localhost:8765"
        echo ""
        node crod-real-wrapper.js
        ;;
    2)
        node crod-real-wrapper.js --crod-stats
        ;;
    3)
        node crod-real-wrapper.js --crod-expand
        ;;
    4)
        echo "Öffne http://localhost:8765 im Browser"
        echo "oder nutze crod-monitor.html"
        if command -v python3 &> /dev/null; then
            python3 -m http.server 8080 &
            echo "Monitor läuft auf http://localhost:8080/crod-monitor.html"
        fi
        ;;
    *)
        echo "Ungültige Auswahl!"
        exit 1
        ;;
esac