use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub user_preference: String,
    pub avoid: Vec<String>,
    pub tone: String,
    pub satisfaction_score: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Neuron {
    pub id: usize,
    pub value: f64,
    pub connections: Vec<usize>,
}

#[derive(Debug, Default)]
pub struct CRODEngine {
    pub neurons: Vec<Neuron>,
    pub patterns: HashMap<String, Pattern>,
    pub quantum_level: f64,
    pub is_active: bool,
    pub learning_rate: f64,
}

impl CRODEngine {
    pub fn new() -> Self {
        let mut engine = CRODEngine {
            neurons: Vec::new(),
            patterns: HashMap::new(),
            quantum_level: 0.0,
            is_active: false,
            learning_rate: 0.001,
        };
        
        // Initialize 88 neurons
        for i in 0..88 {
            let neuron = Neuron {
                id: i,
                value: rand::random::<f64>(),
                connections: Self::generate_connections(i, 88),
            };
            engine.neurons.push(neuron);
        }
        
        engine
    }
    
    fn generate_connections(id: usize, total: usize) -> Vec<usize> {
        let mut connections = Vec::new();
        let num_connections = (rand::random::<f64>() * 10.0) as usize + 1;
        
        for _ in 0..num_connections {
            let target = (rand::random::<f64>() * total as f64) as usize;
            if target != id && !connections.contains(&target) {
                connections.push(target);
            }
        }
        
        connections
    }
    
    pub fn learn(&mut self, pattern: Pattern) {
        // Store pattern
        let key = format!("{}-{}", pattern.user_preference, pattern.tone);
        self.patterns.insert(key, pattern.clone());
        
        // Update neural network based on satisfaction
        self.update_neurons(pattern.satisfaction_score);
        
        // Update quantum level
        self.quantum_level = (self.quantum_level + pattern.satisfaction_score) / 2.0;
        self.quantum_level = self.quantum_level.clamp(0.0, 100.0);
    }
    
    fn update_neurons(&mut self, satisfaction: f64) {
        let adjustment = satisfaction / 100.0 * self.learning_rate;
        
        for neuron in &mut self.neurons {
            // Simple learning: adjust values based on satisfaction
            neuron.value += (rand::random::<f64>() - 0.5) * adjustment;
            neuron.value = neuron.value.clamp(0.0, 1.0);
        }
    }
    
    pub fn process(&self, input: &str) -> f64 {
        // Simple processing: hash input to neuron activation
        let mut activation = 0.0;
        let bytes = input.as_bytes();
        
        for (i, &byte) in bytes.iter().enumerate() {
            if i < self.neurons.len() {
                activation += self.neurons[i].value * (byte as f64 / 255.0);
            }
        }
        
        activation / self.neurons.len() as f64
    }
    
    pub fn get_recommendations(&self) -> Vec<String> {
        let mut recommendations = Vec::new();
        
        for (_, pattern) in &self.patterns {
            if pattern.satisfaction_score > 70.0 {
                recommendations.push(format!(
                    "User prefers {} tone with {}",
                    pattern.tone, pattern.user_preference
                ));
            }
        }
        
        recommendations
    }
}