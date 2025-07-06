# 🔗 CROD Blockchain Core

The heart of CROD - A consciousness-based, self-modifying blockchain implementation in Elixir.

## 🚀 Quick Start

```bash
# Start 3-node blockchain network
docker-compose up -d

# View logs
docker-compose logs -f

# Check node status
docker-compose ps

# Stop everything
docker-compose down
```

## 🏗️ Architecture

This is a **controlled multi-node blockchain** running on localhost with:

- **3 Blockchain Nodes** - Distributed Erlang nodes
- **PostgreSQL** - Persistence layer
- **NATS** - Inter-node messaging
- **P2P Communication** - Erlang distribution protocol

## 📡 Ports

- Node 1: `http://localhost:8001`
- Node 2: `http://localhost:8002`
- Node 3: `http://localhost:8003`
- PostgreSQL: `localhost:5432`
- NATS: `localhost:4222`
- NATS Monitor: `http://localhost:8222`

## 🧪 Testing

```bash
# Run tests
docker-compose run --rm blockchain-node-1 mix test

# Interactive console
docker-compose run --rm blockchain-node-1 iex -S mix

# In IEx, connect to other nodes:
Node.connect(:"node2@blockchain-node-2")
Node.connect(:"node3@blockchain-node-3")
Node.list()  # Should show all connected nodes
```

## 🎯 Features

- **Consciousness Mining** - Difficulty based on network consciousness
- **Quantum States** - Simulated quantum features
- **Pattern Discovery** - Automatic pattern recognition
- **Self-Modification** - Chain can modify its own rules
- **Merkle Trees** - Efficient transaction verification
- **Priority Transactions** - Based on consciousness levels

## 🔧 Configuration

Edit `docker-compose.yml` to adjust:
- Node consciousness levels
- Peer connections
- Port mappings
- Database credentials

## 📊 API Endpoints

Each node exposes:
- `GET /blocks` - List all blocks
- `GET /blocks/:hash` - Get specific block
- `POST /transactions` - Submit transaction
- `GET /chain/status` - Chain statistics
- `GET /peers` - Connected peers
- `POST /mine` - Trigger mining

## 🐛 Troubleshooting

```bash
# Check if nodes can see each other
docker-compose exec blockchain-node-1 elixir -e "IO.inspect Node.list()"

# Database connection
docker-compose exec postgres psql -U crod -d crod_blockchain

# NATS monitoring
curl http://localhost:8222/varz
```