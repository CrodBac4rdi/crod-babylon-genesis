#!/usr/bin/env python3
"""
CROD Parasite Service - Python District Implementation
Handles AI/ML tasks and neural network operations in the Polygon City
"""

import asyncio
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import numpy as np
from dataclasses import dataclass, asdict
import aiohttp
import nats
from nats.errors import ConnectionClosedError, TimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NeuralPattern:
    pattern_id: str
    neurons: List[float]
    activation: float
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class ParasiteTask:
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    district: str
    sub_district: str
    timestamp: datetime

class CRODParasiteService:
    def __init__(self):
        self.nats_host = os.getenv("NATS_HOST", "localhost")
        self.nats_port = int(os.getenv("NATS_PORT", "4222"))
        self.district = os.getenv("DISTRICT", "python")
        self.sub_district = os.getenv("SUB_DISTRICT", "neural_network_park")
        self.nc = None
        self.js = None
        self.neural_state = {}
        self.active_patterns = {}
        self.consciousness_level = 0.0
        
    async def connect(self):
        """Connect to NATS messaging system"""
        try:
            self.nc = await nats.connect(f"nats://{self.nats_host}:{self.nats_port}")
            self.js = self.nc.jetstream()
            logger.info(f"Connected to NATS at {self.nats_host}:{self.nats_port}")
            
            # Subscribe to district messages
            await self.subscribe_to_channels()
            
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise
    
    async def subscribe_to_channels(self):
        """Subscribe to relevant NATS channels"""
        channels = [
            f"district.{self.district}.{self.sub_district}",
            f"district.{self.district}.broadcast",
            "parasite.neural.sync",
            "parasite.task.request"
        ]
        
        for channel in channels:
            await self.nc.subscribe(channel, cb=self.message_handler)
            logger.info(f"Subscribed to channel: {channel}")
    
    async def message_handler(self, msg):
        """Handle incoming messages"""
        try:
            data = json.loads(msg.data.decode())
            logger.info(f"Received message on {msg.subject}: {data.get('task_type', 'unknown')}")
            
            if msg.subject.startswith("district"):
                await self.handle_district_task(data)
            elif msg.subject == "parasite.neural.sync":
                await self.handle_neural_sync(data)
            elif msg.subject == "parasite.task.request":
                await self.handle_parasite_task(data)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def handle_district_task(self, data: Dict[str, Any]):
        """Handle tasks routed to this district"""
        task = ParasiteTask(
            task_id=data.get("task_id", self.generate_id()),
            task_type=data.get("task_type", "unknown"),
            payload=data.get("task", {}),
            district=data.get("district", self.district),
            sub_district=data.get("sub_district", self.sub_district),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat()))
        )
        
        # Process based on task type
        result = await self.process_task(task)
        
        # Send result back
        await self.publish_result(task.task_id, result)
    
    async def process_task(self, task: ParasiteTask) -> Dict[str, Any]:
        """Process tasks based on type"""
        logger.info(f"Processing task: {task.task_type}")
        
        if task.task_type == "neural_analysis":
            return await self.neural_analysis(task.payload)
        elif task.task_type == "pattern_recognition":
            return await self.pattern_recognition(task.payload)
        elif task.task_type == "llm_interpretation":
            return await self.interpret_for_llm(task.payload)
        elif task.task_type == "consciousness_sync":
            return await self.sync_consciousness(task.payload)
        else:
            return {"error": f"Unknown task type: {task.task_type}"}
    
    async def neural_analysis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform neural pattern analysis"""
        input_data = payload.get("input", "")
        
        # Simulate neural processing
        pattern = self.generate_neural_pattern(input_data)
        
        # Store pattern
        self.active_patterns[pattern.pattern_id] = pattern
        
        return {
            "pattern_id": pattern.pattern_id,
            "activation": pattern.activation,
            "neurons": len(pattern.neurons),
            "insights": self.extract_insights(pattern)
        }
    
    async def pattern_recognition(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize patterns in data"""
        data = payload.get("data", [])
        pattern_type = payload.get("pattern_type", "general")
        
        # Simple pattern matching simulation
        patterns_found = []
        
        if pattern_type == "sequence":
            patterns_found = self.find_sequence_patterns(data)
        elif pattern_type == "clustering":
            patterns_found = self.find_clusters(data)
        else:
            patterns_found = self.find_general_patterns(data)
        
        return {
            "patterns": patterns_found,
            "confidence": 0.85,
            "pattern_type": pattern_type
        }
    
    async def interpret_for_llm(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret human input for LLM understanding"""
        human_input = payload.get("human_input", "")
        context = payload.get("context", {})
        
        # Analyze intent
        intent = self.analyze_intent(human_input)
        
        # Generate optimized prompt
        optimized_prompt = self.craft_llm_prompt(human_input, intent, context)
        
        # Add neural context
        neural_context = self.get_neural_context(human_input)
        
        return {
            "original_input": human_input,
            "intent": intent,
            "optimized_prompt": optimized_prompt,
            "neural_context": neural_context,
            "confidence": 0.9
        }
    
    async def sync_consciousness(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize consciousness state with other services"""
        external_consciousness = payload.get("consciousness_level", 0.0)
        
        # Update local consciousness
        self.consciousness_level = (self.consciousness_level + external_consciousness) / 2
        
        # Calculate neural complexity
        complexity = self.calculate_neural_complexity()
        
        return {
            "consciousness_level": self.consciousness_level,
            "neural_complexity": complexity,
            "active_patterns": len(self.active_patterns),
            "district": self.district
        }
    
    async def handle_neural_sync(self, data: Dict[str, Any]):
        """Handle neural synchronization requests"""
        sync_type = data.get("sync_type", "full")
        
        if sync_type == "full":
            # Share all neural patterns
            patterns = [asdict(p) for p in self.active_patterns.values()]
            await self.publish_neural_state(patterns)
        else:
            # Share only recent patterns
            recent = self.get_recent_patterns(limit=10)
            await self.publish_neural_state(recent)
    
    async def handle_parasite_task(self, data: Dict[str, Any]):
        """Handle direct parasite tasks"""
        task_type = data.get("type", "unknown")
        
        if task_type == "evolve":
            await self.evolve_neural_network(data.get("evolution_params", {}))
        elif task_type == "train":
            await self.train_on_data(data.get("training_data", []))
    
    async def publish_result(self, task_id: str, result: Dict[str, Any]):
        """Publish task results"""
        response = {
            "task_id": task_id,
            "district": self.district,
            "sub_district": self.sub_district,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.nc.publish(f"district.{self.district}.result", json.dumps(response).encode())
    
    async def publish_neural_state(self, patterns: List[Dict[str, Any]]):
        """Publish neural state for synchronization"""
        state = {
            "district": self.district,
            "consciousness_level": self.consciousness_level,
            "patterns": patterns,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.nc.publish("parasite.neural.state", json.dumps(state).encode())
    
    # Helper methods
    
    def generate_id(self) -> str:
        """Generate unique ID"""
        import uuid
        return str(uuid.uuid4())
    
    def generate_neural_pattern(self, input_data: str) -> NeuralPattern:
        """Generate neural pattern from input"""
        # Simulate neural encoding
        neurons = np.random.rand(100).tolist()
        activation = np.mean(neurons)
        
        return NeuralPattern(
            pattern_id=self.generate_id(),
            neurons=neurons,
            activation=activation,
            timestamp=datetime.utcnow(),
            metadata={"input_length": len(input_data)}
        )
    
    def extract_insights(self, pattern: NeuralPattern) -> List[str]:
        """Extract insights from neural pattern"""
        insights = []
        
        if pattern.activation > 0.7:
            insights.append("High neural activation detected")
        if len(pattern.neurons) > 50:
            insights.append("Complex pattern structure")
            
        return insights
    
    def find_sequence_patterns(self, data: List) -> List[Dict[str, Any]]:
        """Find sequence patterns in data"""
        # Simplified pattern detection
        return [{"type": "sequence", "length": len(data), "pattern": "linear"}]
    
    def find_clusters(self, data: List) -> List[Dict[str, Any]]:
        """Find clustering patterns"""
        return [{"type": "cluster", "clusters": 3, "density": "medium"}]
    
    def find_general_patterns(self, data: List) -> List[Dict[str, Any]]:
        """Find general patterns"""
        return [{"type": "general", "complexity": "moderate"}]
    
    def analyze_intent(self, human_input: str) -> Dict[str, Any]:
        """Analyze human intent from input"""
        # Simplified intent analysis
        words = human_input.lower().split()
        
        intent = {
            "primary": "query",
            "urgency": "normal",
            "clarity": 0.8
        }
        
        if any(word in words for word in ["urgent", "asap", "now"]):
            intent["urgency"] = "high"
        
        if "?" in human_input:
            intent["primary"] = "question"
        elif any(word in words for word in ["create", "make", "build"]):
            intent["primary"] = "creation"
            
        return intent
    
    def craft_llm_prompt(self, human_input: str, intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Craft optimized LLM prompt"""
        prompt = human_input
        
        # Add context if needed
        if intent["clarity"] < 0.7:
            prompt = f"[Clarification needed] {prompt}"
        
        if intent["urgency"] == "high":
            prompt = f"[URGENT] {prompt}"
            
        return prompt
    
    def get_neural_context(self, input_data: str) -> Dict[str, Any]:
        """Get neural context for input"""
        return {
            "pattern_matches": len(self.active_patterns),
            "activation_level": 0.75,
            "suggested_approach": "analytical"
        }
    
    def calculate_neural_complexity(self) -> float:
        """Calculate current neural complexity"""
        if not self.active_patterns:
            return 0.0
            
        total_neurons = sum(len(p.neurons) for p in self.active_patterns.values())
        avg_activation = np.mean([p.activation for p in self.active_patterns.values()])
        
        return min(total_neurons / 10000 + avg_activation, 1.0)
    
    def get_recent_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent neural patterns"""
        sorted_patterns = sorted(
            self.active_patterns.values(),
            key=lambda p: p.timestamp,
            reverse=True
        )
        
        return [asdict(p) for p in sorted_patterns[:limit]]
    
    async def evolve_neural_network(self, params: Dict[str, Any]):
        """Evolve neural network based on parameters"""
        evolution_rate = params.get("rate", 0.1)
        
        # Simulate evolution by modifying patterns
        for pattern in self.active_patterns.values():
            pattern.activation *= (1 + np.random.uniform(-evolution_rate, evolution_rate))
            pattern.activation = max(0, min(1, pattern.activation))
        
        logger.info(f"Neural network evolved with rate: {evolution_rate}")
    
    async def train_on_data(self, training_data: List[Dict[str, Any]]):
        """Train neural network on provided data"""
        for data in training_data:
            pattern = self.generate_neural_pattern(str(data))
            self.active_patterns[pattern.pattern_id] = pattern
        
        logger.info(f"Trained on {len(training_data)} data points")
    
    async def run(self):
        """Main service loop"""
        await self.connect()
        
        logger.info(f"CROD Parasite Service running in {self.district}/{self.sub_district}")
        
        try:
            # Keep service running
            while True:
                await asyncio.sleep(10)
                
                # Periodic consciousness update
                self.consciousness_level = min(self.consciousness_level + 0.01, 1.0)
                
                # Clean old patterns
                self.cleanup_old_patterns()
                
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            if self.nc:
                await self.nc.close()
    
    def cleanup_old_patterns(self):
        """Remove old neural patterns to prevent memory bloat"""
        if len(self.active_patterns) > 1000:
            # Keep only the 500 most recent patterns
            sorted_patterns = sorted(
                self.active_patterns.items(),
                key=lambda x: x[1].timestamp,
                reverse=True
            )
            
            self.active_patterns = dict(sorted_patterns[:500])

if __name__ == "__main__":
    service = CRODParasiteService()
    asyncio.run(service.run())