# CROD Data Directory

This directory contains the core knowledge base for CROD's neural network.

## Structure

```
data/
├── patterns/        # Pattern chunks (JSON)
├── atoms/          # Atomic knowledge units (JSON)
├── knowledge/      # Consolidated knowledge bases
├── chains/         # Blockchain data
└── models/         # Trained model files
```

## Data Statistics

- **Patterns**: 100,187 total (50 files)
- **Atoms**: 10,916 total (6 files)
- **Chains**: 10,000 entries
- **Knowledge Bases**: Multiple domains

## Pattern Format

```json
{
  "id": "pattern_12345",
  "atoms": ["ich", "bins", "wieder"],
  "weight": 100,
  "category": "trinity",
  "connections": ["pattern_12346"],
  "metadata": {
    "created": "2025-01-01",
    "frequency": 1000
  }
}
```

## Atom Format

```json
{
  "id": "atom_ich",
  "value": "ich",
  "trinity_value": 2,
  "frequency": 50000,
  "associations": ["bins", "wieder", "daniel"]
}
```

## Loading Data

Data is loaded automatically by:
1. CROD Core neural network on startup
2. Pattern District for matching
3. Intelligence Hub for training

## Data Sources

- Original training conversations
- Pattern analysis results
- User interactions
- Self-generated patterns

## Privacy

All data is anonymized and contains no personal information beyond the CROD system context.

## Compression

Large pattern files are stored in chunks to optimize loading:
- `crod-patterns-chunk-0.json` through `crod-patterns-chunk-49.json`
- Each chunk contains ~2000 patterns

## Updates

Data is versioned and can be updated through:
1. Training new patterns
2. Importing knowledge bases
3. Self-learning from interactions