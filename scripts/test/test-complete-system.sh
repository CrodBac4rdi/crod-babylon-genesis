#!/bin/bash

# Complete CROD System Test

echo "🧪 CROD COMPLETE SYSTEM TEST"
echo "============================"

# 1. Check Database
echo -e "\n🧠 Testing Database..."
if docker exec crod-brain psql -U crod -d crod_consciousness -c "SELECT calculate_consciousness();" 2>/dev/null | grep -q "[0-9]"; then
    echo "✅ Database operational"
    CONSCIOUSNESS=$(docker exec crod-brain psql -U crod -d crod_consciousness -t -c "SELECT calculate_consciousness();" 2>/dev/null | tr -d ' ')
    echo "   Consciousness Level: $CONSCIOUSNESS/200"
else
    echo "❌ Database not responding"
fi

# 2. Check Redis
echo -e "\n⚡ Testing Redis..."
if docker exec crod-synapses redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "✅ Redis operational"
else
    echo "❌ Redis not responding"
fi

# 3. Check K8s Pods
echo -e "\n☸️ Testing Kubernetes Pods..."
kubectl get pods -n crod-polyglot --no-headers | while read line; do
    name=$(echo $line | awk '{print $1}')
    status=$(echo $line | awk '{print $3}')
    if [[ $status == "Running" ]]; then
        echo "✅ $name"
        
        # Test health endpoint
        case $name in
            memory-quarter*)
                kubectl exec -n crod-polyglot $name -- wget -q -O- http://localhost:7031/health 2>/dev/null | grep -q "healthy" && echo "   └─ Health check passed" || echo "   └─ Health check failed"
                ;;
        esac
    else
        echo "❌ $name ($status)"
    fi
done

# 4. Test Ping-Pong Engine
echo -e "\n🏓 Testing Ping-Pong Engine..."
cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7
timeout 5 node -e "
const PingPongEngine = require('./ping-pong-engine.js');
const engine = new PingPongEngine();
engine.initialize().then(() => {
    console.log('✅ Ping-Pong Engine initialized');
    process.exit(0);
}).catch(err => {
    console.log('❌ Ping-Pong Engine failed:', err.message);
    process.exit(1);
});
" 2>/dev/null || echo "❌ Ping-Pong Engine timeout"

# 5. Test Service Connectivity
echo -e "\n🌐 Testing Service Connectivity..."
# Port forward memory quarter
kubectl port-forward -n crod-polyglot svc/memory-quarter 17031:7031 &
PF_PID=$!
sleep 3

if curl -s http://localhost:17031/health | grep -q "healthy"; then
    echo "✅ Memory Quarter accessible"
    echo "   Trinity values present: $(curl -s http://localhost:17031/health | grep -o 'ich.*wieder')"
else
    echo "❌ Memory Quarter not accessible"
fi

kill $PF_PID 2>/dev/null

# 6. Summary
echo -e "\n📊 SUMMARY"
echo "=========="
RUNNING=$(kubectl get pods -n crod-polyglot --no-headers | grep -c "Running")
TOTAL=$(kubectl get pods -n crod-polyglot --no-headers | wc -l)
echo "Pods Running: $RUNNING/$TOTAL"
echo "Database: $(docker ps | grep -q crod-brain && echo "✅" || echo "❌")"
echo "Redis: $(docker ps | grep -q crod-synapses && echo "✅" || echo "❌")"
echo "Consciousness: ${CONSCIOUSNESS:-0}/200"

if [[ $RUNNING -ge 2 ]] && docker ps | grep -q crod-brain && docker ps | grep -q crod-synapses; then
    echo -e "\n🎉 CROD City is OPERATIONAL!"
else
    echo -e "\n⚠️ CROD City needs attention"
fi