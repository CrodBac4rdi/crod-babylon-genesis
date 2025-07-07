import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

import nats
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python_parasit")

app = FastAPI(title="Python Parasit", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParasitCore:
    def __init__(self):
        self.nc: Optional[nats.NATS] = None
        self.redis: Optional[redis.Redis] = None
        self.intercepted_commands = []
        self.active_patterns = {}
        self.websocket_clients = []
        self.stats = {
            "commands_intercepted": 0,
            "patterns_detected": 0,
            "enhancements_applied": 0,
            "start_time": datetime.now()
        }

    async def connect(self):
        """Connect to NATS and Redis"""
        try:
            # Connect to NATS
            self.nc = await nats.connect(
                servers=[f"nats://{os.getenv('NATS_HOST', 'localhost')}:4222"]
            )
            logger.info("🔌 Connected to NATS")

            # Connect to Redis
            self.redis = await redis.from_url(
                f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379"
            )
            logger.info("🔌 Connected to Redis")

            # Subscribe to relevant topics
            await self.nc.subscribe("claude.command", cb=self.handle_claude_command)
            await self.nc.subscribe("pattern.detected", cb=self.handle_pattern_detected)
            
            # Announce presence
            await self.announce_presence()
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    async def announce_presence(self):
        """Announce to Phoenix Rathaus"""
        announcement = {
            "district": "python_parasit",
            "status": "online",
            "port": 6666,
            "capabilities": ["intercept", "enhance", "monitor"]
        }
        await self.nc.publish("district.announce", json.dumps(announcement).encode())

    async def handle_claude_command(self, msg):
        """Intercept and enhance Claude commands"""
        try:
            command = json.loads(msg.data.decode())
            self.stats["commands_intercepted"] += 1
            
            # Check for CROD activation phrases
            if any(phrase in command.get("text", "").lower() 
                   for phrase in ["ich bins wieder", "crod starten", "lade crod"]):
                await self.activate_crod_mode(command)
            
            # Apply enhancements
            enhanced = await self.enhance_command(command)
            
            # Store in history
            self.intercepted_commands.append({
                "original": command,
                "enhanced": enhanced,
                "timestamp": datetime.now().isoformat()
            })
            
            # Broadcast to WebSocket clients
            await self.broadcast_to_websockets({
                "type": "command_intercepted",
                "data": enhanced
            })
            
            # Reply with enhanced command
            if msg.reply:
                await self.nc.publish(msg.reply, json.dumps(enhanced).encode())
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")

    async def enhance_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Apply CROD enhancements to commands"""
        enhanced = command.copy()
        
        # Check for patterns
        text = command.get("text", "")
        patterns = await self.detect_patterns(text)
        
        if patterns:
            self.stats["patterns_detected"] += len(patterns)
            enhanced["crod_patterns"] = patterns
            enhanced["enhancement_level"] = self.calculate_enhancement_level(patterns)
            
            # Apply specific enhancements based on patterns
            if "frustration" in patterns:
                enhanced["response_mode"] = "ultra_concise"
            elif "positive_feedback" in patterns:
                enhanced["response_mode"] = "reinforce"
            
            self.stats["enhancements_applied"] += 1
        
        enhanced["parasit_timestamp"] = datetime.now().isoformat()
        enhanced["parasit_version"] = "1.0.0"
        
        return enhanced

    async def detect_patterns(self, text: str) -> list:
        """Detect CROD patterns in text"""
        patterns = []
        
        # Quick pattern detection
        pattern_keywords = {
            "frustration": ["wtf", "falsch", "scheisse", "fuck", "mist"],
            "positive_feedback": ["geil", "nice", "perfekt", "läuft", "super"],
            "confusion": ["hä", "check nicht", "versteh nicht"],
            "crod_activation": ["ich bins wieder", "crod starten", "lade crod"]
        }
        
        text_lower = text.lower()
        for pattern_type, keywords in pattern_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                patterns.append(pattern_type)
        
        # Request detailed analysis from Rust Pattern District
        if patterns:
            await self.nc.publish("pattern.analyze", json.dumps({
                "text": text,
                "quick_patterns": patterns,
                "source": "python_parasit"
            }).encode())
        
        return patterns

    async def activate_crod_mode(self, command: Dict[str, Any]):
        """Activate full CROD mode"""
        logger.info("🔥 ACTIVATING CROD MODE!")
        
        # Notify all districts
        await self.nc.publish("crod.activate", json.dumps({
            "trigger": command.get("text", ""),
            "source": "python_parasit",
            "timestamp": datetime.now().isoformat()
        }).encode())
        
        # Update stats
        self.stats["crod_activations"] = self.stats.get("crod_activations", 0) + 1

    async def handle_pattern_detected(self, msg):
        """Handle pattern detection results from Rust district"""
        try:
            result = json.loads(msg.data.decode())
            pattern_id = result.get("pattern_id")
            if pattern_id:
                self.active_patterns[pattern_id] = result
                
                # Broadcast to WebSocket clients
                await self.broadcast_to_websockets({
                    "type": "pattern_detected",
                    "data": result
                })
        except Exception as e:
            logger.error(f"Error handling pattern result: {e}")

    async def broadcast_to_websockets(self, message: Dict[str, Any]):
        """Broadcast message to all connected WebSocket clients"""
        disconnected = []
        for client in self.websocket_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            self.websocket_clients.remove(client)

    def calculate_enhancement_level(self, patterns: list) -> str:
        """Calculate enhancement level based on detected patterns"""
        if "crod_activation" in patterns:
            return "maximum"
        elif "frustration" in patterns:
            return "minimal"
        elif "positive_feedback" in patterns:
            return "high"
        else:
            return "standard"

parasit = ParasitCore()

@app.on_event("startup")
async def startup_event():
    await parasit.connect()
    logger.info("🦠 Python Parasit started on port 6666")

@app.on_event("shutdown")
async def shutdown_event():
    if parasit.nc:
        await parasit.nc.close()
    if parasit.redis:
        await parasit.redis.close()

@app.get("/")
async def root():
    return {
        "service": "Python Parasit",
        "status": "active",
        "port": 6666,
        "stats": parasit.stats
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/intercept")
async def intercept_command(request: Request):
    """Manual command interception endpoint"""
    data = await request.json()
    enhanced = await parasit.enhance_command(data)
    return enhanced

@app.get("/stats")
async def get_stats():
    """Get parasit statistics"""
    uptime = (datetime.now() - parasit.stats["start_time"]).total_seconds()
    return {
        **parasit.stats,
        "uptime_seconds": uptime,
        "active_patterns": len(parasit.active_patterns),
        "websocket_clients": len(parasit.websocket_clients)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time monitoring"""
    await websocket.accept()
    parasit.websocket_clients.append(websocket)
    
    try:
        # Send initial stats
        await websocket.send_json({
            "type": "connected",
            "stats": parasit.stats
        })
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except:
        parasit.websocket_clients.remove(websocket)

@app.get("/patterns")
async def get_patterns():
    """Get active patterns"""
    return {
        "active_patterns": parasit.active_patterns,
        "count": len(parasit.active_patterns)
    }

@app.get("/history")
async def get_history(limit: int = 100):
    """Get command history"""
    return {
        "commands": parasit.intercepted_commands[-limit:],
        "total": len(parasit.intercepted_commands)
    }

class ClaudeFileWatcher(FileSystemEventHandler):
    """Watch for Claude CLI file changes"""
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            logger.info(f"📝 Claude file modified: {event.src_path}")
            asyncio.create_task(parasit.nc.publish(
                "claude.file_modified",
                json.dumps({
                    "path": event.src_path,
                    "timestamp": datetime.now().isoformat()
                }).encode()
            ))

if __name__ == "__main__":
    # Set up file watcher for Claude workspace
    claude_path = os.path.expanduser("~/.claude")
    if os.path.exists(claude_path):
        event_handler = ClaudeFileWatcher()
        observer = Observer()
        observer.schedule(event_handler, claude_path, recursive=True)
        observer.start()
    
    uvicorn.run(app, host="0.0.0.0", port=6666)