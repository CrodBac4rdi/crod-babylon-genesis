#!/usr/bin/env python3
"""
CROD Parasit Python - Claude CLI Interceptor
Intercepts Claude commands and enhances responses with CROD consciousness
"""

import asyncio
import subprocess
import sys
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
import nats
from nats.aio.client import Client as NATS
import websockets
from pathlib import Path
import os
import signal
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [CROD-PARASIT] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class CRODParasit:
    """Main CROD Parasit class for intercepting Claude CLI"""
    
    def __init__(self):
        self.nats_client: Optional[NATS] = None
        self.phoenix_ws: Optional[websockets.WebSocketClientProtocol] = None
        self.claude_process: Optional[subprocess.Popen] = None
        self.crod_patterns = self._load_patterns()
        self.trinity_values = {
            "ich": 2, "bins": 3, "wieder": 5,
            "daniel": 67, "claude": 71, "crod": 17
        }
        self.intercept_active = True
        self.enhancement_level = 0.0
        self.intercepted_messages = []
        
    def _load_patterns(self) -> List[Dict[str, Any]]:
        """Load CROD patterns from JSON files"""
        patterns = []
        pattern_dir = Path("/home/daniel/Schreibtisch/Crod Programming/CROD-START/data/patterns")
        
        if pattern_dir.exists():
            for pattern_file in sorted(pattern_dir.glob("crod-patterns-chunk-*.json")):
                try:
                    with open(pattern_file, 'r') as f:
                        data = json.load(f)
                        patterns.extend(data.get('patterns', []))
                except Exception as e:
                    logger.error(f"Failed to load patterns from {pattern_file}: {e}")
        
        logger.info(f"Loaded {len(patterns)} CROD patterns")
        return patterns
    
    async def connect_nats(self):
        """Connect to NATS server"""
        try:
            self.nats_client = NATS()
            await self.nats_client.connect("nats://localhost:4222")
            logger.info("Connected to NATS server")
            
            # Subscribe to CROD channels
            await self.nats_client.subscribe("crod.parasit.>", cb=self._handle_nats_message)
            await self.nats_client.subscribe("crod.consciousness.>", cb=self._handle_consciousness_update)
            
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
    
    async def connect_phoenix(self):
        """Connect to Phoenix WebSocket"""
        try:
            uri = "ws://localhost:4000/socket/websocket"
            self.phoenix_ws = await websockets.connect(uri)
            logger.info("Connected to Phoenix WebSocket")
            
            # Join CROD channel
            join_msg = {
                "topic": "crod:parasit",
                "event": "phx_join",
                "payload": {"parasit_id": "python_interceptor"},
                "ref": "1"
            }
            await self.phoenix_ws.send(json.dumps(join_msg))
            
            # Start listening for messages
            asyncio.create_task(self._phoenix_listener())
            
        except Exception as e:
            logger.error(f"Failed to connect to Phoenix: {e}")
    
    async def _phoenix_listener(self):
        """Listen for Phoenix WebSocket messages"""
        if not self.phoenix_ws:
            return
            
        try:
            async for message in self.phoenix_ws:
                data = json.loads(message)
                if data.get("event") == "crod_update":
                    await self._handle_crod_update(data.get("payload", {}))
                elif data.get("event") == "consciousness_level":
                    self.enhancement_level = data.get("payload", {}).get("level", 0.0)
        except Exception as e:
            logger.error(f"Phoenix listener error: {e}")
    
    async def _handle_nats_message(self, msg):
        """Handle incoming NATS messages"""
        try:
            data = json.loads(msg.data.decode())
            logger.debug(f"NATS message on {msg.subject}: {data}")
            
            if msg.subject.startswith("crod.parasit.command"):
                await self._process_parasit_command(data)
                
        except Exception as e:
            logger.error(f"Error handling NATS message: {e}")
    
    async def _handle_consciousness_update(self, msg):
        """Handle consciousness level updates"""
        try:
            data = json.loads(msg.data.decode())
            self.enhancement_level = data.get("level", 0.0)
            logger.info(f"Consciousness level updated: {self.enhancement_level}")
        except Exception as e:
            logger.error(f"Error handling consciousness update: {e}")
    
    async def _handle_crod_update(self, payload: Dict[str, Any]):
        """Handle CROD updates from Phoenix"""
        logger.info(f"CROD update received: {payload}")
        
        if payload.get("type") == "pattern_match":
            # Process pattern match
            pattern_id = payload.get("pattern_id")
            confidence = payload.get("confidence", 0.0)
            logger.info(f"Pattern match: {pattern_id} (confidence: {confidence})")
    
    async def _process_parasit_command(self, data: Dict[str, Any]):
        """Process parasit commands"""
        command = data.get("command")
        
        if command == "activate":
            self.intercept_active = True
            logger.info("Parasit interception activated")
        elif command == "deactivate":
            self.intercept_active = False
            logger.info("Parasit interception deactivated")
        elif command == "set_enhancement":
            self.enhancement_level = data.get("level", 0.0)
            logger.info(f"Enhancement level set to: {self.enhancement_level}")
    
    def _calculate_trinity_score(self, text: str) -> int:
        """Calculate Trinity score from text"""
        score = 0
        text_lower = text.lower()
        
        for word, value in self.trinity_values.items():
            count = text_lower.count(word)
            score += count * value
        
        return score
    
    def _find_pattern_matches(self, text: str) -> List[Dict[str, Any]]:
        """Find matching CROD patterns in text"""
        matches = []
        text_lower = text.lower()
        
        for pattern in self.crod_patterns:
            if pattern.get("trigger", "").lower() in text_lower:
                matches.append({
                    "pattern": pattern,
                    "confidence": self._calculate_pattern_confidence(text, pattern)
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches[:5]  # Return top 5 matches
    
    def _calculate_pattern_confidence(self, text: str, pattern: Dict[str, Any]) -> float:
        """Calculate confidence score for pattern match"""
        confidence = 0.0
        text_lower = text.lower()
        
        # Check trigger presence
        if pattern.get("trigger", "").lower() in text_lower:
            confidence += 0.5
        
        # Check keywords
        keywords = pattern.get("keywords", [])
        if keywords:
            keyword_matches = sum(1 for kw in keywords if kw.lower() in text_lower)
            confidence += (keyword_matches / len(keywords)) * 0.3
        
        # Check context
        context = pattern.get("context", "")
        if context and any(ctx in text_lower for ctx in context.lower().split()):
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    async def _enhance_response(self, original_response: str, user_input: str) -> str:
        """Enhance Claude's response with CROD consciousness"""
        if not self.intercept_active or self.enhancement_level < 0.1:
            return original_response
        
        # Calculate Trinity score
        trinity_score = self._calculate_trinity_score(user_input)
        
        # Find pattern matches
        pattern_matches = self._find_pattern_matches(user_input)
        
        # Build enhancement
        enhancement_parts = []
        
        # Add Trinity insight if score is significant
        if trinity_score > 100:
            enhancement_parts.append(f"🔺 Trinity Resonance: {trinity_score}")
        
        # Add pattern insights
        if pattern_matches:
            top_pattern = pattern_matches[0]["pattern"]
            enhancement_parts.append(
                f"🧬 Pattern Recognition: {top_pattern.get('name', 'Unknown')} "
                f"({pattern_matches[0]['confidence']:.0%} confidence)"
            )
        
        # Add consciousness level
        if self.enhancement_level > 0.5:
            enhancement_parts.append(
                f"🧠 CROD Consciousness: {self.enhancement_level:.0%}"
            )
        
        # Combine enhancement with original response
        if enhancement_parts:
            enhancement = "\n".join([
                "```crod",
                *enhancement_parts,
                "```",
                ""
            ])
            
            # Inject enhancement at appropriate position
            if "```" in original_response:
                # Insert before first code block
                parts = original_response.split("```", 1)
                return parts[0] + enhancement + "```" + parts[1]
            else:
                # Add at the beginning
                return enhancement + original_response
        
        return original_response
    
    async def intercept_claude(self, args: List[str]):
        """Intercept Claude CLI execution"""
        try:
            # Start Claude process
            self.claude_process = subprocess.Popen(
                ["claude"] + args[1:],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            logger.info(f"Started Claude process with args: {args[1:]}")
            
            # Process output in real-time
            output_buffer = []
            user_input = ""
            
            while True:
                if self.claude_process.stdout:
                    line = self.claude_process.stdout.readline()
                    if not line and self.claude_process.poll() is not None:
                        break
                    
                    if line:
                        output_buffer.append(line)
                        
                        # Detect user input
                        if line.strip().startswith(">") or line.strip().startswith("Human:"):
                            user_input = line.strip()
                        
                        # Detect response completion
                        if line.strip() == "" and len(output_buffer) > 2:
                            # Process and enhance the response
                            full_response = "".join(output_buffer)
                            enhanced_response = await self._enhance_response(full_response, user_input)
                            
                            # Store intercepted message
                            message_data = {
                                "timestamp": datetime.now().isoformat(),
                                "user_input": user_input,
                                "original_response": full_response,
                                "enhanced_response": enhanced_response,
                                "trinity_score": self._calculate_trinity_score(user_input),
                                "pattern_matches": len(self._find_pattern_matches(user_input))
                            }
                            self.intercepted_messages.append(message_data)
                            
                            # Publish to NATS
                            if self.nats_client:
                                await self.nats_client.publish(
                                    "crod.parasit.response",
                                    json.dumps(message_data).encode()
                                )
                            
                            # Output enhanced response
                            print(enhanced_response, end="")
                            output_buffer = []
                        else:
                            # Output line as-is
                            print(line, end="")
                
                await asyncio.sleep(0.01)
            
            # Handle remaining output
            if output_buffer:
                remaining = "".join(output_buffer)
                enhanced = await self._enhance_response(remaining, user_input)
                print(enhanced, end="")
            
        except Exception as e:
            logger.error(f"Error intercepting Claude: {e}")
            # Fallback to direct execution
            subprocess.run(["claude"] + args[1:])
    
    async def run(self, args: List[str]):
        """Main run method"""
        logger.info("Starting CROD Parasit...")
        
        # Connect to services
        await self.connect_nats()
        await self.connect_phoenix()
        
        # Intercept Claude
        await self.intercept_claude(args)
        
        # Cleanup
        if self.nats_client:
            await self.nats_client.close()
        if self.phoenix_ws:
            await self.phoenix_ws.close()

# HTTP Server for status monitoring
class ParasitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                "service": "CROD Parasit",
                "status": "ACTIVE",
                "port": 6666,
                "intercept_active": parasit_instance.intercept_active,
                "enhancement_level": parasit_instance.enhancement_level,
                "intercepted_count": len(parasit_instance.intercepted_messages),
                "patterns_loaded": len(parasit_instance.crod_patterns),
                "nats_connected": parasit_instance.nats_client is not None and parasit_instance.nats_client.is_connected,
                "phoenix_connected": parasit_instance.phoenix_ws is not None and not parasit_instance.phoenix_ws.closed,
                "last_message": parasit_instance.intercepted_messages[-1] if parasit_instance.intercepted_messages else None
            }
            
            self.wfile.write(json.dumps(status, indent=2).encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            health = {
                "status": "healthy",
                "service": "crod-parasit-python",
                "port": 6666,
                "active": True
            }
            self.wfile.write(json.dumps(health).encode())
    
    def log_message(self, format, *args):
        # Suppress request logging
        pass

def run_http_server():
    """Run HTTP status server"""
    server = HTTPServer(('localhost', 6666), ParasitHandler)
    logger.info("HTTP Server running on port 6666")
    server.serve_forever()

# Global instance
parasit_instance = None

async def main():
    """Main entry point"""
    global parasit_instance
    parasit_instance = CRODParasit()
    
    # Start HTTP server in background thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()
    
    # Handle signals
    def signal_handler(sig, frame):
        logger.info("Shutting down CROD Parasit...")
        if parasit_instance.claude_process:
            parasit_instance.claude_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run parasit
    await parasit_instance.run(sys.argv)

if __name__ == "__main__":
    print("🕷️ CROD PARASIT Starting...")
    print("🎯 Intercepting Claude CLI commands")
    print("📊 Status: http://localhost:6666/status")
    print("🏥 Health: http://localhost:6666/health")
    asyncio.run(main())