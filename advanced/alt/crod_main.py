# crod_main.py - Main entry point (UPDATED)
# Version 2.0 - Mit Engine!

from crod_patterns import CRODPatterns
from crod_storage import CRODStorage
from crod_chat import CRODChat
from crod_engine import CRODEngine  # NEU!

class CROD:
    def __init__(self):
        # Use Engine instead of individual modules
        self.engine = CRODEngine()  # NEU!
        
        # For backwards compatibility
        self.storage = self.engine.storage
        self.patterns = self.engine.patterns
        self.chat = self.engine.chat
        
        print("CROD Mental Systems initialized!")
        print("Modules loaded: storage, patterns, chat, ENGINE")
        
    def run(self):
        """Main loop with engine integration"""
        while True:
            cmd = input("\nCROD> ").strip()
            
            if cmd == 'quit':
                self.engine.save_state()  # Auto-save on quit!
                break
                
            elif cmd.startswith('detect '):
                text = cmd[7:]
                found = self.patterns.detect(text)
                print(f"Patterns found: {found}")
                
            elif cmd.startswith('process '):  # NEU!
                text = cmd[8:]
                result = self.engine.process(text)
                print(f"Processed: {result}")
                
            elif cmd.startswith('chat '):
                msg = cmd[5:]
                response = self.engine.chat_message(msg)
                print(f"CROD: {response}")
                
            elif cmd == 'stats':
                # Erweiterte Stats von Engine!
                stats = self.engine.get_stats()
                print("\n=== ENGINE STATS ===")
                print(f"Version: {stats['version']}")
                print(f"Uptime: {stats['uptime']}")
                print(f"Processed: {stats['processed']}")
                print(f"Top Patterns: {stats.get('top_patterns', [])}")
                
            elif cmd == 'save':  # NEU!
                self.engine.save_state()
                
            elif cmd == 'load':  # NEU!
                self.engine.load_state()
                
            elif cmd == 'help':  # NEU!
                print("\nCommands:")
                print("  detect <text>  - Detect patterns")
                print("  process <text> - Full processing pipeline")
                print("  chat <msg>     - Chat with CROD")
                print("  stats          - Show engine statistics")
                print("  save           - Save current state")
                print("  load           - Load previous state")
                print("  help           - Show this help")
                print("  quit           - Exit (auto-saves)")

if __name__ == '__main__':
    crod = CROD()
    crod.run()