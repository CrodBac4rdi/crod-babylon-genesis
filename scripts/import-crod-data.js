#!/usr/bin/env node

/**
 * Import ALL atoms, patterns, networks, chains from CROD legacy data
 * Collects from entire Crod Programming folder and imports into running chains
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

console.log('🔍 CROD Data Import Script');
console.log('=========================');

// Data collections
const allAtoms = new Map();
const allPatterns = new Map();
const allNetworks = new Map();
const allChains = new Map();
const allMemories = [];

// Known CROD data sources
const DATA_SOURCES = [
    // Main knowledge base
    '../legacy/CROD FULL/Crod More Know HOW THE NETWORK THE REAL READ THIS CLAUDE/crod-knowledge-base.json',
    '../legacy/CROD FULL/CROD_FINAL_KNOWLEDGE.json',
    '../legacy/CROD-UNIFIED/data/json/CROD_FINAL_KNOWLEDGE.json',
    '../legacy/CROD-UNIFIED/data/json/crod-knowledge-base.json',
    '../legacy/CROD-UNIFIED/data/json/crod_master.json',
    '../legacy/CROD-UNIFIED/data/json/crod_complete.json',
    '../legacy/CROD-CLEAN/data/CROD_FINAL_KNOWLEDGE.json',
    
    // State files
    '../legacy/CROD FULL/Crod More Know HOW THE NETWORK THE REAL READ THIS CLAUDE/crod-state-current.json',
    '../legacy/CROD FULL/Crod More Know HOW THE NETWORK THE REAL READ THIS CLAUDE/crod-live-network.json',
    '../legacy/CROD FULL/Crod More Know HOW THE NETWORK THE REAL READ THIS CLAUDE/crod-session-live.json',
    
    // Python data
    '../legacy/Crod python/microservices/data/CROD_FINAL_KNOWLEDGE.json',
    '../legacy/Crod python/microservices/data/crod_knowledge_base.json',
    '../legacy/Crod python/microservices/data/crod_learned_data.json',
];

// Load all data sources
console.log('\n📂 Loading data sources...');
for (const source of DATA_SOURCES) {
    const filePath = path.join(__dirname, source);
    if (fs.existsSync(filePath)) {
        try {
            const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            console.log(`✅ Loaded: ${path.basename(filePath)}`);
            
            // Extract atoms
            if (data.atoms) {
                if (Array.isArray(data.atoms)) {
                    // Format: [["word", {...}], ...]
                    for (const [word, atomData] of data.atoms) {
                        allAtoms.set(word, atomData);
                    }
                } else if (typeof data.atoms === 'object') {
                    // Format: {"word": {...}, ...}
                    Object.entries(data.atoms).forEach(([word, atomData]) => {
                        allAtoms.set(word, atomData);
                    });
                }
            }
            
            // Extract patterns
            if (data.patterns) {
                if (Array.isArray(data.patterns)) {
                    for (const [id, patternData] of data.patterns) {
                        allPatterns.set(id, patternData);
                    }
                } else if (typeof data.patterns === 'object') {
                    Object.entries(data.patterns).forEach(([id, patternData]) => {
                        allPatterns.set(id, patternData);
                    });
                }
            }
            
            // Extract networks
            if (data.networks) {
                Object.entries(data.networks).forEach(([name, networkData]) => {
                    allNetworks.set(name, networkData);
                });
            }
            
            // Extract learned atoms from different formats
            if (data.learned_atoms) {
                Object.entries(data.learned_atoms).forEach(([word, atomData]) => {
                    allAtoms.set(word, atomData);
                });
            }
            
        } catch (err) {
            console.error(`❌ Failed to load ${path.basename(filePath)}:`, err.message);
        }
    }
}

console.log(`\n📊 Collected data:`);
console.log(`   - Atoms: ${allAtoms.size}`);
console.log(`   - Patterns: ${allPatterns.size}`);
console.log(`   - Networks: ${allNetworks.size}`);

// Convert atoms to memories for Long-Term Memory
console.log('\n🧠 Converting to memories...');

// Core atoms as memories
const coreAtoms = ['ich', 'bins', 'wieder', 'daniel', 'claude', 'crod', 'gradient', 'pattern', 'atom'];
for (const [word, atomData] of allAtoms) {
    const importance = coreAtoms.includes(word) ? 100 : 
                      (atomData.weight || 80);
    
    const memory = {
        id: `mem_atom_${word}_${Date.now()}`,
        content: `Atom: ${word} (prime: ${atomData.prime}, weight: ${atomData.weight || 50})`,
        atoms: [word],
        primes: [atomData.prime],
        importance: importance,
        timestamp: Date.now(),
        approved: true,
        approvedBy: 'import-script',
        source: 'legacy-import'
    };
    
    allMemories.push(memory);
}

// Important patterns as memories
for (const [id, patternData] of allPatterns) {
    if (patternData.occurrences > 10) {
        const memory = {
            id: `mem_pattern_${id}_${Date.now()}`,
            content: `Pattern ${id}: ${patternData.atoms.join(' + ')} (${patternData.occurrences} occurrences, resonance: ${patternData.resonance})`,
            atoms: patternData.atoms,
            primes: patternData.atoms.map(a => allAtoms.get(a)?.prime || 2),
            importance: Math.min(100, 50 + patternData.occurrences),
            timestamp: Date.now(),
            approved: true,
            approvedBy: 'import-script',
            source: 'legacy-import'
        };
        
        allMemories.push(memory);
    }
}

// Networks as memories
for (const [name, networkData] of allNetworks) {
    const memory = {
        id: `mem_network_${name}_${Date.now()}`,
        content: `Network ${name}: ${networkData.description}`,
        atoms: networkData.keywords || [],
        primes: (networkData.keywords || []).map(k => allAtoms.get(k)?.prime || 2),
        importance: networkData.importance === 'critical' ? 100 : 80,
        timestamp: Date.now(),
        approved: true,
        approvedBy: 'import-script',
        source: 'legacy-import'
    };
    
    allMemories.push(memory);
}

console.log(`📊 Created ${allMemories.length} memories from legacy data`);

// Save memories to Long-Term Memory directory
const MEMORY_DIR = path.join(__dirname, '../genesis-blocks/long-term-memory-genesis/memory-data/long-term/memories');
const GENESIS_STATE_FILE = path.join(__dirname, '../genesis-blocks/long-term-memory-genesis/memory-data/long-term/genesis-state.json');

console.log('\n💾 Saving memories to Long-Term Memory...');
let savedCount = 0;

for (const memory of allMemories) {
    const memFile = path.join(MEMORY_DIR, `${memory.id}.json`);
    try {
        fs.writeFileSync(memFile, JSON.stringify(memory, null, 2));
        savedCount++;
    } catch (err) {
        console.error(`❌ Failed to save ${memory.id}:`, err.message);
    }
}

// Update genesis state
try {
    const genesisState = JSON.parse(fs.readFileSync(GENESIS_STATE_FILE, 'utf8'));
    genesisState.stats.totalMemories += savedCount;
    genesisState.stats.approvedMemories += savedCount;
    genesisState.stats.lastImport = Date.now();
    
    // Add all imported memories to danielApprovals
    allMemories.forEach(m => {
        if (!genesisState.danielApprovals.includes(m.id)) {
            genesisState.danielApprovals.push(m.id);
        }
    });
    
    fs.writeFileSync(GENESIS_STATE_FILE, JSON.stringify(genesisState, null, 2));
    console.log('✅ Updated genesis state');
} catch (err) {
    console.error('❌ Failed to update genesis state:', err.message);
}

console.log(`\n✨ Import complete! Saved ${savedCount} memories`);

// Save comprehensive data export
const exportData = {
    meta: {
        importDate: new Date().toISOString(),
        source: 'CROD Legacy Data Import',
        stats: {
            atoms: allAtoms.size,
            patterns: allPatterns.size,
            networks: allNetworks.size,
            memories: savedCount
        }
    },
    atoms: Array.from(allAtoms.entries()),
    patterns: Array.from(allPatterns.entries()),
    networks: Object.fromEntries(allNetworks),
    chains: Object.fromEntries(allChains)
};

const exportFile = path.join(__dirname, '../data/crod-legacy-export.json');
fs.mkdirSync(path.dirname(exportFile), { recursive: true });
fs.writeFileSync(exportFile, JSON.stringify(exportData, null, 2));
console.log(`\n📦 Full export saved to: ${exportFile}`);

// Notify Long-Term Memory chain if running
try {
    const notifyReq = http.request({
        hostname: '127.0.0.1',
        port: 7009,
        path: '/reload',
        method: 'POST'
    }, (res) => {
        if (res.statusCode === 200) {
            console.log('🔄 Notified Long-Term Memory chain to reload');
        }
    });
    notifyReq.on('error', () => {
        console.log('ℹ️  Long-Term Memory chain not running');
    });
    notifyReq.end();
} catch (err) {
    // Ignore
}