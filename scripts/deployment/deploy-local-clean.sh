#!/bin/bash
# CLEAN LOCAL DEPLOYMENT - NO GITHUB, JUST LOCAL IMAGES

echo "🏙️ CROD POLYGLOT CITY - LOCAL DEPLOYMENT"
echo "========================================"

# Clean everything first
echo "🧹 Cleaning up..."
kubectl delete all --all -n crod-polyglot 2>/dev/null || true
kubectl delete service gateway-nodeport -n crod-polyglot 2>/dev/null || true

# Ensure namespace
kubectl create namespace crod-polyglot 2>/dev/null || true

# Deploy Redis
echo "📦 Deploying Redis..."
kubectl apply -f pod-configs/redis-cluster.yaml

# Wait for Redis
echo "⏳ Waiting for Redis..."
sleep 5

# Deploy all districts with CORRECT local image names
echo "🏗️ Deploying Districts..."

kubectl apply -f - <<'EOF'
# Meta Chain
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meta-chain
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: meta-chain
  template:
    metadata:
      labels:
        app: meta-chain
    spec:
      containers:
      - name: meta-chain
        image: crod/meta-chain:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_HOST
          value: "redis"
        - name: HTTP_PORT
          value: "8000"
---
apiVersion: v1
kind: Service
metadata:
  name: meta-chain
  namespace: crod-polyglot
spec:
  selector:
    app: meta-chain
  ports:
  - port: 8000
    targetPort: 8000
---
# Pattern District
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pattern-district
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pattern-district
  template:
    metadata:
      labels:
        app: pattern-district
    spec:
      containers:
      - name: pattern-district
        image: crod/pattern-district:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 7007
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
---
apiVersion: v1
kind: Service
metadata:
  name: pattern-district
  namespace: crod-polyglot
spec:
  selector:
    app: pattern-district
  ports:
  - port: 7007
    targetPort: 7007
---
# Memory Quarter
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memory-quarter
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: memory-quarter
  template:
    metadata:
      labels:
        app: memory-quarter
    spec:
      containers:
      - name: memory-quarter
        image: crod/memory-quarter:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 7031
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
---
apiVersion: v1
kind: Service
metadata:
  name: memory-quarter
  namespace: crod-polyglot
spec:
  selector:
    app: memory-quarter
  ports:
  - port: 7031
    targetPort: 7031
---
# Intelligence Hub
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intelligence-hub
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: intelligence-hub
  template:
    metadata:
      labels:
        app: intelligence-hub
    spec:
      containers:
      - name: intelligence-hub
        image: crod/intelligence-hub:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 7113
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
---
apiVersion: v1
kind: Service
metadata:
  name: intelligence-hub
  namespace: crod-polyglot
spec:
  selector:
    app: intelligence-hub
  ports:
  - port: 7113
    targetPort: 7113
---
# Gateway
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
      - name: gateway
        image: crod/gateway:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
        env:
        - name: DISTRICTS
          value: "meta-chain:8000,pattern-district:7007,memory-quarter:7031,intelligence-hub:7113"
        - name: PORT
          value: "8080"
---
apiVersion: v1
kind: Service
metadata:
  name: gateway
  namespace: crod-polyglot
spec:
  selector:
    app: gateway
  ports:
  - port: 8080
    targetPort: 8080
---
# Gateway NodePort
apiVersion: v1
kind: Service
metadata:
  name: gateway-external
  namespace: crod-polyglot
spec:
  type: NodePort
  selector:
    app: gateway
  ports:
  - port: 8888
    targetPort: 8080
    nodePort: 30888
EOF

echo ""
echo "⏳ Waiting for pods..."
sleep 10

echo "📊 Deployment Status:"
kubectl get pods -n crod-polyglot -o wide

echo ""
echo "🎯 NEXT STEPS:"
echo "1. Run the import command with sudo (shown above)"
echo "2. Run this script again: ./deploy-local-clean.sh"
echo "3. Access Gateway at: http://localhost:30888"