#!/bin/bash

# CROD Babylon Genesis - Polyglot City 2025 Startup Script

echo "🏙️ Starting CROD Babylon Genesis Polyglot City 2025..."
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running! Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing CROD containers..."
docker-compose down 2>/dev/null

# Build and start all services
echo "🔨 Building all services..."
docker-compose build

echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
echo ""

services=(
    "nats:4222"
    "crod-rathaus:4000"
    "crod-parasit:6666" 
    "crod-pattern:7007"
    "crod-memory:7031"
    "crod-gateway:7888"
)

for service in "${services[@]}"; do
    name="${service%%:*}"
    port="${service##*:}"
    
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/health" | grep -q "200\|404"; then
        echo "✅ $name is running on port $port"
    else
        echo "❌ $name is not responding on port $port"
    fi
done

echo ""
echo "🌐 Service URLs:"
echo "==============="
echo "📊 NATS Monitor: http://localhost:8222"
echo "🏛️ Phoenix Rathaus: http://localhost:4000"
echo "🕷️ Python Parasit: http://localhost:6666/status"
echo "🔍 Rust Pattern: http://localhost:7007"
echo "💾 Go Memory: http://localhost:7031/metrics"
echo "🚪 JS Gateway: http://localhost:7888"
echo ""
echo "📝 Logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
echo ""
echo "🔥 CROD Babylon Genesis is running!"