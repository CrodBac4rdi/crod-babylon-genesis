#!/bin/bash
# Start both Python Intelligence Hub and Neural Bridge

echo "🧠 Starting Intelligence Hub with Neural Bridge..."

# Start Neural Bridge in background
cd /app && npm install && node neural-bridge.js &

# Start Python app
exec gunicorn --bind 0.0.0.0:7113 --workers 2 --threads 4 app:app