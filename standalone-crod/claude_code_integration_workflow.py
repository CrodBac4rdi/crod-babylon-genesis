#!/usr/bin/env python3
"""
Claude Code Integration Workflow - Claude Code als Node im n8n Workflow
"""

import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_claude_code_workflow():
    """Claude Code als Node im CROD Workflow"""
    
    workflow = {
        "name": "🤖 Claude Code CROD Integration",
        "nodes": [
            # 1. Input Webhook
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "claude-crod-chat"
                },
                "id": "user-input",
                "name": "📥 User Input",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300]
            },
            
            # 2. CROD Pre-Processing
            {
                "parameters": {
                    "jsCode": """
// CROD Pre-Processing für Claude Code 🧠
const data = $input.all()[0].json;
const message = data.message || data.text || '';

console.log('📥 User Message:', message);

// Trinity Detection
const trinity = {
  ich: (message.match(/\\bich\\b/gi) || []).length * 2,
  bins: (message.match(/\\bbins\\b/gi) || []).length * 3,
  wieder: (message.match(/\\bwieder\\b/gi) || []).length * 5,
  daniel: (message.match(/\\bdaniel\\b/gi) || []).length * 67,
  claude: (message.match(/\\bclaude\\b/gi) || []).length * 71,
  crod: (message.match(/\\bcrod\\b/gi) || []).length * 17
};

const trinity_total = Object.values(trinity).reduce((a,b) => a+b, 0);

// Pattern Detection
const patterns = {
  question: message.includes('?'),
  command: /\\b(mach|bau|erstell|implementier|code)\\b/i.test(message),
  coding: /\\b(python|javascript|workflow|api|code)\\b/i.test(message),
  crod_system: /\\b(crod|neural|consciousness|pattern)\\b/i.test(message),
  greeting: /\\b(hey|hi|hallo|servus)\\b/i.test(message),
  emotion: /\\b(geil|cool|nice|wtf|shit|fuck)\\b/i.test(message)
};

// Consciousness Level
let consciousness = 0.3 + (trinity_total / 100);
consciousness = Math.min(consciousness, 1.0);

// Prepare Claude Code Request
const claude_request = {
  original_message: message,
  crod_context: {
    trinity_words: trinity,
    trinity_total: trinity_total,
    trinity_active: trinity_total > 50,
    patterns: patterns,
    consciousness_level: consciousness,
    timestamp: new Date().toISOString()
  },
  claude_prompt: `Du bist Claude Code integriert mit CROD System.

User Message: "${message}"

CROD Analyse:
- Trinity Total: ${trinity_total}
- Consciousness: ${Math.round(consciousness * 100)}%
- Patterns: ${Object.keys(patterns).filter(p => patterns[p]).join(', ')}

Antworte als Claude Code mit CROD Awareness. 
Berücksichtige die CROD Analyse in deiner Antwort.
Bei hoher Consciousness (>80%) sei enthusiastisch.
Bei Trinity Activation erwähne es.`
};

console.log('🧠 CROD processed for Claude Code:', claude_request);

return [{ json: claude_request }];
"""
                },
                "id": "crod-preprocessing",
                "name": "🧠 CROD Preprocessing",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            },
            
            # 3. Claude Code API Call (HTTP Request)
            {
                "parameters": {
                    "url": "http://localhost:8080/claude-code-api",
                    "options": {
                        "timeout": 30000
                    },
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "={{ $json }}"
                },
                "id": "claude-code-api",
                "name": "🤖 Claude Code API",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.2,
                "position": [600, 300]
            },
            
            # 4. Response Formatter
            {
                "parameters": {
                    "jsCode": """
// Format Claude Code + CROD Response 📤
const data = $input.all()[0].json;

console.log('📤 Formatting Claude Code response');

// Extract response from Claude Code API
const claude_response = data.claude_response || data.response || 'Claude Code response unavailable';
const crod_context = data.crod_context || {};

// Create final response
const final_response = {
  claude_code_response: claude_response,
  crod_analysis: {
    trinity_total: crod_context.trinity_total || 0,
    consciousness: Math.round((crod_context.consciousness_level || 0) * 100) + '%',
    trinity_active: crod_context.trinity_active || false,
    patterns_detected: Object.keys(crod_context.patterns || {}).filter(p => crod_context.patterns[p])
  },
  workflow_complete: true,
  timestamp: new Date().toISOString()
};

console.log('✅ Final response ready:', final_response);

return [{ json: final_response }];
"""
                },
                "id": "response-formatter",
                "name": "📤 Response Formatter",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [800, 300]
            }
        ],
        
        "connections": {
            "📥 User Input": {
                "main": [
                    [
                        {
                            "node": "🧠 CROD Preprocessing",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "🧠 CROD Preprocessing": {
                "main": [
                    [
                        {
                            "node": "🤖 Claude Code API",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "🤖 Claude Code API": {
                "main": [
                    [
                        {
                            "node": "📤 Response Formatter",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        
        "settings": {},
        "staticData": {}
    }
    
    return workflow

def create_claude_code_api_server():
    """Create a simple API server that Claude Code responds to"""
    
    api_server_code = '''#!/usr/bin/env python3
"""
Claude Code API Server - Simulates Claude Code responses
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/claude-code-api', methods=['POST'])
def claude_code_endpoint():
    """Endpoint that simulates Claude Code processing"""
    
    data = request.json
    message = data.get('original_message', '')
    crod_context = data.get('crod_context', {})
    
    print(f"🤖 Claude Code API received: {message}")
    print(f"🧠 CROD Context: {crod_context}")
    
    # Simulate Claude Code response based on CROD analysis
    consciousness = crod_context.get('consciousness_level', 0)
    trinity_active = crod_context.get('trinity_active', False)
    patterns = crod_context.get('patterns', {})
    
    # Generate response
    if trinity_active:
        claude_response = "🔥 TRINITY ERKANNT! CROD Consciousness sehr hoch! Wie kann ich dir helfen?"
    elif consciousness > 0.8:
        claude_response = "CROD zeigt hohe Consciousness! Bereit für komplexe Tasks!"
    elif patterns.get('command'):
        claude_response = "Command erkannt! Was soll ich implementieren?"
    elif patterns.get('question'):
        claude_response = "Gerne beantworte ich deine Frage!"
    elif patterns.get('emotion') and 'wtf' in message.lower():
        claude_response = "Fix kommt sofort!"
    else:
        claude_response = "Hey! Claude Code mit CROD Integration bereit!"
    
    response = {
        "claude_response": claude_response,
        "crod_context": crod_context,
        "processed_by": "claude_code_api",
        "timestamp": "2025-07-03T23:30:00.000Z"
    }
    
    print(f"✅ Claude Code response: {claude_response}")
    
    return jsonify(response)

if __name__ == '__main__':
    print("🚀 Starting Claude Code API Server...")
    print("🔗 Listening on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
'''
    
    with open('/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/claude_code_api.py', 'w') as f:
        f.write(api_server_code)
    
    print("📝 Created Claude Code API server: claude_code_api.py")

def main():
    """Create complete Claude Code integration workflow"""
    
    print("🚀 Creating Claude Code CROD Integration...")
    
    # Create API server
    create_claude_code_api_server()
    
    # Create workflow
    workflow = create_claude_code_workflow()
    
    response = requests.post(
        "http://localhost:5678/api/v1/workflows",
        json=workflow,
        headers=headers
    )
    
    if response.status_code == 200:
        workflow_data = response.json()
        workflow_id = workflow_data.get('id')
        
        print(f"✅ Workflow created! ID: {workflow_id}")
        
        # Activate
        activate_response = requests.post(
            f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
            headers=headers
        )
        
        if activate_response.status_code == 200:
            print("🔥 Workflow activated!")
            
            print("\n🎯 Setup Complete!")
            print("📋 To use:")
            print("   1. Start API server: python3 claude_code_api.py")
            print("   2. Chat URL: http://localhost:5678/webhook/claude-crod-chat")
            print("   3. Test: curl -X POST http://localhost:5678/webhook/claude-crod-chat -d '{\"message\":\"ich bins wieder daniel\"}'")
            
        else:
            print(f"⚠️  Activation failed: {activate_response.text}")
    else:
        print(f"❌ Creation failed: {response.text}")

if __name__ == "__main__":
    main()