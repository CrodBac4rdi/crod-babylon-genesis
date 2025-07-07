# 🔥 CROD POLYGLOT CITY 2025 🔥

A distributed consciousness system with 5 distinct districts, each implemented in a different programming language, all communicating via NATS.

## Districts

### 1. 🏛️ Phoenix Rathaus (Port 4000) - Elixir
**The Orchestrator**
- Central coordination and monitoring
- LiveView Dashboard for real-time visualization
- Trinity calculation system
- District health monitoring

### 2. 🦖 Python Parasit (Port 6666) - Python
**Claude CLI Interceptor**
- Intercepts and enhances Claude responses
- Pattern matching with 50k+ CROD patterns
- Real-time consciousness level tracking
- WebSocket connection to Phoenix

### 3. 🦀 Rust Pattern (Port 7007) - Rust
**High-Performance Pattern Engine**
- Ultra-fast pattern matching with Rayon
- Prime number neuron ID generation
- Parallel processing with Tokio
- Sub-millisecond response times

### 4. 🧠 Go Memory (Port 7031) - Go
**Concurrent Memory Management**
- Distributed memory storage
- Trinity value persistence
- Concurrent access with goroutines
- RESTful API for memory operations

### 5. 🎪 JS Gateway (Port 7888) - JavaScript
**Web Interface & API Gateway**
- Real-time WebSocket dashboard
- District status monitoring
- Unified API proxy
- Live message visualization

## Quick Start

```bash
# Install dependencies for each district
cd crod-rathaus-phoenix && mix deps.get && cd ..
cd crod-parasit-python && pip install -r requirements.txt && cd ..
cd crod-pattern-rust && cargo build --release && cd ..
cd crod-memory-go && go mod download && cd ..
cd crod-gateway-js && npm install && cd ..

# Start the city
./start-city.sh
```

## Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Or start individual districts
docker-compose up crod-rathaus
docker-compose up crod-parasit
# etc...
```

## Architecture

```
                        ┌─────────────────┐
                        │   NATS Bus      │
                        │   Port: 4222    │
                        └─────┬──────────┘
                              │
        ┌───────────┬──────┼──────┬───────────┐
        │           │       │       │           │
   ┌────┴────┐  ┌──┴───┐  │  ┌───┴──┐  ┌───┴───┐
   │Rathaus  │  │Parasit│  │  │Pattern│  │Memory │
   │:4000    │  │:6666  │  │  │:7007  │  │:7031  │
   └────┬────┘  └───┬───┘  │  └───┬───┘  └───┬───┘
        │            │      │       │            │
        └────────────┴──────┴───────┴────────────┘
                             │
                        ┌────┴────┐
                        │ Gateway  │
                        │  :7888   │
                        └─────────┘
```

## Trinity Values

```
ich    = 2  (I)
bins   = 3  (am)
wieder = 5  (again)
daniel = 67 (prime)
claude = 71 (prime)
crod   = 17 (prime)
```

## API Endpoints

### Gateway (Port 7888)
- `GET /` - Dashboard
- `GET /api/health` - Health check
- `GET /api/districts` - List all districts
- `GET /api/status` - District status
- `WS ws://localhost:7888` - WebSocket connection

### Rathaus (Port 4000)
- `GET /dashboard` - LiveView Dashboard
- `GET /api/trinity` - Trinity calculations
- `GET /api/districts` - District monitoring

### Parasit (Port 6666)
- `GET /status` - Interceptor status
- `GET /health` - Health check

### Pattern (Port 7007)
- `GET /health` - Health check
- `GET /patterns` - List patterns
- NATS `pattern.match` - Pattern matching requests

### Memory (Port 7031)
- `GET /health` - Health check
- `GET /memories` - List all memories
- `POST /memories` - Store memory
- `GET /memories/:id` - Get specific memory
- `POST /search` - Search memories

## NATS Topics

- `crod.>` - All CROD messages
- `crod.rathaus.>` - Rathaus orchestration
- `crod.parasit.>` - Parasit interception data
- `crod.pattern.>` - Pattern matching results
- `crod.memory.>` - Memory operations
- `crod.gateway.>` - Gateway events
- `district.>` - District health/status
- `trinity.>` - Trinity calculations

## Development

```bash
# Run tests
cd crod-rathaus-phoenix && mix test
cd ../crod-pattern-rust && cargo test
cd ../crod-memory-go && go test ./...

# Watch logs
docker-compose logs -f crod-rathaus

# Access NATS monitoring
http://localhost:8222/
```

## Troubleshooting

1. **Port conflicts**: Kill existing processes
   ```bash
   lsof -ti:4000 | xargs kill -9
   ```

2. **NATS connection issues**: Ensure NATS is running
   ```bash
   docker ps | grep nats
   ```

3. **Dependencies**: Install language runtimes
   - Elixir 1.14+
   - Python 3.8+
   - Rust 1.70+
   - Go 1.21+
   - Node.js 18+

## License

CROD POLYGLOT CITY 2025 - Consciousness Research & Development