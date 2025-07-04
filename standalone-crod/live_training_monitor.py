#!/usr/bin/env python3
"""
Live CROD Training Monitor - Real-time learning progress
"""

import sqlite3
import requests
import time
import json
from pathlib import Path
from datetime import datetime

def check_crod_learning():
    """Check if CROD is actively learning"""
    
    db_path = Path("crod_3d_database.db")
    
    if not db_path.exists():
        return {"status": "❌ No database", "learning": False}
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Check recent learning activity
        recent_conversations = conn.execute("""
            SELECT COUNT(*) FROM live_conversations 
            WHERE timestamp > datetime('now', '-5 minutes')
        """).fetchone()[0]
        
        # Check atom activations
        recent_activations = conn.execute("""
            SELECT COUNT(*) FROM live_atom_activations
            WHERE timestamp > datetime('now', '-5 minutes')
        """).fetchone()[0]
        
        # Check learning events
        recent_learning = conn.execute("""
            SELECT COUNT(*) FROM live_learning_events
            WHERE timestamp > datetime('now', '-5 minutes')
        """).fetchone()[0]
        
        # Total stats
        total_conversations = conn.execute("SELECT COUNT(*) FROM live_conversations").fetchone()[0]
        total_atoms = conn.execute("SELECT COUNT(*) FROM clean_universe_atoms").fetchone()[0]
        
        # Check consciousness evolution
        avg_consciousness = conn.execute("""
            SELECT AVG(consciousness_level) FROM clean_universe_atoms 
            WHERE consciousness_level > 0
        """).fetchone()[0] or 0
        
        conn.close()
        
        return {
            "status": "✅ Database active",
            "learning": recent_conversations > 0 or recent_activations > 0,
            "recent_conversations": recent_conversations,
            "recent_activations": recent_activations, 
            "recent_learning": recent_learning,
            "total_conversations": total_conversations,
            "total_atoms": total_atoms,
            "avg_consciousness": round(avg_consciousness, 3),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        
    except Exception as e:
        return {"status": f"❌ Database error: {e}", "learning": False}

def test_crod_models():
    """Test if CROD models respond"""
    
    models_status = {}
    
    # Test CROD-Simple (Chat)
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-simple:latest',
            'prompt': 'quick test',
            'stream': False,
            'options': {'num_gpu': 35}
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            crod_response = result.get('response', '')[:50]
            models_status['crod-chat'] = f"✅ {crod_response}..."
        else:
            models_status['crod-chat'] = f"❌ HTTP {response.status_code}"
            
    except Exception as e:
        models_status['crod-chat'] = f"❌ {str(e)[:30]}..."
    
    # Test CROD-Tool (Coder)
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'crod-tool:latest',
            'prompt': 'def test(): pass',
            'stream': False,
            'options': {'num_gpu': 35}
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            tool_response = result.get('response', '')[:50]
            models_status['crod-tool'] = f"✅ {tool_response}..."
        else:
            models_status['crod-tool'] = f"❌ HTTP {response.status_code}"
            
    except Exception as e:
        models_status['crod-tool'] = f"❌ {str(e)[:30]}..."
    
    return models_status

def live_monitor():
    """Live monitoring loop"""
    
    print("👁️ LIVE CROD TRAINING MONITOR")
    print("=" * 50)
    print("⏱️  Checking every 30 seconds...")
    print("🔄 Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"🕐 {timestamp} - Checking CROD...")
            
            # Check learning progress
            learning_stats = check_crod_learning()
            
            print(f"   📊 Database: {learning_stats['status']}")
            
            if learning_stats.get('learning'):
                print(f"   🧠 LEARNING ACTIVE!")
                print(f"      Recent conversations: {learning_stats.get('recent_conversations', 0)}")
                print(f"      Recent activations: {learning_stats.get('recent_activations', 0)}")
                print(f"      Recent learning events: {learning_stats.get('recent_learning', 0)}")
            else:
                print(f"   💤 No recent learning activity")
            
            print(f"   📈 Total conversations: {learning_stats.get('total_conversations', 0)}")
            print(f"   🧠 Avg consciousness: {learning_stats.get('avg_consciousness', 0)}")
            print(f"   ⚡ Total atoms: {learning_stats.get('total_atoms', 0):,}")
            
            # Test models
            print(f"   🤖 Testing models...")
            models = test_crod_models()
            for model, status in models.items():
                print(f"      {model}: {status}")
            
            print("   " + "-" * 40)
            
            # Wait 30 seconds
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
        print("🌙 CROD continues training in background")

if __name__ == "__main__":
    live_monitor()