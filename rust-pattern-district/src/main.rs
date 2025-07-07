use std::sync::Arc;
use std::time::Duration;
use std::collections::HashMap;

use anyhow::Result;
use axum::{
    routing::{get, post},
    extract::{ws::WebSocket, WebSocketUpgrade, State},
    response::IntoResponse,
    Json, Router,
};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;
use tracing::{info, error};

mod patterns;
mod analyzer;
mod nats_handler;

use patterns::{PatternEngine, Pattern};
use analyzer::PatternAnalyzer;
use nats_handler::NatsHandler;

#[derive(Clone)]
struct AppState {
    pattern_engine: Arc<PatternEngine>,
    analyzer: Arc<PatternAnalyzer>,
    nats: Arc<NatsHandler>,
    cache: Arc<DashMap<String, PatternResult>>,
    stats: Arc<RwLock<ServiceStats>>,
}

#[derive(Default, Serialize)]
struct ServiceStats {
    patterns_analyzed: u64,
    cache_hits: u64,
    cache_misses: u64,
    average_processing_time_ms: f64,
    active_connections: u32,
}

#[derive(Deserialize)]
struct AnalyzeRequest {
    text: String,
    context: Option<HashMap<String, String>>,
    priority: Option<String>,
}

#[derive(Serialize, Clone)]
struct PatternResult {
    patterns: Vec<Pattern>,
    confidence: f64,
    processing_time_ms: u64,
    metadata: HashMap<String, String>,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    info!("🦀 Rust Pattern District starting on port 7007...");

    // Initialize components
    let pattern_engine = Arc::new(PatternEngine::new().await?);
    let analyzer = Arc::new(PatternAnalyzer::new());
    let nats = Arc::new(NatsHandler::new().await?);
    let cache = Arc::new(DashMap::new());
    let stats = Arc::new(RwLock::new(ServiceStats::default()));

    let app_state = AppState {
        pattern_engine: pattern_engine.clone(),
        analyzer,
        nats: nats.clone(),
        cache,
        stats,
    };

    // Start NATS subscriptions
    let nats_state = app_state.clone();
    tokio::spawn(async move {
        if let Err(e) = nats_handler::start_subscriptions(nats_state).await {
            error!("NATS subscription error: {}", e);
        }
    });

    // Announce to Phoenix Rathaus
    nats.announce_district().await?;

    // Build router
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/analyze", post(analyze_pattern))
        .route("/patterns", get(get_patterns))
        .route("/stats", get(get_stats))
        .route("/ws", get(websocket_handler))
        .layer(CorsLayer::permissive())
        .with_state(app_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:7007").await?;
    info!("🚀 Rust Pattern District listening on port 7007");
    
    axum::serve(listener, app).await?;
    Ok(())
}

async fn root() -> impl IntoResponse {
    Json(serde_json::json!({
        "service": "Rust Pattern District",
        "version": "0.1.0",
        "status": "operational",
        "capabilities": ["pattern_matching", "high_performance", "real_time"]
    }))
}

async fn health() -> impl IntoResponse {
    Json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now()
    }))
}

async fn analyze_pattern(
    State(state): State<AppState>,
    Json(request): Json<AnalyzeRequest>,
) -> impl IntoResponse {
    let start = std::time::Instant::now();

    // Check cache first
    if let Some(cached) = state.cache.get(&request.text) {
        let mut stats = state.stats.write().await;
        stats.cache_hits += 1;
        return Json(cached.clone());
    }

    // Perform analysis
    let patterns = state.pattern_engine.find_patterns(&request.text).await;
    let confidence = state.analyzer.calculate_confidence(&patterns, &request.text);
    
    let result = PatternResult {
        patterns,
        confidence,
        processing_time_ms: start.elapsed().as_millis() as u64,
        metadata: request.context.unwrap_or_default(),
    };

    // Update cache
    state.cache.insert(request.text.clone(), result.clone());

    // Update stats
    {
        let mut stats = state.stats.write().await;
        stats.patterns_analyzed += 1;
        stats.cache_misses += 1;
        stats.average_processing_time_ms = 
            (stats.average_processing_time_ms * (stats.patterns_analyzed - 1) as f64 
             + result.processing_time_ms as f64) / stats.patterns_analyzed as f64;
    }

    // Publish result to NATS
    if let Err(e) = state.nats.publish_pattern_result(&result).await {
        error!("Failed to publish pattern result: {}", e);
    }

    Json(result)
}

async fn get_patterns(State(state): State<AppState>) -> impl IntoResponse {
    let patterns = state.pattern_engine.get_all_patterns().await;
    Json(serde_json::json!({
        "patterns": patterns,
        "count": patterns.len()
    }))
}

async fn get_stats(State(state): State<AppState>) -> impl IntoResponse {
    let stats = state.stats.read().await;
    Json(&*stats)
}

async fn websocket_handler(
    ws: WebSocketUpgrade,
    State(state): State<AppState>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: AppState) {
    {
        let mut stats = state.stats.write().await;
        stats.active_connections += 1;
    }

    // Handle WebSocket messages
    while let Some(msg) = socket.recv().await {
        if let Ok(msg) = msg {
            // Process WebSocket messages here
        } else {
            break;
        }
    }

    {
        let mut stats = state.stats.write().await;
        stats.active_connections -= 1;
    }
}