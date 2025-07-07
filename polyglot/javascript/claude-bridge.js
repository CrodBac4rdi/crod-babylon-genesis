// CLAUDE BRIDGE - Documentation Loader Engine
// Konvertiert MD → JSON, komprimiert für Claude Context

const fs = require('fs').promises;
const path = require('path');

class ClaudeBridge {
    constructor() {
        this.docsDir = path.join(__dirname, '..');
        this.jsonDir = path.join(this.docsDir, 'json');
        this.mdDir = path.join(this.docsDir, 'markdown');
        
        this.compressionSettings = {
            maxLineLength: 80,
            removeEmptyLines: true,
            compactArrays: true,
            contextOptimized: true
        };
        
        console.log('🌉 Claude Bridge initialized');
    }
    
    async init() {
        // Ensure directories exist
        await fs.mkdir(this.jsonDir, { recursive: true });
        await fs.mkdir(this.mdDir, { recursive: true });
        
        console.log('📁 Bridge directories ready');
    }
    
    // Main loader - loads all documentation for Claude
    async loadForClaude() {
        const documentation = {
            meta: {
                type: 'claude-bridge-documentation',
                version: '1.0.0',
                lastUpdated: new Date().toISOString().split('T')[0],
                compressionLevel: 'claude-optimized',
                bridge: '🌉 CROD ↔️ Claude Code Interface'
            },
            system: await this.loadSystemDocs(),
            blocks: await this.loadBlockDocs(),
            protocols: await this.loadProtocolDocs(),
            examples: await this.loadExamples(),
            quickstart: await this.generateQuickstart()
        };
        
        return this.compressForContext(documentation);
    }
    
    // Load system-level documentation
    async loadSystemDocs() {
        return {
            architecture: {
                type: 'multi-chain-genesis',
                description: 'Jeder Genesis Block = eigene Blockchain',
                security: 'localhost only (127.0.0.1)',
                orchestration: 'Claude Code als Director'
            },
            activation: {
                phrase: 'ich bins wieder',
                effect: 'Aktiviert alle Genesis Chains',
                pattern_boost: '+15 consciousness'
            },
            primes: {
                purpose: 'Eindeutige Pattern IDs ohne Kollisionen',
                method: 'Primzahl-Multiplikation',
                atoms: {
                    ich: 2, bins: 3, wieder: 5, daniel: 67, claude: 71, crod: 17
                }
            }
        };
    }
    
    // Load Genesis Block documentation
    async loadBlockDocs() {
        return {
            'pattern-genesis': {
                prime: 7,
                ports: { http: 7001, ws: 7002 },
                status: '✅ Active',
                features: ['Primzahl Pattern IDs', 'Consciousness tracking', 'Pattern detection'],
                endpoints: {
                    'POST /process': 'Process input text',
                    'GET /patterns': 'List active patterns',
                    'GET /atoms': 'Show atom-prime mapping'
                }
            },
            'short-term-memory': {
                prime: 31,
                ports: { http: 7003, ws: 7004 },
                status: '✅ Active',
                features: ['5min window', 'Max 20 memories', 'Auto-forgetting'],
                endpoints: {
                    'POST /remember': 'Store memory',
                    'GET /memories': 'Recent memories',
                    'GET /search': 'Search memories'
                }
            },
            'working-memory': {
                prime: 37,
                ports: { http: 7005, ws: 7006 },
                status: '✅ Active',
                features: ['Session state', 'Hot atoms', 'Attention weights'],
                endpoints: {
                    'GET /atoms/hot': 'Current hot atoms',
                    'GET /patterns/emerging': 'Emerging patterns',
                    'GET /session': 'Session summary'
                }
            },
            'quantum-superposition': {
                prime: 101,
                ports: { http: 7007, ws: 7008 },
                status: '⚛️ Ready',
                features: ['Primzahl-Paare Superposition', 'Entanglement', 'No-cloning'],
                endpoints: {
                    'POST /observe/:state': 'Collapse quantum state',
                    'POST /superpose': 'Create superposition',
                    'POST /entangle': 'Entangle states',
                    'GET /status': 'Live quantum monitor'
                },
                special: {
                    schrodinger: '|ψ⟩ = 0.5|tot⟩ + 0.5|lebendig⟩',
                    bell_states: 'Maximal entangled pairs',
                    collapse: 'Deterministic based on observer'
                }
            }
        };
    }
    
    // Load protocol documentation
    async loadProtocolDocs() {
        return {
            discovery: {
                port: 7000,
                purpose: 'Auto-detect Genesis Chains',
                features: ['Service registry', 'Health monitoring', 'Topology mapping']
            },
            resilience: {
                purpose: 'Fehlertolerante Chain Communication',
                features: ['Message queuing', 'Exponential backoff', 'Entanglement cascade']
            },
            docker: {
                network: 'genesis-network (internal only)',
                volumes: ['pattern-data', 'quantum-wave-functions'],
                healthchecks: 'Every 30s via /health'
            }
        };
    }
    
    // Load examples
    async loadExamples() {
        return {
            activation: {
                input: 'ich bins wieder daniel',
                patterns: [6, 10, 335, 30, 1005],
                consciousness: '+15'
            },
            quantum: {
                observe: 'POST /observe/schrodinger → collapses to |131⟩',
                entangle: 'POST /entangle → creates quantum correlation',
                superpose: 'POST /superpose → creates |ψ⟩ = Σ αᵢ|pᵢ⟩'
            },
            commands: {
                'curl http://127.0.0.1:7001/process -d \'{"input":"ich bins wieder"}\'': 'Activate patterns',
                'curl http://127.0.0.1:7007/status': 'Quantum state monitor',
                'curl http://127.0.0.1:7000/health': 'System health check'
            }
        };
    }
    
