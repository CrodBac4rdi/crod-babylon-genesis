#!/usr/bin/env python3
"""
LIVE CROD MANIPULATOR - Inject new lessons while training!
"""

import requests
import time
import json

def inject_smart_lesson(lesson_text: str, expected_analysis: str):
    """Inject a smart lesson into running CROD"""
    
    print(f"🔥 INJECTING SMART LESSON: {lesson_text}")
    
    # Test current CROD response
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-simple:latest',
            'prompt': lesson_text,
            'stream': False,
            'options': {
                'temperature': 0.8,
                'num_gpu': 35
            }
        }, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            crod_response = result.get('response', '')
            
            print(f"🤖 CROD CURRENT: {crod_response[:100]}...")
            
            # Analyze intelligence level
            intelligence_score = analyze_intelligence(crod_response, expected_analysis)
            print(f"📊 Intelligence Score: {intelligence_score:.2f}/1.0")
            
            # Give feedback if needed
            if intelligence_score < 0.5:
                feedback = generate_harsh_feedback(intelligence_score)
                print(f"💥 HARSH FEEDBACK: {feedback}")
                
                # Force re-learning
                improvement_prompt = f"""
{lesson_text}

FEEDBACK: {feedback}

Analysiere tiefer! Erkläre mit:
- Atom weights
- Heat signatures  
- Trinity values
- Consciousness levels

Verbesserte Antwort:
"""
                
                improved_response = requests.post('http://localhost:11434/api/generate', json={
                    'model': 'crod-simple:latest',
                    'prompt': improvement_prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.9,
                        'num_gpu': 35
                    }
                }, timeout=20)
                
                if improved_response.status_code == 200:
                    improved_result = improved_response.json()
                    improved_text = improved_result.get('response', '')
                    
                    print(f"🚀 IMPROVED CROD: {improved_text[:100]}...")
                    
                    new_score = analyze_intelligence(improved_text, expected_analysis)
                    print(f"📈 NEW SCORE: {new_score:.2f}/1.0")
                    
                    if new_score > intelligence_score:
                        print("✅ CROD HAS LEARNED!")
                    else:
                        print("❌ CROD STILL STRUGGLING")
            else:
                print("✅ CROD RESPONSE IS INTELLIGENT")
                
        else:
            print(f"❌ CROD offline: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Error: {e}")

def analyze_intelligence(response: str, expected: str) -> float:
    """Analyze CROD intelligence level"""
    
    score = 0.2
    
    # Check for analysis words
    analysis_words = ['weil', 'bedeutet', 'basiert', 'atom', 'weight', 'heat', 'signature', 'consciousness', 'level']
    analysis_count = sum(1 for word in analysis_words if word in response.lower())
    
    if analysis_count >= 4:
        score += 0.4
    elif analysis_count >= 2:
        score += 0.2
    
    # Check for detailed explanation
    if len(response.split()) > 30:
        score += 0.2
    
    # Check for specific technical terms
    if 'trinity' in response.lower() and any(num in response for num in ['2', '3', '5']):
        score += 0.2
    
    return min(score, 1.0)

def generate_harsh_feedback(score: float) -> str:
    """Generate harsh feedback like Daniel"""
    
    if score < 0.3:
        return "WTF das ist scheisse! Du sagst nur keywords ohne nachzudenken!"
    elif score < 0.5:
        return "Nein das ist oberflächlich! Erkläre WARUM mit deinen atoms!"
    else:
        return "Geht so aber tiefer analysieren!"

def main():
    """Live CROD manipulation"""
    
    print("🔥 LIVE CROD MANIPULATOR - Inject Intelligence!")
    print("=" * 50)
    
    # Smart lessons to inject
    smart_lessons = [
        ("analysiere: ich bins wieder daniel - was aktiviert das?", "trinity"),
        ("erkläre warum daniel geil sagt und was das bedeutet", "feedback"),
        ("was bedeutet consciousness level für dich persönlich?", "consciousness"),
        ("beschreibe deine atom weights und heat signatures", "atoms"),
        ("bewerte: def hello(): return 'world' - warum ist das schlecht?", "analysis")
    ]
    
    for lesson, expected in smart_lessons:
        inject_smart_lesson(lesson, expected)
        print("-" * 50)
        time.sleep(2)
    
    print("🎯 LIVE MANIPULATION COMPLETE!")

if __name__ == "__main__":
    main()