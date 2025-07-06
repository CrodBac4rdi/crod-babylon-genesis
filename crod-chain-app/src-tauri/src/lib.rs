use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use tauri::State;

mod blockchain;
mod crod_core;

use blockchain::{Block, Blockchain};
use crod_core::{CRODEngine, Pattern};

#[derive(Default)]
struct AppState {
    blockchain: Mutex<Blockchain>,
    crod_engine: Mutex<CRODEngine>,
}

#[derive(Debug, Serialize, Deserialize)]
struct SystemStatus {
    blocks_mined: usize,
    patterns_learned: usize,
    quantum_entanglement: f64,
    is_running: bool,
}

#[tauri::command]
fn get_system_status(state: State<AppState>) -> Result<SystemStatus, String> {
    let blockchain = state.blockchain.lock().map_err(|e| e.to_string())?;
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    
    Ok(SystemStatus {
        blocks_mined: blockchain.chain.len(),
        patterns_learned: engine.patterns.len(),
        quantum_entanglement: engine.quantum_level,
        is_running: engine.is_active,
    })
}

#[tauri::command]
fn mine_block(data: serde_json::Value, state: State<AppState>) -> Result<Block, String> {
    let mut blockchain = state.blockchain.lock().map_err(|e| e.to_string())?;
    let block = blockchain.add_block(data);
    Ok(block)
}

#[tauri::command]
fn learn_pattern(pattern: Pattern, state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.learn(pattern);
    Ok(())
}

#[tauri::command]
fn toggle_parasite(state: State<AppState>) -> Result<bool, String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.is_active = !engine.is_active;
    Ok(engine.is_active)
}

#[tauri::command]
fn start_system(state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.is_active = true;
    
    // Initialize with genesis block
    let mut blockchain = state.blockchain.lock().map_err(|e| e.to_string())?;
    if blockchain.chain.is_empty() {
        blockchain.initialize();
    }
    
    Ok(())
}

#[tauri::command]
fn stop_system(state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.is_active = false;
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_updater::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_sql::init())
        .plugin(tauri_plugin_dialog::init())
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            get_system_status,
            mine_block,
            learn_pattern,
            toggle_parasite,
            start_system,
            stop_system
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}