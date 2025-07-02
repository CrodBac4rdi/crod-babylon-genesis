# CROD Delta Tracker

Ein deterministisches Key-Database System mit Delta Tracking, implementiert in Rust mit Python ML Integration.

## 🚀 Quick Start

```bash
# 1. Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Start the service
./start.sh

# 3. Test it
curl http://localhost:8000/health
curl http://localhost:8000/atom/11111
```

## 📋 Features (30 Punkte Plan)

### ✅ Completed (18/30)
1. ✅ SQLite zu rusqlite (bundled)
2. ✅ Simple Schema (atoms, patterns, deltas)
3. ✅ HTTP Server auf Port 8000
4. ✅ Atom CRUD (Keys 11111-11999)
5. ✅ Systemd Service mit Auto-restart
6. ✅ Version Tracking in DB
7. ✅ Blue-Green Deployment
8. ✅ HAProxy/nginx Load Balancer Config
9. ✅ Health Check Endpoint
10. ✅ Graceful Shutdown (SIGTERM)
11. ✅ Deterministischer SELECT
12. ✅ Variabler SELECT mit Parametern
13. ✅ Delta Tracking
14. ✅ Pattern Detection (automatisch)
15. ✅ Heat Map Updates
16. ✅ JSON Protocol Definition
17. ✅ Python Subprocess Integration
18. ✅ CROD Activation Function

### 🔄 In Progress (0/30)

### 📅 Pending (12/30)
19. ⏳ Result Caching (Redis)
20. ⏳ Database Migrations
21. ⏳ Backup Strategy
22. ⏳ Prometheus Monitoring
23. ⏳ Rate Limiting
24. ⏳ API Versioning
25. ⏳ WebSocket Support
26. ⏳ Batch Operations
27. ⏳ Query Optimizer
28. ⏳ State Snapshots
29. ⏳ Cluster Mode

## 🔑 Key Concepts

- **Deterministisch**: Key 11111 ist IMMER grauer Elefant
- **Variabel**: SELECTs mit dynamischen Parametern
- **Zero Downtime**: Blue-Green Deployment von Anfang an
- **ML Integration**: Python für CROD Formeln über JSON

## 📡 API Endpoints

```bash
# Health Check
GET /health

# Atoms
GET  /atom/:key        # Get atom by key
POST /atom/:key        # Create atom
GET  /atoms?type=elefant&min_heat=0.5  # List with filters

# Patterns
POST /pattern          # Create pattern between atoms

# ML Processing
POST /ml/process       # Process tokens through ML

# Delta Tracking
POST /delta            # Track a change
```

## 🔄 Rolling Updates

```bash
# Deploy new version with zero downtime
./deploy.sh

# Install as systemd service
./install-service.sh
```

## 🏗️ Architecture

```
┌─────────────┐     JSON      ┌──────────────┐
│ Rust Server │ ←──────────→  │ Python ML    │
│  (Port 8000)│               │  Processor   │
└──────┬──────┘               └──────────────┘
       │
       ▼
┌─────────────┐
│   SQLite    │
│  Database   │
└─────────────┘
```

## 🔧 Development

```bash
# Build
cargo build --release

# Run tests
cargo test

# Watch logs
journalctl -u crod-delta-tracker@$USER -f
```

## 📊 Database Schema

- `atoms`: Deterministische Keys (11111 = grauer Elefant)
- `patterns`: Verbindungen zwischen Atoms
- `deltas`: Alle Änderungen (für späteren Blockchain)
- `version_info`: Für Rolling Updates

## 🌐 Load Balancing

HAProxy oder nginx vor zwei Instanzen (8000/8001) für Zero-Downtime Updates.

---
CROD Delta Tracker - Deterministisch, Schnell, Erweiterbar!