mod db_engine;

use axum::{
    routing::{get, post},
    Json, Router,
    extract::State,
};
use std::net::SocketAddr;
use std::sync::Arc;
use serde::{Serialize, Deserialize};

#[derive(Serialize)]
struct Status {
    status: String,
    engine: String,
    patterns_stored: usize,
}

#[tokio::main]
async fn main() {
    println!("🦀 CROD Rust Database Engine starting...");
    
    let db = Arc::new(db_engine::CrodDatabase::new());
    
    let app = Router::new()
        .route("/", get(root))
        .route("/status", get(status))
        .route("/pattern", post(store_pattern))
        .with_state(db);
    
    let addr = SocketAddr::from(([127, 0, 0, 1], 7000));
    println!("🚀 Rust DB Engine listening on {}", addr);
    
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> &'static str {
    "CROD Rust Database Engine v1.0"
}

async fn status() -> Json<Status> {
    Json(Status {
        status: "running".to_string(),
        engine: "rust-rocksdb".to_string(),
        patterns_stored: 0,
    })
}

#[derive(Deserialize)]
struct PatternRequest {
    name: String,
    data: Vec<f64>,
    confidence: f64,
}

async fn store_pattern(
    State(db): State<Arc<db_engine::CrodDatabase>>,
    Json(req): Json<PatternRequest>,
) -> Json<serde_json::Value> {
    let pattern = db_engine::Pattern {
        id: uuid::Uuid::new_v4().to_string(),
        name: req.name,
        confidence: req.confidence,
        data: req.data,
        discovered_at: chrono::Utc::now(),
        connections: vec![],
    };
    
    match db.store_pattern(pattern.clone()).await {
        Ok(_) => Json(serde_json::json!({
            "success": true,
            "id": pattern.id,
            "message": "Pattern stored successfully"
        })),
        Err(e) => Json(serde_json::json!({
            "success": false,
            "error": e
        }))
    }
}