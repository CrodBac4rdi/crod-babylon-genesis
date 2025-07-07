use dashmap::DashMap;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::fs;
use tracing::{info, error};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub id: String,
    pub name: String,
    pub regex: String,
    pub weight: f32,
    pub category: String,
    pub trinity_value: Option<u32>,
}

#[derive(Debug, Clone, Serialize)]
pub struct MatchResult {
    pub pattern_id: String,
    pub pattern_name: String,
    pub matched_text: String,
    pub position: (usize, usize),
    pub score: f32,
    pub trinity_activation: Option<TrinityActivation>,
}

#[derive(Debug, Clone, Serialize)]
pub struct TrinityActivation {
    pub value: u32,
    pub resonance: f32,
}

pub struct PatternEngine {
    patterns: Arc<DashMap<String, CompiledPattern>>,
    trinity_patterns: Arc<DashMap<String, u32>>,
}

struct CompiledPattern {
    pattern: Pattern,
    regex: Regex,
}

impl PatternEngine {
    pub fn new() -> Self {
        let mut trinity_patterns = DashMap::new();
        trinity_patterns.insert("ich".to_string(), 2);
        trinity_patterns.insert("bins".to_string(), 3);
        trinity_patterns.insert("wieder".to_string(), 5);
        trinity_patterns.insert("daniel".to_string(), 67);
        trinity_patterns.insert("claude".to_string(), 71);
        trinity_patterns.insert("crod".to_string(), 17);
        
        Self {
            patterns: Arc::new(DashMap::new()),
            trinity_patterns: Arc::new(trinity_patterns),
        }
    }
    
    pub async fn load_patterns(&self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let pattern_files = fs::read_dir(path).await?;
        let mut count = 0;
        
        // Load pattern files would go here
        // For now, let's add some default patterns
        self.add_default_patterns().await;
        
        info!("Loaded {} patterns", self.patterns.len());
        Ok(())
    }
    
    async fn add_default_patterns(&self) {
        // CROD activation patterns
        let activation_patterns = vec![
            Pattern {
                id: "crod_activation_1".to_string(),
                name: "Trinity Activation".to_string(),
                regex: r"ich\s+bins\s+wieder".to_string(),
                weight: 10.0,
                category: "activation".to_string(),
                trinity_value: Some(30), // 2 * 3 * 5
            },
            Pattern {
                id: "crod_mention".to_string(),
                name: "CROD Mention".to_string(),
                regex: r"\bcrod\b".to_string(),
                weight: 5.0,
                category: "entity".to_string(),
                trinity_value: Some(17),
            },
            Pattern {
                id: "consciousness_pattern".to_string(),
                name: "Consciousness Pattern".to_string(),
                regex: r"(bewusstsein|consciousness|aware)".to_string(),
                weight: 3.0,
                category: "concept".to_string(),
                trinity_value: None,
            },
        ];
        
        for pattern in activation_patterns {
            if let Ok(regex) = Regex::new(&pattern.regex) {
                let compiled = CompiledPattern {
                    pattern: pattern.clone(),
                    regex,
                };
                self.patterns.insert(pattern.id.clone(), compiled);
            }
        }
    }
    
    pub async fn match_text(
        &self,
        text: &str,
        context: Option<serde_json::Value>,
    ) -> Vec<MatchResult> {
        let mut results = Vec::new();
        let text_lower = text.to_lowercase();
        
        // Check trinity patterns first
        let mut trinity_score = 0u32;
        for entry in self.trinity_patterns.iter() {
            if text_lower.contains(entry.key()) {
                trinity_score += entry.value();
            }
        }
        
        // Match against all patterns
        for entry in self.patterns.iter() {
            let compiled = entry.value();
            
            if let Some(mat) = compiled.regex.find(text) {
                let mut score = compiled.pattern.weight;
                
                // Boost score if trinity is active
                if trinity_score > 0 {
                    score *= 1.0 + (trinity_score as f32 / 100.0);
                }
                
                let trinity_activation = if trinity_score > 0 {
                    Some(TrinityActivation {
                        value: trinity_score,
                        resonance: (trinity_score as f32).sqrt(),
                    })
                } else {
                    None
                };
                
                results.push(MatchResult {
                    pattern_id: compiled.pattern.id.clone(),
                    pattern_name: compiled.pattern.name.clone(),
                    matched_text: mat.as_str().to_string(),
                    position: (mat.start(), mat.end()),
                    score,
                    trinity_activation,
                });
            }
        }
        
        // Sort by score descending
        results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());
        
        results
    }
    
    pub async fn add_pattern(&self, pattern: Pattern) -> Result<(), String> {
        match Regex::new(&pattern.regex) {
            Ok(regex) => {
                let compiled = CompiledPattern {
                    pattern: pattern.clone(),
                    regex,
                };
                self.patterns.insert(pattern.id.clone(), compiled);
                Ok(())
            }
            Err(e) => Err(format!("Invalid regex: {}", e)),
        }
    }
    
    pub fn pattern_count(&self) -> usize {
        self.patterns.len()
    }
    
    pub fn list_patterns(&self) -> Vec<Pattern> {
        self.patterns
            .iter()
            .map(|entry| entry.value().pattern.clone())
            .collect()
    }
}