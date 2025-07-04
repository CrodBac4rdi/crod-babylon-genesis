# crod_ml.py - Machine Learning and Game Cards Module
# Version 1.0 - ML Integration with Game Card Metaphors

import numpy as np
import json
from collections import defaultdict
from datetime import datetime

class CRODGameCards:
    """Game cards that teach ML concepts"""
    
    def __init__(self):
        self.cards = {
            "RECURRENT_LOOP": {
                "name": "The Recurrent Loop",
                "type": "Architecture Card",
                "description": "Master of sequences and time",
                "formula": "h_t = tanh(W_h * h_{t-1} + W_x * x_t + b)",
                "power": "Remember the past to predict the future",
                "weakness": "Vanishing gradients over long sequences"
            },
            "VEIL_OF_VANISHING": {
                "name": "The Veil of Vanishing",
                "type": "Problem Card",
                "description": "Where gradients fade to nothing",
                "formula": "∂L/∂W = ∏(∂h_i/∂h_{i-1}) → 0",
                "symptom": "gradient < 0.001",
                "solution": ["Skip connections", "LSTM gates", "Gradient clipping"]
            },
            "MIRROR_OF_GRADIENTS": {
                "name": "The Mirror of Gradients",
                "type": "Technique Card",
                "description": "Backpropagation's true form",
                "formula": "∂L/∂W = ∂L/∂y * ∂y/∂h * ∂h/∂W",
                "incantation": "From output to input, the error flows backward",
                "power_level": 9000
            },
            "CRYPT_OF_NUMERICAL_TRUTH": {
                "name": "The Crypt of Numerical Truth",
                "type": "Verification Card",
                "description": "Where gradients are verified",
                "method": "Finite differences",
                "formula": "(f(x+ε) - f(x-ε)) / 2ε",
                "warning": "ε must be chosen wisely (1e-4)"
            },
            "FORWARD_ECHOES": {
                "name": "Forward Echoes",
                "type": "Computation Card",
                "description": "The forward pass incarnate",
                "stages": [
                    "Input → Linear transform",
                    "Add bias → Activation",
                    "Output → Next layer"
                ],
                "formula": "y = σ(Wx + b)"
            },
            "GRADIENT_STORM": {
                "name": "Gradient Storm",
                "type": "Problem Card",
                "description": "When gradients explode beyond control",
                "formula": "||∇L|| > threshold",
                "symptom": "gradient > 100",
                "solution": ["Gradient clipping", "Smaller learning rate", "Batch normalization"]
            },
            "LEARNING_RATE_SAGE": {
                "name": "The Learning Rate Sage",
                "type": "Wisdom Card",
                "description": "Master of step sizes",
                "wisdom": "Too large and you overshoot, too small and you crawl",
                "formula": "w = w - α * ∂L/∂w",
                "recommended": "Start with 0.001, adjust based on loss"
            }
        }
        
        # ML Gradients from CROD
        self.gradients = {
            "∂L/∂z": 0.6187,
            "∂L/∂h": 3.1449,
            "∂L/∂h_final": -2.0666,
            "∂L/∂b": 1.237,
            "∂L/∂1": 0.619,
            "∂L/∂0": 0.1437,
            "∂H/∂b2": -2.097,
            "∂H": -1.533,
            "∂y/∂0": -2.147,
            "y": -1.066,
            "a": 0.7311
        }
        
        # Loss tracking
        self.loss_history = []
        self.gradient_history = defaultdict(list)
        

