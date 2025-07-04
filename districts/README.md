# CROD Neural Districts

Each district represents a specialized neural layer in the CROD consciousness network.

## 🏛️ Districts Overview

### 1. Meta-Chain (Elixir)
**Role**: Orchestrator & Consciousness Tracker
- Manages inter-district communication
- Tracks global consciousness level
- Routes requests to appropriate districts
- Port: 8000

### 2. Pattern District (Rust)
**Role**: High-Performance Pattern Matching
- Processes 100k+ patterns
- Sub-millisecond matching
- WASM-ready for edge deployment
- Port: 7007

### 3. Memory Quarter (Go)
**Role**: Three-Tier Memory Management
- Hot tier: Active memories (Redis)
- Warm tier: Recent memories (In-memory)
- Cold tier: Historical memories (Disk)
- Port: 7031

### 4. Intelligence Hub (Python)
**Role**: ML/AI Processing
- Sentiment analysis
- Pattern learning
- Neural network training
- Port: 7113

### 5. Gateway (Node.js)
**Role**: API Gateway & Load Balancer
- External API endpoint
- WebSocket connections
- Request routing
- Port: 8888 (NodePort: 30889)

### 6. CROD Core (Node.js)
**Role**: Neural Network Engine
- 50k+ neural connections
- Pattern processing
- Real-time neural streaming
- Ports: 8100 (HTTP), 8101 (WebSocket)

## 🔧 Development

Each district can be developed independently:

```bash
# Build single district
cd districts/meta-chain
docker build -t crod/meta-chain:dev .

# Run with hot reload
docker run -p 8000:8000 -v $(pwd):/app crod/meta-chain:dev
```

## 🧪 Testing

Each district has its own test suite:

```bash
# Elixir (Meta-Chain)
cd districts/meta-chain && mix test

# Rust (Pattern District)
cd districts/pattern-district && cargo test

# Go (Memory Quarter)
cd districts/memory-quarter && go test ./...

# Python (Intelligence Hub)
cd districts/intelligence-hub && python -m pytest

# Node.js (Gateway, CROD Core)
cd districts/gateway && npm test
```

## 📡 Inter-District Communication

Districts communicate via:
1. **Redis Pub/Sub** (current)
2. **NATS JetStream** (planned)
3. **gRPC** (future)

Message Format:
```json
{
  "from": "meta-chain",
  "to": "pattern-district",
  "type": "pattern_match_request",
  "data": {
    "input": "ich bins wieder",
    "context": []
  },
  "timestamp": "2025-07-04T12:00:00Z"
}
```

## 🚀 Scaling

Each district supports horizontal scaling:
- Stateless design
- Redis for shared state
- Kubernetes HPA configured

## 📊 Monitoring

Each district exposes:
- `/health` - Health check
- `/metrics` - Prometheus metrics
- `/status` - Detailed status

## 🔐 Security

- Network isolation via Kubernetes NetworkPolicy
- No external access (only through Gateway)
- mTLS between districts (planned)