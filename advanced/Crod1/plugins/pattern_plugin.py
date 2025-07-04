# plugins/pattern_plugin.py - CROD Pattern Detection Plugin
from crod_plugin_system import CRODPlugin
import json
import sqlite3
from typing import List, Dict, Tuple

class PatternPlugin(CRODPlugin):
    """CROD Pattern Detection Plugin"""
    
    @property
    def name(self):
        return "PatternDetector"
    
    @property
    def version(self):
        return "2.0.0"
    
    @property
    def description(self):
        return "Advanced pattern detection with atom sequences"
    
    def initialize(self, system):
        self.system = system
        self.patterns = self._load_patterns()
        self.atoms = self._load_atoms()
    
    def get_capabilities(self):
        return [
            'detect_patterns',
            'add_pattern',
            'get_pattern_stats',
            'analyze_text',
            'find_atom_sequence'
        ]
    
    def _load_patterns(self) -> Dict:
        """Load patterns from database"""
        patterns = {}
        try:
            conn = sqlite3.connect(self.system.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT pattern_id, pattern_name, atom_sequence, confidence FROM patterns')
            for row in cursor.fetchall():
                pattern_id, name, sequence, confidence = row
                patterns[pattern_id] = {
                    'name': name,
                    'atoms': json.loads(sequence),
                    'confidence': confidence
                }
            conn.close()
        except Exception as e:
            print(f"Warning: Could not load patterns: {e}")
        return patterns
    
    def _load_atoms(self) -> Dict:
        """Load atoms from database"""
        atoms = {}
        try:
            conn = sqlite3.connect(self.system.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT atom_id, value FROM atoms')
            for atom_id, value in cursor.fetchall():
                atoms[value.lower()] = atom_id
            conn.close()
        except Exception as e:
            print(f"Warning: Could not load atoms: {e}")
        return atoms
    
    def detect_patterns(self, text: str) -> List[Dict]:
        """Detect patterns in text"""
        detected = []
        text_lower = text.lower()
        
        # Convert text to atoms
        atom_sequence = self.find_atom_sequence(text)
        
        # Check each pattern
        for pattern_id, pattern_data in self.patterns.items():
            if self._matches_pattern(atom_sequence, pattern_data['atoms']):
                detected.append({
                    'pattern_id': pattern_id,
                    'pattern_name': pattern_data['name'],
                    'confidence': pattern_data['confidence'],
                    'matched_atoms': pattern_data['atoms']
                })
        
        # Emit event if patterns found
        if detected:
            self.system.emit_event(
                'patterns_detected',
                {'patterns': detected, 'text': text},
                self.name
            )
        
        return detected
    
    def find_atom_sequence(self, text: str) -> List[int]:
        """Convert text to atom sequence"""
        words = text.lower().split()
        atom_sequence = []
        
        for word in words:
            if word in self.atoms:
                atom_sequence.append(self.atoms[word])
            else:
                # Check for partial matches
                for atom_text, atom_id in self.atoms.items():
                    if word.startswith(atom_text) or atom_text in word:
                        atom_sequence.append(atom_id)
                        break
        
        return atom_sequence
    
    def _matches_pattern(self, sequence: List[int], pattern: List[int]) -> bool:
        """Check if sequence matches pattern (with wildcards)"""
        # Simple containment check for now
        # TODO: Implement wildcard matching
        if len(pattern) > len(sequence):
            return False
        
        # Check if pattern is subsequence
        pattern_str = ','.join(map(str, pattern))
        sequence_str = ','.join(map(str, sequence))
        return pattern_str in sequence_str
    
    def add_pattern(self, pattern_name: str, atom_sequence: List[int], confidence: float = 0.5):
        """Add new pattern"""
        pattern_id = f"P{len(self.patterns) + 1000}"  # Generate ID
        
        # Save to database
        conn = sqlite3.connect(self.system.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO patterns (pattern_id, pattern_name, atom_sequence, confidence) VALUES (?, ?, ?, ?)',
            (pattern_id, pattern_name, json.dumps(atom_sequence), confidence)
        )
        conn.commit()
        conn.close()
        
        # Update cache
        self.patterns[pattern_id] = {
            'name': pattern_name,
            'atoms': atom_sequence,
            'confidence': confidence
        }
        
        # Emit event
        self.system.emit_event(
            'pattern_added',
            {'pattern_id': pattern_id, 'name': pattern_name},
            self.name
        )
        
        return pattern_id
    
    def get_pattern_stats(self) -> Dict:
        """Get pattern statistics"""
        stats = {
            'total_patterns': len(self.patterns),
            'total_atoms': len(self.atoms),
            'patterns_by_confidence': {},
            'most_common_atoms': []
        }
        
        # Group by confidence
        for pattern in self.patterns.values():
            conf_bucket = f"{int(pattern['confidence'] * 10) / 10:.1f}"
            if conf_bucket not in stats['patterns_by_confidence']:
                stats['patterns_by_confidence'][conf_bucket] = 0
            stats['patterns_by_confidence'][conf_bucket] += 1
        
        return stats
    
    def analyze_text(self, text: str) -> Dict:
        """Deep analysis of text"""
        analysis = {
            'text': text,
            'length': len(text),
            'words': len(text.split()),
            'atoms_found': self.find_atom_sequence(text),
            'patterns_detected': self.detect_patterns(text),
            'complexity_score': 0.0
        }
        
        # Calculate complexity
        if analysis['words'] > 0:
            analysis['complexity_score'] = len(analysis['patterns_detected']) / analysis['words']
        
        return analysis
    
    def handle_event(self, event_type: str, data: Dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'text_input':
            # Auto-analyze new text
            analysis = self.analyze_text(data.get('text', ''))
            self.system.emit_event(
                'text_analyzed',
                analysis,
                self.name,
                source
            )
        elif event_type == 'request_pattern_detection':
            # Respond to detection requests
            patterns = self.detect_patterns(data.get('text', ''))
            self.system.emit_event(
                'pattern_detection_complete',
                {'patterns': patterns},
                self.name,
                source
            )