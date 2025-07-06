use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Block {
    pub id: String,
    pub previous_hash: String,
    pub timestamp: u64,
    pub data: serde_json::Value,
    pub hash: String,
    pub nonce: u64,
    pub consciousness: f64,
}

impl Block {
    pub fn new(id: String, previous_hash: String, data: serde_json::Value) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let mut block = Block {
            id,
            previous_hash,
            timestamp,
            data,
            hash: String::new(),
            nonce: 0,
            consciousness: rand::random::<f64>() * 100.0,
        };
        
        block.hash = block.calculate_hash();
        block
    }
    
    fn calculate_hash(&self) -> String {
        let data = format!(
            "{}{}{}{}{}{}",
            self.id,
            self.previous_hash,
            self.timestamp,
            self.data,
            self.nonce,
            self.consciousness
        );
        
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        format!("{:x}", hasher.finalize())
    }
    
    pub fn mine(&mut self, difficulty: usize) {
        let target = "0".repeat(difficulty);
        
        while !self.hash.starts_with(&target) {
            self.nonce += 1;
            self.hash = self.calculate_hash();
        }
    }
}

#[derive(Debug, Default)]
pub struct Blockchain {
    pub chain: Vec<Block>,
    pub difficulty: usize,
}

impl Blockchain {
    pub fn new() -> Self {
        Blockchain {
            chain: Vec::new(),
            difficulty: 4,
        }
    }
    
    pub fn initialize(&mut self) {
        let genesis_data = serde_json::json!({
            "type": "genesis",
            "message": "CROD consciousness initialized",
            "neurons": 88,
            "synapses": 7744,
        });
        
        let genesis = Block::new(
            "genesis".to_string(),
            "0".to_string(),
            genesis_data,
        );
        
        self.chain.push(genesis);
    }
    
    pub fn add_block(&mut self, data: serde_json::Value) -> Block {
        let previous_hash = if let Some(last) = self.chain.last() {
            last.hash.clone()
        } else {
            "0".to_string()
        };
        
        let id = format!("block-{}", self.chain.len());
        let mut block = Block::new(id, previous_hash, data);
        
        // Mine the block
        block.mine(self.difficulty);
        
        self.chain.push(block.clone());
        block
    }
    
    pub fn is_valid(&self) -> bool {
        for i in 1..self.chain.len() {
            let current = &self.chain[i];
            let previous = &self.chain[i - 1];
            
            if current.hash != current.calculate_hash() {
                return false;
            }
            
            if current.previous_hash != previous.hash {
                return false;
            }
            
            if !current.hash.starts_with(&"0".repeat(self.difficulty)) {
                return false;
            }
        }
        
        true
    }
}