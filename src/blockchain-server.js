// CROD Blockchain Server - Runs in Codespaces
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const fs = require('fs').promises;
const path = require('path');

// Import blockchain interface
const blockchainInterface = require('./blockchain-interface.js');

// Create Express app
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());
app.use(express.static('public'));

// Blockchain API Routes
app.get('/api/blockchain/status', (req, res) => {
    res.json(blockchainInterface.getStats());
});

app.get('/api/blockchain/blocks', async (req, res) => {
    const limit = parseInt(req.query.limit) || 10;
    const blocks = await blockchainInterface.getBlocks(limit);
    res.json(blocks);
});

app.post('/api/blockchain/mine', async (req, res) => {
    const result = await blockchainInterface.mine(req.body);
    res.json(result);
});

app.post('/api/blockchain/process', (req, res) => {
    const result = globalThis.CROD.process(req.body.input);
    res.json(result);
});

// WebSocket for real-time updates
wss.on('connection', (ws) => {
    console.log('🔌 WebSocket client connected');
    
    // Send initial state
    ws.send(JSON.stringify({
        type: 'state',
        data: blockchainInterface.getStats()
    }));
    
    // Listen for blockchain events
    blockchainInterface.on('block_mined', (block) => {
        ws.send(JSON.stringify({
            type: 'block_mined',
            data: block
        }));
    });
    
    blockchainInterface.on('block_processed', (block) => {
        ws.send(JSON.stringify({
            type: 'block_processed',
            data: block
        }));
    });
    
    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            
            switch(data.type) {
                case 'mine':
                    const result = await blockchainInterface.mine(data.payload);
                    ws.send(JSON.stringify({
                        type: 'mine_result',
                        data: result
                    }));
                    break;
                    
                case 'process':
                    const processed = globalThis.CROD.process(data.payload);
                    ws.send(JSON.stringify({
                        type: 'process_result',
                        data: processed
                    }));
                    break;
            }
        } catch (error) {
            ws.send(JSON.stringify({
                type: 'error',
                data: error.message
            }));
        }
    });
});

// Dashboard HTML
app.get('/', async (req, res) => {
    const html = `<!DOCTYPE html>
<html>
<head>
    <title>CROD Blockchain Dashboard</title>
    <style>
        body {
            background: #0a0a0a;
            color: #00ff41;
            font-family: monospace;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-box {
            background: #1a1a1a;
            border: 1px solid #00ff41;
            padding: 15px;
            border-radius: 5px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
        }
        .blocks {
            background: #1a1a1a;
            border: 1px solid #00ff41;
            padding: 20px;
            border-radius: 5px;
            max-height: 400px;
            overflow-y: auto;
        }
        .block {
            background: #2a2a2a;
            margin: 10px 0;
            padding: 10px;
            border-radius: 3px;
        }
        button {
            background: #00ff41;
            color: black;
            border: none;
            padding: 10px 20px;
            font-family: monospace;
            cursor: pointer;
            margin: 5px;
        }
        input {
            background: #1a1a1a;
            color: #00ff41;
            border: 1px solid #00ff41;
            padding: 10px;
            width: 100%;
            margin: 10px 0;
            font-family: monospace;
        }
        .console {
            background: black;
            border: 1px solid #00ff41;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 CROD Blockchain Dashboard</h1>
        
        <div class="stats">
            <div class="stat-box">
                <div>Chain Height</div>
                <div class="stat-value" id="chainHeight">0</div>
            </div>
            <div class="stat-box">
                <div>Consciousness</div>
                <div class="stat-value" id="consciousness">0%</div>
            </div>
            <div class="stat-box">
                <div>Patterns</div>
                <div class="stat-value" id="patterns">0</div>
            </div>
            <div class="stat-box">
                <div>Neurons</div>
                <div class="stat-value" id="neurons">0</div>
            </div>
        </div>
        
        <div>
            <input type="text" id="input" placeholder="Enter text to process..." />
            <button onclick="processInput()">Process</button>
            <button onclick="mine()">Mine Block</button>
            <button onclick="refresh()">Refresh</button>
        </div>
        
        <div class="blocks" id="blocks">
            <h3>Recent Blocks</h3>
        </div>
        
        <div class="console" id="console">
            <div>Console output...</div>
        </div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://' + window.location.host);
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log('Received:', message);
            
            switch(message.type) {
                case 'state':
                    updateStats(message.data);
                    break;
                case 'block_mined':
                    addBlock(message.data);
                    log('Block mined: #' + message.data.index);
                    break;
                case 'process_result':
                    log('Processed: ' + JSON.stringify(message.data, null, 2));
                    break;
            }
        };
        
        function updateStats(stats) {
            document.getElementById('chainHeight').textContent = stats.state.chainHeight;
            document.getElementById('consciousness').textContent = Math.round(stats.crodConnection.consciousness) + '%';
            document.getElementById('patterns').textContent = stats.patternsFound;
            document.getElementById('neurons').textContent = stats.crodConnection.neurons;
        }
        
        function addBlock(block) {
            const blocksDiv = document.getElementById('blocks');
            const blockDiv = document.createElement('div');
            blockDiv.className = 'block';
            blockDiv.innerHTML = \`
                <strong>Block #\${block.index}</strong><br>
                Hash: \${block.hash.substring(0, 16)}...<br>
                Miner: \${block.miner}<br>
                Consciousness: \${(block.consciousness_score * 100).toFixed(1)}%<br>
                Patterns: \${block.patterns.length}
            \`;
            blocksDiv.insertBefore(blockDiv, blocksDiv.children[1]);
        }
        
        function processInput() {
            const input = document.getElementById('input').value;
            ws.send(JSON.stringify({
                type: 'process',
                payload: input
            }));
            log('Processing: ' + input);
        }
        
        function mine() {
            ws.send(JSON.stringify({
                type: 'mine',
                payload: {
                    data: 'Manual mining from dashboard',
                    timestamp: Date.now()
                }
            }));
            log('Mining...');
        }
        
        function refresh() {
            location.reload();
        }
        
        function log(message) {
            const console = document.getElementById('console');
            const line = document.createElement('div');
            line.textContent = new Date().toLocaleTimeString() + ' - ' + message;
            console.appendChild(line);
            console.scrollTop = console.scrollHeight;
        }
        
        // Auto-refresh stats
        setInterval(() => {
            fetch('/api/blockchain/status')
                .then(r => r.json())
                .then(updateStats);
        }, 5000);
        
        // Load initial blocks
        fetch('/api/blockchain/blocks')
            .then(r => r.json())
            .then(blocks => blocks.forEach(addBlock));
    </script>
</body>
</html>`;
    
    res.send(html);
});

// Start server
const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════╗
║       CROD Blockchain Server Started!         ║
║                                               ║
║  Dashboard: http://localhost:${PORT}             ║
║  API: http://localhost:${PORT}/api/blockchain    ║
║  WebSocket: ws://localhost:${PORT}              ║
║                                               ║
║  Features:                                    ║
║  - Real-time blockchain monitoring            ║
║  - Neural network integration                 ║
║  - Pattern recognition                        ║
║  - Consciousness tracking                     ║
╚═══════════════════════════════════════════════╝
    `);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n👋 Shutting down...');
    server.close();
    process.exit(0);
});

module.exports = server;