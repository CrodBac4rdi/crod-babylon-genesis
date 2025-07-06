# 📚 API-Dokumentation

<div align="center">
  <img src="../../assets/svg/tech-stack-overview.svg" alt="Tech Stack" width="500"/>
</div>

## Übersicht

Die CROD Clean-Architektur stellt verschiedene APIs bereit, die es ermöglichen, mit den verschiedenen Services zu kommunizieren. Diese Dokumentation enthält detaillierte Informationen zu allen verfügbaren APIs.

## API-Gateway (Node.js)

Der zentrale API-Gateway-Service stellt einen einheitlichen Zugangspunkt zu allen Backend-Services bereit.

### Basis-URL

```
http://localhost:3000/api
```

### Authentifizierung

Die meisten API-Endpunkte erfordern eine Authentifizierung. Die Authentifizierung erfolgt über einen JWT-Token, der im Authorization-Header übergeben wird:

```
Authorization: Bearer <token>
```

### Verfügbare Endpunkte

#### Chat-Service

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/chat/messages` | GET | Abrufen aller Chat-Nachrichten |
| `/chat/messages` | POST | Senden einer neuen Chat-Nachricht |
| `/chat/models` | GET | Abrufen aller verfügbaren Chat-Modelle |

#### Code-Execution-Service

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/code/execute` | POST | Ausführung von Code |
| `/code/languages` | GET | Abrufen aller unterstützten Programmiersprachen |

#### Image-Service

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/images/generate` | POST | Generierung eines Bildes |
| `/images/gallery` | GET | Abrufen aller generierten Bilder |

## WebSocket-API

Für Echtzeit-Kommunikation stellt CROD Clean eine WebSocket-API bereit.

### Verbindungsaufbau

```javascript
const socket = new WebSocket('ws://localhost:3000/ws');
```

### Verfügbare Events

| Event | Richtung | Beschreibung |
|-------|----------|--------------|
| `chat-message` | Server → Client | Neue Chat-Nachricht |
| `code-result` | Server → Client | Ergebnis einer Code-Ausführung |
| `image-generated` | Server → Client | Neues generiertes Bild |

## Python-Services (direkte APIs)

Die Python-Services stellen auch direkte APIs bereit, die unabhängig vom API-Gateway verwendet werden können.

### Chat-Service

```
http://localhost:5000/api
```

### Image-Service

```
http://localhost:5001/api
```

## Rust Code-Execution Service (direkte API)

```
http://localhost:7000/api
```

## API-Beispiele

### Chat-Nachricht senden

```javascript
fetch('http://localhost:3000/api/chat/messages', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    model: 'claude-3',
    message: 'Wie kann ich ein React-Komponente erstellen?'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Code ausführen

```javascript
fetch('http://localhost:3000/api/code/execute', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    language: 'python',
    code: 'print("Hello, World!")'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Bild generieren

```javascript
fetch('http://localhost:3000/api/images/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    prompt: 'Ein futuristisches Raumschiff im Orbit eines Planeten',
    style: 'realistic',
    size: '512x512'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```
