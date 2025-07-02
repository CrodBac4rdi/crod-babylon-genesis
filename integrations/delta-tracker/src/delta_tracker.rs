use anyhow::Result;
use sqlx::SqlitePool;
use chrono::Utc;
use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Delta {
    pub delta_type: String,
    pub entity_type: String,
    pub entity_id: i64,
    pub old_value: Option<String>,
    pub new_value: Option<String>,
}

pub struct DeltaTracker {
    pool: SqlitePool,
    current_chain_id: i64,
}

impl DeltaTracker {
    pub fn new(pool: SqlitePool) -> Self {
        Self { 
            pool,
            current_chain_id: 1, // Default to pattern-genesis
        }
    }

    /// Track a selection made by CROD
    pub async fn track_selection(
        &self,
        action: &str,
        selected_keys: &[i64],
        context_hash: &str
    ) -> Result<()> {
        let mut tx = self.pool.begin().await?;
        
        // Create a new block for this selection
        let block_hash = self.calculate_block_hash(action, selected_keys, context_hash);
        
        // Get last block number
        let last_block_num: Option<i64> = sqlx::query_scalar(
            "SELECT MAX(block_number) FROM blocks WHERE chain_id = ?"
        )
        .bind(self.current_chain_id)
        .fetch_one(&mut *tx)
        .await?;
        
        let block_number = last_block_num.unwrap_or(0) + 1;
        
        // Insert block
        let block_id: i64 = sqlx::query_scalar(
            r#"INSERT INTO blocks (chain_id, block_number, block_hash, previous_hash) 
               VALUES (?, ?, ?, ?) RETURNING block_id"#
        )
        .bind(self.current_chain_id)
        .bind(block_number)
        .bind(&block_hash)
        .bind("previous_hash_placeholder") // In real implementation, get from last block
        .fetch_one(&mut *tx)
        .await?;
        
        // Create delta for this selection
        let delta = Delta {
            delta_type: "selection".to_string(),
            entity_type: "keys".to_string(),
            entity_id: selected_keys.len() as i64,
            old_value: None,
            new_value: Some(serde_json::to_string(selected_keys)?),
        };
        
        self.insert_delta(&mut tx, block_id, &delta).await?;
        
        // Log CROD decision
        sqlx::query(
            r#"INSERT INTO crod_decisions (input_context, selected_keys, decision_reason) 
               VALUES (?, ?, ?)"#
        )
        .bind(context_hash)
        .bind(serde_json::to_string(selected_keys)?)
        .bind(format!("Action: {}", action))
        .execute(&mut *tx)
        .await?;
        
        // Update heat map for selected keys
        for key in selected_keys {
            self.update_heat_map(&mut tx, *key).await?;
        }
        
        tx.commit().await?;
        Ok(())
    }

    /// Track a state change
    pub async fn track_state_change(
        &self,
        old_state: serde_json::Value,
        new_state: serde_json::Value
    ) -> Result<Vec<Delta>> {
        let deltas = self.calculate_deltas(&old_state, &new_state);
        
        if !deltas.is_empty() {
            let mut tx = self.pool.begin().await?;
            
            // Create block for state change
            let block_hash = self.calculate_state_hash(&new_state);
            let block_id = self.create_block(&mut tx, &block_hash).await?;
            
            // Insert all deltas
            for delta in &deltas {
                self.insert_delta(&mut tx, block_id, delta).await?;
            }
            
            tx.commit().await?;
        }
        
        Ok(deltas)
    }

    /// Calculate deltas between two states
    fn calculate_deltas(&self, old: &serde_json::Value, new: &serde_json::Value) -> Vec<Delta> {
        let mut deltas = Vec::new();
        
        if let (Some(old_obj), Some(new_obj)) = (old.as_object(), new.as_object()) {
            // Find added keys
            for (key, value) in new_obj {
                if !old_obj.contains_key(key) {
                    deltas.push(Delta {
                        delta_type: "added".to_string(),
                        entity_type: "property".to_string(),
                        entity_id: self.hash_to_id(key),
                        old_value: None,
                        new_value: Some(value.to_string()),
                    });
                } else if old_obj.get(key) != Some(value) {
                    // Modified
                    deltas.push(Delta {
                        delta_type: "modified".to_string(),
                        entity_type: "property".to_string(),
                        entity_id: self.hash_to_id(key),
                        old_value: old_obj.get(key).map(|v| v.to_string()),
                        new_value: Some(value.to_string()),
                    });
                }
            }
            
            // Find removed keys
            for (key, value) in old_obj {
                if !new_obj.contains_key(key) {
                    deltas.push(Delta {
                        delta_type: "removed".to_string(),
                        entity_type: "property".to_string(),
                        entity_id: self.hash_to_id(key),
                        old_value: Some(value.to_string()),
                        new_value: None,
                    });
                }
            }
        }
        
        deltas
    }

