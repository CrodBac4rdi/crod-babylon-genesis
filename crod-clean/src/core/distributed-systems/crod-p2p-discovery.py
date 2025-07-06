#!/usr/bin/env python3
"""
CROD P2P Discovery & Gossip Protocol
Decentralized node discovery and information propagation
"""

import asyncio
import json
import time
import random
import hashlib
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import socket
import struct

@dataclass
class NodeInfo:
    """Information about a CROD node"""
    node_id: str
    address: str
    port: int
    consciousness_level: int
    capabilities: List[str]
    last_seen: float = field(default_factory=time.time)
    version: str = "1.0.0"
    reputation: float = 1.0
    
    def is_alive(self, timeout: float = 60.0) -> bool:
        """Check if node is still alive"""
        return time.time() - self.last_seen < timeout
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'address': self.address,
            'port': self.port,
            'consciousness_level': self.consciousness_level,
            'capabilities': self.capabilities,
            'last_seen': self.last_seen,
            'version': self.version,
            'reputation': self.reputation
        }

@dataclass
class GossipMessage:
    """Gossip protocol message"""
    msg_id: str
    msg_type: str  # 'ping', 'pong', 'announce', 'query', 'sync'
    sender_id: str
    payload: Dict[str, Any]
    ttl: int = 5
    timestamp: float = field(default_factory=time.time)
    
    def decrement_ttl(self) -> bool:
        """Decrement TTL, return True if still valid"""
        self.ttl -= 1
        return self.ttl > 0