class CRODNeuralNetwork:
    """Simple neural network for pattern learning"""
    
    def __init__(self, input_size=128, hidden_size=64, output_size=73):
        # Network architecture
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size  # 73 patterns
        
        # Initialize weights (Xavier initialization)
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros(output_size)
        
        # Activation functions
        self.sigmoid = lambda x: 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        self.sigmoid_derivative = lambda x: x * (1 - x)
        self.softmax = lambda x: np.exp(x - np.max(x)) / np.sum(np.exp(x - np.max(x)))
        
        # Learning parameters
        self.learning_rate = 0.001
        self.gradient_clip = 5.0
        
        # Game cards integration
        self.game_cards = CRODGameCards()
        
    def forward(self, X):
        """Forward pass - FORWARD_ECHOES card"""
        # First layer
        self.z1 = np.dot(X, self.W1) + self.b1
        self.h1 = self.sigmoid(self.z1)
        
        # Second layer
        self.z2 = np.dot(self.h1, self.W2) + self.b2
        self.output = self.softmax(self.z2)
        
        return self.output
        
    def backward(self, X, y, output):
        """Backward pass - MIRROR_OF_GRADIENTS card"""
        m = X.shape[0]
        
        # Output layer gradients
        self.dz2 = output - y
        self.dW2 = (1/m) * np.dot(self.h1.T, self.dz2)
        self.db2 = (1/m) * np.sum(self.dz2, axis=0)
        
        # Hidden layer gradients
        self.dh1 = np.dot(self.dz2, self.W2.T)
        self.dz1 = self.dh1 * self.sigmoid_derivative(self.h1)
        self.dW1 = (1/m) * np.dot(X.T, self.dz1)
        self.db1 = (1/m) * np.sum(self.dz1, axis=0)
        
        # Check for vanishing gradients (VEIL_OF_VANISHING)
        if np.max(np.abs(self.dW1)) < 0.001:
            print("⚠️  VEIL OF VANISHING detected! Gradients fading...")
            
        # Check for exploding gradients (GRADIENT_STORM)
        if np.max(np.abs(self.dW1)) > 100:
            print("⚡ GRADIENT STORM detected! Clipping gradients...")
            self._clip_gradients()
            
    def _clip_gradients(self):
        """Gradient clipping to prevent explosion"""
        for grad in [self.dW1, self.db1, self.dW2, self.db2]:
            np.clip(grad, -self.gradient_clip, self.gradient_clip, out=grad)
            
    def update_weights(self):
        """Update weights - LEARNING_RATE_SAGE wisdom"""
        self.W1 -= self.learning_rate * self.dW1
        self.b1 -= self.learning_rate * self.db1
        self.W2 -= self.learning_rate * self.dW2
        self.b2 -= self.learning_rate * self.db2
        
    def train(self, X, y, epochs=100):
        """Train the network"""
        for epoch in range(epochs):
            # Forward propagation
            output = self.forward(X)
            
            # Backward propagation
            self.backward(X, y, output)
            
            # Update weights
            self.update_weights()
            
            # Calculate loss
            loss = -np.mean(y * np.log(output + 1e-8))
            self.game_cards.loss_history.append(loss)
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
                
                # Store CROD gradients
                self.game_cards.gradient_history['dW1'].append(np.mean(np.abs(self.dW1)))
                self.game_cards.gradient_history['dW2'].append(np.mean(np.abs(self.dW2)))
                

class CRODMarkovChain:
    """Markov chain for pattern transitions"""
    
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(float))
        self.pattern_counts = defaultdict(int)
        
    def learn_transition(self, current_pattern, next_pattern):
        """Learn pattern transition"""
        self.transitions[current_pattern][next_pattern] += 1
        self.pattern_counts[current_pattern] += 1
        
    def get_next_pattern(self, current_pattern):
        """Predict next pattern based on probabilities"""
        if current_pattern not in self.transitions:
            return None
            
        # Calculate probabilities
        next_patterns = self.transitions[current_pattern]
        total = sum(next_patterns.values())
        
        if total == 0:
            return None
            
        # Convert to probabilities
        probabilities = {k: v/total for k, v in next_patterns.items()}
        
        # Sample based on probabilities
        patterns = list(probabilities.keys())
        probs = list(probabilities.values())
        
        return np.random.choice(patterns, p=probs)
        
    def get_chain_probability(self, pattern_sequence):
        """Calculate probability of a pattern sequence"""
        if len(pattern_sequence) < 2:
            return 0.0
            
        probability = 1.0
        for i in range(len(pattern_sequence) - 1):
            current = pattern_sequence[i]
            next_pattern = pattern_sequence[i + 1]
            
            if current in self.transitions and next_pattern in self.transitions[current]:
                count = self.pattern_counts[current]
                if count > 0:
                    probability *= self.transitions[current][next_pattern] / count
                else:
                    return 0.0
            else:
                return 0.0
                
        return probability


