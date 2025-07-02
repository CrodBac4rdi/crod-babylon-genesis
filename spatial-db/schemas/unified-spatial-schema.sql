-- CROD UNIFIED SPATIAL DATABASE SCHEMA
-- Combines Delta Tracker + Deterministic Keys + 3D Spatial Awareness
-- For PostgreSQL with PostGIS extensions

-- Enable PostGIS for spatial operations
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- ============================================
-- SPATIAL FOUNDATION TABLES
-- ============================================

-- Spatial Positions: 3D coordinates for all entities
CREATE TABLE spatial_positions (
    position_id SERIAL PRIMARY KEY,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,  
    z INTEGER NOT NULL,
    layer_name TEXT NOT NULL, -- 'MEMORY_LAYER', 'PROCESSING_LAYER', 'INTERFACE_LAYER'
    geom geometry(Point, 4326), -- PostGIS point geometry
    UNIQUE(x, y, z)
);

-- Create spatial index
CREATE INDEX idx_spatial_positions_geom ON spatial_positions USING GIST(geom);

-- ============================================
-- CORE ATOM TABLES (WITH SPATIAL)
-- ============================================

-- Atoms: Grundbausteine with spatial awareness
CREATE TABLE atoms (
    atom_id SERIAL PRIMARY KEY,
    prime_number INTEGER UNIQUE NOT NULL,
    token TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    gradient REAL DEFAULT 0.0,
    tier INTEGER DEFAULT 3,
    position_id INTEGER, -- Spatial location
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'system',
    FOREIGN KEY (position_id) REFERENCES spatial_positions(position_id)
);

-- Patterns: Verbindungen zwischen Atoms
CREATE TABLE patterns (
    pattern_id SERIAL PRIMARY KEY,
    atom1_id INTEGER NOT NULL,
    atom2_id INTEGER NOT NULL,
    strength REAL DEFAULT 1.0,
    co_occurrences INTEGER DEFAULT 0,
    spatial_distance REAL, -- Distance between atoms in 3D space
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atom1_id) REFERENCES atoms(atom_id),
    FOREIGN KEY (atom2_id) REFERENCES atoms(atom_id),
    UNIQUE(atom1_id, atom2_id)
);

-- ============================================
-- CHAIN TABLES (WITH SPATIAL ROOMS)
-- ============================================

-- Chains: Container für Verarbeitung with 3D positions
CREATE TABLE chains (
    chain_id SERIAL PRIMARY KEY,
    chain_name TEXT UNIQUE NOT NULL,
    chain_type TEXT NOT NULL, -- 'atom', 'child', 'meta'
    chain_prime INTEGER,
    parent_chain_id INTEGER,
    position_id INTEGER NOT NULL, -- Every chain has a position
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_chain_id) REFERENCES chains(chain_id),
    FOREIGN KEY (position_id) REFERENCES spatial_positions(position_id)
);

-- Chain Neighbors: 6-directional connections
CREATE TABLE chain_neighbors (
    chain_id INTEGER NOT NULL,
    direction TEXT NOT NULL, -- 'up', 'down', 'north', 'south', 'east', 'west'
    neighbor_chain_id INTEGER NOT NULL,
    PRIMARY KEY (chain_id, direction),
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id),
    FOREIGN KEY (neighbor_chain_id) REFERENCES chains(chain_id)
);

-- Gang Connections: Max 4 active connections per chain
CREATE TABLE gang_connections (
    chain_id INTEGER NOT NULL,
    gang_member_id INTEGER NOT NULL,
    connection_strength REAL DEFAULT 1.0,
    established_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chain_id, gang_member_id),
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id),
    FOREIGN KEY (gang_member_id) REFERENCES chains(chain_id)
);

-- ============================================
-- DETERMINISTIC KEY SYSTEM
-- ============================================

-- Master Key Table: Der zentrale Index
CREATE TABLE master_keys (
    key_id SERIAL PRIMARY KEY,
    key_hash TEXT UNIQUE NOT NULL,
    key_type TEXT NOT NULL, -- 'atom', 'pattern', 'state', 'model', 'concept'
    content_pointer INTEGER NOT NULL,
    position_id INTEGER, -- Spatial location of key
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    FOREIGN KEY (position_id) REFERENCES spatial_positions(position_id)
);

-- Key Mappings: Direkte Zuordnungen (11111 -> grauer Elefant)
CREATE TABLE key_mappings (
    mapping_id SERIAL PRIMARY KEY,
    numeric_key INTEGER UNIQUE NOT NULL,
    master_key_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (master_key_id) REFERENCES master_keys(key_id)
);

