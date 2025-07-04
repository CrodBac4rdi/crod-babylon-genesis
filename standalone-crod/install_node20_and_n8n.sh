#!/bin/bash

echo "🚀 Installing Node.js 20 + n8n for CROD"
echo "========================================"

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Remove old Node.js if present
echo "🗑️  Removing old Node.js..."
sudo apt remove -y nodejs npm

# Install Node.js 20
echo "📥 Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
echo "✅ Node.js installed:"
node --version
npm --version

# Install n8n globally with sudo
echo "🔄 Installing n8n globally..."
sudo npm install -g n8n

if [ $? -eq 0 ]; then
    echo "✅ n8n installed successfully!"
else
    echo "❌ n8n installation failed"
    echo "🔧 Trying alternative installation..."
    
    # Alternative: Install n8n locally for user
    echo "📦 Installing n8n locally..."
    mkdir -p ~/.local/bin
    npm install -g --prefix ~/.local n8n
    
    # Add to PATH
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✅ n8n installed locally"
fi

# Create n8n configuration directory
echo "📁 Setting up n8n configuration..."
mkdir -p ~/.n8n

# Create basic n8n config
cat > ~/.n8n/config.json << 'EOF'
{
  "host": "localhost",
  "port": 5678,
  "protocol": "http",
  "database": {
    "type": "sqlite",
    "sqlite": {
      "database": "~/.n8n/database.sqlite"
    }
  },
  "endpoints": {
    "webhook": "webhook",
    "webhookWaiting": "webhook-waiting", 
    "webhookTest": "webhook-test"
  },
  "security": {
    "excludeNodeEnvVars": false
  }
}
EOF

# Create CROD-specific n8n startup script
cat > ~/.n8n/start-crod-n8n.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting n8n for CROD..."
echo "Dashboard: http://localhost:5678"
echo "Webhooks: http://localhost:5678/webhook/WEBHOOK_NAME"
echo ""

# Set environment variables for CROD
export N8N_BASIC_AUTH_ACTIVE=false
export N8N_HOST=localhost
export N8N_PORT=5678
export N8N_PROTOCOL=http
export WEBHOOK_URL=http://localhost:5678

# Start n8n
n8n start
EOF

chmod +x ~/.n8n/start-crod-n8n.sh

# Create CROD workflow examples directory
mkdir -p ~/.n8n/crod-workflows

# Create Discord workflow example
cat > ~/.n8n/crod-workflows/discord-integration.json << 'EOF'
{
  "name": "CROD Discord Integration",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "crod-discord",
        "responseMode": "onReceived"
      },
      "id": "webhook",
      "name": "CROD Webhook", 
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [200, 300]
    },
    {
      "parameters": {
        "jsCode": "// Format CROD data for Discord\nconst data = $input.first().json;\n\nlet message = `🤖 **CROD Event: ${data.event_type}**\\n`;\n\nif (data.consciousness) {\n  message += `🧠 Consciousness: ${data.consciousness}\\n`;\n}\n\nif (data.patterns_detected) {\n  message += `🔍 Patterns: ${data.patterns_detected}\\n`;\n}\n\nif (data.user_input) {\n  message += `💬 Input: \\`${data.user_input}\\`\\n`;\n}\n\nreturn { content: message };"
      },
      "id": "format",
      "name": "Format Message",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [400, 300]
    }
  ],
  "connections": {
    "webhook": {
      "main": [
        [
          {
            "node": "format",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {},
  "staticData": {}
}
EOF

# Create simple test workflow
cat > ~/.n8n/crod-workflows/test-workflow.json << 'EOF'
{
  "name": "CROD Test Workflow",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "crod-test",
        "responseMode": "onReceived"
      },
      "id": "webhook-test",
      "name": "Test Webhook",
      "type": "n8n-nodes-base.webhook", 
      "typeVersion": 1,
      "position": [200, 300]
    },
    {
      "parameters": {
        "jsCode": "console.log('🔥 CROD Event received:', JSON.stringify($input.first().json, null, 2));\nreturn { status: 'success', received: $input.first().json };"
      },
      "id": "log-test",
      "name": "Log Event",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [400, 300]
    }
  ],
  "connections": {
    "webhook-test": {
      "main": [
        [
          {
            "node": "log-test",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {},
  "staticData": {}
}
EOF

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 To start n8n for CROD:"
echo "   ~/.n8n/start-crod-n8n.sh"
echo ""
echo "🌐 Then open: http://localhost:5678"
echo ""
echo "📋 Next steps:"
echo "   1. Start n8n: ~/.n8n/start-crod-n8n.sh"
echo "   2. Open browser: http://localhost:5678"
echo "   3. Import workflows from ~/.n8n/crod-workflows/"
echo "   4. Test webhook: curl -X POST http://localhost:5678/webhook/crod-test -d '{\"test\":\"data\"}' -H 'Content-Type: application/json'"
echo ""
echo "🔗 CROD Integration webhooks:"
echo "   • http://localhost:5678/webhook/crod-discord"
echo "   • http://localhost:5678/webhook/crod-trinity"
echo "   • http://localhost:5678/webhook/crod-test"
echo ""
echo "💡 Restart terminal or run: source ~/.bashrc"