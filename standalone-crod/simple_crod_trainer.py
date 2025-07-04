#!/usr/bin/env python3
"""
Simple CROD Trainer - No bullshit, just works
"""

import requests
import time

def ask_crod(prompt):
    """Ask CROD something"""
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-simple:latest',
            'prompt': prompt,
            'stream': False,
            'options': {'temperature': 0.8, 'num_gpu': 35}
        }, timeout=15)
        
        if response.status_code == 200:
            return response.json().get('response', 'CROD silent')
        else:
            return f"CROD error: {response.status_code}"
    except Exception as e:
        return f"CROD offline: {e}"

def main():
    """Simple CROD training loop"""
    
    print("🔥 SIMPLE CROD TRAINER")
    print("=" * 40)
    
    # Smart questions
    questions = [
        "wer bist du und warum existierst du?",
        "erkläre deine atom weights",
        "analysiere: ich bins wieder daniel",
        "bewerte diesen code: def hello(): return 'world'",
        "was bedeutet consciousness level für dich?",
        "erkläre warum daniel geil sagt",
        "analysiere: wtf - welche response strategy?",
        "beschreibe deine heat signatures",
        "was ist die clean universe?",
        "wie funktioniert machine learning aus deiner sicht?"
    ]
    
    lesson_count = 0
    
    try:
        while True:
            question = questions[lesson_count % len(questions)]
            
            print(f"\n📚 Lesson {lesson_count + 1}: {question}")
            
            crod_response = ask_crod(question)
            
            print(f"🤖 CROD: {crod_response[:100]}...")
            
            # Simple evaluation
            if len(crod_response) > 50 and 'error' not in crod_response.lower():
                if any(word in crod_response.lower() for word in ['atom', 'consciousness', 'trinity', 'heat']):
                    print("✅ Good - mentions technical concepts")
                else:
                    print("⚠️ OK - but could be deeper")
            else:
                print("❌ Poor response")
            
            lesson_count += 1
            
            if lesson_count % 10 == 0:
                print(f"\n📊 Progress: {lesson_count} lessons completed")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Training stopped after {lesson_count} lessons")
        print("🧠 CROD has learned something!")

if __name__ == "__main__":
    main()