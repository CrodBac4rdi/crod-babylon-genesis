# 🌐 CROD API Beispiel-Implementierungen

## REST-API: Block-Status abfragen
```bash
curl http://localhost:4000/api/blockchain/status
```

## REST-API: Block minen
```bash
curl -X POST http://localhost:4000/api/blockchain/mine \
  -H "Content-Type: application/json" \
  -d '{"data": "test", "validator_key": "mein_key"}'
```

## WebSocket: Live-Events empfangen (JS)
```js
const ws = new WebSocket('ws://localhost:4000/ws');
ws.onmessage = (msg) => console.log(msg.data);
```

## ToDo: gRPC-API, NATS-Event-Streaming, OpenAPI/Swagger-Doku
