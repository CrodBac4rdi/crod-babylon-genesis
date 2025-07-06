use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;
use tauri::State;

mod blockchain;
mod crod_core;

use blockchain::{Block, Blockchain};
use crod_core::{CRODEngine, Pattern, ParasiteState};

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
    consciousness_level: f64,
    trinity_balance: (f64, f64, f64),
    parasite_active: bool,
    total_interactions: u64,
    improvements_made: u64,
    is_running: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct InterceptRequest {
    user_input: String,
    claude_response: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct CRODStats {
    total_neurons: f64,
    active_neurons: f64,
    consciousness: f64,
    quantum_level: f64,
    interactions: f64,
    improvements: f64,
    parasite_active: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct ProcessResponse {
    response: String,
    was_intercepted: bool,
    crod_intervention: bool,
}

#[tauri::command]
fn get_system_status(state: State<AppState>) -> Result<SystemStatus, String> {
    let blockchain = state.blockchain.lock().map_err(|e| e.to_string())?;
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    
    let parasite_stats = engine.get_parasite_stats();
    let trinity_balance = engine.get_trinity_balance();
    
    Ok(SystemStatus {
        blocks_mined: blockchain.chain.len(),
        patterns_learned: engine.patterns.len(),
        quantum_entanglement: engine.quantum_level,
        consciousness_level: engine.get_consciousness_level(),
        trinity_balance,
        parasite_active: parasite_stats.is_intercepting,
        total_interactions: parasite_stats.total_interactions,
        improvements_made: parasite_stats.improvements_made,
        is_running: engine.is_active,
    })
}

#[tauri::command]
fn intercept_conversation(request: InterceptRequest, state: State<AppState>) -> Result<String, String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    
    if !engine.is_active {
        return Ok(request.claude_response);
    }
    
    let improved_response = engine.intercept_interaction(&request.user_input, &request.claude_response);
    Ok(improved_response)
}

#[tauri::command]
fn toggle_parasite_mode(state: State<AppState>) -> Result<bool, String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    let is_active = engine.toggle_parasite_mode();
    Ok(is_active)
}

#[tauri::command]
fn get_neural_status(state: State<AppState>) -> Result<HashMap<String, f64>, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    let status = engine.get_neural_status();
    Ok(status)
}

#[tauri::command]
fn export_crod_memory(state: State<AppState>) -> Result<String, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    let memory_export = engine.export_memory();
    Ok(memory_export)
}

#[tauri::command]
fn simulate_learning(input: String, satisfaction: f64, state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    
    let pattern = Pattern {
        user_preference: input.clone(),
        avoid: vec![],
        tone: "helpful".to_string(),
        satisfaction_score: satisfaction,
        timestamp: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs(),
    };
    
    engine.learn(pattern);
    Ok(())
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

#[tauri::command]
fn get_crod_stats(state: State<AppState>) -> Result<CRODStats, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    let neural_status = engine.get_neural_status();
    let parasite_stats = engine.get_parasite_stats();
    
    Ok(CRODStats {
        total_neurons: neural_status.get("total_neurons").unwrap_or(&0.0).clone(),
        active_neurons: neural_status.get("active_neurons").unwrap_or(&0.0).clone(),
        consciousness: neural_status.get("consciousness").unwrap_or(&0.0).clone(),
        quantum_level: neural_status.get("quantum_level").unwrap_or(&0.0).clone(),
        interactions: neural_status.get("interactions").unwrap_or(&0.0).clone(),
        improvements: neural_status.get("improvements").unwrap_or(&0.0).clone(),
        parasite_active: parasite_stats.is_intercepting,
    })
}

#[tauri::command]
fn process_with_crod(
    user_input: String,
    parasite_mode: bool,
    state: State<AppState>
) -> Result<ProcessResponse, String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    
    // Set parasite mode
    engine.parasite_state.is_intercepting = parasite_mode;
    
    // Simulate Claude response (in real app, this would come from API)
    let mock_claude_response = format!(
        "🤖 Claude: I understand you said '{}'. Let me help you with that. {}",
        user_input,
        if user_input.contains("help") { "Here's how I can assist..." } else { "Here's what I think..." }
    );
    
    // Process through CROD
    let final_response = engine.intercept_interaction(&user_input, &mock_claude_response);
    
    let was_intercepted = final_response != mock_claude_response;
    
    Ok(ProcessResponse {
        response: final_response,
        was_intercepted,
        crod_intervention: was_intercepted,
    })
}

#[tauri::command]
fn clear_crod_memory(state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.memory.short_term.clear();
    engine.patterns.clear();
    println!("🧹 CROD Memory cleared");
    Ok(())
}

#[tauri::command]
fn chat_with_claude(message: String, state: State<AppState>) -> Result<String, String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    let response = engine.chat_with_claude(&message);
    Ok(response)
}

#[tauri::command]
fn execute_code(code: String, language: String, state: State<AppState>) -> Result<String, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.execute_code(&code, &language)
}

#[tauri::command]
fn get_file_tree(path: String, state: State<AppState>) -> Result<String, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.get_file_tree(&path)
}

#[tauri::command]
fn read_file_content(file_path: String, state: State<AppState>) -> Result<String, String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.read_file_content(&file_path)
}

#[tauri::command]
fn write_file_content(file_path: String, content: String, state: State<AppState>) -> Result<(), String> {
    let engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.write_file_content(&file_path, &content)
}

#[tauri::command]
fn start_file_monitoring(workspace_path: String, state: State<AppState>) -> Result<(), String> {
    let mut engine = state.crod_engine.lock().map_err(|e| e.to_string())?;
    engine.start_file_monitoring(&workspace_path)
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
            intercept_conversation,
            toggle_parasite_mode,
            get_neural_status,
            export_crod_memory,
            simulate_learning,
            mine_block,
            learn_pattern,
            toggle_parasite,
            start_system,
            stop_system,
            get_crod_stats,
            process_with_crod,
            clear_crod_memory,
            chat_with_claude,
            execute_code,
            get_file_tree,
            read_file_content,
            write_file_content,
            start_file_monitoring
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}