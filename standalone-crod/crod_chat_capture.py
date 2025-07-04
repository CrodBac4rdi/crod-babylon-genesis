#!/usr/bin/env python3
"""
CROD Chat Capture - FINALLY captures ALL Claude chat automatically!
"""

import json
import asyncio
import websockets
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class ChatFileHandler(FileSystemEventHandler):
    def __init__(self, websocket_uri="ws://localhost:8765"):
        self.ws_uri = websocket_uri
        self.last_position = 0
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Look for Claude chat files
        if "claude" in event.src_path or "chat" in event.src_path:
            asyncio.run(self.process_file(event.src_path))
            
    async def process_file(self, filepath):
        """Read new content from file and send to CROD"""
        try:
            with open(filepath, 'r') as f:
                f.seek(self.last_position)
                new_content = f.read()
                self.last_position = f.tell()
                
                if new_content.strip():
                    # Parse and send each line
                    for line in new_content.split('\n'):
                        if line.strip():
                            await self.send_to_crod(line)
                            
        except Exception as e:
            print(f"Error reading file: {e}")
            
    async def send_to_crod(self, content):
        """Send content to CROD Mirror"""
        try:
            # Detect role from content patterns
            role = "user"
            if "Assistant:" in content or "🔥" in content:
                role = "assistant"
                
            async with websockets.connect(self.ws_uri) as websocket:
                message = {
                    'type': 'chat',
                    'role': role,
                    'content': content,
                    'timestamp': time.time()
                }
                await websocket.send(json.dumps(message))
                
        except Exception as e:
            pass  # Silent fail to not interrupt chat

class StdinCapture:
    """Capture stdin/stdout for direct integration"""
    def __init__(self):
        self.ws_uri = "ws://localhost:8765"
        
    async def capture_and_send(self):
        """Read from stdin and send to CROD"""
        print("📡 CROD Chat Capture Active - All messages are being processed!")
        
        # Monitor stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        
        while True:
            try:
                line = await reader.readline()
                if line:
                    content = line.decode().strip()
                    if content:
                        # Determine role
                        role = "user" if not any(x in content for x in ["🔥", "✅", "```"]) else "assistant"
                        
                        # Send to CROD
                        async with websockets.connect(self.ws_uri) as websocket:
                            message = {
                                'type': 'chat',
                                'role': role,
                                'content': content,
                                'timestamp': time.time()
                            }
                            await websocket.send(json.dumps(message))
                            
            except Exception as e:
                await asyncio.sleep(0.1)

# Hook into Claude environment
def setup_claude_hook():
    """Setup automatic chat capture"""
    hook_script = """
# CROD Chat Capture Hook
crod_capture() {
    # Capture both user input and assistant output
    while IFS= read -r line; do
        echo "$line"  # Pass through
        # Send to CROD in background
        echo "$line" | python3 /home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_chat_capture.py --stdin 2>/dev/null &
    done
}

# Hook into shell if not already done
if [[ ! "$PROMPT_COMMAND" =~ "crod_capture" ]]; then
    export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND; }crod_capture"
fi
"""
    
    # Write hook to shell config
    shell_rc = Path.home() / ".bashrc"
    
    # Check if hook already exists
    with open(shell_rc, 'r') as f:
        content = f.read()
        
    if "CROD Chat Capture Hook" not in content:
        with open(shell_rc, 'a') as f:
            f.write("\n" + hook_script + "\n")
        print("✅ Claude hook installed! Restart shell to activate.")
    else:
        print("✅ Claude hook already installed!")

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        # Single message mode from stdin
        content = sys.stdin.read().strip()
        if content:
            async with websockets.connect("ws://localhost:8765") as websocket:
                message = {
                    'type': 'chat',
                    'role': 'mixed',
                    'content': content,
                    'timestamp': time.time()
                }
                await websocket.send(json.dumps(message))
    else:
        # Setup hook
        setup_claude_hook()
        
        # Start stdin capture
        capture = StdinCapture()
        await capture.capture_and_send()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 CROD Chat Capture stopped")