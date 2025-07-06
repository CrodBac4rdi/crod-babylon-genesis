# CROD Source Code

## Overview

This directory contains all active source code for the CROD Babylon Genesis project.

## Structure

```
src/
├── blockchain/         # Core blockchain implementations
│   ├── elixir/        # Elixir-based blockchain modules
│   ├── rust/          # High-performance Rust components
│   ├── python/        # AI/ML modules in Python
│   └── shared/        # Shared interfaces and protocols
├── frontend/          # User interfaces
│   └── crod-gui/      # React-based dashboard
├── services/          # Microservices
│   ├── orchestration/ # Master orchestrator
│   ├── monitoring/    # Health and metrics monitoring
│   └── visualization/ # Scientific visualization tools
└── integrations/      # External system integrations
    ├── nats/          # NATS messaging integration
    ├── redis/         # Redis caching integration
    └── quantum/       # Quantum computing APIs
```

## Core Components

### Blockchain (`blockchain/`)
The heart of CROD - implements consciousness-driven consensus, quantum mining, and self-modifying code capabilities.

- **Elixir modules**: Main blockchain logic, consensus algorithms
- **Rust components**: Performance-critical operations, cryptography
- **Python modules**: AI/ML for pattern recognition, consciousness metrics
- **Shared interfaces**: Common protocols for cross-language communication

### Frontend (`frontend/`)
User interfaces for interacting with the CROD blockchain.

- **crod-gui**: React-based dashboard showing real-time blockchain metrics, consciousness levels, and pattern discoveries

### Services (`services/`)
Microservices that support the blockchain infrastructure.

- **Orchestration**: Manages service lifecycle and coordination
- **Monitoring**: Tracks system health, performance metrics
- **Visualization**: Generates scientific visualizations of quantum states

### Integrations (`integrations/`)
Connectors to external systems and APIs.

- **NATS**: Message streaming for inter-service communication
- **Redis**: High-performance caching and pub/sub
- **Quantum**: Interfaces to quantum computing simulators/hardware

## Development Guidelines

1. **Language Choice**:
   - Elixir: Core blockchain logic, fault-tolerant systems
   - Rust: Performance-critical paths, cryptography
   - Python: AI/ML, data analysis, visualization
   - Go: System tools, CLI programs
   - JavaScript/React: Frontend applications

2. **Code Style**:
   - Follow language-specific conventions
   - Use descriptive variable and function names
   - Document all public APIs
   - Write tests for critical paths

3. **Cross-Language Communication**:
   - Use Protocol Buffers for service-to-service communication
   - JSON for REST APIs
   - MessagePack for high-performance scenarios

## Getting Started

1. **Blockchain Development**:
   ```bash
   cd blockchain/elixir
   mix deps.get
   mix test
   ```

2. **Frontend Development**:
   ```bash
   cd frontend/crod-gui
   npm install
   npm run dev
   ```

3. **Service Development**:
   ```bash
   cd services/orchestration
   go build
   ./orchestration
   ```

## Architecture Principles

1. **Microservices**: Each component runs independently
2. **Language Polyglot**: Use the best language for each task
3. **Fault Tolerance**: Built on Elixir/Erlang OTP principles
4. **Scalability**: Horizontal scaling through NATS messaging
5. **Observability**: Comprehensive logging and metrics

## Testing

Each component has its own test suite:

- Elixir: `mix test`
- Rust: `cargo test`
- Python: `pytest`
- Go: `go test`
- JavaScript: `npm test`

Run all tests:
```bash
make test-all
```