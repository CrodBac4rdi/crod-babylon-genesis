#!/bin/bash

# Setup GitHub Container Registry für lokales K8s

echo "🔐 Setting up GHCR for local K8s..."
echo "==================================="

# 1. Docker login to GHCR
echo "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" | docker login ghcr.io -u CrodBac4rdi --password-stdin

# 2. Create K8s secret from Docker config
kubectl create secret generic ghcr-secret \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson \
    -n crod-polyglot \
    --dry-run=client -o yaml | kubectl apply -f -

# 3. Update all deployments to use GHCR images
echo "📝 Updating deployments to use GHCR..."

for file in k8s/*.yaml; do
    # Backup original
    cp $file $file.backup
    
    # Replace image references
    sed -i 's|image: crod/|image: ghcr.io/crodbac4rdi/|g' $file
    
    # Add imagePullSecrets if not present
    if ! grep -q "imagePullSecrets:" $file; then
        sed -i '/spec:/,/containers:/ {
            /containers:/ i\      imagePullSecrets:\n      - name: ghcr-secret
        }' $file
    fi
done

echo "✅ Setup complete!"
echo ""
echo "🚀 Now you can:"
echo "   1. Wait for GitHub Actions to build (check: https://github.com/CrodBac4rdi/crod-babylon-genesis/actions)"
echo "   2. Deploy with: kubectl apply -f k8s/"
echo "   3. Updates happen automatically when you push code!"