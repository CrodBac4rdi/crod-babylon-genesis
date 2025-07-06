#!/bin/bash

echo "🚀 Starting CROD P2P Blockchain Network"
echo "======================================"

# Kill any existing nodes
echo "🛑 Stopping existing nodes..."
docker stop crod-node-1 crod-node-2 crod-node-3 2>/dev/null
docker rm crod-node-1 crod-node-2 crod-node-3 2>/dev/null

# Start Node 1
echo "🔗 Starting Node 1 (Port 8001)..."
docker run --rm -d \
  --name crod-node-1 \
  --network host \
  -v $(pwd):/app \
  -w /app \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8001 --node node1

sleep 3

# Start Node 2 (connects to Node 1)
echo "🔗 Starting Node 2 (Port 8002)..."
docker run --rm -d \
  --name crod-node-2 \
  --network host \
  -v $(pwd):/app \
  -w /app \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8002 --node node2 --peers http://localhost:8001

sleep 3

# Start Node 3 (connects to both)
echo "🔗 Starting Node 3 (Port 8003)..."
docker run --rm -d \
  --name crod-node-3 \
  --network host \
  -v $(pwd):/app \
  -w /app \
  elixir:1.15-alpine \
  elixir multi_node_blockchain.ex --port 8003 --node node3 --peers http://localhost:8001,http://localhost:8002

echo ""
echo "✅ P2P Network Started!"
echo ""
echo "📡 Nodes:"
echo "  - Node 1: http://localhost:8001"
echo "  - Node 2: http://localhost:8002"
echo "  - Node 3: http://localhost:8003"
echo ""
echo "🔧 Test Commands:"
echo "  - Check node status: curl http://localhost:8001/"
echo "  - View chain: curl http://localhost:8001/chain"
echo "  - Add transaction: curl -X POST http://localhost:8001/transaction -H 'Content-Type: application/json' -d '{\"from\":\"Daniel\",\"to\":\"CROD\",\"amount\":100}'"
echo "  - Mine block: curl -X POST http://localhost:8001/mine"
echo ""
echo "📊 Monitor logs:"
echo "  - docker logs -f crod-node-1"
echo "  - docker logs -f crod-node-2"
echo "  - docker logs -f crod-node-3"