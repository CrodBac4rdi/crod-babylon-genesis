#!/bin/bash

echo "Starting CROD Gateway on port 7888..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the gateway
npm start