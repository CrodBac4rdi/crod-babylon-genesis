use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use nats::Connection;
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    env,
    sync::{Arc, Mutex},
};
use tower_http::cors::CorsLayer;
use tracing::{info, warn};

#[derive(Clone)]
struct AppState {
    nats_conn: Arc<Mutex<Connection>>,
    patterns: Arc<Mutex<HashMap<String, Pattern>>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Pattern {
    id: String,
    name: String,
    regex: String,
    weight: f32,
}

#[derive(Serialize)]
struct ServiceInfo {
    service: String,
    port: u16,
    status: String,
    patterns_loaded: usize,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let port = env::var("PORT").unwrap_or_else(|_| "7007".to_string());
    let nats_url = env::var("NATS_URL").unwrap_or_else(|_| "nats://localhost:4222".to_string());

    // Connect to NATS
    let nc = nats::connect(&nats_url).expect("Failed to connect to NATS");
    info!("Connected to NATS at {}", nats_url);

    // Announce presence
    let _ = nc.publish(
        "crod.district.online",
        serde_json::to_string(&serde_json::json!({
            "district": "rust-pattern",
            "port": port.parse::<u16>().unwrap_or(7007)
        }))
        .unwrap(),
    );

    // Initialize patterns
    let mut patterns = HashMap::new();
    patterns.insert(
        "trinity".to_string(),
        Pattern {
            id: "trinity".to_string(),
            name: "Trinity Pattern".to_string(),
            regex: r"ich.*bins.*wieder".to_string(),
            weight: 1.0,
        },
    );
    patterns.insert(
        "crod".to_string(),
        Pattern {
            id: "crod".to_string(),
            name: "CROD Pattern".to_string(),
            regex: r"crod|CROD|Crod".to_string(),
            weight: 0.8,
        },
    );

    let state = AppState {
        nats_conn: Arc::new(Mutex::new(nc)),
        patterns: Arc::new(Mutex::new(patterns)),
    };

    // Subscribe to pattern requests
    let state_clone = state.clone();
    tokio::spawn(async move {
        loop {
            if let Ok(nc) = state_clone.nats_conn.lock() {
                if let Ok(sub) = nc.subscribe("crod.pattern.match") {
                    for msg in sub.messages() {
                        if let Ok(data) = serde_json::from_slice::<serde_json::Value>(&msg.data) {
                            info!("Pattern match request: {:?}", data);
                            // Process pattern matching here
                        }
                    }
                }
            }
            tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
        }
    });

    let app = Router::new()
        .route("/", get(index))
        .route("/patterns", get(get_patterns))
        .route("/match", post(match_pattern))
        .layer(CorsLayer::permissive())
        .with_state(state);

    let addr = format!("0.0.0.0:{}", port);
    info!("Rust Pattern District listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn index(State(state): State<AppState>) -> Json<ServiceInfo> {
    let patterns_count = state.patterns.lock().unwrap().len();
    Json(ServiceInfo {
        service: "CROD Rust Pattern District".to_string(),
        port: 7007,
        status: "matching".to_string(),
        patterns_loaded: patterns_count,
    })
}

async fn get_patterns(State(state): State<AppState>) -> Json<Vec<Pattern>> {
    let patterns = state.patterns.lock().unwrap();
    Json(patterns.values().cloned().collect())
}

#[derive(Deserialize)]
struct MatchRequest {
    text: String,
}

#[derive(Serialize)]
struct MatchResponse {
    matches: Vec<String>,
    confidence: f32,
}

async fn match_pattern(
    State(state): State<AppState>,
    Json(req): Json<MatchRequest>,
) -> Result<Json<MatchResponse>, StatusCode> {
    let patterns = state.patterns.lock().unwrap();
    let mut matches = Vec::new();
    let mut total_weight = 0.0;

    for (id, pattern) in patterns.iter() {
        if let Ok(re) = regex::Regex::new(&pattern.regex) {
            if re.is_match(&req.text) {
                matches.push(id.clone());
                total_weight += pattern.weight;
            }
        }
    }

    Ok(Json(MatchResponse {
        matches,
        confidence: total_weight.min(1.0),
    }))
}