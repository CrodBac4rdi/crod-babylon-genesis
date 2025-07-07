use async_nats::{Client, Subscriber};
use serde_json;
use std::sync::Arc;
use tracing::{info, error};

use crate::pattern_engine::{PatternEngine, MatchResult};

pub struct NatsClient {
    client: Client,
}

impl NatsClient {
    pub async fn new(url: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let client = async_nats::connect(url).await?;
        info!("Connected to NATS at {}", url);
        
        Ok(Self { client })
    }
    
    pub async fn is_connected(&self) -> bool {
        // Check connection status
        true // Simplified for now
    }
    
    pub async fn subscribe_patterns(&self, engine: Arc<PatternEngine>) {
        let mut subscriber = self.client
            .subscribe("crod.patterns.>")
            .await
            .expect("Failed to subscribe to pattern topics");
            
        info!("Subscribed to crod.patterns.*");
        
        while let Some(msg) = subscriber.next().await {
            match msg.subject.as_str() {
                "crod.patterns.match" => {
                    if let Ok(request) = serde_json::from_slice::<serde_json::Value>(&msg.data) {
                        if let Some(text) = request.get("text").and_then(|v| v.as_str()) {
                            let matches = engine.match_text(text, None).await;
                            
                            // Send response
                            if let Some(reply) = msg.reply {
                                let response = serde_json::to_vec(&matches).unwrap_or_default();
                                let _ = self.client.publish(reply, response.into()).await;
                            }
                        }
                    }
                }
                "crod.patterns.add" => {
                    // Handle pattern addition
                    info!("Received pattern add request");
                }
                _ => {}
            }
        }
    }
    
    pub async fn publish_matches(&self, matches: &[MatchResult]) -> Result<(), Box<dyn std::error::Error>> {
        let data = serde_json::to_vec(matches)?;
        
        self.client
            .publish("crod.patterns.matches", data.into())
            .await?;
            
        Ok(())
    }
}