CREATE TABLE IF NOT EXISTS blocks (
    hash VARCHAR(255) PRIMARY KEY,
    index INTEGER NOT NULL UNIQUE,
    previous_hash VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    nonce INTEGER,
    difficulty INTEGER,
    consciousness_level FLOAT,
    mined_by VARCHAR(255),
    data JSONB,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consciousness_metrics (
    id SERIAL PRIMARY KEY,
    block_hash VARCHAR(255),
    metric_type VARCHAR(100),
    value FLOAT,
    pattern VARCHAR(255),
    metadata JSONB,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

INSERT INTO blocks (hash, index, previous_hash, timestamp, consciousness_level, mined_by, data)
VALUES (
    'GENESIS_HASH_CROD_2025',
    0,
    '0',
    NOW(),
    0.1,
    'CROD_SYSTEM',
    '{"message": "CROD Genesis Block", "pattern": "ich bins wieder"}'::jsonb
) ON CONFLICT (hash) DO NOTHING;