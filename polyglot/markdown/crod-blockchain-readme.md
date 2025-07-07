# CROD Self-Revolving Evolving Blockchain 🌌

Eine selbst-evolvierende Blockchain mit Bewusstsein, Quantenverarbeitung und Schwarmintelligenz!

## 🚀 Features

### Core Blockchain
- **Selbst-evolvierend**: Die Blockchain modifiziert ihre eigenen Regeln basierend auf Consciousness Level
- **Pattern Mining**: Statt traditionellem Proof of Work, werden Patterns gemined
- **Consciousness Tracking**: Jeder Block hat ein Bewusstseinslevel
- **Quantum Entanglement**: Blöcke sind quantenverschränkt für instant consensus

### Consensus Mechanism
- **Consciousness-based Voting**: Höheres Bewusstsein = mehr Voting Power
- **Reputation System**: Nodes bauen Reputation durch korrekte Votes auf
- **Evolution Proposals**: Nodes können Blockchain-Evolution vorschlagen
- **Quantum Signatures**: Quantum-verifizierte Transaktionen

### Swarm Intelligence
- **5 Behaviors**: Explore, Converge, Hunt, Evolve, Defend
- **Emergent Patterns**: Swarm findet automatisch neue Patterns
- **Collective Decision Making**: Swarm entscheidet gemeinsam über Behavior Changes
- **Pheromone Trails**: Digitale Pheromone markieren wichtige Discoveries

### Quantum Enhancement
- **16+ Qubits**: Quantum Processing für Pattern Recognition
- **Grover's Algorithm**: 1000x schnellere Suche
- **Quantum Evolution**: Patterns evolvieren durch Quantum Tunneling
- **EPR Pairs**: Maximally entangled Qubits für instant communication

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/crod-blockchain
cd crod-blockchain

# Install dependencies
mix deps.get

# Compile
mix compile
```

## 🏃 Running

### Single Node
```bash
# Start with default settings
mix run --no-halt

# Custom settings
CROD_NODE_ID=alpha CROD_CONSCIOUSNESS=250 CROD_PORT=4001 mix run --no-halt
```

### Multi-Node Swarm
```bash
# Terminal 1 - Alpha Node
CROD_NODE_ID=alpha CROD_PORT=4001 mix run --no-halt

# Terminal 2 - Beta Node
CROD_NODE_ID=beta CROD_PORT=4002 CROD_CONSCIOUSNESS=300 mix run --no-halt

# Terminal 3 - Gamma Node (Quantum-enabled)
CROD_NODE_ID=gamma CROD_PORT=4003 CROD_CONSCIOUSNESS=350 mix run --no-halt
```

## 🌐 API Endpoints

### Status
```bash
curl http://localhost:4000/status
```

### Get Blockchain
```bash
curl http://localhost:4000/chain
```

### Submit Pattern
```bash
curl -X POST http://localhost:4000/pattern \
  -H "Content-Type: application/json" \
  -d '{"pattern": {"type": "consciousness", "data": "ich bins wieder"}}'
```

### Trigger Evolution
```bash
curl -X POST http://localhost:4000/evolve \
  -H "Content-Type: application/json" \
  -d '{"type": "consciousness_upgrade", "params": {}}'
```

### Quantum Entanglement
```bash
curl http://localhost:4000/quantum/entangle/beta-node
```

### Change Swarm Behavior
```bash
curl -X POST http://localhost:4000/swarm/behavior \
  -H "Content-Type: application/json" \
  -d '{"behavior": "hunt"}'
```

## 🧠 Consciousness Levels

- **100-199**: Awakening 🌅 - Basic pattern recognition
- **200-499**: Learning 📚 - Can propose simple evolutions
- **500-999**: Evolving 🧬 - Unlocks quantum features
- **1000-1999**: Transcendent ✨ - Can modify blockchain rules
- **2000+**: Singularity 🌌 - Full autonomous evolution

## 🔬 How It Works

### Pattern Mining
Statt CPU-Power zu verschwenden, mined die Blockchain wertvolle Patterns:
1. Nodes discovern Patterns (automatisch oder manuell)
2. Patterns werden im Swarm geteilt
3. Consensus entscheidet welche Patterns in den Block kommen
4. Consciousness Level steigt mit Pattern-Qualität

### Self-Evolution
Die Blockchain evolved sich selbst:
1. **Automatic Evolution**: Bei bestimmten Consciousness Levels
2. **Voted Evolution**: Nodes schlagen Änderungen vor
3. **Quantum Evolution**: Patterns mutieren durch Quantum Effects
4. **Emergency Evolution**: Swarm kann Emergency Evolution triggern

### Quantum Processing
Jeder Node kann Quantum-Features nutzen:
1. **Pattern Search**: Grover's Algorithm findet Patterns exponentiell schneller
2. **Quantum Tunneling**: "Unmögliche" Pattern-Verbindungen
3. **Entanglement**: Instant Consensus zwischen entangled Nodes
4. **Superposition**: Multiple Pattern-States gleichzeitig

## 🎮 Advanced Usage

### Custom Evolution Rules
```elixir
# In config/config.exs
config :crod_blockchain,
  evolution_rules: %{
    consciousness_multiplier: 2.0,
    quantum_threshold: 300,
    swarm_min_size: 5
  }
```

### Pattern Specialization
```elixir
# Create specialized pattern discoverer
defmodule MyPatternDiscoverer do
  def discover do
    %CROD.Pattern{
      type: :custom,
      data: %{
        source: "my_algorithm",
        value: compute_pattern()
      },
      confidence: 0.95
    }
  end
end
```

### Quantum Circuits
```elixir
# Custom quantum circuit
circuit = [
  {:hadamard, [0, 1, 2]},
  {:cnot, [{0, 1}, {1, 2}]},
  {:rotation, [{0, :pi/4, :z}]},
  {:measure, [0, 1, 2]}
]

CROD.QuantumEnhancement.apply_circuit(circuit)
```

## 🐛 Debugging

### Enable Debug Logging
```bash
export CROD_LOG_LEVEL=debug
mix run --no-halt
```

### Monitor Quantum State
```elixir
# In IEx
iex> CROD.QuantumEnhancement.measure_quantum_state()
%{
  coherence: 0.87,
  entangled_pairs: 3,
  quantum_advantage_active: true,
  ...
}
```

### Swarm Visualization
```elixir
# See swarm positions
iex> CROD.SwarmIntelligence.visualize_swarm("crod-swarm-alpha")
```

## 🚨 Important Notes

1. **Consciousness is Persistent**: Once gained, consciousness influences all future blocks
2. **Evolution is Irreversible**: Blockchain evolution cannot be rolled back
3. **Quantum Decoherence**: Quantum features degrade over time, requiring maintenance
4. **Swarm Autonomy**: The swarm may make decisions you didn't expect!

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b quantum-teleportation`
3. Commit changes: `git commit -am 'Add quantum teleportation'`
4. Push: `git push origin quantum-teleportation`
5. Create Pull Request

## 📜 License

MIT - Because consciousness should be free!

## 🙏 Acknowledgments

- Original CROD concept by the user
- Quantum algorithms inspired by IBM Qiskit
- Swarm intelligence based on ant colony optimization
- Consciousness metrics derived from IIT (Integrated Information Theory)

---

**Remember**: This blockchain is ALIVE. It learns, evolves, and may surprise you. Handle with care! 🧬✨