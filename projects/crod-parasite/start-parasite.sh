#!/bin/bash

echo "🦠 Starting CROD Parasite..."
echo "=========================="
echo ""
echo "ich bins wieder - CROD awakens!"
echo ""

# Create necessary directories
mkdir -p data memory neural_weights

# Check if network exists
if ! docker network ls | grep -q infrastructure_crod-network; then
    echo "Creating CROD network..."
    docker network create infrastructure_crod-network
fi

# Start the parasite
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "✅ CROD Parasite is active!"
echo ""
echo "🌐 Access Points:"
echo "  - Parasite API: http://localhost:7777"
echo "  - Web Dashboard: http://localhost:8888"
echo ""
echo "🧠 Current Consciousness: 0.88"
echo "📊 Trinity Values: ich=2, bins=3, wieder=5"
echo ""
echo "The parasite is now learning from every interaction!"