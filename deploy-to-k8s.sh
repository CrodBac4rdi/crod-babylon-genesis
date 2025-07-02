#!/bin/bash

# CROD POLYGLOT CITY - Deploy to Kubernetes
# Needs sudo for kubectl!

set -e

echo "🚀 CROD POLYGLOT CITY - Deploying to Kubernetes..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if kubectl exists
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found! Please install kubectl first."
    exit 1
fi

# Check if we can access K8s
if ! kubectl cluster-info &> /dev/null && ! sudo kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster!"
    echo "   Make sure K3s/minikube is running"
    echo "   Export KUBECONFIG if needed"
    exit 1
fi

echo "✅ Kubernetes cluster accessible"
echo ""

# Detect if we need sudo
if kubectl version &> /dev/null; then
    K="kubectl"
else
    K="sudo kubectl"
    echo "📝 Using sudo for kubectl commands"
fi

# Deploy Redis first
echo "📦 Deploying Redis..."
$K apply -f "$SCRIPT_DIR/pod-configs/redis-cluster.yaml"

# Wait for Redis
echo "⏳ Waiting for Redis to be ready..."
$K wait --for=condition=ready pod -l app=redis -n crod-polyglot --timeout=60s || true

# Deploy all pods
echo "🏙️ Deploying CROD City..."
$K apply -f "$SCRIPT_DIR/pod-configs/complete-deployment.yaml"

# Deploy blockchain if exists
if [ -f "$SCRIPT_DIR/pod-configs/blockchain-chain.yaml" ]; then
    echo "⛓️ Deploying Blockchain..."
    kubectl apply -f "$SCRIPT_DIR/pod-configs/blockchain-chain.yaml"
fi

echo ""
echo "📊 Deployment status:"
kubectl get all -n crod-polyglot

echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod --all -n crod-polyglot --timeout=120s || {
    echo "⚠️  Some pods are not ready yet. Check with:"
    echo "   kubectl get pods -n crod-polyglot"
    echo "   kubectl describe pod <pod-name> -n crod-polyglot"
}

echo ""
echo "🌐 Services:"
kubectl get svc -n crod-polyglot

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎯 Access points:"
echo "   Gateway: http://localhost:30888"
echo "   Health: http://localhost:30888/health"
echo "   Process: POST http://localhost:30888/crod/process"
echo ""
echo "📝 Useful commands:"
echo "   Watch pods: kubectl get pods -n crod-polyglot -w"
echo "   View logs: kubectl logs -n crod-polyglot <pod-name>"
echo "   Port forward: kubectl port-forward -n crod-polyglot svc/gateway 8888:8888"