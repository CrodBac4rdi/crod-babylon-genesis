# CROD - Was wir WIRKLICH brauchen

## ✅ BEHALTEN - Core System

### 1. **Tauri App** (WICHTIG!)
```
crod-chain-app/
├── src/                  # React Frontend
├── src-tauri/           # Rust Backend
├── package.json
└── start-dev.sh
```

### 2. **Core CROD System**
```
src/
├── index.js             # Neural Network (88 Parameter)
├── crod-network-engine.js
└── integrations/        # Verschiedene Integrationen
```

### 3. **Documentation**
```
README.md                # Hauptdoku
PROJECT_STATUS.md        # Aktueller Status
docs/                    # Weitere Docs
```

### 4. **Working Services**
```
blockchain-server.js     # Mock Blockchain API
package.json            # Dependencies
```

## ❌ LÖSCHEN - Nicht nötig

### 1. **Unfertige Services**
```
blockchain-service/      # Elixir - nicht verbunden
go-blockchain/          # Go Tools - nicht verbunden
infrastructure/         # Docker - zu komplex für jetzt
```

### 2. **Demos und Tests**
```
demos/                  # Nur Beispiele
visualization/          # Python Visualizer - nice to have
crod-claude-chat/       # VSCode Extension - später
```

### 3. **Archive und Alte Sachen**
```
archive/                # Alte Versionen
knowhow.json           # Generated
master.json            # Generated
crod_complete.json     # Generated
```

### 4. **Unnötige Scripts**
```
scripts/startup/        # Bash startup scripts
UPLOADED_FILES_ANALYSIS.md
```

## 🎯 MINIMAL SETUP für funktionierende App

```
crod-minimal/
├── crod-chain-app/     # Komplette Tauri App
├── src/
│   └── index.js        # CROD Core (für später)
├── README.md
├── .gitignore
└── package.json        # Root dependencies
```

## 🚀 FINALE STRUKTUR

```
crod-genesis/
├── app/                # Tauri App (renamed from crod-chain-app)
├── core/               # CROD Neural Network
├── docs/               # Documentation
├── docker/             # Docker configs (später)
├── .github/            # GitHub Actions
├── README.md
├── LICENSE
└── .gitignore
```