-- Create initial tables if not exists
-- Using the schemas we defined

-- First the basic key database schema
.read ../key_database_schema.sql

-- Then the delta tracking schema  
.read ../schema.sql

-- Add some example data for testing
INSERT OR IGNORE INTO content_types (type_id, type_name, base_attributes) VALUES
(5, 'code_pattern', '{"pattern": "string", "language": "string", "complexity": "number"}'),
(6, 'ml_state', '{"weights": "array", "gradients": "array", "loss": "number"}');

-- More test elephants with different keys
INSERT OR IGNORE INTO dynamic_content (content_id, content_type_id, attributes) VALUES
(4, 1, '{"type": "elephant", "color": "grün", "size": "klein", "has_hat": false}'),
(5, 1, '{"type": "elephant", "color": "gelb", "size": "mittel", "has_hat": true}');

INSERT OR IGNORE INTO master_keys (key_id, key_hash, key_type, content_pointer) VALUES
(4, 'elephant_green_small', 'concept', 4),
(5, 'elephant_yellow_medium_hat', 'concept', 5);

INSERT OR IGNORE INTO key_mappings (numeric_key, master_key_id, description) VALUES
(11114, 4, 'grüner kleiner Elefant'),
(11115, 5, 'gelber mittlerer Elefant mit Hut');

-- Create chain for testing
INSERT OR IGNORE INTO chains (chain_id, chain_name, chain_type, chain_prime) VALUES
(5, 'delta-tracker', 'meta', 31);