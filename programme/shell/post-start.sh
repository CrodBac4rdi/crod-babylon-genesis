#!/bin/bash
# CROD Post-Start Commands
# Runs every time the Codespace starts

# Apply security rules
bash .devcontainer/security-setup.sh

# Show welcome message
cat ~/.crod_welcome 2>/dev/null || echo "🔥 CROD Ready!"

# Check services
echo ""
echo "Checking services..."
kubectl get pods -n crod-polyglot 2>/dev/null || echo "K8s not ready yet"
redis-cli ping 2>/dev/null && echo "Redis: ✅" || echo "Redis: ❌"

echo ""
echo "🔒 Security: All ports localhost only!"
echo "🚀 Ready to develop CROD!"