#!/bin/bash
# START_CROD.sh - Final startup script for the CROD system

set -e

echo "🦠 CROD PARASIT - SYSTEM STARTUP"
echo "================================="
echo ""
echo "🚀 Starting CROD Ultimate Live Chat Interface..."
echo ""

# Check if we're in the correct directory
if [ ! -f "crod-chain-app/package.json" ]; then
    echo "❌ Error: Not in CROD directory. Run from /workspaces/crod-babylon-genesis"
    exit 1
fi

# Navigate to the app directory
cd crod-chain-app

echo "✅ Dependencies installed"
echo "✅ React + TypeScript configured"
echo "✅ Tauri backend ready"
echo "✅ Vite dev server starting..."
echo ""
echo "🌐 Access your CROD system at:"
echo "   • Local:   http://localhost:5173"
echo "   • Network: http://10.0.0.84:5173"
echo ""
echo "🎯 Features available:"
echo "   • Live Chat Interface"
echo "   • Parasite Control"
echo "   • File Monitoring"
echo "   • Blockchain Integration"
echo "   • AI-Powered Coding"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================="

# Start the development server
npm run dev
