# CROD Technology Research - Januar 2025

## 🐳 Docker & Kubernetes

### Port Forwarding vs NodePort - THE TRUTH!
- **kubectl port-forward**: NUR für Development/Debugging!
  - Nicht persistent
  - Stirbt wenn Terminal zu
  - NICHT für Production!
  
- **NodePort** (wie unser 30889): 
  - Persistent
  - Für externe Zugriffe gedacht
  - Mit Load Balancer kombinierbar
  
**WIR HABEN DIE GANZE ZEIT PORT-FORWARD GEMACHT OBWOHL WIR NODEPORT HABEN!**

### Best Practices 2025:
- Port-Forward nur für schnelle Tests
- NodePort nur mit Gateway/Load Balancer
- Production: LoadBalancer Service oder Ingress Controller
- Security: Immer nur 127.0.0.1 exposen bei port-forward

## 🔮 Elixir/Phoenix für CROD

### Phoenix LiveView 1.0 (2025)
- Real-time UI ohne JavaScript
- Server-side rendering mit WebSocket updates
- Millionen concurrent connections möglich

### Warum Elixir für Meta-Chain?
- **Erlang VM**: Millionen lightweight processes
- **Fault Tolerance**: Let it crash philosophy
- **Perfect für Orchestration**: Actor model built-in
- **Hot Code Swapping**: Updates ohne Downtime

### Microservices in Elixir:
- Phoenix für monolithische Apps
- Boundary für Module-Grenzen
- RabbitMQ/Commanded für Service Communication
- GenServer = perfekt für State Management

## 🔴 Redis Patterns

### Pub/Sub Best Practices:
1. **Channel Naming**: 
   - `district:name:event` (z.B. `district:pattern:detected`)
   - `crod:global:activation`

2. **Message Format**:
   ```json
   {
     "from": "service-name",
     "type": "event-type",
     "data": {},
     "timestamp": 1234567890
   }
   ```

3. **Patterns für CROD**:
   - Fan-out: Meta-Chain → Alle Districts
   - Fan-in: Alle Districts → Meta-Chain
   - Event Sourcing: Alle Events speichern

## 🏗️ Architektur-Learnings

### Monolith vs Microservices (für CROD):
- **Monolith**: Einfacher, schneller zu entwickeln
- **Microservices**: Skalierbar, fault-isolated
- **CROD Polyglot**: Hybrid! Verschiedene Sprachen für verschiedene Stärken

### Service Mesh (Zukunft?):
- Istio/Linkerd für Service-to-Service Communication
- Automatic retries, circuit breaking
- Observability built-in

## 🚀 Was wir WIRKLICH brauchen:

### 1. **Ingress Controller** statt NodePort
- Nginx Ingress oder Traefik
- Automatic SSL/TLS
- Path-based routing

### 2. **Message Queue** statt nur Redis Pub/Sub
- RabbitMQ oder Kafka für guaranteed delivery
- Event Sourcing für CROD History

### 3. **Service Discovery**
- Consul oder Kubernetes native
- Districts finden sich automatisch

### 4. **Observability Stack**
- Prometheus + Grafana für Metrics
- Jaeger für Distributed Tracing
- ELK Stack für Logs

## 📝 TODOs für CROD:

1. **NodePort 30889 nutzen** - kein port-forward mehr!
2. **Phoenix Channels** in Meta-Chain für WebSocket
3. **gRPC** zwischen Districts (statt HTTP)
4. **NATS** als Message Bus evaluieren
5. **Helm Charts** für deployment

## 🧠 Key Insights:

> "Port-forward ist wie mit Klebeband debuggen - funktioniert, ist aber nicht die Lösung!"

> "Elixir's Actor Model IST bereits ein Neural Network - Neuronen sind GenServers!"

> "Redis Pub/Sub ist gut, aber ohne Persistence verlieren wir Messages"

---
*Research Stand: 3. Januar 2025*