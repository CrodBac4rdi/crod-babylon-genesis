use tokio;
use nats;
use serde::{Deserialize, Serialize};
use serde_json;
use dashmap::DashMap;
use rayon::prelude::*;
use axum::{
    Router,
    routing::get,
    response::Json,
    extract::State,
};
use std::sync::Arc;
use std::time::SystemTime;
use tracing::{info, error};
use tracing_subscriber;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct PatternResult {
    atoms: usize,
    primes: Vec<u64>,
    patterns: Vec<String>,
    timestamp: u64,
    trinity_score: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct HealthStatus {
    service: String,
    port: u16,
    status: String,
    patterns_processed: u64,
    cache_size: usize,
}

struct AppState {
    pattern_cache: DashMap<String, PatternResult>,
    patterns_processed: Arc<tokio::sync::Mutex<u64>>,
    nats_client: Arc<tokio::sync::Mutex<Option<nats::Connection>>>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::fmt::init();
    
    info!("🦀 CROD Pattern District (Rust) starting on port 7007...");
    
    // Create shared state
    let state = Arc::new(AppState {
        pattern_cache: DashMap::new(),
        patterns_processed: Arc::new(tokio::sync::Mutex::new(0)),
        nats_client: Arc::new(tokio::sync::Mutex::new(None)),
    });
    
    // Connect to NATS
    let nats_state = state.clone();
    tokio::spawn(async move {
        loop {
            match nats::connect("nats://localhost:4222") {
                Ok(nc) => {
                    info!("✅ Connected to NATS");
                    
                    // Subscribe to pattern requests
                    let sub = nc.subscribe("pattern.user_input").unwrap();
                    *nats_state.nats_client.lock().await = Some(nc.clone());
                    
                    // Process messages
                    for msg in sub.messages() {
                        let input = String::from_utf8(msg.data).unwrap_or_default();
                        let pattern_cache = &nats_state.pattern_cache;
                        let result = analyze_patterns(&input, pattern_cache).await;
                        
                        // Increment counter
                        let mut count = nats_state.patterns_processed.lock().await;
                        *count += 1;
                        
                        // Publish results
                        let _ = nc.publish("pattern.results", serde_json::to_string(&result).unwrap());
                        
                        info!("Processed pattern for: {}", input.chars().take(50).collect::<String>());
                    }
                }
                Err(e) => {
                    error!("Failed to connect to NATS: {}, retrying in 5s...", e);
                    tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
                }
            }
        }
    });
    
    // Build HTTP router
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/patterns", get(patterns))
        .route("/test", get(test))
        .with_state(state);
    
    // Start HTTP server
    let listener = tokio::net::TcpListener::bind("0.0.0.0:7007").await?;
    info!("🌐 HTTP server listening on http://0.0.0.0:7007");
    
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn root() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "service": "CROD Pattern District",
        "language": "Rust",
        "port": 7007,
        "status": "active",
        "performance": "ultra-fast"
    }))
}

async fn health(State(state): State<Arc<AppState>>) -> Json<HealthStatus> {
    let patterns_processed = *state.patterns_processed.lock().await;
    let cache_size = state.pattern_cache.len();
    
    Json(HealthStatus {
        service: "crod-pattern-rust".to_string(),
        port: 7007,
        status: "healthy".to_string(),
        patterns_processed,
        cache_size,
    })
}

async fn patterns(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let patterns_processed = *state.patterns_processed.lock().await;
    let cache_entries: Vec<(String, PatternResult)> = state.pattern_cache
        .iter()
        .take(10)
        .map(|entry| (entry.key().clone(), entry.value().clone()))
        .collect();
    
    Json(serde_json::json!({
        "total_processed": patterns_processed,
        "cache_size": state.pattern_cache.len(),
        "recent_patterns": cache_entries
    }))
}

async fn test() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "Rust returns patterns"
    }))
}

async fn analyze_patterns(input: &str, cache: &DashMap<String, PatternResult>) -> PatternResult {
    // Check cache first
    if let Some(cached) = cache.get(input) {
        return cached.clone();
    }
    
    let tokens: Vec<&str> = input.split_whitespace().collect();
    
    // Parallel prime calculation for neurons
    let primes: Vec<u64> = tokens.par_iter()
        .map(|token| calculate_prime_id(token))
        .collect();
    
    // Trinity pattern detection
    let trinity_score = calculate_trinity_score(input);
    
    // Detect patterns
    let patterns = detect_patterns(&tokens);
    
    let result = PatternResult {
        atoms: tokens.len(),
        primes,
        patterns,
        timestamp: SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .unwrap()
            .as_secs(),
        trinity_score,
    };
    
    // Cache result
    cache.insert(input.to_string(), result.clone());
    
    result
}

fn calculate_prime_id(token: &str) -> u64 {
    // Simple hash to prime-like number
    let mut hash = 0u64;
    for byte in token.bytes() {
        hash = hash.wrapping_mul(31).wrapping_add(byte as u64);
    }
    
    // Find next prime-like number
    let mut n = hash | 1; // Make odd
    while !is_prime_like(n) {
        n += 2;
    }
    n
}

fn is_prime_like(n: u64) -> bool {
    if n < 2 { return false; }
    if n == 2 { return true; }
    if n % 2 == 0 { return false; }
    
    let sqrt_n = (n as f64).sqrt() as u64;
    for i in (3..=sqrt_n).step_by(2) {
        if n % i == 0 { return false; }
    }
    true
}

fn calculate_trinity_score(input: &str) -> u32 {
    let input_lower = input.to_lowercase();
    let mut score = 0u32;
    
    // Trinity values
    score += input_lower.matches("ich").count() as u32 * 2;
    score += input_lower.matches("bins").count() as u32 * 3;
    score += input_lower.matches("wieder").count() as u32 * 5;
    score += input_lower.matches("daniel").count() as u32 * 67;
    score += input_lower.matches("claude").count() as u32 * 71;
    score += input_lower.matches("crod").count() as u32 * 17;
    
    score
}

fn detect_patterns(tokens: &[&str]) -> Vec<String> {
    let mut patterns = Vec::new();
    
    // Pattern: Repeated tokens
    let mut token_counts = std::collections::HashMap::new();
    for token in tokens {
        *token_counts.entry(*token).or_insert(0) += 1;
    }
    
    for (token, count) in token_counts {
        if count > 1 {
            patterns.push(format!("repeated:{} ({}x)", token, count));
        }
    }
    
    // Pattern: Sequential length increase
    if tokens.len() > 2 {
        let lengths: Vec<usize> = tokens.iter().map(|t| t.len()).collect();
        let mut increasing = true;
        for i in 1..lengths.len() {
            if lengths[i] <= lengths[i-1] {
                increasing = false;
                break;
            }
        }
        if increasing {
            patterns.push("sequential_length_increase".to_string());
        }
    }
    
    // Pattern: Alternating case
    if tokens.len() > 1 {
        let mut alternating = true;
        for i in 0..tokens.len() {
            let expected_case = i % 2 == 0;
            let is_upper = tokens[i].chars().next().unwrap_or('a').is_uppercase();
            if is_upper != expected_case {
                alternating = false;
                break;
            }
        }
        if alternating {
            patterns.push("alternating_case".to_string());
        }
    }
    
    patterns
}