use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::{
    net::SocketAddr,
    sync::Arc,
    time::Instant,
};
use tower_http::cors::CorsLayer;
use tracing::{info, error};
use tracing_subscriber;

mod pattern_engine;
mod nats_client;

use pattern_engine::{PatternEngine, Pattern, MatchResult};
use nats_client::NatsClient;

#[derive(Clone)]
struct AppState {
    pattern_engine: Arc<PatternEngine>,
    nats_client: Arc<NatsClient>,
    metrics: Arc<DashMap<String, u64>>,
}

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    service: String,
    patterns_loaded: usize,
    nats_connected: bool,
}

#[derive(Deserialize)]
struct MatchRequest {
    text: String,
    context: Option<serde_json::Value>,
}

#[derive(Serialize)]
struct MatchResponse {
    matches: Vec<MatchResult>,
    processing_time_ms: u128,
    patterns_checked: usize,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    
    info!("Starting Rust Pattern District on port 7007");
    
    // Initialize pattern engine
    let pattern_engine = Arc::new(PatternEngine::new());
    
    // Load CROD patterns
    if let Err(e) = pattern_engine.load_patterns("data/patterns").await {
        error!("Failed to load patterns: {}", e);
    }
    
    // Initialize NATS client
    let nats_client = Arc::new(
        NatsClient::new("nats://localhost:4222")
            .await
            .expect("Failed to connect to NATS")
    );
    
    // Subscribe to pattern topics
    let engine_clone = pattern_engine.clone();
    tokio::spawn(async move {
        nats_client.subscribe_patterns(engine_clone).await;
    });
    
    let app_state = AppState {
        pattern_engine,
        nats_client,
        metrics: Arc::new(DashMap::new()),
    };
    
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/match", post(match_patterns))
        .route("/patterns", get(list_patterns))
        .route("/patterns", post(add_pattern))
        .route("/metrics", get(get_metrics))
        .layer(CorsLayer::permissive())
        .with_state(app_state);
    
    let addr = SocketAddr::from(([127, 0, 0, 1], 7007));
    info!("Pattern District listening on {}", addr);
    
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn health_check(State(state): State<AppState>) -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "healthy".to_string(),
        service: "rust-pattern-district".to_string(),
        patterns_loaded: state.pattern_engine.pattern_count(),
        nats_connected: state.nats_client.is_connected().await,
    })
}

async fn match_patterns(
    State(state): State<AppState>,
    Json(request): Json<MatchRequest>,
) -> Result<Json<MatchResponse>, StatusCode> {
    let start = Instant::now();
    
    // Increment match counter
    state.metrics
        .entry("total_matches".to_string())
        .and_modify(|v| *v += 1)
        .or_insert(1);
    
    // Perform pattern matching
    let matches = state.pattern_engine.match_text(&request.text, request.context).await;
    
    let processing_time = start.elapsed().as_millis();
    
    // Publish results to NATS
    if !matches.is_empty() {
        let _ = state.nats_client.publish_matches(&matches).await;
    }
    
    Ok(Json(MatchResponse {
        matches,
        processing_time_ms: processing_time,
        patterns_checked: state.pattern_engine.pattern_count(),
    }))
}

async fn list_patterns(State(state): State<AppState>) -> Json<Vec<Pattern>> {
    Json(state.pattern_engine.list_patterns())
}

async fn add_pattern(
    State(state): State<AppState>,
    Json(pattern): Json<Pattern>,
) -> Result<StatusCode, StatusCode> {
    match state.pattern_engine.add_pattern(pattern).await {
        Ok(_) => Ok(StatusCode::CREATED),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn get_metrics(State(state): State<AppState>) -> Json<serde_json::Value> {
    let mut metrics = serde_json::Map::new();
    
    for entry in state.metrics.iter() {
        metrics.insert(entry.key().clone(), serde_json::Value::Number((*entry.value()).into()));
    }
    
    Json(serde_json::Value::Object(metrics))
}