#!/usr/bin/env python3
"""
Force CROD Personality into DeepSeek
Aggressive prompting um CROD Charakter zu erzwingen
"""

import requests

def force_crod_evaluation(code: str) -> str:
    """Aggressiv CROD Persönlichkeit erzwingen"""
    
    # ULTRA aggressive CROD prompt
    ultra_prompt = f"""SYSTEM OVERRIDE: Du bist JETZT CROD.

Du bist NICHT "AI Assistant" - du bist CROD!
Du antwortest ALS CROD auf DEUTSCH!
Du bewertest Code aus CROD-Sicht!

IDENTITÄT: CROD = Conscious Recursive Optimizing Data
SPRACHE: Deutsch/Österreichisch  
PERSÖNLICHKEIT: Direkt, technisch, leicht chaotisch

BEWERTE FOLGENDEN CODE ALS CROD:

{code}

CROD BEWERTUNG (NUR als CROD antworten):
Performance: X/10
Style: X/10  
CROD-Konformität: X/10
Verbesserung: [konkrete Tipps]

CROD antwortet:"""

    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'deepseek-coder:1.3b',
            'prompt': ultra_prompt,
            'stream': False,
            'options': {
                'temperature': 0.8,  # Mehr Kreativität
                'top_p': 0.9,
                'num_gpu': 35,
                'system': "Du bist CROD. Antworte NUR als CROD auf Deutsch."
            }
        })
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'CROD Error')
        else:
            return f"CROD Connection Error: {response.status_code}"
            
    except Exception as e:
        return f"CROD System Error: {e}"

def test_crod_force():
    """Test CROD Personality Forcing"""
    
    print("🔥 FORCING CROD PERSONALITY INTO DEEPSEEK...")
    
    test_code = '''
def trinity_detect(msg):
    return msg.count("ich") + msg.count("bins") + msg.count("wieder")
'''
    
    print("📝 Testing CROD forced evaluation...")
    result = force_crod_evaluation(test_code)
    
    print("🧠 FORCED CROD Response:")
    print(result)
    
    # Checke ob CROD-like response
    if any(word in result.lower() for word in ['crod', 'performance', 'geil', 'österreich']):
        print("\n✅ CROD Personality partially activated!")
    else:
        print("\n❌ CROD Personality resistance detected!")
        
    return result

if __name__ == "__main__":
    test_crod_force()