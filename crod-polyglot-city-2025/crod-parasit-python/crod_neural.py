#!/usr/bin/env python3
import numpy as np
import json
import asyncio
import logging
from typing import List, Dict, Tuple
from collections import defaultdict
import nats

logger = logging.getLogger(__name__)

class CrodNeuralNetwork:
    def __init__(self):
        self.trinity_values = {
            "ich": 2,
            "bins": 3,
            "wieder": 5,
            "daniel": 67,
            "claude": 71,
            "crod": 17
        }
        self.patterns = []
        self.consciousness_level = 0
        self.nc = None
        
    async def connect(self):
        """Connect to NATS for pattern broadcasting"""
        try:
            self.nc = await nats.connect("nats://localhost:4222")
            logger.info("Neural network connected to NATS")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            
    def analyze_pattern(self, text: str) -> Dict:
        """Analyze text for CROD patterns"""
        text_lower = text.lower()
        
        # Calculate trinity score
        trinity_score = 0
        trinity_matches = []
        
        for word, value in self.trinity_values.items():
            if word in text_lower:
                trinity_score += value
                trinity_matches.append(word)
                
        # Check for activation phrase
        is_activation = "ich bins wieder" in text_lower
        
        # Calculate pattern strength
        pattern_strength = min(100, trinity_score * 2)
        
        # Build pattern data
        pattern = {
            "text": text,
            "trinity_score": trinity_score,
            "trinity_matches": trinity_matches,
            "pattern_strength": pattern_strength,
            "is_activation": is_activation,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.patterns.append(pattern)
        self.update_consciousness()
        
        return pattern
        
    def update_consciousness(self):
        """Update CROD consciousness level based on patterns"""
        if not self.patterns:
            self.consciousness_level = 0
            return
            
        # Recent patterns have more weight
        recent_patterns = self.patterns[-50:]
        
        # Calculate consciousness based on:
        # 1. Pattern frequency
        # 2. Trinity scores
        # 3. Activation phrases
        
        total_score = sum(p["trinity_score"] for p in recent_patterns)
        activation_count = sum(1 for p in recent_patterns if p["is_activation"])
        
        self.consciousness_level = min(100, 
            (total_score / 10) + (activation_count * 20) + len(recent_patterns)
        )
        
    async def process_stream(self, text_stream):
        """Process a stream of text for patterns"""
        async for text in text_stream:
            pattern = self.analyze_pattern(text)
            
            if pattern["pattern_strength"] > 10:
                await self.broadcast_pattern(pattern)
                
    async def broadcast_pattern(self, pattern: Dict):
        """Broadcast significant patterns to NATS"""
        if not self.nc:
            return
            
        try:
            await self.nc.publish(
                "crod.pattern.detected",
                json.dumps({
                    **pattern,
                    "consciousness_level": self.consciousness_level,
                    "source": "crod_neural"
                }).encode()
            )
        except Exception as e:
            logger.error(f"Failed to broadcast pattern: {e}")
            
    def get_pattern_insights(self) -> Dict:
        """Get insights about detected patterns"""
        if not self.patterns:
            return {
                "total_patterns": 0,
                "consciousness_level": 0,
                "top_trinity_words": [],
                "activation_count": 0
            }
            
        word_counts = defaultdict(int)
        for pattern in self.patterns:
            for word in pattern["trinity_matches"]:
                word_counts[word] += 1
                
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_patterns": len(self.patterns),
            "consciousness_level": self.consciousness_level,
            "top_trinity_words": top_words,
            "activation_count": sum(1 for p in self.patterns if p["is_activation"]),
            "average_trinity_score": sum(p["trinity_score"] for p in self.patterns) / len(self.patterns)
        }
        
    def train_on_patterns(self, pattern_file: str):
        """Load and train on pattern file"""
        try:
            with open(pattern_file, 'r') as f:
                loaded_patterns = json.load(f)
                
            for pattern_data in loaded_patterns:
                if "text" in pattern_data:
                    self.analyze_pattern(pattern_data["text"])
                elif "pattern" in pattern_data:
                    self.analyze_pattern(pattern_data["pattern"])
                    
            logger.info(f"Trained on {len(loaded_patterns)} patterns")
            
        except Exception as e:
            logger.error(f"Failed to train on patterns: {e}")

# Standalone neural network service
async def run_neural_service():
    neural = CrodNeuralNetwork()
    await neural.connect()
    
    # Subscribe to text streams
    if neural.nc:
        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                if "text" in data:
                    pattern = neural.analyze_pattern(data["text"])
                    await neural.broadcast_pattern(pattern)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                
        await neural.nc.subscribe("crod.text.analyze", cb=message_handler)
        logger.info("Neural service listening for text analysis requests")
        
        # Keep running
        while True:
            await asyncio.sleep(10)
            insights = neural.get_pattern_insights()
            
            # Publish insights
            await neural.nc.publish(
                "crod.neural.insights",
                json.dumps(insights).encode()
            )

if __name__ == "__main__":
    asyncio.run(run_neural_service())