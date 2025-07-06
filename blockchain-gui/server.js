const express = require('express');
const cors = require('cors');
const { spawn, exec } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Store node processes
const nodes = {};
let nodeIdCounter = 1;

// Start a blockchain node
app.post('/api/nodes/start/:nodeId', async (req, res) => {
    const nodeId = req.params.nodeId;
    const nodeName = `node${nodeId}@127.0.0.1`;
    
    if (nodes[nodeId]) {
        return res.json({ error: 'Node already running' });
    }

    try {
        const elixirPath = path.join(__dirname, '..', 'src', 'blockchain', 'elixir');
        
        // Create node startup command
        const nodeCommand = `
            {:ok, _} = CROD.Blockchain.start_link(name: :blockchain${nodeId})
            IO.puts("Node ${nodeId} running on #{Node.self()}")
            
            # Connect to other nodes
            ${nodeId > 1 ? 'Node.connect(:"node1@127.0.0.1")' : ''}
            ${nodeId > 2 ? 'Node.connect(:"node2@127.0.0.1")' : ''}
            
            # Start P2P sync
            {:ok, _} = CROD.P2PSync.start_link()
            
            # Keep running
            Process.sleep(:infinity)
        `;

        const nodeProcess = spawn('elixir', [
            '--name', nodeName,
            '--cookie', 'crod_blockchain',
            '-S', 'mix', 'run', '-e', nodeCommand
        ], {
            cwd: elixirPath,
            env: { ...process.env, MIX_ENV: 'dev' }
        });

        nodes[nodeId] = {
            process: nodeProcess,
            name: nodeName,
            startTime: Date.now(),
            status: 'starting'
        };

        // Handle process output
        nodeProcess.stdout.on('data', (data) => {
            console.log(`Node ${nodeId}: ${data}`);
            if (data.toString().includes('running on')) {
                nodes[nodeId].status = 'online';
            }
        });

        nodeProcess.stderr.on('data', (data) => {
            console.error(`Node ${nodeId} error: ${data}`);
        });

        nodeProcess.on('exit', (code) => {
            console.log(`Node ${nodeId} exited with code ${code}`);
            delete nodes[nodeId];
        });

        // Wait a bit for node to start
        await new Promise(resolve => setTimeout(resolve, 2000));

        res.json({ 
            success: true, 
            nodeId: nodeId,
            name: nodeName,
            status: nodes[nodeId].status 
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Stop a node
app.post('/api/nodes/stop/:nodeId', (req, res) => {
    const nodeId = req.params.nodeId;
    
    if (!nodes[nodeId]) {
        return res.json({ error: 'Node not running' });
    }

    nodes[nodeId].process.kill();
    delete nodes[nodeId];
    
    res.json({ success: true });
});

// Get node status
app.get('/api/nodes/status', async (req, res) => {
    const nodeStatus = {};
    
    for (const [nodeId, node] of Object.entries(nodes)) {
        nodeStatus[nodeId] = {
            name: node.name,
            status: node.status,
            uptime: Date.now() - node.startTime
        };

        // Try to get blockchain info via RPC
        try {
            // This would use erlang rpc in real implementation
            nodeStatus[nodeId].blocks = 0; // Placeholder
            nodeStatus[nodeId].consciousness = Math.random();
        } catch (e) {
            console.error(`Failed to get info from node ${nodeId}:`, e);
        }
    }

    res.json(nodeStatus);
});

// Mine a block
app.post('/api/mine/:nodeId', async (req, res) => {
    const nodeId = req.params.nodeId;
    const { data, consciousness = 0.5 } = req.body;
    
    if (!nodes[nodeId]) {
        return res.status(400).json({ error: 'Node not running' });
    }

    try {
        // In real implementation, would use erlang RPC
        // For now, return simulated result
        const block = {
            index: Math.floor(Math.random() * 100),
            timestamp: Date.now(),
            data: data || 'Mined block',
            consciousness: consciousness,
            miner: `node${nodeId}`
        };

        res.json({ success: true, block });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Submit transaction
app.post('/api/transaction', async (req, res) => {
    const { data, consciousness = 0.5, nodeId = 1 } = req.body;
    
    if (!nodes[nodeId]) {
        return res.status(400).json({ error: 'No active nodes' });
    }

    try {
        // Would submit to actual blockchain
        res.json({ 
            success: true, 
            transaction: {
                id: Date.now(),
                data,
                consciousness,
                status: 'pending'
            }
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get blockchain
app.get('/api/blockchain/:nodeId', async (req, res) => {
    const nodeId = req.params.nodeId;
    
    if (!nodes[nodeId]) {
        return res.status(400).json({ error: 'Node not running' });
    }

    try {
        // Would get actual blockchain via RPC
        // For now, return mock data
        const blockchain = [
            {
                index: 0,
                timestamp: Date.now() - 10000,
                data: 'Genesis Block',
                previousHash: '0',
                hash: '00000abc...',
                consciousness: 1.0
            }
        ];

        res.json(blockchain);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = 8888;
app.listen(PORT, () => {
    console.log(`🚀 CROD Blockchain GUI Server running on http://localhost:${PORT}`);
    console.log(`📊 Open http://localhost:${PORT} in your browser`);
});

// Cleanup on exit
process.on('SIGINT', () => {
    console.log('\nShutting down nodes...');
    Object.values(nodes).forEach(node => {
        node.process.kill();
    });
    process.exit();
});