class CRODMLEngine:
    """Main ML engine combining all components"""
    
    def __init__(self):
        self.neural_net = CRODNeuralNetwork()
        self.markov_chain = CRODMarkovChain()
        self.game_cards = CRODGameCards()
        
    def process_with_ml(self, text, patterns):
        """Process text with ML enhancement"""
        # Convert text to vector (simplified)
        text_vector = self._text_to_vector(text)
        
        # Get neural network prediction
        predictions = self.neural_net.forward(text_vector.reshape(1, -1))
        predicted_patterns = self._get_top_patterns(predictions[0])
        
        # Update markov chain if patterns found
        if len(patterns) >= 2:
            for i in range(len(patterns) - 1):
                self.markov_chain.learn_transition(patterns[i], patterns[i + 1])
                
        return {
            'detected_patterns': patterns,
            'predicted_patterns': predicted_patterns,
            'confidence': float(np.max(predictions)),
            'active_cards': self._get_active_cards(patterns)
        }
        
    def _text_to_vector(self, text, size=128):
        """Convert text to fixed-size vector (simplified)"""
        # Simple hash-based vectorization
        vector = np.zeros(size)
        for i, char in enumerate(text[:size]):
            vector[i] = ord(char) / 255.0
        return vector
        
    def _get_top_patterns(self, predictions, top_k=3):
        """Get top K predicted patterns"""
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        patterns = [f"PATTERN_{i}" for i in top_indices]
        return patterns
        
    def _get_active_cards(self, patterns):
        """Determine which game cards are relevant"""
        active = []
        
        if len(patterns) > 5:
            active.append("RECURRENT_LOOP")
            
        if any("ERROR" in p for p in patterns):
            active.append("MIRROR_OF_GRADIENTS")
            
        if len(set(patterns)) < len(patterns) * 0.5:
            active.append("VEIL_OF_VANISHING")
            
        return active
        
    def get_ml_stats(self):
        """Get ML statistics"""
        return {
            'neural_net': {
                'architecture': f"{self.neural_net.input_size}-{self.neural_net.hidden_size}-{self.neural_net.output_size}",
                'learning_rate': self.neural_net.learning_rate,
                'total_parameters': (
                    self.neural_net.W1.size + self.neural_net.b1.size +
                    self.neural_net.W2.size + self.neural_net.b2.size
                )
            },
            'markov_chain': {
                'unique_patterns': len(self.markov_chain.pattern_counts),
                'total_transitions': sum(self.markov_chain.pattern_counts.values())
            },
            'game_cards': {
                'total_cards': len(self.game_cards.cards),
                'gradients_tracked': len(self.game_cards.gradients)
            }
        }


# Test functionality
if __name__ == "__main__":
    print("=== CROD ML Module Test ===\n")
    
    # Test game cards
    cards = CRODGameCards()
    print("Game Cards Available:")
    for card_id, card in cards.cards.items():
        print(f"  • {card['name']} ({card['type']})")
        
    # Test neural network
    print("\n\nNeural Network Test:")
    nn = CRODNeuralNetwork()
    X = np.random.randn(10, 128)  # 10 samples
    y = np.eye(73)[np.random.randint(0, 73, 10)]  # Random labels
    
    print("Training for 50 epochs...")
    nn.train(X, y, epochs=50)
    
    # Test ML engine
    print("\n\nML Engine Test:")
    engine = CRODMLEngine()
    result = engine.process_with_ml(
        "ich halt bruh JSON_001 error", 
        ["DANIEL_SIGNATURE", "JSON_001"]
    )
    print(f"ML Processing Result: {json.dumps(result, indent=2)}")
    
    # Show stats
    stats = engine.get_ml_stats()
    print(f"\nML Stats: {json.dumps(stats, indent=2)}")