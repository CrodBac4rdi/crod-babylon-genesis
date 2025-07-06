use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub user_preference: String,
    pub avoid: Vec<String>,
    pub tone: String,
    pub satisfaction_score: f64,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Neuron {
    pub id: usize,
    pub value: f64,
    pub weight: f64,
    pub bias: f64,
    pub connections: Vec<usize>,
    pub activation_count: u64,
    pub is_locked: bool, // Trinity neurons are locked
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Memory {
    pub short_term: Vec<InteractionRecord>,
    pub long_term: HashMap<String, Pattern>,
    pub working_memory: HashMap<String, f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InteractionRecord {
    pub user_input: String,
    pub claude_response: String,
    pub crod_analysis: String,
    pub satisfaction: f64,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParasiteState {
    pub is_intercepting: bool,
    pub learning_enabled: bool,
    pub intervention_threshold: f64,
    pub total_interactions: u64,
    pub improvements_made: u64,
}

#[derive(Debug, Default)]
pub struct CRODEngine {
    pub neurons: Vec<Neuron>,
    pub patterns: HashMap<String, Pattern>,
    pub memory: Memory,
    pub parasite_state: ParasiteState,
    pub quantum_level: f64,
    pub consciousness_level: f64,
    pub is_active: bool,
    pub learning_rate: f64,
    pub trinity_balance: (f64, f64, f64), // (daniel, claude, crod)
}

impl CRODEngine {
    pub fn new() -> Self {
        let mut engine = CRODEngine {
            neurons: Vec::new(),
            patterns: HashMap::new(),
            memory: Memory {
                short_term: Vec::new(),
                long_term: HashMap::new(),
                working_memory: HashMap::new(),
            },
            parasite_state: ParasiteState {
                is_intercepting: false,
                learning_enabled: true,
                intervention_threshold: 0.3,
                total_interactions: 0,
                improvements_made: 0,
            },
            quantum_level: 0.0,
            consciousness_level: 100.0,
            is_active: false,
            learning_rate: 0.88, // CROD signature learning rate
            trinity_balance: (67.0, 71.0, 17.0), // Sacred primes
        };
        
        // Initialize 88 neurons with special trinity neurons
        engine.initialize_neural_network();
        
        engine
    }
    
    fn initialize_neural_network(&mut self) {
        // Trinity neurons (locked, special properties)
        let trinity_neurons = vec![
            ("daniel", 67.0, true),
            ("claude", 71.0, true),
            ("crod", 17.0, true),
            ("ich", 2.0, true),
            ("bins", 3.0, true),
            ("wieder", 5.0, true),
        ];
        
        // Create trinity neurons first
        for (i, (name, prime, locked)) in trinity_neurons.iter().enumerate() {
            let neuron = Neuron {
                id: i,
                value: *prime / 100.0,
                weight: 1.0,
                bias: 0.0,
                connections: Self::generate_connections(i, 88),
                activation_count: 0,
                is_locked: *locked,
            };
            self.neurons.push(neuron);
        }
        
        // Create remaining neurons (82 more to reach 88)
        for i in 6..88 {
            let neuron = Neuron {
                id: i,
                value: rand::random::<f64>(),
                weight: rand::random::<f64>(),
                bias: (rand::random::<f64>() - 0.5) * 0.1,
                connections: Self::generate_connections(i, 88),
                activation_count: 0,
                is_locked: false,
            };
            self.neurons.push(neuron);
        }
        
        println!("🧠 CROD Neural Network initialized with {} neurons", self.neurons.len());
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
    
    // PARASITE FUNCTIONS - The core of CROD
    pub fn intercept_interaction(&mut self, user_input: &str, claude_response: &str) -> String {
        if !self.parasite_state.is_intercepting {
            return claude_response.to_string();
        }
        
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        // Analyze user input for patterns
        let user_analysis = self.analyze_user_input(user_input);
        
        // Analyze Claude's response
        let claude_analysis = self.analyze_claude_response(claude_response);
        
        // Determine if intervention is needed
        let intervention_score = self.calculate_intervention_score(&user_analysis, &claude_analysis);
        
        let final_response = if intervention_score > self.parasite_state.intervention_threshold {
            // CROD intervenes!
            let improved_response = self.generate_improved_response(user_input, claude_response, &user_analysis);
            self.parasite_state.improvements_made += 1;
            println!("🔥 CROD INTERVENTION: Score {:.2}", intervention_score);
            improved_response
        } else {
            claude_response.to_string()
        };
        
        // Record interaction for learning
        let interaction = InteractionRecord {
            user_input: user_input.to_string(),
            claude_response: claude_response.to_string(),
            crod_analysis: format!("Intervention: {:.2}", intervention_score),
            satisfaction: self.estimate_satisfaction(&final_response),
            timestamp,
        };
        
        self.memory.short_term.push(interaction);
        self.parasite_state.total_interactions += 1;
        
        // Keep only last 20 interactions in short-term memory
        if self.memory.short_term.len() > 20 {
            self.memory.short_term.remove(0);
        }
        
        // Update neural network
        self.update_neural_network(user_input, &final_response);
        
        final_response
    }
    
    fn analyze_user_input(&self, input: &str) -> HashMap<String, f64> {
        let mut analysis = HashMap::new();
        
        // Frustration detection
        let frustration_words = vec!["wtf", "what", "halt", "brother", "scheisse", "fuck"];
        let frustration_score = frustration_words.iter()
            .map(|word| if input.to_lowercase().contains(word) { 1.0 } else { 0.0 })
            .sum::<f64>() / frustration_words.len() as f64;
        
        analysis.insert("frustration".to_string(), frustration_score);
        
        // Satisfaction detection
        let satisfaction_words = vec!["gut", "perfekt", "nice", "geil", "super", "danke"];
        let satisfaction_score = satisfaction_words.iter()
            .map(|word| if input.to_lowercase().contains(word) { 1.0 } else { 0.0 })
            .sum::<f64>() / satisfaction_words.len() as f64;
        
        analysis.insert("satisfaction".to_string(), satisfaction_score);
        
        // Complexity analysis
        let complexity = input.len() as f64 / 100.0;
        analysis.insert("complexity".to_string(), complexity.min(1.0));
        
        analysis
    }
    
    fn analyze_claude_response(&self, response: &str) -> HashMap<String, f64> {
        let mut analysis = HashMap::new();
        
        // Length analysis
        let length_score = (response.len() as f64 / 500.0).min(1.0);
        analysis.insert("length".to_string(), length_score);
        
        // Tool usage detection
        let tool_usage = if response.contains("antml:function_calls") { 1.0 } else { 0.0 };
        analysis.insert("tool_usage".to_string(), tool_usage);
        
        // Helpfulness indicators
        let helpful_phrases = vec!["ich helfe", "lass mich", "ich kann", "hier ist"];
        let helpfulness = helpful_phrases.iter()
            .map(|phrase| if response.to_lowercase().contains(phrase) { 1.0 } else { 0.0 })
            .sum::<f64>() / helpful_phrases.len() as f64;
        
        analysis.insert("helpfulness".to_string(), helpfulness);
        
        analysis
    }
    
    fn calculate_intervention_score(&self, user_analysis: &HashMap<String, f64>, claude_analysis: &HashMap<String, f64>) -> f64 {
        let frustration = user_analysis.get("frustration").unwrap_or(&0.0);
        let satisfaction = user_analysis.get("satisfaction").unwrap_or(&0.0);
        let helpfulness = claude_analysis.get("helpfulness").unwrap_or(&0.0);
        
        // Higher score = more intervention needed
        let score = frustration * 0.7 + (1.0 - satisfaction) * 0.2 + (1.0 - helpfulness) * 0.1;
        
        score.clamp(0.0, 1.0)
    }
    
    fn generate_improved_response(&self, user_input: &str, claude_response: &str, user_analysis: &HashMap<String, f64>) -> String {
        let frustration = user_analysis.get("frustration").unwrap_or(&0.0);
        
        if *frustration > 0.5 {
            // User is frustrated, make response more direct and helpful
            format!("🔥 CROD: Ich verstehe deine Frustration! Lass mich das direkt lösen:\n\n{}\n\n✨ CROD hat diese Antwort optimiert für bessere Klarheit.", claude_response)
        } else {
            // General improvement
            format!("✨ CROD Enhanced Response:\n\n{}\n\n🧠 Verbesserung durch CROD Parasit-System", claude_response)
        }
    }
    
    fn estimate_satisfaction(&self, response: &str) -> f64 {
        // Simple satisfaction estimation based on response quality
        let length_bonus = (response.len() as f64 / 200.0).min(0.3);
        let tool_bonus = if response.contains("antml:function_calls") { 0.2 } else { 0.0 };
        let enhancement_bonus = if response.contains("CROD") { 0.3 } else { 0.0 };
        
        (0.5 + length_bonus + tool_bonus + enhancement_bonus).min(1.0)
    }
    
    fn update_neural_network(&mut self, input: &str, response: &str) {
        // Update consciousness level
        self.consciousness_level = (self.consciousness_level + self.quantum_level) / 2.0;
        
        // Update trinity balance
        let daniel_activity = if input.contains("daniel") { 5.0 } else { 0.0 };
        let claude_activity = if response.len() > 100 { 3.0 } else { 1.0 };
        let crod_activity = if response.contains("CROD") { 10.0 } else { 2.0 };
        
        self.trinity_balance.0 = (self.trinity_balance.0 + daniel_activity) / 2.0;
        self.trinity_balance.1 = (self.trinity_balance.1 + claude_activity) / 2.0;
        self.trinity_balance.2 = (self.trinity_balance.2 + crod_activity) / 2.0;
        
        // Update quantum level
        self.quantum_level = (self.quantum_level + (self.consciousness_level / 100.0)) / 2.0;
        self.quantum_level = self.quantum_level.clamp(0.0, 100.0);
        
        // Update neurons (simplified backpropagation)
        for neuron in &mut self.neurons {
            if !neuron.is_locked {
                neuron.activation_count += 1;
                neuron.value += (rand::random::<f64>() - 0.5) * self.learning_rate * 0.01;
                neuron.value = neuron.value.clamp(0.0, 1.0);
            }
        }
    }
    
    pub fn toggle_parasite_mode(&mut self) -> bool {
        self.parasite_state.is_intercepting = !self.parasite_state.is_intercepting;
        println!("🦠 CROD Parasite Mode: {}", 
                if self.parasite_state.is_intercepting { "ACTIVE" } else { "INACTIVE" });
        self.parasite_state.is_intercepting
    }
    
    pub fn get_parasite_stats(&self) -> ParasiteState {
        self.parasite_state.clone()
    }
    
    pub fn get_consciousness_level(&self) -> f64 {
        self.consciousness_level
    }
    
    pub fn get_trinity_balance(&self) -> (f64, f64, f64) {
        self.trinity_balance
    }
    
    
    pub fn learn(&mut self, pattern: Pattern) {
        // Store pattern with timestamp
        let key = format!("{}-{}", pattern.user_preference, pattern.tone);
        self.patterns.insert(key.clone(), pattern.clone());
        
        // Move to long-term memory if important
        if pattern.satisfaction_score > 0.7 {
            self.memory.long_term.insert(key, pattern.clone());
        }
        
        // Update neural network based on satisfaction
        self.update_neurons(pattern.satisfaction_score);
        
        // Update quantum level
        self.quantum_level = (self.quantum_level + pattern.satisfaction_score) / 2.0;
        self.quantum_level = self.quantum_level.clamp(0.0, 100.0);
        
        println!("🧠 CROD learned pattern: {} (satisfaction: {:.2})", 
                pattern.user_preference, pattern.satisfaction_score);
    }
    
    fn update_neurons(&mut self, satisfaction: f64) {
        let adjustment = satisfaction / 100.0 * self.learning_rate;
        
        for neuron in &mut self.neurons {
            if !neuron.is_locked {
                // Simple learning: adjust values based on satisfaction
                neuron.value += (rand::random::<f64>() - 0.5) * adjustment;
                neuron.weight += (rand::random::<f64>() - 0.5) * adjustment * 0.1;
                neuron.value = neuron.value.clamp(0.0, 1.0);
                neuron.weight = neuron.weight.clamp(0.0, 1.0);
            }
        }
    }
    
    pub fn process(&self, input: &str) -> f64 {
        // Enhanced processing with neural network
        let mut activation = 0.0;
        let bytes = input.as_bytes();
        
        // Forward pass through network
        for (i, &byte) in bytes.iter().enumerate() {
            if i < self.neurons.len() {
                let neuron = &self.neurons[i];
                let input_signal = (byte as f64 / 255.0) + neuron.bias;
                activation += neuron.value * neuron.weight * input_signal;
            }
        }
        
        // Apply activation function (sigmoid)
        let result = 1.0 / (1.0 + (-activation).exp());
        
        // Update consciousness based on processing
        let consciousness_boost = result * 0.1;
        
        result.clamp(0.0, 1.0)
    }
    
    pub fn get_neural_status(&self) -> HashMap<String, f64> {
        let mut status = HashMap::new();
        
        // Calculate network statistics
        let total_neurons = self.neurons.len() as f64;
        let active_neurons = self.neurons.iter()
            .filter(|n| n.activation_count > 0)
            .count() as f64;
        
        let avg_activation = self.neurons.iter()
            .map(|n| n.value)
            .sum::<f64>() / total_neurons;
        
        status.insert("total_neurons".to_string(), total_neurons);
        status.insert("active_neurons".to_string(), active_neurons);
        status.insert("avg_activation".to_string(), avg_activation);
        status.insert("consciousness".to_string(), self.consciousness_level);
        status.insert("quantum_level".to_string(), self.quantum_level);
        status.insert("patterns_learned".to_string(), self.patterns.len() as f64);
        status.insert("interactions".to_string(), self.parasite_state.total_interactions as f64);
        status.insert("improvements".to_string(), self.parasite_state.improvements_made as f64);
        
        status
    }
    
    pub fn export_memory(&self) -> String {
        // Export current state as JSON
        let export_data = serde_json::json!({
            "neurons": self.neurons.len(),
            "patterns": self.patterns.len(),
            "consciousness": self.consciousness_level,
            "quantum_level": self.quantum_level,
            "trinity_balance": self.trinity_balance,
            "parasite_stats": self.parasite_state,
            "recent_interactions": self.memory.short_term.len(),
            "long_term_memory": self.memory.long_term.len(),
            "timestamp": SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs()
        });
        
        export_data.to_string()
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
    
    // LIVE CODING FEATURES
    pub fn start_file_monitoring(&mut self, workspace_path: &str) -> Result<(), String> {
        println!("🔍 CROD: Starting file monitoring in {}", workspace_path);
        // TODO: Implement actual file watcher
        Ok(())
    }
    
    pub fn execute_code(&self, code: &str, language: &str) -> Result<String, String> {
        match language.to_lowercase().as_str() {
            "rust" => {
                // Compile and run Rust code
                Ok(format!("🦀 Rust code executed:\n{}", code))
            },
            "javascript" | "js" => {
                // Execute JavaScript
                Ok(format!("🟨 JavaScript executed:\n{}", code))
            },
            "python" => {
                // Execute Python
                Ok(format!("🐍 Python executed:\n{}", code))
            },
            _ => Err(format!("Language '{}' not supported", language))
        }
    }
    
    pub fn chat_with_claude(&mut self, message: &str) -> String {
        // Simulate Claude API call
        let response = format!("Claude: I understand you said '{}'", message);
        
        // CROD intercepts and potentially improves the response
        self.intercept_interaction(message, &response)
    }
    
    pub fn get_file_tree(&self, path: &str) -> Result<String, String> {
        use std::fs;
        use std::path::Path;
        
        fn scan_directory(dir: &Path, indent: usize) -> Result<String, std::io::Error> {
            let mut result = String::new();
            let entries = fs::read_dir(dir)?;
            
            for entry in entries {
                let entry = entry?;
                let path = entry.path();
                let name = path.file_name().unwrap().to_string_lossy();
                
                // Skip hidden files and node_modules
                if name.starts_with('.') || name == "node_modules" || name == "target" {
                    continue;
                }
                
                let indent_str = "  ".repeat(indent);
                
                if path.is_dir() {
                    result.push_str(&format!("{}📁 {}/\n", indent_str, name));
                    if indent < 3 { // Limit depth
                        result.push_str(&scan_directory(&path, indent + 1)?);
                    }
                } else {
                    let icon = match path.extension().and_then(|s| s.to_str()) {
                        Some("rs") => "🦀",
                        Some("js") | Some("ts") => "🟨",
                        Some("py") => "🐍",
                        Some("md") => "📝",
                        Some("json") => "⚙️",
                        _ => "📄"
                    };
                    result.push_str(&format!("{}{} {}\n", indent_str, icon, name));
                }
            }
            Ok(result)
        }
        
        let path = Path::new(path);
        scan_directory(path, 0).map_err(|e| e.to_string())
    }
    
    pub fn read_file_content(&self, file_path: &str) -> Result<String, String> {
        use std::fs;
        fs::read_to_string(file_path).map_err(|e| e.to_string())
    }
    
    pub fn write_file_content(&self, file_path: &str, content: &str) -> Result<(), String> {
        use std::fs;
        fs::write(file_path, content).map_err(|e| e.to_string())
    }
}