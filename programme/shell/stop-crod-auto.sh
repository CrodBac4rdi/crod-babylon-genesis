#!/bin/bash
# 🛑 CROD Auto-Stop Script

echo "🛑 Stopping all CROD services..."

# Kill alle CROD-bezogenen Prozesse
pkill -f "crod_web_studio"
pkill -f "npm run dev"
pkill -f "crod-live-system"
pkill -f "neural-network"
pkill -f "crod_parasite"

echo "✅ All CROD services stopped"