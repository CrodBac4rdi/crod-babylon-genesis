#!/bin/bash

# START CROD - Always Active Mode
# Startet CROD und hält es immer aktiv

echo "🚀 Starting CROD Always Active..."
echo ""

cd "/home/daniel/Schreibtisch/Crod Programming"

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js first: sudo apt install nodejs"
    exit 1
fi

# Run CROD Always Active
node crod-always-active.js

# Alternative: Run in background
# To run in background, uncomment the next line and comment the line above:
# nohup node crod-always-active.js > crod.log 2>&1 &
# echo "✅ CROD running in background. Check crod.log for output."