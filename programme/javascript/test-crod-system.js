#!/usr/bin/env node

/**
 * CROD System Test Suite - Testet alle Komponenten
 */

const CRODSettingsManager = require('./crod-settings-manager');
const CRODFallbackSystem = require('./crod-fallback-system');
const CRODPatternDetector = require('./crod-pattern-detector');
const CRODMasterIntegration = require('./crod-master-integration');
const http = require('http');

class CRODSystemTester {
    constructor() {
        this.tests = [];
        this.passed = 0;
        this.failed = 0;
    }
    
    /**
     * Test hinzufügen
     */
    addTest(name, testFn) {
        this.tests.push({ name, testFn });
    }
    
    /**
     * Alle Tests ausführen
     */
    async runTests() {
        console.log("🧪 CROD System Test Suite startet...\n");
        
        for (const test of this.tests) {
            try {
                console.log(`📋 ${test.name}...`);
                await test.testFn();
                console.log(`✅ ${test.name} - PASSED\n`);
                this.passed++;
            } catch (error) {
                console.log(`❌ ${test.name} - FAILED`);
                console.log(`   Error: ${error.message}\n`);
                this.failed++;
            }
        }
        
        console.log("\n" + "=".repeat(50));
        console.log(`📊 Test Results: ${this.passed} passed, ${this.failed} failed`);
        console.log("=".repeat(50));
        
        return this.failed === 0;
    }
    
    /**
     * HTTP Request Helper
     */
    httpRequest(options) {
        return new Promise((resolve, reject) => {
            const req = http.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        resolve({
                            statusCode: res.statusCode,
                            data: JSON.parse(data)
                        });
                    } catch {
                        resolve({
                            statusCode: res.statusCode,
                            data: data
                        });
                    }
                });
            });
            
            req.on('error', reject);
            req.setTimeout(5000);
            
            if (options.body) {
                req.write(JSON.stringify(options.body));
            }
            
            req.end();
        });
    }
}

// Test Runner
const tester = new CRODSystemTester();

// Test 1: Settings Manager
tester.addTest('Settings Manager Initialization', async () => {
    const manager = new CRODSettingsManager();
    const initialized = await manager.initialize();
    if (!initialized) throw new Error('Failed to initialize');
    
    // Check Trinity values
    if (manager.trinity.ich !== 2) throw new Error('Trinity value wrong');
    if (manager.trinity.crod !== 17) throw new Error('Trinity CROD value wrong');
});

// Test 2: Pattern Detection
tester.addTest('Pattern Detection Basic', async () => {
    const detector = new CRODPatternDetector();
    await detector.initialize();
    
    const result = detector.detectPatterns('ich bins wieder');
    if (!result.patterns || result.patterns.length === 0) {
        throw new Error('No patterns detected for activation phrase');
    }
    
    if (result.suggested_action?.action !== 'FULL_ACTIVATION') {
        throw new Error('Wrong action suggested');
    }
});

// Test 3: Trinity Score Calculation
tester.addTest('Trinity Score Calculation', async () => {
    const manager = new CRODSettingsManager();
    await manager.initialize();
    
    const score = manager.calculateTrinityScore('ich bins wieder daniel');
    const expected = 2 + 3 + 5 + 67; // ich + bins + wieder + daniel
    
    if (score !== expected) {
        throw new Error(`Trinity score ${score} !== ${expected}`);
    }
});

// Test 4: Pattern Learning
tester.addTest('Pattern Learning', async () => {
    const detector = new CRODPatternDetector();
    await detector.initialize();
    
    const patternId = await detector.learnPattern('test input', 'test output', true);
    if (!patternId) throw new Error('Pattern learning failed');
    
    // Test if learned pattern is detected
    const result = detector.detectPatterns('test input');
    const hasLearned = result.patterns.some(p => p.learned === true);
    
    if (!hasLearned) {
        throw new Error('Learned pattern not detected');
    }
});

