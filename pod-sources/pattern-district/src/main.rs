use actix_web::{web, App, HttpResponse, HttpServer, Result};
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Atom {
    word: String,
    heat: f64,
    prime: Option<u32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Pattern {
    id: String,
    atoms: Vec<String>,
    strength: f64,
    occurrences: u32,
}

#[derive(Debug)]
struct PatternDistrict {
    patterns: Arc<Mutex<HashMap<String, Pattern>>>,
    atoms: Arc<Mutex<HashMap<String, Atom>>>,
    redis: Arc<Mutex<redis::aio::Connection>>,
}

impl PatternDistrict {
    async fn new() -> Result<Self, Box<dyn std::error::Error>> {
        let redis_url = std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379".to_string());
        let client = redis::Client::open(redis_url)?;
        let conn = client.get_async_connection().await?;
        
        Ok(PatternDistrict {
            patterns: Arc::new(Mutex::new(HashMap::new())),
            atoms: Arc::new(Mutex::new(HashMap::new())),
            redis: Arc::new(Mutex::new(conn)),
        })
    }

    async fn process_atoms(&self, atoms: Vec<Atom>) -> Result<String, Box<dyn std::error::Error>> {
        let mut patterns = self.patterns.lock().await;
        let mut atom_store = self.atoms.lock().await;
        
        // Store atoms
        for atom in &atoms {
            atom_store.insert(atom.word.clone(), atom.clone());
        }
        
        // Check for patterns (2+ atoms with high heat)
        if atoms.len() >= 2 {
            let hot_atoms: Vec<&Atom> = atoms.iter().filter(|a| a.heat > 50.0).collect();
            
            if hot_atoms.len() >= 2 {
                let pattern_id = hot_atoms.iter()
                    .map(|a| &a.word)
                    .collect::<Vec<_>>()
                    .join("-");
                
                let pattern = patterns.entry(pattern_id.clone()).or_insert(Pattern {
                    id: pattern_id.clone(),
                    atoms: hot_atoms.iter().map(|a| a.word.clone()).collect(),
                    strength: 0.0,
                    occurrences: 0,
                });
                
                pattern.occurrences += 1;
                pattern.strength = (pattern.occurrences as f64).sqrt() * 10.0;
                
                // Publish pattern detection
                let mut redis = self.redis.lock().await;
                let msg = serde_json::json!({
                    "from": "pattern-district",
                    "type": "pattern_detected",
                    "pattern_id": pattern_id,
                    "atoms": pattern.atoms,
                    "strength": pattern.strength,
                });
                
                let _: Result<(), redis::RedisError> = redis.publish("crod:patterns", msg.to_string()).await;
                
                return Ok(pattern_id);
            }
        }
        
        Ok("no_pattern".to_string())
    }
}

#[derive(Deserialize)]
struct ProcessRequest {
    atoms: Vec<Atom>,
}

async fn health() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "district": "pattern-district",
        "language": "rust",
        "port": 7007
    })))
}

async fn process_atoms(
    data: web::Json<ProcessRequest>,
    district: web::Data<PatternDistrict>,
) -> Result<HttpResponse> {
    match district.process_atoms(data.atoms.clone()).await {
        Ok(pattern_id) => Ok(HttpResponse::Ok().json(serde_json::json!({
            "processed": data.atoms.len(),
            "pattern_detected": pattern_id != "no_pattern",
            "pattern_id": pattern_id,
        }))),
        Err(e) => Ok(HttpResponse::InternalServerError().json(serde_json::json!({
            "error": e.to_string()
        }))),
    }
}

async fn get_patterns(district: web::Data<PatternDistrict>) -> Result<HttpResponse> {
    let patterns = district.patterns.lock().await;
    let pattern_list: Vec<&Pattern> = patterns.values().collect();
    
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "total_patterns": pattern_list.len(),
        "patterns": pattern_list,
    })))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    
    let port = std::env::var("PORT").unwrap_or_else(|_| "7007".to_string());
    let bind_addr = format!("0.0.0.0:{}", port);
    
    println!("🦀 Pattern District (Rust) starting on {}", bind_addr);
    
    let district = web::Data::new(
        PatternDistrict::new()
            .await
            .expect("Failed to create PatternDistrict")
    );
    
    HttpServer::new(move || {
        App::new()
            .app_data(district.clone())
            .route("/health", web::get().to(health))
            .route("/process", web::post().to(process_atoms))
            .route("/patterns", web::get().to(get_patterns))
    })
    .bind(&bind_addr)?
    .run()
    .await
}