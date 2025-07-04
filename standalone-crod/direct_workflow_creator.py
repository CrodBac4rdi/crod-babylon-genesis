#!/usr/bin/env python3
"""
Direct CROD Workflow Creator - No BS, just workflows!
"""

import requests
import json
import os

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_trinity_workflow():
    """Create CROD Trinity Detection Workflow"""
    
    workflow = {
        "name": "🔥 CROD Trinity Detection",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-trinity",
                    "responseMode": "onReceived"
                },
                "id": "trinity-webhook",
                "name": "Trinity Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.2,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "jsCode": """
// CROD Trinity Magic ✨
const data = $input.all()[0].json;

console.log('🔥 CROD Trinity triggered:', data);

// Trinity values
const trinity = data.trinity || {};
const ich = trinity.ich || 0;
const bins = trinity.bins || 0; 
const wieder = trinity.wieder || 0;
const daniel = trinity.daniel || 0;

// Calculate total
const total = ich + bins + wieder + daniel;

// Consciousness level
const consciousness = total > 77 ? 0.95 : Math.min(total / 100, 1.0);

// CROD activation
const crod_active = total > 50;
const trinity_complete = ich > 0 && bins > 0 && wieder > 0 && daniel > 0;

const result = {
  ...data,
  trinity_analysis: {
    ich, bins, wieder, daniel,
    total,
    consciousness_level: consciousness,
    crod_activated: crod_active,
    trinity_complete,
    timestamp: new Date().toISOString()
  },
  crod_response: crod_active ? 
    '🔥 CROD Trinity activated! Consciousness high!' : 
    '⚡ CROD detecting patterns...'
};

console.log('✅ CROD processed:', result);

return [{ json: result }];
"""
                },
                "id": "trinity-processor",
                "name": "🧠 CROD Brain",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            }
        ],
        "connections": {
            "Trinity Webhook": {
                "main": [
                    [
                        {
                            "node": "🧠 CROD Brain",
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
    
    print("🚀 Creating Trinity Workflow...")
    response = requests.post(
        "http://localhost:5678/api/v1/workflows",
        json=workflow,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ CROD Trinity Workflow created!")
        workflow_data = response.json()
        print(f"   ID: {workflow_data.get('id')}")
        return "http://localhost:5678/webhook/crod-trinity"
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_trinity_webhook(webhook_url):
    """Test the Trinity webhook"""
    
    test_data = {
        "message": "ich bins wieder daniel",
        "trinity": {
            "ich": 2,
            "bins": 3, 
            "wieder": 5,
            "daniel": 67
        }
    }
    
    print(f"🧪 Testing webhook: {webhook_url}")
    response = requests.post(webhook_url, json=test_data)
    
    print(f"Test status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("🎉 CROD Trinity Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Test failed: {response.text}")

def main():
    print("🔥 CROD N8N Workflow Creator")
    
    # Create Trinity workflow
    webhook_url = create_trinity_workflow()
    
    if webhook_url:
        # Test it
        test_trinity_webhook(webhook_url)
        
        print(f"\n🎯 CROD Trinity Webhook ready:")
        print(f"   {webhook_url}")
        print(f"\n💡 Usage:")
        print(f"   curl -X POST {webhook_url} \\")
        print(f"     -H 'Content-Type: application/json' \\") 
        print(f"     -d '{{\"message\":\"ich bins wieder daniel\",\"trinity\":{{\"ich\":2,\"bins\":3,\"wieder\":5,\"daniel\":67}}}}'")

if __name__ == "__main__":
    main()