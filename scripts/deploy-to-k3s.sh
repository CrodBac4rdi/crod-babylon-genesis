#!/bin/bash
# DEPLOY CROD TO K3S

echo "🚀 DEPLOYING CROD TO K3S..."

export KUBECONFIG=~/.kube/config

# 1. Create namespace
echo "📁 Creating namespace..."
kubectl apply -f k8s/namespaces/crod-namespace.yaml

# 2. Create ConfigMap
echo "⚙️ Creating ConfigMap..."
kubectl apply -f k8s/configmaps/crod-config.yaml

# 3. Build Docker images locally
echo "🔨 Building Docker images..."
cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-START

# Build Meta-Chain
docker build -t crod/meta-chain:latest ./meta-chain

# Build Pattern Genesis
docker build -t crod/pattern-genesis:latest ./genesis-blocks/ACTIVE/pattern-genesis

# Build Gateway
docker build -t crod/claude-gateway:latest ./chain-protocol/gateway

# 4. Deploy to K3s
echo "🚀 Deploying to K3s..."
kubectl apply -f k8s/deployments/

# 5. Wait for pods
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=redis -n crod-system --timeout=60s
kubectl wait --for=condition=ready pod -l app=meta-chain -n crod-system --timeout=60s
kubectl wait --for=condition=ready pod -l app=pattern-genesis -n crod-system --timeout=60s
kubectl wait --for=condition=ready pod -l app=claude-gateway -n crod-system --timeout=60s

# 6. Show status
echo ""
echo "✅ CROD DEPLOYED TO K3S!"
echo ""
kubectl get pods -n crod-system
echo ""
echo "🌐 Gateway available at: http://localhost:30888"
echo ""
echo "📊 To check logs:"
echo "kubectl logs -n crod-system -l app=meta-chain"