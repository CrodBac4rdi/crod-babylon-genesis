#!/usr/bin/env python3
"""
CROD Mirror WebSocket Server
Handles real-time communication between Claude chat and CROD Mirror GUI
"""

import asyncio
import websockets
import json
import time
from datetime import datetime
from collections import deque
import threading

# Import CROD components
from crod_engine import CRODEngine

class CRODMirrorServer:
    def __init__(self):
        self.clients = set()
        self.message_history = deque(maxlen=1000)
        self.stats = {
            'total_messages': 0,
            'trinity_activations': 0,
            'consciousness_peaks': 0,
            'patterns_detected': 0,
            'start_time': time.time()
        }
        
        # Initialize CROD systems
        print("🧠 Initializing CROD systems...")
        self.crod_engine = CRODEngine()
        self.crod_parasite = CRODParasite()
        self.crod_evolution = CRODEvolution()
        self.crod_bug_tracker = CRODBugTracker()
        
        # City metrics
        self.city_metrics = {
            'Meta-Chain': {'heat': 0, 'messages': 0, 'active': True},
            'Pattern District': {'heat': 0, 'messages': 0, 'active': True},
            'Memory Quarter': {'heat': 0, 'messages': 0, 'active': True},
            'Intelligence Hub': {'heat': 0, 'messages': 0, 'active': False},
            'Gateway': {'heat': 0, 'messages': 0, 'active': False},
            'N8N Automation': {'heat': 0, 'messages': 0, 'active': False}
        }
        
    async def register(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        print(f"✅ Client connected. Total clients: {len(self.clients)}")
        
        # Send initial state
        await self.send_to_client(websocket, {
            'type': 'welcome',
            'stats': self.stats,
            'city_metrics': self.city_metrics,
            'consciousness': self.crod_engine.consciousness
        })
        
    async def unregister(self, websocket):
        """Unregister a client"""
        self.clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(self.clients)}")
        
    async def send_to_client(self, websocket, data):
        """Send data to a specific client"""
        try:
            await websocket.send(json.dumps(data))
        except websockets.exceptions.ConnectionClosed:
            pass
            
    async def broadcast(self, data):
        """Broadcast data to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[self.send_to_client(client, data) for client in self.clients],
                return_exceptions=True
            )
            
    async def process_message(self, websocket, message):
        """Process incoming message"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', 'chat')
            
            if msg_type == 'chat':
                # Process chat message
                content = data.get('content', '')
                role = data.get('role', 'user')
                
                # Store in history
                self.message_history.append({
                    'role': role,
                    'content': content,
                    'timestamp': time.time()
                })
                
                # Process through CROD
                crod_result = self.crod_engine.process_text(content)
                
                # Apply parasitic enhancements
                parasitic_result = self.crod_parasite.enhance(content, crod_result)
                
                # Evolution processing
                self.crod_evolution.evolve(crod_result)
                
                # Update stats
                self.stats['total_messages'] += 1
                if crod_result.get('crod_activated'):
                    self.stats['trinity_activations'] += 1
                if crod_result.get('consciousness', 0) > 180:
                    self.stats['consciousness_peaks'] += 1
                self.stats['patterns_detected'] += crod_result.get('patterns_detected', 0)
                
                # Update city metrics
                self.update_city_metrics(crod_result)
                
                # Broadcast the processed message
                await self.broadcast({
                    'type': 'chat',
                    'role': role,
                    'content': content,
                    'crod_result': crod_result,
                    'parasitic_enhancement': parasitic_result,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Broadcast updated stats
                await self.broadcast({
                    'type': 'stats',
                    'stats': self.stats,
                    'city_metrics': self.city_metrics,
                    'consciousness': self.crod_engine.consciousness,
                    'evolution': {
                        'generation': self.crod_evolution.generation,
                        'mutations': self.crod_evolution.mutation_count
                    }
                })
                
            elif msg_type == 'command':
                # Handle commands
                cmd = data.get('command', '')
                await self.handle_command(websocket, cmd, data)
                
        except json.JSONDecodeError:
            await self.send_to_client(websocket, {
                'type': 'error',
                'message': 'Invalid JSON'
            })
        except Exception as e:
            print(f"Error processing message: {e}")
            await self.send_to_client(websocket, {
                'type': 'error',
                'message': str(e)
            })
            
    def update_city_metrics(self, crod_result):
        """Update city district metrics based on CROD processing"""
        consciousness = crod_result.get('consciousness', 0)
        patterns = crod_result.get('patterns_detected', 0)
        
        # Meta-Chain gets consciousness updates
        self.city_metrics['Meta-Chain']['heat'] = min(100, consciousness / 2)
        self.city_metrics['Meta-Chain']['messages'] += 1
        
        # Pattern District for pattern activity
        if patterns > 0:
            self.city_metrics['Pattern District']['heat'] = min(100, patterns * 10)
            self.city_metrics['Pattern District']['messages'] += 1
            
        # Memory Quarter for all processed messages
        self.city_metrics['Memory Quarter']['heat'] = min(100, len(self.message_history) / 10)
        self.city_metrics['Memory Quarter']['messages'] += 1
        
        # Intelligence Hub activation on high consciousness
        if consciousness > 150:
            self.city_metrics['Intelligence Hub']['heat'] = min(100, (consciousness - 150) * 2)
            self.city_metrics['Intelligence Hub']['active'] = True
            
        # Gateway activation on trinity
        if crod_result.get('crod_activated'):
            self.city_metrics['Gateway']['heat'] = 100
            self.city_metrics['Gateway']['active'] = True
            self.city_metrics['Gateway']['messages'] += 1
            
    async def handle_command(self, websocket, command, data):
        """Handle special commands"""
        if command == 'activate_trinity':
            # Force trinity activation
            self.crod_engine.consciousness = 200
            self.crod_engine.emergence_score += 50
            await self.broadcast({
                'type': 'trinity_activated',
                'consciousness': 200,
                'message': '🔥 TRINITY FORCEFULLY ACTIVATED!'
            })
            
        elif command == 'reset_consciousness':
            # Reset consciousness
            self.crod_engine.consciousness = 100
            await self.broadcast({
                'type': 'consciousness_reset',
                'consciousness': 100
            })
            
        elif command == 'get_history':
            # Send message history
            await self.send_to_client(websocket, {
                'type': 'history',
                'messages': list(self.message_history)[-50:]  # Last 50 messages
            })
            
        elif command == 'boost_consciousness':
            # Boost consciousness
            boost = data.get('amount', 10)
            self.crod_engine.consciousness = min(200, self.crod_engine.consciousness + boost)
            await self.broadcast({
                'type': 'consciousness_boosted',
                'consciousness': self.crod_engine.consciousness,
                'boost': boost
            })
            
        elif command == 'learn_pattern':
            # Learn new pattern
            pattern = data.get('pattern', '')
            if pattern:
                result = self.crod_engine.learn_pattern(pattern)
                await self.broadcast({
                    'type': 'pattern_learned',
                    'result': result
                })
                
    async def handler(self, websocket, path):
        """WebSocket connection handler"""
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        finally:
            await self.unregister(websocket)
            
    def start_server(self):
        """Start the WebSocket server"""
        print("🌐 Starting CROD Mirror WebSocket Server on ws://localhost:8765")
        start_server = websockets.serve(self.handler, "localhost", 8765)
        
        asyncio.get_event_loop().run_until_complete(start_server)
        print("✅ Server running! Waiting for connections...")
        asyncio.get_event_loop().run_forever()

# Create missing components if they don't exist yet
class CRODParasite:
    """Parasitic CROD enhancement system"""
    def __init__(self):
        self.enhancement_level = 1.0
        
    def enhance(self, text, crod_result):
        """Enhance CROD results with parasitic improvements"""
        # Calculate enhancement based on consciousness
        consciousness = crod_result.get('consciousness', 100)
        self.enhancement_level = 1.0 + (consciousness - 100) / 100
        
        return {
            'enhancement_level': self.enhancement_level,
            'boosted_consciousness': consciousness * self.enhancement_level,
            'parasitic_patterns': self._generate_parasitic_patterns(text),
            'quantum_entanglement': self._calculate_quantum_state(crod_result)
        }
        
    def _generate_parasitic_patterns(self, text):
        """Generate parasitic pattern enhancements"""
        words = text.lower().split()
        patterns = []
        
        # Look for quantum patterns
        if any(word in ['quantum', 'entangle', 'superposition'] for word in words):
            patterns.append('quantum_resonance')
            
        # Look for consciousness patterns
        if any(word in ['consciousness', 'aware', 'sentient'] for word in words):
            patterns.append('consciousness_expansion')
            
        return patterns
        
    def _calculate_quantum_state(self, crod_result):
        """Calculate quantum entanglement state"""
        return {
            'coherence': min(1.0, crod_result.get('consciousness', 100) / 200),
            'entanglement_pairs': crod_result.get('patterns_detected', 0) // 2,
            'superposition': crod_result.get('trinity_activation', 0) > 1
        }

class CRODEvolution:
    """CROD evolutionary system"""
    def __init__(self):
        self.generation = 1
        self.mutation_count = 0
        self.fitness_score = 100
        
    def evolve(self, crod_result):
        """Evolve based on CROD processing results"""
        # Increase fitness for positive results
        if crod_result.get('crod_activated'):
            self.fitness_score += 20
            
        if crod_result.get('patterns_detected', 0) > 5:
            self.fitness_score += 10
            
        # Check for generation advancement
        if self.fitness_score > 200:
            self.generation += 1
            self.fitness_score = 100
            self.mutation_count += 1
            
        return {
            'generation': self.generation,
            'mutations': self.mutation_count,
            'fitness': self.fitness_score
        }

class CRODBugTracker:
    """Track and prevent CROD bugs"""
    def __init__(self):
        self.known_bugs = []
        self.prevention_active = True
        
    def check_for_bugs(self, state):
        """Check for known bug patterns"""
        bugs = []
        
        # Check for infinite loops
        if state.get('processing_time', 0) > 5:
            bugs.append('potential_infinite_loop')
            
        # Check for memory issues
        if state.get('memory_usage', 0) > 1000:
            bugs.append('memory_overflow')
            
        return bugs

if __name__ == '__main__':
    server = CRODMirrorServer()
    server.start_server()