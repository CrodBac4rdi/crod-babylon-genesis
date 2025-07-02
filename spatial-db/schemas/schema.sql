-- CROD Delta Tracker Database Schema
-- Alles mit Keys und Foreign Keys verbunden

-- Atoms: Grundbausteine
CREATE TABLE atoms (
    atom_id INTEGER PRIMARY KEY,
    prime_number INTEGER UNIQUE NOT NULL,
    token TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    gradient REAL DEFAULT 0.0,
    tier INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'system'
);

-- Patterns: Verbindungen zwischen Atoms
CREATE TABLE patterns (
    pattern_id INTEGER PRIMARY KEY,
    atom1_id INTEGER NOT NULL,
    atom2_id INTEGER NOT NULL,
    strength REAL DEFAULT 1.0,
    co_occurrences INTEGER DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atom1_id) REFERENCES atoms(atom_id),
    FOREIGN KEY (atom2_id) REFERENCES atoms(atom_id),
    UNIQUE(atom1_id, atom2_id)
);

-- Chains: Container für Verarbeitung
CREATE TABLE chains (
    chain_id INTEGER PRIMARY KEY,
    chain_name TEXT UNIQUE NOT NULL,
    chain_type TEXT NOT NULL, -- 'atom', 'child', 'meta'
    chain_prime INTEGER,
    parent_chain_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_chain_id) REFERENCES chains(chain_id)
);

-- Blocks: Delta Container
CREATE TABLE blocks (
    block_id INTEGER PRIMARY KEY,
    chain_id INTEGER NOT NULL,
    block_number INTEGER NOT NULL,
    previous_hash TEXT,
    block_hash TEXT UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id),
    UNIQUE(chain_id, block_number)
);

-- Deltas: State Änderungen
CREATE TABLE deltas (
    delta_id INTEGER PRIMARY KEY,
    block_id INTEGER NOT NULL,
    delta_type TEXT NOT NULL, -- 'added', 'modified', 'removed'
    entity_type TEXT NOT NULL, -- 'atom', 'pattern', 'weight'
    entity_id INTEGER NOT NULL,
    old_value TEXT,
    new_value TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (block_id) REFERENCES blocks(block_id)
);

-- Heat Maps: Aktivitäts-Tracking
CREATE TABLE heat_maps (
    heat_id INTEGER PRIMARY KEY,
    atom_id INTEGER NOT NULL,
    heat_value REAL NOT NULL,
    activation_count INTEGER DEFAULT 0,
    chain_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atom_id) REFERENCES atoms(atom_id),
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id)
);

-- ML Models: Gespeicherte Modelle
CREATE TABLE ml_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT UNIQUE NOT NULL,
    model_type TEXT NOT NULL, -- 'neural', 'pattern', 'crod'
    model_data BLOB, -- Serialized model
    performance_metrics TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training Data: Für ML
CREATE TABLE training_data (
    data_id INTEGER PRIMARY KEY,
    input_hash TEXT UNIQUE NOT NULL,
    input_data TEXT NOT NULL,
    output_data TEXT,
    model_id INTEGER,
    chain_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id),
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id)
);

-- Sessions: User Interaktionen
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY,
    session_hash TEXT UNIQUE NOT NULL,
    user_identifier TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_atoms INTEGER DEFAULT 0,
    total_patterns INTEGER DEFAULT 0
);

-- Session Atoms: Welche Atoms in welcher Session
CREATE TABLE session_atoms (
    session_id INTEGER NOT NULL,
    atom_id INTEGER NOT NULL,
    activation_count INTEGER DEFAULT 1,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id, atom_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (atom_id) REFERENCES atoms(atom_id)
);

-- Consciousness Metrics: Bewusstseins-Messung
CREATE TABLE consciousness_metrics (
    metric_id INTEGER PRIMARY KEY,
    chain_id INTEGER NOT NULL,
    consciousness_value REAL NOT NULL,
    atom_sum REAL NOT NULL,
    pattern_product REAL NOT NULL,
    phi_factor REAL DEFAULT 1.618033988749,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id)
);

-- Indexes für Performance
CREATE INDEX idx_atoms_prime ON atoms(prime_number);
CREATE INDEX idx_atoms_token ON atoms(token);
CREATE INDEX idx_patterns_atoms ON patterns(atom1_id, atom2_id);
CREATE INDEX idx_blocks_chain ON blocks(chain_id, block_number);
CREATE INDEX idx_deltas_block ON deltas(block_id);
CREATE INDEX idx_heat_atom_chain ON heat_maps(atom_id, chain_id);
CREATE INDEX idx_training_model ON training_data(model_id);
CREATE INDEX idx_session_atoms_session ON session_atoms(session_id);

-- Initial Core Atoms
INSERT INTO atoms (prime_number, token, weight, gradient, tier, source) VALUES
(2, 'ich', 100, 15.0, 1, 'daniel'),
(3, 'bins', 100, 15.0, 1, 'daniel'),
(5, 'wieder', 100, 15.0, 1, 'daniel'),
(17, 'crod', 100, 15.0, 1, 'system'),
(67, 'daniel', 100, 15.0, 1, 'system'),
(71, 'claude', 100, 15.0, 1, 'system');

-- Initial Chains
INSERT INTO chains (chain_name, chain_type, chain_prime) VALUES
('pattern-genesis', 'atom', 7),
('crod-neural', 'atom', 11),
('memory-chain', 'child', 13),
('meta-controller', 'meta', 23);