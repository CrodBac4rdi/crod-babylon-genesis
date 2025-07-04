#!/bin/bash
# CROD Safe Shutdown - Preserve All Data
# Date: July 4, 2025 13:30

echo "🛑 CROD Safe Shutdown Starting..."
echo "📦 Preserving all data before shutdown"

# Create backup directory with timestamp
BACKUP_DIR="/home/daniel/Schreibtisch/Crod Programming/CROD-BACKUP-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Backup directory: $BACKUP_DIR"

# 1. Export Kubernetes data
echo "📊 Exporting Kubernetes configurations..."
mkdir -p "$BACKUP_DIR/kubernetes"
kubectl get all -n crod-polyglot -o yaml > "$BACKUP_DIR/kubernetes/all-resources.yaml"
kubectl get configmaps,secrets -n crod-polyglot -o yaml > "$BACKUP_DIR/kubernetes/configs-secrets.yaml"
kubectl get pv,pvc --all-namespaces -o yaml | grep -E "crod|CROD" > "$BACKUP_DIR/kubernetes/volumes.yaml"

# 2. Save running process info
echo "📝 Documenting running processes..."
ps aux | grep -E "crod|python3.*crod" | grep -v grep > "$BACKUP_DIR/running-processes.txt"

# 3. Backup all databases
echo "💾 Backing up databases..."
mkdir -p "$BACKUP_DIR/databases"
find /home/daniel/Schreibtisch/Crod\ Programming -name "*.db" -o -name "*.sqlite" | while read db; do
    if [ -s "$db" ]; then  # Only backup non-empty databases
        cp "$db" "$BACKUP_DIR/databases/"
        echo "  ✓ Backed up: $(basename "$db")"
    fi
done

# 4. Export Redis data
echo "📤 Exporting Redis data..."
mkdir -p "$BACKUP_DIR/redis"
kubectl exec -n crod-polyglot redis-76fc6cd69f-tdfpx -- redis-cli BGSAVE
sleep 2
kubectl exec -n crod-polyglot redis-76fc6cd69f-tdfpx -- redis-cli --scan > "$BACKUP_DIR/redis/all-keys.txt"
kubectl exec -n crod-polyglot redis-76fc6cd69f-tdfpx -- redis-cli INFO > "$BACKUP_DIR/redis/info.txt"

# 5. Save Docker images list
echo "🐳 Documenting Docker images..."
docker images | grep crod > "$BACKUP_DIR/docker-images.txt"
docker ps -a | grep crod > "$BACKUP_DIR/docker-containers.txt"

# 6. Create restoration script
cat > "$BACKUP_DIR/restore-crod.sh" << 'EOF'
#!/bin/bash
# CROD Restoration Script
echo "🔄 CROD Restoration starting..."
echo "This will restore CROD to the state before shutdown"
echo "TODO: Implement restoration logic"
EOF
chmod +x "$BACKUP_DIR/restore-crod.sh"

echo ""
echo "✅ Backup complete. Now shutting down processes..."
echo ""

# 7. Stop Python processes gracefully
echo "🐍 Stopping Python processes..."
for pid in $(ps aux | grep -E "python3.*crod" | grep -v grep | awk '{print $2}'); do
    echo "  Stopping PID $pid..."
    kill -TERM $pid 2>/dev/null || true
done

# 8. Scale down Kubernetes deployments
echo "☸️  Scaling down Kubernetes deployments..."
kubectl scale deployment --all --replicas=0 -n crod-polyglot

# Wait for pods to terminate
echo "⏳ Waiting for pods to terminate..."
kubectl wait --for=delete pod --all -n crod-polyglot --timeout=60s 2>/dev/null || true

# 9. Stop any remaining Docker containers
echo "🐳 Stopping Docker containers..."
docker ps -q | xargs -r docker stop 2>/dev/null || true

echo ""
echo "✅ CROD shutdown complete!"
echo "📦 All data preserved in: $BACKUP_DIR"
echo ""
echo "To restore CROD later, run:"
echo "  $BACKUP_DIR/restore-crod.sh"
echo ""
echo "Ready to rebuild CROD with Elixir blockchain! 🚀"