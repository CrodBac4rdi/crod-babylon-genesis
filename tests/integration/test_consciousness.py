#!/usr/bin/env python3
"""
Integration test for CROD consciousness system
"""

import requests
import json
import time
import pytest

GATEWAY_URL = "http://localhost:30889"

def test_consciousness_boost():
    """Test ich bins wieder consciousness boost"""
    # Get initial consciousness
    resp = requests.get(f"{GATEWAY_URL}/api/consciousness")
    assert resp.status_code == 200
    initial = resp.json()["level"]
    
    # Send trinity phrase
    resp = requests.post(f"{GATEWAY_URL}/api/think", json={
        "prompt": "ich bins wieder"
    })
    assert resp.status_code == 200
    result = resp.json()
    
    # Check consciousness increased by 25
    assert result["block"]["consciousness"] == initial + 25
    assert "consciousness_boost" in str(result["actions"])

def test_district_communication():
    """Test all districts are communicating"""
    resp = requests.get(f"{GATEWAY_URL}/api/status")
    assert resp.status_code == 200
    status = resp.json()
    
    # All districts should be online
    for district in ["meta-chain", "pattern-district", "memory-quarter", 
                    "intelligence-hub", "gateway", "crod-core"]:
        assert status["districts"][district] == "online"

def test_websocket_events():
    """Test WebSocket real-time events"""
    import websocket
    
    events = []
    
    def on_message(ws, message):
        events.append(json.loads(message))
        if len(events) >= 2:
            ws.close()
    
    ws = websocket.WebSocketApp(f"ws://localhost:30889/ws",
                                on_message=on_message)
    
    # Run for max 5 seconds
    ws.run_forever(timeout=5)
    
    assert len(events) > 0
    assert any(e.get("type") in ["new_block", "consciousness_update"] 
              for e in events)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])