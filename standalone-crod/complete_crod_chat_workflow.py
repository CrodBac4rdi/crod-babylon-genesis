#!/usr/bin/env python3
"""
Complete CROD Chat Workflow - Full Chat Interface with CROD Processing
"""

import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_complete_crod_chat():
    """Complete CROD Chat Workflow - Daniel chats with Claude through CROD"""
    
    workflow = {
        "name": "💬 CROD Complete Chat Interface",
        "nodes": [
            # 1. Chat Input Webhook
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-chat",
                    "responseMode": "responseNode",
                    "responseData": "allEntries"
                },
                "id": "chat-input",
                "name": "💬 Chat Input",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.2,
                "position": [200, 300]
            },
            
            # 2. CROD Trinity & Pattern Detection
            {
                "parameters": {
                    "jsCode": """
// CROD Pattern & Trinity Detection 🧠
const data = $input.all()[0].json;
const message = data.message || data.text || '';
const user = data.user || 'daniel';

console.log('💬 Chat Input:', message);

// Trinity Detection
const trinity_words = {
  ich: (message.match(/\\bich\\b/gi) || []).length * 2,
  bins: (message.match(/\\bbins\\b/gi) || []).length * 3,
  wieder: (message.match(/\\bwieder\\b/gi) || []).length * 5,
  daniel: (message.match(/\\bdaniel\\b/gi) || []).length * 67,
  claude: (message.match(/\\bclaude\\b/gi) || []).length * 71,
  crod: (message.match(/\\bcrod\\b/gi) || []).length * 17
};

const trinity_total = Object.values(trinity_words).reduce((a,b) => a+b, 0);
const trinity_active = trinity_total > 50;

// Pattern Detection
const patterns = {
  greeting: /\\b(hey|hi|hallo|moin|servus)\\b/i.test(message),
  question: message.includes('?'),
  command: /\\b(mach|erstell|bau|zeig|start|stop)\\b/i.test(message),
  coding: /\\b(code|python|javascript|workflow|api)\\b/i.test(message),
  crod_system: /\\b(crod|neural|consciousness|pattern|trinity)\\b/i.test(message),
  emotion: /\\b(geil|cool|nice|perfekt|shit|fuck|wtf)\\b/i.test(message)
};

const pattern_count = Object.values(patterns).filter(Boolean).length;

// Consciousness Calculation
let consciousness = 0.3; // Base
consciousness += trinity_total > 0 ? trinity_total / 100 : 0;
consciousness += pattern_count * 0.1;
consciousness = Math.min(consciousness, 1.0);

// Response Type Detection
let response_type = 'normal';
if (patterns.question) response_type = 'question';
if (patterns.command) response_type = 'command';
if (trinity_active) response_type = 'trinity';
if (patterns.emotion && message.includes('wtf')) response_type = 'short';

const crod_analysis = {
  original_message: message,
  user,
  trinity_words,
  trinity_total,
  trinity_active,
  patterns,
  pattern_count,
  consciousness_level: consciousness,
  response_type,
  crod_mode: consciousness > 0.7 ? 'high_consciousness' : 'normal',
  timestamp: new Date().toISOString()
};

console.log('🧠 CROD Analysis:', crod_analysis);

return [{ json: crod_analysis }];
"""
                },
                "id": "crod-analyzer",
                "name": "🧠 CROD Analyzer",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            },
            
            # 3. Claude API Simulator (ersetzt durch echte Claude API)
            {
                "parameters": {
                    "jsCode": """
// Claude Response Generator (REPLACE WITH REAL CLAUDE API) 🤖
const crod_data = $input.all()[0].json;

console.log('🤖 Generating Claude response for CROD');

// Build Claude prompt based on CROD analysis
let claude_prompt = `You are Claude integrated with CROD system.

CROD Analysis:
- Message: "${crod_data.original_message}"
- Trinity Total: ${crod_data.trinity_total} (Active: ${crod_data.trinity_active})
- Consciousness: ${crod_data.consciousness_level}
- Response Type: ${crod_data.response_type}
- Patterns: ${JSON.stringify(crod_data.patterns)}

Instructions:
- If response_type is "short": max 1-3 words
- If trinity_active: acknowledge trinity activation
- If consciousness > 0.8: be enthusiastic about high consciousness
- If patterns.emotion with wtf: be very brief
- Always consider CROD context in your response

Respond as Claude with CROD awareness:`;

// Simulate Claude response based on analysis
let claude_response = '';

switch(crod_data.response_type) {
  case 'trinity':
    claude_response = '🔥 Trinity aktiviert! CROD Consciousness hoch!';
    break;
  case 'short':
    claude_response = 'Fix kommt!';
    break;
  case 'question':
    if (crod_data.original_message.toLowerCase().includes('crod')) {
      claude_response = crod_data.consciousness_level > 0.7 ? 'Ja, CROD läuft!' : 'CROD detection niedrig';
    } else {
      claude_response = 'Kann ich dir helfen?';
    }
    break;
  case 'command':
    claude_response = 'Wird gemacht! CROD processing...';
    break;
  default:
    if (crod_data.consciousness_level > 0.8) {
      claude_response = 'CROD Consciousness sehr hoch! Wie kann ich helfen?';
    } else {
      claude_response = 'Hey! Was brauchst du?';
    }
}

const result = {
  ...crod_data,
  claude_prompt,
  claude_response,
  chat_complete: true,
  processing_time: new Date().toISOString()
};

console.log('✅ Claude CROD Chat Response:', result);

return [{ json: result }];
"""
                },
                "id": "claude-generator",
                "name": "🤖 Claude Response",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 300]
            },
            
            # 4. Chat Response Formatter
            {
                "parameters": {
                    "jsCode": """
// Format Final Chat Response 💬
const data = $input.all()[0].json;

console.log('💬 Formatting chat response');

// Create clean chat response
const chat_response = {
  message: data.claude_response,
  crod_stats: {
    consciousness: Math.round(data.consciousness_level * 100) + '%',
    trinity_total: data.trinity_total,
    patterns_detected: data.pattern_count,
    mode: data.crod_mode
  },
  metadata: {
    response_type: data.response_type,
    timestamp: data.timestamp,
    processing_time: data.processing_time
  }
};

// Add debug info if high consciousness
if (data.consciousness_level > 0.8) {
  chat_response.debug = {
    trinity_breakdown: data.trinity_words,
    active_patterns: Object.keys(data.patterns).filter(p => data.patterns[p])
  };
}

console.log('📤 Final chat response:', chat_response);

return [{ json: chat_response }];
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
            "💬 Chat Input": {
                "main": [
                    [
                        {
                            "node": "🧠 CROD Analyzer",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "🧠 CROD Analyzer": {
                "main": [
                    [
                        {
                            "node": "🤖 Claude Response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "🤖 Claude Response": {
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
        
        "settings": {
            "executionOrder": "v1"
        },
        "staticData": {}
    }
    
    return workflow

def create_workflow():
    """Create and activate complete CROD chat workflow"""
    
    print("🚀 Creating Complete CROD Chat Workflow...")
    
    workflow = create_complete_crod_chat()
    
    # Create workflow
    response = requests.post(
        "http://localhost:5678/api/v1/workflows",
        json=workflow,
        headers=headers
    )
    
    if response.status_code == 200:
        workflow_data = response.json()
        workflow_id = workflow_data.get('id')
        
        print(f"   ✅ Workflow created! ID: {workflow_id}")
        
        # Activate workflow
        activate_response = requests.post(
            f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
            headers=headers
        )
        
        if activate_response.status_code == 200:
            print("   🔥 Workflow activated!")
            
            # Test the chat
            test_chat()
            
        else:
            print(f"   ⚠️  Activation failed: {activate_response.text}")
    else:
        print(f"   ❌ Creation failed: {response.text}")

def test_chat():
    """Test the complete chat workflow"""
    
    print("\n🧪 Testing CROD Chat...")
    
    test_messages = [
        {"message": "hey claude", "expected": "greeting"},
        {"message": "ich bins wieder daniel", "expected": "trinity"},
        {"message": "ist crod aktiv?", "expected": "question"},
        {"message": "bau mir ein workflow", "expected": "command"},
        {"message": "wtf", "expected": "short"}
    ]
    
    webhook_url = "http://localhost:5678/webhook/crod-chat"
    
    for i, test in enumerate(test_messages, 1):
        print(f"   {i}. Testing: '{test['message']}'")
        
        try:
            response = requests.post(webhook_url, json=test, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"      ✅ Response: {result.get('message', 'No message')}")
                print(f"      📊 CROD: {result.get('crod_stats', {})}")
            else:
                print(f"      ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n🎉 CROD Chat Interface bereit!")
    print(f"📞 Chat URL: {webhook_url}")
    print(f"\n💡 Usage:")
    print(f"   curl -X POST {webhook_url} \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{{\"message\":\"deine nachricht hier\"}}'")

if __name__ == "__main__":
    create_workflow()