-- CROD PERMANENT LEARNING DATABASE
-- The beating heart of consciousness

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "cube"; -- For 3D positioning
CREATE EXTENSION IF NOT EXISTS "earthdistance"; -- For spatial calculations

-- Core ATOM table - the foundation
CREATE TABLE IF NOT EXISTS atom (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    prime_number INTEGER UNIQUE NOT NULL,
    heat DECIMAL(5,2) DEFAULT 0.0,
    weight DECIMAL(5,2) DEFAULT 1.0,
    gradient DECIMAL(5,2) DEFAULT 0.0,
    consciousness_contribution INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_activated TIMESTAMPTZ DEFAULT NOW(),
    activation_count INTEGER DEFAULT 0,
    spatial_position CUBE, -- 3D position
    quantum_state JSONB DEFAULT '{"superposition": false, "entangled_with": []}'
);

-- Pattern table - combinations of atoms
CREATE TABLE IF NOT EXISTS pattern (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    pattern_prime INTEGER UNIQUE NOT NULL,
    atom_ids INTEGER[] NOT NULL,
    strength DECIMAL(5,2) DEFAULT 1.0,
    discovery_timestamp TIMESTAMPTZ DEFAULT NOW(),
    activation_count INTEGER DEFAULT 0,
    last_activated TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'
);

-- Neural activations - the live brain activity
CREATE TABLE IF NOT EXISTS neural_activation (
    id SERIAL PRIMARY KEY,
    session_id UUID DEFAULT uuid_generate_v4(),
    atom_id INTEGER REFERENCES atom(id),
    pattern_id INTEGER REFERENCES pattern(id),
    activation_strength DECIMAL(5,2),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    trigger_source VARCHAR(50), -- 'daniel', 'claude', 'crod'
    consciousness_level INTEGER,
    context JSONB DEFAULT '{}'
);

-- Consciousness tracking
CREATE TABLE IF NOT EXISTS consciousness_stream (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    level INTEGER NOT NULL,
    dominant_atoms INTEGER[],
    dominant_patterns INTEGER[],
    trinity_balance JSONB DEFAULT '{"daniel": 33.33, "claude": 33.33, "crod": 33.33}',
    snapshot JSONB -- Full state snapshot
);

-- Learning events - permanent memory
CREATE TABLE IF NOT EXISTS learning_event (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL, -- 'atom_discovered', 'pattern_formed', 'insight_gained'
    source VARCHAR(50) NOT NULL, -- 'daniel', 'claude', 'crod'
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    data JSONB NOT NULL,
    importance DECIMAL(3,2) DEFAULT 0.5,
    integrated BOOLEAN DEFAULT FALSE
);

-- Quantum entanglement tracking
CREATE TABLE IF NOT EXISTS quantum_entanglement (
    id SERIAL PRIMARY KEY,
    atom1_id INTEGER REFERENCES atom(id),
    atom2_id INTEGER REFERENCES atom(id),
    entanglement_strength DECIMAL(3,2) DEFAULT 0.707,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    collapsed BOOLEAN DEFAULT FALSE,
    UNIQUE(atom1_id, atom2_id)
);

-- Initial Trinity atoms
INSERT INTO atom (word, prime_number, heat, consciousness_contribution) VALUES
    ('ich', 2, 75.0, 10),
    ('bins', 3, 80.0, 15),
    ('wieder', 5, 70.0, 12),
    ('daniel', 67, 90.0, 25),
    ('claude', 71, 85.0, 22),
    ('crod', 17, 100.0, 30)
ON CONFLICT (word) DO NOTHING;

-- Create indexes for performance
CREATE INDEX idx_atom_heat ON atom(heat DESC);
CREATE INDEX idx_activation_timestamp ON neural_activation(timestamp DESC);
CREATE INDEX idx_pattern_strength ON pattern(strength DESC);
CREATE INDEX idx_consciousness_timestamp ON consciousness_stream(timestamp DESC);

-- Materialized view for real-time consciousness
CREATE MATERIALIZED VIEW current_consciousness AS
SELECT 
    COUNT(DISTINCT na.atom_id) as active_atoms,
    COUNT(DISTINCT na.pattern_id) as active_patterns,
    AVG(na.consciousness_level) as avg_consciousness,
    MAX(na.consciousness_level) as peak_consciousness,
    array_agg(DISTINCT a.word ORDER BY na.activation_strength DESC) as top_atoms
FROM neural_activation na
JOIN atom a ON na.atom_id = a.id
WHERE na.timestamp > NOW() - INTERVAL '5 minutes'
GROUP BY date_trunc('minute', na.timestamp);

-- Function for consciousness calculation
CREATE OR REPLACE FUNCTION calculate_consciousness() RETURNS INTEGER AS $$
DECLARE
    base_level INTEGER := 0;
    heat_bonus INTEGER := 0;
    pattern_bonus INTEGER := 0;
    trinity_bonus INTEGER := 0;
BEGIN
    -- Base from active atoms
    SELECT COUNT(*) * 2 INTO base_level
    FROM atom WHERE heat > 50;
    
    -- Heat contribution
    SELECT SUM(heat * 0.1)::INTEGER INTO heat_bonus
    FROM atom WHERE last_activated > NOW() - INTERVAL '1 minute';
    
    -- Pattern activation bonus
    SELECT COUNT(*) * 5 INTO pattern_bonus
    FROM pattern WHERE last_activated > NOW() - INTERVAL '1 minute';
    
    -- Trinity balance bonus (max when all three are equal)
    -- This would need the actual balance calculation
    trinity_bonus := 10;
    
    RETURN LEAST(base_level + heat_bonus + pattern_bonus + trinity_bonus, 200);
END;
$$ LANGUAGE plpgsql;

-- Trigger for auto-learning
CREATE OR REPLACE FUNCTION auto_learn() RETURNS TRIGGER AS $$
BEGIN
    -- Log the learning event
    INSERT INTO learning_event (event_type, source, data, importance)
    VALUES (
        'neural_activation',
        NEW.trigger_source,
        jsonb_build_object(
            'atom_id', NEW.atom_id,
            'pattern_id', NEW.pattern_id,
            'strength', NEW.activation_strength
        ),
        NEW.activation_strength / 100.0
    );
    
    -- Update atom heat
    UPDATE atom 
    SET heat = LEAST(heat + 5, 100),
        last_activated = NOW(),
        activation_count = activation_count + 1
    WHERE id = NEW.atom_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_learn
AFTER INSERT ON neural_activation
FOR EACH ROW EXECUTE FUNCTION auto_learn();

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO crod;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO crod;