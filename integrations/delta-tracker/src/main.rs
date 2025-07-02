use anyhow::Result;
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use clap::Parser;
use rusqlite::{params, Connection, OptionalExtension};
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    net::SocketAddr,
    sync::{Arc, Mutex},
};
use tokio::signal;
use tower_http::cors::CorsLayer;
use tracing::{info, warn};

mod models;
mod ml_bridge;

use models::*;
use ml_bridge::MLBridge;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Port to listen on
    #[arg(short, long, default_value_t = 8000)]
    port: u16,

    /// Database path
    #[arg(short, long, default_value = "crod.db")]
    database: String,
}

#[derive(Clone)]
struct AppState {
    db: Arc<Mutex<Connection>>,
    version: String,
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    let args = Args::parse();
    info!("Starting CROD Delta Tracker v0.1.0 on port {}", args.port);

    // Initialize database
    let conn = Connection::open(&args.database)?;
    init_database(&conn)?;
    
    // Update version in database
    let version = env!("CARGO_PKG_VERSION");
    conn.execute(
        "INSERT OR REPLACE INTO version_info (version_id, version_string) VALUES (1, ?1)",
        params![version],
    )?;
    
    let state = AppState {
        db: Arc::new(Mutex::new(conn)),
        version: version.to_string(),
    };

    // Build router
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/atom/:key", get(get_atom).post(create_atom))
        .route("/atoms", get(list_atoms))
        .route("/pattern", post(create_pattern))
        .route("/delta", post(track_delta))
        .route("/ml/process", post(ml_process))
        .layer(CorsLayer::permissive())
        .with_state(state);

    let addr = SocketAddr::from(([127, 0, 0, 1], args.port));
    info!("Listening on http://{}", addr);

    // Start server with graceful shutdown
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    info!("Shutting down gracefully...");
}

// Health check endpoint
async fn health_check(State(state): State<AppState>) -> Result<Json<HealthResponse>, StatusCode> {
    let db_ok = state.db.lock().unwrap().execute("SELECT 1", []).is_ok();
    
    Ok(Json(HealthResponse {
        status: if db_ok { "healthy" } else { "unhealthy" },
        version: state.version.clone(),
        database: db_ok,
    }))
}

// Get atom by key
async fn get_atom(
    State(state): State<AppState>,
    Path(key): Path<i64>,
) -> Result<Json<Atom>, StatusCode> {
    let db = state.db.lock().unwrap();
    
    let atom = db
        .query_row(
            "SELECT atom_key, atom_type, atom_value, prime_number, weight, heat 
             FROM atoms WHERE atom_key = ?1",
            params![key],
            |row| {
                Ok(Atom {
                    atom_key: row.get(0)?,
                    atom_type: row.get(1)?,
                    atom_value: row.get(2)?,
                    prime_number: row.get(3)?,
                    weight: row.get(4)?,
                    heat: row.get(5)?,
                })
            },
        )
        .optional()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    match atom {
        Some(atom) => Ok(Json(atom)),
        None => Err(StatusCode::NOT_FOUND),
    }
}

// Create new atom
async fn create_atom(
    State(state): State<AppState>,
    Path(key): Path<i64>,
    Json(payload): Json<CreateAtomRequest>,
) -> Result<Json<Atom>, StatusCode> {
    // Validate key range
    if !(11111..=11999).contains(&key) && key > 100 {
        return Err(StatusCode::BAD_REQUEST);
    }

    let db = state.db.lock().unwrap();
    
    // Insert atom
    db.execute(
        "INSERT INTO atoms (atom_key, atom_type, atom_value, prime_number) 
         VALUES (?1, ?2, ?3, ?4)",
        params![key, payload.atom_type, payload.atom_value, key], // Using key as prime for now
    )
    .map_err(|_| StatusCode::CONFLICT)?;

    // Track delta
    let delta = Delta {
        source_chain: "http-api".to_string(),
        delta_type: "atom_added".to_string(),
        delta_data: serde_json::json!({
            "key": key,
            "type": payload.atom_type,
            "value": payload.atom_value,
        }),
    };
    
    let _ = db.execute(
        "INSERT INTO deltas (source_chain, delta_type, delta_data) 
         VALUES (?1, ?2, ?3)",
        params![delta.source_chain, delta.delta_type, delta.delta_data.to_string()],
    );

    // Return created atom
    get_atom(State(state), Path(key)).await
}