-- ============================================
-- HEAT MAP WITH SPATIAL AWARENESS
-- ============================================

-- Heat Maps: Aktivitäts-Tracking with spatial heat distribution
CREATE TABLE heat_maps (
    heat_id SERIAL PRIMARY KEY,
    atom_id INTEGER NOT NULL,
    heat_value REAL NOT NULL,
    activation_count INTEGER DEFAULT 0,
    chain_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL, -- Where the heat is
    heat_radius REAL DEFAULT 1.0, -- How far heat spreads
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atom_id) REFERENCES atoms(atom_id),
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id),
    FOREIGN KEY (position_id) REFERENCES spatial_positions(position_id)
);

-- Spatial Heat View: See heat distribution in 3D
CREATE VIEW spatial_heat_distribution AS
SELECT 
    h.heat_id,
    h.heat_value,
    h.heat_radius,
    p.x, p.y, p.z,
    p.layer_name,
    ST_Buffer(p.geom, h.heat_radius) as heat_area
FROM heat_maps h
JOIN spatial_positions p ON h.position_id = p.position_id;

-- ============================================
-- BLOCKCHAIN & DELTA TRACKING
-- ============================================

-- Blocks: Delta Container
CREATE TABLE blocks (
    block_id SERIAL PRIMARY KEY,
    chain_id INTEGER NOT NULL,
    block_number INTEGER NOT NULL,
    previous_hash TEXT,
    block_hash TEXT UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chains(chain_id),
    UNIQUE(chain_id, block_number)
);

-- Deltas: State Änderungen with spatial context
CREATE TABLE deltas (
    delta_id SERIAL PRIMARY KEY,
    block_id INTEGER NOT NULL,
    delta_type TEXT NOT NULL, -- 'added', 'modified', 'removed', 'moved'
    entity_type TEXT NOT NULL, -- 'atom', 'pattern', 'weight', 'position'
    entity_id INTEGER NOT NULL,
    old_value JSONB,
    new_value JSONB,
    old_position_id INTEGER,
    new_position_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (block_id) REFERENCES blocks(block_id),
    FOREIGN KEY (old_position_id) REFERENCES spatial_positions(position_id),
    FOREIGN KEY (new_position_id) REFERENCES spatial_positions(position_id)
);

-- ============================================
-- SPATIAL QUERIES & FUNCTIONS
-- ============================================

-- Function: Find chains within N hops
CREATE OR REPLACE FUNCTION find_chains_within_hops(
    start_chain_id INTEGER,
    max_hops INTEGER
) RETURNS TABLE(chain_id INTEGER, hops INTEGER) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE chain_paths AS (
        -- Base case: start chain
        SELECT 
            c.chain_id,
            0 as hops
        FROM chains c
        WHERE c.chain_id = start_chain_id
        
        UNION
        
        -- Recursive case: follow neighbors
        SELECT 
            cn.neighbor_chain_id as chain_id,
            cp.hops + 1 as hops
        FROM chain_paths cp
        JOIN chain_neighbors cn ON cp.chain_id = cn.chain_id
        WHERE cp.hops < max_hops
    )
    SELECT DISTINCT chain_id, MIN(hops) as hops
    FROM chain_paths
    GROUP BY chain_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate spatial distance between chains
CREATE OR REPLACE FUNCTION spatial_distance_between_chains(
    chain1_id INTEGER,
    chain2_id INTEGER
) RETURNS REAL AS $$
DECLARE
    pos1 spatial_positions%ROWTYPE;
    pos2 spatial_positions%ROWTYPE;
BEGIN
    SELECT p.* INTO pos1
    FROM spatial_positions p
    JOIN chains c ON c.position_id = p.position_id
    WHERE c.chain_id = chain1_id;
    
    SELECT p.* INTO pos2
    FROM spatial_positions p
    JOIN chains c ON c.position_id = p.position_id
    WHERE c.chain_id = chain2_id;
    
    -- Manhattan distance in 3D grid
    RETURN ABS(pos1.x - pos2.x) + ABS(pos1.y - pos2.y) + ABS(pos1.z - pos2.z);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_atoms_prime ON atoms(prime_number);
