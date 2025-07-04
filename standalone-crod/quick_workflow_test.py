#!/usr/bin/env python3
"""
Quick CROD Workflow Test - No Auth needed
"""

import requests
import json

def test_n8n_direct():
    """Test n8n directly without auth"""
    
    print("🚀 Testing n8n direct connection...")
    
    # Test n8n health
    try:
        health = requests.get("http://localhost:5678/healthz")
        print(f"   Health: {health.status_code}")
    except Exception as e:
        print(f"   Health failed: {e}")
        return
    
    # Simple webhook workflow JSON
    workflow = {
        "name": "CROD Trinity Test",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crod-test",
                    "responseMode": "onReceived"
                },
                "id": "webhook1",
                "name": "Trinity Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "values": {
                        "string": [
                            {
                                "name": "message",
                                "value": "CROD Trinity detected!"
                            }
                        ]
                    }
                },
                "id": "response1",
                "name": "Response",
                "type": "n8n-nodes-base.set",
                "typeVersion": 1,
                "position": [400, 300]
            }
        ],
        "connections": {
            "Trinity Webhook": {
                "main": [
                    [
                        {
                            "node": "Response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True
    }
    
    # Try creating workflow
    try:
        print("   Creating workflow...")
        response = requests.post(
            "http://localhost:5678/api/v1/workflows",
            json=workflow,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Workflow creation: {response.status_code}")
        
        if response.status_code == 201:
            workflow_data = response.json()
            webhook_url = f"http://localhost:5678/webhook/crod-test"
            print(f"   ✅ Workflow created!")
            print(f"   🔗 Webhook URL: {webhook_url}")
            
            # Test the webhook
            test_data = {
                "message": "ich bins wieder daniel",
                "trinity": {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67}
            }
            
            print("   Testing webhook...")
            webhook_response = requests.post(webhook_url, json=test_data)
            print(f"   Webhook test: {webhook_response.status_code}")
            if webhook_response.status_code == 200:
                print(f"   Response: {webhook_response.text}")
                print("   🎉 CROD Workflow läuft!")
            
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Workflow creation failed: {e}")

if __name__ == "__main__":
    test_n8n_direct()