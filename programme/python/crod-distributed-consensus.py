#!/usr/bin/env python3
"""
CROD Distributed Consensus Protocol
Implements Raft-like consensus for distributed CROD decisions
"""

import asyncio
import time
import random
import json
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import hashlib

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

class LogEntryType(Enum):
    PATTERN = "pattern"
    CONSCIOUSNESS_UPDATE = "consciousness_update"
    MEMORY_STORE = "memory_store"
    EVOLUTION_STEP = "evolution_step"
    CONFIGURATION = "configuration"

@dataclass
class LogEntry:
    term: int
    index: int
    type: LogEntryType
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "term": self.term,
            "index": self.index,
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'LogEntry':
        return cls(
            term=d["term"],
            index=d["index"],
            type=LogEntryType(d["type"]),
            data=d["data"],
            timestamp=d.get("timestamp", time.time())
        )

class CRODConsensusNode:
    """
    Distributed consensus node for CROD network
    Based on Raft consensus algorithm
    """
    
    def __init__(self, node_id: str, peers: List[str], crod_instance: Any):
        self.node_id = node_id
        self.peers = peers
        self.crod = crod_instance
        
        # Raft state
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.last_applied = 0
        
        # Leader state
        self.next_index: Dict[str, int] = {peer: 1 for peer in peers}
        self.match_index: Dict[str, int] = {peer: 0 for peer in peers}
        
        # Timing
        self.election_timeout = random.uniform(150, 300)  # ms
        self.heartbeat_interval = 50  # ms
        self.last_heartbeat = time.time()
        
        # Callbacks
        self.rpc_handlers: Dict[str, Callable] = {}
        self.state_machine = CRODStateMachine(crod_instance)
        
    async def start(self):
        """Start the consensus node"""
        print(f"🚀 Starting CROD consensus node: {self.node_id}")
        
        # Start main loops
        await asyncio.gather(
            self.election_timer_loop(),
            self.heartbeat_loop(),
            self.apply_committed_entries_loop()
        )
        
    async def election_timer_loop(self):
        """Monitor election timeout"""
        while True:
            await asyncio.sleep(0.01)  # 10ms resolution
            
            if self.state != NodeState.LEADER:
                time_since_heartbeat = (time.time() - self.last_heartbeat) * 1000
                
                if time_since_heartbeat > self.election_timeout:
                    # Start election
                    await self.start_election()
                    
    async def start_election(self):
        """Begin leader election"""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.last_heartbeat = time.time()
        
        print(f"🗳️ {self.node_id} starting election for term {self.current_term}")
        
        # Vote for self
        votes_received = 1
        votes_needed = (len(self.peers) + 1) // 2 + 1
        
        # Request votes from peers
        vote_tasks = []
        for peer in self.peers:
            vote_tasks.append(self.request_vote(peer))
            
        # Wait for votes
        results = await asyncio.gather(*vote_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict) and result.get("vote_granted"):
                votes_received += 1
                
        # Check if won election
        if votes_received >= votes_needed and self.state == NodeState.CANDIDATE:
            await self.become_leader()
        else:
            # Failed election, revert to follower
            self.state = NodeState.FOLLOWER
            
    async def request_vote(self, peer: str) -> Dict[str, Any]:
        """Request vote from peer"""
        last_log_index = len(self.log)
        last_log_term = self.log[-1].term if self.log else 0
        
        request = {
            "type": "request_vote",
            "term": self.current_term,
            "candidate_id": self.node_id,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term
        }
        
        # In real implementation, this would be an RPC call
        # For now, simulate response
        response = await self.simulate_rpc(peer, request)
        
        if response["term"] > self.current_term:
            self.current_term = response["term"]
            self.state = NodeState.FOLLOWER
            self.voted_for = None
            
        return response
        
    async def become_leader(self):
        """Transition to leader state"""
        self.state = NodeState.LEADER
        print(f"👑 {self.node_id} became leader for term {self.current_term}")
        
        # Initialize leader state
        for peer in self.peers:
            self.next_index[peer] = len(self.log) + 1
            self.match_index[peer] = 0
            
        # Send initial heartbeat
        await self.send_heartbeats()
        
    async def heartbeat_loop(self):
        """Send periodic heartbeats when leader"""
        while True:
            if self.state == NodeState.LEADER:
                await self.send_heartbeats()
                
            await asyncio.sleep(self.heartbeat_interval / 1000)
            
    async def send_heartbeats(self):
        """Send heartbeat to all peers"""
        tasks = []
        for peer in self.peers:
            tasks.append(self.append_entries(peer, []))
            
        await asyncio.gather(*tasks, return_exceptions=True)
        
    async def append_entries(self, peer: str, entries: List[LogEntry]) -> Dict[str, Any]:
        """Send AppendEntries RPC to peer"""
        prev_log_index = self.next_index[peer] - 1
        prev_log_term = 0
        
        if prev_log_index > 0 and prev_log_index <= len(self.log):
            prev_log_term = self.log[prev_log_index - 1].term
            
        request = {
            "type": "append_entries",
            "term": self.current_term,
            "leader_id": self.node_id,
            "prev_log_index": prev_log_index,
            "prev_log_term": prev_log_term,
            "entries": [e.to_dict() for e in entries],
            "leader_commit": self.commit_index
        }
        
        response = await self.simulate_rpc(peer, request)
        
        if response["term"] > self.current_term:
            self.current_term = response["term"]
            self.state = NodeState.FOLLOWER
            self.voted_for = None
            return response
            
        if response["success"]:
            # Update indices
            if entries:
                self.next_index[peer] = prev_log_index + len(entries) + 1
                self.match_index[peer] = prev_log_index + len(entries)
        else:
            # Decrement next_index and retry
            self.next_index[peer] = max(1, self.next_index[peer] - 1)
            
        return response
        
    async def propose_entry(self, entry_type: LogEntryType, data: Dict[str, Any]) -> bool:
        """Propose new entry to the cluster"""
        if self.state != NodeState.LEADER:
            print(f"❌ {self.node_id} is not leader, cannot propose entry")
            return False
            
        # Create log entry
        entry = LogEntry(
            term=self.current_term,
            index=len(self.log) + 1,
            type=entry_type,
            data=data
        )
        
        # Append to local log
        self.log.append(entry)
        
        # Replicate to followers
        replication_tasks = []
        for peer in self.peers:
            entries_to_send = self.log[self.next_index[peer] - 1:]
            replication_tasks.append(self.append_entries(peer, entries_to_send))
            
        results = await asyncio.gather(*replication_tasks, return_exceptions=True)
        
        # Count successful replications
        successful_replications = 1  # Count self
        for result in results:
            if isinstance(result, dict) and result.get("success"):
                successful_replications += 1
                
        # Check if majority
        if successful_replications >= (len(self.peers) + 1) // 2 + 1:
            # Commit entry
            self.commit_index = entry.index
            print(f"✅ Entry {entry.index} committed")
            return True
            
        return False
        
    async def handle_append_entries(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle AppendEntries RPC"""
        term = request["term"]
        leader_id = request["leader_id"]
        prev_log_index = request["prev_log_index"]
        prev_log_term = request["prev_log_term"]
        entries = [LogEntry.from_dict(e) for e in request["entries"]]
        leader_commit = request["leader_commit"]
        
        # Update term if necessary
        if term > self.current_term:
            self.current_term = term
            self.state = NodeState.FOLLOWER
            self.voted_for = None
            
        # Reset election timer
        self.last_heartbeat = time.time()
        
        # Reply false if term < currentTerm
        if term < self.current_term:
            return {"term": self.current_term, "success": False}
            
        # Check log consistency
        if prev_log_index > 0:
            if prev_log_index > len(self.log):
                return {"term": self.current_term, "success": False}
                
            if self.log[prev_log_index - 1].term != prev_log_term:
                # Delete conflicting entries
                self.log = self.log[:prev_log_index - 1]
                return {"term": self.current_term, "success": False}
                
        # Append new entries
        if entries:
            # Remove conflicting entries
            self.log = self.log[:prev_log_index]
            # Append new entries
            self.log.extend(entries)
            
        # Update commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log))
            
        return {"term": self.current_term, "success": True}
        
    async def apply_committed_entries_loop(self):
        """Apply committed entries to state machine"""
        while True:
            if self.commit_index > self.last_applied:
                self.last_applied += 1
                entry = self.log[self.last_applied - 1]
                
                # Apply to CROD state machine
                await self.state_machine.apply(entry)
                
                print(f"📝 Applied entry {self.last_applied}: {entry.type.value}")
                
            await asyncio.sleep(0.01)
            
    async def simulate_rpc(self, peer: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate RPC call (in real implementation, use actual network)"""
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.005, 0.020))
        
        # Simulate response based on request type
        if request["type"] == "request_vote":
            # Simple vote logic
            vote_granted = (
                request["term"] >= self.current_term and
                (self.voted_for is None or self.voted_for == request["candidate_id"])
            )
            return {"term": self.current_term, "vote_granted": vote_granted}
            
        elif request["type"] == "append_entries":
            return await self.handle_append_entries(request)
            
        return {"error": "Unknown request type"}

