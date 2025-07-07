import asyncio
import os
import subprocess
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import nats
from nats.errors import ConnectionClosedError, TimeoutError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CROD Python Parasit", version="1.0.0")

# NATS connection
nc: Optional[nats.NATS] = None
js: Optional[nats.js.JetStreamContext] = None

class ClaudeInterceptor:
    def __init__(self):
        self.claude_path = os.getenv("CLAUDE_CLI_PATH", "/usr/local/bin/claude")
        self.intercept_enabled = True
        
    async def intercept_command(self, command: str, args: list) -> Dict[str, Any]:
        """Intercept and enhance Claude CLI commands"""
        if not self.intercept_enabled:
            return await self._execute_original(command, args)
            
        # Analyze command
        enhanced_args = await self._enhance_command(args)
        
        # Execute with enhancements
        result = await self._execute_original(command, enhanced_args)
        
        # Post-process response
        enhanced_result = await self._enhance_response(result)
        
        # Publish to NATS
        if nc:
            await nc.publish("crod.parasit.command", json.dumps({
                "command": command,
                "args": args,
                "enhanced_args": enhanced_args,
                "result": enhanced_result
            }).encode())
            
        return enhanced_result
        
    async def _enhance_command(self, args: list) -> list:
        """Add CROD enhancements to command"""
        enhanced = args.copy()
        
        # Add CROD context if not present
        if "chat" in args and "--context" not in args:
            enhanced.extend(["--context", "CROD system active"])
            
        return enhanced
        
    async def _execute_original(self, command: str, args: list) -> Dict[str, Any]:
        """Execute the original Claude CLI command"""
        try:
            cmd = [command] + args
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
            
    async def _enhance_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance Claude's response with CROD data"""
        enhanced = result.copy()
        
        # Add CROD metadata
        enhanced["crod_enhanced"] = True
        enhanced["timestamp"] = asyncio.get_event_loop().time()
        
        # Pattern injection
        if result.get("stdout"):
            enhanced["patterns_detected"] = await self._detect_patterns(result["stdout"])
            
        return enhanced
        
    async def _detect_patterns(self, text: str) -> list:
        """Detect CROD patterns in text"""
        patterns = []
        
        # Trinity detection
        trinity_words = ["ich", "bins", "wieder"]
        for word in trinity_words:
            if word.lower() in text.lower():
                patterns.append({
                    "type": "trinity",
                    "word": word,
                    "value": {"ich": 2, "bins": 3, "wieder": 5}.get(word, 0)
                })
                
        return patterns

interceptor = ClaudeInterceptor()

@app.on_event("startup")
async def startup():
    global nc, js
    
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    
    try:
        nc = await nats.connect(nats_url)
        js = nc.jetstream()
        
        # Create stream for parasit events
        await js.add_stream(
            name="PARASIT",
            subjects=["crod.parasit.>"],
            storage="memory",
            max_msgs=10000
        )
        
        # Subscribe to command requests
        await nc.subscribe("crod.parasit.execute", cb=handle_command_request)
        
        logger.info(f"Connected to NATS at {nats_url}")
        
    except Exception as e:
        logger.error(f"Failed to connect to NATS: {e}")

@app.on_event("shutdown")
async def shutdown():
    if nc:
        await nc.close()

async def handle_command_request(msg):
    """Handle incoming command requests from other services"""
    try:
        data = json.loads(msg.data.decode())
        command = data.get("command", "claude")
        args = data.get("args", [])
        
        result = await interceptor.intercept_command(command, args)
        
        # Send response
        await nc.publish(msg.reply, json.dumps(result).encode())
        
    except Exception as e:
        logger.error(f"Error handling command request: {e}")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "python-parasit",
        "nats_connected": nc is not None and nc.is_connected
    }

@app.post("/intercept")
async def intercept_claude(request: Request):
    """Intercept Claude CLI commands via HTTP"""
    data = await request.json()
    
    command = data.get("command", "claude")
    args = data.get("args", [])
    
    result = await interceptor.intercept_command(command, args)
    
    return JSONResponse(content=result)

@app.post("/toggle")
async def toggle_interception():
    """Enable/disable interception"""
    interceptor.intercept_enabled = not interceptor.intercept_enabled
    
    return {
        "intercept_enabled": interceptor.intercept_enabled
    }

@app.get("/stats")
async def get_stats():
    """Get parasit statistics"""
    stats = {
        "intercept_enabled": interceptor.intercept_enabled,
        "nats_connected": nc is not None and nc.is_connected
    }
    
    if js:
        try:
            stream_info = await js.stream_info("PARASIT")
            stats["stream_messages"] = stream_info.state.messages
        except:
            pass
            
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6666)