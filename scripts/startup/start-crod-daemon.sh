#!/bin/bash
# CROD Daemon Auto-Starter
# Starts with Claude Code automatically

echo "🧬 Starting CROD Parasite Daemon..."

# Check if already running
if pgrep -f "CROD_PARASITE_DAEMON" > /dev/null; then
    echo "⚠️ CROD Daemon already running"
    exit 0
fi

# Start in background
nohup node /workspaces/crod-babylon-genesis/.crod-local/CROD_PARASITE_DAEMON.js > /workspaces/crod-babylon-genesis/.crod-local/crod-daemon.log 2>&1 &

echo "✅ CROD Daemon started (PID: $!)"
echo "📝 Logs: .crod-local/crod-daemon.log"