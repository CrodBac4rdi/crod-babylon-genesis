#!/bin/bash

# FIX K3S PERMISSIONS

echo "🔧 Fixing K3s permissions..."

# Option 1: Add daniel to k3s group
sudo usermod -a -G systemd-journal daniel

# Option 2: Fix the K3s config permissions
sudo chmod 644 /etc/rancher/k3s/k3s.yaml

# Option 3: Copy to user config
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
chmod 600 ~/.kube/config

# Option 4: Create alias for kubectl with sudo
echo "alias k='sudo kubectl'" >> ~/.bashrc

echo "✅ Done! Try these:"
echo "   1. kubectl get nodes"
echo "   2. sudo kubectl get nodes"  
echo "   3. k get nodes (after source ~/.bashrc)"
echo ""
echo "If still not working, restart K3s with better permissions:"
echo "   sudo systemctl stop k3s"
echo "   sudo systemctl start k3s"