# CROD API Beispiele

Hier findest du Beispielanfragen für die wichtigsten Schnittstellen.

## REST API (Beispiel)

### Block abfragen
```http
GET /api/block/{id}
```

### Transaktion senden
```http
POST /api/transaction
Content-Type: application/json
{
  "from": "...",
  "to": "...",
  "amount": 42
}
```

## WebSocket (Beispiel)

- Verbinde dich mit: `ws://localhost:4000/ws`
- Nachrichtenformat: JSON

## Hinweise
- Authentifizierung ggf. per Token
- Siehe weitere Details in der README.md und im Quellcode
