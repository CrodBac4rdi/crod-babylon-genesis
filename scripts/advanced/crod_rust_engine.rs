// CROD Rust Knowledge Engine
// FUCK SQL - PURE RUST POWER!

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use regex::Regex;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CRODAtom {
    id: String,
    content: String,
    atom_type: String,
    category: String,
    heat: f64,
    sources: Vec<String>,
    mention_count: u32,
    metadata: HashMap<String, serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CRODPattern {
    id: String,
    atoms: Vec<String>,
    pattern_type: String,
    strength: f64,
    connections: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CRODChain {
    id: String,
    patterns: Vec<String>,
    chain_type: String,
    flow: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CRODNetwork {
    id: String,
    chains: Vec<String>,
    network_type: String,
    topology: String,
}

struct CRODEngine {
    atoms: HashMap<String, CRODAtom>,
    patterns: HashMap<String, CRODPattern>,
    chains: HashMap<String, CRODChain>,
    networks: HashMap<String, CRODNetwork>,
    content_index: HashMap<String, Vec<String>>, // content -> atom_ids
    type_index: HashMap<String, Vec<String>>,    // type -> atom_ids
    category_index: HashMap<String, Vec<String>>, // category -> atom_ids
}

impl CRODEngine {
    fn new() -> Self {
        Self {
            atoms: HashMap::new(),
            patterns: HashMap::new(),
            chains: HashMap::new(),
            networks: HashMap::new(),
            content_index: HashMap::new(),
            type_index: HashMap::new(),
            category_index: HashMap::new(),
        }
    }

    fn load_from_jsonl(&mut self, file_path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::open(file_path)?;
        let reader = BufReader::new(file);

        for line in reader.lines() {
            let line = line?;
            if let Ok(atom) = serde_json::from_str::<CRODAtom>(&line) {
                self.add_atom(atom);
            }
        }

        println!("🧠 Loaded {} atoms into Rust engine", self.atoms.len());
        Ok(())
    }

    fn add_atom(&mut self, atom: CRODAtom) {
        // Update indexes
        self.content_index
            .entry(atom.content.to_lowercase())
            .or_insert_with(Vec::new)
            .push(atom.id.clone());

        self.type_index
            .entry(atom.atom_type.clone())
            .or_insert_with(Vec::new)
            .push(atom.id.clone());

        self.category_index
            .entry(atom.category.clone())
            .or_insert_with(Vec::new)
            .push(atom.id.clone());

        self.atoms.insert(atom.id.clone(), atom);
    }

    // ULTRA FAST SEARCH - NO SQL BULLSHIT!
    fn search_content(&self, query: &str) -> Vec<&CRODAtom> {
        let query_lower = query.to_lowercase();
        self.atoms
            .values()
            .filter(|atom| atom.content.to_lowercase().contains(&query_lower))
            .collect()
    }

    fn search_regex(&self, pattern: &str) -> Vec<&CRODAtom> {
        if let Ok(re) = Regex::new(pattern) {
            self.atoms
                .values()
                .filter(|atom| re.is_match(&atom.content))
                .collect()
        } else {
            Vec::new()
        }
    }

    fn get_by_type(&self, atom_type: &str) -> Vec<&CRODAtom> {
        if let Some(atom_ids) = self.type_index.get(atom_type) {
            atom_ids
                .iter()
                .filter_map(|id| self.atoms.get(id))
                .collect()
        } else {
            Vec::new()
        }
    }

    fn get_high_heat(&self, threshold: f64) -> Vec<&CRODAtom> {
        self.atoms
            .values()
            .filter(|atom| atom.heat >= threshold)
            .collect()
    }

    fn get_most_mentioned(&self, limit: usize) -> Vec<&CRODAtom> {
        let mut atoms: Vec<&CRODAtom> = self.atoms.values().collect();
        atoms.sort_by(|a, b| b.mention_count.cmp(&a.mention_count));
        atoms.into_iter().take(limit).collect()
    }

    // PATTERN DETECTION IN RUST!
    fn detect_technology_patterns(&self) -> Vec<CRODPattern> {
        let mut patterns = Vec::new();
        
        // Group technologies by category
        let tech_atoms = self.get_by_type("technology");
        let mut category_groups: HashMap<String, Vec<String>> = HashMap::new();
        
        for atom in tech_atoms {
            category_groups
                .entry(atom.category.clone())
                .or_insert_with(Vec::new)
                .push(atom.id.clone());
        }
        
        for (category, atom_ids) in category_groups {
            if atom_ids.len() >= 2 {
                let pattern = CRODPattern {
                    id: format!("pattern_{}_{}", category, atom_ids.len()),
                    atoms: atom_ids,
                    pattern_type: "technology_cluster".to_string(),
                    strength: 0.8,
                    connections: Vec::new(),
                };
                patterns.push(pattern);
            }
        }
        
        patterns
    }

    fn detect_performance_patterns(&self) -> Vec<CRODPattern> {
        let mut patterns = Vec::new();
        
        let perf_atoms = self.get_by_type("performance");
        if perf_atoms.len() >= 3 {
            let atom_ids: Vec<String> = perf_atoms.iter().map(|a| a.id.clone()).collect();
            let pattern = CRODPattern {
                id: "pattern_performance_cluster".to_string(),
                atoms: atom_ids,
                pattern_type: "performance_cluster".to_string(),
                strength: 0.9,
                connections: Vec::new(),
            };
            patterns.push(pattern);
        }
        
        patterns
    }

    // COMPLEX QUERIES IN RUST!
    fn complex_query(&self, query: &str) -> Vec<&CRODAtom> {
        match query {
            "high_performance_tech" => {
                self.atoms
                    .values()
                    .filter(|atom| {
                        atom.atom_type == "technology" 
                        && atom.heat >= 0.8
                        && (atom.content.contains("fast") 
                            || atom.content.contains("performance")
                            || atom.content.contains("speed"))
                    })
                    .collect()
            },
            "critical_security" => {
                self.atoms
                    .values()
                    .filter(|atom| {
                        atom.category == "security" 
                        && atom.heat >= 0.7
                        && atom.mention_count >= 2
                    })
                    .collect()
            },
            "immediate_wins" => {
                self.atoms
                    .values()
                    .filter(|atom| {
                        atom.content.contains("week") 
                        || atom.content.contains("day")
                        || atom.content.contains("easy")
                    })
                    .collect()
            },
            _ => self.search_content(query),
        }
    }

    // STATISTICS - FUCK SQL AGGREGATIONS!
    fn get_stats(&self) -> HashMap<String, u32> {
        let mut stats = HashMap::new();
        
        stats.insert("total_atoms".to_string(), self.atoms.len() as u32);
        
        let mut type_counts = HashMap::new();
        let mut category_counts = HashMap::new();
        let mut high_heat_count = 0;
        
        for atom in self.atoms.values() {
            *type_counts.entry(atom.atom_type.clone()).or_insert(0) += 1;
            *category_counts.entry(atom.category.clone()).or_insert(0) += 1;
            
            if atom.heat >= 0.8 {
                high_heat_count += 1;
            }
        }
        
        stats.insert("high_heat_atoms".to_string(), high_heat_count);
        stats.insert("unique_types".to_string(), type_counts.len() as u32);
        stats.insert("unique_categories".to_string(), category_counts.len() as u32);
        
        stats
    }

    // PRINT RESULTS BEAUTIFULLY
    fn print_search_results(&self, results: Vec<&CRODAtom>, query: &str) {
        println!("\n🔍 Search results for: '{}'", query);
        println!("Found {} atoms:", results.len());
        
        for (i, atom) in results.iter().take(10).enumerate() {
            println!(
                "{}. [{}] {} (heat: {:.2}, mentions: {})", 
                i + 1,
                atom.atom_type,
                atom.content,
                atom.heat,
                atom.mention_count
            );
        }
        
        if results.len() > 10 {
            println!("... and {} more", results.len() - 10);
        }
    }
}

// MAIN DEMO FUNCTION
fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🦀 CROD Rust Knowledge Engine Starting...");
    
    let mut engine = CRODEngine::new();
    
    // Load CROD knowledge
    let knowledge_file = "/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH/crod_master_knowledge.jsonl";
    engine.load_from_jsonl(knowledge_file)?;
    
    // Show stats
    let stats = engine.get_stats();
    println!("\n📊 Engine Statistics:");
    for (key, value) in stats {
        println!("   {}: {}", key, value);
    }
    
    // Demo searches
    println!("\n🚀 Demo Searches:");
    
    let redis_results = engine.search_content("redis");
    engine.print_search_results(redis_results, "redis");
    
    let tech_results = engine.get_by_type("technology");
    println!("\n🔧 Technologies: {} found", tech_results.len());
    for tech in tech_results.iter().take(5) {
        println!("   {} (heat: {:.2})", tech.content, tech.heat);
    }
    
    let high_heat = engine.get_high_heat(0.8);
    println!("\n🔥 High heat atoms: {} found", high_heat.len());
    
    let most_mentioned = engine.get_most_mentioned(5);
    println!("\n🏆 Most mentioned:");
    for atom in most_mentioned {
        println!("   {} ({} mentions)", atom.content, atom.mention_count);
    }
    
    // Complex queries
    let perf_tech = engine.complex_query("high_performance_tech");
    engine.print_search_results(perf_tech, "high_performance_tech");
    
    // Pattern detection
    let tech_patterns = engine.detect_technology_patterns();
    println!("\n🔗 Detected {} technology patterns", tech_patterns.len());
    
    let perf_patterns = engine.detect_performance_patterns();
    println!("🔗 Detected {} performance patterns", perf_patterns.len());
    
    println!("\n✅ RUST ENGINE DEMO COMPLETE!");
    println!("🦀 NO SQL, NO BULLSHIT, JUST PURE RUST SPEED!");
    
    Ok(())
}