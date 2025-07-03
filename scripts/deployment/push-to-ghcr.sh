#!/bin/bash

# Push all CROD images to GitHub Container Registry
# Nutzt dein GitHub Pro für unlimited private packages!

set -e

GITHUB_USER="CrodBac4rdi"
GITHUB_REPO="crod-start"
REGISTRY="ghcr.io"

echo "🚀 Pushing CROD to GitHub Container Registry (ghcr.io)"
echo "=================================================="

# Login to GitHub Container Registry
echo "📝 Please login to GitHub Container Registry:"
echo "You need a Personal Access Token with 'write:packages' permission"
echo "Create one at: https://github.com/settings/tokens/new"
echo ""
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -s -p "Enter your GitHub PAT: " GITHUB_TOKEN
echo ""

echo $GITHUB_TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin

# Tag and push all images
IMAGES=(
    "crod/meta-chain-elixir"
    "crod/pattern-district-rust"
    "crod/memory-quarter-go"
    "crod/intelligence-hub-python"
    "crod/gateway-node"
)

for IMAGE in "${IMAGES[@]}"; do
    echo ""
    echo "📦 Processing $IMAGE..."
    
    # Check if image exists locally
    if docker images | grep -q "$IMAGE"; then
        # Tag for GitHub registry
        NEW_TAG="$REGISTRY/$GITHUB_USERNAME/${IMAGE#crod/}"
        
        echo "  🏷️  Tagging as $NEW_TAG"
        docker tag "$IMAGE:latest" "$NEW_TAG:latest"
        docker tag "$IMAGE:latest" "$NEW_TAG:$(date +%Y%m%d-%H%M%S)"
        
        echo "  📤 Pushing to GitHub..."
        docker push "$NEW_TAG:latest"
        docker push "$NEW_TAG:$(date +%Y%m%d-%H%M%S)"
        
        echo "  ✅ $IMAGE pushed successfully!"
    else
        echo "  ⚠️  $IMAGE not found locally, skipping..."
    fi
done

echo ""
echo "🎉 All images pushed to GitHub Container Registry!"
echo ""
echo "📋 Update your K8s deployments to use:"
echo "   $REGISTRY/$GITHUB_USERNAME/<image-name>:latest"
echo ""
echo "🔒 These images are PRIVATE and only accessible with authentication!"