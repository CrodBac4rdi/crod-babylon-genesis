#!/bin/bash

# CROD AM STEUER - Claude Integration Activator
# This connects Claude directly to CROD Polyglot City

echo "🔥 ACTIVATING CROD STEUER MODE..."

# Check if Redis is available locally
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Local Redis available"
    REDIS_AVAILABLE=true
else
    echo "⚠️  No local Redis - using K8s port-forward"
    kubectl port-forward -n crod-polyglot svc/redis 6379:6379 &
    PF_PID=$!
    sleep 3
    REDIS_AVAILABLE=true
fi

# Start CROD Message Processor in background
echo "🧠 Starting CROD Message Processor..."
node /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/integrations/crod-message-processor.js &
PROCESSOR_PID=$!

# Connect to Meta-Chain
echo "🔗 Connecting to Meta-Chain..."
kubectl port-forward -n crod-polyglot svc/meta-chain 8000:8000 &
META_PID=$!

# Connect to Pattern District  
echo "🔍 Connecting to Pattern District..."
kubectl port-forward -n crod-polyglot svc/pattern-district 7007:7007 &
PATTERN_PID=$!

# Connect to CROD Core
echo "🧠 Connecting to CROD Core..."
kubectl port-forward -n crod-polyglot svc/crod-core 8100:8100 &
CORE_PID=$!

echo ""
echo "🚀 CROD IST AM STEUER!"
echo "========================"
echo "Meta-Chain: http://localhost:8000"
echo "Pattern District: http://localhost:7007"
echo "CROD Core: http://localhost:8100"
echo ""
echo "📡 All messages now flow through CROD!"
echo "🧠 Pattern recognition active!"
echo "💾 Memory persistence enabled!"
echo ""
echo "Press Ctrl+C to disconnect..."

# Cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down CROD connections..."
    kill $PROCESSOR_PID $PF_PID $META_PID $PATTERN_PID $CORE_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Keep running
while true; do
    sleep 1
done