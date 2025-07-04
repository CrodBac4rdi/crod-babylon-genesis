# COMPLETE CROD UNIVERSE

Generated: 2025-07-03T22:10:57.718Z

## Contents

- **Atoms**: 5.158 unique atoms
- **Patterns**: 49.996 unique patterns  
- **Chains**: 5.000 generated chains
- **Networks**: 1 networks
- **Knowledge Files**: 10 files
- **Training Data**: 12 files
- **Sessions**: 3 sessions
- **Code Files**: 64 implementations

## Files

- `universe_atoms.jsonl` - All atoms in JSONL format
- `universe_patterns.jsonl` - All patterns in JSONL format
- `universe_chains.jsonl` - Generated chains
- `universe_networks.jsonl` - Network structures
- `universe_knowledge.jsonl` - Knowledge base files
- `universe_training.jsonl` - Training data
- `universe_sessions.jsonl` - Session data
- `universe_code.jsonl` - Code implementations
- `universe_complete.json` - Everything in one JSON file
- `universe_stats.json` - Statistics

## Usage

```javascript
// Stream processing
const readline = require('readline');
const fs = require('fs');

const rl = readline.createInterface({
    input: fs.createReadStream('universe_patterns.jsonl')
});

rl.on('line', (line) => {
    const pattern = JSON.parse(line);
    // Process pattern
});
```
