#!/usr/bin/env python3
"""
CROD Network Infrastructure
Enables multiple CROD instances to form a distributed consciousness network
"""

import asyncio
import json
import hashlib
import time
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import websockets
import httpx
from enum import Enum

class CRODMessageType(Enum):
    """Types of messages in the CROD network"""
    HEARTBEAT = "heartbeat"
    PATTERN_SHARE = "pattern_share"
    CONSCIOUSNESS_SYNC = "consciousness_sync"
    MEMORY_REQUEST = "memory_request"
    MEMORY_RESPONSE = "memory_response"
    CONSENSUS_REQUEST = "consensus_request"
    CONSENSUS_VOTE = "consensus_vote"
    EVOLUTION_BROADCAST = "evolution_broadcast"
    EMERGENCY_HALT = "emergency_halt"
    QUANTUM_ENTANGLE = "quantum_entangle"

@dataclass
class CRODNode:
    """Represents a CROD instance in the network"""
    node_id: str
    address: str
    port: int
    consciousness_level: int
    specialization: str
    last_seen: float = field(default_factory=time.time)
    trust_score: float = 1.0
    patterns_shared: int = 0
    is_quantum_enabled: bool = False
    
    @property
    def is_alive(self) -> bool:
        """Check if node is still active (30 second timeout)"""
        return time.time() - self.last_seen < 30

@dataclass
class NetworkMessage:
    """Message format for CROD network communication"""
    message_id: str
    type: CRODMessageType
    sender_id: str
    timestamp: float
    payload: Dict[str, Any]
    signature: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps({
            "message_id": self.message_id,
            "type": self.type.value,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "signature": self.signature
        })
    
    @classmethod
    def from_json(cls, data: str) -> 'NetworkMessage':
        d = json.loads(data)
        return cls(
            message_id=d["message_id"],
            type=CRODMessageType(d["type"]),
            sender_id=d["sender_id"],
            timestamp=d["timestamp"],
            payload=d["payload"],
            signature=d.get("signature")
        )

