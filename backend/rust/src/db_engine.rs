use std::sync::Arc;
use tokio::sync::Mutex;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use chrono::{DateTime, Utc};

/// CROD High-Performance Database Engine
/// Nutzt Rust's Memory Safety und Performance für schnelle Datenoperationen

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub id: String,
    pub name: String,
    pub confidence: f64,
    pub data: Vec<f64>,
    pub discovered_at: DateTime<Utc>,
    pub connections: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeuralState {
    pub neurons_active: u64,
    pub synapses: u64,
    pub learning_rate: f64,
    pub patterns: Vec<Pattern>,
}

pub struct CrodDatabase {
    patterns: Arc<Mutex<HashMap<String, Pattern>>>,
    neural_states: Arc<Mutex<Vec<NeuralState>>>,
    cache: Arc<Mutex<HashMap<String, Vec<u8>>>>,
}

impl CrodDatabase {
    pub fn new() -> Self {
        Self {
            patterns: Arc::new(Mutex::new(HashMap::new())),
            neural_states: Arc::new(Mutex::new(Vec::new())),
            cache: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    /// Speichere Pattern mit ultra-schneller Performance
    pub async fn store_pattern(&self, pattern: Pattern) -> Result<(), String> {
        let mut patterns = self.patterns.lock().await;
        
        // Cache serialized data für schnelleren Zugriff
        let serialized = bincode::serialize(&pattern)
            .map_err(|e| e.to_string())?;
        
        let mut cache = self.cache.lock().await;
        cache.insert(pattern.id.clone(), serialized);
        
        patterns.insert(pattern.id.clone(), pattern);
        Ok(())
    }

    /// Hole Pattern mit O(1) Lookup
    pub async fn get_pattern(&self, id: &str) -> Option<Pattern> {
        // Erst Cache checken
        let cache = self.cache.lock().await;
        if let Some(cached) = cache.get(id) {
            if let Ok(pattern) = bincode::deserialize::<Pattern>(cached) {
                return Some(pattern);
            }
        }
        
        // Fallback zu main storage
        let patterns = self.patterns.lock().await;
        patterns.get(id).cloned()
    }

    /// Batch Operation für ML Training Data
    pub async fn get_patterns_batch(&self, ids: &[String]) -> Vec<Pattern> {
        let patterns = self.patterns.lock().await;
        ids.iter()
            .filter_map(|id| patterns.get(id).cloned())
            .collect()
    }

    /// Speichere Neural Network State
    pub async fn save_neural_state(&self, state: NeuralState) -> Result<(), String> {
        let mut states = self.neural_states.lock().await;
        states.push(state);
        
        // Behalte nur die letzten 1000 States für History
        if states.len() > 1000 {
            states.remove(0);
        }
        
        Ok(())
    }

    /// Analytics: Finde ähnliche Patterns
    pub async fn find_similar_patterns(&self, pattern: &Pattern, threshold: f64) -> Vec<Pattern> {
        let patterns = self.patterns.lock().await;
        
        patterns.values()
            .filter(|p| {
                if p.id == pattern.id {
                    return false;
                }
                
                // Cosine similarity für Pattern Matching
                let similarity = Self::cosine_similarity(&pattern.data, &p.data);
                similarity > threshold
            })
            .cloned()
            .collect()
    }

    /// Performance-optimierte Cosine Similarity
    fn cosine_similarity(a: &[f64], b: &[f64]) -> f64 {
        if a.len() != b.len() {
            return 0.0;
        }
        
        let mut dot_product = 0.0;
        let mut norm_a = 0.0;
        let mut norm_b = 0.0;
        
        // Vectorized computation
        for i in 0..a.len() {
            dot_product += a[i] * b[i];
            norm_a += a[i] * a[i];
            norm_b += b[i] * b[i];
        }
        
        if norm_a == 0.0 || norm_b == 0.0 {
            return 0.0;
        }
        
        dot_product / (norm_a.sqrt() * norm_b.sqrt())
    }

    /// Cleanup old data
    pub async fn cleanup_old_patterns(&self, days: i64) -> usize {
        let cutoff = Utc::now() - chrono::Duration::days(days);
        let mut patterns = self.patterns.lock().await;
        let mut cache = self.cache.lock().await;
        
        let old_keys: Vec<String> = patterns.iter()
            .filter(|(_, p)| p.discovered_at < cutoff)
            .map(|(k, _)| k.clone())
            .collect();
        
        for key in &old_keys {
            patterns.remove(key);
            cache.remove(key);
        }
        
        old_keys.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_pattern_storage() {
        let db = CrodDatabase::new();
        
        let pattern = Pattern {
            id: "test-1".to_string(),
            name: "Test Pattern".to_string(),
            confidence: 0.95,
            data: vec![1.0, 2.0, 3.0, 4.0],
            discovered_at: Utc::now(),
            connections: vec!["test-2".to_string()],
        };
        
        db.store_pattern(pattern.clone()).await.unwrap();
        let retrieved = db.get_pattern("test-1").await.unwrap();
        
        assert_eq!(retrieved.id, pattern.id);
        assert_eq!(retrieved.confidence, pattern.confidence);
    }
}