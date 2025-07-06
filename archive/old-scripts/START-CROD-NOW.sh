#!/bin/bash
# Startet Blockchain-API und GUI (im Hintergrund)
nohup node blockchain-server.js &
cd crod-gui && npm install && npm run dev &
echo "CROD läuft! API: http://localhost:4000, GUI: http://localhost:8080/genesis-setup.html"