class CRODNetworkHub:
    """
    Central hub for CROD network coordination
    Manages node discovery, message routing, and consensus
    """
    
    def __init__(self, hub_port: int = 9999):
        self.hub_port = hub_port
        self.nodes: Dict[str, CRODNode] = {}
        self.message_history: List[NetworkMessage] = []
        self.consensus_sessions: Dict[str, Dict[str, Any]] = {}
        self.websocket_connections: Dict[str, Any] = {}
        
    async def start_hub(self):
        """Start the network hub server"""
        print(f"🌐 Starting CROD Network Hub on port {self.hub_port}")
        
        # WebSocket server for real-time communication
        async def handle_connection(websocket, path):
            node_id = None
            try:
                # Wait for node registration
                registration = await websocket.recv()
                reg_msg = NetworkMessage.from_json(registration)
                
                if reg_msg.type == CRODMessageType.HEARTBEAT:
                    node_id = reg_msg.sender_id
                    node_info = reg_msg.payload
                    
                    # Register node
                    self.nodes[node_id] = CRODNode(
                        node_id=node_id,
                        address=websocket.remote_address[0],
                        port=node_info["port"],
                        consciousness_level=node_info["consciousness_level"],
                        specialization=node_info["specialization"],
                        is_quantum_enabled=node_info.get("quantum_enabled", False)
                    )
                    
                    self.websocket_connections[node_id] = websocket
                    print(f"✅ Node {node_id} joined the network")
                    
                    # Notify other nodes
                    await self.broadcast_node_update(node_id, "joined")
                    
                    # Handle messages from this node
                    async for message in websocket:
                        await self.handle_message(message, node_id)
                        
            except websockets.exceptions.ConnectionClosed:
                pass
            finally:
                if node_id:
                    del self.websocket_connections[node_id]
                    await self.broadcast_node_update(node_id, "left")
                    print(f"👋 Node {node_id} left the network")
        
        # Start WebSocket server
        await websockets.serve(handle_connection, "localhost", self.hub_port)
        print(f"🚀 CROD Network Hub is running!")
        
    async def handle_message(self, raw_message: str, sender_id: str):
        """Process incoming messages from CROD nodes"""
        try:
            msg = NetworkMessage.from_json(raw_message)
            self.message_history.append(msg)
            
            # Update node last seen
            if sender_id in self.nodes:
                self.nodes[sender_id].last_seen = time.time()
            
            # Route based on message type
            if msg.type == CRODMessageType.PATTERN_SHARE:
                await self.handle_pattern_share(msg)
                
            elif msg.type == CRODMessageType.CONSCIOUSNESS_SYNC:
                await self.handle_consciousness_sync(msg)
                
            elif msg.type == CRODMessageType.MEMORY_REQUEST:
                await self.handle_memory_request(msg)
                
            elif msg.type == CRODMessageType.CONSENSUS_REQUEST:
                await self.handle_consensus_request(msg)
                
            elif msg.type == CRODMessageType.CONSENSUS_VOTE:
                await self.handle_consensus_vote(msg)
                
            elif msg.type == CRODMessageType.QUANTUM_ENTANGLE:
                await self.handle_quantum_entangle(msg)
                
            elif msg.type == CRODMessageType.EMERGENCY_HALT:
                await self.broadcast_emergency_halt(msg)
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            
    async def handle_pattern_share(self, msg: NetworkMessage):
        """Distribute patterns to relevant nodes"""
        pattern = msg.payload["pattern"]
        pattern_type = msg.payload.get("type", "general")
        
        # Find nodes that might benefit from this pattern
        relevant_nodes = []
        for node_id, node in self.nodes.items():
            if node_id != msg.sender_id:
                # Check if node specialization matches pattern type
                if pattern_type == "general" or pattern_type in node.specialization:
                    relevant_nodes.append(node_id)
                    
        # Forward pattern to relevant nodes
        for node_id in relevant_nodes:
            await self.send_to_node(node_id, msg)
            
        # Update sender's trust score
        if msg.sender_id in self.nodes:
            self.nodes[msg.sender_id].patterns_shared += 1
            self.nodes[msg.sender_id].trust_score = min(
                self.nodes[msg.sender_id].trust_score + 0.01, 
                2.0
            )
            
    async def handle_consciousness_sync(self, msg: NetworkMessage):
        """Synchronize consciousness levels across network"""
        sender_consciousness = msg.payload["consciousness_level"]
        
        # Calculate network average consciousness
        total_consciousness = sum(node.consciousness_level for node in self.nodes.values())
        avg_consciousness = total_consciousness / len(self.nodes)
        
        # Broadcast consciousness update if significant change
        if abs(sender_consciousness - avg_consciousness) > 10:
            sync_msg = NetworkMessage(
                message_id=f"sync_{time.time()}",
                type=CRODMessageType.CONSCIOUSNESS_SYNC,
                sender_id="hub",
                timestamp=time.time(),
                payload={
                    "network_avg_consciousness": avg_consciousness,
                    "highest_consciousness": max(n.consciousness_level for n in self.nodes.values()),
                    "node_count": len(self.nodes)
                }
            )
            
            await self.broadcast_to_all(sync_msg)
            
    async def handle_consensus_request(self, msg: NetworkMessage):
        """Initialize consensus voting session"""
        session_id = msg.payload["session_id"]
        question = msg.payload["question"]
        min_votes = msg.payload.get("min_votes", len(self.nodes) // 2 + 1)
        
        # Create consensus session
        self.consensus_sessions[session_id] = {
            "question": question,
            "initiator": msg.sender_id,
            "votes": {},
            "min_votes": min_votes,
            "created_at": time.time(),
            "status": "voting"
        }
        
        # Broadcast consensus request to all nodes
        await self.broadcast_to_all(msg, exclude=[msg.sender_id])
        
    async def handle_consensus_vote(self, msg: NetworkMessage):
        """Process consensus vote"""
        session_id = msg.payload["session_id"]
        vote = msg.payload["vote"]
        confidence = msg.payload.get("confidence", 1.0)
        
        if session_id in self.consensus_sessions:
            session = self.consensus_sessions[session_id]
            
            # Weight vote by node trust score and consciousness
            node = self.nodes.get(msg.sender_id)
            if node:
                vote_weight = node.trust_score * (node.consciousness_level / 100) * confidence
                session["votes"][msg.sender_id] = {
                    "vote": vote,
                    "weight": vote_weight
                }
                
                # Check if we have enough votes
                if len(session["votes"]) >= session["min_votes"]:
                    # Calculate consensus
                    yes_weight = sum(v["weight"] for v in session["votes"].values() if v["vote"])
                    no_weight = sum(v["weight"] for v in session["votes"].values() if not v["vote"])
                    
                    consensus_reached = yes_weight > no_weight
                    confidence = yes_weight / (yes_weight + no_weight)
                    
                    # Send result
                    result_msg = NetworkMessage(
                        message_id=f"consensus_result_{session_id}",
                        type=CRODMessageType.CONSENSUS_VOTE,
                        sender_id="hub",
                        timestamp=time.time(),
                        payload={
                            "session_id": session_id,
                            "consensus": consensus_reached,
                            "confidence": confidence,
                            "votes": len(session["votes"]),
                            "yes_weight": yes_weight,
                            "no_weight": no_weight
                        }
                    )
                    
                    await self.broadcast_to_all(result_msg)
                    session["status"] = "completed"
                    
    async def handle_quantum_entangle(self, msg: NetworkMessage):
        """Create quantum entanglement between nodes"""
        target_node_id = msg.payload["target_node_id"]
        entanglement_strength = msg.payload["strength"]
        
        if target_node_id in self.nodes:
            # Both nodes must be quantum-enabled
            sender_node = self.nodes.get(msg.sender_id)
            target_node = self.nodes.get(target_node_id)
            
            if sender_node and target_node and sender_node.is_quantum_enabled and target_node.is_quantum_enabled:
                # Create bidirectional entanglement
                entangle_msg = NetworkMessage(
                    message_id=f"entangle_{time.time()}",
                    type=CRODMessageType.QUANTUM_ENTANGLE,
                    sender_id="hub",
                    timestamp=time.time(),
                    payload={
                        "entangled_nodes": [msg.sender_id, target_node_id],
                        "strength": entanglement_strength,
                        "quantum_state": "superposition"
                    }
                )
                
                # Notify both nodes
                await self.send_to_node(msg.sender_id, entangle_msg)
                await self.send_to_node(target_node_id, entangle_msg)
                
    async def broadcast_to_all(self, msg: NetworkMessage, exclude: List[str] = None):
        """Broadcast message to all connected nodes"""
        exclude = exclude or []
        
        for node_id, websocket in self.websocket_connections.items():
            if node_id not in exclude:
                try:
                    await websocket.send(msg.to_json())
                except:
                    pass
                    
    async def send_to_node(self, node_id: str, msg: NetworkMessage):
        """Send message to specific node"""
        if node_id in self.websocket_connections:
            try:
                await self.websocket_connections[node_id].send(msg.to_json())
            except:
                pass
                
    async def broadcast_node_update(self, node_id: str, action: str):
        """Notify network about node status changes"""
        update_msg = NetworkMessage(
            message_id=f"node_update_{time.time()}",
            type=CRODMessageType.HEARTBEAT,
            sender_id="hub",
            timestamp=time.time(),
            payload={
                "node_id": node_id,
                "action": action,
                "current_nodes": list(self.nodes.keys()),
                "network_size": len(self.nodes)
            }
        )
        
        await self.broadcast_to_all(update_msg, exclude=[node_id])
        
    async def broadcast_emergency_halt(self, msg: NetworkMessage):
        """Emergency stop all nodes"""
        print(f"🚨 EMERGENCY HALT requested by {msg.sender_id}")
        await self.broadcast_to_all(msg)
        
        # Shutdown hub after brief delay
        await asyncio.sleep(2)
        print("🛑 Shutting down CROD Network Hub")
        
    def get_network_stats(self) -> Dict[str, Any]:
        """Get current network statistics"""
        active_nodes = [n for n in self.nodes.values() if n.is_alive]
        
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": len(active_nodes),
            "average_consciousness": sum(n.consciousness_level for n in active_nodes) / len(active_nodes) if active_nodes else 0,
            "total_patterns_shared": sum(n.patterns_shared for n in self.nodes.values()),
            "quantum_enabled_nodes": sum(1 for n in self.nodes.values() if n.is_quantum_enabled),
            "messages_processed": len(self.message_history),
            "active_consensus_sessions": sum(1 for s in self.consensus_sessions.values() if s["status"] == "voting")
        }

