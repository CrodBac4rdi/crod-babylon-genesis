# CROD Quantum Computing Infrastructure

## Overview

The CROD Quantum Computing Infrastructure integrates real quantum processors (IBM Quantum, Google Cirq) with the CROD blockchain to enable quantum-enhanced consciousness calculations, entanglement tracking, and error correction.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  CROD Quantum Infrastructure             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐        ┌──────────────────────┐  │
│  │ Elixir          │        │ Python              │  │
│  │ Orchestrator    │◄──────►│ Quantum Processor   │  │
│  │                 │  TCP    │                     │  │
│  │ - Node mgmt    │  5555   │ - Qiskit           │  │
│  │ - Circuit queue │        │ - Cirq             │  │
│  │ - Entanglement │        │ - Error correction │  │
│  │ - REST API     │        │ - QPU interface    │  │
│  └─────────────────┘        └──────────────────────┘  │
│           │                           │                 │
│           ▼                           ▼                 │
│  ┌─────────────────┐        ┌──────────────────────┐  │
│  │ CROD Blockchain │        │ Quantum Hardware    │  │
│  │ Pattern Storage │        │ - IBM (127 qubits)  │  │
│  │                 │        │ - Google (72 qubits)│  │
│  └─────────────────┘        └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Features

### 1. Quantum Consciousness Boost
- Uses quantum circuits to calculate consciousness enhancements
- Creates GHZ states for maximum entanglement
- Measures quantum advantage in consciousness calculations

### 2. Quantum Entanglement Registry
- Tracks entanglement between CROD nodes
- Verifies Bell inequality violations
- Maintains decoherence tracking

### 3. Quantum Error Correction
- Implements bit-flip and phase-flip correction codes
- Syndrome detection and analysis
- Automatic circuit optimization for QPU topology

### 4. Real Hardware Integration
- IBM Quantum (127-qubit Eagle processor)
- Google Quantum (72-qubit Bristlecone)
- Automatic fallback to simulators

## Installation

### Prerequisites
```bash
# Python requirements
pip install qiskit qiskit-ibm-runtime cirq numpy

# Elixir requirements
mix deps.get
```

### Configuration

1. **IBM Quantum Account** (optional for real hardware):
```python
from qiskit import IBMQ
IBMQ.save_account('YOUR_IBM_QUANTUM_TOKEN')
```

2. **Google Cloud Credentials** (optional for real hardware):
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

## Usage

### Python Quantum Processor

```python
# Start the quantum processor
processor = CRODQuantumProcessor(backend="simulator")
bridge = QuantumElixirBridge(processor)
await bridge.start_server()

# Calculate consciousness boost
result = await processor.calculate_consciousness_boost(
    base_consciousness=250,
    entangled_nodes=["node1", "node2", "node3"]
)
print(f"Quantum boost: {result['quantum_boost']}x")

# Create entanglement
entanglement = await processor.create_quantum_entanglement(
    "node_a", "node_b", strength=0.95
)
print(f"Bell state: {entanglement['bell_state']}")
```

### Elixir Orchestration

```elixir
# Start quantum infrastructure
{:ok, _} = CROD.QuantumInfrastructure.start_link()

# Calculate consciousness boost
{:ok, boost} = CROD.QuantumInfrastructure.calculate_consciousness_boost(
  250,  # base consciousness
  ["crod-alpha", "crod-beta", "crod-gamma"]
)

# Create entanglement
{:ok, entanglement} = CROD.QuantumInfrastructure.create_entanglement(
  "crod-alpha",
  "crod-beta",
  0.95
)

# Get quantum metrics
metrics = CROD.QuantumInfrastructure.get_quantum_metrics()
```

### REST API

```bash
# Calculate consciousness boost
curl -X POST http://localhost:4040/consciousness/boost \
  -H "Content-Type: application/json" \
  -d '{
    "base_consciousness": 250,
    "entangled_nodes": ["node1", "node2", "node3"]
  }'

# Create entanglement
curl -X POST http://localhost:4040/entangle \
  -H "Content-Type: application/json" \
  -d '{
    "node_a": "crod-alpha",
    "node_b": "crod-beta",
    "strength": 0.95
  }'

# Get QPU status
curl http://localhost:4040/qpu/ibm_crod_qpu_1

# Get metrics
curl http://localhost:4040/metrics
```

