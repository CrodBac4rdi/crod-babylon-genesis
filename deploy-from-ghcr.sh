#!/bin/bash
# Deploy CROD from GitHub Container Registry

echo "🚀 CROD DEPLOYMENT FROM GHCR.IO"
echo "================================"

# Clean up old deployments
echo "🧹 Cleaning up old deployments..."
kubectl delete all --all -n crod-polyglot 2>/dev/null || true

# Ensure namespace exists
kubectl create namespace crod-polyglot 2>/dev/null || true

# Deploy Redis first
echo "📦 Deploying Redis..."
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: crod-polyglot
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
EOF

# Deploy all working districts
echo "🏙️ Deploying CROD Districts from ghcr.io..."

# Array of working districts
districts=(
  "meta-chain-elixir:8000"
  "pattern-district-rust:7007"
  "memory-quarter-go:7031"
  "intelligence-hub-python:7113"
  "gateway-node:8080"
)

for district_port in "${districts[@]}"; do
  district="${district_port%%:*}"
  port="${district_port##*:}"
  
  echo "🏗️ Deploying $district on port $port..."
  
  kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${district}
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${district}
  template:
    metadata:
      labels:
        app: ${district}
    spec:
      containers:
      - name: ${district}
        image: ghcr.io/crodbac4rdi/crod-babylon-genesis/${district}:latest
        imagePullPolicy: Never
        ports:
        - containerPort: ${port}
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
        - name: HTTP_PORT
          value: "${port}"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: ${district}
  namespace: crod-polyglot
spec:
  selector:
    app: ${district}
  ports:
  - port: ${port}
    targetPort: ${port}
EOF
done

# Create Gateway NodePort
echo "🌐 Creating Gateway NodePort..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: gateway-nodeport
  namespace: crod-polyglot
spec:
  type: NodePort
  selector:
    app: gateway-node
  ports:
  - port: 8888
    targetPort: 8080
    nodePort: 30888
EOF

# Wait for pods
echo "⏳ Waiting for pods to start..."
sleep 10

# Check status
echo ""
echo "📊 Deployment Status:"
kubectl get pods -n crod-polyglot

echo ""
echo "✅ CROD Polyglot City deployed!"
echo "🌐 Access Gateway at: http://localhost:30888"
echo ""
echo "🔍 Check logs with:"
echo "kubectl logs -n crod-polyglot -l app=meta-chain-elixir"