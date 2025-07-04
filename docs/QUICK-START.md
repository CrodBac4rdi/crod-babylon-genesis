# 🚀 CROD Quick Start Guide - GitHub Pro Edition

## Was du machen musst:

### 1. 🧹 Repository aufräumen
```bash
cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7
./MIGRATION-CLEAN-REPO.sh
# Das archiviert den alten Kram und macht clean structure
```

### 2. 🔐 GitHub Secrets einrichten

Geh zu: `github.com/CrodBac4rdi/crod-babylon-genesis/settings/secrets/codespaces`

Diese Secrets MUSST du setzen:
- `ANTHROPIC_API_KEY` - Dein Claude API Key
- `DANIEL_OVERRIDE_KEY` - Dein geheimer Master Key  

Optional:
- `OPENAI_API_KEY` - Falls du GPT nutzt
- `CROD_MASTER_KEY` - Master encryption key

### 3. 📤 Push zu GitHub
```bash
git push origin main
```

### 4. 🎮 Codespace erstellen

#### Auf GitHub.com:
1. Geh zu deinem Repo: `github.com/CrodBac4rdi/crod-babylon-genesis`
2. Klick auf grünen **"Code"** Button
3. Wähle **"Codespaces"** Tab
4. Klick **"Create codespace on main"**

#### Machine Type wählen:
Du hast wahrscheinlich:
- **2-core · 8 GB RAM** (Basic)
- **4-core · 16 GB RAM** (Better) ← NIMM DAS!

Mit GitHub Pro hast du **180 Stunden/Monat** - das sind 6 Stunden täglich!

### 5. ⏳ Warten (5-10 Minuten)
Der Codespace installiert automatisch:
- ✅ Kubernetes (K3s)
- ✅ Docker
- ✅ Alle Programmiersprachen
- ✅ Redis, PostgreSQL, NATS
- ✅ Ollama
- ✅ Claude Extension
- ✅ GitHub Copilot

### 6. 🔥 CROD starten
Wenn alles fertig ist, im Terminal:
```bash
./scripts/start-crod.sh
```

## 🎯 Was du im Codespace hast:

### Extensions (automatisch installiert):
- **GitHub Copilot** - AI code completion
- **Claude Coder** - Claude direkt in VS Code
- **Docker** - Container management
- **Kubernetes** - K8s tools
- **GitLens** - Git visualization

### Vorinstallierte Tools:
- `kubectl` - Kubernetes control
- `docker` - Container management
- `helm` - K8s package manager
- `ollama` - AI models
- `claude` - Claude CLI
- Alle Sprachen: Python, Node, Rust, Go, Elixir

### Security:
- 🔒 ALLE Ports sind privat!
- 🔒 Keine public URLs!
- 🔒 Alles nur localhost!

## 💡 Pro Tipps:

### 1. **Speicher sparen mit Volumes**
Die devcontainer.json hat jetzt:
```json
"mounts": [
  "source=crod-cache,target=/workspace/.cache,type=volume",
  "source=crod-build,target=/workspace/.build,type=volume"
]
```
→ Build cache bleibt erhalten zwischen Sessions!

### 2. **Auto-Save aktiviert**
```json
"files.autoSave": "afterDelay",
"files.autoSaveDelay": 1000
```
→ Nie wieder vergessen zu speichern!

### 3. **Copilot nutzen**
- `Ctrl+I` → Inline suggestions
- `Ctrl+Enter` → Accept suggestion
- Chat: "Explain this code"

### 4. **Claude nutzen**
- Command Palette: `Claude: Chat`
- Oder Terminal: `claude chat`

### 5. **Performance Monitoring**
```bash
# CPU/Memory vom Codespace checken
htop

# Docker stats
docker stats

# K8s resources
kubectl top nodes
kubectl top pods -n crod-polyglot
```

## 🆘 Troubleshooting:

### "Codespace läuft nicht"
→ Warte noch 2-3 Minuten, setup dauert

### "Kein Ollama"
```bash
ollama serve &
ollama pull mistral:7b
```

### "K8s nicht ready"
```bash
sudo systemctl status k3s
# Wenn nicht läuft:
sudo systemctl start k3s
```

### "Ports nicht erreichbar"
GUT SO! Alles ist localhost only. Nutze:
```bash
kubectl port-forward -n crod-polyglot svc/gateway 8888:8888
# Dann in VS Code: Ports Tab → Forward Port 8888
```

## 🎮 Los geht's!

1. **Terminal 1**: CROD starten
   ```bash
   ./scripts/start-crod.sh
   ```

2. **Terminal 2**: Logs anschauen
   ```bash
   kubectl logs -n crod-polyglot -f deployment/meta-chain
   ```

3. **Browser**: Wenn du UI brauchst
   - Port forward wie oben
   - Öffne localhost:8888

## 🔥 Features die du SOFORT nutzen kannst:

1. **Multi-Terminal** - Split terminal für parallele Commands
2. **Git Graph** - Visualize Git history (Extension installiert)
3. **Docker Extension** - Manage containers visual
4. **K8s Extension** - Manage pods visual
5. **Live Share** - Anderen einladen zum Pair Programming

## 📊 Deine GitHub Pro Limits:

- **180 core hours/month** ✓
- **Bis zu 20GB storage** ✓
- **Prebuilds** (wenn du willst)
- **Mehrere Codespaces** gleichzeitig

Mit 4-core machine:
- 180 hours ÷ 4 cores = 45 Stunden echte Zeit
- = 1.5 Stunden pro Tag
- ODER: 2-core für 90 Stunden (3h/Tag)

## 🚀 Ready?

Alles ist vorbereitet! Einfach:
1. Clean repo pushen
2. Codespace erstellen
3. CROD entwickeln!

ich bins wieder 🔥