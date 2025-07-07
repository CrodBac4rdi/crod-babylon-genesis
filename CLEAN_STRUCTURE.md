# SAUBERE ORDNERSTRUKTUR FÜR CROD

```
crod-babylon-genesis/
├── src/                      # Source Code
│   ├── core/                # Kern-System
│   │   ├── neural/         # Neural Network
│   │   ├── parasite/       # Parasite System
│   │   └── trinity/        # Trinity System
│   │
│   ├── districts/           # Polyglot Districts
│   │   ├── elixir/         # Rathaus
│   │   ├── rust/           # Pattern District
│   │   ├── python/         # Intelligence Hub
│   │   ├── go/             # Memory Quarter
│   │   └── javascript/     # Gateway
│   │
│   └── shared/             # Gemeinsame Komponenten
│       ├── configs/        # Konfigurationen
│       ├── utils/          # Utilities
│       └── types/          # Type Definitions
│
├── scripts/                 # Ausführbare Scripts
│   ├── install/            # Installation
│   ├── start/              # Start Scripts
│   └── tools/              # Entwickler Tools
│
├── docs/                    # Dokumentation
│   ├── architecture/       # Architektur Diagramme
│   ├── api/                # API Dokumentation
│   └── guides/             # Anleitungen
│
├── tests/                   # Tests
│   ├── unit/               # Unit Tests
│   ├── integration/        # Integration Tests
│   └── e2e/                # End-to-End Tests
│
├── docker/                  # Docker Files
│   ├── images/             # Docker Images
│   └── compose/            # Docker Compose
│
├── .github/                 # GitHub Actions
├── .env.example            # Environment Template
├── README.md               # Hauptdokumentation
└── package.json            # Node Dependencies
```

## WAS WOHIN GEHÖRT:

### /src/core/
- CROD.js → neural/
- crod_parasite*.py → parasite/
- Trinity logic → trinity/

### /src/districts/
- Jede Sprache in eigenen Ordner
- Klare Trennung der Services

### /scripts/
- Alle .sh files
- Start/Stop/Install Scripts

### /docs/
- Alle .md files
- SVG Diagramme
- API Specs

### GELÖSCHT WERDEN:
- CROD-FLAT/ (alles nach src/)
- claude_crazy/archive/ (unnötiger Ballast)
- Duplicate files
- Old reports
- Session files