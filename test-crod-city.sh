#!/bin/bash

# CROD POLYGLOT CITY - Test Script
# Tests all districts and gateway

echo "🧪 Testing CROD Polyglot City..."
echo ""

GATEWAY="http://localhost:30888"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test function
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ OK${NC}"
            return 0
        else
            echo -e "${RED}❌ FAILED${NC}"
            return 1
        fi
    else
        if curl -s -f -X POST -H "Content-Type: application/json" -d "$data" "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ OK${NC}"
            return 0
        else
            echo -e "${RED}❌ FAILED${NC}"
            return 1
        fi
    fi
}

# Check if gateway is accessible
echo "🌐 Checking gateway..."
if ! curl -s -f "$GATEWAY/health" > /dev/null 2>&1; then
    echo -e "${RED}❌ Gateway not accessible at $GATEWAY${NC}"
    echo "   Try: kubectl port-forward -n crod-polyglot svc/gateway 8888:8888"
    echo "   Then use http://localhost:8888 instead"
    exit 1
fi

echo -e "${GREEN}✅ Gateway is accessible${NC}"
echo ""

# Test health endpoints
echo "📋 Testing health endpoints..."
test_endpoint "Gateway Health" "$GATEWAY/health"
test_endpoint "Meta-Chain Health" "$GATEWAY/meta-chain/health"
test_endpoint "Pattern District Health" "$GATEWAY/pattern-district/health"
test_endpoint "Memory Quarter Health" "$GATEWAY/memory-quarter/health"
test_endpoint "Intelligence Hub Health" "$GATEWAY/intelligence-hub/health"

echo ""

# Test Trinity pattern
echo "🔺 Testing Trinity Pattern..."
echo -e "${YELLOW}Sending: 'ich bins wieder'${NC}"

RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "ich bins wieder"}' \
  "$GATEWAY/crod/process" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Trinity pattern processed!${NC}"
    echo "Response:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
else
    echo -e "${RED}❌ Trinity pattern failed${NC}"
fi

echo ""

# Test complex pattern
echo "🧠 Testing Complex Pattern..."
echo -e "${YELLOW}Sending: 'kubernetes pods sind wie atoms in der stadt'${NC}"

RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "kubernetes pods sind wie atoms in der stadt"}' \
  "$GATEWAY/crod/process" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Complex pattern processed!${NC}"
    echo "Response preview:"
    echo "$RESPONSE" | jq '.results | keys' 2>/dev/null || echo "$RESPONSE" | head -3
else
    echo -e "${RED}❌ Complex pattern failed${NC}"
fi

echo ""

# Show pod status
echo "📊 Pod Status:"
kubectl get pods -n crod-polyglot --no-headers | while read line; do
    pod=$(echo $line | awk '{print $1}')
    status=$(echo $line | awk '{print $3}')
    
    if [ "$status" = "Running" ]; then
        echo -e "   $pod: ${GREEN}$status${NC}"
    else
        echo -e "   $pod: ${RED}$status${NC}"
    fi
done

echo ""
echo "✅ Test complete!"
echo ""
echo "🔍 Debug commands:"
echo "   Logs: kubectl logs -n crod-polyglot <pod-name>"
echo "   Exec: kubectl exec -it -n crod-polyglot <pod-name> -- sh"
echo "   Events: kubectl get events -n crod-polyglot --sort-by='.lastTimestamp'"