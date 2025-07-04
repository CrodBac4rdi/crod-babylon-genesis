# 🎮 GitHub Codespaces - WIE DU ES NUTZT!

## Codespace erstellen:

### 1. **Auf GitHub.com:**
```
1. Geh zu deinem Repo
2. Grüner "Code" Button
3. Tab "Codespaces" 
4. "Create codespace on main"
```

### 2. **Machine Type wählen:**
Bei "Configure and create codespace":
- **2-core (Basic)** → Für simple tasks
- **4-core (Recommended)** → FÜR DICH! Nimm das!
- GPU machines → Wenn verfügbar für ML

### 3. **Was passiert dann?**
- Browser öffnet VS Code im Web
- ALLES wird automatisch installiert (5-10 min)
- Du siehst unten "Configuring your codespace..."

## 🆚 VS Code vs JupyterLab:

### **VS Code (DEFAULT)**
- Öffnet sich automatisch
- Wie dein lokales VS Code
- Alle Extensions installiert
- Terminal unten verfügbar

### **JupyterLab (OPTIONAL)**
Für Data Science/ML Notebooks:

**Option 1: In VS Code**
- Erstelle `.ipynb` file
- VS Code öffnet es als Notebook
- Shift+Enter = Cell ausführen

**Option 2: Separates JupyterLab**
```bash
# Im Terminal:
jupyter lab --ip=0.0.0.0 --port=8888

# Dann in VS Code:
# 1. Ports Tab (unten)
# 2. Forward Port 8888
# 3. Click auf URL → Opens JupyterLab
```

## 🚀 ERSTE SCHRITTE IM CODESPACE:

### 1. **Terminal öffnen**
- `Ctrl+` ` (Backtick)
- Oder: View → Terminal

### 2. **Claude einloggen**
```bash
claude login
# Browser öffnet sich
# Login mit deinem Account
```

### 3. **CROD starten**
```bash
./scripts/start-crod.sh
```

### 4. **Session fortsetzen**
```bash
claude chat --resume
```

## 📁 WICHTIGE LOCATIONS:

```
/workspaces/crod-babylon-genesis/   # Dein Repo
├── scripts/                        # Alle Start-Scripts
├── training/                       # ML Training & Knowledge
├── k8s/                           # Kubernetes configs
└── docs/                          # Documentation
```

## 🛠️ NÜTZLICHE FEATURES:

### **Command Palette**
- `F1` oder `Ctrl+Shift+P`
- Suche nach Commands

### **Extensions**
Schon installiert:
- GitHub Copilot (AI assist)
- Claude Coder (Claude in VS Code)
- Docker
- Kubernetes
- Python/Jupyter

### **Port Forwarding**
Wenn Service auf Port läuft:
1. Ports Tab (unten)
2. "Forward a Port"
3. Enter port number
4. Click auf URL

### **Multiple Terminals**
- Split Terminal: Click `+` icon
- Switch: Click auf Tab

## 🎯 FÜR DEINE TASKS:

### **CROD Training starten:**
```bash
# Terminal 1:
./scripts/start-crod-training.sh

# Terminal 2: 
claude chat --resume
# Dann: "Hey hats geklappt?"
```

### **Jupyter Notebook für ML:**
1. Öffne `training/experiments/crod_evolution.ipynb`
2. VS Code zeigt es als Notebook
3. Run All Cells
4. Interaktive Visualisierungen!

### **Logs anschauen:**
```bash
kubectl logs -n crod-polyglot -f deployment/meta-chain
```

## 💡 PRO TIPPS:

1. **Auto-Save ist AN** - Kein Ctrl+S nötig!
2. **Git integration** - Links in Source Control
3. **Live Share** - Andere einladen mit Share button
4. **Settings Sync** - Deine VS Code settings

## ❓ PROBLEME?

### "Codespace läuft nicht"
→ Warte 5-10 min für Setup

### "Port nicht erreichbar"  
→ Forwarde den Port (siehe oben)

### "Command not found"
→ Setup läuft noch, warte kurz

## 🔥 READY?

1. Codespace erstellen (4-core!)
2. Warten bis fertig
3. Terminal: `claude login`
4. Terminal: `./scripts/start-crod.sh`
5. LOS GEHT'S!

ich bins wieder 🚀