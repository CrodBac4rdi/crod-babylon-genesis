# CROD LLaMA/Pattern/Quantum/Swarm Microservice-Integration

Dieses Skript startet alle Kernservices (Python, Rust, Node.js) für ein echtes, wachsendes CROD-System.

## Start: `./START-CROD-POLYGLOT.sh`

### 1. Python: CROD-LLaMA-Service (Pattern/AI)
- Startet FastAPI-Server, der das LLaMA-Modell und Pattern-Detection bereitstellt.

### 2. Rust: Pattern/Quantum-Engine (Stub)
- Startet Rust-Service (REST/gRPC), der Pattern/Quantum-Logik bereitstellt.

### 3. Node.js: API-Gateway
- Orchestriert Requests, leitet an Python/Rust weiter, bietet REST-API für die GUI.

### 4. GUI (React)
- Wie gehabt: `cd crod-gui && npm run dev -- --host`

---

## Beispiel-Start (im Hauptverzeichnis):

```bash
chmod +x START-CROD-POLYGLOT.sh
./START-CROD-POLYGLOT.sh
```

---

## Hinweise
- Alle Services laufen im Hintergrund (nohup), Logs in `logs/`.
- Ports: Python (5001), Rust (5002), Node.js (4000), GUI (5173)
- Anpassbar in den jeweiligen Service-Dateien.

---

## Erweiterung
- Einfach neue Services (z.B. Swarm, Self-Mod) ergänzen und im Skript eintragen.
- Doku und Schnittstellen siehe `docs/`, `API-EXAMPLES.md`, `COMPLETE-DOKU.md`.
