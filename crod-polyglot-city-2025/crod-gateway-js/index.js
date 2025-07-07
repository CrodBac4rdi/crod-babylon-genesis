const express = require('express');
const WebSocket = require('ws');
const { connect, StringCodec } = require('nats');
const cors = require('cors');
const http = require('http');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 7888;
const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';

// Initialize Express app
const app = express();
const server = http.createServer(app);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// WebSocket server
const wss = new WebSocket.Server({ server });

// NATS connection
let nc = null;
const sc = StringCodec();

// District routing configuration
const districts = {
  rathaus: { url: 'http://localhost:4000', ws: 'ws://localhost:4000/socket/websocket' },
  pattern: { url: 'http://localhost:7007', port: 7007 },
  memory: { url: 'http://localhost:7031', port: 7031 },
  parasit: { url: 'http://localhost:6666', port: 6666 }
};

// Connected WebSocket clients
const wsClients = new Set();

// Connect to NATS
async function connectNATS() {
  try {
    nc = await connect({ servers: NATS_URL });
    console.log('< Gateway connected to NATS');

    // Subscribe to all district events
    const sub = nc.subscribe('district.>', { queue: 'gateway' });
    (async () => {
      for await (const msg of sub) {
        const data = JSON.parse(sc.decode(msg.data));
        
        // Broadcast to all WebSocket clients
        broadcastToClients({
          type: 'nats_event',
          topic: msg.subject,
          data: data,
          timestamp: new Date().toISOString()
        });
      }
    })();

    // Subscribe to pattern events
    const patternSub = nc.subscribe('pattern.>');
    (async () => {
      for await (const msg of patternSub) {
        const data = JSON.parse(sc.decode(msg.data));
        
        broadcastToClients({
          type: 'pattern_event',
          topic: msg.subject,
          data: data,
          timestamp: new Date().toISOString()
        });
      }
    })();

    // Publish gateway status
    setInterval(async () => {
      const status = {
        service: 'gateway-js',
        type: 'district',
        status: 'active',
        language: 'javascript',
        port: PORT,
        connected_clients: wsClients.size,
        timestamp: new Date().toISOString()
      };
      
      await nc.publish('district.gateway.status', sc.encode(JSON.stringify(status)));
    }, 30000);

  } catch (err) {
    console.error('L Failed to connect to NATS:', err);
    setTimeout(connectNATS, 5000); // Retry after 5 seconds
  }
}

// Broadcast to all connected WebSocket clients
function broadcastToClients(data) {
  const message = JSON.stringify(data);
  wsClients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log(' New WebSocket client connected');
  wsClients.add(ws);

  // Send initial status
  ws.send(JSON.stringify({
    type: 'connected',
    message: 'Connected to CROD Gateway',
    districts: Object.keys(districts),
    timestamp: new Date().toISOString()
  }));

  // Handle client messages
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      
      // Handle different message types
      switch (data.type) {
        case 'ping':
          ws.send(JSON.stringify({ type: 'pong', timestamp: new Date().toISOString() }));
          break;
          
        case 'publish':
          if (nc && data.topic && data.payload) {
            await nc.publish(data.topic, sc.encode(JSON.stringify(data.payload)));
            ws.send(JSON.stringify({ type: 'published', topic: data.topic }));
          }
          break;
          
        case 'subscribe':
          // Client wants to subscribe to specific topics
          ws.send(JSON.stringify({ 
            type: 'subscribed', 
            topic: data.topic,
            message: 'You will receive events for this topic'
          }));
          break;
          
        default:
          ws.send(JSON.stringify({ type: 'error', message: 'Unknown message type' }));
      }
    } catch (err) {
      console.error('Error handling WebSocket message:', err);
      ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
    }
  });

  // Handle disconnection
  ws.on('close', () => {
    console.log('Client disconnected');
    wsClients.delete(ws);
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err);
    wsClients.delete(ws);
  });
});

// API Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'crod-gateway-js',
    port: PORT,
    nats_connected: nc !== null,
    websocket_clients: wsClients.size,
    timestamp: new Date().toISOString()
  });
});

// Get all districts status
app.get('/api/districts', async (req, res) => {
  const districtStatus = {};
  
  for (const [name, config] of Object.entries(districts)) {
    try {
      // Try to fetch health from each district
      const response = await fetch(`${config.url}/health`);
      if (response.ok) {
        districtStatus[name] = {
          status: 'online',
          port: config.port || 'unknown',
          url: config.url
        };
      } else {
        districtStatus[name] = {
          status: 'error',
          port: config.port || 'unknown',
          url: config.url
        };
      }
    } catch (err) {
      districtStatus[name] = {
        status: 'offline',
        port: config.port || 'unknown',
        url: config.url,
        error: err.message
      };
    }
  }
  
  res.json({
    districts: districtStatus,
    gateway: {
      port: PORT,
      websocket_clients: wsClients.size,
      nats_connected: nc !== null
    }
  });
});

// Proxy requests to districts
app.use('/api/:district/*', async (req, res) => {
  const { district } = req.params;
  const districtConfig = districts[district];
  
  if (!districtConfig) {
    return res.status(404).json({ error: 'District not found' });
  }
  
  try {
    const path = req.params[0];
    const url = `${districtConfig.url}/${path}`;
    
    // Forward the request
    const response = await fetch(url, {
      method: req.method,
      headers: req.headers,
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined
    });
    
    const data = await response.json();
    res.status(response.status).json(data);
    
  } catch (err) {
    res.status(502).json({ 
      error: 'Bad Gateway', 
      message: `Failed to reach ${district} district`,
      details: err.message 
    });
  }
});

// Serve index page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
async function start() {
  // Connect to NATS
  await connectNATS();
  
  // Start HTTP server
  server.listen(PORT, () => {
    console.log(`=€ CROD Gateway running on port ${PORT}`);
    console.log(`=á WebSocket server ready`);
    console.log(`< Dashboard: http://localhost:${PORT}`);
  });
}

// Handle shutdown gracefully
process.on('SIGTERM', async () => {
  console.log('Shutting down gateway...');
  
  // Close WebSocket connections
  wsClients.forEach(client => client.close());
  wss.close();
  
  // Close NATS connection
  if (nc) {
    await nc.drain();
  }
  
  // Close HTTP server
  server.close(() => {
    console.log('Gateway shutdown complete');
    process.exit(0);
  });
});

// Start the gateway
start().catch(console.error);