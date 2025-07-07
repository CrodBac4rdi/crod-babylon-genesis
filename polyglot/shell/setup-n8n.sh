#!/bin/bash
# N8N Setup for CROD

echo "🔧 Setting up N8N for CROD..."

# Create directories
mkdir -p ~/.n8n/workflows
mkdir -p ~/.n8n/nodes

# Install N8N globally
npm install -g n8n

# Create CROD workflow directory
mkdir -p n8n-workflows

# Create basic CROD workflow
cat > n8n-workflows/crod-pattern-detection.json << 'EOF'
{
  "name": "CROD Pattern Detection",
  "nodes": [{
    "parameters": {
      "path": "crod-pattern",
      "responseMode": "onReceived",
      "responseData": "allEntries"
    },
    "name": "Webhook",
    "type": "n8n-nodes-base.webhook",
    "typeVersion": 1,
    "position": [250, 300]
  }, {
    "parameters": {
      "url": "http://localhost:3001/api/blockchain/add",
      "requestMethod": "POST",
      "jsonParameters": true,
      "options": {},
      "bodyParametersJson": "={{ $json }}"
    },
    "name": "Mine Block",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 1,
    "position": [450, 300]
  }],
  "connections": {
    "Webhook": {
      "main": [[{
        "node": "Mine Block",
        "type": "main",
        "index": 0
      }]]
    }
  }
}
EOF

echo "✅ N8N setup complete!"
echo "Start N8N with: n8n start"
echo "Access at: http://localhost:5678"