# CROD Docker Infrastructure

## Overview

Consolidated Docker configuration for all CROD services.

## Structure

```
docker/
├── services/           # Service-specific Dockerfiles
│   ├── Dockerfile.base      # Base Elixir image with common dependencies
│   ├── Dockerfile.master    # Master orchestrator service
│   ├── Dockerfile.memory    # Memory management service
│   ├── Dockerfile.neural    # Neural network bridge service
│   ├── Dockerfile.pattern   # Pattern discovery service
│   ├── Dockerfile.quantum   # Quantum computing service
│   └── Dockerfile.timetravel # Time-travel debugging service
├── compose/            # Docker Compose configurations
│   ├── docker-compose.yml       # Main services
│   └── docker-compose.dev.yml   # Development overrides
└── scripts/            # Docker utility scripts

## Services

### Base Image (`Dockerfile.base`)
- Elixir 1.14
- Erlang/OTP 25
- Common dependencies for all services
- Health check utilities

### Master Orchestrator (`Dockerfile.master`)
- Extends base image
- Includes orchestration-specific dependencies
- NATS client libraries
- Service discovery tools

### Memory Service (`Dockerfile.memory`)
- Redis client libraries
- Memory optimization tools
- Caching mechanisms

### Neural Bridge (`Dockerfile.neural`)
- Python interop libraries
- TensorFlow/PyTorch bindings
- Neural network runtime

### Pattern Discovery (`Dockerfile.pattern`)
- Mathematical libraries
- Pattern recognition algorithms
- Data analysis tools

### Quantum Service (`Dockerfile.quantum`)
- Quantum simulation libraries
- Cryptographic tools
- Quantum algorithm implementations

### Time-Travel Service (`Dockerfile.timetravel`)
- Event sourcing libraries
- State reconstruction tools
- Debugging utilities

## Usage

### Build Individual Service

```bash
# Build base image
docker build -f services/Dockerfile.base -t crod/base:latest .

# Build specific service
docker build -f services/Dockerfile.neural -t crod/neural:latest .
```

### Build All Services

```bash
# Use the build script
./scripts/build-all.sh
```

### Run Services

```bash
# Development environment
docker-compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml up

# Production environment
docker-compose -f compose/docker-compose.yml up -d
```

## Best Practices

1. Always extend from `Dockerfile.base` for consistency
2. Use multi-stage builds to minimize image size
3. Pin dependency versions for reproducibility
4. Include health checks in all service images
5. Use `.dockerignore` to exclude unnecessary files

## Environment Variables

Common environment variables used across services:

- `CROD_ENV` - Environment (development/production)
- `CROD_NODE_NAME` - Unique node identifier
- `NATS_URL` - NATS server connection string
- `REDIS_URL` - Redis connection string
- `LOG_LEVEL` - Logging verbosity