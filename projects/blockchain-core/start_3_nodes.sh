#!/bin/bash

echo "🚀 Starting 3-Node P2P Blockchain"
echo "================================="

# Kill existing
docker stop crod-p2p-1 crod-p2p-2 crod-p2p-3 2>/dev/null
docker rm crod-p2p-1 crod-p2p-2 crod-p2p-3 2>/dev/null

# Start nodes
echo "🔗 Starting Node 1..."
docker run --rm -d --name crod-p2p-1 -p 8001:8001 \
  -v $(pwd):/app -w /app \
  elixir:1.15-alpine elixir simple_p2p_node.ex --port 8001 --node node1

echo "🔗 Starting Node 2..."  
docker run --rm -d --name crod-p2p-2 -p 8002:8002 \
  -v $(pwd):/app -w /app \
  elixir:1.15-alpine elixir simple_p2p_node.ex --port 8002 --node node2

echo "🔗 Starting Node 3..."
docker run --rm -d --name crod-p2p-3 -p 8003:8003 \
  -v $(pwd):/app -w /app \
  elixir:1.15-alpine elixir simple_p2p_node.ex --port 8003 --node node3

sleep 5

echo ""
echo "✅ Nodes started! Now connecting them..."
echo ""

# Connect nodes
echo "🔗 Connecting Node 2 to Node 1..."
curl -X POST http://localhost:8002/connect \
  -H "Content-Type: application/json" \
  -d '{"peer":"node1@localhost"}'

echo ""
echo "🔗 Connecting Node 3 to Node 1..."
curl -X POST http://localhost:8003/connect \
  -H "Content-Type: application/json" \
  -d '{"peer":"node1@localhost"}'

echo ""
echo "✅ P2P Network Ready!"
echo ""
echo "📡 Nodes:"
echo "  - http://localhost:8001"
echo "  - http://localhost:8002" 
echo "  - http://localhost:8003"
echo ""
echo "🧪 Test it:"
echo "  curl http://localhost:8001/"
echo "  curl http://localhost:8001/chain"