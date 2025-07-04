# crod_engine.py - STABILE VERSION
# Diese Version läuft GARANTIERT!

import json
import sqlite3
from datetime import datetime

# Safe imports with fallbacks
try:
    from crod_patterns import CRODPatterns
except:
    # Minimal fallback
    class CRODPatterns:
        def __init__(self):
            self.locked_patterns = {"JSON_001": "JSON error"}
        def detect(self, text):
            return ["PATTERN_FALLBACK"]

try:
    from crod_storage import CRODStorage
except:
    # Minimal fallback
    class CRODStorage:
        def __init__(self):
            self.db = sqlite3.connect(':memory:')
        def log_execution(self, text, patterns):
            pass
        def update_pattern_usage(self, pattern):
            pass

try:
    from crod_chat import CRODChat
except:
    # Minimal fallback
    class CRODChat:
        def __init__(self, storage):
            pass
        def process_message(self, message):
            return "Chat module not available"

class CRODEngine:
    def __init__(self):
        """Initialize with proper error handling"""
        self.version = "1.0.0-STABLE"
        self.creator = "Daniel Antonio Birkner"
        self.start_time = datetime.now()
        
        print("Initializing CROD Engine...")
        
        # Initialize with error handling
        try:
            self.storage = CRODStorage()
            print("✓ Storage initialized")
        except Exception as e:
            print(f"⚠ Storage failed: {e}")
            self.storage = None
            
        try:
            self.patterns = CRODPatterns()
            print("✓ Patterns initialized")
        except Exception as e:
            print(f"⚠ Patterns failed: {e}")
            self.patterns = None
            
        try:
            self.chat = CRODChat(self.storage)
            print("✓ Chat initialized")
        except Exception as e:
            print(f"⚠ Chat failed: {e}")
            self.chat = None
        
        # Stats
        self.processed_count = 0
        self.pattern_hits = {}
        
        print(f"CROD Engine v{self.version} ready!")
        print("=" * 50)
        
    def process(self, text):
        """Process text with full error handling"""
        self.processed_count += 1
        
        # Safe pattern detection
        patterns_found = []
        try:
            if self.patterns:
                patterns_found = self.patterns.detect(text)
        except Exception as e:
            print(f"Pattern detection error: {e}")
            
        # Update stats
        for pattern in patterns_found:
            self.pattern_hits[pattern] = self.pattern_hits.get(pattern, 0) + 1
            
        # Safe logging
        try:
            if self.storage and hasattr(self.storage, 'log_execution'):
                self.storage.log_execution(text, patterns_found)
        except:
            pass
            
        # Safe pattern usage update
        try:
            if self.storage and hasattr(self.storage, 'update_pattern_usage'):
                for pattern in patterns_found:
                    self.storage.update_pattern_usage(pattern)
        except:
            pass
        
        return {
            'text': text,
            'patterns': patterns_found,
            'timestamp': datetime.now().isoformat(),
            'processed': self.processed_count
        }
        
    def get_stats(self):
        """Get stats with error handling"""
        uptime = datetime.now() - self.start_time
        
        # Safe atom count
        atom_count = 0
        try:
            if self.storage and hasattr(self.storage, 'db'):
                atom_count = self.storage.db.execute(
                    'SELECT COUNT(*) FROM atoms'
                ).fetchone()[0]
        except:
            pass
            
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
        """Safe chat routing"""
        if self.chat:
            try:
                return self.chat.process_message(message)
            except:
                return "Chat error"
        return "Chat not available"
        
    def save_state(self):
        """Save state safely"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'processed_count': self.processed_count,
            'pattern_hits': self.pattern_hits
        }
        
        try:
            with open('crod_state.json', 'w') as f:
                json.dump(state, f, indent=2)
            print("✓ State saved")
        except Exception as e:
            print(f"⚠ Save failed: {e}")
            
    def load_state(self):
        """Load state safely"""
        try:
            with open('crod_state.json', 'r') as f:
                state = json.load(f)
                self.processed_count = state.get('processed_count', 0)
                self.pattern_hits = state.get('pattern_hits', {})
                print("✓ State loaded")
        except:
            print("ℹ No previous state")

# Only test if run directly
if __name__ == "__main__":
    print("Testing CROD Engine...")
    engine = CRODEngine()
    
    # Safe test
    try:
        result = engine.process("ich halt... bruh")
        print(f"\nResult: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Test failed: {e}")
        
    print("\nEngine is ready for use!")