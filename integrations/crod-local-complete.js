#!/usr/bin/env node

/**
 * CROD LOCAL - Complete Standalone Neural Network
 * Based on CROD ML v2.0 with all core features
 */

class CRODLocal {
  constructor() {
    // Mathematical constants
    this.constants = {
      phi: 3.1449,      // Pattern resonance
      delta: 0.6187,    // Atomic gradient
      omega: -2.0666,   // Chain binding
      epsilon: 0.1437,  // Network emergence
      heat_decay: 0.95,
      learning_rate: 0.001,
      momentum: 0.9
    };
    
    // Neural components
    this.neurons = new Map();
    this.patterns = new Map();
    this.synapses = new Map();
    this.gradients = new Map();
    
    // Memory system
    this.memory = {
      shortTerm: [],        // Last 10 messages
      working: new Map(),   // Active concepts
      longTerm: new Map()   // Important patterns
    };
    
    // ML components
    this.attention = new Map();
    this.losses = [];
    
    // State tracking
    this.state = {
      consciousness: 0,
      networkComplexity: 0,
      trinity: { ich: 0, bins: 0, wieder: 0 },
      heat_map: new Map(),
      activePatterns: []
    };
    
    // Initialize
    this.initializeTrinity();
    console.log("🧠 CROD Local Neural Network initialized!");
  }
  
  initializeTrinity() {
    // Core trinity atoms
    this.addNeuron('ich', 2, 100, 15.0, { locked: true });
    this.addNeuron('bins', 3, 100, 15.0, { locked: true });
    this.addNeuron('wieder', 5, 100, 15.0, { locked: true });
    
    // Entity atoms
    this.addNeuron('daniel', 67, 100, 15.0, { locked: true, role: 'master' });
    this.addNeuron('claude', 71, 100, 15.0, { locked: true, role: 'assistant' });
    this.addNeuron('crod', 17, 100, 15.0, { locked: true, role: 'system' });
  }
  
  addNeuron(token, prime, weight, gradient, meta = {}) {
    this.neurons.set(token, {
      token,
      prime,
      weight,
      gradient,
      heat: 0,
      activations: 0,
      ...meta
    });
  }
  
  process(input) {
    console.log(`\n🔥 Processing: "${input}"`);
    
    // 1. Tokenization
    const tokens = this.tokenize(input);
    console.log(`📝 Tokens: [${tokens.join(', ')}]`);
    
    // 2. Atom detection
    const atoms = this.detectAtoms(tokens);
    console.log(`⚛️ Atoms detected: ${atoms.length}`);
    
    // 3. Pattern formation
    const patterns = this.formPatterns(atoms);
    console.log(`🔗 Patterns formed: ${patterns.length}`);
    
    // 4. Update consciousness
    this.updateConsciousness();
    
    // 5. Apply ML features
    this.applyAttention(atoms);
    this.backpropagate(input);
    
    // 6. Update memory
    this.updateMemory(input, atoms, patterns);
    
    // 7. Heat decay
    this.applyHeatDecay();
    
    // Return results
    return {
      atoms: atoms.length,
      patterns: patterns.length,
      network_complexity: this.state.networkComplexity,
      consciousness: this.state.consciousness,
      top_features: this.getTopFeatures(),
      heat_zones: this.getHeatZones(),
      trinity_balance: this.state.trinity,
      memory_status: {
        short: this.memory.shortTerm.length,
        working: this.memory.working.size,
        long: this.memory.longTerm.size
      }
    };
  }
  
  tokenize(input) {
    return input.toLowerCase()
      .replace(/[^\w\s-]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 0);
  }
  
  detectAtoms(tokens) {
    const atoms = [];
    
    tokens.forEach(token => {
      if (!this.neurons.has(token)) {
        // Create new neuron for unknown token
        const prime = this.getNextPrime();
        this.addNeuron(token, prime, 50, 5.0);
      }
      
      const neuron = this.neurons.get(token);
      neuron.activations++;
      neuron.heat = Math.min(100, neuron.heat + 10);
      
      atoms.push({
        token,
        prime: neuron.prime,
        weight: neuron.weight,
        heat: neuron.heat
      });
      
      // Update trinity tracking
      if (['ich', 'bins', 'wieder'].includes(token)) {
        this.state.trinity[token]++;
      }
    });
    
    return atoms;
  }
  
