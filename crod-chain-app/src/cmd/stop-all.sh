#!/bin/bash
# Stop all CROD services

pkill -f "npm run tauri"
pkill -f "cargo-tauri"
echo "CROD stopped"