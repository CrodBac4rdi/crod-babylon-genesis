#!/bin/bash

echo "🚀 Starting CROD Blockchain GUI..."

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm init -y > /dev/null 2>&1
    npm install express cors > /dev/null 2>&1
fi

# Start the server
echo "🌐 Starting GUI server on http://localhost:8888"
node server.js &

# Wait a bit
sleep 2

# Open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8888
elif command -v open &> /dev/null; then
    open http://localhost:8888
fi

# Keep running
wait