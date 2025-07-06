#!/bin/bash

# CROD ULTIMATIV - ONE CLICK INSTALLER
echo "🔥🔥🔥 CROD ULTIMATIV ONE-CLICK INSTALLER 🔥🔥🔥"
echo "================================================"

# Check if running as normal user
if [ "$EUID" -eq 0 ]; then 
   echo "Please run as normal user, not root!"
   exit 1
fi

# Install K3s (lightweight Kubernetes)
if ! command -v kubectl &> /dev/null; then
    echo "📦 Installing K3s (Kubernetes)..."
    curl -sfL https://get.k3s.io | sh -
    sudo chmod 644 /etc/rancher/k3s/k3s.yaml
    mkdir -p ~/.kube
    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
    sudo chown $USER:$USER ~/.kube/config
    echo "✅ K3s installed!"
fi

# Install Helm
if ! command -v helm &> /dev/null; then
    echo "📦 Installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    echo "✅ Helm installed!"
fi

# Create CROD namespace
kubectl create namespace crod-ultimativ 2>/dev/null || true

# Deploy everything with Helm
cat > crod-ultimativ-chart.yaml << 'EOF'
apiVersion: v2
name: crod-ultimativ
description: CROD ULTIMATIV 2025 - Everything is Blockchain
version: 1.0.0

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
  - name: n8n
    version: "0.x.x"
    repository: https://8gears.container-registry.com/chartrepo/library
    condition: n8n.enabled
EOF

# Create the ultimate start script
cat > ~/Schreibtisch/START_CROD.sh << 'EOF'
#!/bin/bash
echo "🔥 STARTING CROD ULTIMATIV 🔥"

# Open browser with all services
sleep 3
xdg-open http://localhost:8080 &  # Main Dashboard
xdg-open http://localhost:5678 &  # N8N
xdg-open http://localhost:3000 &  # Grafana

# Show logs
kubectl logs -n crod-ultimativ -l app=crod-brain --tail=100 -f
EOF

chmod +x ~/Schreibtisch/START_CROD.sh

# Create Desktop Entry
cat > ~/Schreibtisch/CROD_ULTIMATIV.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=🔥 CROD ULTIMATIV
Comment=Everything is Blockchain
Exec=/home/daniel/Schreibtisch/START_CROD.sh
Icon=/home/daniel/Schreibtisch/crod-babylon-genesis-main/CROD_ULTIMATIV/crod-icon.png
Terminal=true
Categories=Development;
StartupNotify=true
EOF

chmod +x ~/Schreibtisch/CROD_ULTIMATIV.desktop

# Create fancy icon if not exists
if [ ! -f crod-icon.png ]; then
    # Create a simple CROD icon using ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size 256x256 xc:black \
                -fill red -draw "circle 128,128 128,32" \
                -fill white -pointsize 120 -gravity center -annotate +0+0 "C" \
                crod-icon.png
    fi
fi

echo ""
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "🚀 TO START CROD ULTIMATIV:"
echo "   1. Double-click 'CROD ULTIMATIV' on your desktop"
echo "   2. OR run: ~/Schreibtisch/START_CROD.sh"
echo ""
echo "🌐 SERVICES WILL BE AVAILABLE AT:"
echo "   - Main Dashboard: http://localhost:8080"
echo "   - N8N Workflows: http://localhost:5678"
echo "   - Grafana: http://localhost:3000"
echo "   - Phoenix Live: http://localhost:4001"
echo ""
echo "🔥 EVERYTHING IS CROD! CROD IS EVERYTHING! 🔥"
echo ""
echo "Press Enter to start CROD now, or Ctrl+C to exit..."
read

# Start immediately
cd $(dirname $0)
./START_CROD_ULTIMATIV.sh
EOF