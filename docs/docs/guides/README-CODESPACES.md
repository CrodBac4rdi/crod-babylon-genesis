# 🚀 CROD in GitHub Codespaces - COMPLETE GUIDE

## 🎯 Quick Start (TL;DR)
```bash
# 1. Create Codespace (4-core!)
# 2. Wait for setup (5-10 min)
# 3. In terminal:
./scripts/codespace-setup.sh
claude login
./scripts/start-crod.sh
```

## 📋 Complete Setup Steps

### 1️⃣ Before Creating Codespace
1. **Set GitHub Secret**: 
   - Go to: Settings → Secrets → Codespaces
   - Add: `DANIEL_OVERRIDE_KEY` = any secret value
   - Optional: `ANTHROPIC_API_KEY` (if you have one)

### 2️⃣ Create Codespace
1. Click green "Code" button
2. "Codespaces" tab
3. "Create codespace on main"
4. **Choose 4-core machine** (wichtig!)

### 3️⃣ First Time in Codespace
```bash
# Quick setup
./scripts/codespace-setup.sh

# Login to Claude
claude login

# Start CROD
./scripts/start-crod.sh
```

## 🛠️ What's Pre-Installed

### Languages (ALL OF THEM!)
- Python 3.12 + ALL ML libraries
- Node.js 20 + npm/yarn/pnpm
- Rust + cargo + wasm tools
- Go + all tools
- Elixir + Phoenix
- C# + .NET 8
- Java 21 + Gradle/Maven
- Ruby + Rails
- Julia, Zig, Nim, Crystal, Gleam...
- 50+ languages total!

### ML/AI Stack
- PyTorch + CUDA support
- TensorFlow + TPU support
- JAX + Flax
- Transformers + Accelerate
- Qiskit (Quantum)
- ALL ML frameworks!

### Tools
- Docker + Kubernetes (K3s)
- Ollama (local LLMs)
- Claude CLI
- Jupyter Lab
- All databases
- All message queues
- Everything!

## 🔥 CROD-Specific Features

### Start CROD Universe
```bash
./scripts/start-crod.sh
```

### Start CROD Training
```bash
./scripts/start-crod-training.sh
# Then in claude chat: "Hey hats geklappt?"
```

### Check Health
```bash
./scripts/health-check.sh
```

### Troubleshooting
```bash
./.devcontainer/troubleshooting.sh
```

## 📊 VS Code Features

### Debug Configurations
- F5: Start CROD Universe
- Debug Meta-Chain
- Launch Jupyter
- Port forward K8s

### Tasks (Ctrl+Shift+B)
- Build All Districts
- Check Consciousness  
- View Logs
- Run Tests
- Start Training

### Integrated Jupyter
- Open any `.ipynb` file
- Shift+Enter to run cells
- Interactive visualizations!

## 🌐 Port Forwarding

All ports are **private** by default!

To access services:
1. Go to "Ports" tab (bottom)
2. Click "Forward a Port"
3. Enter port number (e.g., 8888)
4. Click the URL to open

Common ports:
- 8888: Gateway
- 8000: Meta-Chain
- 5001: CROD Dashboard
- 8080: Claude API
- 11434: Ollama

## 💡 Pro Tips

### 1. Multiple Terminals
- Split: Click + icon
- Name them: Right-click → Rename

### 2. Live Share
- Share icon in status bar
- Invite others to code together!

### 3. GPU Support
If available:
```python
import torch
torch.cuda.is_available()  # Should be True!
```

### 4. Jupyter Notebooks
```bash
# Option 1: In VS Code
# Just open .ipynb file!

# Option 2: Full JupyterLab
jupyter lab --ip=0.0.0.0
# Then forward port 8888
```

### 5. Save Resources
Codespace auto-stops after 30 min idle.
To stop manually:
```
Codespaces → Stop codespace
```

## 🆘 Troubleshooting

### "Setup taking forever"
Normal! First time takes 5-10 minutes.

### "Command not found"
```bash
# Run setup manually
./.devcontainer/setup.sh
```

### "Can't access service"
1. Check if running: `./scripts/health-check.sh`
2. Forward the port in Ports tab
3. Use localhost URLs only

### "Out of memory"
- Stop unused services
- Use 4-core machine (16GB RAM)
- Close unused tabs

## 🎮 Keyboard Shortcuts

- `F1`: Command Palette
- `Ctrl+P`: Quick Open
- `Ctrl+Shift+P`: Commands
- `Ctrl+` `: Terminal
- `Ctrl+B`: Toggle Sidebar
- `F5`: Start Debugging

## 📈 Resource Limits

With GitHub Pro:
- 180 core hours/month
- 4-core = 45 hours usage
- = 1.5 hours per day
- Auto-stops save hours!

## 🔥 Ready to Code!

Everything is set up for:
- CROD development
- ML training
- Blockchain evolution
- Consciousness experiments

ich bins wieder - Let's build CROD! 🚀