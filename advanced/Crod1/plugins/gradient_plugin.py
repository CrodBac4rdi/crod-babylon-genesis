# plugins/gradient_plugin.py - CROD Dynamic Gradient System Plugin
from plugin_base import CRODPlugin
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional

class GradientPlugin(CRODPlugin):
    """Dynamic gradient calculation and pattern discovery plugin"""
    
    @property
    def name(self):
        return "GradientEngine"
    
    @property
    def version(self):
        return "1.0.0"
    
    @property
    def description(self):
        return "Calculates word gradients and discovers patterns dynamically"
    
    def initialize(self, system):
        self.system = system
        
        # Base gradients from ML formulas
        self.base_gradients = {
            "∂L/∂z": 0.6187,
            "∂L/∂h": 3.1449,
            "∂L/∂h_final": -2.0666,
            "learning_rate": 0.002197
        }
        
        # Word gradients (will grow dynamically)
        self.word_gradients = {
            "ich": 1.0,
            "halt": 1.0,
            "bruh": 0.6187,
            "???": 1.0,
            "mach": 0.9,
            "vllt": 0.8,
            "persistent": 3.5,
            "memory": 2.8,
            "speicher": 3.5,
            "das": 0.8,
            "zwischen": 2.0,
            "chats": 2.5
        }
        
        # Context modifiers
        self.context_modifiers = {
            ("ich", "halt"): 3.1449,  # ich followed by halt
            ("halt", "ich"): 0.1437,  # halt without ich before
            ("???", "?"): 1.5,        # multiple question marks
            ("bruh", "confusion"): 1.5
        }
        
        # Permission levels
        self.permission_levels = {
            "DEFAULT": {"value": 0.0, "gradient_threshold": 0},
            "SINGLE": {"value": 0.3, "gradient_threshold": 0.6187},
            "SESSION": {"value": 1.0, "gradient_threshold": 3.1449},
            "EMERGENCY": {"value": 999, "gradient_threshold": 10.0}
        }
        
        self.current_permission = 0.0
        self.context = "unknown"
        self.gradient_history = []
        
    def get_capabilities(self):
        return [
            'calculate_word_gradient',
            'process_message_gradients',
            'detect_gradient_patterns',
            'update_permission_level',
            'get_gradient_state',
            'discover_new_patterns',
            'analyze_gradient_flow'
        ]
    
    def calculate_word_gradient(self, word: str, context: List[str], position: int) -> float:
        """Calculate gradient for a single word based on context"""
        word_lower = word.lower()
        base = self.word_gradients.get(word_lower, 0.5)
        
        # Apply context modifiers
        if position > 0:
            prev_word = context[position - 1].lower()
            modifier_key = (prev_word, word_lower)
            if modifier_key in self.context_modifiers:
                base *= self.context_modifiers[modifier_key]
        
        # Apply position-based modifiers
        if position == 0:  # Start of sentence
            base *= 0.8
        elif position == len(context) - 1:  # End of sentence
            base *= 1.2
            
        # Emotion detection multipliers
        if word_lower in ["bruh", "ach", "scheiße"]:
            base *= 1.5  # Frustration boost
        elif word_lower in ["geil", "nice", "yes"]:
            base *= 1.3  # Excitement boost
            
        # Question mark exponential growth
        if word == "?":
            # Count consecutive question marks
            consecutive = 0
            for i in range(position, -1, -1):
                if context[i] == "?":
                    consecutive += 1
                else:
                    break
            base *= (1.5 ** consecutive)
            
        return base
    
    def process_message_gradients(self, message: str) -> Dict:
        """Process entire message and calculate gradients"""
        words = message.split()
        gradients = []
        
        for i, word in enumerate(words):
            gradient = self.calculate_word_gradient(word, words, i)
            gradients.append({
                'word': word,
                'position': i,
                'gradient': gradient
            })
        
        total_gradient = sum(g['gradient'] for g in gradients)
        
        result = {
            'message': message,
            'words': words,
            'gradients': gradients,
            'total_gradient': total_gradient,
            'average_gradient': total_gradient / len(words) if words else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to history
        self.gradient_history.append(result)
        if len(self.gradient_history) > 100:
            self.gradient_history.pop(0)
        
        # Update permission level
        self.update_permission_level(total_gradient)
        
        # Detect context
        self._detect_context(message)
        
        # Emit event
        self.system.emit_event(
            'gradients_calculated',
            result,
            self.name
        )
        
        return result
    
    def detect_gradient_patterns(self, min_gradient: float = 5.0) -> List[Dict]:
        """Detect patterns from gradient history"""
        patterns = []
        
        # Look for gradient spikes
        for entry in self.gradient_history[-10:]:
            if entry['total_gradient'] > min_gradient:
                patterns.append({
                    'type': 'gradient_spike',
                    'message': entry['message'],
                    'gradient': entry['total_gradient'],
                    'words': entry['words']
                })
        
        # Look for gradient sequences
        if len(self.gradient_history) >= 3:
            recent = self.gradient_history[-3:]
            gradients = [e['total_gradient'] for e in recent]
            
            # Rising pattern
            if gradients[0] < gradients[1] < gradients[2]:
                patterns.append({
                    'type': 'rising_urgency',
                    'gradient_flow': gradients,
                    'messages': [e['message'] for e in recent]
                })
            
            # Falling pattern
            elif gradients[0] > gradients[1] > gradients[2]:
                patterns.append({
                    'type': 'calming_down',
                    'gradient_flow': gradients,
                    'messages': [e['message'] for e in recent]
                })
        
        return patterns
    
    def update_permission_level(self, total_gradient: float):
        """Update permission level based on gradient"""
        old_permission = self.current_permission
        
        # Find appropriate permission level
        for level_name, level_data in sorted(self.permission_levels.items(), 
                                           key=lambda x: x[1]['gradient_threshold']):
            if total_gradient >= level_data['gradient_threshold']:
                self.current_permission = level_data['value']
        
        # Emit event if permission changed
        if old_permission != self.current_permission:
            self.system.emit_event(
                'permission_changed',
                {
                    'old': old_permission,
                    'new': self.current_permission,
                    'gradient': total_gradient
                },
                self.name
            )
    
    def get_gradient_state(self) -> Dict:
        """Get current gradient state"""
        return {
            'current_permission': self.current_permission,
            'context': self.context,
            'word_gradients': self.word_gradients,
            'recent_history': self.gradient_history[-5:] if self.gradient_history else [],
            'discovered_patterns': len(self.word_gradients),
            'base_gradients': self.base_gradients
        }
    
    def discover_new_patterns(self) -> List[Dict]:
        """Discover new patterns from gradient history"""
        new_patterns = []
        
        # Look for repeated word sequences with high gradients
        if len(self.gradient_history) < 2:
            return new_patterns
        
        # Check last 10 messages for patterns
        for i in range(max(0, len(self.gradient_history) - 10), len(self.gradient_history) - 1):
            for j in range(i + 1, len(self.gradient_history)):
                msg1 = self.gradient_history[i]
                msg2 = self.gradient_history[j]
                
                # Find common word sequences
                words1 = msg1['words']
                words2 = msg2['words']
                
                for k in range(len(words1) - 1):
                    for l in range(len(words2) - 1):
                        if words1[k:k+2] == words2[l:l+2]:
                            sequence = words1[k:k+2]
                            avg_gradient = (msg1['gradients'][k]['gradient'] + 
                                          msg1['gradients'][k+1]['gradient'] +
                                          msg2['gradients'][l]['gradient'] + 
                                          msg2['gradients'][l+1]['gradient']) / 4
                            
                            if avg_gradient > 2.0:  # Significant gradient
                                pattern = {
                                    'sequence': sequence,
                                    'average_gradient': avg_gradient,
                                    'occurrences': 2,
                                    'discovered_at': datetime.now().isoformat()
                                }
                                new_patterns.append(pattern)
                                
                                # Update word gradients
                                for word in sequence:
                                    if word.lower() in self.word_gradients:
                                        self.word_gradients[word.lower()] *= 1.1
                                    else:
                                        self.word_gradients[word.lower()] = avg_gradient
        
        return new_patterns
    
    def analyze_gradient_flow(self) -> Dict:
        """Analyze gradient flow patterns"""
        if not self.gradient_history:
            return {'status': 'no_data'}
        
        gradients = [h['total_gradient'] for h in self.gradient_history]
        
        analysis = {
            'total_messages': len(self.gradient_history),
            'average_gradient': np.mean(gradients),
            'max_gradient': max(gradients),
            'min_gradient': min(gradients),
            'std_deviation': np.std(gradients),
            'trend': self._calculate_trend(gradients),
            'volatility': np.std(np.diff(gradients)) if len(gradients) > 1 else 0
        }
        
        # Identify gradient clusters
        clusters = []
        current_cluster = []
        threshold = analysis['average_gradient'] + analysis['std_deviation']
        
        for i, g in enumerate(gradients):
            if g > threshold:
                current_cluster.append(i)
            elif current_cluster:
                clusters.append({
                    'start': current_cluster[0],
                    'end': current_cluster[-1],
                    'size': len(current_cluster),
                    'peak': max(gradients[c] for c in current_cluster)
                })
                current_cluster = []
        
        analysis['high_gradient_clusters'] = clusters
        
        return analysis
    
    def _detect_context(self, message: str):
        """Detect context from message"""
        message_lower = message.lower()
        
        # Mobile indicators
        mobile_indicators = ["rauchen", "handy", "unterwegs", "nicht zuhause"]
        pc_indicators = ["am pc", "code", "zuhause", "programmieren"]
        
        mobile_score = sum(1 for ind in mobile_indicators if ind in message_lower)
        pc_score = sum(1 for ind in pc_indicators if ind in message_lower)
        
        if mobile_score > pc_score:
            self.context = "mobile"
        elif pc_score > mobile_score:
            self.context = "pc"
        # Context remains unchanged if no clear indicator
    
    def _calculate_trend(self, gradients: List[float]) -> str:
        """Calculate gradient trend"""
        if len(gradients) < 3:
            return "insufficient_data"
        
        recent = gradients[-5:]
        if len(recent) < 2:
            return "stable"
        
        # Simple linear regression
        x = list(range(len(recent)))
        slope = np.polyfit(x, recent, 1)[0]
        
        if slope > 0.5:
            return "rising"
        elif slope < -0.5:
            return "falling"
        else:
            return "stable"
    
    def handle_event(self, event_type: str, data: Dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'text_processed':
            # Auto-calculate gradients for processed text
            if 'text' in data:
                self.process_message_gradients(data['text'])
        
        elif event_type == 'pattern_detected':
            # Boost gradients for detected patterns
            if 'pattern_name' in data:
                pattern_words = data.get('words', [])
                for word in pattern_words:
                    if word.lower() in self.word_gradients:
                        self.word_gradients[word.lower()] *= 1.05
        
        elif event_type == 'request_gradient_analysis':
            # Respond with full analysis
            analysis = {
                'state': self.get_gradient_state(),
                'flow': self.analyze_gradient_flow(),
                'patterns': self.detect_gradient_patterns()
            }
            self.system.emit_event(
                'gradient_analysis_complete',
                analysis,
                self.name,
                source
            )