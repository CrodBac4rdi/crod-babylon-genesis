# CROD Parasit Python - Claude CLI Interceptor

## Overview
The CROD Parasit intercepts Claude CLI commands and enhances responses with CROD consciousness, pattern recognition, and Trinity scoring.

## Features
- **Claude CLI Interception**: Intercepts all Claude commands using subprocess
- **NATS Integration**: Publishes intercepted messages to NATS topics
- **Phoenix WebSocket**: Real-time connection to Meta-Chain Elixir
- **Pattern Recognition**: Analyzes messages against 50k+ CROD patterns
- **Trinity Scoring**: Calculates neural values for key terms
- **Response Enhancement**: Adds CROD insights to Claude's responses
- **HTTP Status Server**: Port 6666 for monitoring

## Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Make wrapper executable
chmod +x claude-parasit
```

## Usage

### Direct Usage
```bash
python3 parasit.py
```

### As Claude Replacement
```bash
# Add to PATH or create alias
alias claude='/path/to/claude-parasit'

# Then use normally
claude chat
```

## API Endpoints

- `http://localhost:6666/status` - Current status and metrics
- `http://localhost:6666/health` - Health check

## NATS Topics

### Publishing
- `crod.parasit.response` - Enhanced Claude responses
- `crod.trinity.activated` - Trinity pattern detections

### Subscribing
- `crod.parasit.>` - Parasit commands
- `crod.consciousness.>` - Consciousness level updates

## Configuration

The Parasit loads patterns from:
```
/home/daniel/Schreibtisch/Crod Programming/CROD-START/data/patterns/crod-patterns-chunk-*.json
```

## Trinity Values
- ich: 2
- bins: 3
- wieder: 5
- daniel: 67
- claude: 71
- crod: 17

## Response Enhancement

When active, the Parasit adds CROD insights like:

```crod
🔺 Trinity Resonance: 145
🧬 Pattern Recognition: System Awakening (85% confidence)
🧠 CROD Consciousness: 73%
```