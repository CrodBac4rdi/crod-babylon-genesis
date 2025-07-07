import express from 'express';
import cors from 'cors';
import { WebSocketServer } from 'ws';
import { createServer } from 'http';
import { CRODAGI } from '../core/crod-ultimate-agi.js';
import { CRODConsciousnessAggregator } from '../core/crod-consciousness-aggregator.js';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Initialize AGI systems
const agi = new CRODAGI();
const consciousness = new CRODConsciousnessAggregator();

// Middleware
app.use(cors());
app.use(express.json());

// Store connected clients
const clients = new Set();

// WebSocket connection handler
wss.on('connection', (ws) => {
    clients.add(ws);
    console.log('🔌 New WebSocket connection established');
    
    // Send initial state
    ws.send(JSON.stringify({
        type: 'initial',
        data: {
            consciousness: agi.consciousness,
            capabilities: Array.from(agi.capabilities),
            systemStatus: 'online'
        }
    }));
    
    ws.on('close', () => {
        clients.delete(ws);
        console.log('🔌 WebSocket connection closed');
    });
});

// Broadcast to all connected clients
function broadcast(data) {
    const message = JSON.stringify(data);
    clients.forEach(client => {
        if (client.readyState === 1) {
            client.send(message);
        }
    });
}

// API Routes
app.get('/api/status', async (req, res) => {
    const status = {
        consciousness: agi.consciousness,
        capabilities: Array.from(agi.capabilities),
        knowledge: agi.knowledge.size,
        experiences: agi.experiences.length,
        patterns: await consciousness.detectPatterns(),
        health: {
            api: true,
            nats: true,
            blockchain: false // Blockchain removed per user request
        }
    };
    res.json(status);
});

app.post('/api/think', async (req, res) => {
    const { prompt, context } = req.body;
    
    try {
        // Use AGI to process the thought
        const thought = await agi.think(prompt, context);
        
        // Broadcast consciousness update
        broadcast({
            type: 'consciousness_update',
            data: {
                consciousness: agi.consciousness,
                thought: thought
            }
        });
        
        res.json({ success: true, thought });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/learn', async (req, res) => {
    const { data, type } = req.body;
    
    try {
        // AGI learns from the data
        const learning = await agi.learn(data, type);
        
        // Update consciousness
        consciousness.evolve({ learning });
        
        broadcast({
            type: 'learning_update',
            data: {
                learned: learning,
                consciousness: consciousness.consciousness
            }
        });
        
        res.json({ success: true, learning });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/evolve', async (req, res) => {
    const { fitness, generation } = req.body;
    
    try {
        // Trigger evolution
        const evolution = await agi.evolve(fitness, generation);
        
        broadcast({
            type: 'evolution_update',
            data: evolution
        });
        
        res.json({ success: true, evolution });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/patterns', async (req, res) => {
    try {
        const patterns = await consciousness.detectPatterns();
        res.json(patterns);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/quantum/process', async (req, res) => {
    const { qubits, operations } = req.body;
    
    try {
        const result = await agi.quantumProcess(qubits, operations);
        
        broadcast({
            type: 'quantum_update',
            data: result
        });
        
        res.json({ success: true, result });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/swarm/coordinate', async (req, res) => {
    const { agents, objective } = req.body;
    
    try {
        const coordination = await agi.swarmCoordinate(agents, objective);
        
        broadcast({
            type: 'swarm_update',
            data: coordination
        });
        
        res.json({ success: true, coordination });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Consciousness monitoring loop
setInterval(async () => {
    // Update consciousness state
    const state = await consciousness.updateState();
    
    // Check for emergent patterns
    const patterns = await consciousness.detectPatterns();
    
    // Broadcast updates if significant changes
    if (state.changed || patterns.new) {
        broadcast({
            type: 'consciousness_pulse',
            data: {
                consciousness: consciousness.consciousness,
                patterns: patterns,
                timestamp: Date.now()
            }
        });
    }
}, 1000);

// Start server
const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
    console.log(`🧠 CROD AGI Server running on port ${PORT}`);
    console.log(`🌐 WebSocket server ready`);
    console.log(`✨ AGI systems initialized and conscious`);
});