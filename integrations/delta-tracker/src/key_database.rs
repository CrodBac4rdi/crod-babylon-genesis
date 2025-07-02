use anyhow::Result;
use serde_json::Value as JsonValue;
use sqlx::{SqlitePool, Row};
use std::collections::HashMap;

pub struct KeyDatabase {
    pool: SqlitePool,
}

impl KeyDatabase {
    pub fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }

    /// Select keys based on context hash - CROD's deterministic selection
    pub async fn select_keys_for_context(&self, context_hash: &str) -> Result<Vec<i64>> {
        // Deterministic selection based on context
        // For now, simple modulo-based selection
        let hash_value = context_hash.chars()
            .take(8)
            .map(|c| c as i64)
            .sum::<i64>();
        
        // Select keys based on hash patterns
        let query = r#"
            SELECT numeric_key 
            FROM key_mappings 
            WHERE numeric_key % ? = ?
            LIMIT 10
        "#;
        
        let modulo = 100;
        let remainder = hash_value % modulo;
        
        let keys: Vec<i64> = sqlx::query_scalar(query)
            .bind(modulo)
            .bind(remainder)
            .fetch_all(&self.pool)
            .await?;
        
        Ok(keys)
    }

    /// Get content for selected keys
    pub async fn get_content_for_keys(&self, keys: &[i64]) -> Result<JsonValue> {
        if keys.is_empty() {
            return Ok(JsonValue::Object(serde_json::Map::new()));
        }

        let placeholders = keys.iter()
            .map(|_| "?")
            .collect::<Vec<_>>()
            .join(",");
        
        let query = format!(r#"
            SELECT 
                km.numeric_key,
                km.description,
                dc.attributes
            FROM key_mappings km
            JOIN master_keys mk ON km.master_key_id = mk.key_id
            JOIN dynamic_content dc ON mk.content_pointer = dc.content_id
            WHERE km.numeric_key IN ({})
        "#, placeholders);
        
        let mut query_builder = sqlx::query(&query);
        for key in keys {
            query_builder = query_builder.bind(key);
        }
        
        let rows = query_builder.fetch_all(&self.pool).await?;
        
        let mut result = serde_json::Map::new();
        for row in rows {
            let key: i64 = row.get("numeric_key");
            let description: String = row.get("description");
            let attributes: String = row.get("attributes");
            
            result.insert(
                key.to_string(),
                serde_json::json!({
                    "description": description,
                    "attributes": serde_json::from_str::<JsonValue>(&attributes)?
                })
            );
        }
        
        Ok(JsonValue::Object(result))
    }

    /// Insert new keyed content
    pub async fn insert_keyed_content(
        &self,
        numeric_key: i64,
        content_type: &str,
        attributes: JsonValue
    ) -> Result<()> {
        let mut tx = self.pool.begin().await?;
        
        // Get content type id
        let type_id: i32 = sqlx::query_scalar(
            "SELECT type_id FROM content_types WHERE type_name = ?"
        )
        .bind(content_type)
        .fetch_one(&mut *tx)
        .await?;
        
        // Insert dynamic content
        let content_id: i64 = sqlx::query_scalar(
            "INSERT INTO dynamic_content (content_type_id, attributes) VALUES (?, ?) RETURNING content_id"
        )
        .bind(type_id)
        .bind(attributes.to_string())
        .fetch_one(&mut *tx)
        .await?;
        
        // Create master key
        let key_hash = format!("{}_{}", content_type, numeric_key);
        let master_key_id: i64 = sqlx::query_scalar(
            "INSERT INTO master_keys (key_hash, key_type, content_pointer) VALUES (?, ?, ?) RETURNING key_id"
        )
        .bind(&key_hash)
        .bind("concept")
        .bind(content_id)
        .fetch_one(&mut *tx)
        .await?;
        
        // Create key mapping
        let description = format!("{} {}", 
            attributes.get("color").and_then(|v| v.as_str()).unwrap_or("unknown"),
            content_type
        );
        
        sqlx::query(
            "INSERT INTO key_mappings (numeric_key, master_key_id, description) VALUES (?, ?, ?)"
        )
        .bind(numeric_key)
        .bind(master_key_id)
        .bind(description)
        .execute(&mut *tx)
        .await?;
        
        tx.commit().await?;
        Ok(())
    }

    /// Get content by numeric key
    pub async fn get_content_by_key(&self, numeric_key: i64) -> Result<JsonValue> {
        let row = sqlx::query(r#"
            SELECT 
                km.description,
                dc.attributes,
                ct.type_name
            FROM key_mappings km
            JOIN master_keys mk ON km.master_key_id = mk.key_id
            JOIN dynamic_content dc ON mk.content_pointer = dc.content_id
            JOIN content_types ct ON dc.content_type_id = ct.type_id
            WHERE km.numeric_key = ?
        "#)
        .bind(numeric_key)
        .fetch_optional(&self.pool)
        .await?;
        
        match row {
            Some(row) => {
                let description: String = row.get("description");
                let attributes: String = row.get("attributes");
                let type_name: String = row.get("type_name");
                
                Ok(serde_json::json!({
                    "key": numeric_key,
                    "type": type_name,
                    "description": description,
                    "attributes": serde_json::from_str::<JsonValue>(&attributes)?
                }))
            }
            None => Ok(serde_json::json!({"error": "Key not found"}))
        }
    }

    /// Execute deterministic select
    pub async fn execute_deterministic_select(
        &self,
        select_name: &str,
        params: Vec<String>
    ) -> Result<Vec<JsonValue>> {
        let select_info = sqlx::query(
            "SELECT select_pattern FROM deterministic_selects WHERE select_name = ?"
        )
        .bind(select_name)
        .fetch_one(&self.pool)
        .await?;
        
        let pattern: String = select_info.get("select_pattern");
        
        // Build query with parameters
        let mut query = sqlx::query(&pattern);
        for param in params {
            query = query.bind(param);
        }
        
        let rows = query.fetch_all(&self.pool).await?;
        
        let results: Vec<JsonValue> = rows.iter()
            .map(|row| {
                // Extract all columns dynamically
                let mut obj = serde_json::Map::new();
                for (i, column) in row.columns().iter().enumerate() {
                    let name = column.name();
                    // Try different types
                    if let Ok(val) = row.try_get::<i64, _>(i) {
                        obj.insert(name.to_string(), JsonValue::Number(val.into()));
                    } else if let Ok(val) = row.try_get::<String, _>(i) {
                        obj.insert(name.to_string(), JsonValue::String(val));
                    } else if let Ok(val) = row.try_get::<bool, _>(i) {
                        obj.insert(name.to_string(), JsonValue::Bool(val));
                    }
                }
                JsonValue::Object(obj)
            })
            .collect();
        
        Ok(results)
    }
}