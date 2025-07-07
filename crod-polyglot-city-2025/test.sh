#!/bin/bash

echo "🧪 Testing CROD Polyglot City services..."

# Function to check service
check_service() {
    local name=$1
    local url=$2
    
    if curl -s -f "$url" > /dev/null; then
        echo "✅ $name is online"
    else
        echo "❌ $name is offline"
    fi
}

# Wait for services
sleep 5

# Check each service
check_service "Phoenix Rathaus" "http://localhost:4000"
check_service "Rust Pattern District" "http://localhost:7007"
check_service "Go Memory Quarter" "http://localhost:7031"
check_service "JavaScript Gateway" "http://localhost:7888"

# Check Gateway API status
echo ""
echo "📊 Gateway Status:"
curl -s http://localhost:7888/api/status | jq .

# Check NATS
echo ""
echo "📡 NATS Status:"
curl -s http://localhost:8222/varz | jq '.connections, .in_msgs, .out_msgs' | head -10
