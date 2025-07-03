#!/bin/bash

# Quick fix for local deployment while waiting for GitHub Actions

echo "🔧 Quick fixing local deployment..."

# 1. Delete old broken images
docker rmi crod/meta-chain-elixir:latest 2>/dev/null || true

# 2. Rebuild with correct config
cd pod-sources/meta-chain
docker build -t crod/meta-chain-elixir:v3 --no-cache .
cd ../..

# 3. Update deployment to use v3
kubectl set image deployment/meta-chain-elixir meta-chain=crod/meta-chain-elixir:v3 -n crod-polyglot

# 4. Restart
kubectl rollout restart deployment meta-chain-elixir -n crod-polyglot

echo "✅ Fixed! Waiting for pod to start..."
sleep 10

kubectl get pods -n crod-polyglot