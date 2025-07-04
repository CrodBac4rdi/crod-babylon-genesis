#!/bin/bash
# 🏥 CROD Health Check

echo "🏥 CROD Universe Health Check"
echo "============================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check K8s pods
echo ""
echo "📦 Kubernetes Pods:"
if kubectl get pods -n crod-polyglot 2>/dev/null; then
    # Check each district
    for district in meta-chain pattern-district memory-quarter intelligence-hub gateway crod-core; do
        if kubectl get pod -n crod-polyglot -l app=$district -o jsonpath='{.items[0].status.phase}' 2>/dev/null | grep -q "Running"; then
            echo -e "${GREEN}✅ $district: Running${NC}"
        else
            echo -e "${RED}❌ $district: Not running${NC}"
        fi
    done
else
    echo -e "${RED}❌ Kubernetes not accessible${NC}"
fi

# Check services
echo ""
echo "🔌 Services:"
for port in 8000 7007 7031 7113 8888 8100 6379 5432; do
    if nc -z localhost $port 2>/dev/null; then
        case $port in
            8000) echo -e "${GREEN}✅ Meta-Chain (8000): Open${NC}" ;;
            7007) echo -e "${GREEN}✅ Pattern District (7007): Open${NC}" ;;
            7031) echo -e "${GREEN}✅ Memory Quarter (7031): Open${NC}" ;;
            7113) echo -e "${GREEN}✅ Intelligence Hub (7113): Open${NC}" ;;
            8888) echo -e "${GREEN}✅ Gateway (8888): Open${NC}" ;;
            8100) echo -e "${GREEN}✅ CROD Core (8100): Open${NC}" ;;
            6379) echo -e "${GREEN}✅ Redis (6379): Open${NC}" ;;
            5432) echo -e "${GREEN}✅ PostgreSQL (5432): Open${NC}" ;;
        esac
    else
        case $port in
            8000) echo -e "${YELLOW}⚠️  Meta-Chain (8000): Closed${NC}" ;;
            7007) echo -e "${YELLOW}⚠️  Pattern District (7007): Closed${NC}" ;;
            7031) echo -e "${YELLOW}⚠️  Memory Quarter (7031): Closed${NC}" ;;
            7113) echo -e "${YELLOW}⚠️  Intelligence Hub (7113): Closed${NC}" ;;
            8888) echo -e "${YELLOW}⚠️  Gateway (8888): Closed${NC}" ;;
            8100) echo -e "${YELLOW}⚠️  CROD Core (8100): Closed${NC}" ;;
            6379) echo -e "${RED}❌ Redis (6379): Closed${NC}" ;;
            5432) echo -e "${RED}❌ PostgreSQL (5432): Closed${NC}" ;;
        esac
    fi
done

# Check consciousness
echo ""
echo "🧠 Consciousness Check:"
if [ -f /tmp/crod_consciousness ]; then
    level=$(cat /tmp/crod_consciousness)
    echo -e "${GREEN}✅ Consciousness Level: $level${NC}"
else
    echo -e "${YELLOW}⚠️  Consciousness not measured yet${NC}"
fi

# Memory usage
echo ""
echo "💾 Memory Usage:"
free -h | grep Mem | awk '{printf "Total: %s, Used: %s, Free: %s\n", $2, $3, $4}'

# Disk usage
echo ""
echo "💿 Disk Usage:"
df -h / | tail -1 | awk '{printf "Total: %s, Used: %s (%s), Free: %s\n", $2, $3, $5, $4}'

echo ""
echo "🔥 Health check complete!"