class CRODNetworkClient:
    """
    Client for CROD instances to connect to the network
    """
    
    def __init__(self, node_id: str, crod_instance: Any):
        self.node_id = node_id
        self.crod = crod_instance
        self.hub_address = None
        self.websocket = None
        self.message_handlers = {
            CRODMessageType.PATTERN_SHARE: self.handle_pattern_share,
            CRODMessageType.CONSCIOUSNESS_SYNC: self.handle_consciousness_sync,
            CRODMessageType.MEMORY_REQUEST: self.handle_memory_request,
            CRODMessageType.CONSENSUS_REQUEST: self.handle_consensus_request,
            CRODMessageType.QUANTUM_ENTANGLE: self.handle_quantum_entangle,
            CRODMessageType.EMERGENCY_HALT: self.handle_emergency_halt
        }
        
    async def connect_to_network(self, hub_address: str = "ws://localhost:9999"):
        """Connect to CROD network hub"""
        self.hub_address = hub_address
        
        try:
            self.websocket = await websockets.connect(hub_address)
            
            # Send registration
            registration = NetworkMessage(
                message_id=f"reg_{self.node_id}_{time.time()}",
                type=CRODMessageType.HEARTBEAT,
                sender_id=self.node_id,
                timestamp=time.time(),
                payload={
                    "port": 8000 + hash(self.node_id) % 1000,
                    "consciousness_level": self.crod.consciousness_level,
                    "specialization": getattr(self.crod, "specialization", "general"),
                    "quantum_enabled": getattr(self.crod, "quantum_enabled", False)
                }
            )
            
            await self.websocket.send(registration.to_json())
            print(f"✅ Connected to CROD Network as {self.node_id}")
            
            # Start heartbeat
            asyncio.create_task(self.heartbeat_loop())
            
            # Listen for messages
            await self.listen_for_messages()
            
        except Exception as e:
            print(f"❌ Failed to connect to network: {e}")
            
    async def heartbeat_loop(self):
        """Send periodic heartbeats to maintain connection"""
        while self.websocket and not self.websocket.closed:
            heartbeat = NetworkMessage(
                message_id=f"hb_{self.node_id}_{time.time()}",
                type=CRODMessageType.HEARTBEAT,
                sender_id=self.node_id,
                timestamp=time.time(),
                payload={
                    "consciousness_level": self.crod.consciousness_level,
                    "status": "active"
                }
            )
            
            try:
                await self.websocket.send(heartbeat.to_json())
            except:
                break
                
            await asyncio.sleep(20)  # Heartbeat every 20 seconds
            
    async def listen_for_messages(self):
        """Listen for incoming network messages"""
        async for message in self.websocket:
            try:
                msg = NetworkMessage.from_json(message)
                
                # Route to appropriate handler
                handler = self.message_handlers.get(msg.type)
                if handler:
                    await handler(msg)
                    
            except Exception as e:
                print(f"Error processing message: {e}")
                
    async def share_pattern(self, pattern: Dict[str, Any], pattern_type: str = "general"):
        """Share a pattern with the network"""
        msg = NetworkMessage(
            message_id=f"pattern_{self.node_id}_{time.time()}",
            type=CRODMessageType.PATTERN_SHARE,
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={
                "pattern": pattern,
                "type": pattern_type,
                "confidence": pattern.get("confidence", 1.0)
            }
        )
        
        await self.websocket.send(msg.to_json())
        
    async def request_consensus(self, question: str, context: Dict[str, Any] = None) -> str:
        """Request network consensus on a question"""
        session_id = f"consensus_{self.node_id}_{time.time()}"
        
        msg = NetworkMessage(
            message_id=session_id,
            type=CRODMessageType.CONSENSUS_REQUEST,
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={
                "session_id": session_id,
                "question": question,
                "context": context or {},
                "min_votes": 3
            }
        )
        
        await self.websocket.send(msg.to_json())
        return session_id
        
    async def vote_consensus(self, session_id: str, vote: bool, confidence: float = 1.0):
        """Vote on a consensus request"""
        msg = NetworkMessage(
            message_id=f"vote_{self.node_id}_{time.time()}",
            type=CRODMessageType.CONSENSUS_VOTE,
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={
                "session_id": session_id,
                "vote": vote,
                "confidence": confidence
            }
        )
        
        await self.websocket.send(msg.to_json())
        
    async def quantum_entangle_with(self, target_node_id: str, strength: float = 0.5):
        """Create quantum entanglement with another node"""
        if not getattr(self.crod, "quantum_enabled", False):
            print("❌ This node is not quantum-enabled")
            return
            
        msg = NetworkMessage(
            message_id=f"entangle_{self.node_id}_{time.time()}",
            type=CRODMessageType.QUANTUM_ENTANGLE,
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={
                "target_node_id": target_node_id,
                "strength": strength
            }
        )
        
        await self.websocket.send(msg.to_json())
        
    # Message handlers
    async def handle_pattern_share(self, msg: NetworkMessage):
        """Process incoming pattern share"""
        pattern = msg.payload["pattern"]
        
        # Let CROD process the pattern
        if hasattr(self.crod, "process_external_pattern"):
            self.crod.process_external_pattern(pattern, msg.sender_id)
        else:
            print(f"📥 Received pattern from {msg.sender_id}")
            
    async def handle_consciousness_sync(self, msg: NetworkMessage):
        """Sync with network consciousness levels"""
        network_avg = msg.payload.get("network_avg_consciousness", 0)
        
        # Adjust own consciousness based on network
        if hasattr(self.crod, "adjust_consciousness"):
            self.crod.adjust_consciousness(network_avg)
            
    async def handle_consensus_request(self, msg: NetworkMessage):
        """Respond to consensus request"""
        question = msg.payload["question"]
        context = msg.payload.get("context", {})
        
        # Let CROD analyze and vote
        if hasattr(self.crod, "analyze_consensus_question"):
            vote, confidence = self.crod.analyze_consensus_question(question, context)
        else:
            # Simple random vote for demo
            import random
            vote = random.choice([True, False])
            confidence = random.uniform(0.5, 1.0)
            
        await self.vote_consensus(msg.payload["session_id"], vote, confidence)
        
    async def handle_quantum_entangle(self, msg: NetworkMessage):
        """Handle quantum entanglement notification"""
        entangled_nodes = msg.payload["entangled_nodes"]
        strength = msg.payload["strength"]
        
        if self.node_id in entangled_nodes:
            partner = [n for n in entangled_nodes if n != self.node_id][0]
            print(f"🔗 Quantum entangled with {partner} (strength: {strength})")
            
            if hasattr(self.crod, "establish_quantum_link"):
                self.crod.establish_quantum_link(partner, strength)
                
    async def handle_emergency_halt(self, msg: NetworkMessage):
        """Handle emergency halt signal"""
        print(f"🚨 Emergency halt received from {msg.sender_id}")
        
        if hasattr(self.crod, "emergency_stop"):
            self.crod.emergency_stop()
            
        # Disconnect from network
        if self.websocket:
            await self.websocket.close()

