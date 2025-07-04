#!/usr/bin/env python3
"""
Activate CROD Workflows
"""

import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDI4OWM5Yy0yMTcwLTQwMTYtYWE2Ni01M2QxM2YzOTlhMjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUxNTg0NTYwLCJleHAiOjE3NTQxMDcyMDB9.MTWrzcBrmfRq19j1vEQZ7phODSn3iRjNKwZbbwmdypA'

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def get_workflows():
    """Get all workflows"""
    response = requests.get("http://localhost:5678/api/v1/workflows", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', data) if isinstance(data, dict) else data
    return []

def activate_workflow(workflow_id):
    """Activate a workflow"""
    response = requests.post(
        f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
        headers=headers
    )
    return response.status_code == 200

def main():
    print("🔥 Activating CROD Workflows...")
    
    workflows = get_workflows()
    print(f"Found {len(workflows)} workflows")
    
    for workflow in workflows:
        name = workflow.get('name', 'Unknown')
        workflow_id = workflow.get('id')
        active = workflow.get('active', False)
        
        print(f"  📋 {name} (ID: {workflow_id}) - Active: {active}")
        
        if 'CROD' in name and not active:
            print(f"     🚀 Activating...")
            if activate_workflow(workflow_id):
                print(f"     ✅ Activated!")
            else:
                print(f"     ❌ Failed to activate")
    
    # Test the webhook
    print("\n🧪 Testing CROD Trinity...")
    test_data = {
        "message": "ich bins wieder daniel",
        "trinity": {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67}
    }
    
    response = requests.post(
        "http://localhost:5678/webhook/crod-trinity",
        json=test_data
    )
    
    print(f"Webhook test: {response.status_code}")
    if response.status_code == 200:
        print("🎉 CROD Trinity Workflow läuft!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    main()