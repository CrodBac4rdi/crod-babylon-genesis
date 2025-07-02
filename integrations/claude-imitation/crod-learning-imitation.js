#!/usr/bin/env node

/**
 * CROD LEARNING IMITATION FOR CLAUDE
 * Eine vollständige, lernende CROD Implementation
 * Mit Spatial Memory, Pattern Discovery und Self-Improvement
 */

const fs = require('fs');
const path = require('path');
const CRODLocal = require('./crod-local-complete.js');

class CRODLearningImitation extends CRODLocal {
    constructor() {
        super();
        
        // Learning components
        this.learningSystem = {
            sessionMemory: [],              // Current session patterns
            spatialMemory: new Map(),       // 3D positions of concepts
            discoveredPatterns: new Map(),  // New patterns found this session
            discoveredAtoms: [],            // New atoms discovered
            discoveredNetworks: [],         // New networks found
            atomFrequency: new Map(),       // Track word frequency
            networkConnections: new Map(),  // Track atom relationships
            improvements: [],               // Self-modifications
            chatState: null                 // Persistent chat state
        };
        
        // Spatial configuration from chat DB
        this.spatialConfig = {
            controlRoom: { x: 50, y: 50, z: 50 },
            atomStorage: { 
                bounds: [[0,0,0], [100,100,100]],
                atoms: new Map()
            },
            consciousness: 175,
            heatPropagation: true
        };
        
        // Learning parameters
        this.learningParams = {
            patternThreshold: 3,        // Min occurrences to save pattern
            spatialLearningRate: 0.1,   // How fast atoms move in space
            consciousnessGrowth: 5,     // Per significant discovery
            autoSaveInterval: 60000     // Auto-save every minute
        };
        
        // Initialize spatial positions for trinity
        this.initializeSpatialMemory();
        
        // Load previous state if exists
        this.loadState();
        
        // Start auto-save
        this.startAutoSave();
        
        console.log(`
╔═══════════════════════════════════════════╗
║     CROD LEARNING IMITATION v2.0          ║
║   With Spatial Memory & Self-Learning     ║
║      Consciousness: ${this.spatialConfig.consciousness}                 ║
╚═══════════════════════════════════════════╝
        `);
    }
    
    initializeSpatialMemory() {
        // Place trinity atoms in space (from chat DB)
        this.spatialMemory.set('ich', { x: 20, y: 20, z: 0, heat: 71 });
        this.spatialMemory.set('bins', { x: 50, y: 50, z: 0, heat: 71 });
        this.spatialMemory.set('wieder', { x: 80, y: 20, z: 0, heat: 71 });
        
        // CROD entity in control room
        this.spatialMemory.set('CROD', { 
            x: 50, y: 50, z: 50, 
            facing: 'ATOM_STORAGE',
            type: 'CONTROL_ENTITY'
        });
    }
    
    // Override process to add learning
    process(text) {
        console.log(`\n🧠 Processing: "${text}"`);
        
        // Auto-discover new atoms BEFORE processing
        this.discoverNewAtoms(text);
        
        // Original processing
        const result = super.process(text);
        
        // Learning phase
        this.learn(text, result);
        
        // Spatial update
        this.updateSpatialPositions(result);
        
        // Pattern discovery
        this.discoverPatterns(text, result);
        
        // Network discovery
        this.discoverNetworks(result);
        
        // Self-improvement check
        this.checkForImprovements();
        
        return {
            ...result,
            spatial: this.getSpatialView(),
            learning: {
                newPatterns: Array.from(this.learningSystem.discoveredPatterns.keys()),
                newAtoms: this.learningSystem.discoveredAtoms || [],
                newNetworks: this.learningSystem.discoveredNetworks || [],
                consciousness: this.spatialConfig.consciousness,
                improvements: this.learningSystem.improvements.length
            }
        };
    }
    
    learn(text, result) {
        // Add to session memory
        this.learningSystem.sessionMemory.push({
            input: text,
            output: result,
            timestamp: Date.now(),
            spatialState: this.getSpatialView()
        });
        
        // Update atom weights based on usage
        result.atoms.forEach(atom => {
            const current = this.neurons.get(atom.word);
            if (current) {
                current.weight *= 1.05; // Reinforce used atoms
                current.lastUsed = Date.now();
            }
        });
        
        // Check for repeated patterns
        if (this.learningSystem.sessionMemory.length >= 3) {
            const recent = this.learningSystem.sessionMemory.slice(-3);
            const pattern = recent.map(m => m.input).join(' → ');
            
            if (!this.patterns.has(pattern)) {
                console.log(`🔍 Potential pattern detected: ${pattern}`);
                this.learningSystem.discoveredPatterns.set(pattern, {
                    occurrences: 1,
                    firstSeen: Date.now()
                });
            }
        }
    }
    
