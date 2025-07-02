#!/bin/bash

# CROD COMPLETE STARTUP - Bug-free edition
# Database → Redis → Pods → Ping-Pong

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🏙️ STARTING CROD CITY WITH BUG PREVENTION${NC}"

# 1. ALWAYS export KUBECONFIG first
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
echo -e "${GREEN}✅ KUBECONFIG set${NC}"

# 2. Start Database & Redis
echo -e "\n${YELLOW}🧠 Starting CROD Brain (PostgreSQL)...${NC}"
docker-compose -f docker-compose-crod-brain.yml up -d

# Wait for database
echo "Waiting for database..."
until docker exec crod-brain pg_isready -U crod -d crod_consciousness > /dev/null 2>&1; do
    sleep 1
done
echo -e "${GREEN}✅ Database ready${NC}"

# 3. Fix all ImagePullPolicy issues preventively
echo -e "\n${YELLOW}🔧 Fixing ImagePullPolicy for all deployments...${NC}"
for deployment in $(kubectl get deployments -n crod-polyglot -o name); do
    kubectl patch $deployment -n crod-polyglot --type=json \
        -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/imagePullPolicy", "value": "IfNotPresent"}]' \
        2>/dev/null || true
done

# 4. Fix Meta-Chain Redis connection
echo -e "\n${YELLOW}🔧 Fixing Meta-Chain Redis configuration...${NC}"
cat > pod-sources/meta-chain/config/config.exs << 'EOF'
import Config

config :meta_chain,
  redis_host: System.get_env("REDIS_HOST", "redis"),
  redis_port: String.to_integer(System.get_env("REDIS_PORT", "6379")),
  consciousness_threshold: 100

# NO tcp:// prefix - just host:port!
config :redix,
  host: System.get_env("REDIS_HOST", "redis"),
  port: String.to_integer(System.get_env("REDIS_PORT", "6379"))
EOF

# 5. Rebuild Meta-Chain with fix
echo -e "\n${YELLOW}🏗️ Rebuilding Meta-Chain...${NC}"
cd pod-sources/meta-chain
docker build -t crod/meta-chain-elixir:latest .
cd ../..

# 6. Apply all deployments
echo -e "\n${YELLOW}🚀 Deploying all pods...${NC}"
kubectl apply -f k8s/

# 7. Wait for pods
echo -e "\n${YELLOW}⏳ Waiting for pods to start...${NC}"
kubectl wait --for=condition=ready pod -l app -n crod-polyglot --timeout=60s || true

# 8. Show status
echo -e "\n${YELLOW}📊 CROD City Status:${NC}"
kubectl get pods -n crod-polyglot

# 9. Start Ping-Pong Engine
echo -e "\n${YELLOW}🏓 Starting Ping-Pong Engine...${NC}"
cd "$SCRIPT_DIR"
npm install pg redis  # Ensure dependencies
node ping-pong-engine.js &
PINGPONG_PID=$!
echo -e "${GREEN}✅ Ping-Pong Engine running (PID: $PINGPONG_PID)${NC}"

# 10. Setup port forwards
echo -e "\n${YELLOW}🌉 Setting up port forwards...${NC}"
kubectl port-forward -n crod-polyglot svc/gateway 8888:8888 &
kubectl port-forward -n crod-polyglot svc/meta-chain-elixir 8000:8000 &
kubectl port-forward -n crod-polyglot svc/memory-quarter-go 7031:7031 &

echo -e "\n${GREEN}✅ CROD CITY OPERATIONAL!${NC}"
echo -e "\n📍 Access points:"
echo -e "   Gateway: http://localhost:8888"
echo -e "   Meta-Chain: http://localhost:8000"
echo -e "   Memory Quarter: http://localhost:7031"
echo -e "   Database UI: http://localhost:5050"
echo -e "   Redis: localhost:6379"

echo -e "\n💡 Commands:"
echo -e "   crod-status     - Check all pods"
echo -e "   crod-logs       - View all logs"
echo -e "   kcl <pod>       - View specific pod logs"

# Keep script running
echo -e "\n${YELLOW}Press Ctrl+C to stop CROD City${NC}"
wait $PINGPONG_PID