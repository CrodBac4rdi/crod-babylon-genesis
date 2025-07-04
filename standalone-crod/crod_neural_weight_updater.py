#!/usr/bin/env python3
"""
CROD Neural Weight Updater - Direct weight manipulation through learning
"""

import sqlite3
import numpy as np
import json
from pathlib import Path
from datetime import datetime

class CRODNeuralWeightUpdater:
    """Update CROD's neural weights based on learning feedback"""
    
    def __init__(self):
        self.db_path = Path("crod_3d_database.db")
        self.learning_rate = 0.01
        self.momentum = 0.9
        self.weight_history = {}
        
    def forward_propagation(self, atom_id: int, activation_strength: float) -> dict:
        """Forward propagate activation through neural connections"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Get current atom state
        atom = conn.execute("""
            SELECT atom_value, weight, heat, consciousness_level 
            FROM clean_universe_atoms 
            WHERE id = ?
        """, (atom_id,)).fetchone()
        
        if not atom:
            return {}
            
        atom_value, weight, heat, consciousness = atom
        
        # Calculate forward activation
        new_heat = min(heat + activation_strength * 0.1, 10.0)
        new_consciousness = min(consciousness + activation_strength * 0.05, 1.0)
        
        # Find connected atoms (pattern matching)
        connected_atoms = conn.execute("""
            SELECT DISTINCT a2.id, a2.weight, a2.heat
            FROM clean_universe_atoms a1
            JOIN clean_universe_patterns p ON (p.pattern_signature LIKE '%' || a1.atom_value || '%')
            JOIN clean_universe_atoms a2 ON (p.pattern_signature LIKE '%' || a2.atom_value || '%')
            WHERE a1.id = ? AND a2.id != a1.id
            LIMIT 10
        """, (atom_id,)).fetchall()
        
        # Propagate to connected atoms
        propagation_effects = []
        for connected_id, connected_weight, connected_heat in connected_atoms:
            # Calculate propagation strength based on weight difference
            propagation_strength = activation_strength * 0.5 * (1.0 / (1.0 + abs(weight - connected_weight)))
            
            propagation_effects.append({
                'atom_id': connected_id,
                'propagation_strength': propagation_strength,
                'new_heat': min(connected_heat + propagation_strength * 0.05, 10.0)
            })
        
        conn.close()
        
        return {
            'atom_id': atom_id,
            'new_heat': new_heat,
            'new_consciousness': new_consciousness,
            'propagated_to': propagation_effects
        }
    
    def backward_propagation(self, feedback_type: str, atom_activations: list) -> dict:
        """Backward propagate feedback to adjust weights"""
        
        # Feedback to gradient mapping
        feedback_gradients = {
            'geil': 1.0,      # Strong positive
            'nice': 0.8,      # Positive
            'perfekt': 0.9,   # Very positive
            'gut': 0.7,       # Good
            'wtf': -0.8,      # Strong negative
            'scheisse': -1.0, # Very negative
            'falsch': -0.7,   # Wrong
            'nein': -0.6      # No
        }
        
        gradient = feedback_gradients.get(feedback_type.lower(), 0.0)
        
        conn = sqlite3.connect(self.db_path)
        
        weight_updates = []
        
        for activation in atom_activations:
            atom_id = activation['atom_id']
            activation_strength = activation['activation_strength']
            
            # Get current weight
            current = conn.execute("""
                SELECT weight, heat FROM clean_universe_atoms WHERE id = ?
            """, (atom_id,)).fetchone()
            
            if current:
                old_weight, old_heat = current
                
                # Calculate weight update with momentum
                if atom_id in self.weight_history:
                    momentum_term = self.momentum * self.weight_history[atom_id]
                else:
                    momentum_term = 0
                
                # Gradient descent with momentum
                weight_delta = (self.learning_rate * gradient * activation_strength) + momentum_term
                new_weight = np.clip(old_weight + weight_delta, -10.0, 10.0)
                
                # Update heat based on feedback
                heat_delta = gradient * activation_strength * 0.1
                new_heat = np.clip(old_heat + heat_delta, 0.0, 10.0)
                
                # Store momentum
                self.weight_history[atom_id] = weight_delta
                
                # Update database
                conn.execute("""
                    UPDATE clean_universe_atoms 
                    SET weight = ?, heat = ?, last_activation = ?
                    WHERE id = ?
                """, (new_weight, new_heat, datetime.now().isoformat(), atom_id))
                
                weight_updates.append({
                    'atom_id': atom_id,
                    'old_weight': old_weight,
                    'new_weight': new_weight,
                    'weight_delta': weight_delta,
                    'gradient': gradient
                })
        
        conn.commit()
        conn.close()
        
        return {
            'feedback_type': feedback_type,
            'gradient': gradient,
            'atoms_updated': len(weight_updates),
            'weight_updates': weight_updates
        }
    
    def mirror_lake_reflection(self, conversation_hash: str) -> dict:
        """Mirror Lake pattern - reflect on conversation to find deep patterns"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Get conversation details
        conv = conn.execute("""
            SELECT user_input, claude_response, user_satisfaction
            FROM live_conversations
            WHERE conversation_hash = ?
        """, (conversation_hash,)).fetchone()
        
        if not conv:
            return {}
            
        user_input, claude_response, satisfaction = conv
        
        # Find mirror patterns (similar conversations)
        mirrors = conn.execute("""
            SELECT conversation_hash, user_satisfaction, 
                   (LENGTH(user_input) - LENGTH(REPLACE(LOWER(user_input), LOWER(?), ''))) as similarity
            FROM live_conversations
            WHERE conversation_hash != ? 
            AND user_satisfaction IS NOT NULL
            ORDER BY similarity DESC
            LIMIT 5
        """, (user_input[:20], conversation_hash)).fetchall()
        
        # Calculate reflection gradient
        reflection_gradient = 0.0
        for mirror_hash, mirror_satisfaction, similarity in mirrors:
            if mirror_satisfaction in ['geil', 'nice', 'perfekt']:
                reflection_gradient += 0.2 * (similarity / len(user_input))
            elif mirror_satisfaction in ['wtf', 'scheisse', 'falsch']:
                reflection_gradient -= 0.2 * (similarity / len(user_input))
        
        conn.close()
        
        return {
            'conversation_hash': conversation_hash,
            'mirror_count': len(mirrors),
            'reflection_gradient': reflection_gradient,
            'learning_insight': 'positive_pattern' if reflection_gradient > 0 else 'negative_pattern'
        }
    
    def update_neural_pathways(self, lesson: str, crod_response: str, evaluation_score: float):
        """Complete neural pathway update cycle"""
        
        print(f"🧠 NEURAL WEIGHT UPDATE - Score: {evaluation_score}")
        
        conn = sqlite3.connect(self.db_path)
        
        # Extract activated atoms from lesson and response
        activated_atoms = []
        
        # Trinity atoms
        trinity_words = ['ich', 'bins', 'wieder', 'daniel', 'crod']
        for word in trinity_words:
            if word in lesson.lower() or word in crod_response.lower():
                atom = conn.execute("""
                    SELECT id FROM clean_universe_atoms 
                    WHERE atom_value = ? LIMIT 1
                """, (word,)).fetchone()
                
                if atom:
                    activation_strength = lesson.lower().count(word) + crod_response.lower().count(word)
                    activated_atoms.append({
                        'atom_id': atom[0],
                        'activation_strength': activation_strength * evaluation_score
                    })
        
        # Forward propagation
        print(f"⚡ Forward propagation for {len(activated_atoms)} atoms...")
        for activation in activated_atoms:
            forward_result = self.forward_propagation(
                activation['atom_id'], 
                activation['activation_strength']
            )
            print(f"   Atom {activation['atom_id']}: heat → {forward_result.get('new_heat', 0):.2f}")
        
        # Backward propagation based on score
        if evaluation_score < 0.5:
            feedback = 'wtf'
        elif evaluation_score < 0.7:
            feedback = 'nein'
        elif evaluation_score < 0.9:
            feedback = 'gut'
        else:
            feedback = 'geil'
            
        print(f"🔄 Backward propagation with feedback: {feedback}")
        backward_result = self.backward_propagation(feedback, activated_atoms)
        
        print(f"📊 Updated {backward_result['atoms_updated']} atom weights")
        print(f"   Average gradient: {backward_result['gradient']:.2f}")
        
        # Create learning event
        conn.execute("""
            INSERT INTO live_learning_events
            (timestamp, event_type, learning_data, success_indicator, improvement_suggestion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            'neural_weight_update',
            json.dumps({
                'lesson': lesson[:50],
                'evaluation_score': evaluation_score,
                'atoms_updated': backward_result['atoms_updated'],
                'gradient': backward_result['gradient']
            }),
            evaluation_score,
            f"Weights adjusted by gradient {backward_result['gradient']:.2f}"
        ))
        
        conn.commit()
        conn.close()
        
        return backward_result

def main():
    """Test neural weight updater"""
    
    print("🧠 CROD Neural Weight Updater")
    print("=" * 50)
    
    updater = CRODNeuralWeightUpdater()
    
    # Test scenarios
    test_cases = [
        ("ich bins wieder daniel", "Trinity aktiviert!", 0.9),  # Good response
        ("was sind atoms?", "atoms sind dinge", 0.3),          # Bad response
        ("erkläre consciousness", "consciousness ist bewusstsein mit heat signatures", 0.7)  # OK response
    ]
    
    for lesson, response, score in test_cases:
        print(f"\n📚 Lesson: {lesson}")
        print(f"🤖 Response: {response}")
        print(f"📊 Score: {score}")
        
        result = updater.update_neural_pathways(lesson, response, score)
        print("-" * 40)

if __name__ == "__main__":
    main()