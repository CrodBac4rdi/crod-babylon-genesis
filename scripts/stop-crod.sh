#!/bin/bash
# Stop CROD gracefully

echo "🛑 Stopping CROD..."

# Stop Kubernetes deployments
if command -v kubectl &> /dev/null; then
    echo "Scaling down Kubernetes deployments..."
    kubectl scale deployment --all --replicas=0 -n crod-polyglot 2>/dev/null || true
fi

# Stop Docker Compose
if [ -f docker-compose.yml ]; then
    docker-compose down
fi

# Stop standalone services
pkill -f "ollama serve" 2>/dev/null || true
pkill -f "nats-server" 2>/dev/null || true

echo "✅ CROD stopped"