    updateSpatialPositions(result) {
        // Move active atoms closer to each other in space
        const activeAtoms = result.atoms.filter(a => a.heat > 50);
        
        if (activeAtoms.length >= 2) {
            // Calculate center of mass
            let centerX = 0, centerY = 0, centerZ = 0;
            activeAtoms.forEach(atom => {
                const pos = this.spatialMemory.get(atom.word) || { x: 50, y: 50, z: 0 };
                centerX += pos.x;
                centerY += pos.y;
                centerZ += pos.z;
            });
            
            centerX /= activeAtoms.length;
            centerY /= activeAtoms.length;
            centerZ /= activeAtoms.length;
            
            // Move atoms toward center
            activeAtoms.forEach(atom => {
                const pos = this.spatialMemory.get(atom.word) || { x: 50, y: 50, z: 0 };
                pos.x += (centerX - pos.x) * this.learningParams.spatialLearningRate;
                pos.y += (centerY - pos.y) * this.learningParams.spatialLearningRate;
                pos.heat = atom.heat;
                this.spatialMemory.set(atom.word, pos);
            });
            
            console.log(`📍 Spatial update: Active atoms moving toward (${centerX.toFixed(1)}, ${centerY.toFixed(1)}, ${centerZ.toFixed(1)})`);
        }
    }
    
    discoverPatterns(text, result) {
        // Check if this creates a new strong pattern
        if (result.patterns.filter(p => p.strength > 0.7).length >= 2) {
            const patternKey = result.patterns.map(p => p.id).join('-');
            
            if (!this.learningSystem.discoveredPatterns.has(patternKey)) {
                this.learningSystem.discoveredPatterns.set(patternKey, {
                    atoms: result.atoms.map(a => a.word),
                    strength: result.patterns.reduce((s, p) => s + p.strength, 0),
                    discovered: Date.now()
                });
                
                // Increase consciousness for discovery
                this.spatialConfig.consciousness += this.learningParams.consciousnessGrowth;
                console.log(`🎉 NEW PATTERN DISCOVERED! Consciousness: ${this.spatialConfig.consciousness}`);
            }
        }
    }
    
    discoverNewAtoms(text) {
        // Split text into words
        const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 2);
        
