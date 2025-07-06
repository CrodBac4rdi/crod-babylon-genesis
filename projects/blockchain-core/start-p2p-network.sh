#!/bin/bash

echo "🚀 Starting CROD P2P Blockchain Network"
echo "======================================"
echo ""

# Stop any existing nodes
echo "🛑 Stopping existing nodes..."
docker stop crod-node-1 crod-node-2 crod-node-3 2>/dev/null
docker rm crod-node-1 crod-node-2 crod-node-3 2>/dev/null

# Start 3 nodes
echo "🚀 Starting Node 1 (Port 8001)..."
docker run --rm -d --name crod-node-1 \
  -p 8001:8001 \
  -v $(pwd):/app \
  -w /app \
  --network host \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8001 --node_id node1

sleep 2

echo "🚀 Starting Node 2 (Port 8002)..."
docker run --rm -d --name crod-node-2 \
  -p 8002:8002 \
  -v $(pwd):/app \
  -w /app \
  --network host \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8002 --node_id node2 --peers "http://localhost:8001"

sleep 2

echo "🚀 Starting Node 3 (Port 8003)..."
docker run --rm -d --name crod-node-3 \
  -p 8003:8003 \
  -v $(pwd):/app \
  -w /app \
  --network host \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8003 --node_id node3 --peers "http://localhost:8001,http://localhost:8002"

sleep 5

echo ""
echo "✅ P2P Network is running!"
echo ""
echo "📊 Node Status:"
echo "==============="
echo "Node 1: http://localhost:8001"
curl -s http://localhost:8001 | jq .
echo ""
echo "Node 2: http://localhost:8002"
curl -s http://localhost:8002 | jq .
echo ""
echo "Node 3: http://localhost:8003"
curl -s http://localhost:8003 | jq .
echo ""
echo "🔗 Test Commands:"
echo "  Add transaction: curl -X POST http://localhost:8001/transactions/add -H 'Content-Type: application/json' -d '{\"from\":\"alice\",\"to\":\"bob\",\"amount\":10}'"
echo "  Mine block: curl -X POST http://localhost:8001/mine"
echo "  View chain: curl http://localhost:8001/chain | jq ."
echo ""
echo "📝 Logs:"
echo "  docker logs -f crod-node-1"
echo "  docker logs -f crod-node-2"
echo "  docker logs -f crod-node-3"