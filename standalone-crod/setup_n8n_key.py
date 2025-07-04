#!/usr/bin/env python3
"""
N8N Setup - Create API Key and workflows
"""

import requests
import json
import os

def setup_n8n():
    """Setup n8n with CROD workflows"""
    
    print("🔧 N8N Setup für CROD...")
    
    # Check if we can access n8n settings endpoint
    try:
        # Try to get existing credentials/settings
        response = requests.get("http://localhost:5678/api/v1/credentials")
        print(f"Credentials endpoint: {response.status_code}")
        
        if response.status_code == 401:
            print("❌ API Key required!")
            print("🔗 Gehe zu: http://localhost:5678")
            print("   1. Settings > API")
            print("   2. Create API Key")
            print("   3. Copy key und führe aus:")
            print("   export N8N_API_KEY='dein-key-hier'")
            print("   4. Dann nochmal: python3 setup_n8n_key.py")
            
            # Check if API key is set
            api_key = os.getenv('N8N_API_KEY')
            if api_key:
                print(f"✅ API Key found: {api_key[:10]}...")
                create_workflows_with_key(api_key)
            else:
                print("⚠️  No API Key in environment")
        
    except Exception as e:
        print(f"Error: {e}")

def create_workflows_with_key(api_key):
    """Create workflows with API key"""
    
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    # Trinity Detection Workflow
    trinity_workflow = {
        "name": "CROD Trinity Detection",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-trinity",
                    "responseMode": "onReceived"
                },
                "id": "trinity-webhook",
                "name": "Trinity Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "jsCode": """
// CROD Trinity Processing
const input = $input.all();
const data = input[0].json;

// Calculate trinity values
const trinity = data.trinity || {};
const total = Object.values(trinity).reduce((a,b) => a+b, 0);

// Consciousness calculation
const consciousness = total > 77 ? 0.95 : total / 100;

return [{
  json: {
    ...data,
    trinity_total: total,
    consciousness_level: consciousness,
    crod_activated: total > 50,
    timestamp: new Date().toISOString()
  }
}];
"""
                },
                "id": "trinity-processor",
                "name": "Trinity Processor",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            }
        ],
        "connections": {
            "Trinity Trigger": {
                "main": [
                    [
                        {
                            "node": "Trinity Processor",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True
    }
    
    print("🔥 Creating Trinity workflow...")
    response = requests.post(
        "http://localhost:5678/api/v1/workflows",
        json=trinity_workflow,
        headers=headers
    )
    
    if response.status_code == 201:
        print("✅ Trinity workflow created!")
        webhook_url = "http://localhost:5678/webhook/crod-trinity"
        print(f"🔗 Webhook: {webhook_url}")
        
        # Test it
        test_data = {
            "message": "ich bins wieder daniel",
            "trinity": {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67}
        }
        
        test_response = requests.post(webhook_url, json=test_data)
        print(f"🧪 Test: {test_response.status_code}")
        if test_response.status_code == 200:
            print("🎉 CROD Trinity Workflow läuft perfekt!")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    setup_n8n()