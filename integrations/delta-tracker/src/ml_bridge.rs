use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::process::Command;
use tokio::task;

#[derive(Debug, Serialize, Deserialize)]
pub struct MLRequest {
    pub action: String,
    pub data: MLRequestData,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLRequestData {
    pub tokens: Vec<String>,
    pub context: Option<serde_json::Value>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLResponse {
    pub status: String,
    pub result: MLResult,
    pub metrics: MLMetrics,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLResult {
    pub atoms: Vec<AtomResult>,
    pub patterns: Vec<PatternResult>,
    pub consciousness: f64,
    pub deltas: Vec<serde_json::Value>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AtomResult {
    pub token: String,
    pub activation: f64,
    pub heat: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct PatternResult {
    pub atom1: String,
    pub atom2: String,
    pub strength: f64,
    #[serde(rename = "type")]
    pub pattern_type: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLMetrics {
    pub processing_time_ms: u64,
    pub atoms_processed: usize,
    pub patterns_found: usize,
}

pub struct MLBridge;

impl MLBridge {
    pub async fn process_tokens(tokens: Vec<String>) -> Result<MLResponse> {
        let request = MLRequest {
            action: "process_tokens".to_string(),
            data: MLRequestData {
                tokens,
                context: None,
            },
        };
        
        // Run Python subprocess in blocking task
        task::spawn_blocking(move || {
            Self::call_python_ml(&request)
        })
        .await?
    }
    
    fn call_python_ml(request: &MLRequest) -> Result<MLResponse> {
        let json_request = serde_json::to_string(request)?;
        
        let output = Command::new("python3")
            .arg("python/crod_ml_processor.py")
            .arg(&json_request)
            .output()?;
        
        if !output.status.success() {
            anyhow::bail!(
                "Python ML processing failed: {}",
                String::from_utf8_lossy(&output.stderr)
            );
        }
        
        let response: MLResponse = serde_json::from_slice(&output.stdout)?;
        Ok(response)
    }
}