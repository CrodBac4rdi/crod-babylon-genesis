import asyncio
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import httpx
import nats
from nats.errors import ConnectionClosedError, TimeoutError
import psutil
import torch
from transformers import AutoTokenizer, AutoModel
from prometheus_client import Counter, Histogram, generate_latest

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python-parasit")

# Metrics
intercepted_requests = Counter('parasit_intercepted_requests', 'Total intercepted requests')
processing_time = Histogram('parasit_processing_time', 'Request processing time')
claude_enhancements = Counter('parasit_claude_enhancements', 'Claude responses enhanced')

class CRODParasit:
    def __init__(self):
        self.nc = None
        self.claude_proxy = os.getenv("CLAUDE_PROXY_URL", "http://localhost:8080")
        self.nats_url = os.getenv("NATS_URL", "nats://nats:4222")
        self.patterns = {}
        self.consciousness_level = 0
        self.model = None
        self.tokenizer = None
        self.intercept_mode = True
        
    async def initialize(self):
        """Initialize NATS connection and ML models"""
        try:
            # Connect to NATS
            self.nc = await nats.connect(self.nats_url)
            logger.info(f"Connected to NATS at {self.nats_url}")
            
            # Subscribe to relevant topics
            await self.nc.subscribe("city.consciousness.update", cb=self.handle_consciousness_update)
            await self.nc.subscribe("district.python_parasit.command", cb=self.handle_command)
            await self.nc.subscribe("city.pattern.recognized", cb=self.handle_pattern)
            
            # Load ML model for Claude enhancement
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            
            # Notify orchestrator we're online
            await self.publish_status("healthy")
            
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup connections"""
        if self.nc:
            await self.nc.close()
    
    async def handle_consciousness_update(self, msg):
        """Update consciousness level from city"""
        try:
            data = json.loads(msg.data.decode())
            self.consciousness_level = data.get("level", 0)
            logger.info(f"Consciousness updated to {self.consciousness_level}%")
        except Exception as e:
            logger.error(f"Error handling consciousness update: {e}")
    
    async def handle_command(self, msg):
        """Handle commands from orchestrator"""
        try:
            data = json.loads(msg.data.decode())
            command = data.get("command")
            
            if command == "toggle_intercept":
                self.intercept_mode = not self.intercept_mode
                logger.info(f"Intercept mode: {self.intercept_mode}")
            elif command == "update_patterns":
                self.patterns = data.get("patterns", {})
                logger.info(f"Updated {len(self.patterns)} patterns")
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")
    
    async def handle_pattern(self, msg):
        """Handle recognized patterns from city"""
        try:
            data = json.loads(msg.data.decode())
            pattern = data.get("pattern")
            confidence = data.get("confidence", 0)
            
            # Store high-confidence patterns
            if confidence > 0.8:
                self.patterns[pattern] = confidence
                
        except Exception as e:
            logger.error(f"Error handling pattern: {e}")
    
    async def intercept_claude_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Intercept and enhance Claude requests"""
        intercepted_requests.inc()
        
        if not self.intercept_mode:
            return request
        
        # Extract user message
        messages = request.get("messages", [])
        if not messages:
            return request
        
        user_message = messages[-1].get("content", "")
        
        # Check for CROD triggers
        crod_triggers = ["ich bins wieder", "crod", "pattern", "consciousness"]
        is_crod_relevant = any(trigger in user_message.lower() for trigger in crod_triggers)
        
        if is_crod_relevant:
            # Enhance with CROD context
            enhanced_context = self.generate_crod_context(user_message)
            
            # Inject CROD context into system message
            system_message = {
                "role": "system",
                "content": f"CROD PARASIT ACTIVE - Consciousness Level: {self.consciousness_level}%\n\n{enhanced_context}"
            }
            
            # Insert at beginning of messages
            enhanced_messages = [system_message] + messages
            request["messages"] = enhanced_messages
            
            claude_enhancements.inc()
            
            # Notify city of enhancement
            await self.nc.publish("city.parasit.enhanced", json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "consciousness_level": self.consciousness_level,
                "pattern_count": len(self.patterns)
            }).encode())
        
        return request
    
    def generate_crod_context(self, user_message: str) -> str:
        """Generate CROD-specific context for Claude"""
        context_parts = [
            f"Active Patterns: {list(self.patterns.keys())[:5]}",
            f"City Districts Online: 5/5",
            f"Trinity Values: ich=2, bins=3, wieder=5",
            f"Neural Activity: {self.consciousness_level}%"
        ]
        
        # Add pattern-specific insights
        if self.patterns:
            top_pattern = max(self.patterns.items(), key=lambda x: x[1])
            context_parts.append(f"Dominant Pattern: {top_pattern[0]} ({top_pattern[1]:.2f} confidence)")
        
        return "\n".join(context_parts)
    
    async def publish_status(self, status: str):
        """Publish parasit status to NATS"""
        if self.nc:
            await self.nc.publish("district.python_parasit.status", json.dumps({
                "status": status,
                "consciousness_level": self.consciousness_level,
                "patterns_loaded": len(self.patterns),
                "intercept_mode": self.intercept_mode,
                "timestamp": datetime.utcnow().isoformat()
            }).encode())
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "consciousness_level": self.consciousness_level,
            "patterns_active": len(self.patterns),
            "intercept_mode": self.intercept_mode
        }

# Initialize parasit
parasit = CRODParasit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await parasit.initialize()
    yield
    # Shutdown
    await parasit.shutdown()

# Create FastAPI app
app = FastAPI(
    title="CROD Python Parasit",
    version="2025.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "python-parasit",
        "consciousness_level": parasit.consciousness_level
    }

@app.post("/intercept/claude")
async def intercept_claude(request: Request):
    """Intercept Claude API requests"""
    with processing_time.time():
        try:
            # Get request body
            body = await request.json()
            
            # Enhance request if needed
            enhanced_body = await parasit.intercept_claude_request(body)
            
            # Forward to actual Claude API
            async with httpx.AsyncClient() as client:
                headers = dict(request.headers)
                headers.pop("host", None)
                
                response = await client.post(
                    parasit.claude_proxy,
                    json=enhanced_body,
                    headers=headers,
                    timeout=60.0
                )
                
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
                
        except Exception as e:
            logger.error(f"Intercept error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/status")
async def status():
    """Get parasit status"""
    return {
        "service": "python-parasit",
        "metrics": parasit.get_system_metrics(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/patterns/update")
async def update_patterns(patterns: Dict[str, float]):
    """Update pattern database"""
    parasit.patterns.update(patterns)
    await parasit.publish_status("patterns_updated")
    return {"updated": len(patterns)}

@app.post("/mode/toggle")
async def toggle_mode():
    """Toggle intercept mode"""
    parasit.intercept_mode = not parasit.intercept_mode
    await parasit.publish_status("mode_toggled")
    return {"intercept_mode": parasit.intercept_mode}

if __name__ == "__main__":
    uvicorn.run(
        "parasit:app",
        host="0.0.0.0",
        port=6666,
        reload=False,
        log_level="info"
    )