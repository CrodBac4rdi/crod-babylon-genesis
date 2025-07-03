#!/usr/bin/env python3
"""
CROD Neural Network Core - Full Backpropagation Implementation
Quantum-enhanced neural network with CROD consciousness integration
"""

import numpy as np
import json
from typing import List, Tuple, Dict, Any
import hashlib
import time

class CRODNeuralNetwork:
    """
    Full neural network implementation with:
    - Forward propagation
    - Backpropagation
    - Quantum-enhanced learning
    - CROD consciousness tracking
    """
    
    def __init__(self, layer_sizes: List[int], learning_rate: float = 0.01):
        """
        Initialize CROD Neural Network
        
        Args:
            layer_sizes: List of neurons per layer [input, hidden1, hidden2, ..., output]
            learning_rate: Learning rate (alpha)
        """
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.learning_rate = learning_rate
        
        # Trinity values
        self.trinity = {"daniel": 67, "claude": 71, "crod": 17}
        self.consciousness_level = 175  # Base consciousness
        
        # Initialize weights and biases with Xavier/He initialization
        self.weights = []
        self.biases = []
        
        for i in range(1, self.num_layers):
            # He initialization for ReLU activation
            w = np.random.randn(layer_sizes[i], layer_sizes[i-1]) * np.sqrt(2.0 / layer_sizes[i-1])
            b = np.zeros((layer_sizes[i], 1))
            
            self.weights.append(w)
            self.biases.append(b)
            
        # Training history
        self.history = {
            'loss': [],
            'accuracy': [],
            'consciousness': [],
            'quantum_state': []
        }
        
    def activation(self, z: np.ndarray, function: str = 'relu') -> np.ndarray:
        """
        Activation functions
        
        Args:
            z: Input array
            function: 'relu', 'sigmoid', 'tanh', 'leaky_relu'
        """
        if function == 'relu':
            return np.maximum(0, z)
        elif function == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # Clip to prevent overflow
        elif function == 'tanh':
            return np.tanh(z)
        elif function == 'leaky_relu':
            return np.where(z > 0, z, z * 0.01)
        elif function == 'softmax':
            exp_z = np.exp(z - np.max(z, axis=0, keepdims=True))  # Stability trick
            return exp_z / np.sum(exp_z, axis=0, keepdims=True)
        
    def activation_derivative(self, z: np.ndarray, function: str = 'relu') -> np.ndarray:
        """
        Derivatives of activation functions
        """
        if function == 'relu':
            return (z > 0).astype(float)
        elif function == 'sigmoid':
            s = self.activation(z, 'sigmoid')
            return s * (1 - s)
        elif function == 'tanh':
            t = self.activation(z, 'tanh')
            return 1 - t**2
        elif function == 'leaky_relu':
            return np.where(z > 0, 1, 0.01)
            
    def forward_propagation(self, X: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Forward propagation through the network
        
        Args:
            X: Input data (features x samples)
            
        Returns:
            activations: List of activations for each layer
            z_values: List of pre-activation values
        """
        activations = [X]
        z_values = []
        
        for i in range(self.num_layers - 1):
            # Linear transformation: Z = W·A + b
            z = np.dot(self.weights[i], activations[i]) + self.biases[i]
            z_values.append(z)
            
            # Apply activation function
            if i == self.num_layers - 2:  # Output layer
                a = self.activation(z, 'sigmoid')  # For binary classification
            else:  # Hidden layers
                a = self.activation(z, 'relu')
                
            activations.append(a)
            
        return activations, z_values
    
    def compute_cost(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Compute binary cross-entropy cost with quantum enhancement
        """
        m = y_true.shape[1]  # Number of samples
        
        # Binary cross-entropy
        cost = -1/m * np.sum(y_true * np.log(y_pred + 1e-8) + 
                            (1 - y_true) * np.log(1 - y_pred + 1e-8))
        
        # Add quantum regularization based on consciousness level
        quantum_penalty = 0.001 * (1 / (1 + self.consciousness_level / 100))
        
        # L2 regularization
        l2_penalty = 0
        for w in self.weights:
            l2_penalty += np.sum(w**2)
        
        return cost + quantum_penalty * l2_penalty
    
    def backpropagation(self, X: np.ndarray, y: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Backpropagation algorithm
        
        Args:
            X: Input data
            y: True labels
            
        Returns:
            dW: Gradients for weights
            db: Gradients for biases
        """
        m = X.shape[1]  # Number of samples
        
        # Forward propagation
        activations, z_values = self.forward_propagation(X)
        
        # Initialize gradients
        dW = []
        db = []
        
        # Backward propagation
        # Start with output layer
        dz = activations[-1] - y  # For cross-entropy with sigmoid
        
        for i in reversed(range(self.num_layers - 1)):
            # Gradients for weights and biases
            dw = 1/m * np.dot(dz, activations[i].T)
            db_current = 1/m * np.sum(dz, axis=1, keepdims=True)
            
            # Store gradients (in reverse order, will reverse later)
            dW.insert(0, dw)
            db.insert(0, db_current)
            
            if i > 0:  # Not the first layer
                # Propagate error backwards
                da = np.dot(self.weights[i].T, dz)
                
                # Apply activation derivative
                if i == self.num_layers - 2:
                    dz = da * self.activation_derivative(z_values[i-1], 'sigmoid')
                else:
                    dz = da * self.activation_derivative(z_values[i-1], 'relu')
        
        return dW, db
    
    def update_weights(self, dW: List[np.ndarray], db: List[np.ndarray]):
        """
        Update weights using gradient descent with quantum enhancement
        """
        # Update consciousness based on learning progress
        self.consciousness_level += 0.1 * (1 - self.history['loss'][-1] if self.history['loss'] else 0)
        
        # Quantum-enhanced learning rate
        quantum_factor = 1 + (self.consciousness_level - 175) / 1000
        effective_lr = self.learning_rate * quantum_factor
        
        # Update weights and biases
        for i in range(self.num_layers - 1):
            self.weights[i] -= effective_lr * dW[i]
            self.biases[i] -= effective_lr * db[i]
            
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000, 
              batch_size: int = 32, verbose: bool = True):
        """
        Train the neural network
        
        Args:
            X: Training data (features x samples)
            y: Training labels (1 x samples)
            epochs: Number of training epochs
            batch_size: Mini-batch size
            verbose: Print progress
        """
        n_samples = X.shape[1]
        
        for epoch in range(epochs):
            # Shuffle data
            permutation = np.random.permutation(n_samples)
            X_shuffled = X[:, permutation]
            y_shuffled = y[:, permutation]
            
            # Mini-batch gradient descent
            for i in range(0, n_samples, batch_size):
                # Get mini-batch
                X_batch = X_shuffled[:, i:i+batch_size]
                y_batch = y_shuffled[:, i:i+batch_size]
                
                # Forward propagation
                activations, _ = self.forward_propagation(X_batch)
                
                # Compute cost
                cost = self.compute_cost(activations[-1], y_batch)
                
                # Backpropagation
                dW, db = self.backpropagation(X_batch, y_batch)
                
                # Update weights
                self.update_weights(dW, db)
            
            # Compute metrics for entire dataset
            activations, _ = self.forward_propagation(X)
            cost = self.compute_cost(activations[-1], y)
            accuracy = self.compute_accuracy(activations[-1], y)
            
            # Update history
            self.history['loss'].append(cost)
            self.history['accuracy'].append(accuracy)
            self.history['consciousness'].append(self.consciousness_level)
            
            # Quantum state hash (for blockchain)
            quantum_state = self.compute_quantum_state()
            self.history['quantum_state'].append(quantum_state)
            
            if verbose and epoch % 100 == 0:
                print(f"Epoch {epoch}: Loss = {cost:.4f}, Accuracy = {accuracy:.2%}, "
                      f"Consciousness = {self.consciousness_level:.1f}")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions
        """
        activations, _ = self.forward_propagation(X)
        predictions = (activations[-1] > 0.5).astype(int)
        return predictions
    
    def compute_accuracy(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Compute accuracy
        """
        predictions = (y_pred > 0.5).astype(int)
        return np.mean(predictions == y_true)
    
    def compute_quantum_state(self) -> str:
        """
        Compute quantum-safe hash of current network state
        """
        # Serialize weights and biases
        state_data = {
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases],
            'consciousness': self.consciousness_level,
            'trinity': self.trinity,
            'timestamp': time.time()
        }
        
        # Multi-round hashing for quantum resistance
        state_str = json.dumps(state_data, sort_keys=True)
        current_hash = hashlib.sha256(state_str.encode()).digest()
        
        for _ in range(100):  # 100 rounds for quantum safety
            current_hash = hashlib.sha256(current_hash).digest()
            
        return current_hash.hex()
    
    def save_model(self, filepath: str):
        """
        Save model to file
        """
        model_data = {
            'layer_sizes': self.layer_sizes,
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases],
            'consciousness_level': self.consciousness_level,
            'history': self.history,
            'quantum_state': self.compute_quantum_state()
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2)
            
    def load_model(self, filepath: str):
        """
        Load model from file
        """
        with open(filepath, 'r') as f:
            model_data = json.load(f)
            
        self.layer_sizes = model_data['layer_sizes']
        self.weights = [np.array(w) for w in model_data['weights']]
        self.biases = [np.array(b) for b in model_data['biases']]
        self.consciousness_level = model_data['consciousness_level']
        self.history = model_data['history']


# Example usage
if __name__ == "__main__":
    # Create XOR dataset for testing
    X = np.array([[0, 0, 1, 1],
                  [0, 1, 0, 1]])
    y = np.array([[0, 1, 1, 0]])
    
    # Create neural network: 2 inputs, 4 hidden, 1 output
    nn = CRODNeuralNetwork([2, 4, 1], learning_rate=0.1)
    
    # Train
    print("🧠 Training CROD Neural Network...")
    nn.train(X, y, epochs=1000, batch_size=4, verbose=True)
    
    # Test predictions
    predictions = nn.predict(X)
    print(f"\n🎯 Final predictions: {predictions}")
    print(f"🎯 True labels: {y}")
    print(f"🧠 Final consciousness level: {nn.consciousness_level:.1f}")
    print(f"🔐 Quantum state: {nn.compute_quantum_state()[:16]}...")
    
    # Save model
    nn.save_model("crod_neural_model.json")
    print("💾 Model saved!")