# 🏗️ CROD Project Structure

## 📁 Directory Organization

```
crod-babylon-genesis/
│
├── 🚀 current/                    # Active, working code
│   ├── working/                   # Production-ready components
│   │   ├── blockchain-server.js   # Core blockchain API
│   │   ├── crod-gui/             # React dashboard
│   │   └── training/             # AI/ML training modules
│   └── docs/                     # Latest documentation
│       ├── ARCHITECTURE.md       # System design
│       ├── API.md               # API reference
│       └── CRITICAL-2025-UPDATES.md
│
├── 🔧 in-progress/               # Features under development
│   ├── polyglot/                 # Multi-language integration
│   │   ├── elixir/              # Orchestration layer
│   │   ├── rust/                # High-performance computing
│   │   ├── python/              # AI/ML processing
│   │   ├── go/                  # Memory management
│   │   └── crod-polyglot-api.js # Gateway service
│   ├── districts/                # Neural network districts
│   │   ├── pattern-genesis/      # Prime 7 district
│   │   ├── memory-districts/     # Prime 31 & 37
│   │   └── quantum-node/         # Prime 101
│   └── k8s/                      # Kubernetes configs
│       ├── deployments/          # Service deployments
│       └── crod-helm-chart/      # Helm chart
│
├── 📦 blockchain/                # Blockchain implementations
│   ├── elixir/                   # Elixir blockchain
│   │   ├── mix.exs              # Dependencies
│   │   └── lib/                 # Source code
│   ├── rust/                     # Rust components
│   │   ├── Cargo.toml           # Dependencies
│   │   └── src/                 # Source code
│   └── evolution/                # Self-modifying engine
│       └── history/             # Evolution tracking
│
├── 🗃️ archive/                   # Historical code
│   ├── old/                      # Deprecated features
│   ├── experiments/              # R&D prototypes
│   ├── planning/                 # Original designs
│   └── old-scripts/              # Deprecated scripts
│
├── 📊 visualization/             # Visual components
│   ├── diagrams/                 # Architecture diagrams
│   └── components/               # React viz components
│
├── 🔗 integrations/              # External integrations
│   ├── mcp/                      # Model Context Protocol
│   ├── a2a/                      # Agent-to-Agent
│   └── quantum-accelerators/     # Quantum computing
│
├── 📈 monitoring/                # Observability
│   ├── prometheus/               # Metrics collection
│   ├── grafana/                  # Dashboards
│   └── alerts/                   # Alert rules
│
├── 🧪 tests/                     # Test suites
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
│
├── 📝 docs/                      # Documentation root
│   ├── guides/                   # User guides
│   ├── api/                      # API docs
│   └── architecture/             # Design docs
│
├── 🔧 config/                    # Configuration files
│   ├── development/              # Dev configs
│   ├── production/               # Prod configs
│   └── crod.yaml                # Main config
│
├── 📊 data/                      # Runtime data
│   ├── blockchain/               # Chain data
│   ├── patterns/                 # Discovered patterns
│   └── models/                   # AI models
│
├── 📜 logs/                      # Application logs
│   ├── blockchain/               # Blockchain logs
│   ├── gui/                      # Frontend logs
│   └── districts/                # District logs
│
├── 🛠️ scripts/                   # Utility scripts
│   ├── setup/                    # Setup scripts
│   ├── deploy/                   # Deployment scripts
│   └── maintenance/              # Maintenance scripts
│
├── 🐳 Docker files               # Containerization
│   ├── docker-compose.yml        # Development stack
│   ├── docker-compose.blockchain.yml # Full blockchain
│   └── Dockerfile.*              # Service images
│
├── ⚙️ CI/CD                      # Automation
│   └── .github/
│       └── workflows/            # GitHub Actions
│
└── 📄 Root files                 # Project root
    ├── README.md                 # Project overview
    ├── ROADMAP-2025.md          # Development roadmap
    ├── CONTRIBUTING.md          # Contribution guide
    ├── SECURITY.md              # Security policy
    ├── LICENSE                  # MIT License
    ├── CROD-LAUNCHER.sh        # Main launcher
    └── START.sh                # Quick start script
```

## 🎯 Key Components

### 1. Core Services

