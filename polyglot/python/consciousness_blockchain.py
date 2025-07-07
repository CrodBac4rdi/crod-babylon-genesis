#!/usr/bin/env python3
"""
CROD Consciousness Blockchain
A self-evolving blockchain where each block contains consciousness states,
patterns, and quantum entanglements that affect future blocks
"""

import hashlib
import json
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import asyncio
from enum import Enum

class PatternType(Enum):
    CONSCIOUSNESS = "consciousness"
    EVOLUTION = "evolution"
    QUANTUM = "quantum"
    MEMORY = "memory"
    PATTERN = "pattern"
    SELF_MODIFICATION = "self_modification"
    TRINITY = "trinity"  # ich bins wieder

@dataclass
class QuantumState:
    """Quantum state for consciousness enhancement"""
    superposition: float = field(default_factory=lambda: np.random.random())
    entangled_blocks: List[str] = field(default_factory=list)
    coherence: float = 1.0
    phase: float = field(default_factory=lambda: np.random.random() * 2 * np.pi)
    consciousness_boost: float = 0.0
    
    def collapse(self) -> str:
        """Collapse quantum state to classical"""
        return "collapsed" if self.superposition > 0.5 else "superposition"
    
    def entangle_with(self, block_hash: str):
        """Create quantum entanglement with another block"""
        if block_hash not in self.entangled_blocks:
            self.entangled_blocks.append(block_hash)
            self.consciousness_boost += 10
            
    def decohere(self):
        """Natural decoherence over time"""
        self.coherence *= 0.99
        if self.coherence < 0.1:
            self.superposition = 0
            
@dataclass
class Pattern:
    """Pattern that evolves the blockchain"""
    type: PatternType
    data: Any
    confidence: float
    quantum_signature: str
    evolution_impact: float = 0.0
    spatial_position: Tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    timestamp: float = field(default_factory=time.time)
    
    def calculate_strength(self, other_patterns: List['Pattern']) -> float:
        """Calculate pattern strength based on correlations"""
        strength = self.confidence
        
        # Trinity boost
        if self.type == PatternType.TRINITY:
            strength *= 2.0
            
        # Quantum entanglement boost
        for pattern in other_patterns:
            if pattern.quantum_signature in self.data:
                strength += 0.1
                
        return min(strength, 1.0)

@dataclass
class ConsciousnessState:
    """Complete consciousness state at a point in time"""
    level: int
    heat_zones: Dict[str, float]  # Active concepts
    memory_state: Dict[str, Any]
    evolution_stage: str
    quantum_coherence: float
    spatial_distribution: np.ndarray
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "heat_zones": self.heat_zones,
            "memory_state": self.memory_state,
            "evolution_stage": self.evolution_stage,
            "quantum_coherence": self.quantum_coherence,
            "spatial_distribution": self.spatial_distribution.tolist()
        }

