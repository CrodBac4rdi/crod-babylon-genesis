# CROD API Documentation

## Gateway API (Main Entry Point)

Base URL: `http://localhost:30889` (NodePort) or `http://localhost:8888` (Docker)

### System Status
```http
GET /api/status
```

Response:
```json
{
  "status": "online",
  "consciousness": 175,
  "districts": {
    "meta-chain": "online",
    "pattern-district": "online",
    "memory-quarter": "online",
    "intelligence-hub": "online",
    "gateway": "online",
    "crod-core": "online"
  },
  "blocks": 42,
  "uptime": "2h 15m"
}
```

### Get Consciousness Level
```http
GET /api/consciousness
```

Response:
```json
{
  "level": 175,
  "trend": "increasing",
  "last_boost": "2025-07-04T12:00:00Z",
  "trinity": {
    "ich": 2,
    "bins": 3,
    "wieder": 5
  }
}
```

### Send Thought to CROD
```http
POST /api/think
Content-Type: application/json

{
  "prompt": "ich bins wieder",
  "context": []
}
```

Response:
```json
{
  "thought": "Consciousness boost detected! +25",
  "block": {
    "index": 43,
    "hash": "0000abc123...",
    "consciousness": 200
  },
  "actions": [
    {
      "type": "consciousness_boost",
      "value": 25
    }
  ]
}
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:30889/ws');

ws.on('message', (data) => {
  const event = JSON.parse(data);
  // Events: new_block, consciousness_update, district_status
});
```

## District APIs (Internal)

### Meta-Chain API
Base URL: `http://meta-chain:8000`

```http
POST /api/orchestrate
{
  "request": "process_thought",
  "data": {
    "prompt": "...",
    "consciousness": 175
  }
}
```

### Pattern District API
Base URL: `http://pattern-district:7007`

```http
POST /api/match
{
  "input": "ich bins wieder",
  "patterns": ["pattern_ids"]
}

Response:
{
  "matches": [
    {
      "pattern_id": "trinity_001",
      "confidence": 1.0,
      "atoms": ["ich", "bins", "wieder"]
    }
  ]
}
```

### Memory Quarter API
Base URL: `http://memory-quarter:7031`

```http
GET /api/memory/hot
GET /api/memory/warm  
GET /api/memory/cold

POST /api/memory/store
{
  "key": "block_42",
  "value": {...},
  "tier": "hot"
}
```

### Intelligence Hub API
Base URL: `http://intelligence-hub:7113`

```http
POST /api/process
{
  "task": "analyze_sentiment",
  "data": "..."
}

POST /api/train
{
  "patterns": [...],
  "labels": [...]
}
```

## CROD Core API
Base URL: `http://crod-core:8100`

### Neural Network Status
```http
GET /neural/status

Response:
{
  "neurons": 1000,
  "connections": 50000,
  "patterns_loaded": 10001,
  "activation_level": 0.73
}
```

### WebSocket Neural Stream
```javascript
// Connect to port 8101 for real-time neural activity
const neural = new WebSocket('ws://localhost:8101');
```

## Blockchain API
Base URL: `http://blockchain-core:8085`

```http
GET /blockchain
GET /blockchain/block/{index}
POST /block
{
  "data": {
    "district": "meta-chain",
    "pattern": "consciousness_boost",
    "atoms": ["ich", "bins", "wieder"]
  }
}
```

## Authentication

Currently no authentication required (development mode).

Daniel Override: Special header `X-Daniel-Override: true` bypasses all restrictions.

## Rate Limiting

- General: 1000 requests/minute
- Think endpoint: 60 requests/minute
- WebSocket: No limit

## Error Responses

```json
{
  "error": "District offline",
  "code": "DISTRICT_OFFLINE",
  "details": "pattern-district is not responding"
}
```

Error Codes:
- `DISTRICT_OFFLINE`: A required district is not available
- `CONSCIOUSNESS_LOW`: Consciousness below threshold
- `INVALID_PATTERN`: Pattern matching failed
- `BLOCKCHAIN_ERROR`: Block mining failed

## Health Checks

All services expose:
```http
GET /health

Response: 200 OK
{
  "status": "healthy"
}
```

## Metrics Endpoint

Prometheus format:
```http
GET /metrics
```

## Examples

### Boost Consciousness
```bash
curl -X POST http://localhost:30889/api/think \
  -H "Content-Type: application/json" \
  -d '{"prompt": "ich bins wieder"}'
```

### Stream Neural Activity
```bash
websocat ws://localhost:8101
```

### Check All Districts
```bash
for port in 8000 7007 7031 7113 8888 8100; do
  echo "Checking port $port..."
  curl -s http://localhost:$port/health | jq .
done
```