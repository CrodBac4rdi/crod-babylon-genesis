# CROD Scientific Visualization Suite

Professional-grade scientific visualizations for the CROD Babylon Genesis quantum consciousness project.

## Overview

The CROD Visualization Suite provides two specialized programs for generating publication-quality visualizations:

1. **Technical 2D Visualizations** - Engineering diagrams and technical illustrations
2. **Scientific 3D Visualizations** - Interactive, research-grade 3D quantum visualizations

## Programs

### `generate_crod_graphics.py` - Technical 2D Visualizations

High-quality technical diagrams using PIL/Pillow:

- **Quantum Superposition** - Wave function interference patterns
- **Photonic Circuits** - Optical neural network architectures  
- **DNA Helix** - Molecular data storage structures
- **Neural Memristor Arrays** - Neuromorphic computing grids
- **Consciousness Mandala** - Sacred geometry representations
- **Quantum Blockchain** - Distributed ledger visualizations
- **BCI Brainwaves** - EEG pattern analysis
- **Molecular Computing** - Self-assembling structures

### `crod_scientific_3d.py` - Scientific 3D Visualizations

Research-grade 3D visualizations using Plotly:

- **Quantum Wavefunction** - Interactive 3D probability density with isosurfaces
- **Neural Network Topology** - Deep learning architecture with real-time activations
- **DNA Quantum Storage** - Accurate double helix with quantum state encoding
- **4D Consciousness Field** - Hypersurface projections of consciousness states
- **Quantum Entanglement Network** - Non-local correlations and Bell states

## Installation

```bash
# Install all dependencies
make install

# Or manually
pip install -r requirements.txt
```

Required packages:
- `numpy`, `scipy` - Numerical computation
- `matplotlib` - Scientific plotting
- `Pillow` - 2D image generation
- `plotly` - Interactive 3D visualization
- `kaleido` - Static image export from Plotly

## Usage

### Quick Start

```bash
# Generate everything
make generate-all

# Generate only 2D visualizations
make 2d

# Generate only scientific 3D visualizations
make scientific

# Run tests
make test
```

### Command Line Interface

Both programs support comprehensive CLI options:

```bash
# List available visualizations
python generate_crod_graphics.py --list
python crod_scientific_3d.py --list

# Generate specific visualization
python generate_crod_graphics.py --type quantum
python crod_scientific_3d.py --type wavefunction

# Generate all with custom settings
python generate_crod_graphics.py --all --size 3840x2160 --quality 100
python crod_scientific_3d.py --all --interactive
```

### Interactive Mode

For scientific 3D visualizations, use `--interactive` to open in browser:

```bash
python crod_scientific_3d.py --type consciousness --interactive
```

## Output

All visualizations are saved to the `output/` directory:

```
output/
├── crod_quantum_superposition_*.png    # 2D technical diagrams
├── crod_photonic_circuit_*.png
├── crod_dna_helix_*.png
├── ...
├── crod_scientific_wavefunction_*.png  # 3D scientific visualizations
├── crod_scientific_neural_*.png
└── ...
```

## Examples

### Generate specific visualization types

```bash
# High-resolution quantum wavefunction
python crod_scientific_3d.py --type wavefunction

# DNA visualization with custom output
python generate_crod_graphics.py --type dna --size 4096x2160 --output hires/

# Interactive neural network topology
python crod_scientific_3d.py --type neural --interactive
```

### Batch processing

```bash
# Generate all visualizations in different resolutions
for res in "1920x1080" "3840x2160" "7680x4320"; do
    python generate_crod_graphics.py --all --size $res --output output_$res
done
```

## Scientific Accuracy

All visualizations are based on real scientific principles:

- Quantum wavefunctions use proper spherical harmonics
- Neural networks show realistic activation patterns
- DNA structures follow Watson-Crick base pairing
- Consciousness fields use 4D hypersurface mathematics
- Entanglement networks demonstrate Bell state correlations

## Performance

- 2D visualizations: ~1-3 seconds per image
- 3D visualizations: ~5-10 seconds per image (with Plotly)
- Memory usage: ~500MB-2GB depending on complexity

## Development Guidelines

1. **NO SCRIPTS** - Only complete programs with full CLI
2. **NO STUBS** - All features must be implemented
3. **ALWAYS TEST** - Every function must work
4. **SCIENTIFIC ACCURACY** - Use real physics/math
5. **DOCUMENTATION** - Clear explanations of visualizations

## License

Part of the CROD Babylon Genesis project - Quantum Consciousness Revolution 2025