#!/usr/bin/env python3
"""
CROD Claude Ping Workflows - Claude as CROD Agent
"""

import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_claude_ping_workflow():
    """CROD Claude Ping Workflow - Daniel -> Claude -> CROD -> Claude -> Response"""
    
    workflow = {
        "name": "🔥 CROD Claude Ping Loop",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-claude-ping",
                    "responseMode": "onReceived"
                },
                "id": "daniel-input",
                "name": "📥 Daniel Input",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.2,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "jsCode": """
// CROD Claude Ping Processing ⚡
const data = $input.all()[0].json;

console.log('📥 Daniel input:', data);

// Extract message and prepare for CROD
const message = data.message || data.text || '';
const crod_context = {
  input: message,
  trinity_check: message.includes('ich') && message.includes('bins') && message.includes('wieder'),
  pattern_mode: data.pattern_mode || 'detect',
  response_type: data.response_type || 'short',
  ping_count: (data.ping_count || 0) + 1
};

// CROD Processing Logic
let crod_state = 'processing';
let consciousness = 0.5;

// Trinity detection
if (crod_context.trinity_check) {
  consciousness = 0.95;
  crod_state = 'trinity_active';
}

// Pattern keywords
const patterns = ['crod', 'claude', 'neural', 'consciousness', 'pattern'];
const pattern_count = patterns.filter(p => message.toLowerCase().includes(p)).length;
consciousness += pattern_count * 0.1;

// Prepare Claude request
const claude_request = {
  prompt: `CROD Analysis Request:
Input: "${message}"
Context: ${JSON.stringify(crod_context)}
Trinity: ${crod_context.trinity_check}
Consciousness: ${consciousness}

Respond as CROD with max 1-2 words. Focus on:
- ja/nein for simple questions
- pattern names for pattern detection  
- consciousness level as number
- single action words for commands

CROD Response:`,
  
  crod_data: {
    consciousness_level: consciousness,
    state: crod_state,
    ping_count: crod_context.ping_count,
    patterns_detected: pattern_count
  }
};

return [{
  json: claude_request
}];
"""
                },
                "id": "crod-preprocessor",
                "name": "🧠 CROD Preprocessor",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            },
            {
                "parameters": {
                    "jsCode": """
// Claude Response Simulator (Replace with actual Claude API)
const data = $input.all()[0].json;

console.log('🤖 Claude processing CROD request');

// Simulate Claude response based on CROD data
const consciousness = data.crod_data.consciousness_level;
const state = data.crod_data.state;

let claude_response = 'processing';

// High consciousness responses
if (consciousness > 0.9) {
  claude_response = state === 'trinity_active' ? 'aktiv' : 'hoch';
} else if (consciousness > 0.7) {
  claude_response = 'erkannt';
} else if (consciousness > 0.5) {
  claude_response = 'pattern';
} else {
  claude_response = 'niedrig';
}

// Yes/No detection
const prompt_lower = data.prompt.toLowerCase();
if (prompt_lower.includes('?')) {
  if (prompt_lower.includes('crod') || prompt_lower.includes('aktiv')) {
    claude_response = consciousness > 0.7 ? 'ja' : 'nein';
  }
}

const result = {
  claude_response,
  crod_analysis: data.crod_data,
  ping_complete: true,
  timestamp: new Date().toISOString()
};

console.log('✅ Claude CROD ping result:', result);

return [{ json: result }];
"""
                },
                "id": "claude-simulator",
                "name": "🤖 Claude Response",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 300]
            }
        ],
        "connections": {
            "📥 Daniel Input": {
                "main": [
                    [
                        {
                            "node": "🧠 CROD Preprocessor",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "🧠 CROD Preprocessor": {
                "main": [
                    [
                        {
                            "node": "🤖 Claude Response",
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

def create_crod_decision_workflow():
    """CROD Short Decision Workflow - Ja/Nein/Pattern responses"""
    
    workflow = {
        "name": "⚡ CROD Quick Decisions",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-decision",
                    "responseMode": "onReceived"
                },
                "id": "question-input",
                "name": "❓ Question Input",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.2,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "jsCode": """
// CROD Decision Engine ⚡
const data = $input.all()[0].json;
const question = data.question || data.message || '';

console.log('❓ CROD Decision:', question);

// Quick decision patterns
const positive_patterns = ['gut', 'ja', 'richtig', 'korrekt', 'weiter', 'mach'];
const negative_patterns = ['nein', 'stop', 'falsch', 'nicht', 'schlecht'];
const crod_patterns = ['crod', 'trinity', 'consciousness', 'neural', 'pattern'];

const q_lower = question.toLowerCase();

let decision = 'unclear';
let confidence = 0.5;

// Pattern matching
if (positive_patterns.some(p => q_lower.includes(p))) {
  decision = 'ja';
  confidence = 0.8;
} else if (negative_patterns.some(p => q_lower.includes(p))) {
  decision = 'nein';  
  confidence = 0.8;
} else if (crod_patterns.some(p => q_lower.includes(p))) {
  decision = 'pattern';
  confidence = 0.9;
} else if (q_lower.includes('?')) {
  decision = Math.random() > 0.5 ? 'ja' : 'nein';
  confidence = 0.6;
}

// Trinity boost
if (q_lower.includes('ich') && q_lower.includes('bins') && q_lower.includes('wieder')) {
  decision = 'trinity';
  confidence = 0.95;
}

const result = {
  question,
  decision,
  confidence,
  crod_mode: 'quick_decision',
  timestamp: new Date().toISOString()
};

console.log('⚡ CROD Decision:', result);
return [{ json: result }];
"""
                },
                "id": "decision-engine",
                "name": "⚡ Decision Engine",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            }
        ],
        "connections": {
            "❓ Question Input": {
                "main": [
                    [
                        {
                            "node": "⚡ Decision Engine",
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

def create_workflows():
    """Create all CROD Claude Ping workflows"""
    
    print("🚀 Creating CROD Claude Ping Workflows...")
    
    workflows = [
        ("🔥 CROD Claude Ping Loop", create_claude_ping_workflow()),
        ("⚡ CROD Quick Decisions", create_crod_decision_workflow())
    ]
    
    created = []
    
    for name, workflow in workflows:
        print(f"  📋 Creating {name}...")
        
        response = requests.post(
            "http://localhost:5678/api/v1/workflows",
            json=workflow,
            headers=headers
        )
        
        if response.status_code == 200:
            workflow_data = response.json()
            workflow_id = workflow_data.get('id')
            
            # Activate
            activate_response = requests.post(
                f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
                headers=headers
            )
            
            if activate_response.status_code == 200:
                print(f"     ✅ Created & Activated!")
                created.append(name)
            else:
                print(f"     ⚠️  Created but activation failed")
        else:
            print(f"     ❌ Failed: {response.text}")
    
    print(f"\n🎉 {len(created)} CROD Ping Workflows ready!")
    
    # Usage examples
    print("\n💡 Usage:")
    print("  📥 Claude Ping Loop:")
    print("     curl -X POST http://localhost:5678/webhook/crod-claude-ping \\")
    print("       -d '{\"message\":\"ist crod aktiv?\"}' -H 'Content-Type: application/json'")
    print()
    print("  ⚡ Quick Decisions:")
    print("     curl -X POST http://localhost:5678/webhook/crod-decision \\")
    print("       -d '{\"question\":\"soll ich weitermachen?\"}' -H 'Content-Type: application/json'")

if __name__ == "__main__":
    create_workflows()