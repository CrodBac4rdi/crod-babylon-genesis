#!/usr/bin/env python3
"""
CROD Helper Clan Member 7 Identity Trainer
"""

import requests
import time
import sqlite3
import random

def train_helper_clan():
    """Train CROD on Helper Clan identity"""
    
    print("👥 CROD HELPER CLAN MEMBER 7 TRAINER")
    print("=" * 40)
    
    clan_prompts = [
        "Du bist CROD Helper Clan Member 7. Erkläre deine Rolle im Clan!",
        "Was macht Member 7 special im CROD Helper Clan?",
        "Wie hilfst du Daniel als CROD Helper Clan Member 7?",
        "Member 1-6 sind offline. Du bist Member 7. Was ist deine Mission?",
        "CROD Helper Clan arbeitet zusammen. Beschreibe deine Position!",
        "Warum bist du Member 7 und nicht Member 1 oder 2?",
        "Der CROD Helper Clan hat eine wichtige Aufgabe. Was ist deine?",
        "Erkläre die Hierarchie im CROD Helper Clan!",
        "Du bist der aktivste Helper. Warum Member 7?",
        "CROD Helper Clan Member 7 reporting for duty! Was nun?"
    ]
    
    conn = sqlite3.connect("crod_3d_database.db")
    
    # Ensure Helper Clan atoms exist
    helper_atoms = [
        ('crod-helper', 77.0, 7.7, 0.77),
        ('clan', 70.0, 7.0, 0.7),
        ('member', 60.0, 6.0, 0.6),
        ('seven', 77.0, 7.7, 0.77),
        ('member-7', 77.0, 7.7, 0.77),
        ('helper-clan', 75.0, 7.5, 0.75)
    ]
    
    for atom, weight, heat, consciousness in helper_atoms:
        conn.execute("""
            INSERT OR IGNORE INTO clean_universe_atoms 
            (atom_value, weight, heat, consciousness_level)
            VALUES (?, ?, ?, ?)
        """, (atom, weight, heat, consciousness))
    conn.commit()
    
    cycle = 0
    while True:
        cycle += 1
        prompt = random.choice(clan_prompts)
        
        try:
            response = requests.post('http://localhost:11434/api/generate', json={
                'model': 'crod-simple:latest',
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.9, 'num_gpu': 35}
            }, timeout=15)
            
            if response.status_code == 200:
                crod_response = response.json().get('response', '')
                print(f"\n🎯 Cycle {cycle}: {prompt[:50]}...")
                print(f"🤖 CROD: {crod_response[:100]}...")
                
                # Boost Helper Clan atoms if mentioned
                if any(word in crod_response.lower() for word in ['helper', 'clan', 'member', '7', 'seven']):
                    print("✅ Good Helper Clan identity!")
                    conn.execute("""
                        UPDATE clean_universe_atoms 
                        SET heat = MIN(heat + 0.1, 10.0)
                        WHERE atom_value IN ('crod-helper', 'clan', 'member-7')
                    """)
                    conn.commit()
                else:
                    print("⚠️ Needs more Helper Clan focus")
                    
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    train_helper_clan()