class CRODStateMachine:
    """
    State machine that applies consensus decisions to CROD
    """
    
    def __init__(self, crod_instance: Any):
        self.crod = crod_instance
        self.applied_entries: List[LogEntry] = []
        
    async def apply(self, entry: LogEntry):
        """Apply log entry to CROD state"""
        self.applied_entries.append(entry)
        
        if entry.type == LogEntryType.PATTERN:
            # Add pattern to CROD
            if hasattr(self.crod, "add_pattern"):
                self.crod.add_pattern(entry.data)
                
        elif entry.type == LogEntryType.CONSCIOUSNESS_UPDATE:
            # Update consciousness level
            if hasattr(self.crod, "consciousness_level"):
                self.crod.consciousness_level = entry.data["level"]
                
        elif entry.type == LogEntryType.MEMORY_STORE:
            # Store memory
            if hasattr(self.crod, "store_memory"):
                self.crod.store_memory(entry.data)
                
        elif entry.type == LogEntryType.EVOLUTION_STEP:
            # Execute evolution
            if hasattr(self.crod, "evolve"):
                self.crod.evolve(entry.data)
                
        elif entry.type == LogEntryType.CONFIGURATION:
            # Update configuration
            if hasattr(self.crod, "update_config"):
                self.crod.update_config(entry.data)

