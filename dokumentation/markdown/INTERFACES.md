# Schnittstellen & Komponenten-Übersicht

## Übersicht

- **blockchain/**: Kern-Blockchain-Logik (Elixir, Python, Rust)
- **crod-core/**: Subsysteme (game_theory, neural, quantum, self_modification)
- **crod-gui/**: Web-Frontend (React, Vite)
- **integrations/**: Anbindung externer KI/Services
- **k8s/**: Kubernetes-Deployments

## Schnittstellen

### REST API
- Pfad: `/api/`
- Siehe API-EXAMPLES.md für Beispiele

### WebSocket
- Pfad: `/ws` (z.B. für Live-Events)

### Datenbank
- Postgres (mit PostGIS), Redis, NATS

### Interne Kommunikation
- gRPC, HTTP, Message-Broker (NATS)

## Hinweise
- Details zu Endpunkten und Datenformaten siehe Quellcode und API-EXAMPLES.md
- Änderungen an Schnittstellen bitte dokumentieren!
