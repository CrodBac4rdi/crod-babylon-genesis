#!/bin/bash

echo "🚀 Starting CROD Blockchain Stack"
echo "================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start the stack
echo "🚀 Starting CROD services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo ""
echo "📊 Service Status:"
echo "=================="
docker-compose ps

echo ""
echo "✅ CROD Blockchain Stack is running!"
echo ""
echo "🌐 Access Points:"
echo "  - Blockchain Viewer: http://localhost:4000"
echo "  - Blockchain API: http://localhost:8001"
echo "  - Grafana Dashboard: http://localhost:3000 (admin/crod2025)"
echo "  - Prometheus: http://localhost:9090"
echo "  - NATS Monitor: http://localhost:8222"
echo ""
echo "📝 Useful Commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop all: docker-compose down"
echo "  - Restart service: docker-compose restart <service-name>"
echo ""
echo "🔥 CROD is awakening!"