    async fn insert_delta(
        &self,
        tx: &mut sqlx::Transaction<'_, sqlx::Sqlite>,
        block_id: i64,
        delta: &Delta
    ) -> Result<()> {
        sqlx::query(
            r#"INSERT INTO deltas (block_id, delta_type, entity_type, entity_id, old_value, new_value)
               VALUES (?, ?, ?, ?, ?, ?)"#
        )
        .bind(block_id)
        .bind(&delta.delta_type)
        .bind(&delta.entity_type)
        .bind(delta.entity_id)
        .bind(&delta.old_value)
        .bind(&delta.new_value)
        .execute(&mut **tx)
        .await?;
        
        Ok(())
    }

    async fn create_block(
        &self,
        tx: &mut sqlx::Transaction<'_, sqlx::Sqlite>,
        block_hash: &str
    ) -> Result<i64> {
        let last_block_num: Option<i64> = sqlx::query_scalar(
            "SELECT MAX(block_number) FROM blocks WHERE chain_id = ?"
        )
        .bind(self.current_chain_id)
        .fetch_one(&mut **tx)
        .await?;
        
        let block_number = last_block_num.unwrap_or(0) + 1;
        
        let block_id = sqlx::query_scalar(
            r#"INSERT INTO blocks (chain_id, block_number, block_hash, previous_hash)
               VALUES (?, ?, ?, ?) RETURNING block_id"#
        )
        .bind(self.current_chain_id)
        .bind(block_number)
        .bind(block_hash)
        .bind("previous") // Simplified
        .fetch_one(&mut **tx)
        .await?;
        
        Ok(block_id)
    }

    async fn update_heat_map(
        &self,
        tx: &mut sqlx::Transaction<'_, sqlx::Sqlite>,
        key: i64
    ) -> Result<()> {
        // Check if atom exists for this key
        let atom_id: Option<i64> = sqlx::query_scalar(
            "SELECT atom_id FROM atoms WHERE prime_number = ?"
        )
        .bind(key % 1000) // Simple mapping for demo
        .fetch_optional(&mut **tx)
        .await?;
        
        if let Some(atom_id) = atom_id {
            // Update or insert heat map entry
            sqlx::query(
                r#"INSERT INTO heat_maps (atom_id, heat_value, activation_count, chain_id)
                   VALUES (?, 1.0, 1, ?)
                   ON CONFLICT(atom_id, chain_id) DO UPDATE SET
                   heat_value = heat_value * 0.95 + 1.0,
                   activation_count = activation_count + 1"#
            )
            .bind(atom_id)
            .bind(self.current_chain_id)
            .execute(&mut **tx)
            .await?;
        }
        
        Ok(())
    }

    fn calculate_block_hash(&self, action: &str, keys: &[i64], context: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(action.as_bytes());
        hasher.update(context.as_bytes());
        for key in keys {
            hasher.update(key.to_string().as_bytes());
        }
        hasher.update(Utc::now().timestamp().to_string().as_bytes());
        hex::encode(hasher.finalize())
    }

    fn calculate_state_hash(&self, state: &serde_json::Value) -> String {
        let mut hasher = Sha256::new();
        hasher.update(state.to_string().as_bytes());
        hasher.update(Utc::now().timestamp().to_string().as_bytes());
        hex::encode(hasher.finalize())
    }

    fn hash_to_id(&self, key: &str) -> i64 {
        let mut hasher = Sha256::new();
        hasher.update(key.as_bytes());
        let hash = hasher.finalize();
        let mut id = 0i64;
        for (i, byte) in hash.iter().take(8).enumerate() {
            id |= (*byte as i64) << (i * 8);
        }
        id.abs()
    }
}