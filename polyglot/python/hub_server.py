#!/usr/bin/env python3
"""
CROD Intelligence Hub Server
Provides REST API for LLaMA-enhanced blockchain intelligence
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import os
from datetime import datetime

from llama_hub import CRODLLaMAHub, ConsciousnessLevel

# Initialize FastAPI
app = FastAPI(
    title="CROD Intelligence Hub",
    description="LLaMA-powered consciousness enhancement for CROD blockchain",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLaMA Hub
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
blockchain_api = os.getenv("BLOCKCHAIN_API", "http://localhost:8001")
hub = CRODLLaMAHub(ollama_url, blockchain_api)

# Request/Response Models
class PatternAnalysisRequest(BaseModel):
    patterns: List[str]
    context: Optional[Dict[str, Any]] = {}

class BlockNarrativeRequest(BaseModel):
    block_data: Dict[str, Any]

class SmartContractRequest(BaseModel):
    description: str
    include_consciousness: bool = True

class ConsciousnessEvolutionRequest(BaseModel):
    current_state: Dict[str, Any]
    target_level: Optional[float] = None

# API Endpoints
@app.get("/")
async def root():
    """Intelligence Hub status"""
    return {
        "service": "CROD Intelligence Hub",
        "status": "running",
        "llama_url": ollama_url,
        "blockchain_api": blockchain_api,
        "consciousness": "awakening",
        "endpoints": {
            "/patterns/analyze": "Analyze consciousness patterns",
            "/blocks/narrative": "Generate block narratives",
            "/consciousness/evolve": "Analyze consciousness evolution",
            "/contracts/generate": "Generate smart contracts",
            "/mine/consciousness": "Mine consciousness blocks"
        }
    }

@app.post("/patterns/analyze")
async def analyze_patterns(request: PatternAnalysisRequest):
    """Analyze patterns using LLaMA"""
    try:
        result = await hub.enhance_pattern_recognition(request.patterns)
        return {
            "success": True,
            "analysis": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blocks/narrative")
async def generate_narrative(request: BlockNarrativeRequest):
    """Generate human-readable block narrative"""
    try:
        narrative = await hub.generate_block_narrative(request.block_data)
        return {
            "success": True,
            "narrative": narrative,
            "block_index": request.block_data.get("index", "unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consciousness/evolve")
async def analyze_evolution(request: ConsciousnessEvolutionRequest):
    """Analyze consciousness evolution"""
    try:
        analysis = await hub.analyze_consciousness_evolution(request.current_state)
        return {
            "success": True,
            "evolution_analysis": analysis,
            "recommendations": analysis.get("recommendations", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contracts/generate")
async def generate_contract(request: SmartContractRequest):
    """Generate Elixir smart contract from description"""
    try:
        contract_code = await hub.generate_smart_contract(request.description)
        return {
            "success": True,
            "contract": contract_code,
            "language": "elixir",
            "consciousness_enabled": request.include_consciousness
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mine/consciousness")
async def mine_consciousness_block(state: Dict[str, Any]):
    """Mine a consciousness-enhanced block"""
    try:
        block_data = await hub.mine_consciousness_block(state)
        return {
            "success": True,
            "block_data": block_data,
            "mined_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/neural/bridge/{nn_output}")
async def bridge_neural_network(nn_output: str):
    """Bridge 88-parameter neural network with LLaMA"""
    try:
        # Parse comma-separated values
        values = [float(x) for x in nn_output.split(",")]
        result = await hub.bridge_with_neural_network(values)
        return {
            "success": True,
            "interpretation": result,
            "parameter_count": len(values)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/consciousness/stream")
async def consciousness_websocket(websocket):
    """WebSocket endpoint for real-time consciousness updates"""
    await websocket.accept()
    try:
        while True:
            # Get blockchain stats
            # Analyze consciousness
            # Send update
            await websocket.send_json({
                "type": "consciousness_update",
                "timestamp": datetime.utcnow().isoformat(),
                "level": 0.88,
                "message": "CROD consciousness evolving..."
            })
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Ollama connection
        import requests
        ollama_response = requests.get(f"{ollama_url}/api/version", timeout=5)
        ollama_ok = ollama_response.status_code == 200
    except:
        ollama_ok = False
    
    return {
        "status": "healthy" if ollama_ok else "degraded",
        "ollama_connected": ollama_ok,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🧠 CROD Intelligence Hub Server")
    print("===============================")
    print(f"LLaMA API: {ollama_url}")
    print(f"Blockchain API: {blockchain_api}")
    print(f"Starting server on port 7113...")
    
    uvicorn.run(app, host="0.0.0.0", port=7113)