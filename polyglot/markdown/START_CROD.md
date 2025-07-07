# Starting CROD Phoenix

## Quick Start (One Command)

```bash
cd crod-phoenix && mix phx.server
```

That's it! The entire system starts with a single command.

## What Gets Started

When you run `mix phx.server`, the following services automatically start:

1. **Phoenix Web Server** (Port 4000)
   - LiveView Dashboard
   - REST API Endpoints
   - WebSocket Connections

2. **CROD Parasite** (Human-LLM Interpreter)
   - Context Management
   - Memory System
   - Pattern Recognition

3. **Neural Network**
   - Loads from `priv/neural/`
   - Automatic initialization
   - Real-time processing

4. **Polygon City Districts**
   - Orchestrator District
   - Parasite District
   - Neural District

5. **Event Store**
   - PostgreSQL Connection
   - Event Sourcing
   - Read Model Updates

## Prerequisites Check

```bash
# Check Elixir
elixir --version  # Should be 1.15+

# Check PostgreSQL
psql --version    # Should be 14+

# Check NATS (start if needed)
nats-server --version
nats-server -DV  # Start in verbose mode
```

## First Time Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd crod-babylon-genesis/crod-phoenix

# 2. Install dependencies
mix deps.get
mix deps.compile

# 3. Setup database
mix ecto.create
mix ecto.migrate

# 4. Start NATS (in separate terminal)
nats-server

# 5. Start CROD
mix phx.server
```

## Verify Everything is Running

### Check Web Interface
Open browser to: http://localhost:4000

### Check API Health
```bash
curl http://localhost:4000/api/health
```

### Check NATS Connection
```bash
nats pub test.subject "Hello CROD"
```

### Check Neural Network
```bash
curl -X POST http://localhost:4000/api/neural/process \
  -H "Content-Type: application/json" \
  -d '{"input": "ich bins wieder"}'
```

## Environment Options

### Development (Default)
```bash
mix phx.server
```

### Production
```bash
MIX_ENV=prod mix phx.server
```

### Custom Ports
```bash
PORT=8080 mix phx.server
```

### With IEx Shell
```bash
iex -S mix phx.server
```

## Docker Quick Start

```bash
# Build
docker build -t crod-phoenix .

# Run
docker run -p 4000:4000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal/crod_dev \
  -e NATS_URL=nats://host.docker.internal:4222 \
  crod-phoenix
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 4000
lsof -i :4000

# Kill if needed
kill -9 <PID>
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
systemctl status postgresql

# Check connection
psql -U postgres -h localhost
```

### NATS Not Connected
```bash
# Start NATS
nats-server -DV

# Test connection
nats-cli ping
```

## Stop Everything

```bash
# In the terminal running Phoenix
Ctrl+C twice

# Or gracefully
Ctrl+C once, then 'a' for abort
```

## Logs and Monitoring

### View Logs
```bash
# Development logs are in console
# Production logs:
tail -f _build/prod/rel/crod/var/log/erlang.log
```

### LiveDashboard
Visit: http://localhost:4000/dashboard

### Metrics
Visit: http://localhost:4000/metrics

---

That's all! No more complex shell scripts. Just `mix phx.server` and you're running.