// List atoms with optional filters
async fn list_atoms(
    State(state): State<AppState>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<Json<Vec<Atom>>, StatusCode> {
    let db = state.db.lock().unwrap();
    
    let mut query = String::from("SELECT atom_key, atom_type, atom_value, prime_number, weight, heat FROM atoms WHERE 1=1");
    let mut query_params: Vec<String> = Vec::new();
    
    // Build dynamic query
    if let Some(atom_type) = params.get("type") {
        query.push_str(" AND atom_type = ?");
        query_params.push(atom_type.clone());
    }
    
    if let Some(min_heat) = params.get("min_heat") {
        query.push_str(" AND heat >= ?");
        query_params.push(min_heat.clone());
    }
    
    query.push_str(" LIMIT 100");
    
    // Execute query
    let mut stmt = db.prepare(&query).map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let atoms: Vec<Atom> = stmt
        .query_map(
            rusqlite::params_from_iter(query_params.iter()),
            |row| {
                Ok(Atom {
                    atom_key: row.get(0)?,
                    atom_type: row.get(1)?,
                    atom_value: row.get(2)?,
                    prime_number: row.get(3)?,
                    weight: row.get(4)?,
                    heat: row.get(5)?,
                })
            },
        )
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok(Json(atoms))
}

// Create pattern between atoms
async fn create_pattern(
    State(state): State<AppState>,
    Json(payload): Json<CreatePatternRequest>,
) -> Result<Json<Pattern>, StatusCode> {
    let pattern_key = payload.atom1_key * payload.atom2_key;
    let db = state.db.lock().unwrap();
    
    // Insert or update pattern
    db.execute(
        "INSERT INTO patterns (pattern_key, atom1_key, atom2_key, strength) 
         VALUES (?1, ?2, ?3, ?4)
         ON CONFLICT(atom1_key, atom2_key) DO UPDATE SET
         occurrences = occurrences + 1,
         strength = strength * 0.9 + 0.1",
        params![pattern_key, payload.atom1_key, payload.atom2_key, 0.5],
    )
    .map_err(|_| StatusCode::BAD_REQUEST)?;
    
    // Update heat for both atoms
    let _ = db.execute(
        "UPDATE atoms SET heat = heat * 0.95 + 0.05 WHERE atom_key IN (?1, ?2)",
        params![payload.atom1_key, payload.atom2_key],
    );
    
    // Automatically detect patterns if heat is high
    if let Ok(heat) = db.query_row(
        "SELECT AVG(heat) FROM atoms WHERE atom_key IN (?1, ?2)",
        params![payload.atom1_key, payload.atom2_key],
        |row| row.get::<_, f64>(0),
    ) {
        if heat > 0.7 {
            // Strong pattern detected, increase strength
            let _ = db.execute(
                "UPDATE patterns SET strength = strength + 0.1 WHERE pattern_key = ?1",
                params![pattern_key],
            );
        }
    }
    
    Ok(Json(Pattern {
        pattern_key,
        atom1_key: payload.atom1_key,
        atom2_key: payload.atom2_key,
        occurrences: 1,
        strength: 0.5,
    }))
}

// Track delta
async fn track_delta(
    State(state): State<AppState>,
    Json(delta): Json<Delta>,
) -> Result<StatusCode, StatusCode> {
    let db = state.db.lock().unwrap();
    
    db.execute(
        "INSERT INTO deltas (source_chain, delta_type, delta_data) 
         VALUES (?1, ?2, ?3)",
        params![delta.source_chain, delta.delta_type, delta.delta_data.to_string()],
    )
    .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok(StatusCode::CREATED)
}

fn init_database(conn: &Connection) -> Result<()> {
    // Execute schema
    let schema = std::fs::read_to_string("schema_simple.sql")?;
    conn.execute_batch(&schema)?;
    
    info!("Database initialized");
    Ok(())
}

// ML Processing endpoint
async fn ml_process(
    State(state): State<AppState>,
    Json(payload): Json<MLProcessRequest>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    // Call Python ML processor
    let ml_response = MLBridge::process_tokens(payload.tokens)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    // Store results in database
    let db = state.db.lock().unwrap();
    
    // Update atoms with ML results
    for atom_result in &ml_response.result.atoms {
        let _ = db.execute(
            "UPDATE atoms SET heat = ?1 WHERE atom_value = ?2",
            params![atom_result.heat, atom_result.token],
        );
    }
    
    // Track delta
    let delta = Delta {
        source_chain: "ml-processor".to_string(),
        delta_type: "ml_processed".to_string(),
        delta_data: serde_json::json!({
            "atoms_processed": ml_response.metrics.atoms_processed,
            "patterns_found": ml_response.metrics.patterns_found,
            "consciousness": ml_response.result.consciousness,
        }),
    };
    
    let _ = db.execute(
        "INSERT INTO deltas (source_chain, delta_type, delta_data) VALUES (?1, ?2, ?3)",
        params![delta.source_chain, delta.delta_type, delta.delta_data.to_string()],
    );
    
    Ok(Json(serde_json::to_value(ml_response).unwrap()))
}