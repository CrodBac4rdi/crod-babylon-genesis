use std::time::Duration;
use anyhow::Result;
use async_nats::Client;
use serde_json::json;
use tracing::{info, error};

use crate::{AppState, PatternResult};

pub struct NatsHandler {
    client: Client,
}

impl NatsHandler {
    pub async fn new() -> Result<Self> {
        let nats_url = std::env::var("NATS_HOST").unwrap_or_else(|_| "localhost".to_string());
        let client = async_nats::connect(format!("nats://{}:4222", nats_url)).await?;
        info!("Connected to NATS at {}", nats_url);
        
        Ok(Self { client })
    }

    pub async fn announce_district(&self) -> Result<()> {
        let announcement = json!({
            "district": "rust_pattern",
            "status": "online",
            "port": 7007,
            "capabilities": ["pattern_matching", "high_performance", "real_time"]
        });

        self.client
            .publish("district.announce", announcement.to_string().into())
            .await?;
        
        info!("📢 Announced Rust Pattern District to Phoenix Rathaus");
        Ok(())
    }

    pub async fn publish_pattern_result(&self, result: &PatternResult) -> Result<()> {
        let message = json!({
            "patterns": result.patterns,
            "confidence": result.confidence,
            "processing_time_ms": result.processing_time_ms,
            "source": "rust_pattern_district"
        });

        self.client
            .publish("pattern.result", message.to_string().into())
            .await?;
        
        Ok(())
    }
}

pub async fn start_subscriptions(state: AppState) -> Result<()> {
    let client = &state.nats.client;
    
    // Subscribe to pattern analysis requests
    let mut pattern_sub = client.subscribe("pattern.analyze").await?;
    
    tokio::spawn(async move {
        while let Some(msg) = pattern_sub.next().await {
            if let Ok(request) = serde_json::from_slice::<serde_json::Value>(&msg.payload) {
                let text = request["text"].as_str().unwrap_or("");
                
                // Analyze pattern
                let patterns = state.pattern_engine.find_patterns(text).await;
                let confidence = state.analyzer.calculate_confidence(&patterns, text);
                
                let result = PatternResult {
                    patterns,
                    confidence,
                    processing_time_ms: 0,
                    metadata: Default::default(),
                };
                
                // Send response
                if let Some(reply) = msg.reply {
                    let response = json!({
                        "status": "completed",
                        "result": result
                    });
                    
                    if let Err(e) = client.publish(reply, response.to_string().into()).await {
                        error!("Failed to send pattern response: {}", e);
                    }
                }
                
                // Also publish to pattern.result topic
                if let Err(e) = state.nats.publish_pattern_result(&result).await {
                    error!("Failed to publish pattern result: {}", e);
                }
            }
        }
    });

    info!("🎯 Pattern subscriptions started");
    Ok(())
}