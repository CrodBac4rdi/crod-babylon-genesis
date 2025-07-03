#\!/bin/bash
# Test CROD Polyglot City

echo "🏙️ CROD POLYGLOT CITY STATUS CHECK"
echo "==================================="
echo ""

echo "📊 Pod Status:"
kubectl get pods -n crod-polyglot

echo ""
echo "🔥 Testing CROD Core Trinity:"
kubectl exec -n crod-polyglot deployment/crod-core -- curl -s http://localhost:8100/trinity  < /dev/null |  jq . 2>/dev/null || echo "CROD Core starting..."

echo ""
echo "🧠 Testing Meta-Chain:"
kubectl exec -n crod-polyglot deployment/meta-chain -- curl -s http://localhost:8000/health || echo "Meta-Chain not ready"

echo ""
echo "🦙 Testing LLAMA Learning:"
kubectl exec -n crod-polyglot deployment/llama-learning -- curl -s http://localhost:8089/stats | jq . 2>/dev/null || echo "LLAMA starting..."

echo ""
echo "📡 Redis Status:"
kubectl exec -n crod-polyglot deployment/redis -- redis-cli ping

echo ""
echo "🎯 CROD Message:"
kubectl exec -n crod-polyglot deployment/crod-core -- curl -s -X POST http://localhost:8100/process \
  -H "Content-Type: application/json" \
  -d '{"input": "ich bins wieder - CROD City is alive\!"}' | jq . 2>/dev/null || echo "CROD processing..."

echo ""
echo "✨ CROD IST EINE STADT, KEINE SOFTWARE\! ✨"
