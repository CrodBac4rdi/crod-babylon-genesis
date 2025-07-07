# CROD BABYLON GENESIS - Complete Service Map

## Service Port Assignments

### Core Services (Currently Configured)

| Service | Port | Status | Language | Description | Dependencies |
|---------|------|--------|----------|-------------|--------------|
| **Mock Blockchain API** | 3001 | Not Running | Node.js | Express API with WebSocket support | SQLite3, Express, WS |
| **CROD Visualizer** | 8888 | Not Running | Go | System dashboard and metrics visualization | None |
| **Blockchain Explorer** | 8889 | Not Running | Go | Block explorer UI with WebSocket updates | Mock Blockchain API |
| **CROD Monitor** | Terminal | Not Running | Go | Health monitoring console | All services |
| **CROD Chain App** | Dev Mode | Not Running | Tauri/React | Desktop application interface | All backend services |

### Polyglot District Services (Planned/Config)

| Service | Port | Status | Language | Description | Dependencies |
|---------|------|--------|----------|-------------|--------------|
| **Meta-Chain** | 8000 | Not Configured | Elixir | Blockchain core with API server | PostgreSQL, NATS |
| **Pattern Genesis** | 7007 | Not Configured | Rust | Pattern detection engine | Redis/NATS |
| **Short Memory** | 7031 | Not Configured | Go | Short-term memory storage | Redis |
| **Working Memory** | 7037 | Not Configured | Unknown | Working memory processing | Redis |
| **Quantum Node** | 7101 | Not Configured | Unknown | Quantum processing | None |
| **Orchestrator** | 7127 | Not Configured | Unknown | Service orchestration | All services |
| **Time Travel** | 7179 | Not Configured | Unknown | Time-series analysis | PostgreSQL |
| **Intelligence Hub** | 7113 | Not Configured | Python | AI/ML processing hub | Ollama API |
| **CROD Core** | 8100 | Not Configured | Unknown | Core system controller | All services |
| **Gateway** | 8888 | Conflict! | Unknown | API Gateway (conflicts with Visualizer) | All services |

### External Dependencies

| Service | Port | Status | Type | Purpose |
|---------|------|--------|------|---------|
| **PostgreSQL** | 5432 | Not Running | Database | Blockchain & time-series data |
| **Redis** | 6379 | Not Running | Cache/PubSub | Memory storage & messaging |
| **NATS JetStream** | 4222 | Not Running | Message Broker | High-performance messaging (5x Redis) |
| **Ollama** | 11434 | Not Running | AI Service | Local LLM API |

### Additional Services (From Code Analysis)

| Service | Port | Status | Language | Description |
|---------|------|--------|----------|-------------|
| **Elixir API Server** | 4000 | Not Running | Elixir | Blockchain REST API |
| **Pattern Engine** | 4322 | Not Running | Rust | Pattern detection |
| **AI Hub** | 5001 | Not Running | Python | AI processing |
| **Memory Quarter** | 4323 | Not Running | Go | Memory management |

## Service Dependencies Map

```
┌─────────────────────────────────────────────────────────┐
│                     CROD Chain App                      │
│                    (Tauri Desktop)                      │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│                   Frontend Services                      │
├─────────────────────────────────────────────────────────┤
│ • CROD Visualizer (8888)                                │
│ • Blockchain Explorer (8889)                            │
│ • CROD Monitor (Terminal)                               │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│                   Backend Services                       │
├─────────────────────────────────────────────────────────┤
│ • Mock Blockchain API (3001) ─── SQLite3                │
│ • Elixir Blockchain API (4000) ─┬─ PostgreSQL (5432)   │
│                                 └─ NATS (4222)          │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│               Polyglot Districts                         │
├─────────────────────────────────────────────────────────┤
│ • Pattern Genesis (7007) ──────── Redis/NATS           │
│ • Memory Services (7031, 7037) ── Redis (6379)         │
│ • Quantum Node (7101)                                   │
│ • Orchestrator (7127) ─────────── All Services         │
│ • Intelligence Hub (7113) ─────── Ollama (11434)       │
└─────────────────────────────────────────────────────────┘
```

## Current Status Summary

### Running Services
- **None** - No CROD services are currently running

### Port Conflicts Detected
- Port 8888 is assigned to both CROD Visualizer and Gateway service

### Database Status
- SQLite3: Configured for Mock Blockchain API
- PostgreSQL: Not running (required for Elixir blockchain)
- Redis: Not running (required for memory services)
- NATS: Not running (required for message broker)

### Required Actions to Start System

1. **Install External Dependencies:**
   ```bash
   # PostgreSQL
   sudo apt-get install postgresql
   
   # Redis
   sudo apt-get install redis-server
   
   # NATS (via Docker or binary)
   docker run -p 4222:4222 nats:latest -js
   ```

2. **Start Core Services:**
   ```bash
   # From project root
   ./src/cmd/launch-crod-system.sh
   ```

3. **Configure Environment:**
   - Copy `.env.example` to `.env`
   - Set required API keys and secrets
   - Update database connection strings

4. **Resolve Port Conflicts:**
   - Change Gateway port from 8888 to 8889 or another port
   - Update configuration files accordingly

## Service Health Checks

### HTTP Health Endpoints
- Mock Blockchain API: `http://localhost:3001/api/blockchain/status`
- CROD Visualizer: `http://localhost:8888/api/status`
- Blockchain Explorer: `http://localhost:8889/api/blocks`
- Elixir API: `http://localhost:4000/api/blockchain/status`

### WebSocket Endpoints
- Mock Blockchain: `ws://localhost:3001`
- Visualizer: `ws://localhost:8888/ws`
- Explorer: `ws://localhost:8889/ws`

## Network Communication Patterns

1. **REST APIs**: Most services expose REST endpoints
2. **WebSockets**: Real-time updates for UI services
3. **NATS JetStream**: High-performance inter-service messaging
4. **Redis PubSub**: Pattern detection and memory updates
5. **PostgreSQL**: Persistent blockchain and time-series data

## Security Considerations

- All services should run on localhost only in development
- Production deployment requires proper authentication
- API keys must be set via environment variables
- Database credentials should use secrets management
- CROD_NO_PUBLIC_PORTS should be true in production