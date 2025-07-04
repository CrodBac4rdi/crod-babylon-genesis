#!/bin/bash

echo "🔄 Installing n8n for CROD Integration"
echo "======================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found!"
    echo "   Install Node.js first: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   Then: sudo apt-get install -y nodejs"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Install n8n globally
echo "📦 Installing n8n..."
npm install -g n8n

if [ $? -eq 0 ]; then
    echo "✅ n8n installed successfully!"
else
    echo "❌ n8n installation failed"
    echo "   Try: sudo npm install -g n8n"
    exit 1
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

# Create example Discord workflow
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
    },
    {
      "parameters": {
        "webhookUrl": "YOUR_DISCORD_WEBHOOK_URL",
        "text": "={{ $json.content }}"
      },
      "id": "discord",
      "name": "Send to Discord",
      "type": "n8n-nodes-base.discord",
      "typeVersion": 1,
      "position": [600, 300]
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
    },
    "format": {
      "main": [
        [
          {
            "node": "discord",
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
echo "✅ n8n Setup Complete!"
echo ""
echo "🚀 To start n8n for CROD:"
echo "   ~/.n8n/start-crod-n8n.sh"
echo ""
echo "🌐 Then open: http://localhost:5678"
echo ""
echo "📋 CROD Integration:"
echo "   • Import workflows from ~/.n8n/crod-workflows/"
echo "   • Configure Discord webhook URL"
echo "   • Set webhook paths: /webhook/crod-WORKFLOW_NAME"
echo ""
echo "🔗 Example webhook URLs:"
echo "   • http://localhost:5678/webhook/crod-discord"
echo "   • http://localhost:5678/webhook/crod-trinity"
echo "   • http://localhost:5678/webhook/crod-patterns"