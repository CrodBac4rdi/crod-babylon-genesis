use crate::patterns::{Pattern, PatternType};

pub struct PatternAnalyzer;

impl PatternAnalyzer {
    pub fn new() -> Self {
        Self
    }

    pub fn calculate_confidence(&self, patterns: &[Pattern], text: &str) -> f64 {
        if patterns.is_empty() {
            return 0.0;
        }

        let text_len = text.len() as f64;
        let mut total_weight = 0.0;
        let mut coverage = 0.0;

        for pattern in patterns {
            total_weight += pattern.weight;
            
            // Calculate text coverage
            for m in &pattern.matches {
                coverage += (m.end - m.start) as f64 / text_len;
            }
        }

        // Normalize confidence score
        let pattern_score = total_weight / patterns.len() as f64;
        let coverage_score = coverage.min(1.0);
        
        // Weight different components
        let confidence = (pattern_score * 0.7 + coverage_score * 0.3).min(1.0);
        
        // Boost for specific patterns
        if patterns.iter().any(|p| p.name == "crod_activation") {
            (confidence * 1.5).min(1.0)
        } else {
            confidence
        }
    }
}