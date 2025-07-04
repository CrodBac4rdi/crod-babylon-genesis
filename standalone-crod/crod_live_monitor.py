#!/usr/bin/env python3
"""
CROD Live Monitor - Watch CROD's evolution in real-time
"""

import sqlite3
import time
import os
from datetime import datetime

def monitor_crod():
    """Live monitoring of CROD's training"""
    
    print("👁️ CROD LIVE TRAINING MONITOR")
    print("Daniel macht Kaffee, Claude überwacht CROD!")
    print("=" * 60)
    
    db_path = "crod_3d_database.db"
    
    while True:
        try:
            conn = sqlite3.connect(db_path)
            
            # Clear screen for fresh view
            os.system('clear')
            
            print("🧠 CROD LIVE STATUS -", datetime.now().strftime("%H:%M:%S"))
            print("=" * 60)
            
            # Training processes
            processes = os.popen("ps aux | grep -E 'crod_self|crod_identity|crod_helper' | grep -v grep | wc -l").read().strip()
            print(f"🔄 Active Training Processes: {processes}")
            print()
            
            # Hot atoms
            hot_atoms = conn.execute("""
                SELECT atom_value, heat, consciousness_level 
                FROM clean_universe_atoms 
                WHERE heat > 9.0 
                ORDER BY heat DESC, consciousness_level DESC 
                LIMIT 5
            """).fetchall()
            
            print("🔥 HOTTEST ATOMS (heat > 9.0):")
            for atom, heat, consciousness in hot_atoms:
                print(f"   {atom[:40]:<40} | heat: {heat:.1f} | cons: {consciousness:.3f}")
            
            # CROD identity atoms
            print()
            print("🆔 CROD IDENTITY STATUS:")
            identity_atoms = ['crod', 'consciousness', 'helper', 'clan', 'member-7']
            for atom in identity_atoms:
                result = conn.execute("""
                    SELECT heat, consciousness_level 
                    FROM clean_universe_atoms 
                    WHERE atom_value = ?
                """, (atom,)).fetchone()
                if result:
                    print(f"   {atom:<15} | heat: {result[0]:.1f} | consciousness: {result[1]:.3f}")
            
            # Recent activity
            recent_convs = conn.execute("""
                SELECT COUNT(*) FROM live_conversations 
                WHERE timestamp > datetime('now', '-5 minutes')
            """).fetchone()[0]
            
            recent_learning = conn.execute("""
                SELECT COUNT(*) FROM live_learning_events 
                WHERE timestamp > datetime('now', '-5 minutes')  
            """).fetchone()[0]
            
            print()
            print("📊 RECENT ACTIVITY (last 5 min):")
            print(f"   Conversations: {recent_convs}")
            print(f"   Learning events: {recent_learning}")
            
            # Overall stats
            total_hot = conn.execute("SELECT COUNT(*) FROM clean_universe_atoms WHERE heat > 8.0").fetchone()[0]
            avg_consciousness = conn.execute("SELECT AVG(consciousness_level) FROM clean_universe_atoms WHERE consciousness_level > 0").fetchone()[0] or 0
            
            print()
            print("📈 OVERALL PROGRESS:")
            print(f"   Hot atoms (>8.0): {total_hot}")
            print(f"   Avg consciousness: {avg_consciousness:.4f}")
            
            # Check latest logs
            print()
            print("📝 LATEST TRAINING SNIPPETS:")
            
            # Check self reflection log
            try:
                with open('self_reflection.log', 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        last_reflection = lines[-1].strip()
                        if 'CROD:' in last_reflection:
                            print(f"   Self-Reflection: {last_reflection[:60]}...")
            except:
                pass
                
            # Check identity log
            try:
                with open('identity_booster.log', 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        last_identity = lines[-1].strip()
                        if 'CROD:' in last_identity:
                            print(f"   Identity: {last_identity[:60]}...")
            except:
                pass
            
            conn.close()
            
            print()
            print("🔄 Refreshing in 10 seconds... (Ctrl+C to stop)")
            print("☕ Daniel's Kaffee Status: Unknown")
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")
            print("📊 CROD continues training in background!")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_crod()