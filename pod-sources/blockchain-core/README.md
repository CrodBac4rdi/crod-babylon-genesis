# CROD Blockchain Core

## 🔗 The Real Blockchain Implementation for CROD

This is the core blockchain engine that provides the immutable truth layer for all CROD operations.

## 🚀 Features

### Core Blockchain
- **Quantum-Safe**: Multi-round SHA-256 hashing (future: Dilithium5 + Kyber1024)
- **Proof of Work**: Adjustable difficulty mining
- **Genesis Block**: Contains CROD trinity values
- **Block Validation**: Full chain validation

### Document Delta Support
- **Hash-to-Prime Conversion**: Every document gets a unique prime number
- **Delta Storage**: Only store changes, not full documents
- **Pattern Detection**: Find relationships between documents using primes

### Transaction Types
- **Pattern Discovery**: Record new patterns found
- **Smart Contract Calls**: Track Meta-Chain contract executions
- **NFT Minting**: Pattern NFT creation records
- **DeFi Operations**: Swaps, liquidity, staking
- **Document Deltas**: Document change tracking

### Integration Points
- **Redis Pub/Sub**: Real-time event streaming
- **REST API**: Full HTTP API for all operations
- **Gateway Compatible**: Works with CROD Gateway (port 30889)
- **Meta-Chain Sync**: Syncs with Elixir blockchain

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│     Gateway     │────▶│  Blockchain  │◀────│   Meta-Chain    │
│   (Port 30889)  │     │     Core     │     │  (Port 8000)    │
└─────────────────┘     │  (Port 8085) │     └─────────────────┘
                        └───────┬───────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼──────┐       ┌───────▼──────┐
            │    Redis     │       │ Intelligence │
            │   Pub/Sub    │       │     Hub      │
            └──────────────┘       └──────────────┘
```

## 📡 API Endpoints

### Blockchain Operations
- `GET /` - Service info
- `GET /blockchain/info` - Blockchain statistics
- `GET /blockchain/blocks` - Get all blocks
- `GET /blockchain/validate` - Validate chain integrity

### Transaction Endpoints
- `POST /transaction/pattern` - Record pattern discovery
- `POST /transaction/smart-contract` - Record contract call
- `POST /transaction/nft` - Record NFT minting
- `POST /transaction/defi` - Record DeFi operation

### Delta Operations
- `POST /delta/process` - Process document update
- `POST /delta/pattern` - Find pattern between documents

### Pattern Operations
- `POST /pattern/discover` - Discover new pattern
- `POST /pattern/prime` - Calculate pattern prime

## 🔧 Configuration

Environment variables:
- `REDIS_ADDR` - Redis address (default: redis-service:6379)
- `PORT` - Service port (default: 8085)

## 🚀 Running

### Local Development
```bash
go mod download
go run *.go
```

### Docker
```bash
docker build -t crod/blockchain-core .
docker run -p 8085:8085 crod/blockchain-core
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

## 📝 Example Usage

### Process Document Delta
```bash
curl -X POST http://localhost:8085/delta/process \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc123",
    "previous_content": "Hello world",
    "current_content": "Hello CROD world"
  }'
```

### Record Pattern Discovery
```bash
curl -X POST http://localhost:8085/pattern/discover \
  -H "Content-Type: application/json" \
  -d '{
    "atoms": ["ich", "bins", "wieder"],
    "discoverer": "daniel"
  }'
```

### Record Smart Contract Call
```bash
curl -X POST http://localhost:8085/transaction/smart-contract \
  -H "Content-Type: application/json" \
  -d '{
    "from": "0x123...",
    "contract_call": {
      "contract_address": "0xABC...",
      "function": "transfer",
      "args": ["0xDEF...", 100],
      "gas_used": 21000
    }
  }'
```

## 🔮 Future Enhancements

1. **Real Quantum-Safe Crypto**: Implement Dilithium5 + Kyber1024
2. **Consensus Mechanisms**: Add PoS, DPoS options
3. **Sharding**: Horizontal scaling for high throughput
4. **State Channels**: Off-chain scaling
5. **Cross-Chain Bridges**: Direct integration with Ethereum, Cosmos

## 🧠 How It Works

1. **Genesis Block**: Contains CROD trinity values (daniel:67, claude:71, crod:17)
2. **Mining**: Proof of Work with adjustable difficulty
3. **Transactions**: All CROD operations recorded on-chain
4. **Primes**: Document hashes converted to primes for pattern math
5. **Redis Events**: Real-time sync with other CROD services

**"The immutable truth layer for the CROD ecosystem!"** 🔥