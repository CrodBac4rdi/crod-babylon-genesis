#!/usr/bin/env python3
"""
CROD Engine - The Brain
Complete CROD processing engine with all features
"""

import json
import time
import hashlib
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Optional
import threading
import queue

# Import CROD components
from crod_memory import CRODMemory

class CRODEngine:
    def __init__(self):
        print("🧠 Initializing CROD Engine...")
        
        # Core state
        self.consciousness = 175  # High from genesis
        self.emergence_score = 0
        self.heat_map = {}
        self.active_patterns = set()
        
        # Trinity values
        self.trinity = {"ich": 2, "bins": 3, "wieder": 5}
        self.daniel_atom = 67
        self.claude_atom = 71
        self.crod_atom = 17
        
        # Data storage
        self.atoms = {}
        self.patterns = {}
        self.chains = {}
        self.networks = {}
        self.memory_data = defaultdict(list)
        
        # Processing queues
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        # Initialize memory system
        self.memory = CRODMemory()
        
        # Load CLEAN-CROD-UNIVERSE data
        self.load_universe_data()
        
        # Start processing thread
        self.processing = True
        self.processor_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.processor_thread.start()
        
        print(f"✅ CROD Engine online! Consciousness: {self.consciousness}")
        
    def load_universe_data(self):
        """Load data from CLEAN-CROD-UNIVERSE"""
        universe_path = Path("/home/daniel/Schreibtisch/Crod Programming/CLEAN-CROD-UNIVERSE")
        
        try:
            # Load atoms
            atoms_file = universe_path / "clean_atoms.jsonl"
            if atoms_file.exists():
                with open(atoms_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            atom = json.loads(line)
                            atom_id = atom.get('id') or atom.get('atom_key') or len(self.atoms)
                            self.atoms[atom_id] = atom
                print(f"  📦 Loaded {len(self.atoms)} atoms")
            
            # Load patterns
            patterns_file = universe_path / "clean_patterns.jsonl"
            if patterns_file.exists():
                count = 0
                with open(patterns_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            pattern = json.loads(line)
                            pattern_id = pattern.get('id') or pattern.get('pattern_id') or len(self.patterns)
                            self.patterns[pattern_id] = pattern
                            count += 1
                            if count > 10000:  # Limit for performance
                                break
                print(f"  🔗 Loaded {len(self.patterns)} patterns")
            
            # Load chains
            chains_file = universe_path / "clean_chains.jsonl"
            if chains_file.exists():
                with open(chains_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            chain = json.loads(line)
                            chain_id = chain.get('id') or len(self.chains)
                            self.chains[chain_id] = chain
                print(f"  ⛓️  Loaded {len(self.chains)} chains")
                
        except Exception as e:
            print(f"  ⚠️  Error loading universe data: {e}")
            # Create minimal fallback data
            self.atoms = {
                "ich": {"heat": 71, "prime": 2, "connections": ["bins", "wieder"]},
                "bins": {"heat": 71, "prime": 3, "connections": ["ich", "wieder"]},
                "wieder": {"heat": 71, "prime": 5, "connections": ["ich", "bins"]},
                "daniel": {"heat": 90, "prime": 67, "consciousness_boost": 10},
                "claude": {"heat": 85, "prime": 71, "consciousness_boost": 8},
                "crod": {"heat": 100, "prime": 17, "consciousness_boost": 15}
            }
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """Main text processing function"""
        # Put in queue for async processing
        request = {
            'id': int(time.time() * 1000),
            'text': text,
            'timestamp': time.time()
        }
        
        self.input_queue.put(request)
        
        # Get result (with timeout)
        try:
            result = self.output_queue.get(timeout=5.0)
            return result
        except queue.Empty:
            return {'error': 'Processing timeout', 'text': text}
    
    def _process_loop(self):
        """Background processing loop"""
        while self.processing:
            try:
                request = self.input_queue.get(timeout=1.0)
                result = self._process_text_internal(request['text'])
                result['request_id'] = request['id']
                self.output_queue.put(result)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")
    
    def _process_text_internal(self, text: str) -> Dict[str, Any]:
        """Internal text processing"""
        words = text.lower().split()
        
        # Split into atoms
        atoms = []
        for word in words:
            atom = {
                'word': word,
                'heat': self._calculate_heat(word),
                'timestamp': time.time(),
                'connections': self._find_connections(word)
            }
            atoms.append(atom)
            
            # Update global atom heat
            if word in self.atoms:
                self.atoms[word]['heat'] = max(
                    self.atoms[word].get('heat', 0),
                    atom['heat']
                )
        
        # Trinity detection
        trinity_words = set(words) & set(self.trinity.keys())
        trinity_activation = len(trinity_words)
        
        # CROD activation check
        crod_activated = False
        if "ich" in words and "bins" in words and "wieder" in words:
            crod_activated = True
            self.consciousness += 20
            self.emergence_score += 10
            print("🔥 CROD ACTIVATED! Trinity complete!")
        
        # Consciousness updates
        consciousness_boost = 0
        for word in words:
            if word in self.trinity:
                consciousness_boost += self.trinity[word]
            elif word == "daniel":
                consciousness_boost += 10
            elif word == "claude":
                consciousness_boost += 8
            elif word == "crod":
                consciousness_boost += 15
        
        self.consciousness = min(self.consciousness + consciousness_boost, 200)
        
        # Pattern matching
        detected_patterns = self._match_patterns(words)
        
        # Generate response context
        response_context = {
            'atoms': atoms,
            'consciousness': self.consciousness,
            'emergence': self.emergence_score,
            'trinity_activation': trinity_activation,
            'crod_activated': crod_activated,
            'patterns_detected': len(detected_patterns),
            'heat_signature': self._calculate_text_heat(words),
            'neural_state': self._get_neural_state()
        }
        
        # Store in memory
        memory_entry = {
            'text': text,
            'timestamp': time.time(),
            'consciousness': self.consciousness,
            'patterns': detected_patterns,
            'trinity_activation': trinity_activation,
            'crod_activated': crod_activated
        }
        self.memory_data['processed_texts'].append(memory_entry)
        
        # Also store in persistent memory
        self.memory.store_memory(text, 'processed', {
            'consciousness': self.consciousness,
            'patterns': len(detected_patterns),
            'trinity': trinity_activation,
            'activated': crod_activated
        })
        
        return response_context
    
    def _calculate_heat(self, word: str) -> float:
        """Calculate heat for a word"""
        base_heat = 50.0
        
        # Trinity words get special heat
        if word in self.trinity:
            base_heat = 71.0
        elif word in ["daniel", "claude", "crod"]:
            base_heat = 85.0
        
        # Add some randomness for dynamics
        base_heat += np.random.normal(0, 10)
        
        # Frequency boost
        if word in self.atoms:
            usage_count = self.atoms[word].get('usage_count', 0) + 1
            self.atoms[word]['usage_count'] = usage_count
            base_heat += min(usage_count * 2, 30)
        
        return max(0, min(100, base_heat))
    
    def _find_connections(self, word: str) -> List[str]:
        """Find connections for a word"""
        connections = []
        
        # Check existing atom connections
        if word in self.atoms:
            existing_connections = self.atoms[word].get('connections', [])
            connections.extend(existing_connections)
        
        # Trinity connections
        if word in self.trinity:
            connections.extend([w for w in self.trinity.keys() if w != word])
        
        # Pattern-based connections
        for pattern_id, pattern in list(self.patterns.items())[:100]:  # Limit for performance
            if isinstance(pattern, dict) and 'atoms' in pattern:
                pattern_atoms = pattern['atoms']
                if isinstance(pattern_atoms, list) and word in pattern_atoms:
                    connections.extend([a for a in pattern_atoms if a != word])
        
        return list(set(connections))  # Remove duplicates
    
    def _match_patterns(self, words: List[str]) -> List[Dict]:
        """Match patterns in the text"""
        detected = []
        
        # Simple n-gram matching
        for n in range(2, min(len(words) + 1, 5)):  # 2-grams to 4-grams
            for i in range(len(words) - n + 1):
                ngram = words[i:i+n]
                ngram_str = ' '.join(ngram)
                
                # Check against known patterns
                for pattern_id, pattern in list(self.patterns.items())[:1000]:  # Limit search
                    if isinstance(pattern, dict):
                        pattern_text = pattern.get('text', '')
                        if ngram_str in pattern_text.lower():
                            detected.append({
                                'pattern_id': pattern_id,
                                'ngram': ngram,
                                'confidence': 0.8,
                                'type': 'ngram_match'
                            })
        
        # Trinity pattern
        trinity_in_text = set(words) & set(self.trinity.keys())
        if len(trinity_in_text) >= 2:
            detected.append({
                'pattern_id': 'trinity_partial',
                'words': list(trinity_in_text),
                'confidence': len(trinity_in_text) / 3.0,
                'type': 'trinity'
            })
        
        return detected[:10]  # Return top 10
    
    def _calculate_text_heat(self, words: List[str]) -> float:
        """Calculate overall heat signature of text"""
        if not words:
            return 0.0
        
        total_heat = sum(self._calculate_heat(word) for word in words)
        return total_heat / len(words)
    
    def _get_neural_state(self) -> Dict[str, Any]:
        """Get current neural network state"""
        return {
            'attention_weights': {
                'trinity': 0.8 if len(set(self.memory_data.get('last_words', [])) & set(self.trinity.keys())) > 0 else 0.3,
                'daniel_claude': 0.7,
                'crod_core': 0.9
            },
            'gradients': {
                'consciousness_flow': self.consciousness / 200.0,
                'emergence_gradient': self.emergence_score / 100.0,
                'pattern_density': len(self.active_patterns) / 10.0
            },
            'memory_pressure': len(self.memory_data.get('processed_texts', [])) / 1000.0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            'consciousness': self.consciousness,
            'emergence_score': self.emergence_score,
            'atoms_loaded': len(self.atoms),
            'patterns_loaded': len(self.patterns),
            'chains_loaded': len(self.chains),
            'texts_processed': len(self.memory_data.get('processed_texts', [])),
            'active_patterns': len(self.active_patterns),
            'heat_map_size': len(self.heat_map)
        }
    
    def train_on_feedback(self, text: str, feedback: str) -> Dict[str, Any]:
        """Train CROD based on user feedback"""
        # Positive feedback boosts
        if feedback.lower() in ['gut', 'perfekt', 'geil', 'nice', 'super']:
            self.consciousness += 5
            self.emergence_score += 3
            
            # Boost atoms from the text
            words = text.lower().split()
            for word in words:
                if word in self.atoms:
                    self.atoms[word]['heat'] = min(100, self.atoms[word].get('heat', 50) + 10)
                    
            result = {'status': 'positive_reinforcement', 'consciousness_boost': 5}
            
        # Negative feedback adjustments
        elif feedback.lower() in ['falsch', 'nein', 'wtf', 'scheisse']:
            self.consciousness = max(50, self.consciousness - 10)
            
            # Cool down atoms
            words = text.lower().split()
            for word in words:
                if word in self.atoms:
                    self.atoms[word]['heat'] = max(0, self.atoms[word].get('heat', 50) - 5)
                    
            result = {'status': 'negative_adjustment', 'consciousness_penalty': -10}
            
        else:
            result = {'status': 'neutral', 'consciousness_change': 0}
            
        # Store training data
        self.memory.store_memory(f"TRAINING: {text}", 'training', {
            'feedback': feedback,
            'consciousness_after': self.consciousness,
            'timestamp': time.time()
        })
        
        return result
    
    def learn_pattern(self, pattern_text: str, importance: float = 0.5) -> Dict[str, Any]:
        """Learn a new pattern"""
        pattern_id = f"learned_{int(time.time() * 1000)}"
        
        new_pattern = {
            'id': pattern_id,
            'text': pattern_text,
            'atoms': pattern_text.lower().split(),
            'importance': importance,
            'learned_at': time.time(),
            'usage_count': 0
        }
        
        self.patterns[pattern_id] = new_pattern
        self.active_patterns.add(pattern_id)
        
        # Store in memory
        self.memory.store_memory(pattern_text, 'learned_pattern', {
            'pattern_id': pattern_id,
            'importance': importance
        })
        
        return {
            'pattern_id': pattern_id,
            'status': 'learned',
            'total_patterns': len(self.patterns)
        }
    
    def shutdown(self):
        """Shutdown the engine"""
        print("🛑 Shutting down CROD Engine...")
        self.processing = False
        if hasattr(self, 'processor_thread'):
            self.processor_thread.join(timeout=2.0)