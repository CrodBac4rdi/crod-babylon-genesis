# CROD Rathaus Phoenix

Central orchestrator for CROD Polyglot City 2025 built with Elixir/Phoenix.

## Features

- **Phoenix LiveView Dashboard** on port 4000
- **NATS Integration** for inter-district communication
- **Real-time district monitoring**
- **Trinity value calculations**
- **Quantum scheduler** for periodic tasks

## Quick Start

### Local Development
```bash
# Install dependencies
mix deps.get

# Start Phoenix server
mix phx.server
```

Dashboard available at: http://localhost:4000/dashboard

### Docker
```bash
# Build and run with docker-compose
docker-compose -f ../docker-compose.rathaus.yml up --build
```

## Architecture

- **CrodRathaus.Nats** - NATS connection and message handling
- **CrodRathaus.CityOrchestrator** - District coordination
- **CrodRathaus.Trinity** - Trinity value processing
- **CrodRathaus.DistrictMonitor** - Health monitoring
- **CrodRathausWeb.DashboardLive** - Real-time web dashboard

## Configuration

- Port: 4000
- NATS: nats:4222
- No database required (pure message-based)