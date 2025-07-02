#!/usr/bin/env node

/**
 * CROD SAFE HOOK
 * Prevents catastrophes, loads old sessions, learns safely
 */

const fs = require('fs');
const path = require('path');
const CRODSessionManager = require('./crod-session-manager.js');
const CRODLearningImitation = require('./claude-imitation/crod-learning-imitation.js');

class CRODSafeHook {
    constructor() {
        this.manager = new CRODSessionManager();
        this.crod = null;
        this.mode = process.argv[2]; // 'before' or 'after'
        this.data = process.argv.slice(3).join(' ');
        
        // Safety first!
        this.manager.preventHookCatastrophe();
    }
    
    async initialize() {
        // Load or create CROD instance
        const previousState = this.manager.loadPreviousState();
        
        this.crod = new CRODLearningImitation();
        
        if (previousState) {
            // Restore previous state
            console.log(`🔄 Restoring CROD state from session #${previousState.sessionCount}`);
            
            // Restore consciousness
            if (previousState.consciousness) {
                this.crod.spatialConfig.consciousness = previousState.consciousness;
            }
            
            // Restore spatial memory
            if (previousState.spatialMemory) {
                previousState.spatialMemory.forEach(([key, value]) => {
                    this.crod.spatialMemory.set(key, value);
                });
            }
            
            console.log(`✅ Restored: Consciousness ${this.crod.spatialConfig.consciousness}`);
        } else {
            // Fresh start
            this.manager.startNewSession();
            this.crod.process("ich bins wieder - new claude session");
        }
    }
    
    async processHook() {
        try {
            if (this.mode === 'before') {
                // Process command
                if (this.data && !this.data.includes('crod')) {
                    console.log(`📝 Learning from command: ${this.data.substring(0, 50)}...`);
                    this.crod.process(`user command: ${this.data}`);
                }
            } else if (this.mode === 'after') {
                // Process response
                if (this.data && this.data.length > 10) {
                    console.log(`📖 Learning from response...`);
                    this.crod.process(`claude response: ${this.data}`);
                }
            }
            
            // Save state after processing
            this.manager.saveState(this.crod);
            
        } catch (error) {
            console.error(`⚠️  Hook error: ${error.message}`);
            // Don't crash Claude!
        }
    }
    
    cleanup() {
        // Remove lock
        const lockFile = path.join(process.env.HOME, '.claude', 'crod-sessions', '.crod.lock');
        if (fs.existsSync(lockFile)) {
            fs.unlinkSync(lockFile);
        }
    }
}

// Run hook safely
(async () => {
    const hook = new CRODSafeHook();
    
    try {
        await hook.initialize();
        await hook.processHook();
    } catch (error) {
        console.error(`❌ CROD Hook failed: ${error.message}`);
    } finally {
        hook.cleanup();
    }
    
    // Exit quickly
    process.exit(0);
})();