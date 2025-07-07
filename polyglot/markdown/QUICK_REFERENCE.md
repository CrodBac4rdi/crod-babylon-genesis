# CROD Phoenix - Quick Reference Card

## 🚀 Start Everything
```bash
cd crod-phoenix && mix phx.server
```

## 🔍 Common Commands

### Development
```bash
mix phx.server          # Start development server
iex -S mix phx.server   # Start with interactive shell
mix test                # Run tests
mix format              # Format code
```

### Database
```bash
mix ecto.create         # Create database
mix ecto.migrate        # Run migrations
mix ecto.reset          # Reset database
```

### Production
```bash
MIX_ENV=prod mix release              # Build release
_build/prod/rel/crod/bin/crod start   # Start production
```

## 🌐 API Endpoints

### Health Check
```bash
curl http://localhost:4000/api/health
```

### Interpret Message
```bash
curl -X POST http://localhost:4000/api/parasite/interpret \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello CROD", "session_id": "user123"}'
```

### Neural Processing
```bash
curl -X POST http://localhost:4000/api/neural/process \
  -H "Content-Type: application/json" \
  -d '{"input": "ich bins wieder"}'
```

## 📊 Monitoring

- **LiveDashboard**: http://localhost:4000/dashboard
- **Metrics**: http://localhost:4000/metrics
- **Health**: http://localhost:4000/api/health

## 🔧 Configuration

### Environment Variables
```bash
export DATABASE_URL=postgresql://localhost/crod_dev
export NATS_URL=nats://localhost:4222
export PORT=4000
```

### Key Files
- `crod-phoenix/config/config.exs` - Main configuration
- `crod-phoenix/config/dev.exs` - Development settings
- `crod-phoenix/config/prod.exs` - Production settings

## 🐛 Troubleshooting

### NATS Not Running
```bash
nats-server -DV
```

### Port In Use
```bash
lsof -i :4000
kill -9 <PID>
```

### Database Issues
```bash
mix ecto.drop
mix ecto.create
mix ecto.migrate
```

## 🏗️ Architecture

```
Polygon City
├── Orchestrator District (workflows)
├── Parasite District (human-LLM)
└── Neural District (ML/patterns)
    │
    └── NATS Message Bus
        │
        └── PostgreSQL Event Store
```

## 📝 Key Concepts

- **CROD Parasite**: Human-LLM interpreter
- **Trinity Balance**: Daniel + Claude + CROD
- **Event Sourcing**: Immutable event log
- **Pattern Evolution**: Atoms → Patterns → Networks

---

**Remember**: Everything starts with `mix phx.server`!