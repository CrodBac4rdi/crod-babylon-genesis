/**
 * CROD Clean System Test
 * Tests all major components
 */

const axios = require('axios');
const WebSocket = require('ws');

const SERVICES = {
    core: 'http://localhost:3000',
    visualization: 'http://localhost:5000',
    performance: 'http://localhost:8080',
    websocket: 'ws://localhost:8765'
};

async function testService(name, url, endpoint = '/health') {
    try {
        const response = await axios.get(url + endpoint);
        console.log(`✅ ${name}: OK (${response.status})`);
        return true;
    } catch (error) {
        console.log(`❌ ${name}: Failed (${error.message})`);
        return false;
    }
}

async function testWebSocket() {
    return new Promise((resolve) => {
        const ws = new WebSocket(SERVICES.websocket);
        
        ws.on('open', () => {
            console.log('✅ WebSocket: Connected');
            ws.close();
            resolve(true);
        });
        
        ws.on('error', (err) => {
            console.log(`❌ WebSocket: Failed (${err.message})`);
            resolve(false);
        });
        
        setTimeout(() => {
            ws.close();
            resolve(false);
        }, 5000);
    });
}

async function runTests() {
    console.log('🧪 Testing CROD Clean System...\n');
    
    const results = [];
    
    // Test Core API
    results.push(await testService('Core API', SERVICES.core, '/api/status'));
    
    // Test Visualization
    results.push(await testService('Visualization', SERVICES.visualization, '/api/status'));
    
    // Test Performance Backend
    results.push(await testService('Performance', SERVICES.performance, '/health'));
    
    // Test WebSocket
    results.push(await testWebSocket());
    
    // Test specific endpoints
    console.log('\n📊 Testing Specific Endpoints...\n');
    
    try {
        // Test Neural Processing
        const neuralResponse = await axios.post(SERVICES.core + '/api/neural/process', {
            input: 'test pattern'
        });
        console.log('✅ Neural Processing: OK');
        console.log(`   Patterns found: ${neuralResponse.data.patterns.length}`);
        console.log(`   Confidence: ${neuralResponse.data.confidence.toFixed(2)}`);
    } catch (err) {
        console.log('❌ Neural Processing: Failed');
    }
    
    try {
        // Test Visualization Generation
        const vizResponse = await axios.get(SERVICES.core + '/api/visualization/generate');
        console.log('✅ Visualization Generation: OK');
        console.log(`   Type: ${vizResponse.data.type}`);
        console.log(`   Animated: ${vizResponse.data.animated}`);
    } catch (err) {
        console.log('❌ Visualization Generation: Failed');
    }
    
    // Summary
    const passed = results.filter(r => r).length;
    const total = results.length;
    
    console.log('\n📈 Test Summary:');
    console.log(`   Passed: ${passed}/${total}`);
    console.log(`   Success Rate: ${((passed/total) * 100).toFixed(0)}%`);
    
    process.exit(passed === total ? 0 : 1);
}

// Add delay to allow services to start
setTimeout(runTests, 3000);