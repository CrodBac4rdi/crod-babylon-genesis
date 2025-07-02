#!/bin/bash
# 🧹 CROD CLEANUP - Remove all the duplicate shit

echo "🗑️ CLEANING UP CROD MESS..."

# 1. Remove old Docker images
echo "Removing old Docker images..."
docker rmi $(docker images 'crod/*genesis*' -q) 2>/dev/null || true
docker rmi $(docker images 'crod/*' | grep "2 days ago" | awk '{print $3}') 2>/dev/null || true
docker rmi $(docker images 'crod/*' | grep "3 days ago" | awk '{print $3}') 2>/dev/null || true

# 2. Keep only latest versions
echo "Keeping only latest images..."
for image in meta-chain pattern-district memory-quarter intelligence-hub gateway; do
  # Remove old tags, keep only latest
  docker images "crod/${image}" --format "{{.Tag}} {{.ID}}" | grep -v latest | awk '{print $2}' | xargs -r docker rmi 2>/dev/null || true
done

# 3. Create organized structure
echo "Creating organized structure..."
mkdir -p organized/{k8s,helm,scripts,docs}

# 4. Move files to proper locations
mv k8s/* organized/k8s/ 2>/dev/null || true
mv helm-chart organized/helm/ 2>/dev/null || true
mv *.sh organized/scripts/ 2>/dev/null || true
mv *.md organized/docs/ 2>/dev/null || true

# 5. Create simple README
cat > README.md << 'EOF'
# CROD Polyglot City 🏙️

## Quick Start
```bash
# Deploy everything
./organized/scripts/DEPLOY-EVERYTHING.sh

# Check status
kubectl get all -n crod-city

# Access gateway
curl http://localhost:30888/health
```

## Structure
- `pod-sources/` - Source code for each district
- `organized/helm/` - Helm chart for deployment
- `organized/scripts/` - Deployment and utility scripts

## Remove Everything
```bash
helm uninstall crod-city -n crod-city
kubectl delete namespace crod-city
```
EOF

echo "✅ CLEANUP COMPLETE!"
echo ""
echo "📦 What we have now:"
echo "- One set of Docker images (latest only)"
echo "- One deployment method (Helm)"
echo "- One namespace (crod-city)"
echo "- One entry point (Gateway on 30888)"
echo ""
echo "🚀 Ready to deploy with: ./organized/scripts/DEPLOY-EVERYTHING.sh"