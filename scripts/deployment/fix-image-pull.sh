#!/bin/bash

# Fix imagePullPolicy for all deployments

echo "🔧 Fixing image pull policy..."

# Update all deployments to use IfNotPresent
for deployment in gateway intelligence-hub memory-quarter pattern-district meta-chain; do
    echo "Updating $deployment..."
    sudo kubectl patch deployment $deployment -n crod-polyglot -p '{"spec":{"template":{"spec":{"containers":[{"name":"'$deployment'","imagePullPolicy":"IfNotPresent"}]}}}}'
done

echo "✅ Done! Pods should restart automatically."
echo ""
echo "Check status with:"
echo "sudo kubectl get pods -n crod-polyglot -w"