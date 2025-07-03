-- CROD Document Registry Schema Extension
-- Integrates with Spatial Database for Hash-Document System

-- ============================================
-- DOCUMENT REGISTRY TABLES
-- ============================================

-- Document Registry: Main table for all documents
CREATE TABLE IF NOT EXISTS document_registry (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_hash VARCHAR(64) UNIQUE NOT NULL,
    prime_number NUMERIC(1000) UNIQUE NOT NULL, -- Big integers for primes
    document_type VARCHAR(50) DEFAULT 'generic',
    content_size INTEGER,
    position_id INTEGER, -- Spatial position in 3D grid
    heat DECIMAL(10,4) DEFAULT 0.0,
    atom_weight DECIMAL(10,4) DEFAULT 100.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    current_version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    FOREIGN KEY (position_id) REFERENCES spatial_positions(position_id)
);

-- Document Content Storage (optional, for small docs)
CREATE TABLE IF NOT EXISTS document_content (
    document_id UUID PRIMARY KEY REFERENCES document_registry(document_id),
    content TEXT,
    content_type VARCHAR(50), -- 'text', 'json', 'markdown', etc.
    encoding VARCHAR(20) DEFAULT 'utf-8'
);

-- Delta Storage: Track all changes
CREATE TABLE IF NOT EXISTS document_deltas (
    delta_id SERIAL PRIMARY KEY,
    document_id UUID REFERENCES document_registry(document_id),
    from_hash VARCHAR(64),
    to_hash VARCHAR(64),
    delta_type VARCHAR(20) NOT NULL, -- 'add', 'modify', 'remove'
    delta_content JSONB NOT NULL,
    delta_size INT,
    prime_reference NUMERIC(1000),
    block_hash VARCHAR(64), -- Reference to blockchain
    heat_change DECIMAL(10,4) DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document Patterns: Relationships between documents
CREATE TABLE IF NOT EXISTS document_patterns (
    pattern_id NUMERIC(2000) PRIMARY KEY, -- prime1 * prime2
    document_1 UUID REFERENCES document_registry(document_id),
    document_2 UUID REFERENCES document_registry(document_id),
    pattern_type VARCHAR(50),
    pattern_name VARCHAR(100),
    strength DECIMAL(10,4),
    heat_transfer DECIMAL(10,4) DEFAULT 0.0,
    first_detected TIMESTAMPTZ DEFAULT NOW(),
    last_seen TIMESTAMPTZ DEFAULT NOW(),
    occurrence_count INT DEFAULT 1,
    UNIQUE(document_1, document_2)
);

-- Document Atoms: Link documents to CROD atoms
CREATE TABLE IF NOT EXISTS document_atoms (
    document_id UUID REFERENCES document_registry(document_id),
    atom_id INTEGER REFERENCES atoms(atom_id),
    relevance DECIMAL(10,4) DEFAULT 1.0,
    position_in_doc INTEGER,
    PRIMARY KEY (document_id, atom_id)
);

-- ============================================
-- SPATIAL DOCUMENT VIEWS
-- ============================================

-- View: Documents in 3D space with heat
CREATE VIEW spatial_documents AS
SELECT 
    dr.document_id,
    dr.document_hash,
    dr.prime_number,
    dr.heat,
    sp.x, sp.y, sp.z,
    sp.layer_name,
    ST_MakePoint(sp.x, sp.y, sp.z) as spatial_point
FROM document_registry dr
JOIN spatial_positions sp ON dr.position_id = sp.position_id
WHERE dr.is_active = true;

-- View: Document heat propagation
CREATE VIEW document_heat_propagation AS
SELECT 
    d1.document_id as source_doc,
    d2.document_id as target_doc,
    dp.heat_transfer,
    spatial_distance_between_chains(
        (SELECT chain_id FROM chains WHERE position_id = d1.position_id LIMIT 1),
        (SELECT chain_id FROM chains WHERE position_id = d2.position_id LIMIT 1)
    ) as spatial_distance
FROM document_patterns dp
JOIN document_registry d1 ON dp.document_1 = d1.document_id
JOIN document_registry d2 ON dp.document_2 = d2.document_id
WHERE dp.heat_transfer > 0;

-- ============================================
-- FUNCTIONS FOR DOCUMENT MANAGEMENT
-- ============================================

-- Function: Register new document with automatic prime assignment
CREATE OR REPLACE FUNCTION register_document(
    p_content TEXT,
    p_doc_type VARCHAR(50) DEFAULT 'generic'
) RETURNS UUID AS $$
DECLARE
    v_hash VARCHAR(64);
    v_prime NUMERIC(1000);
    v_doc_id UUID;
    v_position_id INTEGER;
BEGIN
    -- Calculate hash
    v_hash := encode(sha256(p_content::bytea), 'hex');
    
    -- Check if document already exists
    SELECT document_id INTO v_doc_id
    FROM document_registry
    WHERE document_hash = v_hash;
    
    IF v_doc_id IS NOT NULL THEN
        RETURN v_doc_id;
    END IF;
    
    -- Generate prime from hash (simplified version)
    v_prime := hash_to_prime(v_hash);
    
    -- Assign spatial position (find empty spot)
    SELECT position_id INTO v_position_id
    FROM spatial_positions
    WHERE position_id NOT IN (
        SELECT position_id FROM document_registry WHERE position_id IS NOT NULL
    )
    LIMIT 1;
    
    -- Insert document
    INSERT INTO document_registry (
        document_hash, prime_number, document_type, 
        content_size, position_id
    ) VALUES (
        v_hash, v_prime, p_doc_type,
        length(p_content), v_position_id
    ) RETURNING document_id INTO v_doc_id;
    
    -- Store content
    INSERT INTO document_content (document_id, content, content_type)
    VALUES (v_doc_id, p_content, p_doc_type);
    
    RETURN v_doc_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Process document delta
CREATE OR REPLACE FUNCTION process_document_delta(
    p_doc_id UUID,
    p_new_content TEXT,
    p_delta_json JSONB
) RETURNS INTEGER AS $$
DECLARE
    v_old_hash VARCHAR(64);
    v_new_hash VARCHAR(64);
    v_new_prime NUMERIC(1000);
    v_delta_id INTEGER;
    v_heat_increase DECIMAL(10,4);
BEGIN
    -- Get old hash
    SELECT document_hash INTO v_old_hash
    FROM document_registry
    WHERE document_id = p_doc_id;
    
    -- Calculate new hash
    v_new_hash := encode(sha256(p_new_content::bytea), 'hex');
    v_new_prime := hash_to_prime(v_new_hash);
    
    -- Calculate heat increase based on delta size
    v_heat_increase := (p_delta_json->>'additions')::INT / 100.0 + 
                      (p_delta_json->>'deletions')::INT / 200.0;
    
    -- Insert delta record
    INSERT INTO document_deltas (
        document_id, from_hash, to_hash, delta_type,
        delta_content, prime_reference, heat_change
    ) VALUES (
        p_doc_id, v_old_hash, v_new_hash, 'modify',
        p_delta_json, v_new_prime, v_heat_increase
    ) RETURNING delta_id INTO v_delta_id;
    
    -- Update document registry
    UPDATE document_registry
    SET document_hash = v_new_hash,
        prime_number = v_new_prime,
        heat = heat + v_heat_increase,
        updated_at = NOW(),
        current_version = current_version + 1
    WHERE document_id = p_doc_id;
    
    -- Update content
    UPDATE document_content
    SET content = p_new_content
    WHERE document_id = p_doc_id;
    
    RETURN v_delta_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Find document patterns
CREATE OR REPLACE FUNCTION find_document_patterns(
    p_doc_id UUID,
    p_min_strength DECIMAL DEFAULT 0.5
) RETURNS TABLE(
    related_doc_id UUID,
    pattern_strength DECIMAL,
    pattern_type VARCHAR,
    common_atoms TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN dp.document_1 = p_doc_id THEN dp.document_2
            ELSE dp.document_1
        END as related_doc_id,
        dp.strength as pattern_strength,
        dp.pattern_type,
        ARRAY(
            SELECT a.token
            FROM document_atoms da1
            JOIN document_atoms da2 ON da1.atom_id = da2.atom_id
            JOIN atoms a ON da1.atom_id = a.atom_id
            WHERE da1.document_id = p_doc_id
            AND da2.document_id = CASE 
                WHEN dp.document_1 = p_doc_id THEN dp.document_2
                ELSE dp.document_1
            END
        ) as common_atoms
    FROM document_patterns dp
    WHERE (dp.document_1 = p_doc_id OR dp.document_2 = p_doc_id)
    AND dp.strength >= p_min_strength
    ORDER BY dp.strength DESC;
END;
$$ LANGUAGE plpgsql;

-- Helper function: Hash to Prime conversion
CREATE OR REPLACE FUNCTION hash_to_prime(p_hash VARCHAR(64)) 
RETURNS NUMERIC AS $$
DECLARE
    v_num NUMERIC;
    v_hex_part VARCHAR(16);
BEGIN
    -- Take first 16 chars of hash for manageable prime
    v_hex_part := substring(p_hash, 1, 16);
    v_num := ('x' || v_hex_part)::bit(64)::bigint::numeric;
    
    -- Find next prime (simplified - real implementation would be more robust)
    WHILE NOT is_prime(v_num) LOOP
        v_num := v_num + 1;
    END LOOP;
    
    RETURN v_num;
END;
$$ LANGUAGE plpgsql;

-- Helper function: Simple primality test
CREATE OR REPLACE FUNCTION is_prime(n NUMERIC) 
RETURNS BOOLEAN AS $$
DECLARE
    i NUMERIC;
BEGIN
    IF n <= 1 THEN RETURN FALSE; END IF;
    IF n <= 3 THEN RETURN TRUE; END IF;
    IF n % 2 = 0 OR n % 3 = 0 THEN RETURN FALSE; END IF;
    
    i := 5;
    WHILE i * i <= n LOOP
        IF n % i = 0 OR n % (i + 2) = 0 THEN
            RETURN FALSE;
        END IF;
        i := i + 6;
    END LOOP;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_doc_registry_hash ON document_registry(document_hash);
CREATE INDEX idx_doc_registry_prime ON document_registry(prime_number);
CREATE INDEX idx_doc_registry_position ON document_registry(position_id);
CREATE INDEX idx_doc_registry_heat ON document_registry(heat DESC);
CREATE INDEX idx_doc_deltas_doc ON document_deltas(document_id);
CREATE INDEX idx_doc_deltas_timestamp ON document_deltas(created_at DESC);
CREATE INDEX idx_doc_patterns_strength ON document_patterns(strength DESC);
CREATE INDEX idx_doc_atoms_relevance ON document_atoms(relevance DESC);

-- ============================================
-- TRIGGERS FOR AUTOMATION
-- ============================================

-- Trigger: Auto-update timestamps
CREATE OR REPLACE FUNCTION update_document_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER document_registry_update_timestamp
BEFORE UPDATE ON document_registry
FOR EACH ROW
EXECUTE FUNCTION update_document_timestamp();

-- Trigger: Auto-create patterns when documents share atoms
CREATE OR REPLACE FUNCTION check_document_patterns()
RETURNS TRIGGER AS $$
DECLARE
    v_pattern_id NUMERIC;
    v_strength DECIMAL;
    v_common_atoms INTEGER;
BEGIN
    -- Find documents with common atoms
    FOR v_pattern_id, v_common_atoms IN
        SELECT 
            dr2.prime_number * NEW.prime_number,
            COUNT(DISTINCT da2.atom_id)
        FROM document_atoms da1
        JOIN document_atoms da2 ON da1.atom_id = da2.atom_id
        JOIN document_registry dr2 ON da2.document_id = dr2.document_id
        WHERE da1.document_id = NEW.document_id
        AND da2.document_id != NEW.document_id
        GROUP BY dr2.prime_number
        HAVING COUNT(DISTINCT da2.atom_id) > 3
    LOOP
        v_strength := v_common_atoms::DECIMAL / 10.0;
        
        INSERT INTO document_patterns (
            pattern_id, document_1, document_2,
            pattern_type, strength
        ) VALUES (
            v_pattern_id, NEW.document_id, 
            (SELECT document_id FROM document_registry WHERE prime_number = v_pattern_id / NEW.prime_number),
            'atom-overlap', v_strength
        ) ON CONFLICT (document_1, document_2) DO UPDATE
        SET strength = GREATEST(document_patterns.strength, v_strength),
            occurrence_count = document_patterns.occurrence_count + 1,
            last_seen = NOW();
    END LOOP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER document_pattern_detection
AFTER INSERT OR UPDATE ON document_atoms
FOR EACH ROW
EXECUTE FUNCTION check_document_patterns();

-- ============================================
-- INITIAL TEST DATA
-- ============================================

-- Test: Register CROD documentation
SELECT register_document(
    'CROD Hash-Document System: Every document becomes an atom with a unique prime number.',
    'markdown'
);

SELECT register_document(
    'Delta tracking enables efficient storage by only saving changes between versions.',
    'text'
);

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO crod_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO crod_user;