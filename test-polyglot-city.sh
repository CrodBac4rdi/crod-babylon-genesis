#!/bin/bash
# 🏙️ CROD Polyglot City Test Script

echo "🔥 Testing CROD Polyglot City Communication 🔥"
echo "==========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test each district
test_district() {
    local name=$1
    local port=$2
    local endpoint=$3
    
    echo -ne "Testing $name... "
    
    # Port forward in background
    kubectl port-forward -n crod-polyglot svc/$name $port:$port > /dev/null 2>&1 &
    PF_PID=$!
    sleep 2
    
    # Test endpoint
    if curl -s http://localhost:$port$endpoint > /dev/null 2>&1; then
        echo -e "${GREEN}✅ ONLINE${NC}"
        curl -s http://localhost:$port$endpoint | jq . 2>/dev/null || curl -s http://localhost:$port$endpoint
    else
        echo -e "${RED}❌ OFFLINE${NC}"
    fi
    
    # Kill port forward
    kill $PF_PID 2>/dev/null
    echo ""
}

# Test all districts
echo -e "${YELLOW}🧠 Meta-Chain (Elixir)${NC}"
test_district "meta-chain" 8000 "/health"

echo -e "${YELLOW}🔍 Pattern District (Rust)${NC}"
test_district "pattern-district" 7007 "/health"

echo -e "${YELLOW}💾 Memory Quarter (Go)${NC}"
test_district "memory-quarter" 7031 "/health"

echo -e "${YELLOW}🤖 Intelligence Hub (Python)${NC}"
test_district "intelligence-hub" 7113 "/health"

echo -e "${YELLOW}🔗 Blockchain Core (Go)${NC}"
test_district "blockchain-core" 8085 "/health"

echo -e "${YELLOW}🦙 LLAMA Learning (Node.js)${NC}"
test_district "llama-learning" 8089 "/health"

echo -e "${YELLOW}🌐 Gateway${NC}"
test_district "gateway" 8080 "/health"

# Test Redis connectivity
echo -e "${YELLOW}📡 Testing Redis Pub/Sub${NC}"
kubectl exec -n crod-polyglot redis-76fc6cd69f-pjpkp -- redis-cli ping
kubectl exec -n crod-polyglot redis-76fc6cd69f-pjpkp -- redis-cli pubsub channels

echo ""
echo "🏁 Test Complete!"