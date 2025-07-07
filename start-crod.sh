#!/bin/bash

echo "🔥 Starting CROD Polyglot City 2025..."

# Build and start all services
docker-compose down
docker-compose build --parallel
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo "🌐 Services available at:"
echo "  - Phoenix Rathaus: http://localhost:4000"
echo "  - Python Parasit: http://localhost:6666"
echo "  - Rust Pattern: http://localhost:7007"
echo "  - Go Memory: http://localhost:7031"
echo "  - JS Gateway: http://localhost:7888"
echo "  - NATS Monitor: http://localhost:8222"

echo "✅ CROD Polyglot City is running!"