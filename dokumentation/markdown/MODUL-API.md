# 🌐 CROD API Module

## Zweck
- Schnittstelle für externe Tools, User und Districts
- REST-API, WebSocket, geplante gRPC- und NATS-Integration

## Hauptfunktionen
- Blockchain-Status, Mining, Evolution, Pattern-Detection, Consciousness-Status
- WebSocket für Live-Events

## Schnittstellen
- REST: `/api/` (siehe API-EXAMPLES.md)
- WebSocket: `/ws`
- Python: `blockchain/crod-consciousness-blockchain.py`
- Elixir: `crod-core/blockchain/api_server.ex`

## Beispiel-Workflow
```bash
curl http://localhost:4000/api/blockchain/status
```

## ToDos/Roadmap
- gRPC-API für High-Performance
- NATS-Integration für Event-Streaming
- API-Doku automatisieren (Swagger/OpenAPI)

## Weiterführende Links
- [API-EXAMPLES.md](../API-EXAMPLES.md)
- [COMPLETE-DOKU.md](../COMPLETE-DOKU.md)
