#!/bin/bash

# Setup GitHub Container Registry authentication for K8s

echo "🔐 Setting up GHCR authentication for Kubernetes"
echo "=============================================="
echo ""
echo "You need a GitHub Personal Access Token (PAT) with 'read:packages' scope"
echo "Create one at: https://github.com/settings/tokens/new"
echo ""

read -p "Enter your GitHub username: " GITHUB_USER
read -s -p "Enter your GitHub PAT: " GITHUB_TOKEN
echo ""

# Create docker config
DOCKER_CONFIG=$(echo -n "$GITHUB_USER:$GITHUB_TOKEN" | base64 -w 0)
DOCKER_CONFIG_JSON=$(echo -n '{"auths":{"ghcr.io":{"auth":"'$DOCKER_CONFIG'"}}}' | base64 -w 0)

# Update the secret file
sed -i "s|<BASE64_ENCODED_DOCKER_CONFIG>|$DOCKER_CONFIG_JSON|" k8s/image-pull-secret.yaml

# Apply to cluster
kubectl apply -f k8s/image-pull-secret.yaml

# Update all deployments to use the secret
for deployment in meta-chain pattern-district memory-quarter intelligence-hub gateway; do
    kubectl patch deployment $deployment -n crod-polyglot --type='json' \
        -p='[{"op": "add", "path": "/spec/template/spec/imagePullSecrets", "value": [{"name": "ghcr-secret"}]}]' \
        2>/dev/null || echo "Deployment $deployment not found, skipping..."
done

echo ""
echo "✅ GHCR authentication configured!"
echo ""
echo "📝 Remember to update your deployments to use:"
echo "   image: ghcr.io/$GITHUB_USER/<image-name>:latest"