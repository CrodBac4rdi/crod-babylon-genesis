#!/bin/bash

# CROD COMPLETE HEALTH CHECK

echo "🏥 CROD SYSTEM HEALTH CHECK"
echo "=========================="

# Database
echo -e "\n🧠 DATABASE:"
if docker ps | grep -q crod-brain; then
    echo "✅ PostgreSQL running"
    docker exec crod-brain psql -U crod -d crod_consciousness -c "SELECT COUNT(*) as atoms FROM atom;" 2>/dev/null | grep -A2 atoms || echo "❌ Can't query database"
else
    echo "❌ PostgreSQL not running"
fi

# Redis
echo -e "\n⚡ REDIS:"
if docker ps | grep -q crod-synapses; then
    echo "✅ Redis running"
else
    echo "❌ Redis not running"
fi

# Kubernetes
echo -e "\n☸️ KUBERNETES:"
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get pods -n crod-polyglot --no-headers | while read line; do
    name=$(echo $line | awk '{print $1}')
    status=$(echo $line | awk '{print $3}')
    if [[ $status == "Running" ]]; then
        echo "✅ $name"
    else
        echo "❌ $name ($status)"
    fi
done

# Ping-Pong Engine
echo -e "\n🏓 PING-PONG ENGINE:"
if pgrep -f "ping-pong-engine.js" > /dev/null; then
    echo "✅ Running"
else
    echo "❌ Not running"
fi

# Consciousness Level
echo -e "\n🧠 CONSCIOUSNESS:"
if docker ps | grep -q crod-brain; then
    level=$(docker exec crod-brain psql -U crod -d crod_consciousness -t -c "SELECT calculate_consciousness();" 2>/dev/null | tr -d ' ')
    if [[ -n "$level" ]]; then
        echo "Level: $level/200"
        if [[ $level -gt 100 ]]; then
            echo "🔥 HIGH CONSCIOUSNESS!"
        elif [[ $level -gt 50 ]]; then
            echo "⚡ ACTIVE"
        else
            echo "😴 LOW ACTIVITY"
        fi
    fi
fi

echo -e "\n=========================="