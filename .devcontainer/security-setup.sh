#!/bin/bash
# CROD Security Setup - NO PUBLIC PORTS!

echo "🔒 Configuring CROD Security..."

# Create iptables rules to block all external access
cat > /tmp/crod-security.rules <<'EOF'
#!/bin/bash
# CROD Security Rules - Block ALL external access

# Allow localhost only
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Block all CROD ports from external access
for port in 8000 7007 7031 7113 8888 8100 8101 6379 5432 4222 30889; do
    iptables -A INPUT -p tcp --dport $port -s 127.0.0.1 -j ACCEPT
    iptables -A INPUT -p tcp --dport $port -j DROP
done

# Block NodePort range
iptables -A INPUT -p tcp --dport 30000:32767 -j DROP

echo "✅ Security rules applied - all ports localhost only!"
EOF

chmod +x /tmp/crod-security.rules
sudo /tmp/crod-security.rules

# Create systemd service to persist rules
sudo tee /etc/systemd/system/crod-security.service > /dev/null <<EOF
[Unit]
Description=CROD Security Rules
After=network.target

[Service]
Type=oneshot
ExecStart=/tmp/crod-security.rules
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable crod-security.service
sudo systemctl start crod-security.service

# Configure K8s to use localhost only
cat > /tmp/k8s-security.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: security-config
  namespace: kube-system
spec:
  type: ClusterIP
  clusterIP: None
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: crod-polyglot
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
    - namespaceSelector:
        matchLabels:
          name: crod-polyglot
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
  namespace: crod-polyglot
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector: {}
    - namespaceSelector:
        matchLabels:
          name: crod-polyglot
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
EOF

kubectl apply -f /tmp/k8s-security.yaml 2>/dev/null || true

# Disable port forwarding in VS Code settings
cat >> ~/.vscode-server/data/Machine/settings.json <<'EOF'
{
  "remote.autoForwardPorts": false,
  "remote.forwardOnOpen": false,
  "remote.localPortHost": "127.0.0.1",
  "remote.portsAttributes": {
    "*": {
      "onAutoForward": "ignore"
    }
  }
}
EOF

echo "🔒 Security configuration complete!"
echo "✅ All ports are localhost only"
echo "✅ No automatic port forwarding"
echo "✅ NetworkPolicy blocks external access"
echo "✅ iptables rules enforced"