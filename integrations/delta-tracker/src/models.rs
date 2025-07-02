use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Atom {
    pub atom_key: i64,
    pub atom_type: String,
    pub atom_value: String,
    pub prime_number: i64,
    pub weight: f64,
    pub heat: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Pattern {
    pub pattern_key: i64,
    pub atom1_key: i64,
    pub atom2_key: i64,
    pub occurrences: i32,
    pub strength: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Delta {
    pub source_chain: String,
    pub delta_type: String,
    pub delta_data: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CreateAtomRequest {
    pub atom_type: String,
    pub atom_value: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CreatePatternRequest {
    pub atom1_key: i64,
    pub atom2_key: i64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: &'static str,
    pub version: String,
    pub database: bool,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MLProcessRequest {
    pub tokens: Vec<String>,
}