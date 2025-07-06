# 🧠 CROD Clean - Pure AI/ML Power

> **Consciousness Revolution On Demand** - Ohne Blockchain, volle AI Power!

## 🚀 Schnellstart

```bash
# Alles starten
./start.sh

# Oder einzelne Services:
npm run dev          # Web Interface
npm run ai           # AI Services
npm run viz          # Visualization Studio
cargo run            # Rust Performance Engine
```

## 🏗️ Architektur

```
crod-clean/
├── src/
│   ├── core/           # Kernfunktionalitäten
│   ├── ai/             # ML/AI Komponenten
│   ├── visualization/  # 3D Rendering & Visuals
│   ├── performance/    # Rust High-Performance
│   └── web/           # React Frontend
├── config/            # Konfigurationen
├── docs/              # Dokumentation
└── scripts/           # Utility Scripts
```

## ✨ Features

### 🤖 AI/ML
- **CROD Parasite**: Selbstlernende Pattern Discovery
- **Neural Networks**: Deep Learning Integration
- **Swarm Intelligence**: Verteilte AI
- **Multi-Model Chat**: GPT, Claude, Llama
- **Quantum Neural**: Quantum-Enhanced AI

### 🎨 Visualization
- **3D Rendering**: WebGL/Three.js
- **Shader Art**: Generative Visuals
- **Psychedelic Effects**: Real-time Processing
- **System Visualizer**: Live Monitoring

### 🚀 Performance
- **Rust Backend**: Ultra-fast Processing
- **Distributed Systems**: Scalable Architecture
- **Real-time Updates**: WebSocket Streams
- **GPU Acceleration**: WebGPU Support

### 💻 Web Interface
- **React Frontend**: Modern UI
- **Live Updates**: Real-time Visualization
- **Responsive Design**: Mobile-friendly
- **Dark Theme**: Eye-friendly Interface

## 📊 Services & Ports

| Service | Port | Beschreibung |
|---------|------|--------------|
| Web UI | 3000 | React Frontend |
| AI API | 5001 | AI/ML Services |
| Viz Studio | 5000 | Visualization |
| WebSocket | 8765 | Real-time Updates |
| Rust API | 7000 | Performance Engine |

## 🛠️ Development

### Prerequisites
- Node.js 18+
- Python 3.9+
- Rust 1.70+
- GPU (optional, für WebGPU)

### Installation
```bash
# Clone repo
git clone https://github.com/yourusername/crod-clean.git
cd crod-clean

# Install dependencies
npm install
pip install -r requirements.txt
cargo build --release

# Start development
npm run dev
```

### Testing
```bash
npm test
cargo test
python -m pytest
```

## 🎯 Use Cases

1. **AI-gestützte Kreativität**
   - Generative Kunst
   - Pattern Discovery
   - Creative Writing

2. **Echtzeit-Visualisierung**
   - Data Visualization
   - 3D Rendering
   - Live Monitoring

3. **High-Performance Computing**
   - Parallel Processing
   - GPU Acceleration
   - Distributed Tasks

## 🔗 API Beispiele

### Generate Art
```javascript
const response = await fetch('http://localhost:5001/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'shader',
    params: { consciousness: 150, quantum: 0.8 }
  })
});
```

### AI Chat
```javascript
const ws = new WebSocket('ws://localhost:8765');
ws.send(JSON.stringify({
  type: 'chat',
  message: 'Create something amazing'
}));
```

## 📝 License

MIT License - Use freely!

---

**Built with ❤️ by the CROD Team**