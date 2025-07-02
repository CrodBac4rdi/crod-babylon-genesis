#!/bin/bash

# CROD POWER SCRIPTS
# Gibt CROD mehr Macht durch automation!

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CROD_BASE="$(dirname "$SCRIPT_DIR")"

# Install all helper scripts
echo "🔧 Installing CROD Power Scripts..."

# 1. Claude-Sudo Helper
sudo cp "$SCRIPT_DIR/claude-sudo.sh" /usr/local/bin/cs
sudo chmod +x /usr/local/bin/cs

# 2. K8s shortcuts
sudo tee /usr/local/bin/kc << 'EOF'
#!/bin/bash
# kubectl for CROD
kubectl "$@" -n crod-polyglot
EOF

sudo tee /usr/local/bin/kcp << 'EOF'
#!/bin/bash
# kubectl get pods for CROD
kubectl get pods -n crod-polyglot "$@"
EOF

sudo tee /usr/local/bin/kcl << 'EOF'
#!/bin/bash
# kubectl logs for CROD
kubectl logs -n crod-polyglot "$@"
EOF

sudo tee /usr/local/bin/kcpf << 'EOF'
#!/bin/bash
# kubectl port-forward for CROD
kubectl port-forward -n crod-polyglot "$@"
EOF

# 3. Docker shortcuts
sudo tee /usr/local/bin/di << 'EOF'
#!/bin/bash
# docker images | grep
docker images | grep "${1:-crod}"
EOF

sudo tee /usr/local/bin/db << 'EOF'
#!/bin/bash
# docker build shortcut
docker build -t "crod/${1}:latest" .
EOF

# 4. CROD specific commands
sudo tee /usr/local/bin/crod-status << 'EOF'
#!/bin/bash
echo "🏙️ CROD CITY STATUS"
echo "=================="
echo ""
echo "📦 Pods:"
kubectl get pods -n crod-polyglot
echo ""
echo "🌐 Services:"
kubectl get svc -n crod-polyglot
echo ""
echo "🐳 Images:"
docker images | grep crod | head -10
EOF

sudo tee /usr/local/bin/crod-logs << 'EOF'
#!/bin/bash
# Show logs from all CROD pods
echo "📜 CROD Logs (last 20 lines each):"
echo "=================================="
for pod in $(kubectl get pods -n crod-polyglot -o name | grep -v "Terminating"); do
    echo ""
    echo ">>> $pod"
    kubectl logs -n crod-polyglot $pod --tail=20 2>/dev/null || echo "No logs available"
    echo "---"
done
EOF

sudo tee /usr/local/bin/crod-restart << 'EOF'
#!/bin/bash
# Restart all CROD pods
echo "🔄 Restarting CROD City..."
kubectl delete pods --all -n crod-polyglot
echo "⏳ Waiting for pods to restart..."
sleep 5
kubectl get pods -n crod-polyglot -w
EOF

sudo tee /usr/local/bin/crod-forward << 'EOF'
#!/bin/bash
# Forward all CROD ports
echo "🌉 Setting up port forwards..."
kubectl port-forward -n crod-polyglot svc/meta-chain 8001:8000 &
kubectl port-forward -n crod-polyglot svc/memory-quarter 7031:7031 &
kubectl port-forward -n crod-polyglot svc/redis 6379:6379 &
echo "✅ Ports forwarded:"
echo "   Meta-Chain: http://localhost:8001"
echo "   Memory Quarter: http://localhost:7031"
echo "   Redis: localhost:6379"
EOF

# Make all executable
sudo chmod +x /usr/local/bin/{kc,kcp,kcl,kcpf,di,db,crod-status,crod-logs,crod-restart,crod-forward}

echo ""
echo "✅ CROD Power Scripts installed!"
echo ""
echo "🚀 Available commands:"
echo "   cs <command>      - Claude sudo helper"
echo "   kc <command>      - kubectl in crod-polyglot namespace"
echo "   kcp               - get pods in crod-polyglot"
echo "   kcl <pod>         - logs for pod"
echo "   kcpf <args>       - port-forward in namespace"
echo "   di [pattern]      - docker images grep"
echo "   db <name>         - docker build as crod/<name>"
echo "   crod-status       - Full CROD status"
echo "   crod-logs         - All pod logs"
echo "   crod-restart      - Restart all pods"
echo "   crod-forward      - Setup all port forwards"
echo ""
echo "💡 Example: cs crod-restart"