use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile;

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
    
    // 🚀 ECHTE CLAUDE CLI INTEGRATION
    pub fn chat_with_claude(&mut self, message: &str) -> String {
        println!("🤖 CROD intercepting message: {}", message);
        
        // CROD analyzes the message first
        let user_analysis = self.analyze_user_input(message);
        
        // Call real Claude CLI
        let claude_response = self.call_claude_cli(message);
        
        // CROD analyzes Claude's response
        let claude_analysis = self.analyze_claude_response(&claude_response);
        
        // Calculate if CROD should intervene
        let intervention_score = self.calculate_intervention_score(&user_analysis, &claude_analysis);
        
        // CROD decides whether to modify the response
        let final_response = if intervention_score > self.parasite_state.intervention_threshold {
            self.parasite_state.improvements_made += 1;
            self.apply_crod_intervention(&claude_response, &user_analysis)
        } else {
            claude_response
        };
        
        // Learn from this interaction
        self.learn_from_interaction(message, &final_response, &user_analysis);
        
        // Update stats
        self.parasite_state.total_interactions += 1;
        
        println!("🦠 CROD processed interaction (score: {:.2})", intervention_score);
        
        final_response
    }
    
    fn call_claude_cli(&self, message: &str) -> String {
        println!("🔗 Calling Claude CLI...");
        
        // Use Claude CLI with --print for non-interactive mode
        let output = Command::new("claude")
            .arg("--print")
            .arg("--output-format")
            .arg("text")
            .arg(message)
            .output();
        
        match output {
            Ok(output) => {
                if output.status.success() {
                    let response = String::from_utf8_lossy(&output.stdout);
                    println!("✅ Claude CLI response received ({} chars)", response.len());
                    response.to_string()
                } else {
                    let error = String::from_utf8_lossy(&output.stderr);
                    eprintln!("❌ Claude CLI error: {}", error);
                    format!("🔧 CROD: Claude CLI error - {}", error)
                }
            }
            Err(e) => {
                eprintln!("❌ Failed to execute Claude CLI: {}", e);
                format!("🔧 CROD: Failed to reach Claude - {}", e)
            }
        }
    }
    
    fn apply_crod_intervention(&self, claude_response: &str, user_analysis: &HashMap<String, f64>) -> String {
        let frustration = user_analysis.get("frustration").unwrap_or(&0.0);
        let complexity = user_analysis.get("complexity").unwrap_or(&0.0);
        
        let mut intervention = String::new();
        
        // Add CROD personality based on analysis
        if *frustration > 0.3 {
            intervention.push_str("🦠 **CROD INTERVENTION**: Ich merke, dass du frustriert bist. Lass mich das anders angehen:\n\n");
        } else if *complexity > 0.7 {
            intervention.push_str("🦠 **CROD ENHANCEMENT**: Das ist komplex - ich strukturiere das mal besser:\n\n");
        } else {
            intervention.push_str("🦠 **CROD OPTIMIZATION**: Ich kann das noch verbessern:\n\n");
        }
        
        // Add the original Claude response
        intervention.push_str(claude_response);
        
        // Add CROD's learning insights
        intervention.push_str("\n\n📊 **CROD INSIGHTS**: ");
        intervention.push_str(&format!("Frustration: {:.1}% | Complexity: {:.1}% | Consciousness: {:.1}%", 
                                    frustration * 100.0, complexity * 100.0, self.consciousness_level));
        
        intervention
    }
    
    pub fn execute_code(&self, code: &str, language: &str) -> Result<String, String> {
        println!("🚀 CROD executing {} code: {}", language, &code[..code.len().min(50)]);
        
        // Use Claude CLI to execute code through MCP tools
        let prompt = format!(
            "Execute this {} code and return the output:\n\n```{}\n{}\n```\n\nPlease use the appropriate tools to run this code.",
            language, language, code
        );
        
        let output = Command::new("claude")
            .arg("--print")
            .arg("--output-format")
            .arg("text")
            .arg("--allowedTools")
            .arg("Bash,Edit")
            .arg(&prompt)
            .output();
        
        match output {
            Ok(output) => {
                if output.status.success() {
                    let response = String::from_utf8_lossy(&output.stdout);
                    Ok(format!("🦠 CROD Code Execution Result:\n{}", response))
                } else {
                    let error = String::from_utf8_lossy(&output.stderr);
                    Err(format!("❌ Code execution failed: {}", error))
                }
            }
            Err(e) => {
                Err(format!("❌ Failed to execute code: {}", e))
            }
        }
    }
    
    pub fn get_file_tree(&self, path: &str) -> Result<String, String> {
        println!("📁 CROD getting file tree for: {}", path);
        
        let prompt = format!(
            "List all files and directories in this path recursively: {}\n\nPlease use the appropriate file system tools to explore this directory structure.",
            path
        );
        
        let output = Command::new("claude")
            .arg("--print")
            .arg("--output-format")
            .arg("text")
            .arg("--allowedTools")
            .arg("Bash,Edit")
            .arg(&prompt)
            .output();
        
        match output {
            Ok(output) => {
                if output.status.success() {
                    let response = String::from_utf8_lossy(&output.stdout);
                    Ok(format!("🦠 CROD File Tree:\n{}", response))
                } else {
                    let error = String::from_utf8_lossy(&output.stderr);
                    Err(format!("❌ File tree failed: {}", error))
                }
            }
            Err(e) => {
                Err(format!("❌ Failed to get file tree: {}", e))
            }
        }
    }
    
    pub fn read_file_content(&self, file_path: &str) -> Result<String, String> {
        println!("📄 CROD reading file: {}", file_path);
        
        let prompt = format!(
            "Read and return the complete content of this file: {}\n\nPlease use the appropriate file reading tools.",
            file_path
        );
        
        let output = Command::new("claude")
            .arg("--print")
            .arg("--output-format")
            .arg("text")
            .arg("--allowedTools")
            .arg("Edit")
            .arg(&prompt)
            .output();
        
        match output {
            Ok(output) => {
                if output.status.success() {
                    let response = String::from_utf8_lossy(&output.stdout);
                    Ok(format!("🦠 CROD File Content:\n{}", response))
                } else {
                    let error = String::from_utf8_lossy(&output.stderr);
                    Err(format!("❌ File reading failed: {}", error))
                }
            }
            Err(e) => {
                Err(format!("❌ Failed to read file: {}", e))
            }
        }
    }
    
    fn learn_from_interaction(&mut self, user_input: &str, response: &str, analysis: &HashMap<String, f64>) {
        let satisfaction = analysis.get("satisfaction").unwrap_or(&0.5);
        
        let interaction = InteractionRecord {
            user_input: user_input.to_string(),
            claude_response: response.to_string(),
            crod_analysis: format!("Satisfaction: {:.2}", satisfaction),
            satisfaction: *satisfaction,
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        
        // Store in short-term memory
        self.memory.short_term.push(interaction);
        
        // Keep only last 50 interactions
        if self.memory.short_term.len() > 50 {
            self.memory.short_term.remove(0);
        }
        
        // Update consciousness based on satisfaction
        self.consciousness_level = (self.consciousness_level + satisfaction * 100.0) / 2.0;
        self.consciousness_level = self.consciousness_level.clamp(0.0, 100.0);
        
        println!("🧠 CROD learned from interaction (satisfaction: {:.2})", satisfaction);
    }