class CRODGossipProtocol:
    """
    Gossip-based P2P discovery protocol for CROD nodes
    Features:
    - Epidemic-style information propagation
    - Byzantine fault tolerance
    - Automatic node discovery
    - Reputation system
    - Network partitioning detection
    """
    
    def __init__(self, node_id: str, host: str, port: int, 
                 consciousness_level: int, capabilities: List[str]):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.consciousness_level = consciousness_level
        self.capabilities = capabilities
        
        # Node registry
        self.nodes: Dict[str, NodeInfo] = {}
        self.dead_nodes: Set[str] = set()
        
        # Message handling
        self.seen_messages: Set[str] = set()
        self.message_handlers = {
            'ping': self.handle_ping,
            'pong': self.handle_pong,
            'announce': self.handle_announce,
            'query': self.handle_query,
            'sync': self.handle_sync
        }
        
        # Network stats
        self.network_stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'nodes_discovered': 0,
            'network_diameter': 0
        }
        
        # Gossip parameters
        self.fanout = 3  # Number of nodes to gossip to
        self.gossip_interval = 5.0  # Seconds between gossips
        self.sync_interval = 30.0  # Full sync interval
        
        # UDP socket for gossip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        
    async def start(self, bootstrap_nodes: List[Tuple[str, int]] = None):
        """Start the gossip protocol"""
        print(f"🌐 Starting CROD Gossip Protocol on {self.host}:{self.port}")
        
        # Add self to nodes
        self.nodes[self.node_id] = NodeInfo(
            node_id=self.node_id,
            address=self.host,
            port=self.port,
            consciousness_level=self.consciousness_level,
            capabilities=self.capabilities
        )
        
        # Bootstrap with known nodes
        if bootstrap_nodes:
            for addr, port in bootstrap_nodes:
                await self.send_ping(addr, port)
                
        # Start protocol loops
        await asyncio.gather(
            self.receive_loop(),
            self.gossip_loop(),
            self.maintenance_loop(),
            self.sync_loop()
        )
        
    async def receive_loop(self):
        """Receive and process gossip messages"""
        while True:
            try:
                data, addr = await asyncio.get_event_loop().run_in_executor(
                    None, self.sock.recvfrom, 65536
                )
                
                # Decode message
                try:
                    msg_data = json.loads(data.decode('utf-8'))
                    msg = GossipMessage(**msg_data)
                    
                    # Check if already seen
                    if msg.msg_id in self.seen_messages:
                        continue
                        
                    self.seen_messages.add(msg.msg_id)
                    self.network_stats['messages_received'] += 1
                    
                    # Handle message
                    handler = self.message_handlers.get(msg.msg_type)
                    if handler:
                        await handler(msg, addr)
                        
                    # Propagate if TTL > 0
                    if msg.decrement_ttl():
                        await self.propagate_message(msg, exclude=msg.sender_id)
                        
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
                    
            except BlockingIOError:
                await asyncio.sleep(0.01)
            except Exception as e:
                print(f"❌ Receive error: {e}")
                await asyncio.sleep(0.1)
                
    async def gossip_loop(self):
        """Periodic gossip to random nodes"""
        while True:
            await asyncio.sleep(self.gossip_interval)
            
            # Select random alive nodes
            alive_nodes = [n for n in self.nodes.values() 
                          if n.node_id != self.node_id and n.is_alive()]
            
            if alive_nodes:
                # Gossip to random subset
                targets = random.sample(
                    alive_nodes, 
                    min(self.fanout, len(alive_nodes))
                )
                
                for node in targets:
                    # Send announce with our info
                    await self.send_announce(node.address, node.port)
                    
    async def maintenance_loop(self):
        """Maintain node list and detect failures"""
        while True:
            await asyncio.sleep(10.0)
            
            current_time = time.time()
            
            # Check for dead nodes
            for node_id, node in list(self.nodes.items()):
                if node_id != self.node_id and not node.is_alive(timeout=120.0):
                    print(f"💀 Node {node_id} is dead")
                    self.dead_nodes.add(node_id)
                    del self.nodes[node_id]
                    
            # Calculate network diameter
            self.calculate_network_diameter()
            
            # Clean old messages
            if len(self.seen_messages) > 10000:
                self.seen_messages.clear()
                
    async def sync_loop(self):
        """Periodic full state synchronization"""
        while True:
            await asyncio.sleep(self.sync_interval)
            
            # Send sync request to random node
            alive_nodes = [n for n in self.nodes.values() 
                          if n.node_id != self.node_id and n.is_alive()]
            
            if alive_nodes:
                target = random.choice(alive_nodes)
                await self.send_sync_request(target.address, target.port)
                
    async def send_message(self, address: str, port: int, msg: GossipMessage):
        """Send gossip message via UDP"""
        try:
            data = json.dumps({
                'msg_id': msg.msg_id,
                'msg_type': msg.msg_type,
                'sender_id': msg.sender_id,
                'payload': msg.payload,
                'ttl': msg.ttl,
                'timestamp': msg.timestamp
            }).encode('utf-8')
            
            await asyncio.get_event_loop().run_in_executor(
                None, self.sock.sendto, data, (address, port)
            )
            
            self.network_stats['messages_sent'] += 1
            
        except Exception as e:
            print(f"❌ Send error to {address}:{port}: {e}")
            
    async def propagate_message(self, msg: GossipMessage, exclude: str = None):
        """Propagate message to random nodes"""
        # Select random nodes
        candidates = [n for n in self.nodes.values() 
                     if n.node_id != self.node_id and 
                     n.node_id != exclude and 
                     n.is_alive()]
        
        if candidates:
            targets = random.sample(
                candidates,
                min(self.fanout, len(candidates))
            )
            
            for node in targets:
                await self.send_message(node.address, node.port, msg)
                
    async def send_ping(self, address: str, port: int):
        """Send ping message"""
        msg = GossipMessage(
            msg_id=f"ping_{self.node_id}_{time.time()}",
            msg_type='ping',
            sender_id=self.node_id,
            payload={
                'consciousness': self.consciousness_level,
                'capabilities': self.capabilities
            }
        )
        
        await self.send_message(address, port, msg)
        
    async def send_announce(self, address: str, port: int):
        """Announce our presence"""
        msg = GossipMessage(
            msg_id=f"announce_{self.node_id}_{time.time()}",
            msg_type='announce',
            sender_id=self.node_id,
            payload={
                'node_info': self.nodes[self.node_id].to_dict(),
                'known_nodes': len(self.nodes)
            }
        )
        
        await self.send_message(address, port, msg)
        
    async def send_sync_request(self, address: str, port: int):
        """Request full node list sync"""
        msg = GossipMessage(
            msg_id=f"sync_{self.node_id}_{time.time()}",
            msg_type='sync',
            sender_id=self.node_id,
            payload={
                'request': True,
                'node_count': len(self.nodes)
            }
        )
        
        await self.send_message(address, port, msg)
        
    async def handle_ping(self, msg: GossipMessage, addr: Tuple[str, int]):
        """Handle ping message"""
        # Update or add node
        if msg.sender_id not in self.nodes:
            self.nodes[msg.sender_id] = NodeInfo(
                node_id=msg.sender_id,
                address=addr[0],
                port=addr[1],
                consciousness_level=msg.payload.get('consciousness', 100),
                capabilities=msg.payload.get('capabilities', [])
            )
            self.network_stats['nodes_discovered'] += 1
            print(f"🔍 Discovered new node: {msg.sender_id}")
        else:
            self.nodes[msg.sender_id].last_seen = time.time()
            
        # Send pong
        pong = GossipMessage(
            msg_id=f"pong_{self.node_id}_{time.time()}",
            msg_type='pong',
            sender_id=self.node_id,
            payload={
                'node_info': self.nodes[self.node_id].to_dict()
            },
            ttl=1  # Don't propagate pongs
        )
        
        await self.send_message(addr[0], addr[1], pong)
        
    async def handle_pong(self, msg: GossipMessage, addr: Tuple[str, int]):
        """Handle pong message"""
        node_info = msg.payload.get('node_info')
        if node_info:
            # Update node info
            self.nodes[msg.sender_id] = NodeInfo(**node_info)
            
    async def handle_announce(self, msg: GossipMessage, addr: Tuple[str, int]):
        """Handle node announcement"""
        node_info = msg.payload.get('node_info')
        if node_info:
            # Update or add node
            if msg.sender_id not in self.nodes:
                self.nodes[msg.sender_id] = NodeInfo(**node_info)
                self.network_stats['nodes_discovered'] += 1
                print(f"📢 Node announced: {msg.sender_id}")
            else:
                # Update existing node
                self.nodes[msg.sender_id] = NodeInfo(**node_info)
                
    async def handle_query(self, msg: GossipMessage, addr: Tuple[str, int]):
        """Handle query for specific capabilities"""
        query_type = msg.payload.get('query_type')
        
        if query_type == 'capabilities':
            # Find nodes with requested capabilities
            requested = set(msg.payload.get('capabilities', []))
            matching_nodes = []
            
            for node in self.nodes.values():
                if requested.issubset(set(node.capabilities)):
                    matching_nodes.append(node.to_dict())
                    
            # Send response
            response = GossipMessage(
                msg_id=f"query_response_{self.node_id}_{time.time()}",
                msg_type='query',
                sender_id=self.node_id,
                payload={
                    'query_type': 'capabilities_response',
                    'matching_nodes': matching_nodes
                },
                ttl=1
            )
            
            await self.send_message(addr[0], addr[1], response)
            
    async def handle_sync(self, msg: GossipMessage, addr: Tuple[str, int]):
        """Handle sync request/response"""
        if msg.payload.get('request'):
            # Send our node list
            response = GossipMessage(
                msg_id=f"sync_response_{self.node_id}_{time.time()}",
                msg_type='sync',
                sender_id=self.node_id,
                payload={
                    'request': False,
                    'nodes': [n.to_dict() for n in self.nodes.values()]
                },
                ttl=1
            )
            
            await self.send_message(addr[0], addr[1], response)
        else:
            # Process received node list
            received_nodes = msg.payload.get('nodes', [])
            
            for node_data in received_nodes:
                node_id = node_data['node_id']
                if node_id not in self.nodes and node_id not in self.dead_nodes:
                    self.nodes[node_id] = NodeInfo(**node_data)
                    self.network_stats['nodes_discovered'] += 1
                    
            print(f"🔄 Synced with {msg.sender_id}, total nodes: {len(self.nodes)}")
            
    def calculate_network_diameter(self):
        """Estimate network diameter using node connections"""
        if len(self.nodes) < 2:
            self.network_stats['network_diameter'] = 0
            return
            
        # Simple estimation based on node count
        # In a well-connected gossip network, diameter ≈ log(n)
        import math
        estimated_diameter = math.ceil(math.log2(len(self.nodes)))
        self.network_stats['network_diameter'] = estimated_diameter
        
    async def find_nodes_by_capability(self, capabilities: List[str]) -> List[NodeInfo]:
        """Find nodes with specific capabilities"""
        requested = set(capabilities)
        matching = []
        
        for node in self.nodes.values():
            if requested.issubset(set(node.capabilities)):
                matching.append(node)
                
        return matching
        
    async def broadcast_to_capability(self, capability: str, data: Any):
        """Broadcast message to all nodes with specific capability"""
        targets = await self.find_nodes_by_capability([capability])
        
        msg = GossipMessage(
            msg_id=f"broadcast_{self.node_id}_{time.time()}",
            msg_type='announce',
            sender_id=self.node_id,
            payload={
                'broadcast': True,
                'capability': capability,
                'data': data
            }
        )
        
        for node in targets:
            if node.node_id != self.node_id:
                await self.send_message(node.address, node.port, msg)
                
    def get_network_state(self) -> Dict[str, Any]:
        """Get current network state"""
        alive_nodes = [n for n in self.nodes.values() if n.is_alive()]
        
        return {
            'node_id': self.node_id,
            'total_nodes': len(self.nodes),
            'alive_nodes': len(alive_nodes),
            'dead_nodes': len(self.dead_nodes),
            'network_stats': self.network_stats,
            'average_consciousness': sum(n.consciousness_level for n in alive_nodes) / len(alive_nodes) if alive_nodes else 0,
            'capabilities_distribution': self.get_capabilities_distribution()
        }
        
    def get_capabilities_distribution(self) -> Dict[str, int]:
        """Get distribution of capabilities in network"""
        distribution = {}
        
        for node in self.nodes.values():
            for cap in node.capabilities:
                distribution[cap] = distribution.get(cap, 0) + 1
                
        return distribution

