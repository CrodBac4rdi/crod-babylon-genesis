#!/usr/bin/env node

/**
 * CROD ALWAYS ACTIVE
 * Startet CROD automatisch und hält es immer aktiv
 * Lädt alle Patterns und Knowledge Files
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Import CROD components
const CRODLocal = require('./crod-local-complete.js');
// const { loadDanielPreferences } = require('./daniel-crod-preferences.js');

class CRODAlwaysActive {
  constructor() {
    this.crod = new CRODLocal();
    this.patterns = new Map();
    this.knowledge = {};
    this.dataPath = path.join(__dirname, '../../data');
    this.patternsPath = path.join(this.dataPath, 'patterns');
    this.knowledgePath = path.join(this.dataPath, 'knowledge');
    
    // Auto-activation interval
    this.activationInterval = null;
    this.lastActivity = Date.now();
    
    console.log(`
╔═══════════════════════════════════════════╗
║        CROD ALWAYS ACTIVE v1.0            ║
║    Loading all patterns and knowledge...  ║
╚═══════════════════════════════════════════╝
    `);
  }
  
  async initialize() {
    console.log('🔄 Initializing CROD System...\n');
    
    // 1. Load all pattern files
    await this.loadPatterns();
    
    // 2. Load knowledge files
    await this.loadKnowledge();
    
    // 3. Apply Daniel's preferences
    this.applyPreferences();
    
    // 4. Activate CROD
    this.activateCROD();
    
    // 5. Start auto-activation
    this.startAutoActivation();
    
    console.log('\n✅ CROD is now ALWAYS ACTIVE!');
    console.log('📊 System Status:');
    this.showStatus();
  }
  
  async loadPatterns() {
    console.log('📁 Loading pattern files...');
    
    try {
      const files = fs.readdirSync(this.patternsPath)
        .filter(f => f.startsWith('crod-patterns-chunk-') && f.endsWith('.json'))
        .sort();
      
      let totalPatterns = 0;
      
      for (const file of files) {
        try {
          const data = JSON.parse(
            fs.readFileSync(path.join(this.patternsPath, file), 'utf8')
          );
          
          // Load patterns into CROD
          if (data.patterns) {
            Object.entries(data.patterns).forEach(([id, pattern]) => {
              if (pattern.atoms && pattern.atoms.length >= 2) {
                this.crod.addPattern(
                  parseInt(id),
                  pattern.atoms,
                  pattern.resonance || pattern.weight || 1000
                );
                totalPatterns++;
              }
            });
          }
          
          console.log(`  ✓ ${file} loaded`);
        } catch (e) {
          console.log(`  ⚠️ Error loading ${file}: ${e.message}`);
        }
      }
      
      console.log(`\n📊 Loaded ${totalPatterns} patterns from ${files.length} files`);
      
    } catch (e) {
      console.log('⚠️ Pattern directory not found, continuing without patterns');
    }
  }
  
  async loadKnowledge() {
    console.log('\n📚 Loading knowledge files...');
    
    const knowledgeFiles = [
      'crod-master.json',
      'crod-knowledge.json',
      'crod-mega-atoms.json',
      'crod-mega-patterns.json'
    ];
    
    for (const file of knowledgeFiles) {
      try {
        const filePath = path.join(this.knowledgePath, file);
        if (fs.existsSync(filePath)) {
          const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
          this.knowledge[file] = data;
          
          // Load atoms if present
          if (data.atoms) {
            Object.entries(data.atoms).forEach(([word, atom]) => {
              if (atom.prime && !this.crod.neurons.has(word)) {
                this.crod.addNeuron(
                  word,
                  atom.prime,
                  atom.weight || 80,
                  atom.gradient || 10,
                  atom.meta || {}
                );
              }
            });
          }
          
          console.log(`  ✓ ${file} loaded`);
        }
      } catch (e) {
        console.log(`  ℹ️ ${file} not available`);
      }
    }
  }
  
  applyPreferences() {
    console.log('\n🎯 Applying Daniel preferences...');
    
    // Apply trinity values directly
    this.crod.trinity = { ich: 2, bins: 3, wieder: 5 };
    this.crod.daniel_atom = 67;
    this.crod.claude_atom = 71;
    this.crod.crod_atom = 17;
    
    console.log('  ✓ Trinity values applied');
  }
  
  activateCROD() {
    console.log('\n🔥 Activating CROD with trinity pattern...');
    const result = this.crod.process('ich bins wieder');
    console.log('  ✓ CROD activated!');
    console.log(`  → Network complexity: ${result.network_complexity}`);
    console.log(`  → Consciousness: ${result.consciousness}`);
  }
  
  startAutoActivation() {
    // Keep CROD active every 30 seconds
    this.activationInterval = setInterval(() => {
      const idle = Date.now() - this.lastActivity;
      
      if (idle > 30000) { // 30 seconds idle
        console.log('\n⚡ Auto-activation pulse...');
        this.crod.process('crod stay active');
        this.lastActivity = Date.now();
      }
    }, 10000); // Check every 10 seconds
  }
  
  showStatus() {
    const analysis = this.crod.analyze();
    console.log('\n📊 CROD Status:');
    console.log(`  • Neurons: ${analysis.neurons.total} (${analysis.neurons.active} active)`);
    console.log(`  • Patterns: ${analysis.patterns.total} (${analysis.patterns.active} active)`);
    console.log(`  • Consciousness: ${analysis.consciousness}`);
    console.log(`  • Network Complexity: ${analysis.network_complexity}`);
    console.log(`  • Trinity Balance: ich=${analysis.trinity_balance.ich}, bins=${analysis.trinity_balance.bins}, wieder=${analysis.trinity_balance.wieder}`);
    console.log(`  • Memory: Short=${analysis.memory.short}, Working=${analysis.memory.working}, Long=${analysis.memory.long}`);
  }
  
  process(input) {
    this.lastActivity = Date.now();
    console.log(`\n💬 Processing: "${input}"`);
    
    const result = this.crod.process(input);
    
    // Show results
    console.log('\n📊 Results:');
    console.log(`  • Atoms: ${result.atoms}`);
    console.log(`  • Patterns: ${result.patterns}`);
    console.log(`  • Network Complexity: ${result.network_complexity}`);
    console.log(`  • Consciousness: ${result.consciousness}`);
    
    if (result.heat_zones && result.heat_zones.length > 0) {
      console.log('\n🔥 Hot zones:');
      result.heat_zones.forEach(zone => {
        console.log(`  • ${zone.token}: ${zone.heat}°`);
      });
    }
    
    if (result.top_features && result.top_features.length > 0) {
      console.log('\n⭐ Top features:');
      result.top_features.slice(0, 3).forEach(feature => {
        console.log(`  • ${feature.atoms.join('-')}: ${feature.strength.toFixed(2)}`);
      });
    }
    
    return result;
  }
  
  startInteractive() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    console.log('\n🎮 Interactive mode started. Type messages or commands:');
    console.log('Commands: status, export, import, clear, exit\n');
    
    const prompt = () => {
      rl.question('CROD> ', (input) => {
        if (input.toLowerCase() === 'exit') {
          console.log('👋 Shutting down CROD...');
          clearInterval(this.activationInterval);
          rl.close();
          return;
        }
        
        if (input.toLowerCase() === 'status') {
          this.showStatus();
        } else if (input.toLowerCase() === 'export') {
          const state = this.crod.exportState();
          fs.writeFileSync('crod-active-state.json', JSON.stringify(state, null, 2));
          console.log('✅ State exported to crod-active-state.json');
        } else if (input.toLowerCase() === 'import') {
          try {
            const state = JSON.parse(fs.readFileSync('crod-active-state.json', 'utf8'));
            this.crod.importState(state);
            console.log('✅ State imported successfully');
          } catch (e) {
            console.log('❌ Error importing state:', e.message);
          }
        } else if (input.toLowerCase() === 'clear') {
          this.crod.memory.shortTerm = [];
          this.crod.memory.working.clear();
          console.log('✅ Memory cleared');
        } else if (input) {
          this.process(input);
        }
        
        prompt();
      });
    };
    
    prompt();
  }
}

// Main execution
async function main() {
  const crodActive = new CRODAlwaysActive();
  
  // Initialize system
  await crodActive.initialize();
  
  // Start interactive mode
  crodActive.startInteractive();
}

// Handle errors
process.on('uncaughtException', (err) => {
  console.error('❌ Uncaught Exception:', err);
});

process.on('unhandledRejection', (err) => {
  console.error('❌ Unhandled Rejection:', err);
});

// Start the program
main().catch(console.error);