| Service | Location | Port | Purpose |
|---------|----------|------|---------|
| Blockchain API | `current/working/blockchain-server.js` | 8000 | Main blockchain REST API |
| React GUI | `current/working/crod-gui/` | 8080 | Web dashboard |
| LLaMA Service | `current/working/training/llama-7b/` | 5001 | AI model service |
| Polyglot Gateway | `in-progress/polyglot/` | 4000 | Multi-language coordinator |

### 2. Neural Districts

| District | Prime | Port | Function |
|----------|-------|------|----------|
| Pattern Genesis | 7 | 7007 | Pattern discovery & matching |
| Short-term Memory | 31 | 7031 | Temporary data storage |
| Working Memory | 37 | 7037 | Active computation memory |
| Quantum Superposition | 101 | 7101 | Quantum state processing |
| Neural Genesis | 113 | 7113 | Neural network creation |
| Master Orchestrator | 127 | 7127 | System coordination |
| Time Travel | 179 | 7179 | Historical state navigation |

### 3. Language Responsibilities

| Language | Purpose | Key Features |
|----------|---------|--------------|
| **Elixir** | Meta-chain orchestration | Fault tolerance, distributed systems |
| **Rust** | High-performance compute | Memory safety, speed, quantum NIFs |
| **Python** | AI/ML processing | LLaMA integration, data science |
| **Go** | Memory management | Concurrent operations, efficiency |
| **Node.js** | API & blockchain core | Async I/O, web services |

## 🔄 Data Flow

```
User Request → API Gateway (4000)
     ↓
Polyglot Router
     ↓
┌────┴────┬────────┬────────┬────────┐
│ Elixir  │  Rust  │ Python │   Go   │
│Orchestr.│Pattern │   AI   │ Memory │
└────┬────┴────────┴────────┴────────┘
     ↓
NATS Message Bus (4222)
     ↓
Neural Districts (7xxx ports)
     ↓
Blockchain Core (8000)
     ↓
Response → User
```

## 🚀 Quick Commands

### Start Services
```bash
# Interactive menu
./CROD-LAUNCHER.sh

# Quick start (blockchain + GUI)
./CROD-LAUNCHER.sh --quick

# Full blockchain stack
./CROD-LAUNCHER.sh --full

# Development mode
./CROD-LAUNCHER.sh --dev
```

### Check Status
```bash
# Service status
./CROD-LAUNCHER.sh --status

# View logs
tail -f logs/**/*.log

# Check specific service
curl http://localhost:8000/status
```

### Development
```bash
# Run tests
npm test

# Build GUI
cd current/working/crod-gui && npm run build

# Start specific district
cd in-progress/districts/pattern-genesis && cargo run
```

## 📋 Configuration Files

### Main Config (`config/crod.yaml`)
```yaml
blockchain:
  network: mainnet
  genesis_password: "secure-password"
  consensus: "consciousness-driven"

districts:
  enabled: true
  auto_scale: true
  
api:
  rate_limit: 1000
  cors_enabled: true
```

### Environment Variables
```bash
# .env file
CROD_ENV=development
BLOCKCHAIN_PORT=8000
GUI_PORT=8080
NATS_URL=nats://localhost:4222
LOG_LEVEL=info
```

## 🔐 Security Considerations

1. **Secrets Management**
   - Use `.env` files (never commit)
   - Kubernetes secrets for production
   - Hardware security modules for keys

2. **Network Security**
   - All services behind API gateway
   - TLS/SSL for external communication
   - Port access control

3. **Code Security**
   - Post-quantum cryptography
   - Regular security audits
   - Dependency scanning

## 🎨 Development Workflow

1. **Feature Development**
   - Create feature branch
   - Develop in `in-progress/`
   - Test thoroughly
   - Move to `current/` when ready

2. **Testing**
   - Unit tests for each component
   - Integration tests for districts
   - E2E tests for full flow

3. **Deployment**
   - Local: Docker Compose
   - Staging: Kubernetes
   - Production: Multi-region K8s

## 📚 Additional Resources

- [Architecture Deep Dive](docs/architecture/DEEP-DIVE.md)
- [API Documentation](docs/api/REFERENCE.md)
- [Security Guide](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)

---

*For questions or issues, check our [GitHub Issues](https://github.com/CrodBac4rdi/crod-babylon-genesis/issues)*