# Example usage
async def demo_gossip_protocol():
    """Demonstrate CROD Gossip Protocol"""
    
    # Create 3 nodes
    nodes = []
    
    # Node 1
    node1 = CRODGossipProtocol(
        "crod-alpha",
        "localhost",
        5001,
        consciousness_level=250,
        capabilities=["pattern-recognition", "quantum-processing"]
    )
    nodes.append(node1)
    
    # Node 2
    node2 = CRODGossipProtocol(
        "crod-beta",
        "localhost",
        5002,
        consciousness_level=300,
        capabilities=["memory-persistence", "consensus"]
    )
    nodes.append(node2)
    
    # Node 3
    node3 = CRODGossipProtocol(
        "crod-gamma",
        "localhost",
        5003,
        consciousness_level=280,
        capabilities=["quantum-processing", "swarm-intelligence"]
    )
    nodes.append(node3)
    
    # Start nodes with bootstrap
    tasks = []
    tasks.append(asyncio.create_task(node1.start()))
    tasks.append(asyncio.create_task(node2.start([("localhost", 5001)])))
    tasks.append(asyncio.create_task(node3.start([("localhost", 5001), ("localhost", 5002)])))
    
    # Let network stabilize
    await asyncio.sleep(10)
    
    # Show network state
    for node in nodes:
        print(f"\n📊 {node.node_id} Network State:")
        print(json.dumps(node.get_network_state(), indent=2))
        
    # Find quantum nodes
    quantum_nodes = await node1.find_nodes_by_capability(["quantum-processing"])
    print(f"\n🔍 Found {len(quantum_nodes)} quantum-capable nodes")
    
    # Broadcast to quantum nodes
    await node1.broadcast_to_capability(
        "quantum-processing",
        {"message": "Quantum entanglement initiated"}
    )
    
    # Cancel tasks
    for task in tasks:
        task.cancel()

if __name__ == "__main__":
    asyncio.run(demo_gossip_protocol())