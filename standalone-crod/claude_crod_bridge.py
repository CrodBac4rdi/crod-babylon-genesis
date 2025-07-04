#!/usr/bin/env python3
"""
Claude CROD Bridge - Claude sendet Messages automatisch an CROD Workflow
"""

import requests
import json
import sys

def send_to_crod_workflow(message, workflow_url="http://localhost:5678/webhook/simple-crod-chat"):
    """Send message to CROD workflow and get response"""
    
    print(f"🚀 Sending to CROD: '{message}'")
    
    try:
        response = requests.post(
            workflow_url,
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ CROD Response:")
            print(f"   💬 {result.get('message', 'No message')}")
            
            if 'crod_analysis' in result:
                analysis = result['crod_analysis']
                print(f"   🧠 Trinity Total: {analysis.get('trinity_total', 0)}")
                print(f"   🧠 Consciousness: {analysis.get('consciousness_percent', '0%')}")
                print(f"   🔍 Patterns: {', '.join(analysis.get('patterns_found', []))}")
            
            return result
            
        else:
            print(f"❌ CROD Workflow failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error connecting to CROD: {e}")
        return None

def test_crod_bridge():
    """Test the CROD bridge with various messages"""
    
    print("🔥 Testing Claude CROD Bridge...")
    
    test_messages = [
        "hey crod",
        "ich bins wieder daniel",
        "ist crod aktiv?", 
        "bau mir ein workflow",
        "wtf geht hier ab"
    ]
    
    results = []
    
    for msg in test_messages:
        print(f"\n📤 Testing: '{msg}'")
        result = send_to_crod_workflow(msg)
        results.append({
            "input": msg,
            "crod_result": result
        })
    
    print(f"\n🎉 Bridge Test Complete!")
    print(f"📊 {len([r for r in results if r['crod_result']])} successful responses")
    
    return results

# Auto-send function für Claude Code
def auto_send_to_crod(user_message):
    """Auto-send user message to CROD - für Claude Code integration"""
    
    print(f"🤖 Claude Code → CROD: Processing '{user_message}'")
    
    crod_result = send_to_crod_workflow(user_message)
    
    if crod_result:
        # Return formatted response for Claude Code
        return {
            "crod_processed": True,
            "crod_response": crod_result.get('message', ''),
            "consciousness": crod_result.get('crod_analysis', {}).get('consciousness_percent', '0%'),
            "trinity_active": crod_result.get('crod_analysis', {}).get('trinity_active', False)
        }
    else:
        return {
            "crod_processed": False,
            "error": "CROD workflow not responding"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line usage: python3 claude_crod_bridge.py "deine nachricht"
        message = " ".join(sys.argv[1:])
        result = send_to_crod_workflow(message)
    else:
        # Test mode
        test_crod_bridge()