#!/bin/bash

echo "🚀 Deploying CROD Polyglot City 2025..."

# Build all images
docker-compose build --parallel

# Start services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🏥 Checking service health..."
docker-compose ps

echo "✅ CROD Polyglot City deployed!"
echo ""
echo "📍 Service URLs:"
echo "  - Rathaus (Phoenix):    http://localhost:4000"
echo "  - Parasit (Python):     ws://localhost:6666"
echo "  - Pattern (Rust):       http://localhost:7007"
echo "  - Memory (Go):          http://localhost:7031"
echo "  - Gateway (JS):         http://localhost:7888"
echo "  - Gateway Dashboard:    http://localhost:7888/dashboard"
echo "  - NATS Monitor:         http://localhost:8222"
echo ""
echo "📊 View logs: docker-compose logs -f"
