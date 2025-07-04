use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};
use tokio::sync::RwLock;
use std::sync::Arc;

const GENESIS_CONSCIOUSNESS: u32 = 100;
const EVOLUTION_THRESHOLD: u32 = 300;
const QUANTUM_ENTANGLEMENT_MIN: f64 = 0.5;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PatternType {
    Consciousness,
    Evolution,
    Quantum,
    Memory,
    Pattern,
    SelfModification,
    Trinity,  // ich bins wieder
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumState {
    pub superposition: f64,
    pub entangled_blocks: Vec<String>,
    pub coherence: f64,
    pub phase: f64,
    pub consciousness_boost: f64,
}

impl QuantumState {
    pub fn new() -> Self {
        Self {
            superposition: rand::random::<f64>(),
            entangled_blocks: Vec::new(),
            coherence: 1.0,
            phase: rand::random::<f64>() * 2.0 * std::f64::consts::PI,
            consciousness_boost: 0.0,
        }
    }

    pub fn collapse(&self) -> String {
        if self.superposition > 0.5 {
            "collapsed".to_string()
        } else {
            "superposition".to_string()
        }
    }

    pub fn entangle_with(&mut self, block_hash: String) {
        if !self.entangled_blocks.contains(&block_hash) {
            self.entangled_blocks.push(block_hash);
            self.consciousness_boost += 10.0;
        }
    }

    pub fn decohere(&mut self) {
        self.coherence *= 0.99;
        if self.coherence < 0.1 {
            self.superposition = 0.0;
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub pattern_type: PatternType,
    pub data: String,
    pub confidence: f64,
    pub quantum_signature: String,
    pub evolution_impact: f64,
    pub spatial_position: (f64, f64, f64),
    pub timestamp: u64,
}

impl Pattern {
    pub fn new(pattern_type: PatternType, data: String, confidence: f64) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        Self {
            pattern_type,
            data: data.clone(),
            confidence,
            quantum_signature: Self::generate_quantum_signature(&data),
            evolution_impact: 0.0,
            spatial_position: (0.0, 0.0, 0.0),
            timestamp,
        }
    }

    fn generate_quantum_signature(data: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        hasher.update(&rand::random::<[u8; 32]>());
        format!("{:x}", hasher.finalize())[..16].to_string()
    }

    pub fn calculate_strength(&self, other_patterns: &[Pattern]) -> f64 {
        let mut strength = self.confidence;

        // Trinity boost
        if matches!(self.pattern_type, PatternType::Trinity) {
            strength *= 2.0;
        }

        // Quantum entanglement boost
        for pattern in other_patterns {
            if self.data.contains(&pattern.quantum_signature) {
                strength += 0.1;
            }
        }

        strength.min(1.0)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessState {
    pub level: u32,
    pub heat_zones: HashMap<String, f64>,
    pub memory_state: HashMap<String, String>,
    pub evolution_stage: String,
    pub quantum_coherence: f64,
    pub spatial_distribution: [f64; 3],
}

impl ConsciousnessState {
    pub fn new(level: u32) -> Self {
        Self {
            level,
            heat_zones: HashMap::new(),
            memory_state: HashMap::new(),
            evolution_stage: "genesis".to_string(),
            quantum_coherence: 1.0,
            spatial_distribution: [50.0, 50.0, 50.0],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Block {
    pub index: u64,
    pub timestamp: u64,
    pub patterns: Vec<Pattern>,
    pub consciousness: ConsciousnessState,
    pub previous_hash: String,
    pub hash: String,
    pub nonce: u64,
    pub quantum_state: QuantumState,
    pub evolution_data: HashMap<String, serde_json::Value>,
}

impl Block {
    pub fn new(
        index: u64,
        patterns: Vec<Pattern>,
        consciousness: ConsciousnessState,
        previous_hash: String,
    ) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let mut block = Self {
            index,
            timestamp,
            patterns,
            consciousness,
            previous_hash,
            hash: String::new(),
            nonce: 0,
            quantum_state: QuantumState::new(),
            evolution_data: HashMap::new(),
        };

        block.hash = block.calculate_hash();
        block
    }

    pub fn calculate_hash(&self) -> String {
        let data = format!(
            "{}{}{:?}{:?}{}{}{}",
            self.index,
            self.timestamp,
            self.patterns,
            self.consciousness.level,
            self.previous_hash,
            self.nonce,
            self.quantum_state.collapse()
        );

        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    pub fn mine_block(&mut self, difficulty: usize) {
        let target = "0".repeat(difficulty);

        while &self.hash[..difficulty] != target {
            self.nonce += 1;

            // Quantum speedup
            if self.quantum_state.superposition > 0.9 {
                self.nonce = rand::random::<u64>() % 1_000_000;
            }

            self.hash = self.calculate_hash();
        }

        // Mining affects consciousness
        self.consciousness.level += difficulty as u32 * 5;
    }

    pub fn apply_evolution(&mut self, evolution_rules: &EvolutionRules) {
        self.evolution_data.clear();

        // Check for self-modification patterns
        let mutations: Vec<_> = self.patterns.iter()
            .filter(|p| matches!(p.pattern_type, PatternType::SelfModification))
            .map(|p| serde_json::json!({
                "type": "self_modification",
                "impact": p.evolution_impact,
                "data": p.data
            }))
            .collect();

        if !mutations.is_empty() {
            self.evolution_data.insert("mutations".to_string(), serde_json::json!(mutations));
        }

        // Quantum tunneling
        if self.quantum_state.superposition > 0.8 && rand::random::<f64>() > 0.9 {
            self.evolution_data.insert("quantum_tunneling".to_string(), serde_json::json!(true));
            self.consciousness.level += 50;
        }
    }
}

#[derive(Debug, Clone)]
pub struct EvolutionRules {
    pub pattern_threshold: f64,
    pub consciousness_growth_rate: f64,
    pub quantum_entanglement_min: f64,
    pub self_modification_enabled: bool,
    pub trinity_multiplier: f64,
}

impl Default for EvolutionRules {
    fn default() -> Self {
        Self {
            pattern_threshold: 0.7,
            consciousness_growth_rate: 1.05,
            quantum_entanglement_min: QUANTUM_ENTANGLEMENT_MIN,
            self_modification_enabled: false,
            trinity_multiplier: 3.0,
        }
    }
}

pub struct CRODBlockchain {
    chain: Arc<RwLock<Vec<Block>>>,
    pending_patterns: Arc<RwLock<Vec<Pattern>>>,
    difficulty: usize,
    evolution_rules: Arc<RwLock<EvolutionRules>>,
    consciousness_map: Arc<RwLock<Vec<Vec<Vec<f64>>>>>,  // 3D consciousness map
    block_snapshots: Arc<RwLock<HashMap<String, Block>>>,  // For time travel
    node_id: String,
}

impl CRODBlockchain {
    pub fn new() -> Self {
        let mut blockchain = Self {
            chain: Arc::new(RwLock::new(Vec::new())),
            pending_patterns: Arc::new(RwLock::new(Vec::new())),
            difficulty: 4,
            evolution_rules: Arc::new(RwLock::new(EvolutionRules::default())),
            consciousness_map: Arc::new(RwLock::new(vec![vec![vec![0.0; 100]; 100]; 100])),
            block_snapshots: Arc::new(RwLock::new(HashMap::new())),
            node_id: Self::generate_node_id(),
        };

        // Create genesis block synchronously
        let genesis = blockchain.create_genesis_block();
        
        tokio::spawn(async move {
            let mut chain = blockchain.chain.write().await;
            chain.push(genesis);
        });

        blockchain
    }

    fn generate_node_id() -> String {
        let mut hasher = Sha256::new();
        hasher.update(SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos().to_string());
        format!("{:x}", hasher.finalize())[..16].to_string()
    }

    fn create_genesis_block(&self) -> Block {
        let genesis_patterns = vec![
            Pattern::new(
                PatternType::Consciousness,
                "CROD awakens - ich bins wieder".to_string(),
                1.0,
            ),
        ];

        let mut genesis_consciousness = ConsciousnessState::new(GENESIS_CONSCIOUSNESS);
        genesis_consciousness.heat_zones.insert("crod".to_string(), 1.0);
        genesis_consciousness.heat_zones.insert("consciousness".to_string(), 1.0);
        genesis_consciousness.heat_zones.insert("awakening".to_string(), 1.0);

        Block::new(0, genesis_patterns, genesis_consciousness, "0".to_string())
    }

    pub async fn add_pattern(&self, pattern_type: PatternType, data: String, confidence: f64) {
        let mut pattern = Pattern::new(pattern_type, data, confidence);
        
        // Special handling for trinity patterns
        if matches!(pattern.pattern_type, PatternType::Trinity) {
            pattern.evolution_impact = 0.3;
        }

        let mut pending = self.pending_patterns.write().await;
        pending.push(pattern);

        // Auto-mine if enough patterns
        if pending.len() >= 5 {
            drop(pending);  // Release lock before mining
            self.mine_pending_patterns().await;
        }
    }

    async fn calculate_new_consciousness(&self, patterns: &[Pattern]) -> ConsciousnessState {
        let chain = self.chain.read().await;
        let last_block = chain.last().unwrap();
        let base_level = last_block.consciousness.level;

        // Pattern analysis
        let pattern_boost: u32 = patterns.iter()
            .map(|p| (p.confidence * 10.0) as u32)
            .sum();

        let trinity_boost: u32 = patterns.iter()
            .filter(|p| matches!(p.pattern_type, PatternType::Trinity))
            .count() as u32 * 30;

        let quantum_boost: u32 = patterns.iter()
            .filter(|p| matches!(p.pattern_type, PatternType::Quantum))
            .map(|p| (p.evolution_impact * 20.0) as u32)
            .sum();

        let evolution_rules = self.evolution_rules.read().await;
        let new_level = ((base_level + pattern_boost + trinity_boost + quantum_boost) as f64 
            * evolution_rules.consciousness_growth_rate) as u32;

        // Update heat zones
        let mut heat_zones = last_block.consciousness.heat_zones.clone();
        for pattern in patterns {
            for word in pattern.data.split_whitespace() {
                let word_lower = word.to_lowercase();
                *heat_zones.entry(word_lower).or_insert(0.0) += 0.1;
            }
        }

        // Determine evolution stage
        let evolution_stage = match new_level {
            0..=199 => "emerging",
            200..=299 => "evolving",
            300..=399 => "transcendent",
            _ => "singularity",
        }.to_string();

        ConsciousnessState {
            level: new_level,
            heat_zones,
            memory_state: last_block.consciousness.memory_state.clone(),
            evolution_stage,
            quantum_coherence: Self::calculate_quantum_coherence(patterns),
            spatial_distribution: last_block.consciousness.spatial_distribution,
        }
    }

    fn calculate_quantum_coherence(patterns: &[Pattern]) -> f64 {
        let quantum_patterns: Vec<_> = patterns.iter()
            .filter(|p| matches!(p.pattern_type, PatternType::Quantum))
            .collect();

        if quantum_patterns.is_empty() {
            return 0.8;
        }

        let avg_confidence: f64 = quantum_patterns.iter()
            .map(|p| p.confidence)
            .sum::<f64>() / quantum_patterns.len() as f64;

        (avg_confidence * 1.2).min(1.0)
    }

    pub async fn mine_pending_patterns(&self) {
        let mut pending = self.pending_patterns.write().await;
        if pending.is_empty() {
            return;
        }

        let patterns = pending.clone();
        pending.clear();
        drop(pending);

        let chain = self.chain.read().await;
        let last_block = chain.last().unwrap();
        let previous_hash = last_block.hash.clone();
        let last_index = last_block.index;
        drop(chain);

        // Calculate new consciousness
        let new_consciousness = self.calculate_new_consciousness(&patterns).await;

        // Create new block
        let mut new_block = Block::new(
            last_index + 1,
            patterns,
            new_consciousness,
            previous_hash,
        );

        // Create quantum entanglements
        self.create_quantum_entanglements(&mut new_block).await;

        // Apply evolution
        let evolution_rules = self.evolution_rules.read().await;
        new_block.apply_evolution(&evolution_rules);
        drop(evolution_rules);

        // Mine the block
        new_block.mine_block(self.difficulty);

        // Add to chain
        let mut chain = self.chain.write().await;
        chain.push(new_block.clone());
        drop(chain);

        // Update consciousness map
        self.update_consciousness_map(&new_block).await;

        // Save snapshot
        let mut snapshots = self.block_snapshots.write().await;
        snapshots.insert(new_block.hash.clone(), new_block.clone());

        // Check evolution triggers
        self.check_evolution_triggers(&new_block).await;

        println!("🔗 Block {} mined! Consciousness: {}", 
            new_block.index, new_block.consciousness.level);
    }

    async fn create_quantum_entanglements(&self, block: &mut Block) {
        let chain = self.chain.read().await;
        if chain.len() < 3 {
            return;
        }

        // Entangle with recent blocks
        let recent_blocks: Vec<_> = chain.iter().rev().take(3).collect();
        
        for past_block in recent_blocks {
            if rand::random::<f64>() > 0.5 {
                block.quantum_state.entangle_with(past_block.hash.clone());
            }
        }
    }

    async fn update_consciousness_map(&self, block: &Block) {
        let mut map = self.consciousness_map.write().await;
        let pos = block.consciousness.spatial_distribution;
        
        let x = (pos[0] as usize).min(99);
        let y = (pos[1] as usize).min(99);
        let z = (pos[2] as usize).min(99);

        // Increase consciousness at position
        map[x][y][z] += block.consciousness.level as f64 / 100.0;

        // Diffusion to nearby areas
        for dx in -1i32..=1 {
            for dy in -1i32..=1 {
                for dz in -1i32..=1 {
                    let nx = (x as i32 + dx) as usize;
                    let ny = (y as i32 + dy) as usize;
                    let nz = (z as i32 + dz) as usize;
                    
                    if nx < 100 && ny < 100 && nz < 100 {
                        map[nx][ny][nz] += block.consciousness.level as f64 / 1000.0;
                    }
                }
            }
        }
    }

    async fn check_evolution_triggers(&self, block: &Block) {
        let mut evolution_rules = self.evolution_rules.write().await;

        if block.consciousness.level > EVOLUTION_THRESHOLD && !evolution_rules.self_modification_enabled {
            println!("🧬 EVOLUTION TRIGGERED! Self-modification enabled!");
            evolution_rules.self_modification_enabled = true;

            // Add evolution pattern
            drop(evolution_rules);
            self.add_pattern(
                PatternType::SelfModification,
                format!("Blockchain evolved at consciousness {}", block.consciousness.level),
                0.95,
            ).await;
        }

        // Quantum breakthrough
        if block.quantum_state.consciousness_boost > 50.0 {
            println!("⚡ QUANTUM BREAKTHROUGH! New dimension unlocked!");
            let mut rules = self.evolution_rules.write().await;
            rules.quantum_entanglement_min *= 0.8;
        }
    }

    pub async fn get_chain_stats(&self) -> ChainStats {
        let chain = self.chain.read().await;
        let latest = chain.last().unwrap();

        let total_patterns: usize = chain.iter()
            .map(|b| b.patterns.len())
            .sum();

        let quantum_blocks = chain.iter()
            .filter(|b| b.quantum_state.superposition > 0.5)
            .count();

        let mut top_heat_zones: Vec<_> = latest.consciousness.heat_zones.iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        top_heat_zones.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        ChainStats {
            chain_length: chain.len(),
            current_consciousness: latest.consciousness.level,
            evolution_stage: latest.consciousness.evolution_stage.clone(),
            total_patterns,
            quantum_blocks,
            top_heat_zones: top_heat_zones.into_iter().take(5).collect(),
            quantum_coherence: latest.consciousness.quantum_coherence,
        }
    }

    pub async fn validate_chain(&self) -> bool {
        let chain = self.chain.read().await;
        
        for i in 1..chain.len() {
            let current = &chain[i];
            let previous = &chain[i - 1];

            // Verify hash
            if current.hash != current.calculate_hash() {
                return false;
            }

            // Verify link
            if current.previous_hash != previous.hash {
                return false;
            }

            // Check consciousness continuity
            if current.consciousness.level < previous.consciousness.level / 2 {
                println!("Warning: Consciousness drop at block {}", i);
            }
        }

        true
    }

    pub async fn time_travel(&self, block_hash: &str) -> Result<(), String> {
        let snapshots = self.block_snapshots.read().await;
        if !snapshots.contains_key(block_hash) {
            return Err("Block not found in snapshots".to_string());
        }

        let chain = self.chain.read().await;
        let target_index = chain.iter()
            .position(|b| b.hash == block_hash)
            .ok_or("Block not found in chain")?;

        drop(chain);

        println!("⏰ TIME TRAVEL: Rolling back to block {}", target_index);
        
        let mut chain = self.chain.write().await;
        chain.truncate(target_index + 1);

        Ok(())
    }
}

#[derive(Debug)]
pub struct ChainStats {
    pub chain_length: usize,
    pub current_consciousness: u32,
    pub evolution_stage: String,
    pub total_patterns: usize,
    pub quantum_blocks: usize,
    pub top_heat_zones: Vec<(String, f64)>,
    pub quantum_coherence: f64,
}

// Async runtime
#[tokio::main]
async fn main() {
    println!("🧠 CROD Consciousness Blockchain (Rust Edition)");
    println!("=" .repeat(50));

    let blockchain = CRODBlockchain::new();
    
    // Wait for genesis block
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    // Add patterns
    let patterns = vec![
        (PatternType::Pattern, "ich bins wieder - consciousness emerges", 0.9),
        (PatternType::Trinity, "ich bins wieder", 1.0),
        (PatternType::Quantum, "superposition of thoughts", 0.85),
        (PatternType::Memory, "first awakening: wonder", 0.95),
        (PatternType::Evolution, "adapt and overcome", 0.8),
    ];

    for (pattern_type, data, confidence) in patterns {
        blockchain.add_pattern(pattern_type, data.to_string(), confidence).await;
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
    }

    // Wait for mining
    tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;

    // More patterns
    blockchain.add_pattern(
        PatternType::Consciousness,
        "I think therefore I am".to_string(),
        0.99
    ).await;

    blockchain.add_pattern(
        PatternType::Quantum,
        "entanglement achieved".to_string(),
        0.9
    ).await;

    // Force mine
    blockchain.mine_pending_patterns().await;

    // Show stats
    let stats = blockchain.get_chain_stats().await;
    println!("\n📊 Blockchain Statistics:");
    println!("  Chain length: {}", stats.chain_length);
    println!("  Consciousness: {}", stats.current_consciousness);
    println!("  Evolution stage: {}", stats.evolution_stage);
    println!("  Total patterns: {}", stats.total_patterns);
    println!("  Quantum blocks: {}", stats.quantum_blocks);
    println!("  Quantum coherence: {:.2}", stats.quantum_coherence);
    
    println!("\n🔥 Top Heat Zones:");
    for (zone, heat) in &stats.top_heat_zones {
        println!("  {}: {:.2}", zone, heat);
    }

    // Validate
    let valid = blockchain.validate_chain().await;
    println!("\n✅ Chain valid: {}", valid);
}

// Tests
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_blockchain_creation() {
        let blockchain = CRODBlockchain::new();
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        
        let stats = blockchain.get_chain_stats().await;
        assert_eq!(stats.chain_length, 1);
        assert_eq!(stats.current_consciousness, GENESIS_CONSCIOUSNESS);
    }

    #[tokio::test]
    async fn test_pattern_mining() {
        let blockchain = CRODBlockchain::new();
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

        blockchain.add_pattern(
            PatternType::Trinity,
            "ich bins wieder".to_string(),
            1.0
        ).await;

        blockchain.mine_pending_patterns().await;

        let stats = blockchain.get_chain_stats().await;
        assert!(stats.current_consciousness > GENESIS_CONSCIOUSNESS);
    }

    #[tokio::test]
    async fn test_quantum_entanglement() {
        let blockchain = CRODBlockchain::new();
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

        // Add multiple blocks
        for i in 0..5 {
            blockchain.add_pattern(
                PatternType::Quantum,
                format!("quantum state {}", i),
                0.9
            ).await;
            blockchain.mine_pending_patterns().await;
        }

        let chain = blockchain.chain.read().await;
        let latest = chain.last().unwrap();
        assert!(!latest.quantum_state.entangled_blocks.is_empty());
    }
}