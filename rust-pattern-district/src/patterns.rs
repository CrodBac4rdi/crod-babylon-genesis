use std::collections::HashMap;
use aho_corasick::{AhoCorasick, PatternID};
use regex::Regex;
use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub id: String,
    pub name: String,
    pub pattern_type: PatternType,
    pub matches: Vec<Match>,
    pub weight: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PatternType {
    Keyword,
    Regex,
    Trinity,
    Composite,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Match {
    pub start: usize,
    pub end: usize,
    pub text: String,
}

pub struct PatternEngine {
    keyword_matcher: AhoCorasick,
    regex_patterns: Vec<(String, Regex)>,
    trinity_values: HashMap<String, u32>,
}

impl PatternEngine {
    pub async fn new() -> Result<Self> {
        // Initialize keyword patterns
        let keywords = vec![
            "ich bins wieder",
            "crod starten",
            "lade crod",
            "wtf", "falsch", "scheisse", "fuck", "mist", "verdammt",
            "geil", "nice", "perfekt", "läuft", "super", "gut",
            "hä", "check nicht", "versteh nicht", "was meinst",
        ];
        
        let keyword_matcher = AhoCorasick::new(keywords)?;

        // Initialize regex patterns
        let regex_patterns = vec![
            ("frustration", Regex::new(r"(wieder nicht|schon wieder|immer noch)")?),
            ("command", Regex::new(r"(sudo|chmod|chown|mkdir|cd|ls)")?),
            ("code_block", Regex::new(r"```[\s\S]*?```")?),
            ("url", Regex::new(r"https?://[^\s]+")?),
            ("file_path", Regex::new(r"/[a-zA-Z0-9/_.-]+")?),
        ];

        // Trinity values
        let mut trinity_values = HashMap::new();
        trinity_values.insert("ich".to_string(), 2);
        trinity_values.insert("bins".to_string(), 3);
        trinity_values.insert("wieder".to_string(), 5);
        trinity_values.insert("daniel".to_string(), 67);
        trinity_values.insert("claude".to_string(), 71);
        trinity_values.insert("crod".to_string(), 17);

        Ok(Self {
            keyword_matcher,
            regex_patterns: regex_patterns.into_iter()
                .map(|(name, regex)| (name.to_string(), regex))
                .collect(),
            trinity_values,
        })
    }

    pub async fn find_patterns(&self, text: &str) -> Vec<Pattern> {
        let mut patterns = Vec::new();

        // Find keyword matches
        for mat in self.keyword_matcher.find_iter(text) {
            let pattern_id = mat.pattern();
            let matched_text = &text[mat.start()..mat.end()];
            
            patterns.push(Pattern {
                id: format!("keyword_{}", pattern_id.as_usize()),
                name: self.determine_pattern_name(matched_text),
                pattern_type: PatternType::Keyword,
                matches: vec![Match {
                    start: mat.start(),
                    end: mat.end(),
                    text: matched_text.to_string(),
                }],
                weight: self.calculate_weight(matched_text),
            });
        }

        // Find regex matches
        for (name, regex) in &self.regex_patterns {
            for mat in regex.find_iter(text) {
                patterns.push(Pattern {
                    id: format!("regex_{}", name),
                    name: name.clone(),
                    pattern_type: PatternType::Regex,
                    matches: vec![Match {
                        start: mat.start(),
                        end: mat.end(),
                        text: mat.as_str().to_string(),
                    }],
                    weight: 1.0,
                });
            }
        }

        // Check for trinity patterns
        let trinity_score = self.calculate_trinity_score(text);
        if trinity_score > 0 {
            patterns.push(Pattern {
                id: "trinity".to_string(),
                name: "Trinity Pattern".to_string(),
                pattern_type: PatternType::Trinity,
                matches: vec![],
                weight: trinity_score as f64,
            });
        }

        patterns
    }

    fn determine_pattern_name(&self, matched_text: &str) -> String {
        match matched_text.to_lowercase().as_str() {
            "ich bins wieder" | "crod starten" | "lade crod" => "crod_activation",
            "wtf" | "falsch" | "scheisse" | "fuck" | "mist" | "verdammt" => "frustration",
            "geil" | "nice" | "perfekt" | "läuft" | "super" | "gut" => "positive_feedback",
            "hä" | "check nicht" | "versteh nicht" | "was meinst" => "confusion",
            _ => "unknown",
        }.to_string()
    }

    fn calculate_weight(&self, matched_text: &str) -> f64 {
        match matched_text.to_lowercase().as_str() {
            "ich bins wieder" => 10.0,
            "crod starten" | "lade crod" => 8.0,
            "wtf" | "scheisse" | "fuck" => 5.0,
            "geil" | "perfekt" => 7.0,
            _ => 1.0,
        }
    }

    fn calculate_trinity_score(&self, text: &str) -> u32 {
        let text_lower = text.to_lowercase();
        let mut score = 1u32;

        for (word, value) in &self.trinity_values {
            if text_lower.contains(word) {
                score = score.wrapping_mul(*value);
            }
        }

        if score > 1 { score % 256 } else { 0 }
    }

    pub async fn get_all_patterns(&self) -> Vec<String> {
        let mut patterns = vec![
            "crod_activation",
            "frustration",
            "positive_feedback",
            "confusion",
        ];

        for (name, _) in &self.regex_patterns {
            patterns.push(name);
        }

        patterns.into_iter().map(String::from).collect()
    }
}