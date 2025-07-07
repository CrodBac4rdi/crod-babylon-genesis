# CROD Migration Guide: From Chaos to Clean Architecture

## Overview

This guide explains the migration from the previous scattered implementation to the new clean Phoenix/Elixir orchestrator architecture.

## What Changed

### ❌ Removed
- **Blockchain Implementation** → Replaced with PostgreSQL Event Sourcing
- **Shell Scripts** → Replaced with proper Elixir/Go programs
- **Redundant Files** → Consolidated into single source of truth
- **Multiple Web Interfaces** → Unified Phoenix LiveView
- **Redis** → Replaced with NATS (10x faster)

### ✅ Added
- **Phoenix Orchestrator** → Central control system
- **CROD Parasite** → Human-LLM interpreter as core feature
- **Polygon City Architecture** → District-based service organization
- **Event Sourcing** → Immutable history without blockchain overhead
- **NATS Messaging** → High-performance pub/sub system

## Migration Steps

### 1. Backup Existing Data
```bash
# Backup any important configuration or data
cp -r /old/crod/data /backup/location
```

### 2. Install New System
```bash
cd crod-phoenix
mix deps.get
mix ecto.setup
```

### 3. Migrate Neural Network Configuration
The neural network files are preserved:
- `crod-master.json` → `crod-phoenix/priv/neural/crod-master.json`
- `crod-neural-network.js` → `crod-phoenix/priv/neural/crod-neural-network.js`

### 4. Update Environment Variables
```bash
# Old
export REDIS_URL=redis://localhost:6379
export BLOCKCHAIN_NODE=http://localhost:8545

# New
export NATS_URL=nats://localhost:4222
export DATABASE_URL=postgresql://localhost/crod_dev
```

### 5. API Endpoint Changes

| Old Endpoint | New Endpoint | Notes |
|-------------|--------------|-------|
| `/blockchain/mine` | N/A | Removed - use event sourcing |
| `/api/process` | `/api/parasite/interpret` | Enhanced with context |
| `/redis/pub` | NATS pub/sub | Via NATS client |
| Multiple UIs | `/` | Unified Phoenix LiveView |

## Key Architectural Changes

### From Blockchain to Event Sourcing
```elixir
# Old: Blockchain transaction
Block.create_transaction(from, to, amount)
Blockchain.mine_block()

# New: Event sourcing
%TransferRequested{from: from, to: to, amount: amount}
|> EventStore.append_to_stream()
```

### From Scripts to Services
```bash
# Old: Shell script chaos
./scripts/start-crod.sh
./scripts/crod-launcher.sh

# New: Supervised Elixir services
mix phx.server  # Starts everything
```

### From Redis to NATS
```elixir
# Old: Redis pub/sub
Redis.publish("channel", message)

# New: NATS messaging
NATS.publish("district.orchestrator", message)
```

## Data Migration

### PostgreSQL Setup
```sql
-- Create event store
CREATE DATABASE crod_eventstore;

-- Create read models
CREATE DATABASE crod_dev;
```

### Import Historical Data
```elixir
# Convert old data to events
OldData.all()
|> Enum.map(&DataMigrator.to_event/1)
|> EventStore.append_to_stream("migration-#{Date.utc_today}")
```

## Deprecated Features

### No Longer Supported
- Direct blockchain mining
- Shell script automation
- Multiple separate UIs
- Redis-based messaging

### Replaced With
- Event sourcing with PostgreSQL
- Elixir GenServer supervision
- Unified Phoenix LiveView
- NATS high-performance messaging

## Troubleshooting

### Common Issues

1. **NATS Connection Failed**
   ```bash
   # Ensure NATS is running
   nats-server -DV
   ```

2. **Database Migration Errors**
   ```bash
   # Reset and recreate
   mix ecto.drop
   mix ecto.create
   mix ecto.migrate
   ```

3. **Neural Network Not Loading**
   ```bash
   # Check file permissions
   chmod 644 priv/neural/*.json
   chmod 644 priv/neural/*.js
   ```

## Benefits of New Architecture

### Performance
- 10x faster messaging with NATS
- Efficient event sourcing vs blockchain
- Optimized Elixir processes

### Maintainability
- Single source of truth
- Clear district boundaries
- Supervised fault tolerance

### Scalability
- Horizontal scaling via districts
- Event sourcing for read replicas
- NATS clustering support

## Support

For migration assistance:
1. Check the [README.md](README.md) for setup instructions
2. Review example code in `crod-phoenix/lib/`
3. Open an issue on GitHub for specific problems

## Timeline

- **Phase 1** (Complete): Core Phoenix structure
- **Phase 2** (Current): CROD Parasite implementation
- **Phase 3** (Next): n8n workflow integration
- **Phase 4** (Future): Advanced neural features

---

Remember: This migration simplifies the system while preserving all essential functionality. The new architecture is cleaner, faster, and more maintainable.