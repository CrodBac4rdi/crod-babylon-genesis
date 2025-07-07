#!/bin/bash
set -e

echo "🔥 CROD Polyglot City 2025 Deployment Script"
echo "============================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/patterns data/models

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Build all services
echo "🏗️ Building all districts..."
docker-compose build --parallel

# Start NATS cluster first
echo "🚀 Starting NATS cluster..."
docker-compose up -d nats-1 nats-2 nats-3

# Wait for NATS to be healthy
echo "⏳ Waiting for NATS cluster to be ready..."
sleep 10

# Start Phoenix Rathaus
echo "🏛️ Starting Phoenix Rathaus (Orchestrator)..."
docker-compose up -d phoenix-rathaus

# Wait for Phoenix to be ready
sleep 5

# Start all other districts
echo "🏙️ Starting all districts..."
docker-compose up -d python-parasit rust-pattern go-memory

# Wait for districts to register
sleep 10

# Start JS Gateway
echo "🌉 Starting JS Gateway..."
docker-compose up -d js-gateway

echo ""
echo "✅ CROD Polyglot City is now running!"
echo ""
echo "🌐 Access points:"
echo "   - Phoenix Rathaus: http://localhost:4000"
echo "   - Python Parasit: http://localhost:5000"
echo "   - Rust Pattern: http://localhost:7007"
echo "   - Go Memory: http://localhost:7031"
echo "   - JS Gateway: http://localhost:8888"
echo "   - NATS Monitor: http://localhost:8222"
echo ""
echo "📊 Check status: docker-compose ps"
echo "📋 View logs: docker-compose logs -f [service-name]"
echo "🛑 Stop all: docker-compose down"