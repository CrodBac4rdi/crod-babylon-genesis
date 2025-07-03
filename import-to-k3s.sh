#!/bin/bash
# Import Docker images to K3s

echo "🔄 IMPORTING DOCKER IMAGES TO K3S"
echo "================================"

# List of our images
images=(
  "crod/meta-chain:latest"
  "crod/pattern-district:latest"
  "crod/memory-quarter:latest"
  "crod/intelligence-hub:latest"
  "crod/gateway:latest"
  "redis:7-alpine"
)

# Check which images exist
echo "📋 Checking Docker images..."
for img in "${images[@]}"; do
  if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${img}$"; then
    echo "✅ Found: $img"
  else
    echo "❌ Missing: $img"
  fi
done

echo ""
echo "🚀 Now run WITH SUDO:"
echo ""
echo "sudo -E bash -c '"
for img in "${images[@]}"; do
  echo "  docker save $img | sudo k3s ctr images import -"
done
echo "'"
echo ""
echo "This will import all images to K3s containerd!"