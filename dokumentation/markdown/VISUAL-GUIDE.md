# 🎯 CROD Visual Testing Guide

## What Can You Test RIGHT NOW

<svg viewBox="0 0 900 800" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="450" y="30" text-anchor="middle" font-family="Arial" font-size="24" font-weight="bold">CROD Testing Flow</text>
  
  <!-- Step 1: Start System -->
  <rect x="50" y="60" width="250" height="120" fill="#3b82f6" stroke="#2563eb" stroke-width="3" rx="10"/>
  <text x="175" y="100" text-anchor="middle" fill="white" font-family="Arial" font-size="18" font-weight="bold">1. Start System</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-family="Arial" font-size="14">./start-simple.sh</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-family="Arial" font-size="12">Starts API + GUI</text>
  
  <!-- Arrow -->
  <path d="M 300 120 L 350 120" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  
  <!-- Step 2: Create Genesis -->
  <rect x="350" y="60" width="250" height="120" fill="#10b981" stroke="#059669" stroke-width="3" rx="10"/>
  <text x="475" y="100" text-anchor="middle" fill="white" font-family="Arial" font-size="18" font-weight="bold">2. Create Genesis</text>
  <text x="475" y="125" text-anchor="middle" fill="white" font-family="Arial" font-size="12">curl -X POST</text>
  <text x="475" y="145" text-anchor="middle" fill="white" font-family="Arial" font-size="12">localhost:4000/genesis</text>
  <text x="475" y="165" text-anchor="middle" fill="white" font-family="Arial" font-size="11">Returns: password & key</text>
  
  <!-- Arrow -->
  <path d="M 600 120 L 650 120" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  
  <!-- Step 3: View Dashboard -->
  <rect x="650" y="60" width="200" height="120" fill="#8b5cf6" stroke="#7c3aed" stroke-width="3" rx="10"/>
  <text x="750" y="100" text-anchor="middle" fill="white" font-family="Arial" font-size="18" font-weight="bold">3. Dashboard</text>
  <text x="750" y="130" text-anchor="middle" fill="white" font-family="Arial" font-size="12">Open Browser:</text>
  <text x="750" y="150" text-anchor="middle" fill="white" font-family="Arial" font-size="12">localhost:8080</text>
  
  <!-- Testing Options -->
  <text x="450" y="220" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">What You Can Test</text>
  
  <!-- API Tests -->
  <g transform="translate(50, 250)">
    <rect width="380" height="200" fill="#fee2e2" stroke="#dc2626" stroke-width="2" rx="8"/>
    <text x="190" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">🔌 API Tests</text>
    
    <text x="20" y="60" font-family="Arial" font-size="13">✓ Check Status:</text>
    <text x="30" y="80" font-family="monospace" font-size="11">curl localhost:4000/status</text>
    
    <text x="20" y="110" font-family="Arial" font-size="13">✓ Mine Blocks:</text>
    <text x="30" y="130" font-family="monospace" font-size="11">curl -X POST localhost:4000/mine \</text>
    <text x="30" y="145" font-family="monospace" font-size="11">  -d '{"data":{"msg":"Hello"}}' \</text>
    <text x="30" y="160" font-family="monospace" font-size="11">  -H 'Content-Type: application/json'</text>
    
    <text x="20" y="185" font-family="Arial" font-size="13">✓ View All Blocks:</text>
    <text x="30" y="200" font-family="monospace" font-size="11">curl localhost:4000/blocks</text>
  </g>
  
  <!-- GUI Tests -->
  <g transform="translate(470, 250)">
    <rect width="380" height="200" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="8"/>
    <text x="190" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">🎨 GUI Tests</text>
    
    <text x="20" y="60" font-family="Arial" font-size="13">✓ Genesis Setup Page:</text>
    <text x="30" y="80" font-family="monospace" font-size="11">localhost:8080/genesis-setup.html</text>
    
    <text x="20" y="110" font-family="Arial" font-size="13">✓ Main Dashboard:</text>
    <text x="30" y="130" font-family="monospace" font-size="11">localhost:8080</text>
    
    <text x="20" y="160" font-family="Arial" font-size="13">✓ Real-time Updates:</text>
    <text x="30" y="180" font-family="Arial" font-size="12">Watch blocks appear as you mine!</text>
  </g>
  
  <!-- Advanced Tests -->
  <g transform="translate(50, 480)">
    <rect width="380" height="150" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" rx="8"/>
    <text x="190" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">🧪 Advanced Tests</text>
    
    <text x="20" y="60" font-family="Arial" font-size="13">✓ Game Theory Engine:</text>
    <text x="30" y="80" font-family="monospace" font-size="11">cd engines/game-theory && npm test</text>
    
    <text x="20" y="105" font-family="Arial" font-size="13">✓ Neural Network Demo:</text>
    <text x="30" y="125" font-family="monospace" font-size="11">cd neural && node demo.js</text>
  </g>
  
  <!-- Integration Tests -->
  <g transform="translate(470, 480)">
    <rect width="380" height="150" fill="#dcfce7" stroke="#22c55e" stroke-width="2" rx="8"/>
    <text x="190" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">🔗 Integration Tests</text>
    
    <text x="20" y="60" font-family="Arial" font-size="13">✓ Claude Pattern Detection:</text>
    <text x="30" y="80" font-family="monospace" font-size="11">curl localhost:8888/detect-patterns</text>
    
    <text x="20" y="105" font-family="Arial" font-size="13">✓ Check Logs:</text>
    <text x="30" y="125" font-family="monospace" font-size="11">tail -f logs/*.log</text>
  </g>
  
  <!-- Status Box -->
  <g transform="translate(200, 660)">
    <rect width="500" height="100" fill="#f3f4f6" stroke="#6b7280" stroke-width="2" rx="8"/>
    <text x="250" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Current System Status</text>
    <text x="250" y="55" text-anchor="middle" font-family="Arial" font-size="14">✅ Blockchain Core: Working</text>
    <text x="250" y="75" text-anchor="middle" font-family="Arial" font-size="14">✅ Web GUI: Working</text>
    <text x="250" y="95" text-anchor="middle" font-family="Arial" font-size="14">⚠️  AI Integration: Partial (needs API key)</text>
  </g>
  
  <!-- Arrow marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

## Quick Test Sequence

```bash
# 1. Start everything
./start-simple.sh

# 2. In a new terminal, create genesis block
curl -X POST http://localhost:4000/genesis

# 3. Mine some blocks
curl -X POST http://localhost:4000/mine \
  -H 'Content-Type: application/json' \
  -d '{"data":{"message":"First block!"}}'

curl -X POST http://localhost:4000/mine \
  -H 'Content-Type: application/json' \
  -d '{"data":{"value":42,"type":"test"}}'

# 4. Check your blockchain
curl http://localhost:4000/blocks | jq .

# 5. Open browser to see dashboard
# http://localhost:8080
```

## Expected Results

### Genesis Block Response:
```json
{
  "genesis": {
    "index": 0,
    "timestamp": 1234567890,
    "data": {"message": "CROD Genesis Block"},
    "hash": "abc123..."
  },
  "credentials": {
    "password": "crod-2025-01-04-xyz",
    "publicKey": "CROD-PUB-abc123..."
  }
}
```

### Mining Response:
```json
{
  "block": {
    "index": 1,
    "timestamp": 1234567891,
    "data": {"message": "First block!"},
    "previousHash": "abc123...",
    "hash": "def456...",
    "nonce": 12345
  },
  "miningTime": "234ms"
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Wait 3 seconds after starting, services need time |
| GUI shows blank page | Check if you're in crod-gui directory |
| Can't mine blocks | Create genesis block first |
| Ports already in use | Run `pkill -f node` and `pkill -f python3` |

## What's NOT Working Yet

- ❌ Polyglot service integration (Elixir, Rust, Go)
- ❌ Actual AI model training
- ❌ Quantum simulation
- ❌ Time travel features
- ❌ Multi-node consensus

## Next Steps

1. **Get AI Working**: Add your Claude/OpenAI API keys
2. **Connect Services**: Wire up the pattern detection to blockchain
3. **Test Game Theory**: Run the Nash equilibrium calculations
4. **Deploy Multi-Node**: Test with multiple blockchain nodes