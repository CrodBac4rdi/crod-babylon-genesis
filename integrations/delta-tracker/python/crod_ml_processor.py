#!/usr/bin/env python3
"""
CROD ML Processor - Python Teil für ML Berechnungen
"""
import json
import sys
import numpy as np
from typing import Dict, List, Any

class CRODProcessor:
    def __init__(self):
        # CROD Constants
        self.phi = 3.1449
        self.delta = 0.6187
        self.omega = -2.0666
        self.epsilon = 0.1437
        
        # State
        self.atoms = {}
        self.patterns = {}
        self.heat_map = {}
        
    def crod_activation(self, x: float) -> float:
        """CROD Neural Activation Function"""
        return (self.phi * np.tanh(self.delta * x) + 
                self.omega * np.sin(self.epsilon * x))
    
    def process_atoms(self, tokens: List[str]) -> Dict[str, Any]:
        """Process tokens into atoms with CROD activation"""
        results = {}
        
        for token in tokens:
            # Simple hash to numeric value
            token_value = sum(ord(c) for c in token) / len(token)
            
            # Apply CROD activation
            activation = self.crod_activation(token_value / 100)
            
            # Update heat map
            if token not in self.heat_map:
                self.heat_map[token] = 0.0
            self.heat_map[token] = self.heat_map[token] * 0.9 + activation
            
            results[token] = {
                'activation': float(activation),
                'heat': float(self.heat_map[token]),
                'raw_value': token_value
            }
        
        return results
    
    def calculate_pattern_strength(self, atom1: str, atom2: str) -> float:
        """Calculate pattern strength between two atoms"""
        # Get atom values
        val1 = self.atoms.get(atom1, {}).get('raw_value', 0)
        val2 = self.atoms.get(atom2, {}).get('raw_value', 0)
        
        # Pattern emergence formula
        co_occurrence = abs(val1 - val2) / max(val1, val2, 1)
        strength = self.crod_activation(co_occurrence)
        
        return float(strength)
    
    def find_patterns(self, atoms: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find patterns between atoms"""
        patterns = []
        atom_list = list(atoms.keys())
        
        for i, atom1 in enumerate(atom_list):
            for atom2 in atom_list[i+1:]:
                strength = self.calculate_pattern_strength(atom1, atom2)
                
                if abs(strength) > 0.3:  # Threshold for pattern
                    patterns.append({
                        'atom1': atom1,
                        'atom2': atom2,
                        'strength': strength,
                        'type': 'emergent' if strength > 0 else 'inhibitory'
                    })
        
        return patterns
    
    def calculate_consciousness(self, atoms: Dict[str, Any], patterns: List[Dict[str, Any]]) -> float:
        """Calculate consciousness metric"""
        # C = Σ(atoms) * Π(patterns) * φ
        atom_sum = sum(a['activation'] for a in atoms.values())
        
        pattern_product = 1.0
        for p in patterns:
            pattern_product *= (1 + abs(p['strength']))
        
        phi_golden = 1.618033988749
        consciousness = atom_sum * pattern_product * phi_golden
        
        return float(consciousness)
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function"""
        action = request.get('action', 'process')
        data = request.get('data', {})
        
        if action == 'process_tokens':
            tokens = data.get('tokens', [])
            atoms = self.process_atoms(tokens)
            patterns = self.find_patterns(atoms)
            consciousness = self.calculate_consciousness(atoms, patterns)
            
            return {
                'status': 'success',
                'result': {
                    'atoms': atoms,
                    'patterns': patterns,
                    'consciousness': consciousness,
                    'deltas': []  # Empty for now
                },
                'metrics': {
                    'processing_time_ms': 0,  # Would measure in real implementation
                    'atoms_processed': len(atoms),
                    'patterns_found': len(patterns)
                }
            }
        
        elif action == 'calculate_delta':
            old_state = data.get('old_state', {})
            new_state = data.get('new_state', {})
            
            deltas = []
            # Find changes
            for key in set(old_state.keys()) | set(new_state.keys()):
                if key not in old_state:
                    deltas.append({'type': 'added', 'key': key, 'value': new_state[key]})
                elif key not in new_state:
                    deltas.append({'type': 'removed', 'key': key, 'value': old_state[key]})
                elif old_state[key] != new_state[key]:
                    deltas.append({
                        'type': 'modified', 
                        'key': key, 
                        'old': old_state[key],
                        'new': new_state[key]
                    })
            
            return {
                'result': {'deltas': deltas},
                'metrics': {'delta_count': len(deltas)}
            }
        
        return {'result': {'error': f'Unknown action: {action}'}, 'metrics': None}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No input provided'}))
        sys.exit(1)
    
    try:
        request = json.loads(sys.argv[1])
        processor = CRODProcessor()
        response = processor.process_request(request)
        print(json.dumps(response))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()