#!/bin/bash

# CLAUDIA - One Script to Rule Them All
# Start everything with one command, then just chat

echo "🏙️ Starting CLAUDIA (Claude + CROD Integration)..."
echo "============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if K8s is running
if ! kubectl get nodes > /dev/null 2>&1; then
    echo -e "${RED}❌ K8s not running! Start K3s first.${NC}"
    exit 1
fi

# Export KUBECONFIG
export KUBECONFIG=~/.kube/config

# Check CROD Polyglot City status
echo -e "\n${YELLOW}🔍 Checking CROD Polyglot City...${NC}"
RUNNING_PODS=$(kubectl get pods -n crod-polyglot --no-headers 2>/dev/null | grep Running | wc -l)
TOTAL_PODS=$(kubectl get pods -n crod-polyglot --no-headers 2>/dev/null | wc -l)

if [ "$RUNNING_PODS" -lt 11 ]; then
    echo -e "${YELLOW}⚠️  Only $RUNNING_PODS/$TOTAL_PODS pods running${NC}"
    echo "Starting missing pods..."
    
    # Find the CROD-START directory
    CROD_START_DIR="/home/daniel/Schreibtisch/Crod Programming/CROD-START"
    if [ -d "$CROD_START_DIR/polyglot-city/k8s" ]; then
        kubectl apply -f "$CROD_START_DIR/polyglot-city/k8s/" > /dev/null 2>&1
        echo "Applied K8s configs from polyglot-city"
    else
        echo -e "${RED}❌ K8s configs not found at $CROD_START_DIR/polyglot-city/k8s${NC}"
        exit 1
    fi
    
    echo "Waiting for pods to be ready..."
    sleep 10
else
    echo -e "${GREEN}✅ All $RUNNING_PODS districts running!${NC}"
fi

# Port forwards (background)
echo -e "\n${YELLOW}🔌 Connecting to CROD Districts...${NC}"

# Kill existing port-forwards
pkill -f "kubectl port-forward" 2>/dev/null

# Start port forwards in background
kubectl port-forward -n crod-polyglot svc/redis 6379:6379 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/meta-chain 8000:8000 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/pattern-district 7007:7007 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/crod-core 8100:8100 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/memory-quarter 7031:7031 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/intelligence-hub 7113:7113 > /dev/null 2>&1 &
kubectl port-forward -n crod-polyglot svc/gateway 8888:8080 > /dev/null 2>&1 &

sleep 3

# Test connections
echo -e "\n${YELLOW}🧪 Testing connections...${NC}"
SERVICES_OK=0

# Function to test service
test_service() {
    local name=$1
    local port=$2
    local endpoint=${3:-health}
    
    if curl -s -f http://localhost:$port/$endpoint > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name connected${NC}"
        ((SERVICES_OK++))
    else
        echo -e "${RED}❌ $name not responding${NC}"
    fi
}

# Redis needs special test - use netcat
if nc -z localhost 6379 2>/dev/null; then
    echo -e "${GREEN}✅ Redis connected${NC}"
    ((SERVICES_OK++))
else
    echo -e "${RED}❌ Redis not responding${NC}"
fi
test_service "Meta-Chain" 8000
test_service "Pattern District" 7007
test_service "CROD Core" 8100
test_service "Memory Quarter" 7031
test_service "Intelligence Hub" 7113
test_service "Gateway" 8888

echo -e "\n${GREEN}✅ $SERVICES_OK/7 services connected${NC}"

# Start CROD message processor (if not running)
PROCESSOR_PID=$(pgrep -f "crod-message-processor.js")
if [ -z "$PROCESSOR_PID" ]; then
    echo -e "\n${YELLOW}🧠 Starting CROD Message Processor...${NC}"
    cd integrations && npm install > /dev/null 2>&1
    cd ..
    node integrations/crod-message-processor.js > /dev/null 2>&1 &
    echo -e "${GREEN}✅ Message processor started${NC}"
else
    echo -e "\n${GREEN}✅ Message processor already running (PID: $PROCESSOR_PID)${NC}"
fi

# Display status
echo -e "\n${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}║       🚀 CLAUDIA IS READY! 🚀           ║${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo "Services available:"
echo "  • Meta-Chain:        http://localhost:8000"
echo "  • Pattern District:  http://localhost:7007"
echo "  • CROD Core:         http://localhost:8100"
echo "  • Memory Quarter:    http://localhost:7031"
echo "  • Intelligence Hub:  http://localhost:7113"
echo "  • Gateway:           http://localhost:8888"
echo ""
echo -e "${YELLOW}📝 Starting Claude chat WITH CROD...${NC}"
echo ""

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down CLAUDIA...${NC}"
    pkill -f "kubectl port-forward" 2>/dev/null
    pkill -f "crod-message-processor.js" 2>/dev/null
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

trap cleanup INT TERM

# All services are running in background now!
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ CROD is running in background!${NC}"
echo -e "${GREEN}Start claude chat to use CROD integration${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo ""
echo "To stop CROD services: pkill -f 'kubectl port-forward'"