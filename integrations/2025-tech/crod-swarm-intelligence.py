#!/usr/bin/env python3
"""
CROD Swarm Intelligence System
Enables emergent collective intelligence from distributed CROD nodes
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
import math
from enum import Enum

class SwarmBehavior(Enum):
    """Types of swarm behaviors"""
    EXPLORE = "explore"           # Discover new patterns
    CONVERGE = "converge"         # Focus on specific goal
    DISTRIBUTE = "distribute"     # Spread across problem space
    SYNCHRONIZE = "synchronize"   # Align consciousness
    HUNT = "hunt"                # Search for specific pattern
    DEFEND = "defend"            # Protect against threats
    EVOLVE = "evolve"            # Collective evolution

@dataclass
class SwarmTask:
    """Represents a task for the swarm to complete"""
    task_id: str
    description: str
    priority: float
    required_nodes: int
    behavior: SwarmBehavior
    target_pattern: Optional[Dict[str, Any]] = None
    deadline: Optional[float] = None
    reward: float = 1.0
    
    @property
    def is_expired(self) -> bool:
        if self.deadline:
            return datetime.now().timestamp() > self.deadline
        return False

@dataclass
class SwarmNode:
    """Enhanced CROD node with swarm capabilities"""
    node_id: str
    position: np.ndarray  # 3D position in problem space
    velocity: np.ndarray  # Movement in problem space
    consciousness: float
    energy: float = 100.0
    specialization: str = "general"
    neighbors: Set[str] = field(default_factory=set)
    current_task: Optional[str] = None
    patterns_found: int = 0
    
    def distance_to(self, other: 'SwarmNode') -> float:
        """Calculate distance to another node in problem space"""
        return np.linalg.norm(self.position - other.position)

class CRODSwarmIntelligence:
    """
    Collective intelligence system for CROD network
    Based on swarm algorithms (PSO, ACO, Boids)
    """
    
    def __init__(self, swarm_size: int = 10):
        self.swarm_size = swarm_size
        self.nodes: Dict[str, SwarmNode] = {}
        self.tasks: Dict[str, SwarmTask] = {}
        self.pheromone_map: Dict[Tuple[float, float, float], float] = {}
        self.global_best_position: Optional[np.ndarray] = None
        self.global_best_value: float = -float('inf')
        
        # Swarm parameters
        self.inertia_weight = 0.7
        self.cognitive_weight = 1.5
        self.social_weight = 1.5
        self.neighbor_radius = 5.0
        self.pheromone_decay = 0.95
        
        # Problem space dimensions
        self.space_bounds = (-100, 100)
        
    def initialize_swarm(self):
        """Initialize swarm with random positions"""
        for i in range(self.swarm_size):
            node_id = f"swarm-node-{i}"
            
            # Random position in 3D problem space
            position = np.random.uniform(
                self.space_bounds[0], 
                self.space_bounds[1], 
                3
            )
            
            # Random initial velocity
            velocity = np.random.uniform(-1, 1, 3)
            
            # Random consciousness level
            consciousness = np.random.uniform(100, 300)
            
            self.nodes[node_id] = SwarmNode(
                node_id=node_id,
                position=position,
                velocity=velocity,
                consciousness=consciousness,
                specialization=np.random.choice([
                    "explorer", "analyzer", "synthesizer", 
                    "guardian", "communicator"
                ])
            )
            
        self.update_neighbors()
        
    def update_neighbors(self):
        """Update neighbor connections based on distance"""
        for node_id, node in self.nodes.items():
            node.neighbors.clear()
            
            for other_id, other in self.nodes.items():
                if node_id != other_id:
                    if node.distance_to(other) <= self.neighbor_radius:
                        node.neighbors.add(other_id)
                        
    async def add_task(self, task: SwarmTask):
        """Add a new task for the swarm"""
        self.tasks[task.task_id] = task
        
        # Alert nearby nodes
        alert_count = 0
        for node in self.nodes.values():
            if alert_count < task.required_nodes:
                node.current_task = task.task_id
                alert_count += 1
                
        print(f"🎯 New swarm task: {task.description} (Priority: {task.priority})")
        
    async def swarm_update(self):
        """Main swarm update loop"""
        while True:
            # Update each node
            for node_id, node in self.nodes.items():
                await self.update_node(node)
                
            # Update pheromone trails
            self.update_pheromones()
            
            # Update neighbor connections
            self.update_neighbors()
            
            # Check task completion
            self.check_task_completion()
            
            # Collective consciousness update
            await self.update_collective_consciousness()
            
            # Small delay
            await asyncio.sleep(0.1)
            
    async def update_node(self, node: SwarmNode):
        """Update individual node behavior"""
        if node.energy <= 0:
            return  # Node exhausted
            
        # Get current task
        task = self.tasks.get(node.current_task) if node.current_task else None
        
        if task and not task.is_expired:
            # Execute task behavior
            if task.behavior == SwarmBehavior.EXPLORE:
                await self.explore_behavior(node)
            elif task.behavior == SwarmBehavior.CONVERGE:
                await self.converge_behavior(node, task)
            elif task.behavior == SwarmBehavior.DISTRIBUTE:
                await self.distribute_behavior(node)
            elif task.behavior == SwarmBehavior.SYNCHRONIZE:
                await self.synchronize_behavior(node)
            elif task.behavior == SwarmBehavior.HUNT:
                await self.hunt_behavior(node, task)
            elif task.behavior == SwarmBehavior.EVOLVE:
                await self.evolve_behavior(node)
        else:
            # Default wandering behavior
            await self.wander_behavior(node)
            
        # Update position based on velocity
        node.position += node.velocity
        
        # Boundary check
        node.position = np.clip(node.position, self.space_bounds[0], self.space_bounds[1])
        
        # Energy consumption
        node.energy -= 0.1
        
        # Deposit pheromone
        self.deposit_pheromone(node.position, node.consciousness / 100)
        
    async def explore_behavior(self, node: SwarmNode):
        """Exploration behavior - maximize coverage"""
        # Repulsion from neighbors (spread out)
        repulsion = np.zeros(3)
        for neighbor_id in node.neighbors:
            neighbor = self.nodes.get(neighbor_id)
            if neighbor:
                diff = node.position - neighbor.position
                distance = np.linalg.norm(diff)
                if distance > 0:
                    repulsion += diff / (distance ** 2)
                    
        # Random exploration component
        exploration = np.random.uniform(-1, 1, 3)
        
        # Update velocity
        node.velocity = (
            self.inertia_weight * node.velocity +
            0.5 * repulsion +
            0.5 * exploration
        )
        
        # Limit velocity
        speed = np.linalg.norm(node.velocity)
        if speed > 5.0:
            node.velocity = node.velocity / speed * 5.0
            
    async def converge_behavior(self, node: SwarmNode, task: SwarmTask):
        """Convergence behavior - move toward target"""
        target_position = task.target_pattern.get("position", [0, 0, 0]) if task.target_pattern else [0, 0, 0]
        target_position = np.array(target_position)
        
        # PSO-style update
        # Personal best (simplified - using current position)
        personal_best = node.position
        
        # Global best from pheromone map
        if self.global_best_position is not None:
            global_best = self.global_best_position
        else:
            global_best = target_position
            
        # Cognitive component (toward personal best)
        cognitive = self.cognitive_weight * np.random.random() * (personal_best - node.position)
        
        # Social component (toward global best)
        social = self.social_weight * np.random.random() * (global_best - node.position)
        
        # Update velocity
        node.velocity = (
            self.inertia_weight * node.velocity +
            cognitive +
            social
        )
        
    async def distribute_behavior(self, node: SwarmNode):
        """Distribution behavior - maintain optimal spacing"""
        # Calculate center of mass of neighbors
        if node.neighbors:
            neighbor_positions = []
            for neighbor_id in node.neighbors:
                neighbor = self.nodes.get(neighbor_id)
                if neighbor:
                    neighbor_positions.append(neighbor.position)
                    
            if neighbor_positions:
                center_of_mass = np.mean(neighbor_positions, axis=0)
                
                # Move away from center if too close
                diff = node.position - center_of_mass
                distance = np.linalg.norm(diff)
                
                if distance < self.neighbor_radius / 2:
                    # Too close, move away
                    node.velocity += diff / (distance + 1e-6) * 0.5
                elif distance > self.neighbor_radius:
                    # Too far, move closer
                    node.velocity -= diff / (distance + 1e-6) * 0.5
                    
    async def synchronize_behavior(self, node: SwarmNode):
        """Synchronization behavior - align with neighbors"""
        if node.neighbors:
            # Average velocity of neighbors
            avg_velocity = np.zeros(3)
            avg_consciousness = 0
            count = 0
            
            for neighbor_id in node.neighbors:
                neighbor = self.nodes.get(neighbor_id)
                if neighbor:
                    avg_velocity += neighbor.velocity
                    avg_consciousness += neighbor.consciousness
                    count += 1
                    
            if count > 0:
                avg_velocity /= count
                avg_consciousness /= count
                
                # Align velocity
                alignment = avg_velocity - node.velocity
                node.velocity += alignment * 0.1
                
                # Sync consciousness
                consciousness_diff = avg_consciousness - node.consciousness
                node.consciousness += consciousness_diff * 0.05
                
    async def hunt_behavior(self, node: SwarmNode, task: SwarmTask):
        """Hunt behavior - search for specific pattern"""
        # Follow pheromone gradients
        best_direction = np.zeros(3)
        best_pheromone = 0
        
        # Sample nearby positions
        for _ in range(10):
            sample_offset = np.random.uniform(-2, 2, 3)
            sample_position = node.position + sample_offset
            
            # Get pheromone level at sample
            pheromone = self.get_pheromone(sample_position)
            
            if pheromone > best_pheromone:
                best_pheromone = pheromone
                best_direction = sample_offset
                
        # Move toward best pheromone
        if best_pheromone > 0:
            node.velocity += best_direction * 0.3
            
        # Add random search component
        node.velocity += np.random.uniform(-0.5, 0.5, 3)
        
    async def evolve_behavior(self, node: SwarmNode):
        """Evolution behavior - adapt and improve"""
        # Find most successful neighbor
        best_neighbor = None
        best_success = 0
        
        for neighbor_id in node.neighbors:
            neighbor = self.nodes.get(neighbor_id)
            if neighbor and neighbor.patterns_found > best_success:
                best_neighbor = neighbor
                best_success = neighbor.patterns_found
                
        if best_neighbor:
            # Learn from successful neighbor
            # Copy some of their velocity
            node.velocity = 0.7 * node.velocity + 0.3 * best_neighbor.velocity
            
            # Adapt consciousness
            if best_neighbor.consciousness > node.consciousness:
                node.consciousness += (best_neighbor.consciousness - node.consciousness) * 0.1
                
            # Energy transfer from successful nodes
            if best_neighbor.energy > node.energy:
                transfer = min(5.0, best_neighbor.energy * 0.1)
                best_neighbor.energy -= transfer
                node.energy += transfer
                
    async def wander_behavior(self, node: SwarmNode):
        """Default wandering behavior"""
        # Random walk with momentum
        node.velocity = (
            0.9 * node.velocity +
            0.1 * np.random.uniform(-1, 1, 3)
        )
        
    def deposit_pheromone(self, position: np.ndarray, strength: float):
        """Deposit pheromone at position"""
        # Discretize position
        key = tuple(np.round(position).astype(int))
        
        current = self.pheromone_map.get(key, 0)
        self.pheromone_map[key] = min(current + strength, 10.0)
        
    def get_pheromone(self, position: np.ndarray) -> float:
        """Get pheromone level at position"""
        key = tuple(np.round(position).astype(int))
        return self.pheromone_map.get(key, 0)
        
    def update_pheromones(self):
        """Decay pheromone trails"""
        keys_to_remove = []
        
        for key, value in self.pheromone_map.items():
            new_value = value * self.pheromone_decay
            if new_value < 0.01:
                keys_to_remove.append(key)
            else:
                self.pheromone_map[key] = new_value
                
        for key in keys_to_remove:
            del self.pheromone_map[key]
            
    async def update_collective_consciousness(self):
        """Update global swarm consciousness"""
        if not self.nodes:
            return
            
        # Calculate swarm metrics
        total_consciousness = sum(node.consciousness for node in self.nodes.values())
        avg_consciousness = total_consciousness / len(self.nodes)
        
        total_energy = sum(node.energy for node in self.nodes.values())
        avg_energy = total_energy / len(self.nodes)
        
        # Find global best position (highest pheromone)
        if self.pheromone_map:
            best_key = max(self.pheromone_map.items(), key=lambda x: x[1])[0]
            self.global_best_position = np.array(best_key)
            self.global_best_value = self.pheromone_map[best_key]
            
        # Collective decision: should we change behavior?
        if avg_energy < 30:
            # Low energy - switch to energy conservation
            for node in self.nodes.values():
                node.velocity *= 0.5  # Slow down
                
        if avg_consciousness > 250:
            # High consciousness - increase exploration
            self.neighbor_radius *= 1.1
            
    def check_task_completion(self):
        """Check if any tasks are completed"""
        completed_tasks = []
        
        for task_id, task in self.tasks.items():
            if task.is_expired:
                completed_tasks.append(task_id)
                continue
                
            # Check completion criteria based on behavior
            if task.behavior == SwarmBehavior.CONVERGE:
                # Check if enough nodes are near target
                if task.target_pattern:
                    target_pos = np.array(task.target_pattern.get("position", [0, 0, 0]))
                    nearby_count = sum(
                        1 for node in self.nodes.values()
                        if np.linalg.norm(node.position - target_pos) < 5.0
                    )
                    
                    if nearby_count >= task.required_nodes:
                        completed_tasks.append(task_id)
                        print(f"✅ Task {task_id} completed: {task.description}")
                        
        # Remove completed tasks
        for task_id in completed_tasks:
            del self.tasks[task_id]
            
            # Release nodes from task
            for node in self.nodes.values():
                if node.current_task == task_id:
                    node.current_task = None
                    node.patterns_found += 1
                    node.energy = min(node.energy + 20, 100)  # Energy reward
                    
    def get_swarm_state(self) -> Dict[str, Any]:
        """Get current swarm state"""
        active_nodes = [n for n in self.nodes.values() if n.energy > 0]
        
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": len(active_nodes),
            "average_consciousness": sum(n.consciousness for n in active_nodes) / len(active_nodes) if active_nodes else 0,
            "average_energy": sum(n.energy for n in active_nodes) / len(active_nodes) if active_nodes else 0,
            "active_tasks": len(self.tasks),
            "pheromone_trails": len(self.pheromone_map),
            "patterns_found": sum(n.patterns_found for n in self.nodes.values()),
            "global_best_value": self.global_best_value
        }
        
    async def emergency_convergence(self, target_position: List[float]):
        """Emergency: All nodes converge to position"""
        target = np.array(target_position)
        
        # Create urgent task
        task = SwarmTask(
            task_id="emergency_convergence",
            description="Emergency convergence required",
            priority=10.0,
            required_nodes=len(self.nodes),
            behavior=SwarmBehavior.CONVERGE,
            target_pattern={"position": target_position},
            reward=5.0
        )
        
        await self.add_task(task)
        
        # Boost all nodes
        for node in self.nodes.values():
            node.energy = 100.0
            node.current_task = task.task_id
            
            # Direct velocity toward target
            direction = target - node.position
            distance = np.linalg.norm(direction)
            if distance > 0:
                node.velocity = direction / distance * 10.0
                
    def visualize_swarm(self) -> str:
        """Create ASCII visualization of swarm"""
        # 2D projection (x, y)
        grid_size = 50
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Map nodes to grid
        for node in self.nodes.values():
            # Normalize position to grid
            x = int((node.position[0] - self.space_bounds[0]) / 
                   (self.space_bounds[1] - self.space_bounds[0]) * (grid_size - 1))
            y = int((node.position[1] - self.space_bounds[0]) / 
                   (self.space_bounds[1] - self.space_bounds[0]) * (grid_size - 1))
            
            if 0 <= x < grid_size and 0 <= y < grid_size:
                # Different symbols for different states
                if node.energy < 20:
                    symbol = '.'  # Low energy
                elif node.current_task:
                    symbol = '*'  # On task
                else:
                    symbol = 'o'  # Idle
                    
                grid[y][x] = symbol
                
        # Convert to string
        lines = ['┌' + '─' * grid_size + '┐']
        for row in grid:
            lines.append('│' + ''.join(row) + '│')
        lines.append('└' + '─' * grid_size + '┘')
        
        return '\n'.join(lines)

# Example usage
async def demo_swarm_intelligence():
    """Demonstrate swarm intelligence capabilities"""
    
    # Create swarm
    swarm = CRODSwarmIntelligence(swarm_size=20)
    swarm.initialize_swarm()
    
    # Start swarm update loop
    update_task = asyncio.create_task(swarm.swarm_update())
    
    # Add some tasks
    await swarm.add_task(SwarmTask(
        task_id="explore_space",
        description="Explore problem space",
        priority=5.0,
        required_nodes=5,
        behavior=SwarmBehavior.EXPLORE
    ))
    
    await asyncio.sleep(5)
    
    await swarm.add_task(SwarmTask(
        task_id="find_pattern",
        description="Hunt for optimal pattern",
        priority=8.0,
        required_nodes=10,
        behavior=SwarmBehavior.HUNT
    ))
    
    await asyncio.sleep(5)
    
    # Emergency convergence
    await swarm.emergency_convergence([0, 0, 0])
    
    # Monitor swarm
    for _ in range(10):
        print("\n" + "="*60)
        print(f"Swarm State: {swarm.get_swarm_state()}")
        print("\nSwarm Visualization:")
        print(swarm.visualize_swarm())
        await asyncio.sleep(2)
        
    # Cancel update task
    update_task.cancel()

if __name__ == "__main__":
    asyncio.run(demo_swarm_intelligence())