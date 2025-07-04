# plugins/chat_plugin.py - CROD Chat Plugin
from plugin_base import CRODPlugin
import re
from datetime import datetime
from typing import Dict, List, Any

class ChatPlugin(CRODPlugin):
    """Chat processing and analysis plugin"""
    
    @property
    def name(self):
        return "Chat"
    
    @property
    def version(self):
        return "2.0.0"
    
    @property
    def description(self):
        return "Process chat messages and detect moods, language switches"
    
    def initialize(self, system):
        self.system = system
        self.message_history = []
        self.mood_indicators = {
            'excited': ['yes yes yes', '!!!', '^^', 'hahaha', 'lol', 'awesome'],
            'frustrated': ['ach', 'scheiße', 'bruh', 'ey', 'meh', 'ugh'],
            'thinking': ['...', 'hmm', 'idk', 'maybe', 'perhaps'],
            'satisfied': ['nice', 'perfect', 'good', 'great', 'works'],
            'confused': ['?', 'hä', 'what', 'wie', 'huh']
        }
        self.german_words = ['ich', 'halt', 'auch', 'nicht', 'das', 'ist', 'aber', 'oder', 'wenn']
    
    def get_capabilities(self):
        return [
            'process_message',
            'detect_mood',
            'detect_language',
            'get_message_history',
            'analyze_session',
            'extract_keywords'
        ]
    
    def process_message(self, text: str, user: str = 'user') -> Dict:
        """Process a chat message"""
        timestamp = datetime.now()
        
        # Analyze message
        analysis = {
            'text': text,
            'user': user,
            'timestamp': timestamp.isoformat(),
            'mood': self.detect_mood(text),
            'language': self.detect_language(text),
            'keywords': self.extract_keywords(text),
            'length': len(text),
            'words': len(text.split())
        }
        
        # Store in history
        self.message_history.append(analysis)
        
        # Emit event
        self.system.emit_event(
            'message_processed',
            analysis,
            self.name
        )
        
        # Request pattern detection if available
        if 'detect_patterns' in self.system.capability_map:
            self.system.emit_event(
                'request_pattern_detection',
                {'text': text},
                self.name,
                self.system.capability_map['detect_patterns'][0]
            )
        
        return analysis
    
    def detect_mood(self, text: str) -> Dict:
        """Detect mood from text"""
        text_lower = text.lower()
        mood_scores = {}
        
        for mood, indicators in self.mood_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in text_lower:
                    score += 1
            mood_scores[mood] = score
        
        # Find dominant mood
        dominant_mood = max(mood_scores, key=mood_scores.get) if any(mood_scores.values()) else 'neutral'
        confidence = mood_scores[dominant_mood] / max(len(text.split()), 1)
        
        return {
            'mood': dominant_mood,
            'confidence': min(confidence, 1.0),
            'scores': mood_scores
        }
    
    def detect_language(self, text: str) -> Dict:
        """Detect language (German/English mix)"""
        words = text.lower().split()
        german_count = sum(1 for word in words if word in self.german_words)
        
        # Special patterns
        has_umlauts = bool(re.search(r'[äöüÄÖÜß]', text))
        
        german_ratio = german_count / len(words) if words else 0
        
        return {
            'primary': 'german' if german_ratio > 0.3 or has_umlauts else 'english',
            'german_ratio': german_ratio,
            'has_umlauts': has_umlauts,
            'mixed': german_ratio > 0.1 and german_ratio < 0.9
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords"""
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'der', 'die', 'das', 'und', 'oder', 'aber', 'in', 'auf', 'zu', 'für'}
        
        words = text.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in stopwords]
        
        return list(set(keywords))
    
    def get_message_history(self, limit: int = 50) -> List[Dict]:
        """Get message history"""
        return self.message_history[-limit:]
    
    def analyze_session(self) -> Dict:
        """Analyze the current chat session"""
        if not self.message_history:
            return {'status': 'no_messages'}
        
        total_messages = len(self.message_history)
        
        # Mood distribution
        mood_counts = {}
        for msg in self.message_history:
            mood = msg['mood']['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        # Language distribution
        language_counts = {'english': 0, 'german': 0, 'mixed': 0}
        for msg in self.message_history:
            if msg['language']['mixed']:
                language_counts['mixed'] += 1
            else:
                language_counts[msg['language']['primary']] += 1
        
        # Keywords frequency
        all_keywords = []
        for msg in self.message_history:
            all_keywords.extend(msg['keywords'])
        
        keyword_freq = {}
        for kw in all_keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        
        # Sort by frequency
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_messages': total_messages,
            'mood_distribution': mood_counts,
            'language_distribution': language_counts,
            'top_keywords': top_keywords,
            'session_duration': self._calculate_duration(),
            'average_message_length': sum(msg['length'] for msg in self.message_history) / total_messages
        }
    
    def _calculate_duration(self) -> str:
        """Calculate session duration"""
        if len(self.message_history) < 2:
            return "0:00:00"
        
        first = datetime.fromisoformat(self.message_history[0]['timestamp'])
        last = datetime.fromisoformat(self.message_history[-1]['timestamp'])
        duration = last - first
        
        return str(duration)
    
    def handle_event(self, event_type: str, data: Dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'pattern_detection_complete':
            # Store pattern info with the last message
            if self.message_history and data.get('patterns'):
                self.message_history[-1]['detected_patterns'] = data['patterns']
                
                # Emit enriched message event
                self.system.emit_event(
                    'message_enriched',
                    self.message_history[-1],
                    self.name
                )