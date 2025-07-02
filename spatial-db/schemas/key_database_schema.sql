-- CROD Deterministic Key Database
-- Jeder Key zeigt auf exakt einen Inhalt, aber der Inhalt kann variabel sein

-- Master Key Table: Der zentrale Index
CREATE TABLE master_keys (
    key_id INTEGER PRIMARY KEY,
    key_hash TEXT UNIQUE NOT NULL, -- Deterministischer Hash
    key_type TEXT NOT NULL, -- 'atom', 'pattern', 'state', 'model', 'concept'
    content_pointer INTEGER NOT NULL, -- Zeigt auf spezifische Tabelle
    metadata TEXT, -- JSON für flexible Eigenschaften
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP
);

-- Content Types: Was für Content-Arten gibt es
CREATE TABLE content_types (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT UNIQUE NOT NULL, -- 'elephant', 'color', 'emotion', 'code'
    base_attributes TEXT NOT NULL -- JSON Schema für diesen Typ
);

-- Dynamic Content: Der eigentliche variable Inhalt
CREATE TABLE dynamic_content (
    content_id INTEGER PRIMARY KEY,
    content_type_id INTEGER NOT NULL,
    attributes TEXT NOT NULL, -- JSON mit allen Eigenschaften
    version INTEGER DEFAULT 1,
    FOREIGN KEY (content_type_id) REFERENCES content_types(type_id)
);

-- Key Mappings: Direkte Zuordnungen
CREATE TABLE key_mappings (
    mapping_id INTEGER PRIMARY KEY,
    numeric_key INTEGER UNIQUE NOT NULL, -- z.B. 11111, 11112
    master_key_id INTEGER NOT NULL,
    description TEXT, -- "grauer Elefant", "blauer Elefant"
    FOREIGN KEY (master_key_id) REFERENCES master_keys(key_id)
);

-- Beispiel Elefanten-System:
-- 11111 -> grauer Elefant
-- 11112 -> blauer Elefant  
-- 11113 -> roter Elefant
-- 11121 -> grauer Elefant mit Hut
-- 11122 -> blauer Elefant mit Hut

-- Property Tables für strukturierte Eigenschaften
CREATE TABLE properties (
    property_id INTEGER PRIMARY KEY,
    property_name TEXT UNIQUE NOT NULL, -- 'color', 'size', 'mood'
    property_type TEXT NOT NULL, -- 'string', 'number', 'boolean'
    allowed_values TEXT -- JSON Array mit erlaubten Werten
);

-- Key Properties: Eigenschaften pro Key
CREATE TABLE key_properties (
    key_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    property_value TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    PRIMARY KEY (key_id, property_id),
    FOREIGN KEY (key_id) REFERENCES master_keys(key_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

-- Deterministic Selects: Vordefinierte Abfragen
CREATE TABLE deterministic_selects (
    select_id INTEGER PRIMARY KEY,
    select_name TEXT UNIQUE NOT NULL,
    select_pattern TEXT NOT NULL, -- SQL Template
    parameters TEXT, -- JSON mit Parametern
    expected_keys TEXT -- JSON Array mit erwarteten Keys
);

-- Key Relations: Beziehungen zwischen Keys
CREATE TABLE key_relations (
    relation_id INTEGER PRIMARY KEY,
    key1_id INTEGER NOT NULL,
    key2_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL, -- 'similar', 'opposite', 'parent', 'child'
    strength REAL DEFAULT 1.0,
    FOREIGN KEY (key1_id) REFERENCES master_keys(key_id),
    FOREIGN KEY (key2_id) REFERENCES master_keys(key_id)
);

-- CROD Decision Log: Was CROD entschieden hat
CREATE TABLE crod_decisions (
    decision_id INTEGER PRIMARY KEY,
    input_context TEXT NOT NULL,
    selected_keys TEXT NOT NULL, -- JSON Array
    decision_reason TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success_score REAL
);

-- Views für häufige Abfragen
CREATE VIEW elephant_view AS
SELECT 
    km.numeric_key,
    km.description,
    json_extract(dc.attributes, '$.color') as color,
    json_extract(dc.attributes, '$.has_hat') as has_hat
FROM key_mappings km
JOIN master_keys mk ON km.master_key_id = mk.key_id
JOIN dynamic_content dc ON mk.content_pointer = dc.content_id
WHERE mk.key_type = 'concept' 
AND json_extract(dc.attributes, '$.type') = 'elephant';

-- Indexes für deterministische Performance
CREATE INDEX idx_key_mappings_numeric ON key_mappings(numeric_key);
CREATE INDEX idx_master_keys_hash ON master_keys(key_hash);
CREATE INDEX idx_master_keys_type ON master_keys(key_type);
CREATE INDEX idx_key_properties_key ON key_properties(key_id);
CREATE INDEX idx_key_relations_keys ON key_relations(key1_id, key2_id);

-- Initial Content Types
INSERT INTO content_types (type_name, base_attributes) VALUES
('elephant', '{"type": "elephant", "color": "string", "size": "string", "has_hat": "boolean"}'),
('color', '{"hex": "string", "rgb": "array", "name": "string"}'),
('pattern', '{"atoms": "array", "strength": "number", "type": "string"}'),
('state', '{"chain_id": "number", "values": "object", "timestamp": "string"}');

-- Initial Properties
INSERT INTO properties (property_name, property_type, allowed_values) VALUES
('color', 'string', '["grau", "blau", "rot", "grün", "gelb"]'),
('size', 'string', '["klein", "mittel", "groß"]'),
('has_hat', 'boolean', '[true, false]'),
('mood', 'string', '["happy", "sad", "neutral", "excited"]');

-- Beispiel Elefanten einfügen
INSERT INTO dynamic_content (content_type_id, attributes) VALUES
(1, '{"type": "elephant", "color": "grau", "size": "groß", "has_hat": false}'),
(1, '{"type": "elephant", "color": "blau", "size": "groß", "has_hat": false}'),
(1, '{"type": "elephant", "color": "rot", "size": "klein", "has_hat": true}');

INSERT INTO master_keys (key_hash, key_type, content_pointer) VALUES
('elephant_grey_large', 'concept', 1),
('elephant_blue_large', 'concept', 2),
('elephant_red_small_hat', 'concept', 3);

INSERT INTO key_mappings (numeric_key, master_key_id, description) VALUES
(11111, 1, 'grauer Elefant'),
(11112, 2, 'blauer Elefant'),
(11113, 3, 'roter Elefant mit Hut');

-- Deterministische Select Templates
INSERT INTO deterministic_selects (select_name, select_pattern, parameters) VALUES
('get_elephants_by_color', 
 'SELECT numeric_key, description FROM elephant_view WHERE color = ?', 
 '{"color": "string"}'),
('get_all_with_hat', 
 'SELECT numeric_key, description FROM elephant_view WHERE has_hat = 1', 
 '{}'),
('get_key_range',
 'SELECT * FROM key_mappings WHERE numeric_key BETWEEN ? AND ?',
 '{"start": "number", "end": "number"}');