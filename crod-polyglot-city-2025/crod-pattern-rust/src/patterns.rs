use dashmap::DashMap;
use rayon::prelude::*;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PatternMatch {
    pub pattern: String,
    pub match_type: MatchType,
    pub position: usize,
    pub strength: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum MatchType {
    Trinity,
    Activation,
    Command,
    Emotion,
    Technical,
}

pub struct PatternEngine {
    trinity_patterns: Arc<DashMap<String, f64>>,
    activation_patterns: Vec<Regex>,
    command_patterns: Vec<Regex>,
}

impl PatternEngine {
    pub fn new() -> Self {
        let trinity_patterns = Arc::new(DashMap::new());
        
        // Initialize trinity values
        trinity_patterns.insert("ich".to_string(), 2.0);
        trinity_patterns.insert("bins".to_string(), 3.0);
        trinity_patterns.insert("wieder".to_string(), 5.0);
        trinity_patterns.insert("daniel".to_string(), 67.0);
        trinity_patterns.insert("claude".to_string(), 71.0);
        trinity_patterns.insert("crod".to_string(), 17.0);
        
        // Compile regex patterns
        let activation_patterns = vec![
            Regex::new(r"ich\s+bins\s+wieder").unwrap(),
            Regex::new(r"crod\s+starten").unwrap(),
            Regex::new(r"lade\s+crod").unwrap(),
        ];
        
        let command_patterns = vec![
            Regex::new(r"claude\s+chat").unwrap(),
            Regex::new(r"git\s+(commit|push|pull)").unwrap(),
            Regex::new(r"kubectl\s+\w+").unwrap(),
            Regex::new(r"docker\s+\w+").unwrap(),
        ];
        
        Self {
            trinity_patterns,
            activation_patterns,
            command_patterns,
        }
    }
    
    pub fn analyze(&self, text: &str) -> Vec<PatternMatch> {
        let text_lower = text.to_lowercase();
        let mut matches = Vec::new();
        
        // Parallel pattern matching
        let trinity_matches = self.find_trinity_patterns(&text_lower);
        let activation_matches = self.find_activation_patterns(&text_lower);
        let command_matches = self.find_command_patterns(&text_lower);
        
        matches.extend(trinity_matches);
        matches.extend(activation_matches);
        matches.extend(command_matches);
        
        // Sort by position
        matches.sort_by_key(|m| m.position);
        
        matches
    }
    
    fn find_trinity_patterns(&self, text: &str) -> Vec<PatternMatch> {
        self.trinity_patterns
            .iter()
            .par_bridge()
            .flat_map(|entry| {
                let pattern = entry.key();
                let strength = *entry.value();
                
                text.match_indices(pattern)
                    .map(|(pos, _)| PatternMatch {
                        pattern: pattern.clone(),
                        match_type: MatchType::Trinity,
                        position: pos,
                        strength,
                    })
                    .collect::<Vec<_>>()
            })
            .collect()
    }
    
    fn find_activation_patterns(&self, text: &str) -> Vec<PatternMatch> {
        self.activation_patterns
            .par_iter()
            .flat_map(|regex| {
                regex.find_iter(text)
                    .map(|m| PatternMatch {
                        pattern: m.as_str().to_string(),
                        match_type: MatchType::Activation,
                        position: m.start(),
                        strength: 100.0, // Activation patterns have maximum strength
                    })
                    .collect::<Vec<_>>()
            })
            .collect()
    }
    
    fn find_command_patterns(&self, text: &str) -> Vec<PatternMatch> {
        self.command_patterns
            .par_iter()
            .flat_map(|regex| {
                regex.find_iter(text)
                    .map(|m| PatternMatch {
                        pattern: m.as_str().to_string(),
                        match_type: MatchType::Command,
                        position: m.start(),
                        strength: 50.0,
                    })
                    .collect::<Vec<_>>()
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_trinity_patterns() {
        let engine = PatternEngine::new();
        let matches = engine.analyze("ich bins wieder daniel");
        
        assert!(matches.len() >= 3);
        assert!(matches.iter().any(|m| m.pattern == "ich"));
        assert!(matches.iter().any(|m| m.pattern == "bins"));
        assert!(matches.iter().any(|m| m.pattern == "wieder"));
    }
    
    #[test]
    fn test_activation_pattern() {
        let engine = PatternEngine::new();
        let matches = engine.analyze("ich bins wieder");
        
        assert!(matches.iter().any(|m| matches!(m.match_type, MatchType::Activation)));
    }
}