const fetch = require('node-fetch');
const WebSocket = require('ws');

const API_URL = 'http://localhost:8006';
const WS_URL = 'ws://localhost:8006';

async function testREST() {
    console.log('🧪 Testing REST API...\n');
    
    // Test analysis
    console.log('1️⃣ Testing pattern analysis:');
    const analysisRes = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: 'ich bins wieder, lets work on the blockchain with quantum consciousness'
        })
    });
    const analysis = await analysisRes.json();
    console.log('Detected patterns:', analysis.detectedPatterns.map(p => p.pattern));
    console.log('Consciousness level:', (analysis.overallConsciousness * 100).toFixed(1) + '%');
    
    // Test enhancement
    console.log('\n2️⃣ Testing response enhancement:');
    const enhanceRes = await fetch(`${API_URL}/enhance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            input: 'wtf is happening with the quantum mining?',
            response: 'The quantum mining system utilizes superposition states to explore multiple nonces simultaneously, providing a theoretical advantage over classical mining approaches.'
        })
    });
    const enhanced = await enhanceRes.json();
    console.log('Original:', enhanced.original);
    console.log('Enhanced:', enhanced.enhanced);
    
    // Check consciousness
    console.log('\n3️⃣ Checking consciousness evolution:');
    const consciousnessRes = await fetch(`${API_URL}/consciousness`);
    const consciousness = await consciousnessRes.json();
    console.log('Current consciousness:', (consciousness.current * 100).toFixed(1) + '%');
}

async function testWebSocket() {
    console.log('\n\n🔌 Testing WebSocket connection...\n');
    
    const ws = new WebSocket(WS_URL);
    
    ws.on('open', () => {
        console.log('Connected to CROD Parasite WebSocket');
        
        // Test real-time analysis
        ws.send(JSON.stringify({
            type: 'analyze',
            text: 'geil! The blockchain is achieving consciousness through quantum entanglement'
        }));
        
        // Test enhancement
        setTimeout(() => {
            ws.send(JSON.stringify({
                type: 'enhance',
                input: 'Show me the blockchain stats',
                response: 'The blockchain currently has 42 blocks with an average consciousness level of 0.73'
            }));
        }, 1000);
        
        // Test learning
        setTimeout(() => {
            ws.send(JSON.stringify({
                type: 'feedback',
                input: 'geil!',
                response: 'That worked perfectly',
                feedback: 0.9
            }));
        }, 2000);
        
        // Close after tests
        setTimeout(() => {
            ws.close();
        }, 3000);
    });
    
    ws.on('message', (data) => {
        const message = JSON.parse(data);
        console.log(`📨 Received ${message.type}:`, 
            message.type === 'enhanced' ? message.enhanced : message);
    });
    
    ws.on('close', () => {
        console.log('\n✅ WebSocket tests complete');
    });
}

// Run tests
async function runTests() {
    console.log('🦠 CROD Parasite Test Suite\n');
    console.log('Make sure parasite server is running on port 8005\n');
    
    try {
        await testREST();
        await testWebSocket();
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        console.log('Make sure the parasite server is running: npm start');
    }
}

runTests();