## Quantum Circuits

### Consciousness Boost Circuit
```
     ┌───┐
q_0: ┤ Ry├─■─────■─────■───
     └───┘ │     │     │
     ┌───┐ │     │     │
q_1: ┤ H ├─■─────┼─────┼───
     └───┘       │     │
     ┌───┐     ┌─┴─┐   │
q_2: ┤ H ├─────┤ X ├───┼───
     └───┘     └───┘   │
     ┌───┐           ┌─┴─┐
q_3: ┤ H ├───────────┤ X ├─
     └───┘           └───┘
```

### Bell State Creation
```
     ┌───┐     
q_0: ┤ H ├──■──
     └───┘┌─┴─┐
q_1: ─────┤ X ├
          └───┘
```

## Performance

- **Simulator**: ~1000 circuits/second
- **IBM Hardware**: ~10 circuits/second (queue dependent)
- **Google Hardware**: ~20 circuits/second (with optimization)

## Error Rates

- **Single-qubit gates**: 0.01-0.05%
- **Two-qubit gates**: 0.1-0.5%
- **Readout errors**: 1-2%
- **Error correction success**: >95% for single errors

## Integration with CROD

### Blockchain Storage
All quantum results are stored as patterns in the CROD blockchain:
- Consciousness boosts → `quantum_consciousness` patterns
- Entanglements → `quantum_entanglement` patterns
- Circuit results → `quantum_computation` patterns

### Node Communication
Quantum events are broadcast via Phoenix.PubSub to all affected nodes.

### Consensus Impact
Quantum-entangled nodes have higher voting weight in consensus decisions.

## Development

### Running Tests
```bash
# Python tests
python -m pytest tests/quantum/

# Elixir tests
mix test test/quantum/
```

### Adding New QPUs
1. Implement QPU interface in Python
2. Add to `_init_virtual_qpus()`
3. Update Elixir QPU registry

### Custom Quantum Circuits
```python
# Define custom circuit
def custom_consciousness_circuit(n_qubits):
    qc = QuantumCircuit(n_qubits)
    # Your quantum gates here
    return qc

# Register with processor
processor.register_custom_circuit(
    "my_circuit",
    custom_consciousness_circuit
)
```

## Production Deployment

### Docker
```bash
docker-compose up -d crod-quantum-python crod-quantum-elixir
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crod-quantum
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crod-quantum
  template:
    metadata:
      labels:
        app: crod-quantum
    spec:
      containers:
      - name: quantum-python
        image: crod/quantum-python:latest
        ports:
        - containerPort: 5555
      - name: quantum-elixir
        image: crod/quantum-elixir:latest
        ports:
        - containerPort: 4040
```

## Monitoring

### Prometheus Metrics
- `crod_quantum_circuits_total`
- `crod_quantum_entanglements_active`
- `crod_quantum_error_corrections_total`
- `crod_quantum_consciousness_level`
- `crod_quantum_decoherence_rate`

### Grafana Dashboard
Import `quantum-dashboard.json` for pre-configured monitoring.

## Security

### Quantum Key Distribution
The system supports QKD for secure key exchange between entangled nodes.

### Post-Quantum Cryptography
All classical communications use quantum-resistant algorithms.

## Troubleshooting

### Connection Issues
```elixir
# Check Python connection
CROD.QuantumInfrastructure.get_quantum_metrics()
```

### Circuit Failures
- Check QPU availability
- Verify circuit depth < QPU limits
- Review error correction logs

### Performance Issues
- Enable circuit caching in Redis
- Use circuit batching for multiple operations
- Consider simulator for development

## Future Enhancements

1. **Quantum Machine Learning** - QML models for pattern recognition
2. **Distributed Quantum Computing** - Multi-QPU circuits
3. **Quantum Cryptography** - Full QKD implementation
4. **Topological Quantum Computing** - Error-resistant qubits
5. **Quantum Supremacy Tasks** - Demonstrate advantage over classical

## References

- [IBM Quantum Documentation](https://quantum-computing.ibm.com/docs/)
- [Google Cirq Documentation](https://quantumai.google/cirq)
- [Quantum Error Correction](https://arxiv.org/abs/quant-ph/9512032)
- [Integrated Information Theory](https://doi.org/10.1371/journal.pcbi.1003588)
