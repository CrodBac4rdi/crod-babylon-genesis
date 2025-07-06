# 🐳 CROD Infrastructure

Complete Docker infrastructure for running the CROD Blockchain ecosystem.

## 🚀 Quick Start

```bash
# Start everything
./start-crod-stack.sh

# Or manually with docker-compose
docker-compose up -d
```

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Web Interface  │────▶│  Blockchain API  │────▶│   PostgreSQL    │
│   (Port 4000)   │     │   (Port 8001)    │     │   (Port 5432)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                         │
         └───────────┬───────────┘                        │
                     │                                     │
              ┌──────▼──────┐                             │
              │    NATS     │                             │
              │ (Port 4222) │                             │
              └─────────────┘                             │
                     │                                     │
         ┌───────────┴───────────┐                       │
         │                       │                        │
    ┌────▼─────┐          ┌─────▼──────┐                │
    │  Redis   │          │ Prometheus │◀────────────────┘
    │(Port 6379)          │(Port 9090) │
    └──────────┘          └────────────┘
                                 │
                          ┌──────▼──────┐
                          │   Grafana   │
                          │ (Port 3000) │
                          └─────────────┘
```

## 📦 Services

| Service | Port | Description |
|---------|------|-------------|
| **Web Interface** | 4000 | Blockchain viewer and dashboard |
| **Blockchain API** | 8001 | Elixir blockchain REST API |
| **PostgreSQL** | 5432 | Database for persistence |
| **Redis** | 6379 | Caching and pub/sub |
| **NATS** | 4222 | Message bus |
| **Prometheus** | 9090 | Metrics collection |
| **Grafana** | 3000 | Metrics visualization |

## 🛠️ Management

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f blockchain-api

# Stop everything
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart a service
docker-compose restart blockchain-api

# Scale a service
docker-compose up -d --scale blockchain-api=3
```

## 🔧 Configuration

### Environment Variables
Edit `docker-compose.yml` to change:
- Database credentials
- Service ports
- Resource limits

### Monitoring
- Prometheus config: `prometheus.yml`
- Grafana dashboards: `grafana-dashboards/`

## 📊 Monitoring

1. **Grafana**: http://localhost:3000
   - Username: `admin`
   - Password: `crod2025`

2. **Prometheus**: http://localhost:9090
   - Query metrics directly

3. **NATS Monitor**: http://localhost:8222
   - Real-time message bus stats

## 🚨 Troubleshooting

```bash
# Check container status
docker-compose ps

# Check container health
docker inspect crod-blockchain-api | grep -A 5 Health

# View recent logs
docker-compose logs --tail=50

# Access container shell
docker-compose exec blockchain-api sh

# Reset everything
docker-compose down -v
docker-compose up -d
```

## 🔐 Security Notes

- All services run in isolated network
- External ports can be restricted in production
- Use secrets management for credentials
- Enable TLS for production deployment

## 🚀 Production Deployment

For production:
1. Use `.env` file for secrets
2. Enable SSL/TLS
3. Configure firewall rules
4. Set resource limits
5. Enable backups for volumes