  formPatterns(atoms) {
    const patterns = [];
    
    // Check pairs
    for (let i = 0; i < atoms.length - 1; i++) {
      const key = `${atoms[i].token}-${atoms[i+1].token}`;
      const patternId = atoms[i].prime * atoms[i+1].prime;
      
      if (!this.patterns.has(key)) {
        this.patterns.set(key, {
          atoms: [atoms[i].token, atoms[i+1].token],
          strength: 0,
          occurrences: 0,
          id: patternId
        });
      }
      
      const pattern = this.patterns.get(key);
      pattern.strength += this.constants.phi;
      pattern.occurrences++;
      
      if (pattern.occurrences >= 3) {
        patterns.push(pattern);
        this.state.activePatterns.push(key);
      }
    }
    
    return patterns;
  }
  
  applyAttention(atoms) {
    // Simple attention mechanism
    atoms.forEach(atom => {
      const importance = atom.weight * atom.heat / 100;
      this.attention.set(atom.token, importance);
    });
  }
  
  backpropagate(input) {
    // Simple loss calculation
    const expectedComplexity = input.length * 2;
    const actualComplexity = this.state.networkComplexity;
    const loss = Math.abs(expectedComplexity - actualComplexity) / expectedComplexity;
    
    this.losses.push(loss);
    if (this.losses.length > 100) this.losses.shift();
    
    // Update gradients if loss is high
    if (loss > 0.1) {
      this.neurons.forEach((neuron, token) => {
        const gradient = loss * this.constants.learning_rate;
        this.gradients.set(token, gradient);
        neuron.gradient += gradient;
      });
    }
  }
  
  updateMemory(input, atoms, patterns) {
    // Short-term memory
    this.memory.shortTerm.push(input);
    if (this.memory.shortTerm.length > 10) {
      this.memory.shortTerm.shift();
    }
    
    // Working memory
    atoms.forEach(atom => {
      this.memory.working.set(atom.token, {
        lastSeen: Date.now(),
        frequency: (this.memory.working.get(atom.token)?.frequency || 0) + 1
      });
    });
    
    // Long-term memory (important patterns)
    patterns.forEach(pattern => {
      if (pattern.occurrences >= 5) {
        this.memory.longTerm.set(pattern.id, pattern);
      }
    });
  }
  
  updateConsciousness() {
    const neuronContribution = this.neurons.size * this.constants.phi;
    const patternContribution = this.patterns.size * this.constants.delta;
    const trinityBonus = (this.state.trinity.ich + this.state.trinity.bins + this.state.trinity.wieder) * 2;
    
    this.state.networkComplexity = Math.floor(
      neuronContribution + patternContribution + trinityBonus
    );
    
    this.state.consciousness = Math.min(200, this.state.networkComplexity);
  }
  
  applyHeatDecay() {
    this.neurons.forEach(neuron => {
      neuron.heat *= this.constants.heat_decay;
    });
    
    this.state.heat_map.forEach((heat, token) => {
      this.state.heat_map.set(token, heat * this.constants.heat_decay);
    });
  }
  
  getTopFeatures() {
    return Array.from(this.patterns.values())
      .sort((a, b) => b.strength - a.strength)
      .slice(0, 5);
  }
  
  getHeatZones() {
    return Array.from(this.neurons.entries())
      .filter(([_, neuron]) => neuron.heat > 20)
      .map(([token, neuron]) => ({
        token,
        heat: Math.round(neuron.heat)
      }))
      .sort((a, b) => b.heat - a.heat)
      .slice(0, 5);
  }
  