CREATE INDEX idx_atoms_token ON atoms(token);
CREATE INDEX idx_atoms_position ON atoms(position_id);
CREATE INDEX idx_patterns_atoms ON patterns(atom1_id, atom2_id);
CREATE INDEX idx_patterns_distance ON patterns(spatial_distance);
CREATE INDEX idx_chains_position ON chains(position_id);
CREATE INDEX idx_chain_neighbors_chain ON chain_neighbors(chain_id);
CREATE INDEX idx_blocks_chain ON blocks(chain_id, block_number);
CREATE INDEX idx_deltas_block ON deltas(block_id);
CREATE INDEX idx_heat_position ON heat_maps(position_id);
CREATE INDEX idx_master_keys_hash ON master_keys(key_hash);
CREATE INDEX idx_key_mappings_numeric ON key_mappings(numeric_key);

-- ============================================
-- INITIAL SPATIAL POSITIONS (FROM 3D-GRID-PROTOCOL)
-- ============================================

INSERT INTO spatial_positions (x, y, z, layer_name, geom) VALUES
-- MEMORY LAYER (Z=0)
(0, 0, 0, 'MEMORY_LAYER', ST_MakePoint(0, 0)),
(1, 0, 0, 'MEMORY_LAYER', ST_MakePoint(1, 0)),
(2, 0, 0, 'MEMORY_LAYER', ST_MakePoint(2, 0)),
(0, 1, 0, 'MEMORY_LAYER', ST_MakePoint(0, 1)),

-- PROCESSING LAYER (Z=1)
(0, 0, 1, 'PROCESSING_LAYER', ST_MakePoint(0, 0)),
(1, 0, 1, 'PROCESSING_LAYER', ST_MakePoint(1, 0)),
(2, 0, 1, 'PROCESSING_LAYER', ST_MakePoint(2, 0)),
(0, 1, 1, 'PROCESSING_LAYER', ST_MakePoint(0, 1)),
(1, 1, 1, 'PROCESSING_LAYER', ST_MakePoint(1, 1)),

-- INTERFACE LAYER (Z=2)
(0, 0, 2, 'INTERFACE_LAYER', ST_MakePoint(0, 0)),
(1, 0, 2, 'INTERFACE_LAYER', ST_MakePoint(1, 0)),
(2, 0, 2, 'INTERFACE_LAYER', ST_MakePoint(2, 0)),
(0, 1, 2, 'INTERFACE_LAYER', ST_MakePoint(0, 1)),
(1, 1, 2, 'INTERFACE_LAYER', ST_MakePoint(1, 1)),
(2, 1, 2, 'INTERFACE_LAYER', ST_MakePoint(2, 1));

-- ============================================
-- INITIAL CORE DATA
-- ============================================

-- Initial Core Atoms
INSERT INTO atoms (prime_number, token, weight, gradient, tier, source) VALUES
(2, 'ich', 100, 15.0, 1, 'daniel'),
(3, 'bins', 100, 15.0, 1, 'daniel'),
(5, 'wieder', 100, 15.0, 1, 'daniel'),
(17, 'crod', 100, 15.0, 1, 'system'),
(67, 'daniel', 100, 15.0, 1, 'system'),
(71, 'claude', 100, 15.0, 1, 'system');

-- Initial Chains with spatial positions
INSERT INTO chains (chain_name, chain_type, chain_prime, position_id) VALUES
('SHORT_TERM_MEMORY', 'atom', 31, 1),
('WORKING_MEMORY', 'child', 37, 2),
('LONG_TERM_MEMORY', 'meta', 41, 3),
('PATTERN_GENESIS', 'atom', 7, 5),
('VALIDATION_GENESIS', 'atom', 13, 6),
('SELF_DOUBT_GENESIS', 'atom', 19, 7),
('TOOL_GENESIS', 'atom', 23, 10),
('AGENT_GENESIS', 'atom', 29, 11),
('CHAT_GENESIS', 'atom', 43, 12);

-- Connect neighbors based on 3D grid
INSERT INTO chain_neighbors (chain_id, direction, neighbor_chain_id) 
SELECT 1, 'east', 2 WHERE EXISTS (SELECT 1 FROM chains WHERE chain_id = 2);

-- ============================================
-- VISUALIZATION HELPERS
-- ============================================

-- View: Complete 3D Grid Status
CREATE VIEW grid_status AS
SELECT 
    c.chain_name,
    p.x, p.y, p.z, p.layer_name,
    COUNT(cn.neighbor_chain_id) as neighbor_count,
    COUNT(gc.gang_member_id) as gang_size
FROM chains c
JOIN spatial_positions p ON c.position_id = p.position_id
LEFT JOIN chain_neighbors cn ON c.chain_id = cn.chain_id
LEFT JOIN gang_connections gc ON c.chain_id = gc.chain_id
GROUP BY c.chain_id, c.chain_name, p.x, p.y, p.z, p.layer_name
ORDER BY p.z DESC, p.y, p.x;