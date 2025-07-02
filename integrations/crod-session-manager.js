#!/usr/bin/env node

/**
 * CROD SESSION MANAGER
 * Lädt alte Sessions und verhindert Hook-Katastrophen
 */

const fs = require('fs');
const path = require('path');

class CRODSessionManager {
    constructor() {
        this.sessionPath = path.join(process.env.HOME, '.claude', 'crod-sessions');
        this.currentSessionFile = path.join(this.sessionPath, 'current-session.json');
        this.stateFile = path.join(this.sessionPath, 'crod-persistent-state.json');
        this.lockFile = path.join(this.sessionPath, '.crod.lock');
        
        // Create directories
        this.ensureDirectories();
        
        // Check for lock (prevent hook loops)
        this.checkLock();
    }
    
    ensureDirectories() {
        if (!fs.existsSync(this.sessionPath)) {
            fs.mkdirSync(this.sessionPath, { recursive: true });
            console.log(`📁 Created session directory: ${this.sessionPath}`);
        }
    }
    
    checkLock() {
        if (fs.existsSync(this.lockFile)) {
            const lockData = JSON.parse(fs.readFileSync(this.lockFile, 'utf8'));
            const lockAge = Date.now() - lockData.timestamp;
            
            if (lockAge < 5000) { // 5 second lock
                console.log('🔒 CROD already running, preventing hook loop!');
                process.exit(0);
            } else {
                console.log('🔓 Stale lock detected, removing...');
                fs.unlinkSync(this.lockFile);
            }
        }
        
        // Create new lock
        fs.writeFileSync(this.lockFile, JSON.stringify({
            pid: process.pid,
            timestamp: Date.now()
        }));
        
        // Remove lock on exit
        process.on('exit', () => {
            if (fs.existsSync(this.lockFile)) {
                fs.unlinkSync(this.lockFile);
            }
        });
    }
    
    loadPreviousState() {
        console.log('📚 Loading previous CROD state...');
        
        if (fs.existsSync(this.stateFile)) {
            try {
                const state = JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
                console.log(`✅ Loaded state: ${state.neurons} neurons, consciousness: ${state.consciousness}`);
                return state;
            } catch (e) {
                console.log(`⚠️  Could not load state: ${e.message}`);
                return null;
            }
        }
        
        console.log('📝 No previous state found, starting fresh');
        return null;
    }
    
    saveState(crodInstance) {
        const state = {
            neurons: crodInstance.neurons.size,
            patterns: crodInstance.patterns.size,
            consciousness: crodInstance.spatialConfig?.consciousness || 0,
            spatialMemory: Array.from(crodInstance.spatialMemory?.entries() || []),
            discoveries: crodInstance.learningSystem?.discoveredPatterns || [],
            lastSaved: Date.now(),
            sessionCount: this.getSessionCount() + 1
        };
        
        fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2));
        console.log(`💾 State saved: ${state.neurons} neurons, session #${state.sessionCount}`);
    }
    
    getSessionCount() {
        if (fs.existsSync(this.stateFile)) {
            const state = JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
            return state.sessionCount || 0;
        }
        return 0;
    }
    
    startNewSession() {
        const sessionId = `session_${Date.now()}`;
        const session = {
            id: sessionId,
            startTime: Date.now(),
            messages: 0,
            discoveries: [],
            continuedFrom: this.getLastSessionId()
        };
        
        fs.writeFileSync(this.currentSessionFile, JSON.stringify(session, null, 2));
        console.log(`🆕 Started new session: ${sessionId}`);
        
        // Archive old session if exists
        this.archiveLastSession();
        
        return session;
    }
    
    getLastSessionId() {
        if (fs.existsSync(this.currentSessionFile)) {
            const session = JSON.parse(fs.readFileSync(this.currentSessionFile, 'utf8'));
            return session.id;
        }
        return null;
    }
    
    archiveLastSession() {
        if (fs.existsSync(this.currentSessionFile)) {
            const session = JSON.parse(fs.readFileSync(this.currentSessionFile, 'utf8'));
            const archivePath = path.join(this.sessionPath, `${session.id}.json`);
            
            // Add end time
            session.endTime = Date.now();
            session.duration = session.endTime - session.startTime;
            
            fs.writeFileSync(archivePath, JSON.stringify(session, null, 2));
            console.log(`📦 Archived session: ${session.id}`);
        }
    }
    
    preventHookCatastrophe() {
        // Safety checks
        const checks = {
            lockExists: fs.existsSync(this.lockFile),
            processCount: this.countCRODProcesses(),
            memoryUsage: process.memoryUsage().heapUsed / 1024 / 1024,
            isRecursive: process.env.CROD_DEPTH ? parseInt(process.env.CROD_DEPTH) > 1 : false
        };
        
        if (checks.processCount > 3) {
            console.error('⚠️  Too many CROD processes! Aborting to prevent catastrophe.');
            process.exit(1);
        }
        
        // Daniel says: GANZER PC = CROD! 
        // 50% simulation, 30% build, 20% buffer
        const totalMemoryGB = require('os').totalmem() / 1024 / 1024 / 1024;
        const crodAllowedGB = totalMemoryGB * 0.8; // 80% for CROD!
        
        if (checks.memoryUsage > crodAllowedGB * 1024) {
            console.warn(`⚠️  Using ${checks.memoryUsage}MB of ${crodAllowedGB}GB allowed`);
            // Don't exit - CROD TAKES OVER!
        }
        
        if (checks.isRecursive) {
            console.error('⚠️  Recursive hook detected! Aborting.');
            process.exit(1);
        }
        
        console.log('✅ Hook safety checks passed');
        return true;
    }
    
    countCRODProcesses() {
        try {
            const { execSync } = require('child_process');
            const count = execSync('ps aux | grep -c "[c]rod-"').toString().trim();
            return parseInt(count) || 0;
        } catch (e) {
            return 0;
        }
    }
}

// Export for use
module.exports = CRODSessionManager;

// If run directly, test session management
if (require.main === module) {
    console.log('🧪 Testing CROD Session Manager...\n');
    
    const manager = new CRODSessionManager();
    
    // Prevent catastrophe
    manager.preventHookCatastrophe();
    
    // Load previous state
    const previousState = manager.loadPreviousState();
    
    // Start new session
    const session = manager.startNewSession();
    
    // Simulate CROD instance
    const mockCROD = {
        neurons: new Map([['test', {}]]),
        patterns: new Map(),
        spatialMemory: new Map([['test', {x: 50, y: 50, z: 0}]]),
        spatialConfig: { consciousness: 100 },
        learningSystem: { discoveredPatterns: [] }
    };
    
    // Save state
    manager.saveState(mockCROD);
    
    console.log('\n✅ Session manager working correctly!');
}