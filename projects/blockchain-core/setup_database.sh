#!/bin/bash

echo "🗄️  Setting up CROD Blockchain Database"
echo "====================================="
echo ""

# Check if PostgreSQL container is running
if ! docker ps | grep -q crod-postgres; then
    echo "🚀 Starting PostgreSQL container..."
    docker run -d \
        --name crod-postgres \
        -e POSTGRES_USER=crod \
        -e POSTGRES_PASSWORD=crod2025 \
        -e POSTGRES_DB=crod_blockchain \
        -p 5432:5432 \
        postgres:15-alpine
    
    echo "⏳ Waiting for PostgreSQL to start..."
    sleep 10
else
    echo "✅ PostgreSQL container already running"
fi

# Create database if not exists
echo "📊 Creating database..."
docker exec crod-postgres psql -U crod -c "CREATE DATABASE crod_blockchain;" 2>/dev/null || echo "Database already exists"

# Create tables using SQL
echo "📋 Creating tables..."
docker exec crod-postgres psql -U crod -d crod_blockchain << 'EOF'
-- Blocks table
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

CREATE INDEX IF NOT EXISTS idx_blocks_mined_by ON blocks(mined_by);
CREATE INDEX IF NOT EXISTS idx_blocks_consciousness ON blocks(consciousness_level);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    amount DECIMAL,
    data JSONB,
    signature TEXT,
    consciousness_impact FLOAT,
    block_hash VARCHAR(255) REFERENCES blocks(hash),
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_from ON transactions(from_address);
CREATE INDEX IF NOT EXISTS idx_transactions_to ON transactions(to_address);
CREATE INDEX IF NOT EXISTS idx_transactions_block ON transactions(block_hash);

-- Consciousness metrics table
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

CREATE INDEX IF NOT EXISTS idx_metrics_block ON consciousness_metrics(block_hash);
CREATE INDEX IF NOT EXISTS idx_metrics_type ON consciousness_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_metrics_time ON consciousness_metrics(inserted_at);

-- Insert genesis block
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

EOF

echo ""
echo "✅ Database setup complete!"
echo ""
echo "📊 Database Info:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: crod_blockchain"
echo "  User: crod"
echo "  Password: crod2025"
echo ""
echo "🔗 Connection string:"
echo "  postgresql://crod:crod2025@localhost:5432/crod_blockchain"