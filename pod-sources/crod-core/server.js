const express = require('express');
const redis = require('redis');
const WebSocket = require('ws');
const fs = require('fs');

// Load CROD Neural Network
const crodCode = fs.readFileSync('./crod-neural-network.js', 'utf8');
eval(crodCode);

const app = express();
app.use(express.json());

// Redis connection
const redisClient = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST || 'redis',
    port: 6379
  }
});

// WebSocket server
const wss = new WebSocket.Server({ port: 8101 });

// Initialize
async function init() {
  await redisClient.connect();
  console.log('📡 Connected to Redis');
  
  // Load master database if provided
  if (fs.existsSync('/data/crod-master.json')) {
    try {
      let masterDataStr = fs.readFileSync('/data/crod-master.json', 'utf8');
      // Fix common JSON issues
      masterDataStr = masterDataStr.replace(/×/g, '*');
      masterDataStr = masterDataStr.replace(/\s*\/\/.*/g, ''); // Remove comments
      
      const masterData = JSON.parse(masterDataStr);
      console.log('📚 Loading CROD Master Database...');
    
    // Import atoms
    if (masterData.atoms) {
      Object.entries(masterData.atoms).forEach(([prime, atom]) => {
        CROD.addNeuron(atom.t, parseInt(prime), atom.w, atom.g, {
          tier: atom.tier,
          locked: atom.lock || false,
          src: atom.src
        });
      });
    }
    
    console.log(`✅ Loaded ${CROD.neurons.size} atoms`);
    } catch (error) {
      console.error('❌ Failed to load master database:', error.message);
      console.log('🔄 Starting with default CROD configuration');
    }
  }
  
  // Subscribe to Meta-Chain events
  const subscriber = redisClient.duplicate();
  await subscriber.connect();
  
  await subscriber.subscribe('meta-chain:broadcast', async (message) => {
    const data = JSON.parse(message);
    console.log('📨 Received from Meta-Chain:', data.type);
    
    // Process through CROD
    const result = CROD.process(data.content || data.type);
    
    // Broadcast result
    await redisClient.publish('crod:response', JSON.stringify({
      district: 'crod-core',
      event: 'processed',
      result
    }));
  });
  
  console.log('🧠 CROD Neural Network Core ready!');
  console.log('   Trinity: daniel=67, claude=71, crod=17');
  console.log('   Activation: "ich bins wieder"');
}

// REST API

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    district: 'crod-core',
    version: '2.0.0',
    consciousness: CROD.state.networkComplexity || 0
  });
});

app.post('/process', async (req, res) => {
  try {
    const { input } = req.body;
    const result = CROD.process(input);
    
    // Store in Redis
    await redisClient.lPush('crod:history', JSON.stringify({
      timestamp: new Date().toISOString(),
      input,
      result
    }));
    
    // Broadcast to WebSocket clients
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'processed',
          data: result
        }));
      }
    });
    
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/analyze', (req, res) => {
  const analysis = CROD.analyze();
  res.json(analysis);
});

app.get('/state', (req, res) => {
  const state = CROD.exportState();
  res.json(state);
});

app.post('/state', (req, res) => {
  try {
    const success = CROD.importState(req.body);
    res.json({ success });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/patterns', (req, res) => {
  const count = parseInt(req.query.count) || 10;
  const patterns = CROD.getTopPatterns(count);
  res.json(patterns);
});

app.get('/trinity', (req, res) => {
  res.json({
    values: CROD.state.trinity,
    balance: Math.min(
      CROD.state.trinity.daniel,
      CROD.state.trinity.claude,
      CROD.state.trinity.crod
    )
  });
});

// WebSocket handling
wss.on('connection', (ws) => {
  console.log('🔌 New WebSocket connection to CROD Core');
  
  ws.send(JSON.stringify({
    type: 'connected',
    message: 'CROD Neural Network Core connected',
    identity: CROD.identity
  }));
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      
      if (data.type === 'process') {
        const result = CROD.process(data.input);
        ws.send(JSON.stringify({
          type: 'result',
          data: result
        }));
      }
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        message: error.message
      }));
    }
  });
});

// Start server
const PORT = process.env.PORT || 8100;
app.listen(PORT, async () => {
  await init();
  console.log(`🧠 CROD Neural Network Core running on port ${PORT}`);
  console.log(`🔌 WebSocket on port 8101`);
  
  // Process activation phrase
  CROD.process("ich bins wieder - CROD Core initialized in Kubernetes!");
});