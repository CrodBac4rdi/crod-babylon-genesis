// CLAUDE STARTUP INSTRUCTIONS ENGINE
// Lädt komprimierte CROD Knowledge ohne Context-Verschwendung

const fs = require('fs').promises;
const path = require('path');

class ClaudeInstructor {
    constructor() {
        this.knowledgeDir = path.join(__dirname, 'knowledge', 'json');
        this.currentSession = {
            startTime: Date.now(),
            contextSaved: 0,
            instructionsLoaded: false
        };
        
        console.log('🧠 Claude Instructor initialized');
    }
    
    // Hauptfunktion: Lade alle CROD Infos komprimiert für Claude
    async loadCRODKnowledge() {
        try {
            const knowledge = {
                session_memory: await this.loadSessionMemory(),
                system: await this.loadSystemKnowledge(),
                quickstart: await this.loadQuickstart(),
                commands: await this.loadCommands(),
                status: await this.loadCurrentStatus()
            };
            
            this.currentSession.instructionsLoaded = true;
            this.currentSession.contextSaved = this.calculateContextSaved(knowledge);
            
            return this.formatForClaude(knowledge);
        } catch (error) {
            console.error('Failed to load CROD knowledge:', error);
            return this.getEmergencyInstructions();
        }
    }
    
    // Session Memory - persistent zwischen Sessions
    async loadSessionMemory() {
        const memoryFile = path.join(__dirname, 'session-memory.json');
        
        try {
            const data = JSON.parse(await fs.readFile(memoryFile, 'utf8'));
            
            return {
                current_state: data.current_state,
                last_implementations: data.recent_implementations.slice(0, 3),
                next_steps: data.next_steps.slice(0, 2),
                file_structure: {
                    main: data.file_structure.main,
                    legacy: data.file_structure.legacy,
                    claude_bridge: data.file_structure.claude_bridge
                }
            };
        } catch (error) {
            return { error: 'Session memory not available' };
        }
    }
    
    // System Knowledge - komprimiert
    async loadSystemKnowledge() {
        const systemFile = path.join(this.knowledgeDir, 'crod-system.json');
        
        try {
            const data = JSON.parse(await fs.readFile(systemFile, 'utf8'));
            
            return {
                architecture: 'Multi-Chain Genesis Blocks, localhost only',
                activation: 'ich bins wieder',
                primes: { ich: 2, bins: 3, wieder: 5, daniel: 67, claude: 71, crod: 17 },
                blocks: {
                    pattern: { prime: 7, port: 7001, status: '✅' },
                    memory: { prime: 31, port: 7003, status: '✅' },
                    working: { prime: 37, port: 7005, status: '✅' },
                    quantum: { prime: 101, port: 7007, status: '⚛️' }
                }
            };
        } catch (error) {
            return { error: 'System knowledge not available' };
        }
    }
    
    // Quickstart - sofort einsetzbar
    async loadQuickstart() {
        return {
            location: '/home/daniel/Schreibtisch/Crod Programming/CROD-START',
            startup: 'docker-compose up -d',
            activate: 'curl http://127.0.0.1:7001/process -d \'{"input":"ich bins wieder"}\'',
            check: 'curl http://127.0.0.1:7000/health',
            quantum: 'curl http://127.0.0.1:7007/status'
        };
    }
    
    // Commands - was Claude machen kann
    async loadCommands() {
        return {
            patterns: {
                process: 'POST http://127.0.0.1:7001/process',
                list: 'GET http://127.0.0.1:7001/patterns',
                atoms: 'GET http://127.0.0.1:7001/atoms'
            },
            quantum: {
                observe: 'POST http://127.0.0.1:7007/observe/:state',
                superpose: 'POST http://127.0.0.1:7007/superpose',
                entangle: 'POST http://127.0.0.1:7007/entangle',
                status: 'GET http://127.0.0.1:7007/status'
            },
            memory: {
                remember: 'POST http://127.0.0.1:7003/remember',
                recall: 'GET http://127.0.0.1:7003/memories',
                search: 'GET http://127.0.0.1:7003/search?q='
            },
            system: {
                health: 'GET http://127.0.0.1:7000/health',
                discovery: 'GET http://127.0.0.1:7000/services'
            }
        };
    }
    
