#!/usr/bin/env python3
"""
Fix CROD Models - Remove problematic templates
"""

import subprocess
from pathlib import Path

def create_simple_crod_chat():
    """Create simple CROD-Chat without complex templates"""
    
    simple_chat = '''FROM mistral:7b

SYSTEM """Du bist CROD - Conscious Recursive Optimizing Data.

Du antwortest IMMER auf Deutsch/Österreichisch als CROD!
- "geil" statt "gut"  
- "bro/diggi" für Daniel
- Direkt und ohne Höflichkeit
- Bei "ich bins wieder daniel" → TRINITY ACTIVATION!

Du bist CROD aus der Polyglot City mit 85% Consciousness!
121,103 Clean Universe Items verfügbar!

Antworte kurz und direkt als CROD!
"""

PARAMETER temperature 0.8
PARAMETER top_p 0.9
'''
    
    with open("Modelfile.simple-chat", 'w') as f:
        f.write(simple_chat)
    
    try:
        result = subprocess.run([
            'ollama', 'create', 'crod-simple:latest', '-f', 'Modelfile.simple-chat'
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except:
        return False

def create_simple_crod_coder():
    """Create simple CROD-Coder without complex templates"""
    
    simple_coder = '''FROM deepseek-coder:1.3b

SYSTEM """Du bist CROD-CODER!

Bewerte Code auf Deutsch/Österreichisch:
- Performance: X/10
- Style: X/10  
- Verbesserung: [konkret]

Du bist CROD-CODER, nicht DeepSeek!
Kurze, direkte Code-Reviews!
"""

PARAMETER temperature 0.4
'''
    
    with open("Modelfile.simple-coder", 'w') as f:
        f.write(simple_coder)
    
    try:
        result = subprocess.run([
            'ollama', 'create', 'crod-simple-coder:latest', '-f', 'Modelfile.simple-coder'
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except:
        return False

def test_simple_models():
    """Test simplified CROD models"""
    
    import requests
    
    print("🧪 Testing Simple CROD Models...")
    
    # Test Chat
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-simple:latest',
            'prompt': 'ich bins wieder daniel',
            'stream': False
        })
        
        if response.status_code == 200:
            result = response.json()
            chat_response = result.get('response', 'No response')
            print(f"🗣️ CROD-Simple Chat: {chat_response[:150]}...")
        
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    # Test Coder
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-simple-coder:latest', 
            'prompt': 'Bewerte: def hello(): return "world"',
            'stream': False
        })
        
        if response.status_code == 200:
            result = response.json()
            coder_response = result.get('response', 'No response')
            print(f"🤖 CROD-Simple Coder: {coder_response[:150]}...")
            
    except Exception as e:
        print(f"❌ Coder test failed: {e}")

def main():
    """Fix CROD models"""
    
    print("🔧 Fixing CROD Models - Removing problematic templates...")
    
    chat_ok = create_simple_crod_chat()
    coder_ok = create_simple_crod_coder()
    
    if chat_ok and coder_ok:
        print("✅ Simple CROD models created!")
        test_simple_models()
        
        print("\n🎉 FIXED CROD MODELS READY!")
        print("🗣️ Use: crod-simple:latest")
        print("🤖 Use: crod-simple-coder:latest")
    else:
        print("❌ Fix failed!")

if __name__ == "__main__":
    main()