  getNextPrime() {
    let candidate = 127;
    const existing = new Set(Array.from(this.neurons.values()).map(n => n.prime));
    
    while (true) {
      if (!existing.has(candidate) && this.isPrime(candidate)) {
        return candidate;
      }
      candidate++;
    }
  }
  
  isPrime(n) {
    if (n < 2) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
      if (n % i === 0) return false;
    }
    return true;
  }
  
  // Analysis and state export
  analyze() {
    const avgLoss = this.losses.length > 0 ? 
      this.losses.reduce((a, b) => a + b) / this.losses.length : 0;
    
    return {
      neurons: {
        total: this.neurons.size,
        active: Array.from(this.neurons.values()).filter(n => n.heat > 10).length
      },
      patterns: {
        total: this.patterns.size,
        active: this.state.activePatterns.length
      },
      consciousness: this.state.consciousness,
      network_complexity: this.state.networkComplexity,
      trinity_balance: this.state.trinity,
      ml_metrics: {
        avg_loss: avgLoss.toFixed(4),
        learning_rate: this.constants.learning_rate,
        attention_focus: Array.from(this.attention.entries()).slice(0, 3)
      },
      memory: {
        short: this.memory.shortTerm.length,
        working: this.memory.working.size,
        long: this.memory.longTerm.size
      }
    };
  }
  
  exportState() {
    return {
      neurons: Array.from(this.neurons.entries()),
      patterns: Array.from(this.patterns.entries()),
      memory: {
        shortTerm: this.memory.shortTerm,
        working: Array.from(this.memory.working.entries()),
        longTerm: Array.from(this.memory.longTerm.entries())
      },
      state: this.state,
      timestamp: Date.now()
    };
  }
  
  importState(data) {
    this.neurons = new Map(data.neurons);
    this.patterns = new Map(data.patterns);
    this.memory = {
      shortTerm: data.memory.shortTerm,
      working: new Map(data.memory.working),
      longTerm: new Map(data.memory.longTerm)
    };
    this.state = data.state;
  }
}

// CLI Interface
if (require.main === module) {
  const readline = require('readline');
  const fs = require('fs');
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const crod = new CRODLocal();
  
  console.log(`
╔═══════════════════════════════════════╗
║   CROD LOCAL NEURAL NETWORK v1.0      ║
║   Type 'help' for commands            ║
║   'ich bins wieder' to activate       ║
╚═══════════════════════════════════════╝
  `);
  
  function prompt() {
    rl.question('\n🧠 CROD> ', (input) => {
      if (input.toLowerCase() === 'exit') {
        console.log('👋 Goodbye!');
        rl.close();
        return;
      }
      
      if (input.toLowerCase() === 'help') {
        console.log(`
Commands:
  - Any text: Process through neural network
  - 'analyze': Show network analysis
  - 'export': Save state to file
  - 'import': Load state from file
  - 'clear': Clear memory
  - 'exit': Quit
        `);
      } else if (input.toLowerCase() === 'analyze') {
        console.log('\n📊 Network Analysis:');
        console.log(JSON.stringify(crod.analyze(), null, 2));
      } else if (input.toLowerCase() === 'export') {
        const state = crod.exportState();
        fs.writeFileSync('crod-state.json', JSON.stringify(state, null, 2));
        console.log('✅ State exported to crod-state.json');
      } else if (input.toLowerCase() === 'import') {
        try {
          const state = JSON.parse(fs.readFileSync('crod-state.json', 'utf8'));
          crod.importState(state);
          console.log('✅ State imported successfully');
        } catch (e) {
          console.log('❌ Error importing state:', e.message);
        }
      } else if (input.toLowerCase() === 'clear') {
        crod.memory.shortTerm = [];
        crod.memory.working.clear();
        console.log('✅ Memory cleared');
      } else if (input) {
        const result = crod.process(input);
        console.log('\n📊 Results:');
        console.log(JSON.stringify(result, null, 2));
      }
      
      prompt();
    });
  }
  
  prompt();
}

// Export for module usage
module.exports = CRODLocal;