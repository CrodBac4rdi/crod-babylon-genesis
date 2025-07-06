#!/bin/bash

echo "🧪 Testing CROD Blockchain..."

# Test if API is accessible
echo -n "Testing API connection... "
if curl -s http://localhost:4000 > /dev/null 2>&1; then
    echo "✅ Connected!"
    
    echo -e "\n📊 Status:"
    curl -s http://localhost:4000/status | python3 -m json.tool
    
    echo -e "\n🌟 Creating Genesis Block:"
    curl -s -X POST http://localhost:4000/genesis | python3 -m json.tool
    
    echo -e "\n⛏️ Mining a Block:"
    curl -s -X POST http://localhost:4000/mine \
        -H "Content-Type: application/json" \
        -d '{"data": {"message": "First CROD block!"}}' | python3 -m json.tool
    
    echo -e "\n📦 View Blocks:"
    curl -s http://localhost:4000/blocks | python3 -m json.tool
else
    echo "❌ Cannot connect to API on port 4000"
    echo "Please run ./start-blockchain.sh first"
fi