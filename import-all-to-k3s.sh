#!/bin/bash
# Import ALL CROD images to K3s

echo "🔄 Importing all images to K3s..."

IMAGES=(
  "crod/meta-chain:latest"
  "crod/pattern-district:latest"
  "crod/memory-quarter:latest"
  "crod/intelligence-hub:latest"
  "crod/gateway:latest"
  "crod/llama-learning:latest"
  "crod/blockchain-core:latest"
  "crod/delta-quarter:latest"
  "crod/crod-core:latest"
)

for IMAGE in "${IMAGES[@]}"; do
  echo "📦 Importing $IMAGE..."
  sudo docker save $IMAGE | sudo k3s ctr images import -
done

echo "✅ All images imported!"