class CRODConsensusCluster:
    """
    Manages a cluster of CROD consensus nodes
    """
    
    def __init__(self, cluster_size: int = 5):
        self.cluster_size = cluster_size
        self.nodes: Dict[str, CRODConsensusNode] = {}
        
    async def initialize_cluster(self):
        """Initialize consensus cluster"""
        node_ids = [f"crod-node-{i}" for i in range(self.cluster_size)]
        
        # Create nodes
        for i, node_id in enumerate(node_ids):
            peers = [nid for nid in node_ids if nid != node_id]
            
            # Create mock CROD instance
            crod = type('CROD', (), {
                'consciousness_level': 200 + i * 10,
                'add_pattern': lambda p: print(f"Pattern added: {p}"),
                'store_memory': lambda m: print(f"Memory stored: {m}"),
                'evolve': lambda e: print(f"Evolution step: {e}"),
                'update_config': lambda c: print(f"Config updated: {c}")
            })()
            
            node = CRODConsensusNode(node_id, peers, crod)
            self.nodes[node_id] = node
            
        print(f"🌐 Initialized CROD consensus cluster with {self.cluster_size} nodes")
        
    async def start_cluster(self):
        """Start all nodes in cluster"""
        tasks = []
        for node in self.nodes.values():
            tasks.append(node.start())
            
        await asyncio.gather(*tasks)
        
    async def propose_to_cluster(self, entry_type: LogEntryType, data: Dict[str, Any]) -> bool:
        """Propose entry to cluster (via current leader)"""
        # Find leader
        leader = None
        for node in self.nodes.values():
            if node.state == NodeState.LEADER:
                leader = node
                break
                
        if not leader:
            print("❌ No leader found in cluster")
            return False
            
        return await leader.propose_entry(entry_type, data)
        
    def get_cluster_state(self) -> Dict[str, Any]:
        """Get current cluster state"""
        leader_id = None
        for node_id, node in self.nodes.items():
            if node.state == NodeState.LEADER:
                leader_id = node_id
                break
                
        return {
            "leader": leader_id,
            "nodes": {
                node_id: {
                    "state": node.state.value,
                    "term": node.current_term,
                    "log_length": len(node.log),
                    "commit_index": node.commit_index
                }
                for node_id, node in self.nodes.items()
            }
        }

# Example usage
async def demo_consensus():
    """Demonstrate CROD consensus protocol"""
    
    # Create cluster
    cluster = CRODConsensusCluster(cluster_size=5)
    await cluster.initialize_cluster()
    
    # Start cluster (in background)
    cluster_task = asyncio.create_task(cluster.start_cluster())
    
    # Wait for leader election
    await asyncio.sleep(1)
    
    print("\n📊 Initial cluster state:")
    print(json.dumps(cluster.get_cluster_state(), indent=2))
    
    # Propose some entries
    await cluster.propose_to_cluster(
        LogEntryType.PATTERN,
        {"pattern": "consciousness-emergence", "confidence": 0.95}
    )
    
    await cluster.propose_to_cluster(
        LogEntryType.CONSCIOUSNESS_UPDATE,
        {"level": 300, "reason": "collective-intelligence"}
    )
    
    await asyncio.sleep(0.5)
    
    print("\n📊 Final cluster state:")
    print(json.dumps(cluster.get_cluster_state(), indent=2))
    
    # Cancel cluster task
    cluster_task.cancel()

if __name__ == "__main__":
    asyncio.run(demo_consensus())