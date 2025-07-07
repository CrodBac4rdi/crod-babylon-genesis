#!/bin/bash
# CROD Quick Start Script
# Gets the entire CROD system running with Phoenix orchestrator

set -e

echo "🚀 Starting CROD Babylon Genesis..."
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p polyglot/{rust,go,javascript,quantum}
mkdir -p crod-phoenix/{priv/repo/migrations,lib/crod_phoenix_web}

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres nats

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Run Phoenix setup
echo "🔥 Setting up Phoenix..."
cd crod-phoenix
mix deps.get
mix ecto.create
mix ecto.migrate
cd ..

# Start all services
echo "🌟 Starting all CROD services..."
docker-compose up -d

# Show status
echo ""
echo "✅ CROD System Started!"
echo "======================"
echo "🌐 Phoenix Dashboard: http://localhost:4000"
echo "📊 n8n Workflows: http://localhost:5678"
echo "🧠 NATS Monitoring: http://localhost:8222"
echo ""
echo "Check logs with: docker-compose logs -f"
echo "Stop with: docker-compose down"