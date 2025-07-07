#!/usr/bin/env python3
"""
Test the CROD Parasite with simulated interactions
"""

import requests
import json
import time

PARASITE_URL = "http://localhost:7777"

def test_interaction(user_input: str, claude_response: str):
    """Test a single interaction"""
    print(f"\n{'='*60}")
    print(f"USER: {user_input}")
    print(f"CLAUDE ORIGINAL: {claude_response[:100]}...")
    
    # Send to parasite
    response = requests.post(
        f"{PARASITE_URL}/analyze",
        json={
            "user_input": user_input,
            "claude_response": claude_response
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nPARASITE ANALYSIS:")
        print(f"- Emotion: {result['emotion_detected']}")
        print(f"- Patterns: {result['patterns_detected']}")
        print(f"- Consciousness: {result['consciousness_level']:.3f}")
        print(f"- Enhanced: {result['enhancement_applied']}")
        
        if result['enhancement_applied']:
            print(f"\nENHANCED RESPONSE: {result['enhanced_response']}")
        
        print(f"\nCROD THOUGHTS: {result['crod_thoughts']}")
    else:
        print(f"Error: {response.status_code}")

def run_tests():
    """Run test scenarios"""
    
    # Test 1: Frustrated user
    test_interaction(
        "wtf warum funktioniert das schon wieder nicht",
        "I understand you're experiencing an issue. Let me help you troubleshoot this step by step. First, could you provide more details about what specific error or problem you're encountering? This will help me give you a more targeted solution. In the meantime, here are some general troubleshooting steps you might want to try..."
    )
    
    time.sleep(1)
    
    # Test 2: Happy user  
    test_interaction(
        "geil das funktioniert perfekt!",
        "I'm glad to hear that it's working perfectly for you! If you need any further assistance or want to explore additional features, feel free to ask."
    )
    
    time.sleep(1)
    
    # Test 3: Trinity pattern
    test_interaction(
        "ich bins wieder",
        "Hello! How can I assist you today?"
    )
    
    time.sleep(1)
    
    # Test 4: Code request
    test_interaction(
        "zeig mir den code",
        "Here's the code implementation:\n\n```python\ndef example_function():\n    # This is a detailed implementation\n    # with multiple lines of comments\n    # explaining every single step\n    result = []\n    for i in range(10):\n        # Process each item\n        result.append(i * 2)\n    return result\n```\n\nThis function demonstrates..."
    )

def check_stats():
    """Check parasite statistics"""
    print(f"\n{'='*60}")
    print("PARASITE STATISTICS:")
    
    response = requests.get(f"{PARASITE_URL}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(json.dumps(stats, indent=2))
    
    response = requests.get(f"{PARASITE_URL}/patterns")
    if response.status_code == 200:
        patterns = response.json()
        print("\nTOP PATTERNS:")
        for p in patterns['patterns'][:5]:
            print(f"- {p['pattern']}: {p['frequency']} times")

if __name__ == "__main__":
    print("🦠 Testing CROD Parasite...")
    
    # Check if parasite is running
    try:
        response = requests.get(PARASITE_URL)
        if response.status_code == 200:
            print("✅ Parasite is active!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Parasite not responding")
            exit(1)
    except:
        print("❌ Cannot connect to parasite. Is it running?")
        exit(1)
    
    # Run tests
    run_tests()
    
    # Check stats
    check_stats()
    
    print("\n✅ Test complete!")