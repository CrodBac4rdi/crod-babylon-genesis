# 👨‍💻 Entwicklungsanleitung

<div align="center">
  <img src="../../bilder/vision_vs_reality_20250705_191904.png" alt="Vision vs Reality" width="600"/>
</div>

## Übersicht

Diese Anleitung beschreibt den Entwicklungsprozess für das CROD Clean-Projekt. Sie enthält Informationen zur Einrichtung der Entwicklungsumgebung, zu Coding-Standards und zum Beitragsprozess.

## Entwicklungsumgebung einrichten

### Voraussetzungen

- Node.js 18.x oder höher
- Python 3.10 oder höher
- Rust (neueste stabile Version)
- Docker (für Container-basierte Services)
- Git

### Repository klonen

```bash
git clone https://github.com/username/crod-clean.git
cd crod-clean
```

### Backend-Services einrichten

#### Node.js API Gateway

```bash
cd backend/js
npm install
npm run dev
```

Der Service wird auf Port 3000 gestartet.

#### Python Services

```bash
cd backend/python

# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Chat-Service starten
cd chat
uvicorn app:app --reload --port 5000

# In einem anderen Terminal: Image-Service starten
cd backend/python/images
uvicorn app:app --reload --port 5001
```

#### Rust Code-Execution Service

```bash
cd backend/rust
cargo run
```

Der Service wird auf Port 7000 gestartet.

### Frontend einrichten

#### React Web-Anwendung

```bash
cd frontend/react
npm install
npm start
```

Die Anwendung wird auf Port 8000 gestartet.

#### Tauri Desktop-Anwendung

```bash
cd frontend/tauri
npm install
npm run tauri dev
```

## Entwicklungs-Workflow

### Branching-Strategie

Wir verwenden ein Feature-Branch-Workflow:

- `main`: Produktions-Branch
- `develop`: Entwicklungs-Branch
- `feature/feature-name`: Feature-Branches
- `bugfix/bug-name`: Bugfix-Branches

### Commit-Nachrichten

Wir verwenden konventionelle Commit-Nachrichten:

```
feat: Neue Feature-Beschreibung
fix: Bugfix-Beschreibung
docs: Dokumentationsänderung
style: Formatierungsänderung
refactor: Code-Refactoring
test: Hinzufügen/Ändern von Tests
chore: Build-Prozess oder Tools-Änderung
```

### Pull Requests

- Erstelle einen Pull Request von deinem Feature-Branch zum `develop`-Branch
- Füge eine detaillierte Beschreibung der Änderungen hinzu
- Stelle sicher, dass alle Tests bestanden werden
- Warte auf Code-Review und Genehmigung

## Coding-Standards

### Allgemeine Grundsätze

- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- SOLID-Prinzipien
- Kommentiere komplexe Logik
- Schreibe Tests für alle Funktionen

### Node.js / TypeScript

- Folge dem Airbnb JavaScript Style Guide
- Verwende TypeScript für statische Typisierung
- Nutze async/await statt Promises mit then/catch
- Verwende ESLint und Prettier für konsistente Formatierung

```typescript
// Beispiel für guten TypeScript-Code
interface User {
  id: number;
  name: string;
  email: string;
}

async function getUser(id: number): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const user = await response.json();
    return user;
  } catch (error) {
    console.error(`Error fetching user: ${error}`);
    throw error;
  }
}
```

### Python

- Folge PEP 8 Style Guide
- Verwende Type Hints
- Nutze Black für Formatierung
- Verwende Docstrings für Funktionen und Klassen

```python
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def get_messages(user_id: int, limit: Optional[int] = 100) -> List[Dict]:
    """
    Retrieve messages for a specific user.
    
    Args:
        user_id: The ID of the user to get messages for
        limit: Maximum number of messages to return
        
    Returns:
        A list of message dictionaries
        
    Raises:
        ValueError: If user_id is invalid
    """
    if user_id <= 0:
        logger.error(f"Invalid user ID: {user_id}")
        raise ValueError("User ID must be positive")
        
    # Implementation here
    messages = []  # Fetch from database
    
    return messages[:limit]
```

### Rust

- Folge dem Rust API Guidelines
- Nutze rustfmt für Formatierung
- Verwende Clippy für Linting
- Nutze Result und Option für Fehlerbehandlung

```rust
use std::fs::File;
use std::io::{self, Read};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub api_key: String,
    pub timeout: u32,
}

pub fn read_config(path: &str) -> io::Result<Config> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    
    let config: Config = serde_json::from_str(&contents)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
        
    Ok(config)
}
```

## Testen

### Unit-Tests

- Schreibe Unit-Tests für alle Funktionen
- Verwende Mocks für externe Abhängigkeiten
- Strebe hohe Testabdeckung an

### Integration-Tests

- Teste die Interaktion zwischen Services
- Verwende Docker für integrierte Testumgebungen

### End-to-End-Tests

- Teste komplette Benutzer-Flows
- Automatisiere UI-Tests mit Cypress oder Playwright

## CI/CD

Wir verwenden GitHub Actions für CI/CD:

- Automatisierte Tests für alle Pull Requests
- Automatisierte Linting und Formatierung
- Automatisiertes Deployment auf Staging-Umgebung
- Manuelles Deployment auf Produktionsumgebung

## Dokumentation

- Dokumentiere alle öffentlichen APIs
- Halte die README-Dateien aktuell
- Aktualisiere die Architektur-Dokumentation bei Änderungen

## Fehlerbehandlung und Logging

- Implementiere konsistente Fehlerbehandlung
- Logge relevante Informationen mit angemessenem Level
- Verwende strukturiertes Logging (JSON-Format)

## Performance-Optimierung

- Identifiziere Performance-Bottlenecks
- Implementiere Caching, wo angemessen
- Optimiere Datenbankabfragen
- Verwende Profiling-Tools

## Sicherheitsrichtlinien

- Validiere alle Benutzereingaben
- Verwende Parameterisierte Abfragen für Datenbank
- Halte Abhängigkeiten aktuell
- Führe regelmäßige Sicherheitsaudits durch

## Ressourcen

### Node.js/TypeScript
- [TypeScript Dokumentation](https://www.typescriptlang.org/docs/)
- [Express.js Dokumentation](https://expressjs.com/)

### Python
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Rust
- [Rust Buch](https://doc.rust-lang.org/book/)
- [Actix-Web Dokumentation](https://actix.rs/docs/)

### React
- [React Dokumentation](https://reactjs.org/docs/getting-started.html)
- [React Hooks](https://reactjs.org/docs/hooks-intro.html)

### Tauri
- [Tauri Dokumentation](https://tauri.app/v1/guides/)
