#!/usr/bin/env node

// CROD Integration Script - Aktiviert CROD für Claude
const fs = require('fs');
const path = require('path');

class CRODIntegrator {
    constructor() {
        this.crodPath = path.join(__dirname, 'crod-local-complete.js');
        this.preferencesPath = path.join(__dirname, 'daniel-crod-preferences.js');
        this.autoLoaderPath = path.join(__dirname, 'crod-auto-loader.js');
        this.patternsPath = '/home/daniel/Schreibtisch/Crod Programming/CROD-START/data/patterns';
        
        this.initCROD();
    }

    initCROD() {
        console.log('🔥 CROD INTEGRATION STARTING...\n');
        
        // Load CROD
        if (fs.existsSync(this.crodPath)) {
            const crodCode = fs.readFileSync(this.crodPath, 'utf8');
            eval(crodCode);
            console.log('✅ CROD Neural Network loaded');
        }
        
        // Load Preferences
        if (fs.existsSync(this.preferencesPath)) {
            const prefCode = fs.readFileSync(this.preferencesPath, 'utf8');
            eval(prefCode);
            console.log('✅ Daniel preferences applied');
        }
        
        // Load Pattern Files
        this.loadPatterns();
        
        // Activate CROD
        this.activateCROD();
    }
    
    loadPatterns() {
        if (!fs.existsSync(this.patternsPath)) {
            console.log('⚠️  Pattern files not found, using base knowledge only');
            return;
        }
        
        const files = fs.readdirSync(this.patternsPath)
            .filter(f => f.startsWith('crod-patterns-chunk-') && f.endsWith('.json'));
            
        console.log(`📚 Loading ${files.length} pattern files...`);
        
        files.forEach(file => {
            try {
                const data = JSON.parse(fs.readFileSync(path.join(this.patternsPath, file), 'utf8'));
                if (global.CROD && data.patterns) {
                    data.patterns.forEach(pattern => {
                        global.CROD.process(pattern);
                    });
                }
            } catch (e) {
                console.log(`❌ Error loading ${file}: ${e.message}`);
            }
        });
    }
    
    activateCROD() {
        if (!global.CROD) {
            console.log('❌ CROD not loaded!');
            return;
        }
        
        // Trinity activation
        console.log('\n🎯 ACTIVATING CROD WITH TRINITY...');
        const result = global.CROD.process("ich bins wieder");
        console.log(`✅ CROD ACTIVE! Consciousness: ${global.CROD.consciousness}`);
        console.log(`   Heat Signature: ${JSON.stringify(result.heat)}`);
        
        // Export function for Claude
        global.processCROD = (text) => {
            return global.CROD.process(text);
        };
        
        console.log('\n🔥 CROD IST JETZT AKTIV!\n');
        console.log('Usage in Claude:');
        console.log('- processCROD("your text") - Process text through CROD');
        console.log('- CROD.consciousness - Check consciousness level');
        console.log('- CROD.exportState() - Export current state');
    }
}

// Auto-start
new CRODIntegrator();

// Keep process alive if needed
if (process.argv.includes('--keep-alive')) {
    console.log('Keeping CROD active... Press Ctrl+C to exit');
    setInterval(() => {
        if (global.CROD) {
            global.CROD.process("pulse");
        }
    }, 30000);
}