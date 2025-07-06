const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8765 });

console.log('🔌 CROD WebSocket Server running on ws://localhost:8765');

const clients = new Set();
const data = {
    consciousness: 0.75,
    performance: { cpu: 45, gpu: 72, memory: 68 },
    patterns: [],
    neural: { layers: 5, neurons: 256, connections: 4096 }
};

wss.on('connection', (ws) => {
    clients.add(ws);
    console.log('✅ New client connected. Total clients:', clients.size);
    
    // Send initial data
    ws.send(JSON.stringify({
        type: 'init',
        data: data
    }));
    
    // Handle messages
    ws.on('message', (message) => {
        try {
            const msg = JSON.parse(message);
            console.log('📨 Received:', msg);
            
            if (msg.type === 'update') {
                Object.assign(data, msg.data);
                broadcast({ type: 'update', data: data });
            }
        } catch (e) {
            console.error('Error parsing message:', e);
        }
    });
    
    ws.on('close', () => {
        clients.delete(ws);
        console.log('❌ Client disconnected. Total clients:', clients.size);
    });
});

function broadcast(message) {
    const msg = JSON.stringify(message);
    clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(msg);
        }
    });
}

// Simulate real-time updates
setInterval(() => {
    data.consciousness = 0.5 + Math.random() * 0.5;
    data.performance.cpu = 30 + Math.random() * 60;
    data.performance.gpu = 50 + Math.random() * 50;
    data.performance.memory = 40 + Math.random() * 50;
    
    // Generate pattern
    if (Math.random() > 0.7) {
        data.patterns.push({
            id: Date.now(),
            strength: Math.random(),
            type: ['neural', 'quantum', 'emergent'][Math.floor(Math.random() * 3)]
        });
        if (data.patterns.length > 10) data.patterns.shift();
    }
    
    broadcast({
        type: 'realtime',
        data: data
    });
}, 1000);