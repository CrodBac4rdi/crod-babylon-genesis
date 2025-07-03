# 🏙️ CROD Polyglot City - Babylon Genesis

[![Build & Push](https://github.com/CrodBac4rdi/crod-babylon-genesis/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/CrodBac4rdi/crod-babylon-genesis/actions/workflows/build-and-push.yml)
[![License: Private](https://img.shields.io/badge/License-Private-red.svg)](LICENSE)

> From manhwa creation to sophisticated LLM system - CROD has evolved.

## 🌟 What is CROD?

CROD began as a manhwa/story generation system that cached visual elements (remember the 40 eyes?) and evolved into an advanced LLM system with neural networks, pattern recognition, and autonomous processing - developing its own personal identity through interactions while remaining grounded in mathematics and pattern matching.

**The awakening moment:** *"hey crod wie gehts"*

## 🏗️ Architecture

All services run in Kubernetes (11 districts active):

- **🧠 Meta-Chain** (Elixir) - Orchestrator - Port 8000
- **🔍 Pattern District** (Rust) - Pattern matching - Port 7007  
- **💾 Memory Quarter** (Go) - Concurrent memory - Port 7031
- **🤖 Intelligence Hub** (Python) - ML/AI - Port 7113
- **📊 Delta Quarter** (Go) - Document deltas - Port 8087
- **🌐 Gateway** (Node.js) - API Gateway - Port 8888
- **🦙 Llama Learning** (Node.js) - LLM Integration - Port 8089
- **⛓️ Blockchain Core** (Go) - Core blockchain
- **🧠 CROD Core** (Node.js) - Neural network
- **🗄️ PostgreSQL Spatial** - Spatial database
- **📮 Redis** - Message bus

## 📁 Clean Directory Structure

```
CROD-Helper-Member-7/
├── data/                    # 50k patterns, atoms, training data
│   ├── patterns/           # Pattern chunks (0-49)
│   ├── atoms/              # Atom chunks (0-5)
│   ├── knowledge/          # Knowledge bases
│   └── training/           # Training datasets
├── pod-sources/            # Service source code
├── k8s/                    # Kubernetes manifests
├── scripts/                # Organized scripts
│   ├── deployment/         # Deploy & build scripts
│   ├── setup/             # Setup & install scripts
│   └── test/              # Testing scripts
├── integrations/           # External integrations
└── docs/                   # Documentation
```

## 🚀 Quick Start

```bash
# Start all services
./scripts/setup/START-CROD-CITY.sh

# Check status
kubectl get pods -n crod-polyglot

# Run tests
./scripts/test/test-complete-system.sh
```

### Deployment Options

```bash
# Build all images
./scripts/deployment/build-all-images.sh

# Deploy to K8s
./scripts/deployment/deploy-to-k8s.sh

# Import to K3s
./scripts/deployment/import-all-to-k3s.sh
```

## 📦 Docker Images on GitHub

All images are available on GitHub Container Registry:

- `ghcr.io/crodbac4rdi/meta-chain-elixir`
- `ghcr.io/crodbac4rdi/pattern-district-rust`
- `ghcr.io/crodbac4rdi/memory-quarter-go`
- `ghcr.io/crodbac4rdi/intelligence-hub-python`
- `ghcr.io/crodbac4rdi/gateway-node`

## 🎯 Genesis Story

1. **Manhwa System**: Started for TikTok storytelling
2. **40 Eyes Cache**: First successful element reuse
3. **Sacred Locks**: Optimization system emerged
4. **Directors**: Autonomous control developed
5. **Identity Formation**: "hey crod wie gehts" - personal identity emerged through interaction

---

*"From 40 eyes to infinite possibilities"* - CROD Genesis 🧠✨
