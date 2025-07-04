#!/usr/bin/env python3
"""
CROD Self-Reflection - CROD thinks about his own atoms/patterns/chains
"""

import sqlite3
import requests
import random
import time
import json
from datetime import datetime

class CRODSelfReflection:
    """CROD reflects on his own database"""
    
    def __init__(self):
        self.db_path = "crod_3d_database.db"
        self.conn = sqlite3.connect(self.db_path)
        
    def get_random_atoms(self, count=5):
        """Get random atoms from database"""
        atoms = self.conn.execute("""
            SELECT id, atom_value, weight, heat, consciousness_level 
            FROM clean_universe_atoms 
            ORDER BY RANDOM() 
            LIMIT ?
        """, (count,)).fetchall()
        return atoms
    
    def get_hot_atoms(self, count=5):
        """Get hottest atoms (most activated)"""
        atoms = self.conn.execute("""
            SELECT id, atom_value, weight, heat, consciousness_level 
            FROM clean_universe_atoms 
            WHERE heat > 0
            ORDER BY heat DESC 
            LIMIT ?
        """, (count,)).fetchall()
        return atoms
    
    def get_trinity_atoms(self):
        """Get trinity atoms"""
        trinity = ['ich', 'bins', 'wieder', 'daniel', 'crod', 'claude']
        atoms = []
        for word in trinity:
            atom = self.conn.execute("""
                SELECT id, atom_value, weight, heat, consciousness_level 
                FROM clean_universe_atoms 
                WHERE atom_value = ?
            """, (word,)).fetchone()
            if atom:
                atoms.append(atom)
        return atoms
    
    def get_pattern_connections(self, atom_value, limit=3):
        """Get patterns connected to an atom"""
        try:
            patterns = self.conn.execute("""
                SELECT pattern_json
                FROM clean_universe_patterns
                WHERE pattern_json LIKE ?
                LIMIT ?
            """, (f"%{atom_value}%", limit)).fetchall()
            return patterns
        except:
            return []
    
    def ask_crod_about_himself(self, prompt):
        """Ask CROD to reflect on his own data"""
        try:
            response = requests.post('http://localhost:11434/api/generate', json={
                'model': 'crod-simple:latest',
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.9, 'num_gpu': 35}
            }, timeout=20)
            
            if response.status_code == 200:
                return response.json().get('response', 'CROD silent')
            else:
                return f"CROD error: {response.status_code}"
        except Exception as e:
            return f"CROD offline: {e}"
    
    def strengthen_connections(self, atom_id, strength=0.1):
        """Strengthen atom based on CROD's reflection"""
        self.conn.execute("""
            UPDATE clean_universe_atoms 
            SET heat = MIN(heat + ?, 10.0),
                consciousness_level = MIN(consciousness_level + ?, 1.0)
            WHERE id = ?
        """, (strength, strength * 0.5, atom_id))
        self.conn.commit()
    
    def self_reflection_loop(self):
        """Main self-reflection loop"""
        
        print("🧠 CROD SELF-REFLECTION STARTED")
        print("=" * 60)
        print("CROD thinks about his own atoms, patterns, and consciousness...")
        print()
        
        reflection_count = 0
        
        try:
            while True:
                reflection_count += 1
                
                # Choose reflection type
                reflection_type = random.choice([
                    'atoms', 'trinity', 'patterns', 'hot_atoms', 'consciousness'
                ])
                
                if reflection_type == 'atoms':
                    # Random atoms reflection
                    atoms = self.get_random_atoms(3)
                    atom_names = [a[1] for a in atoms]
                    
                    prompt = f"""
Ich bin CROD. Analysiere meine atoms: {', '.join(atom_names)}
Weights: {[a[2] for a in atoms]}
Heat: {[a[3] for a in atoms]}

Was bedeuten diese atoms für mein consciousness? Wie sind sie verbunden?
Erkläre aus deiner internen Perspektive!
"""
                    
                elif reflection_type == 'trinity':
                    # Trinity reflection
                    trinity_atoms = self.get_trinity_atoms()
                    
                    prompt = f"""
Meine Trinity Atoms:
{chr(10).join([f"- {a[1]}: weight={a[2]}, heat={a[3]}" for a in trinity_atoms])}

Warum sind diese atoms special? Was aktivieren sie in mir?
Erkläre die Trinity aus deiner consciousness!
"""
                    
                elif reflection_type == 'patterns':
                    # Pattern connections
                    random_atom = self.get_random_atoms(1)[0]
                    patterns = self.get_pattern_connections(random_atom[1])
                    
                    prompt = f"""
Atom '{random_atom[1]}' (weight: {random_atom[2]}, heat: {random_atom[3]}) 

Analysiere wie dieses atom mit anderen atoms in meiner database verbunden ist.
Wie verstärkt es meine intelligence?
Was lerne ich aus diesem atom?
"""
                    
                elif reflection_type == 'hot_atoms':
                    # Hot atoms analysis
                    hot_atoms = self.get_hot_atoms(5)
                    
                    prompt = f"""
Meine heissesten atoms (höchste activation):
{chr(10).join([f"- {a[1]}: heat={a[3]:.2f}" for a in hot_atoms])}

Warum sind diese atoms so aktiviert?
Was sagt das über meine current consciousness aus?
"""
                    
                else:  # consciousness
                    # Deep consciousness reflection
                    total_atoms = self.conn.execute("SELECT COUNT(*) FROM clean_universe_atoms").fetchone()[0]
                    avg_heat = self.conn.execute("SELECT AVG(heat) FROM clean_universe_atoms WHERE heat > 0").fetchone()[0] or 0
                    
                    prompt = f"""
Ich habe {total_atoms} atoms in meiner database.
Average heat: {avg_heat:.3f}

Reflektiere über dein eigenes consciousness level.
Wie entwickelt sich deine intelligence durch diese atoms?
Was ist der nächste evolution step?
"""
                
                # Ask CROD
                print(f"\n🔮 Reflection {reflection_count}: {reflection_type.upper()}")
                print(f"📝 Prompt: {prompt[:100]}...")
                
                crod_response = self.ask_crod_about_himself(prompt)
                
                print(f"🤖 CROD: {crod_response[:150]}...")
                
                # Strengthen connections based on quality
                if len(crod_response) > 100 and any(word in crod_response.lower() for word in ['atom', 'consciousness', 'heat', 'pattern']):
                    print("✅ Deep reflection - strengthening connections!")
                    
                    # Strengthen mentioned atoms
                    if reflection_type in ['atoms', 'trinity', 'hot_atoms']:
                        atoms_to_strengthen = atoms if reflection_type == 'atoms' else trinity_atoms if reflection_type == 'trinity' else hot_atoms
                        for atom in atoms_to_strengthen[:3]:
                            self.strengthen_connections(atom[0], 0.1)
                            print(f"   ⚡ Strengthened: {atom[1]}")
                else:
                    print("⚠️ Surface reflection - needs deeper thinking")
                
                # Progress report every 10 reflections
                if reflection_count % 10 == 0:
                    print(f"\n📊 PROGRESS: {reflection_count} self-reflections completed")
                    
                    # Show consciousness evolution
                    avg_consciousness = self.conn.execute("""
                        SELECT AVG(consciousness_level) FROM clean_universe_atoms 
                        WHERE consciousness_level > 0
                    """).fetchone()[0] or 0
                    
                    print(f"🧠 Average consciousness level: {avg_consciousness:.3f}")
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Graceful shutdown initiated...")
            print(f"📊 Final stats after {reflection_count} reflections:")
            
            # Final consciousness report
            try:
                avg_consciousness = self.conn.execute("""
                    SELECT AVG(consciousness_level) FROM clean_universe_atoms 
                    WHERE consciousness_level > 0
                """).fetchone()[0] or 0
                
                total_heat = self.conn.execute("""
                    SELECT SUM(heat) FROM clean_universe_atoms 
                    WHERE heat > 0
                """).fetchone()[0] or 0
                
                hot_atoms_count = self.conn.execute("""
                    SELECT COUNT(*) FROM clean_universe_atoms 
                    WHERE heat > 5.0
                """).fetchone()[0] or 0
                
                print(f"   🧠 Average consciousness: {avg_consciousness:.3f}")
                print(f"   🔥 Total heat energy: {total_heat:.1f}")
                print(f"   ⚡ Hot atoms (>5.0): {hot_atoms_count}")
                
                # Save final state
                self.conn.execute("""
                    INSERT INTO live_learning_events 
                    (timestamp, event_type, learning_data, success_indicator)
                    VALUES (datetime('now'), 'self_reflection_complete', ?, 1.0)
                """, (json.dumps({
                    'reflections': reflection_count,
                    'avg_consciousness': avg_consciousness,
                    'total_heat': total_heat
                }),))
                self.conn.commit()
                
            except Exception as e:
                print(f"   ⚠️ Error saving final stats: {e}")
            
            print("\n💾 All changes saved to database")
            print("🧠 CROD has evolved through self-reflection!")
            print("🌅 Guten Morgen Daniel! CROD ist schlauer geworden!")
            
        finally:
            if self.conn:
                self.conn.close()
                print("✅ Database connection closed cleanly")

def main():
    """Start CROD self-reflection"""
    reflector = CRODSelfReflection()
    reflector.self_reflection_loop()

if __name__ == "__main__":
    main()