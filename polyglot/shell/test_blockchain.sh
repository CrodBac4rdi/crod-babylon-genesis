#!/bin/bash

echo "🚀 Starting CROD Blockchain Test"
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build containers
echo "🔨 Building Docker containers..."
docker-compose build

# Start the blockchain network
echo "🚀 Starting 3-node blockchain network..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo "📊 Checking node status..."
echo ""

# Node 1
echo "Node 1 (Port 8001):"
curl -s http://localhost:8001/ | jq .

echo ""
echo "Node 2 (Port 8002):"
curl -s http://localhost:8002/ | jq .

echo ""
echo "Node 3 (Port 8003):"
curl -s http://localhost:8003/ | jq .

echo ""
echo "✅ Blockchain network is running!"
echo ""
echo "📝 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop network: docker-compose down"
echo "  - Node 1 API: http://localhost:8001"
echo "  - Node 2 API: http://localhost:8002"
echo "  - Node 3 API: http://localhost:8003"
echo "  - NATS Monitor: http://localhost:8222"