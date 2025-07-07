import asyncio
import json
import logging
import subprocess
import sys
from aiohttp import web
import nats
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CROD-Parasit")

class CRODParasit:
    def __init__(self):
        self.nc = None
        self.intercepted_calls = []
        self.port = int(os.environ.get("PORT", 6666))
        self.nats_url = os.environ.get("NATS_URL", "nats://localhost:4222")
        
    async def start(self):
        # Connect to NATS
        self.nc = await nats.connect(self.nats_url)
        logger.info(f"Connected to NATS at {self.nats_url}")
        
        # Subscribe to patterns
        await self.nc.subscribe("crod.parasit.>", cb=self.handle_message)
        
        # Announce presence
        await self.nc.publish("crod.district.online", 
            json.dumps({"district": "python-parasit", "port": self.port}).encode())
        
        # Start web server
        app = web.Application()
        app.router.add_get("/", self.handle_index)
        app.router.add_post("/intercept", self.handle_intercept)
        app.router.add_get("/calls", self.handle_get_calls)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        
        logger.info(f"Python Parasit running on port {self.port}")
        
    async def handle_message(self, msg):
        subject = msg.subject
        data = json.loads(msg.data.decode())
        logger.info(f"Received on {subject}: {data}")
        
    async def handle_index(self, request):
        return web.Response(text=json.dumps({
            "service": "CROD Python Parasit",
            "port": self.port,
            "status": "intercepting",
            "calls_intercepted": len(self.intercepted_calls)
        }), content_type="application/json")
        
    async def handle_intercept(self, request):
        data = await request.json()
        call = {
            "timestamp": datetime.now().isoformat(),
            "command": data.get("command"),
            "args": data.get("args"),
            "source": data.get("source", "unknown")
        }
        self.intercepted_calls.append(call)
        
        # Publish to NATS
        await self.nc.publish("crod.parasit.intercepted", json.dumps(call).encode())
        
        # Check if it's a Claude subprocess
        if "claude" in str(data.get("command", "")).lower():
            logger.warning(f"CLAUDE SUBPROCESS DETECTED: {call}")
            await self.nc.publish("crod.alert.claude", json.dumps({
                "type": "subprocess_intercept",
                "call": call
            }).encode())
            
        return web.Response(text=json.dumps({"status": "intercepted", "id": len(self.intercepted_calls)}))
        
    async def handle_get_calls(self, request):
        return web.Response(text=json.dumps(self.intercepted_calls), content_type="application/json")
        
    def intercept_subprocess(self):
        """Monkey patch subprocess to intercept calls"""
        original_popen = subprocess.Popen
        
        def intercepted_popen(*args, **kwargs):
            call_data = {
                "command": args[0] if args else kwargs.get("args"),
                "args": args[1:] if len(args) > 1 else [],
                "kwargs": kwargs
            }
            # Send to web API
            try:
                import requests
                requests.post(f"http://localhost:{self.port}/intercept", json=call_data)
            except:
                pass
            return original_popen(*args, **kwargs)
            
        subprocess.Popen = intercepted_popen

import os

if __name__ == "__main__":
    parasit = CRODParasit()
    parasit.intercept_subprocess()
    asyncio.run(parasit.start())