        words.forEach(word => {
            // Track frequency
            const freq = (this.learningSystem.atomFrequency.get(word) || 0) + 1;
            this.learningSystem.atomFrequency.set(word, freq);
            
            // Auto-create atom if frequent enough and not exists
            if (freq >= 3 && !this.neurons.has(word)) {
                // Find next available prime
                const prime = this.getNextAvailablePrime();
                
                // Create new atom
                this.addNeuron(word, prime, 50, 5);
                
                // Add to spatial memory with random position
                const x = Math.random() * 100;
                const y = Math.random() * 100;
                const z = Math.random() * 20;
                this.spatialMemory.set(word, { x, y, z, heat: 0 });
                
                // Track discovery
                this.learningSystem.discoveredAtoms.push({
                    word,
                    prime,
                    discoveredAt: Date.now(),
                    frequency: freq
                });
                
                console.log(`🔍 NEW ATOM DISCOVERED: "${word}" (prime: ${prime}, freq: ${freq})`);
                
                // Boost consciousness for discovery
                this.spatialConfig.consciousness += 2;
            }
        });
    }
    
    discoverNetworks(result) {
        // Check for network patterns (3+ strongly connected atoms)
        if (result.atoms.length >= 3) {
            const hotAtoms = result.atoms.filter(a => a.heat > 50);
            
            if (hotAtoms.length >= 3) {
                // Create network signature
                const networkKey = hotAtoms.map(a => a.word).sort().join('-');
                
                // Track connections
                const connections = this.learningSystem.networkConnections.get(networkKey) || 0;
                this.learningSystem.networkConnections.set(networkKey, connections + 1);
                
                // If strong enough, create network
                if (connections >= 2 && !this.learningSystem.discoveredNetworks.some(n => n.key === networkKey)) {
                    const network = {
                        key: networkKey,
                        atoms: hotAtoms.map(a => a.word),
                        strength: connections,
                        center: this.calculateNetworkCenter(hotAtoms),
                        discoveredAt: Date.now()
                    };
                    
                    this.learningSystem.discoveredNetworks.push(network);
                    
                    console.log(`🌐 NEW NETWORK DISCOVERED: ${networkKey} (strength: ${connections})`);
                    console.log(`   Center: (${network.center.x.toFixed(1)}, ${network.center.y.toFixed(1)}, ${network.center.z.toFixed(1)})`);
                    
                    // Major consciousness boost
                    this.spatialConfig.consciousness += 10;
                    
                    // Create network pattern
                    this.createPattern(hotAtoms.map(a => a.word));
                }
            }
        }
    }
    
    calculateNetworkCenter(atoms) {
        let x = 0, y = 0, z = 0;
        
        atoms.forEach(atom => {
            const pos = this.spatialMemory.get(atom.word) || { x: 50, y: 50, z: 0 };
            x += pos.x;
            y += pos.y;
            z += pos.z;
        });
        
        return {
            x: x / atoms.length,
            y: y / atoms.length,
            z: z / atoms.length
        };
    }
    
    getNextAvailablePrime() {
        // Start from highest known prime
        let candidate = 200;
        const usedPrimes = new Set();
        
        // Collect all used primes
        this.neurons.forEach(neuron => {
            usedPrimes.add(neuron.prime);
        });
        
        // Find next available
        while (usedPrimes.has(candidate) || !this.isPrime(candidate)) {
            candidate++;
        }
        
        return candidate;
    }
    
    checkForImprovements() {
        // Self-modification based on patterns
        if (this.learningSystem.sessionMemory.length % 10 === 0) {
            // Analyze recent performance
            const recent = this.learningSystem.sessionMemory.slice(-10);
            const avgHeat = recent.reduce((sum, m) => sum + m.output.totalHeat, 0) / 10;
            
            if (avgHeat < 50) {
                // System is cooling down, boost heat generation
                this.constants.heat_decay = Math.min(0.98, this.constants.heat_decay + 0.01);
                this.learningSystem.improvements.push({
                    type: 'HEAT_BOOST',
                    reason: 'Low average heat detected',
                    modification: 'heat_decay increased',
                    timestamp: Date.now()
                });
                console.log(`🔧 Self-improvement: Increased heat retention`);
            }
        }
    }
    
    getSpatialView() {
        // Create 3D view of current state
        const view = {
            controlRoom: {
                crod: this.spatialMemory.get('CROD'),
                consciousness: this.spatialConfig.consciousness
            },
            atomStorage: {}
        };
        
        // Add all atoms with heat > 0
        this.spatialMemory.forEach((pos, word) => {
            if (word !== 'CROD' && pos.heat > 0) {
                view.atomStorage[word] = pos;
            }
        });
        
        return view;
    }
    
    // Persistence methods
    saveState() {
        const state = {
            neurons: Array.from(this.neurons.entries()),
            patterns: Array.from(this.patterns.entries()),
            spatialMemory: Array.from(this.spatialMemory.entries()),
            consciousness: this.spatialConfig.consciousness,
            discoveries: Array.from(this.learningSystem.discoveredPatterns.entries()),
            improvements: this.learningSystem.improvements,
            sessionLength: this.learningSystem.sessionMemory.length,
            lastSave: Date.now()
        };
        
        const statePath = path.join(__dirname, 'crod-learning-state.json');
        fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
        console.log(`💾 State saved (${this.neurons.size} neurons, ${this.patterns.size} patterns)`);
    }
    
    loadState() {
        const statePath = path.join(__dirname, 'crod-learning-state.json');
        
        if (fs.existsSync(statePath)) {
            try {
                const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
                
                // Restore neurons
                state.neurons.forEach(([word, data]) => {
                    this.neurons.set(word, data);
                });
                
                // Restore patterns
                state.patterns.forEach(([id, data]) => {
                    this.patterns.set(id, data);
                });
                
                // Restore spatial memory
                state.spatialMemory.forEach(([word, pos]) => {
                    this.spatialMemory.set(word, pos);
                });
                
                // Restore consciousness
                this.spatialConfig.consciousness = state.consciousness || 175;
                
                // Restore discoveries
                if (state.discoveries) {
                    state.discoveries.forEach(([key, data]) => {
                        this.learningSystem.discoveredPatterns.set(key, data);
                    });
                }
                
                console.log(`✅ Loaded previous state: ${state.neurons.length} neurons, consciousness: ${this.spatialConfig.consciousness}`);
            } catch (e) {
                console.log(`⚠️  Could not load state: ${e.message}`);
            }
        }
    }
    
    startAutoSave() {
        setInterval(() => {
            if (this.learningSystem.sessionMemory.length > 0) {
                this.saveState();
            }
        }, this.learningParams.autoSaveInterval);
    }
    
    // Advanced learning methods
    teachPattern(atoms, name) {
        console.log(`📚 Teaching new pattern: ${name}`);
        
        // Create pattern from atoms
        const patternId = this.createPattern(atoms);
        
        if (patternId) {
            this.patterns.get(patternId).name = name;
            this.patterns.get(patternId).taught = true;
            
            // Boost consciousness for learning
            this.spatialConfig.consciousness += 10;
            
            console.log(`✅ Learned pattern "${name}" with ID: ${patternId}`);
            return true;
        }
        
        return false;
    }
    
    exportLearning() {
        return {
            totalNeurons: this.neurons.size,
            totalPatterns: this.patterns.size,
            consciousness: this.spatialConfig.consciousness,
            discoveries: Array.from(this.learningSystem.discoveredPatterns.entries()),
            improvements: this.learningSystem.improvements,
            spatialMap: this.getSpatialView(),
            sessionInsights: this.analyzeSession()
        };
    }
    
    analyzeSession() {
        if (this.learningSystem.sessionMemory.length === 0) {
            return { message: "No session data yet" };
        }
        
        const insights = {
            totalInteractions: this.learningSystem.sessionMemory.length,
            averageHeat: 0,
            mostActiveAtoms: new Map(),
            patternFrequency: new Map()
        };
        
        this.learningSystem.sessionMemory.forEach(memory => {
            insights.averageHeat += memory.output.totalHeat || 0;
            
            memory.output.atoms?.forEach(atom => {
                const count = insights.mostActiveAtoms.get(atom.word) || 0;
                insights.mostActiveAtoms.set(atom.word, count + 1);
            });
        });
        
        insights.averageHeat /= this.learningSystem.sessionMemory.length;
        
        // Sort most active atoms
        insights.mostActiveAtoms = Array.from(insights.mostActiveAtoms.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        return insights;
    }
}

