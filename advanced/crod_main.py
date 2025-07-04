# crod_main.py - Main entry point
# Version 2.0 - Complete Implementation with Engine

from crod_patterns import CRODPatterns
from crod_storage import CRODStorage
from crod_chat import CRODChat
from crod_engine import CRODEngine

class CROD:
    def __init__(self):
        """Initialize CROD Mental Systems"""
        # Use Engine as central coordinator
        self.engine = CRODEngine()
        
        # Direct access to modules for convenience
        self.storage = self.engine.storage
        self.patterns = self.engine.patterns
        self.chat = self.engine.chat
        
        print("\nCROD Mental Systems initialized!")
        print("Modules loaded: storage, patterns, chat, ENGINE")
        print("Type 'help' for commands\n")
        
    def run(self):
        """Main interactive loop"""
        while True:
            try:
                cmd = input("CROD> ").strip()
                
                if cmd == 'quit' or cmd == 'exit':
                    print("Saving state...")
                    self.engine.save_state()
                    print("Goodbye!")
                    break
                    
                elif cmd.startswith('detect '):
                    text = cmd[7:]
                    found = self.patterns.detect(text)
                    if found:
                        print(f"Patterns found: {found}")
                    else:
                        print("No patterns detected")
                    
                elif cmd.startswith('process '):
                    text = cmd[8:]
                    result = self.engine.process(text)
                    print(f"Processed: {result['patterns']}")
                    print(f"Total processed: {result['processed']}")
                    
                elif cmd.startswith('chat '):
                    msg = cmd[5:]
                    response = self.engine.chat_message(msg)
                    print(f"CROD: {response}")
                    
                elif cmd == 'stats':
                    stats = self.engine.get_stats()
                    print("\n=== ENGINE STATS ===")
                    print(f"Version: {stats['version']}")
                    print(f"Uptime: {stats['uptime']}")
                    print(f"Processed: {stats['processed']}")
                    print(f"Atoms in DB: {stats['atoms']}")
                    if stats['top_patterns']:
                        print("\nTop Patterns:")
                        for pattern, count in stats['top_patterns']:
                            print(f"  {pattern}: {count}")
                    print("==================\n")
                    
                elif cmd == 'atoms':
                    cursor = self.storage.db.cursor()
                    atoms = cursor.execute('SELECT * FROM atoms ORDER BY id').fetchall()
                    print(f"\nTotal atoms: {len(atoms)}")
                    for atom in atoms[:10]:  # Show first 10
                        print(f"  [{atom[0]:4}] {atom[1]:20} (weight: {atom[2]})")
                    if len(atoms) > 10:
                        print(f"  ... and {len(atoms) - 10} more")
                        
                elif cmd.startswith('add atom '):
                    value = cmd[9:]
                    try:
                        atom_id = self.storage.add_atom(value)
                        print(f"Added atom: [{atom_id}] {value}")
                    except:
                        print(f"Atom already exists: {value}")
                        
                elif cmd == 'save':
                    self.engine.save_state()
                    
                elif cmd == 'load':
                    self.engine.load_state()
                    
                elif cmd == 'help' or cmd == '?':
                    self.show_help()
                    
                elif cmd == '':
                    continue
                    
                else:
                    print(f"Unknown command: '{cmd}'. Type 'help' for commands.")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit properly")
            except Exception as e:
                print(f"Error: {e}")
                
    def show_help(self):
        """Display help information"""
        print("\n=== CROD COMMANDS ===")
        print("detect <text>     - Detect patterns in text")
        print("process <text>    - Full processing pipeline")
        print("chat <message>    - Chat with CROD")
        print("stats             - Show engine statistics")
        print("atoms             - List atoms in database")
        print("add atom <value>  - Add new atom")
        print("save              - Save current state")
        print("load              - Load previous state")
        print("help              - Show this help")
        print("quit              - Exit (auto-saves)")
        print("===================\n")

# Entry point
if __name__ == '__main__':
    try:
        crod = CROD()
        crod.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()