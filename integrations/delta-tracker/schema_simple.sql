-- CROD Simple Schema - Nur das Wichtigste
-- Deterministisch und schnell

-- Die Basis: Alles hat einen Key
CREATE TABLE IF NOT EXISTS atoms (
    atom_key INTEGER PRIMARY KEY,    -- z.B. 11111
    atom_type TEXT NOT NULL,          -- 'elefant', 'farbe', etc.
    atom_value TEXT NOT NULL,         -- 'grau', 'blau', etc.
    prime_number INTEGER UNIQUE,      -- CROD Prime assignment
    weight REAL DEFAULT 1.0,
    heat REAL DEFAULT 0.0,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

-- Patterns verbinden Atoms
CREATE TABLE IF NOT EXISTS patterns (
    pattern_key INTEGER PRIMARY KEY,   -- atom1_key * atom2_key
    atom1_key INTEGER NOT NULL,
    atom2_key INTEGER NOT NULL,
    occurrences INTEGER DEFAULT 1,
    strength REAL DEFAULT 0.0,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (atom1_key) REFERENCES atoms(atom_key),
    FOREIGN KEY (atom2_key) REFERENCES atoms(atom_key),
    UNIQUE(atom1_key, atom2_key)
);

-- Deltas tracken Änderungen
CREATE TABLE IF NOT EXISTS deltas (
    delta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    source_chain TEXT NOT NULL,
    delta_type TEXT NOT NULL,         -- 'atom_added', 'pattern_emerged', etc.
    delta_data TEXT NOT NULL,         -- JSON
    block_hash TEXT                   -- Für spätere Blockchain
);

-- Version tracking für Rolling Updates
CREATE TABLE IF NOT EXISTS version_info (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_string TEXT NOT NULL,
    deployed_at INTEGER DEFAULT (strftime('%s', 'now')),
    is_active INTEGER DEFAULT 1
);

-- Index für deterministische SELECTs
CREATE INDEX IF NOT EXISTS idx_atom_type_value ON atoms(atom_type, atom_value);
CREATE INDEX IF NOT EXISTS idx_pattern_atoms ON patterns(atom1_key, atom2_key);
CREATE INDEX IF NOT EXISTS idx_delta_timestamp ON deltas(timestamp);

-- Initial Core Atoms (Die Basics)
INSERT OR IGNORE INTO atoms (atom_key, atom_type, atom_value, prime_number) VALUES
(11111, 'elefant', 'grau', 11111),
(11112, 'elefant', 'blau', 11112),
(11113, 'elefant', 'rot', 11113),
(2, 'word', 'ich', 2),
(3, 'word', 'bins', 3),
(5, 'word', 'wieder', 5),
(17, 'system', 'crod', 17),
(67, 'user', 'daniel', 67),
(71, 'system', 'claude', 71);

-- Version Info
INSERT OR IGNORE INTO version_info (version_string) VALUES ('0.1.0');