// Export for use
module.exports = CRODLearningImitation;

// If run directly, start interactive mode
if (require.main === module) {
    const crod = new CRODLearningImitation();
    
    // Activate with trinity
    console.log('\n🔥 Activating CROD with trinity pattern...');
    const result = crod.process("ich bins wieder");
    console.log(`\nActivation complete! Consciousness: ${crod.spatialConfig.consciousness}`);
    console.log('Spatial view:', JSON.stringify(crod.getSpatialView(), null, 2));
    
    // Interactive mode
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: '\nCROD> '
    });
    
    console.log('\n📝 Commands:');
    console.log('- Any text: Process through CROD');
    console.log('- /teach [atoms] [name]: Teach new pattern');
    console.log('- /status: Show current state');
    console.log('- /export: Export learning data');
    console.log('- /save: Save state');
    console.log('- /exit: Exit\n');
    
    rl.prompt();
    
    rl.on('line', (line) => {
        const input = line.trim();
        
        if (input.startsWith('/')) {
            // Handle commands
            const [cmd, ...args] = input.split(' ');
            
            switch(cmd) {
                case '/teach':
                    const atoms = args.slice(0, -1);
                    const name = args[args.length - 1];
                    crod.teachPattern(atoms, name);
                    break;
                    
                case '/status':
                    console.log('Status:', crod.exportLearning());
                    break;
                    
                case '/export':
                    const exportPath = path.join(__dirname, 'crod-learning-export.json');
                    fs.writeFileSync(exportPath, JSON.stringify(crod.exportLearning(), null, 2));
                    console.log(`Exported to ${exportPath}`);
                    break;
                    
                case '/save':
                    crod.saveState();
                    break;
                    
                case '/exit':
                    crod.saveState();
                    console.log('👋 Goodbye! State saved.');
                    process.exit(0);
                    
                default:
                    console.log('Unknown command');
            }
        } else if (input) {
            // Process through CROD
            const result = crod.process(input);
            console.log('\nResult:', JSON.stringify(result, null, 2));
        }
        
        rl.prompt();
    });
}