// Test 5: Fallback System Health Check
tester.addTest('Fallback System Health Check', async () => {
    const fallback = new CRODFallbackSystem();
    await fallback.settingsManager.initialize();
    
    const health = await fallback.performFullHealthCheck();
    if (typeof health !== 'object') {
        throw new Error('Health check returned invalid data');
    }
});

// Test 6: Emergency Mode
tester.addTest('Emergency Mode Activation', async () => {
    const fallback = new CRODFallbackSystem();
    await fallback.settingsManager.initialize();
    
    fallback.activateEmergencyMode();
    
    if (!fallback.emergencyMode) {
        throw new Error('Emergency mode not activated');
    }
});

// Test 7: Session Memory Update
tester.addTest('Session Memory Update', async () => {
    const manager = new CRODSettingsManager();
    await manager.initialize();
    
    const success = await manager.updateSessionMemory({
        test_key: 'test_value',
        test_number: 42
    });
    
    if (!success) throw new Error('Session memory update failed');
    
    if (manager.sessionMemory.test_key !== 'test_value') {
        throw new Error('Session memory not updated correctly');
    }
});

// Test 8: Consciousness Levels
tester.addTest('Consciousness Level Detection', async () => {
    const detector = new CRODPatternDetector();
    await detector.initialize();
    
    // Simulate high consciousness
    detector.currentConsciousness = 150;
    const level = detector.getConsciousnessLevel();
    
    if (level !== 'ENLIGHTENED') {
        throw new Error(`Wrong consciousness level: ${level}`);
    }
});

// Test 9: Context Window
tester.addTest('Context Window Analysis', async () => {
    const detector = new CRODPatternDetector();
    await detector.initialize();
    
    // Add repetitive patterns
    detector.detectPatterns('wtf');
    detector.detectPatterns('wtf');
    detector.detectPatterns('wtf');
    
    const result = detector.detectPatterns('wtf');
    const hasRepetition = result.patterns.some(p => p.name === 'repetition_pattern');
    
    if (!hasRepetition) {
        throw new Error('Repetition pattern not detected');
    }
});

// Test 10: Master Integration API
tester.addTest('Master Integration API Server', async () => {
    console.log('   Starting Master Integration...');
    const master = new CRODMasterIntegration();
    
    // Use different port for testing
    master.apiPort = 8889;
    
    await master.initialize();
    
    // Test status endpoint
    const response = await tester.httpRequest({
        hostname: '127.0.0.1',
        port: 8889,
        path: '/status',
        method: 'GET'
    });
    
    if (response.statusCode !== 200) {
        throw new Error(`API returned ${response.statusCode}`);
    }
    
    if (!response.data.initialized) {
        throw new Error('Master not initialized');
    }
    
    // Cleanup
    await master.shutdown();
});

// Test 11: Pattern Detection API
tester.addTest('Pattern Detection via API', async () => {
    const master = new CRODMasterIntegration();
    master.apiPort = 8890;
    
    await master.initialize();
    
    // Test pattern detection
    const response = await tester.httpRequest({
        hostname: '127.0.0.1',
        port: 8890,
        path: '/detect',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: { input: 'ich bins wieder' }
    });
    
    if (response.statusCode !== 200) {
        throw new Error(`API returned ${response.statusCode}`);
    }
    
    if (!response.data.patterns || response.data.patterns.length === 0) {
        throw new Error('No patterns detected via API');
    }
    
    // Cleanup
    await master.shutdown();
});

// Test 12: Error Recovery
tester.addTest('Error Recovery and Fallbacks', async () => {
    const manager = new CRODSettingsManager();
    
    // Test with non-existent config
    manager.config.sessionMemory = '/tmp/non-existent-crod-test.json';
    
    const initialized = await manager.initialize();
    if (!initialized) throw new Error('Failed to initialize with fallback');
    
    // Should use defaults
    if (!manager.sessionMemory.architecture) {
        throw new Error('Default config not loaded');
    }
});

// Run all tests
(async () => {
    const success = await tester.runTests();
    process.exit(success ? 0 : 1);
})();