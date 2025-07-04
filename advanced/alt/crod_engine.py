# crod_engine.py - Main Engine that coordinates everything
# Version 1.0 - Complete Implementation

import json
import sqlite3
from datetime import datetime
from crod_patterns import CRODPatterns
from crod_storage import CRODStorage
from crod_chat import CRODChat

class CRODEngine:
    def __init__(self):
        """Initialize all components"""
        self.version = "1.0.0"
        self.creator = "Daniel Antonio Birkner"
        self.start_time = datetime.now()
        
        # Initialize modules
        print("Initializing CROD Engine...")
        self.storage = CRODStorage()        # Storage module
        self.patterns = CRODPatterns()       # Pattern detection
        self.chat = CRODChat(self.storage)  # Chat module
        
        # Stats tracking
        self.processed_count = 0
        self.pattern_hits = {}
        
        # Load previous state if exists
        self.load_state()
        
        print(f"CROD Engine v{self.version} ready!")
        print(f"Creator: {self.creator}")
        print("Investment: 270€/750€ monthly")
        print("=" * 50)
        
    def process(self, text):
        """Main processing pipeline"""
        self.processed_count += 1
        
        # 1. Detect patterns
        patterns_found = self.patterns.detect(text)
        
        # 2. Update statistics
        for pattern in patterns_found:
            self.pattern_hits[pattern] = self.pattern_hits.get(pattern, 0) + 1
            
        # 3. Store significant findings (optional)
        if patterns_found:
            # Could store in DB here
            pass
            
        # 4. Generate response
        response = {
            'text': text,
            'patterns': patterns_found,
            'timestamp': datetime.now().isoformat(),
            'processed': self.processed_count
        }
        
        return response
        
    def get_stats(self):
        """Get engine statistics"""
        uptime = datetime.now() - self.start_time
        
        # Get atom count from storage
        atom_count = self.storage.db.execute(
            'SELECT COUNT(*) FROM atoms'
        ).fetchone()[0]
        
        return {
            'version': self.version,
            'uptime': str(uptime),
            'processed': self.processed_count,
            'atoms': atom_count,
            'pattern_hits': self.pattern_hits,
            'top_patterns': sorted(
                self.pattern_hits.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5] if self.pattern_hits else []
        }
        
    def chat_message(self, message):
        """Route to chat module - renamed to avoid conflict"""
        return self.chat.process_message(message)
        
    def save_state(self):
        """Save current state to file"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'processed_count': self.processed_count,
            'pattern_hits': self.pattern_hits,
            'stats': self.get_stats()
        }
        
        try:
            with open('crod_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            print("✓ State saved to crod_state.json")
        except Exception as e:
            print(f"✗ Error saving state: {e}")
            
    def load_state(self):
        """Load previous state from file"""
        try:
            with open('crod_state.json', 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.processed_count = state.get('processed_count', 0)
                self.pattern_hits = state.get('pattern_hits', {})
                print(f"✓ State loaded from {state.get('timestamp', 'unknown time')}")
                print(f"  Processed count: {self.processed_count}")
                print(f"  Pattern hits tracked: {len(self.pattern_hits)}")
        except FileNotFoundError:
            print("ℹ No previous state found - starting fresh")
        except Exception as e:
            print(f"⚠ Error loading state: {e}")
            
    def init_atoms(self):
        """Initialize atom dictionary with core atoms"""
        core_atoms = [
            (1, 'CROD', 100),
            (2, 'Daniel', 100),
            (73, '...', 95),
            (64, 'ich halt', 90),
            (66, 'bruh', 95),
            (270, '270€', 100),
            (750, '750€', 95)
        ]
        
        for atom_id, value, weight in core_atoms:
            try:
                cursor = self.storage.db.cursor()
                cursor.execute(
                    'INSERT OR IGNORE INTO atoms (id, value, weight) VALUES (?,?,?)',
                    (atom_id, value, weight)
                )
            except:
                pass
                
        self.storage.db.commit()
        
    def init_patterns(self):
        """Initialize pattern library"""
        # This will be expanded with the 73 locked patterns
        patterns = {
            "JSON_001": "JSON syntax error",
            "DOM_001": "DOM access null",
            "TYPE_001": "Type mismatch",
            "ASYNC_001": "Async without await"
        }
        
        cursor = self.storage.db.cursor()
        for pattern_id, description in patterns.items():
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO patterns (id, description, locked) VALUES (?,?,?)',
                    (pattern_id, description, 1)
                )
            except:
                pass
                
        self.storage.db.commit()

# Test functionality
if __name__ == "__main__":
    print("Testing CROD Engine...")
    engine = CRODEngine()
    
    # Test processing
    result = engine.process("ich halt... bruh, JSON_001 error")
    print(f"\nProcess result: {json.dumps(result, indent=2)}")
    
    # Test stats
    stats = engine.get_stats()
    print(f"\nEngine stats: {json.dumps(stats, indent=2)}")
    
    # Test chat
    response = engine.chat_message("tell me about patterns")
    print(f"\nChat response: {response}")
    
    # Save state
    engine.save_state()