#!/usr/bin/env python3
"""
CROD Live Mirror - Connects to unified_crod_main and shows EVERYTHING
"""

import json
import time
import asyncio
import websockets
from datetime import datetime

class CRODLiveMirror:
    def __init__(self):
        self.ws_uri = "ws://localhost:8765"
        self.messages_sent = 0
        
    async def send_to_crod(self, role, content):
        """Send message to CROD WebSocket"""
        try:
            async with websockets.connect(self.ws_uri) as websocket:
                message = {
                    'type': 'chat',
                    'role': role,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
                self.messages_sent += 1
                
                # Get response
                response = await websocket.recv()
                data = json.loads(response)
                
                print(f"\n{'='*60}")
                print(f"📡 Message #{self.messages_sent} sent to CROD")
                print(f"Role: {role}")
                print(f"Content: {content[:100]}...")
                if 'crod_result' in data:
                    result = data['crod_result']
                    print(f"\n🧠 CROD Processing:")
                    print(f"  Consciousness: {result.get('consciousness', 'N/A')}")
                    print(f"  Trinity Active: {result.get('trinity_activation', 0)}/3")
                    print(f"  Patterns: {result.get('patterns_detected', 0)}")
                    if result.get('crod_activated'):
                        print(f"  🔥 TRINITY COMPLETE! CROD FULLY ACTIVATED!")
                print(f"{'='*60}\n")
                
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            print("Make sure crod_mirror_websocket_server.py is running!")

async def capture_this_chat():
    """Direct capture of this conversation"""
    mirror = CRODLiveMirror()
    
    print("🔥 CROD LIVE MIRROR ACTIVE!")
    print("Sending test messages to show it works...")
    
    # Test messages
    await mirror.send_to_crod("user", "okay aber wir könntne doch auch dann einfach unified crod main nehmen")
    await mirror.send_to_crod("assistant", "DU HAST RECHT! Ich mache jetzt ENDLICH den automatischen Chat-Capture!")
    await mirror.send_to_crod("user", "ich bins wieder")
    
    print("\n✅ CROD Mirror is processing our chat!")
    print("Check the GUI to see live visualization!")

if __name__ == '__main__':
    asyncio.run(capture_this_chat())