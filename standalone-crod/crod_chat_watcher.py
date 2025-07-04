#!/usr/bin/env python3
"""
CROD Chat Watcher - Watches Daniel-Claude chat and feeds to Unified CROD
"""

import time
import requests
import json
from datetime import datetime
from pathlib import Path
import sys

# Import unified CROD
sys.path.append(str(Path(__file__).parent))
from unified_crod_main import UnifiedCROD

class CRODChatWatcher:
    """Watches and learns from Daniel-Claude conversations"""
    
    def __init__(self):
        print("👁️ CROD Chat Watcher initializing...")
        
        # Start unified CROD
        self.crod = UnifiedCROD()
        
        # Chat history tracking
        self.last_message_hash = None
        self.conversation_count = 0
        
        print("✅ Chat watcher ready!")
        print("🦠 CROD will learn from your conversation with Claude!\n")
    
    def simulate_live_chat(self):
        """Simulate live chat input (in real implementation, would hook into Claude)"""
        
        # Example conversations that could happen
        example_chats = [
            ("hey claude wie gehts", "Mir geht's gut! Wie kann ich dir helfen?"),
            ("ich bins wieder daniel", "Willkommen zurück Daniel! Was machen wir heute?"),
            ("zeig mir den crod status", "Hier ist der CROD Status..."),
            ("kannst du crod verbessern?", "Ja, ich kann CROD optimieren..."),
            ("wtf das funktioniert nicht", "Lass mich das Problem analysieren..."),
            ("geil das läuft perfekt!", "Freut mich dass es funktioniert!"),
            ("was ist consciousness level?", "Consciousness Level ist..."),
            ("crod helper clan member 7", "CROD Helper Clan Member 7 ist...")
        ]
        
        print("📝 Simulating live chat learning...\n")
        
        for user_input, claude_response in example_chats:
            print(f"👤 Daniel: {user_input}")
            print(f"🤖 Claude: {claude_response}")
            
            # Feed to CROD
            self.crod.process_live_chat(user_input, claude_response)
            
            self.conversation_count += 1
            
            # Show CROD status
            if self.conversation_count % 3 == 0:
                status = self.crod.get_status()
                print(f"\n📊 CROD Learning Progress:")
                print(f"   Atoms: {status['atoms']} (🔥 {status['hot_atoms']} hot)")
                print(f"   Avg Heat: {status['avg_heat']:.2f}")
                print(f"   Max Consciousness: {status['max_consciousness']:.2f}")
                print(f"   Learning Events: {status['learning_events']}\n")
            
            time.sleep(2)
    
    def watch_real_chat(self):
        """Watch real chat (would need integration with Claude API)"""
        
        print("👁️ Watching for real chat messages...")
        print("⚠️  Real-time chat integration requires Claude API hook")
        print("📝 Using simulation mode instead...\n")
        
        # In real implementation:
        # - Monitor Claude API calls
        # - Extract user input and Claude responses
        # - Feed to CROD in real-time
        
        self.simulate_live_chat()
    
    def interactive_mode(self):
        """Interactive mode - manually input conversations"""
        
        print("💬 INTERACTIVE MODE")
        print("Type your conversation with Claude, CROD will learn!")
        print("Format: 'user: message' or 'claude: message'")
        print("Type 'status' to see CROD status, 'quit' to exit\n")
        
        user_buffer = ""
        claude_buffer = ""
        
        while True:
            try:
                inp = input("> ").strip()
                
                if inp.lower() == 'quit':
                    break
                elif inp.lower() == 'status':
                    status = self.crod.get_status()
                    print(f"\n📊 CROD Status:")
                    for key, value in status.items():
                        print(f"   {key}: {value}")
                    print()
                elif inp.startswith("user:"):
                    user_buffer = inp[5:].strip()
                    print(f"👤 Captured user input: {user_buffer}")
                elif inp.startswith("claude:"):
                    claude_buffer = inp[7:].strip()
                    print(f"🤖 Captured Claude response: {claude_buffer}")
                    
                    # Process the conversation
                    if user_buffer and claude_buffer:
                        self.crod.process_live_chat(user_buffer, claude_buffer)
                        print("✅ CROD learned from this interaction!\n")
                        user_buffer = ""
                        claude_buffer = ""
                else:
                    print("❓ Use 'user: message' or 'claude: message' format")
                    
            except KeyboardInterrupt:
                break
        
        print("\n👋 Chat watcher stopped")

def main():
    """Main entry point"""
    import sys
    
    watcher = CRODChatWatcher()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        watcher.interactive_mode()
    else:
        # Auto mode
        try:
            watcher.watch_real_chat()
        except KeyboardInterrupt:
            print("\n🛑 Stopped watching")
    
    # Keep CROD running
    watcher.crod.run_forever()

if __name__ == "__main__":
    main()