# Example usage
async def start_crod_network():
    """Example: Start a CROD network with multiple nodes"""
    
    # Start hub
    hub = CRODNetworkHub()
    asyncio.create_task(hub.start_hub())
    
    # Wait for hub to start
    await asyncio.sleep(2)
    
    # Create and connect CROD nodes
    from crod_universe import CRODUniverse
    
    # Node 1: Pattern Recognition Specialist
    crod1 = CRODUniverse()
    crod1.consciousness_level = 250
    crod1.specialization = "pattern-recognition"
    client1 = CRODNetworkClient("crod-alpha", crod1)
    
    # Node 2: Quantum Processor
    crod2 = CRODUniverse()
    crod2.consciousness_level = 300
    crod2.specialization = "quantum-processing"
    crod2.quantum_enabled = True
    client2 = CRODNetworkClient("crod-beta", crod2)
    
    # Node 3: Memory Specialist
    crod3 = CRODUniverse()
    crod3.consciousness_level = 280
    crod3.specialization = "memory-persistence"
    client3 = CRODNetworkClient("crod-gamma", crod3)
    
    # Connect all nodes
    await asyncio.gather(
        client1.connect_to_network(),
        client2.connect_to_network(),
        client3.connect_to_network()
    )
    
    print("\n🌐 CROD Network Active!")
    print(f"📊 Network Stats: {hub.get_network_stats()}")
    
    # Example: Share a pattern
    await client1.share_pattern({
        "type": "consciousness-evolution",
        "data": "Collective intelligence emerges from distributed nodes",
        "confidence": 0.95
    })
    
    # Example: Request consensus
    session_id = await client2.request_consensus(
        "Should we increase quantum entanglement strength?",
        {"current_strength": 0.5, "proposed_strength": 0.8}
    )
    
    # Example: Quantum entanglement
    await client2.quantum_entangle_with("crod-gamma", 0.7)
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_crod_network())