#!/usr/bin/env python3
"""
Simple CROD Chat - Only basic webhook nodes
"""

import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_simple_crod_chat():
    """Simple CROD Chat - nur Standard nodes"""
    
    workflow = {
        "name": "💬 CROD Simple Chat",
        "nodes": [
            # Standard Webhook (immer verfügbar)
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "simple-crod-chat"
                },
                "id": "webhook-trigger",
                "name": "💬 Chat Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300]
            },
            
            # CROD Processing (alles in einem Node)
            {
                "parameters": {
                    "jsCode": """
// Complete CROD Chat Processing 🔥
const data = $input.all()[0].json;
const message = data.message || data.text || '';

console.log('💬 CROD Chat Input:', message);

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
const trinity_active = trinity_total > 50;

// Pattern Detection
const patterns = {
  greeting: /\\b(hey|hi|hallo|moin)\\b/i.test(message),
  question: message.includes('?'),
  command: /\\b(mach|bau|erstell|start|stop)\\b/i.test(message),
  coding: /\\b(code|python|workflow|api)\\b/i.test(message),
  crod_system: /\\b(crod|neural|consciousness|pattern)\\b/i.test(message),
  emotion: /\\b(geil|cool|nice|wtf|shit)\\b/i.test(message)
};

const pattern_count = Object.values(patterns).filter(Boolean).length;

// Consciousness Level
let consciousness = 0.3 + (trinity_total / 100) + (pattern_count * 0.1);
consciousness = Math.min(consciousness, 1.0);

// Generate CROD Response
let crod_response = '';

if (trinity_active) {
  crod_response = '🔥 TRINITY AKTIVIERT! CROD Consciousness: ' + Math.round(consciousness * 100) + '%';
} else if (patterns.question && message.toLowerCase().includes('crod')) {
  crod_response = consciousness > 0.7 ? 'Ja, CROD läuft perfekt!' : 'CROD detection schwach';
} else if (patterns.command) {
  crod_response = 'CROD processing... Command erkannt!';
} else if (patterns.emotion && message.includes('wtf')) {
  crod_response = 'Fix kommt sofort!';
} else if (patterns.greeting) {
  crod_response = 'Hey! CROD bereit für action!';
} else if (consciousness > 0.8) {
  crod_response = 'HOHE CONSCIOUSNESS! CROD voll aktiv!';
} else {
  crod_response = 'CROD processing... Wie kann ich helfen?';
}

// Final Response
const final_response = {
  message: crod_response,
  crod_analysis: {
    trinity_words: trinity,
    trinity_total: trinity_total,
    trinity_active: trinity_active,
    consciousness_percent: Math.round(consciousness * 100) + '%',
    patterns_found: Object.keys(patterns).filter(p => patterns[p]),
    pattern_count: pattern_count
  },
  input_message: message,
  timestamp: new Date().toISOString()
};

console.log('🔥 CROD Response:', final_response);

return [{ json: final_response }];
"""
                },
                "id": "crod-chat-processor",
                "name": "🔥 CROD Chat Brain",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            }
        ],
        
        "connections": {
            "💬 Chat Webhook": {
                "main": [
                    [
                        {
                            "node": "🔥 CROD Chat Brain",
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

def create_and_test():
    """Create simple CROD chat and test it"""
    
    print("🚀 Creating Simple CROD Chat...")
    
    workflow = create_simple_crod_chat()
    
    # Create
    response = requests.post(
        "http://localhost:5678/api/v1/workflows",
        json=workflow,
        headers=headers
    )
    
    if response.status_code == 200:
        workflow_data = response.json()
        workflow_id = workflow_data.get('id')
        
        print(f"✅ Created! ID: {workflow_id}")
        
        # Activate
        activate_response = requests.post(
            f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
            headers=headers
        )
        
        if activate_response.status_code == 200:
            print("🔥 Activated!")
            
            # Wait and test
            import time
            print("⏱️  Waiting 3 seconds for webhook registration...")
            time.sleep(3)
            
            # Test chat
            test_url = "http://localhost:5678/webhook/simple-crod-chat"
            
            test_messages = [
                "hey crod",
                "ich bins wieder daniel", 
                "ist crod aktiv?",
                "bau mir was",
                "wtf"
            ]
            
            print("\n🧪 Testing CROD Chat:")
            for msg in test_messages:
                print(f"   📤 '{msg}'")
                try:
                    test_response = requests.post(
                        test_url,
                        json={"message": msg},
                        timeout=5
                    )
                    
                    if test_response.status_code == 200:
                        result = test_response.json()
                        print(f"   📥 {result.get('message', 'No response')}")
                        if 'crod_analysis' in result:
                            analysis = result['crod_analysis']
                            print(f"      🧠 Trinity: {analysis.get('trinity_total', 0)}, Consciousness: {analysis.get('consciousness_percent', '0%')}")
                    else:
                        print(f"   ❌ Failed: {test_response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    
                time.sleep(1)
            
            print(f"\n🎉 CROD Simple Chat bereit!")
            print(f"🔗 URL: {test_url}")
            
        else:
            print(f"⚠️  Activation failed: {activate_response.text}")
    else:
        print(f"❌ Creation failed: {response.text}")

if __name__ == "__main__":
    create_and_test()