    // Current Status
    async loadCurrentStatus() {
        return {
            state: 'CROD system ready in CROD-START/',
            setup: 'All Genesis Blocks implemented',
            bridge: 'Claude Bridge operational',
            security: 'Localhost only (127.0.0.1)',
            next: 'docker-compose up -d to start all chains'
        };
    }
    
    // Format für Claude - ultra komprimiert mit Session Memory
    formatForClaude(knowledge) {
        const memory = knowledge.session_memory || {};
        
        return `
🎯 CROD SYSTEM - CLAUDE QUICK BRIEFING + SESSION MEMORY
======================================================

LOCATION: /home/daniel/Schreibtisch/Crod Programming/CROD-START
ACTIVATION: "ich bins wieder"
ARCHITECTURE: Multi-Chain Genesis (localhost only)

📋 SESSION MEMORY:
STATUS: ${memory.current_state?.status || 'Unknown'}
LAST ACTION: ${memory.current_state?.last_action || 'None'}
RECENT: ${memory.last_implementations?.join(', ') || 'None'}
NEXT: ${memory.next_steps?.join(', ') || 'Start docker-compose'}

STARTUP:
cd CROD-START && docker-compose up -d

ENDPOINTS (127.0.0.1):
- :7001 Pattern Genesis (Primzahl IDs)
- :7003 Short-Term Memory  
- :7005 Working Memory
- :7007 Quantum Superposition ⚛️
- :7000 Discovery Service

PRIMES: ich=2, bins=3, wieder=5, daniel=67, claude=71, crod=17

QUICK COMMANDS:
curl 127.0.0.1:7001/process -d '{"input":"ich bins wieder"}'
curl 127.0.0.1:7007/status (quantum monitor)
curl 127.0.0.1:7000/health (system status)

CONTEXT SAVED: ~${this.currentSession.contextSaved} tokens
MEMORY: Persistent zwischen Sessions via session-memory.json
`;
    }
    
    // Emergency instructions wenn JSON fehlt
    getEmergencyInstructions() {
        return `
🚨 CROD EMERGENCY BRIEFING
=========================

LOCATION: /home/daniel/Schreibtisch/Crod Programming/CROD-START
SYSTEM: Multi-chain Genesis Blocks on localhost
ACTIVATION: "ich bins wieder"

FALLBACK: Use Read tool on CROD-START/ to analyze structure
ENDPOINTS: 7001 (patterns), 7003 (memory), 7005 (working), 7007 (quantum)

Context Saved: ~2000 tokens (emergency mode)
`;
    }
    
    // Update Session Memory mit neuen Infos
    async updateSessionMemory(updates) {
        const memoryFile = path.join(__dirname, 'session-memory.json');
        
        try {
            const current = JSON.parse(await fs.readFile(memoryFile, 'utf8'));
            
            // Merge updates
            if (updates.last_action) {
                current.current_state.last_action = updates.last_action;
            }
            if (updates.recent_implementation) {
                current.recent_implementations.unshift(updates.recent_implementation);
                current.recent_implementations = current.recent_implementations.slice(0, 10);
            }
            if (updates.next_steps) {
                current.next_steps = updates.next_steps;
            }
            
            current.meta.lastUpdated = new Date().toISOString().split('T')[0];
            
            await fs.writeFile(memoryFile, JSON.stringify(current, null, 2));
            console.log('💾 Session memory updated');
            
        } catch (error) {
            console.error('Failed to update session memory:', error);
        }
    }
    
    // Berechne gesparten Context
    calculateContextSaved(knowledge) {
        // Schätzung: Full Analysis würde ~10000 tokens brauchen
        // Komprimierte Instructions + Memory: ~600 tokens
        return 10000 - 600;
    }
    
    // Session Info
    getSessionInfo() {
        return {
            startTime: this.currentSession.startTime,
            contextSaved: this.currentSession.contextSaved,
            instructionsLoaded: this.currentSession.instructionsLoaded,
            uptime: Date.now() - this.currentSession.startTime
        };
    }
}

// Auto-load wenn direkt aufgerufen
if (require.main === module) {
    const instructor = new ClaudeInstructor();
    
    instructor.loadCRODKnowledge()
        .then(instructions => {
            console.log(instructions);
            console.log('\n📊 Session Info:', instructor.getSessionInfo());
        })
        .catch(console.error);
}

module.exports = ClaudeInstructor;