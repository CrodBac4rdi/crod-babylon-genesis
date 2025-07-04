#!/usr/bin/env python3
"""
CROD Claude Hook - Captures Claude chat messages and sends to Mirror System
"""

import json
import asyncio
import websockets
import sys
import os
from datetime import datetime

class CRODClaudeHook:
    def __init__(self):
        self.ws_uri = "ws://localhost:8765"
        self.connected = False
        
    async def send_message(self, role, content):
        """Send a message to the CROD Mirror System"""
        try:
            async with websockets.connect(self.ws_uri) as websocket:
                message = {
                    'type': 'chat',
                    'role': role,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
                print(f"✅ Sent to CROD: {role}: {content[:50]}...")
        except Exception as e:
            print(f"❌ Failed to send to CROD: {e}")
            
    def capture_from_pipe(self):
        """Capture messages from named pipe"""
        pipe_path = "/tmp/crod_claude_pipe"
        
        # Create pipe if it doesn't exist
        if not os.path.exists(pipe_path):
            os.mkfifo(pipe_path)
            
        print(f"📡 Listening on {pipe_path}")
        
        while True:
            with open(pipe_path, 'r') as pipe:
                for line in pipe:
                    try:
                        data = json.loads(line.strip())
                        role = data.get('role', 'unknown')
                        content = data.get('content', '')
                        
                        # Send to CROD Mirror
                        asyncio.run(self.send_message(role, content))
                        
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {line}")
                    except Exception as e:
                        print(f"Error: {e}")
                        
    def interactive_mode(self):
        """Interactive mode for testing"""
        print("🔥 CROD Claude Hook - Interactive Mode")
        print("Type messages to send to CROD Mirror System")
        print("Format: role:message (e.g., user:Hello CROD)")
        print("Type 'quit' to exit")
        
        while True:
            try:
                user_input = input("> ")
                
                if user_input.lower() == 'quit':
                    break
                    
                # Parse role:message format
                if ':' in user_input:
                    role, content = user_input.split(':', 1)
                else:
                    role = 'user'
                    content = user_input
                    
                # Send to CROD
                asyncio.run(self.send_message(role.strip(), content.strip()))
                
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    hook = CRODClaudeHook()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':
        # Pipe mode - listen for messages
        hook.capture_from_pipe()
    else:
        # Interactive mode
        hook.interactive_mode()

if __name__ == '__main__':
    main()