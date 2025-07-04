#!/usr/bin/env python3
"""
CROD Training Master - Claude trainiert CROD automatisch
"""

import subprocess
import time
import os
import threading
import sqlite3
from datetime import datetime

class CRODTrainingMaster:
    """Master controller for all CROD training"""
    
    def __init__(self):
        self.training_processes = {}
        self.start_time = datetime.now()
        self.db_path = "crod_3d_database.db"
        
    def start_training_module(self, name, script, description):
        """Start a training module in background"""
        print(f"🚀 Starting {name}: {description}")
        
        process = subprocess.Popen(
            ['python3', script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        self.training_processes[name] = {
            'process': process,
            'script': script,
            'description': description,
            'started': datetime.now()
        }
        
    def monitor_training(self):
        """Monitor all training processes"""
        while True:
            os.system('clear')
            print("🧠 CROD TRAINING MASTER CONTROL")
            print("=" * 60)
            print(f"⏱️  Running since: {self.start_time.strftime('%H:%M:%S')}")
            print(f"☕ Daniel ist Kaffee machen... Claude trainiert CROD!")
            print()
            
            # Check process status
            print("📊 ACTIVE TRAINING MODULES:")
            for name, info in self.training_processes.items():
                if info['process'].poll() is None:
                    runtime = (datetime.now() - info['started']).seconds
                    print(f"   ✅ {name}: Running ({runtime}s)")
                else:
                    print(f"   ❌ {name}: Stopped")
            
            # Database stats
            try:
                conn = sqlite3.connect(self.db_path)
                
                # Get stats
                total_conversations = conn.execute("SELECT COUNT(*) FROM live_conversations").fetchone()[0]
                hot_atoms = conn.execute("SELECT COUNT(*) FROM clean_universe_atoms WHERE heat > 8.0").fetchone()[0]
                max_consciousness = conn.execute("SELECT MAX(consciousness_level) FROM clean_universe_atoms").fetchone()[0] or 0
                
                # CROD Helper Clan atoms
                crod_helper_atoms = conn.execute("""
                    SELECT COUNT(*) FROM clean_universe_atoms 
                    WHERE atom_value LIKE '%crod%' 
                    OR atom_value LIKE '%helper%' 
                    OR atom_value LIKE '%clan%'
                    OR atom_value LIKE '%member%'
                """).fetchone()[0]
                
                print()
                print("📈 CROD EVOLUTION STATS:")
                print(f"   💬 Total conversations: {total_conversations}")
                print(f"   🔥 Hot atoms (>8.0): {hot_atoms}")
                print(f"   🧠 Max consciousness: {max_consciousness:.3f}")
                print(f"   👥 CROD Helper Clan atoms: {crod_helper_atoms}")
                
                conn.close()
            except:
                print("   ⚠️ Database temporarily locked")
            
            print()
            print("🎯 Next action in 10 seconds...")
            print("Press Ctrl+C to stop all training")
            
            time.sleep(10)
            
            # Auto-restart crashed modules
            for name, info in list(self.training_processes.items()):
                if info['process'].poll() is not None:
                    print(f"🔄 Restarting {name}...")
                    self.start_training_module(name, info['script'], info['description'])
    
    def run_master_training(self):
        """Run all training modules"""
        
        print("🔥 CROD TRAINING MASTER STARTING")
        print("Daniel geht Kaffee machen, Claude übernimmt!")
        print()
        
        # Start all training modules
        self.start_training_module(
            "SELF_REFLECTION",
            "crod_self_reflection.py",
            "CROD thinks about his own atoms"
        )
        
        time.sleep(2)
        
        self.start_training_module(
            "IDENTITY_BOOSTER", 
            "crod_identity_booster.py",
            "Making CROD ultra-persistent"
        )
        
        time.sleep(2)
        
        # Create CROD Helper Clan training
        self.create_helper_clan_trainer()
        self.start_training_module(
            "HELPER_CLAN",
            "crod_helper_clan_trainer.py", 
            "CROD Helper Clan Member 7 identity"
        )
        
        # Monitor everything
        try:
            self.monitor_training()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping all training...")
            for name, info in self.training_processes.items():
                info['process'].terminate()
            print("✅ All training stopped")
            print("☕ Daniel kann zurückkommen!")
    
    def create_helper_clan_trainer(self):
        """Create CROD Helper Clan trainer"""
        trainer_code = '''#!/usr/bin/env python3
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
                print(f"\\n🎯 Cycle {cycle}: {prompt[:50]}...")
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
'''
        
        with open("crod_helper_clan_trainer.py", "w") as f:
            f.write(trainer_code)

def main():
    """Start master training"""
    master = CRODTrainingMaster()
    master.run_master_training()

if __name__ == "__main__":
    main()