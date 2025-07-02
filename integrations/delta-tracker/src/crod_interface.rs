use anyhow::Result;
use serde::{Serialize, Deserialize};
use std::process::Command;

/// Interface zwischen Rust und Python/JS
pub struct CrodInterface;

#[derive(Debug, Serialize, Deserialize)]
pub struct MLRequest {
    pub action: String,
    pub data: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLResponse {
    pub result: serde_json::Value,
    pub metrics: Option<serde_json::Value>,
}

impl CrodInterface {
    /// Call Python ML processing
    pub async fn call_python_ml(request: &MLRequest) -> Result<MLResponse> {
        let json_request = serde_json::to_string(request)?;
        
        let output = Command::new("python")
            .arg("../python/crod_ml_processor.py")
            .arg(&json_request)
            .output()?;
        
        if !output.status.success() {
            anyhow::bail!("Python ML processing failed: {}", 
                         String::from_utf8_lossy(&output.stderr));
        }
        
        let response: MLResponse = serde_json::from_slice(&output.stdout)?;
        Ok(response)
    }
    
    /// Call JavaScript pattern processing
    pub async fn call_js_patterns(data: serde_json::Value) -> Result<serde_json::Value> {
        let json_data = serde_json::to_string(&data)?;
        
        let output = Command::new("node")
            .arg("../js/pattern_processor.js")
            .arg(&json_data)
            .output()?;
        
        if !output.status.success() {
            anyhow::bail!("JS pattern processing failed: {}", 
                         String::from_utf8_lossy(&output.stderr));
        }
        
        let result: serde_json::Value = serde_json::from_slice(&output.stdout)?;
        Ok(result)
    }
}