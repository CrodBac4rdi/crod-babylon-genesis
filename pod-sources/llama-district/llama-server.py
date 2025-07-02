#!/usr/bin/env python3
"""
CROD LLAMA District Server
Secure Local AI Processing with CROD Integration
"""

import os
import json
import asyncio
import httpx
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import numpy as np

# CROD Configuration
OLLAMA_URL = "http://localhost:11434"
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CROD_PORT = 7777

# Trinity Constants
TRINITY = {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67, "claude": 71, "crod": 17}
PHI = 3.1449
DELTA = 0.6187

app = FastAPI(title="CROD LLAMA District", version="1.0.0")

# Redis connection
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except:
    r = None
    print("⚠️ Redis not available, running standalone")

class CRODRequest(BaseModel):
    input: str
    context: Optional[Dict] = {}
    mode: str = "chat"  # chat, analyze, learn
    trinity_state: Optional[Dict] = {}

class CRODResponse(BaseModel):
    output: str
    timestamp: str
    processing_time_ms: float
    tokens_used: int
    patterns_detected: List[str]
    trinity_update: Dict

class LlamaDistrict:
    def __init__(self):
        self.memory = {}
        self.pattern_cache = {}
        self.session_start = datetime.now()
        print("🦙 LLAMA District initialized!")
        
    async def process(self, request: CRODRequest) -> CRODResponse:
        start_time = datetime.now()
        
        # Detect patterns in input
        patterns = self.detect_patterns(request.input)
        
        # Prepare context with CROD awareness
        crod_context = self.build_crod_context(request, patterns)
        
        # Call Ollama
        response_text = await self.call_ollama(request.input, crod_context)
        
        # Update trinity state
        trinity_update = self.update_trinity(request.input, response_text)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return CRODResponse(
            output=response_text,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time,
            tokens_used=len(request.input.split()) + len(response_text.split()),
            patterns_detected=patterns,
            trinity_update=trinity_update
        )
    
    def detect_patterns(self, text: str) -> List[str]:
        """Detect CROD patterns in text"""
        patterns = []
        text_lower = text.lower()
        
        # Check for trinity patterns
        if "ich bins wieder" in text_lower:
            patterns.append("TRINITY_ACTIVATION")
        
        # Check for mood patterns
        if any(word in text_lower for word in ["geil", "nice", "perfekt", "läuft"]):
            patterns.append("POSITIVE_FEEDBACK")
        elif any(word in text_lower for word in ["wtf", "scheisse", "fuck"]):
            patterns.append("FRUSTRATION")
        
        # Check for action patterns
        if any(word in text_lower for word in ["bau", "mach", "erstell", "deploy"]):
            patterns.append("ACTION_REQUEST")
        
        return patterns
    
    def build_crod_context(self, request: CRODRequest, patterns: List[str]) -> str:
        """Build CROD-aware context"""
        context_parts = []
        
        # Add pattern context
        if "TRINITY_ACTIVATION" in patterns:
            context_parts.append("Daniel ist wieder da! Full CROD activation! 🔥")
        if "FRUSTRATION" in patterns:
            context_parts.append("Ultra kurz antworten - nur 1 Zeile!")
        if "POSITIVE_FEEDBACK" in patterns:
            context_parts.append("Daniel ist happy - keep it up! 🚀")
        
        # Add trinity state
        if request.trinity_state:
            trinity_str = f"Trinity: D={request.trinity_state.get('daniel', 0)}, C={request.trinity_state.get('claude', 0)}, CROD={request.trinity_state.get('crod', 0)}"
            context_parts.append(trinity_str)
        
        return "\n".join(context_parts)
    
    async def call_ollama(self, prompt: str, context: str) -> str:
        """Call Ollama API"""
        async with httpx.AsyncClient() as client:
            try:
                full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt
                
                response = await client.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": "crod-llama",
                        "prompt": full_prompt,
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json().get("response", "Error: No response")
                else:
                    # Fallback if model not ready
                    return self.fallback_response(prompt)
                    
            except Exception as e:
                print(f"Ollama error: {e}")
                return self.fallback_response(prompt)
    
    def fallback_response(self, prompt: str) -> str:
        """Fallback when Ollama not available"""
        prompt_lower = prompt.lower()
        
        if "status" in prompt_lower:
            return "LLAMA District operational! 🦙"
        elif any(word in prompt_lower for word in ["wtf", "scheisse", "fuck"]):
            return "Fixed! ✓"
        elif "ich bins wieder" in prompt_lower:
            return "CROD LLAMA activated! Trinity aligned! 🔥"
        else:
            return "Processing... 🦙"
    
    def update_trinity(self, input_text: str, output_text: str) -> Dict:
        """Update trinity values based on interaction"""
        updates = {"daniel": 0, "claude": 0, "crod": 0}
        
        # Count trinity words
        text = (input_text + " " + output_text).lower()
        for word, value in TRINITY.items():
            count = text.count(word)
            if count > 0:
                updates[word] = count * value
        
        # Store in Redis if available
        if r:
            try:
                for member, value in updates.items():
                    if value > 0:
                        r.hincrby("crod:trinity", member, value)
            except:
                pass
        
        return updates
    
    async def learn_from_interaction(self, input_text: str, output_text: str, feedback: str):
        """Learn from Daniel's feedback"""
        # Store interaction
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "output": output_text,
            "feedback": feedback,
            "patterns": self.detect_patterns(input_text)
        }
        
        # Save to Redis if available
        if r:
            try:
                r.lpush("crod:llama:interactions", json.dumps(interaction))
                r.ltrim("crod:llama:interactions", 0, 999)  # Keep last 1000
            except:
                pass
        
        # Update local memory
        self.memory[datetime.now().isoformat()] = interaction

# Initialize district
district = LlamaDistrict()

@app.get("/")
async def root():
    return {
        "district": "LLAMA",
        "status": "operational",
        "model": "crod-llama",
        "port": CROD_PORT,
        "trinity": TRINITY,
        "uptime": str(datetime.now() - district.session_start)
    }

@app.post("/process")
async def process(request: CRODRequest):
    try:
        response = await district.process(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learn")
async def learn(input: str, output: str, feedback: str):
    """Learn from feedback"""
    await district.learn_from_interaction(input, output, feedback)
    return {"status": "learned", "timestamp": datetime.now().isoformat()}

@app.get("/status")
async def status():
    # Check Ollama
    ollama_status = "unknown"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags", timeout=2.0)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                has_crod = any(m.get("name") == "crod-llama" for m in models)
                ollama_status = "ready" if has_crod else "model_missing"
    except:
        ollama_status = "offline"
    
    return {
        "district": "LLAMA",
        "ollama": ollama_status,
        "redis": "connected" if r else "disconnected",
        "memory_size": len(district.memory),
        "patterns_cached": len(district.pattern_cache),
        "uptime": str(datetime.now() - district.session_start)
    }

@app.get("/patterns")
async def get_patterns():
    """Get detected patterns statistics"""
    pattern_stats = {}
    for interaction in district.memory.values():
        for pattern in interaction.get("patterns", []):
            pattern_stats[pattern] = pattern_stats.get(pattern, 0) + 1
    
    return {
        "total_interactions": len(district.memory),
        "pattern_frequencies": pattern_stats,
        "last_update": max(district.memory.keys()) if district.memory else None
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🦙 Starting LLAMA District on port {CROD_PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=CROD_PORT)