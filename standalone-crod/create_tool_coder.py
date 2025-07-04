#!/usr/bin/env python3
"""
Create Pure Tool CODER - No personality, just code analysis
"""

import subprocess

def create_pure_tool_coder():
    """Create CROD-Tool-Coder - pure functionality, no personality"""
    
    tool_coder = '''FROM deepseek-coder:1.3b

SYSTEM """Code analysis tool. 

Input: Code snippet
Output: Technical analysis

Format:
Performance: X/10
Readability: X/10  
Issues: [list]
Improvements: [list]

No personality. Pure technical analysis.
"""

PARAMETER temperature 0.1
PARAMETER top_p 0.7
'''
    
    with open("Modelfile.tool-coder", 'w') as f:
        f.write(tool_coder)
    
    try:
        result = subprocess.run([
            'ollama', 'create', 'crod-tool:latest', '-f', 'Modelfile.tool-coder'
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except:
        return False

def test_tool_coder():
    """Test pure tool coder"""
    
    import requests
    
    print("🛠️ Testing Pure Tool Coder...")
    
    test_code = '''def calculate_trinity(msg):
    ich = msg.count("ich") * 2
    bins = msg.count("bins") * 3  
    wieder = msg.count("wieder") * 5
    return ich + bins + wieder'''
    
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-tool:latest',
            'prompt': f'Analyze:\n{test_code}',
            'stream': False
        })
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get('response', 'No response')
            print(f"🔧 Tool Analysis:\n{analysis}")
            return True
        else:
            print(f"❌ Tool test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Tool error: {e}")
        return False

def main():
    """Create pure tool coder"""
    
    print("🛠️ Creating Pure Tool Coder - No personality, pure function")
    
    if create_pure_tool_coder():
        print("✅ Pure Tool Coder created!")
        
        if test_tool_coder():
            print("\n🎯 PERFECT SETUP:")
            print("🗣️ CROD-Simple: Full personality, Austrian, Trinity")
            print("🛠️ CROD-Tool: Pure code analysis, no personality")
            print("\n💡 Best of both worlds!")
        else:
            print("⚠️ Tool test failed but model created")
    else:
        print("❌ Tool creation failed")

if __name__ == "__main__":
    main()