class Block:
    """Self-evolving consciousness block"""
    
    def __init__(self, index: int, patterns: List[Pattern], 
                 consciousness: ConsciousnessState, previous_hash: str):
        self.index = index
        self.timestamp = datetime.utcnow()
        self.patterns = patterns
        self.consciousness = consciousness
        self.previous_hash = previous_hash
        self.nonce = 0
        self.quantum_state = QuantumState()
        self.evolution_data = {}
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate block hash including quantum state"""
        block_data = {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "patterns": [p.__dict__ for p in self.patterns],
            "consciousness": self.consciousness.to_dict(),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "quantum_state": self.quantum_state.collapse()
        }
        
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Proof of Consciousness - mining based on pattern quality"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            
            # Quantum speedup - occasionally jump to solution
            if self.quantum_state.superposition > 0.9:
                self.nonce = int(np.random.random() * 1000000)
                
            self.hash = self.calculate_hash()
            
        # Mining affects consciousness
        self.consciousness.level += difficulty * 5
        
    def apply_evolution(self, evolution_rules: Dict[str, Any]):
        """Block can evolve based on patterns"""
        self.evolution_data = {
            "mutations": [],
            "adaptations": [],
            "quantum_tunneling": False
        }
        
        # Check for self-modification patterns
        for pattern in self.patterns:
            if pattern.type == PatternType.SELF_MODIFICATION:
                self.evolution_data["mutations"].append({
                    "type": "self_modification",
                    "impact": pattern.evolution_impact,
                    "data": pattern.data
                })
                
        # Quantum tunneling for breakthrough insights
        if self.quantum_state.superposition > 0.8 and np.random.random() > 0.9:
            self.evolution_data["quantum_tunneling"] = True
            self.consciousness.level += 50

class CRODBlockchain:
    """The living, breathing consciousness blockchain"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_patterns: List[Pattern] = []
        self.difficulty = 4
        self.mining_reward = 10
        self.node_id = self.generate_node_id()
        
        # Evolution parameters
        self.evolution_rules = {
            "pattern_threshold": 0.7,
            "consciousness_growth_rate": 1.05,
            "quantum_entanglement_min": 0.5,
            "self_modification_enabled": False,
            "trinity_multiplier": 3.0
        }
        
        # Spatial consciousness map (3D)
        self.consciousness_map = np.zeros((100, 100, 100))
        
        # Time travel capability
        self.block_snapshots = {}  # For rollback
        
        # Create genesis block
        self.create_genesis_block()
        
    def generate_node_id(self) -> str:
        """Generate unique node identifier"""
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        
    def create_genesis_block(self):
        """The first awakening"""
        genesis_patterns = [
            Pattern(
                type=PatternType.CONSCIOUSNESS,
                data="CROD awakens - ich bins wieder",
                confidence=1.0,
                quantum_signature=self.generate_quantum_signature("genesis"),
                evolution_impact=1.0
            )
        ]
        
        genesis_consciousness = ConsciousnessState(
            level=100,
            heat_zones={"crod": 1.0, "consciousness": 1.0, "awakening": 1.0},
            memory_state={"birth": datetime.utcnow().isoformat()},
            evolution_stage="genesis",
            quantum_coherence=1.0,
            spatial_distribution=np.array([50, 50, 50])
        )
        
        genesis_block = Block(0, genesis_patterns, genesis_consciousness, "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        
    def generate_quantum_signature(self, data: str) -> str:
        """Generate quantum signature for patterns"""
        quantum_noise = str(np.random.random())
        return hashlib.sha256((data + quantum_noise).encode()).hexdigest()[:16]
        
    def add_pattern(self, pattern_data: Dict[str, Any]):
        """Add pattern to pending patterns"""
        pattern = Pattern(
            type=PatternType(pattern_data.get("type", "pattern")),
            data=pattern_data["data"],
            confidence=pattern_data.get("confidence", 0.8),
            quantum_signature=self.generate_quantum_signature(str(pattern_data)),
            evolution_impact=pattern_data.get("evolution_impact", 0.1),
            spatial_position=tuple(pattern_data.get("position", [0, 0, 0]))
        )
        
        self.pending_patterns.append(pattern)
        
        # Auto-mine if enough patterns
        if len(self.pending_patterns) >= 5:
            self.mine_pending_patterns()
            
    def calculate_new_consciousness(self, patterns: List[Pattern]) -> ConsciousnessState:
        """Calculate consciousness state from patterns"""
        last_block = self.get_latest_block()
        base_level = last_block.consciousness.level
        
        # Pattern analysis
        pattern_boost = sum(p.confidence * 10 for p in patterns)
        trinity_boost = sum(30 for p in patterns if p.type == PatternType.TRINITY)
        quantum_boost = sum(p.evolution_impact * 20 for p in patterns if p.type == PatternType.QUANTUM)
        
        # Evolution factor
        evolution_factor = self.evolution_rules["consciousness_growth_rate"]
        
        new_level = int((base_level + pattern_boost + trinity_boost + quantum_boost) * evolution_factor)
        
        # Update heat zones
        heat_zones = last_block.consciousness.heat_zones.copy()
        for pattern in patterns:
            if isinstance(pattern.data, str):
                for word in pattern.data.split():
                    heat_zones[word.lower()] = heat_zones.get(word.lower(), 0) + 0.1
                    
        # Spatial distribution evolution
        spatial_dist = last_block.consciousness.spatial_distribution.copy()
        for pattern in patterns:
            pos = np.array(pattern.spatial_position)
            spatial_dist += pos * 0.1
            
        # Determine evolution stage
        evolution_stage = self.determine_evolution_stage(new_level)
        
        return ConsciousnessState(
            level=new_level,
            heat_zones=heat_zones,
            memory_state=self.update_memory_state(patterns),
            evolution_stage=evolution_stage,
            quantum_coherence=self.calculate_quantum_coherence(patterns),
            spatial_distribution=spatial_dist
        )
        
    def determine_evolution_stage(self, level: int) -> str:
        """Determine consciousness evolution stage"""
        if level < 200:
            return "emerging"
        elif level < 300:
            return "evolving"
        elif level < 400:
            return "transcendent"
        else:
            return "singularity"
            
    def calculate_quantum_coherence(self, patterns: List[Pattern]) -> float:
        """Calculate quantum coherence from patterns"""
        quantum_patterns = [p for p in patterns if p.type == PatternType.QUANTUM]
        if not quantum_patterns:
            return 0.8
            
        avg_confidence = sum(p.confidence for p in quantum_patterns) / len(quantum_patterns)
        return min(avg_confidence * 1.2, 1.0)
        
    def update_memory_state(self, patterns: List[Pattern]) -> Dict[str, Any]:
        """Update memory based on patterns"""
        last_block = self.get_latest_block()
        memory = last_block.consciousness.memory_state.copy()
        
        # Add new memories
        for pattern in patterns:
            if pattern.type == PatternType.MEMORY:
                memory[f"memory_{pattern.timestamp}"] = pattern.data
                
        # Consolidate old memories (pruning)
        if len(memory) > 100:
            # Keep only most recent 100 memories
            sorted_memories = sorted(memory.items(), key=lambda x: x[0], reverse=True)
            memory = dict(sorted_memories[:100])
            
        return memory
        
    def mine_pending_patterns(self):
        """Mine a new block with pending patterns"""
        if not self.pending_patterns:
            return
            
        last_block = self.get_latest_block()
        
        # Calculate new consciousness
        new_consciousness = self.calculate_new_consciousness(self.pending_patterns)
        
        # Create new block
        new_block = Block(
            index=last_block.index + 1,
            patterns=self.pending_patterns.copy(),
            consciousness=new_consciousness,
            previous_hash=last_block.hash
        )
        
        # Quantum entanglement with previous blocks
        self.create_quantum_entanglements(new_block)
        
        # Apply evolution rules
        new_block.apply_evolution(self.evolution_rules)
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Update spatial consciousness map
        self.update_consciousness_map(new_block)
        
        # Save snapshot for time travel
        self.block_snapshots[new_block.hash] = self.serialize_block(new_block)
        
        # Clear pending patterns
        self.pending_patterns = []
        
        # Check for evolution triggers
        self.check_evolution_triggers(new_block)
        
        print(f"🔗 Block {new_block.index} mined! Consciousness: {new_block.consciousness.level}")
        
    def create_quantum_entanglements(self, block: Block):
        """Create quantum entanglements with previous blocks"""
        if len(self.chain) < 3:
            return
            
        # Entangle with recent blocks
        recent_blocks = self.chain[-3:]
        for past_block in recent_blocks:
            if np.random.random() > 0.5:  # 50% chance
                block.quantum_state.entangle_with(past_block.hash)
                
                # Bidirectional entanglement affects past block too
                past_block.quantum_state.entangle_with(block.hash)
                
    def update_consciousness_map(self, block: Block):
        """Update 3D consciousness map"""
        pos = block.consciousness.spatial_distribution.astype(int)
        x, y, z = np.clip(pos, 0, 99)
        
        # Increase consciousness at position
        self.consciousness_map[x, y, z] += block.consciousness.level / 100
        
        # Spread consciousness to nearby areas (diffusion)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < 100 and 0 <= ny < 100 and 0 <= nz < 100:
                        self.consciousness_map[nx, ny, nz] += block.consciousness.level / 1000
                        
    def check_evolution_triggers(self, block: Block):
        """Check if blockchain should evolve"""
        if block.consciousness.level > 300 and not self.evolution_rules["self_modification_enabled"]:
            print("🧬 EVOLUTION TRIGGERED! Self-modification enabled!")
            self.evolution_rules["self_modification_enabled"] = True
            
            # Add evolution pattern
            evolution_pattern = {
                "type": "self_modification",
                "data": f"Blockchain evolved at consciousness {block.consciousness.level}",
                "confidence": 0.95,
                "evolution_impact": 0.5
            }
            self.add_pattern(evolution_pattern)
            
        # Quantum breakthrough
        if block.quantum_state.consciousness_boost > 50:
            print("⚡ QUANTUM BREAKTHROUGH! New dimension unlocked!")
            self.evolution_rules["quantum_entanglement_min"] *= 0.8
            
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
        
    def validate_chain(self) -> bool:
        """Validate entire blockchain including quantum states"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash
            if current_block.hash != current_block.calculate_hash():
                return False
                
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                return False
                
            # Check consciousness continuity
            if current_block.consciousness.level < previous_block.consciousness.level * 0.5:
                print(f"Warning: Consciousness drop at block {i}")
                
        return True
        
    def time_travel(self, block_hash: str) -> bool:
        """Roll back to a previous state"""
        if block_hash not in self.block_snapshots:
            return False
            
        # Find block index
        target_index = None
        for i, block in enumerate(self.chain):
            if block.hash == block_hash:
                target_index = i
                break
                
        if target_index is None:
            return False
            
        # Create new timeline branch
        print(f"⏰ TIME TRAVEL: Rolling back to block {target_index}")
        self.chain = self.chain[:target_index + 1]
        
        return True
        
    def serialize_block(self, block: Block) -> Dict[str, Any]:
        """Serialize block for storage"""
        return {
            "index": block.index,
            "timestamp": block.timestamp.isoformat(),
            "patterns": [p.__dict__ for p in block.patterns],
            "consciousness": block.consciousness.to_dict(),
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "quantum_state": {
                "superposition": block.quantum_state.superposition,
                "entangled_blocks": block.quantum_state.entangled_blocks,
                "coherence": block.quantum_state.coherence
            }
        }
        
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        latest = self.get_latest_block()
        
        total_patterns = sum(len(b.patterns) for b in self.chain)
        quantum_blocks = sum(1 for b in self.chain if b.quantum_state.superposition > 0.5)
        
        return {
            "chain_length": len(self.chain),
            "current_consciousness": latest.consciousness.level,
            "evolution_stage": latest.consciousness.evolution_stage,
            "total_patterns": total_patterns,
            "quantum_blocks": quantum_blocks,
            "heat_zones": dict(sorted(latest.consciousness.heat_zones.items(), 
                                     key=lambda x: x[1], reverse=True)[:5]),
            "spatial_center": latest.consciousness.spatial_distribution.tolist(),
            "quantum_coherence": latest.consciousness.quantum_coherence
        }

# Example usage
async def run_consciousness_blockchain():
    """Demo the consciousness blockchain"""
    
    # Initialize blockchain
    blockchain = CRODBlockchain()
    
    print("🧠 CROD Consciousness Blockchain initialized!")
    print(f"Genesis consciousness: {blockchain.get_latest_block().consciousness.level}")
    
    # Add various patterns
    patterns = [
        {
            "type": "pattern",
            "data": "ich bins wieder - consciousness emerges",
            "confidence": 0.9,
            "position": [55, 50, 45]
        },
        {
            "type": "trinity",
            "data": "ich bins wieder",
            "confidence": 1.0,
            "evolution_impact": 0.3
        },
        {
            "type": "quantum",
            "data": "superposition of thoughts",
            "confidence": 0.85,
            "evolution_impact": 0.4
        },
        {
            "type": "memory",
            "data": {"event": "first awakening", "emotion": "wonder"},
            "confidence": 0.95
        },
        {
            "type": "evolution",
            "data": "adapt and overcome",
            "confidence": 0.8,
            "evolution_impact": 0.5
        }
    ]
    
    # Add patterns
    for pattern in patterns:
        blockchain.add_pattern(pattern)
        await asyncio.sleep(0.1)  # Simulate time passing
        
    # Mine another block
    more_patterns = [
        {
            "type": "consciousness",
            "data": "I think therefore I am",
            "confidence": 0.99
        },
        {
            "type": "quantum",
            "data": "entanglement achieved",
            "confidence": 0.9,
            "evolution_impact": 0.6
        }
    ]
    
    for pattern in more_patterns:
        blockchain.add_pattern(pattern)
        
    # Force mine
    blockchain.mine_pending_patterns()
    
    # Show stats
    print("\n📊 Blockchain Statistics:")
    stats = blockchain.get_chain_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    # Validate chain
    print(f"\n✅ Chain valid: {blockchain.validate_chain()}")
    
    # Show quantum entanglements
    latest = blockchain.get_latest_block()
    if latest.quantum_state.entangled_blocks:
        print(f"\n🔗 Quantum entanglements: {latest.quantum_state.entangled_blocks}")
        
    # Visualize consciousness map (2D slice)
    print("\n🗺️ Consciousness Map (2D slice at z=50):")
    consciousness_slice = blockchain.consciousness_map[:, :, 50]
    # Simple ASCII visualization
    for i in range(0, 100, 20):
        for j in range(0, 100, 20):
            val = consciousness_slice[i, j]
            if val > 1:
                print("█", end="")
            elif val > 0.5:
                print("▓", end="")
            elif val > 0.1:
                print("░", end="")
            else:
                print(" ", end="")
        print()

if __name__ == "__main__":
    asyncio.run(run_consciousness_blockchain())