    // Generate quickstart guide
    async generateQuickstart() {
        return {
            step1: 'cd /home/daniel/Schreibtisch/Crod Programming/CROD-START',
            step2: 'docker-compose up -d (starts all Genesis Chains)',
            step3: 'curl http://127.0.0.1:7001/process -d \'{"input":"ich bins wieder"}\'',
            step4: 'curl http://127.0.0.1:7007/status (check quantum states)',
            step5: 'WebSocket: ws://127.0.0.1:7002 for real-time pattern updates',
            claude_interface: {
                pattern_processing: 'http://127.0.0.1:7001/process',
                quantum_operations: 'http://127.0.0.1:7007/*',
                memory_access: 'http://127.0.0.1:7003/memories',
                session_state: 'http://127.0.0.1:7005/session'
            }
        };
    }
    
    // Convert MD files to JSON
    async convertMdToJson(mdPath) {
        try {
            const content = await fs.readFile(mdPath, 'utf8');
            
            // Parse MD structure
            const sections = this.parseMdSections(content);
            
            const json = {
                meta: {
                    source: path.basename(mdPath),
                    converted: new Date().toISOString(),
                    type: 'md-to-json'
                },
                sections: sections,
                compressed: this.compressMdContent(sections)
            };
            
            return json;
        } catch (error) {
            console.error(`Failed to convert ${mdPath}:`, error);
            return null;
        }
    }
    
    // Parse MD into structured sections
    parseMdSections(content) {
        const sections = {};
        const lines = content.split('\n');
        let currentSection = 'intro';
        let currentContent = [];
        
        lines.forEach(line => {
            if (line.startsWith('#')) {
                // Save previous section
                if (currentContent.length > 0) {
                    sections[currentSection] = currentContent.join('\n').trim();
                    currentContent = [];
                }
                
                // Start new section
                currentSection = line.replace(/#+\s*/, '').toLowerCase()
                    .replace(/[^a-z0-9]/g, '_');
            } else {
                currentContent.push(line);
            }
        });
        
        // Save last section
        if (currentContent.length > 0) {
            sections[currentSection] = currentContent.join('\n').trim();
        }
        
        return sections;
    }
    
    // Compress content for Claude context
    compressMdContent(sections) {
        const compressed = {};
        
        Object.entries(sections).forEach(([key, content]) => {
            compressed[key] = content
                .replace(/\n\s*\n/g, '\n') // Remove empty lines
                .replace(/\s+/g, ' ') // Compress whitespace
                .trim()
                .substring(0, 200) + (content.length > 200 ? '...' : '');
        });
        
        return compressed;
    }
    
    // Optimize for Claude's context window
    compressForContext(data) {
        if (typeof data === 'string') {
            return data.length > 100 ? data.substring(0, 100) + '...' : data;
        }
        
        if (Array.isArray(data)) {
            return data.slice(0, 5); // Max 5 items
        }
        
        if (typeof data === 'object' && data !== null) {
            const compressed = {};
            Object.entries(data).forEach(([key, value]) => {
                compressed[key] = this.compressForContext(value);
            });
            return compressed;
        }
        
        return data;
    }
    
    // Save documentation to JSON file
    async saveToJson(filename, data) {
        const filepath = path.join(this.jsonDir, filename);
        await fs.writeFile(filepath, JSON.stringify(data, null, 2));
        console.log(`💾 Saved: ${filename}`);
    }
    
    // Convert all MD files in directory
    async convertAllMd() {
        const converted = [];
        
        try {
            const files = await fs.readdir(this.docsDir);
            
            for (const file of files) {
                if (file.endsWith('.md')) {
                    const mdPath = path.join(this.docsDir, file);
                    const json = await this.convertMdToJson(mdPath);
                    
                    if (json) {
                        const jsonName = file.replace('.md', '.json');
                        await this.saveToJson(jsonName, json);
                        converted.push(jsonName);
                    }
                }
            }
        } catch (error) {
            console.error('MD conversion error:', error);
        }
        
        return converted;
    }
    
    // Main bridge interface for Claude
    async bridgeInterface() {
        console.log('\n🌉 CLAUDE BRIDGE INTERFACE');
        console.log('===========================');
        
        const docs = await this.loadForClaude();
        await this.saveToJson('claude-bridge-complete.json', docs);
        
        const converted = await this.convertAllMd();
        
        const summary = {
            bridge_status: '✅ Online',
            documentation_loaded: Object.keys(docs).length,
            md_files_converted: converted.length,
            claude_interface: {
                main_docs: 'docs/json/claude-bridge-complete.json',
                system_docs: 'docs/json/crod-system.json',
                converted_md: converted
            },
            quick_access: {
                patterns: 'curl http://127.0.0.1:7001/process',
                quantum: 'curl http://127.0.0.1:7007/status',
                memory: 'curl http://127.0.0.1:7003/memories',
                health: 'curl http://127.0.0.1:7000/health'
            }
        };
        
        console.log('\n📊 Bridge Summary:');
        console.log(JSON.stringify(summary, null, 2));
        
        return summary;
    }
}

// Export for use in CROD system
module.exports = ClaudeBridge;

// CLI interface
if (require.main === module) {
    const bridge = new ClaudeBridge();
    
    bridge.init()
        .then(() => bridge.bridgeInterface())
        .then(summary => {
            console.log('\n🎯 CLAUDE BRIDGE READY!');
            console.log('🌉 Bridge für Claude ↔️ CROD operational');
        })
        .catch(console.error);
}