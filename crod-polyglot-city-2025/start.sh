#!/bin/bash

echo "🏙️ Starting CROD Polyglot City 2025..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build all services
echo "🔨 Building all districts..."
docker-compose build --parallel

# Start NATS first
echo "📡 Starting NATS message broker..."
docker-compose up -d nats
sleep 5

# Start all services
echo "🚀 Starting all districts..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo "📊 Checking district status..."
echo ""
echo "Phoenix Rathaus (Elixir): http://localhost:4000"
curl -s http://localhost:4000/health || echo "❌ Not responding"
echo ""
echo "Python Parasit: http://localhost:6666"
curl -s http://localhost:6666/health || echo "❌ Not responding"
echo ""
echo "Rust Pattern District: http://localhost:7007"
curl -s http://localhost:7007/health || echo "❌ Not responding"
echo ""
echo "Go Memory Quarter: http://localhost:7031"
curl -s http://localhost:7031/health || echo "❌ Not responding"
echo ""
echo "JavaScript Gateway: http://localhost:7888"
curl -s http://localhost:7888/health || echo "❌ Not responding"
echo ""

echo "✅ CROD Polyglot City is starting up!"
echo "📊 Dashboard: http://localhost:7888/dashboard"
echo "📡 NATS Monitor: http://localhost:8222"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"