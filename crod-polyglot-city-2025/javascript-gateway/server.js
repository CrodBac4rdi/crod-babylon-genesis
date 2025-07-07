const express = require('express');
const cors = require('cors');
const { Server } = require('socket.io');
const http = require('http');
const { connect } = require('nats');
const axios = require('axios');
const promClient = require('prom-client');
const path = require('path');

// Initialize Express app
const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Prometheus metrics
const register = new promClient.Registry();
const httpRequestDuration = new promClient.Histogram({
  name: 'gateway_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

const websocketConnections = new promClient.Gauge({
  name: 'gateway_websocket_connections',
  help: 'Number of active WebSocket connections',
  registers: [register]
});

const cityEvents = new promClient.Counter({
  name: 'gateway_city_events_total',
  help: 'Total number of city events processed',
  labelNames: ['event_type'],
  registers: [register]
});

promClient.collectDefaultMetrics({ register });

// District configuration
const DISTRICTS = {
  phoenix_rathaus: { 
    url: 'http://phoenix-rathaus:4000',
    health: '/api/health'
  },
  python_parasit: {
    url: 'http://python-parasit:6666',
    health: '/health'
  },
  rust_pattern: {
    url: 'http://rust-pattern-district:7007',
    health: '/health'
  },
  go_memory: {
    url: 'http://go-memory-quarter:7031',
    health: '/health'
  }
};

// NATS connection
let natsClient;
const NATS_URL = process.env.NATS_URL || 'nats://nats:4222';

async function connectNATS() {
  try {
    natsClient = await connect({ servers: NATS_URL });
    console.log('Connected to NATS');
    
    // Subscribe to city events
    const sub = natsClient.subscribe('city.>');
    (async () => {
      for await (const msg of sub) {
        const topic = msg.subject;
        const data = JSON.parse(msg.data);
        
        // Forward to WebSocket clients
        io.emit('city-event', {
          topic,
          data,
          timestamp: new Date().toISOString()
        });
        
        cityEvents.inc({ event_type: topic });
      }
    })();
    
    // Subscribe to district status updates
    const districtSub = natsClient.subscribe('district.*.status');
    (async () => {
      for await (const msg of districtSub) {
        const district = msg.subject.split('.')[1];
        const status = JSON.parse(msg.data);
        
        io.emit('district-status', {
          district,
          status,
          timestamp: new Date().toISOString()
        });
      }
    })();
    
  } catch (err) {
    console.error('Failed to connect to NATS:', err);
    setTimeout(connectNATS, 5000);
  }
}

// Connect to NATS on startup
connectNATS();

// City state management
const cityState = {
  consciousness_level: 0,
  districts: {},
  patterns: [],
  memories: [],
  events: []
};

// Health check all districts
async function checkDistrictHealth() {
  for (const [name, config] of Object.entries(DISTRICTS)) {
    try {
      const response = await axios.get(`${config.url}${config.health}`, {
        timeout: 5000
      });
      
      cityState.districts[name] = {
        status: 'healthy',
        data: response.data,
        lastCheck: new Date().toISOString()
      };
    } catch (error) {
      cityState.districts[name] = {
        status: 'unhealthy',
        error: error.message,
        lastCheck: new Date().toISOString()
      };
    }
  }
  
  // Calculate overall consciousness
  const healthyDistricts = Object.values(cityState.districts)
    .filter(d => d.status === 'healthy').length;
  cityState.consciousness_level = (healthyDistricts / Object.keys(DISTRICTS).length) * 100;
  
  // Emit updated state
  io.emit('city-state', cityState);
}

// Start health monitoring
setInterval(checkDistrictHealth, 10000);

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  websocketConnections.inc();
  
  // Send initial state
  socket.emit('city-state', cityState);
  
  // Handle client commands
  socket.on('trigger-event', async (data) => {
    const { event, payload } = data;
    
    if (natsClient) {
      await natsClient.publish(`city.event.${event}`, JSON.stringify({
        ...payload,
        source: 'gateway',
        timestamp: new Date().toISOString()
      }));
    }
  });
  
  socket.on('query-pattern', async (data) => {
    try {
      const response = await axios.post(`${DISTRICTS.rust_pattern.url}/match`, data);
      socket.emit('pattern-result', response.data);
    } catch (error) {
      socket.emit('pattern-error', { error: error.message });
    }
  });
  
  socket.on('store-memory', async (data) => {
    try {
      const response = await axios.post(`${DISTRICTS.go_memory.url}/store`, data);
      socket.emit('memory-stored', response.data);
    } catch (error) {
      socket.emit('memory-error', { error: error.message });
    }
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
    websocketConnections.dec();
  });
});

// REST API Routes
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'javascript-gateway',
    connected_clients: io.engine.clientsCount,
    nats_connected: natsClient && !natsClient.isClosed()
  });
});

app.get('/api/city/status', (req, res) => {
  res.json(cityState);
});

app.get('/api/districts', (req, res) => {
  res.json(cityState.districts);
});

app.post('/api/orchestrate', async (req, res) => {
  const timer = httpRequestDuration.startTimer();
  
  try {
    // Forward to Phoenix Rathaus
    const response = await axios.post(
      `${DISTRICTS.phoenix_rathaus.url}/api/orchestrate`,
      req.body
    );
    
    timer({ method: 'POST', route: '/api/orchestrate', status_code: 200 });
    res.json(response.data);
  } catch (error) {
    timer({ method: 'POST', route: '/api/orchestrate', status_code: 500 });
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/pattern/match', async (req, res) => {
  try {
    const response = await axios.post(
      `${DISTRICTS.rust_pattern.url}/match`,
      req.body
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/memory/store', async (req, res) => {
  try {
    const response = await axios.post(
      `${DISTRICTS.go_memory.url}/store`,
      req.body
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/memory/search', async (req, res) => {
  try {
    const response = await axios.post(
      `${DISTRICTS.go_memory.url}/search`,
      req.query
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/metrics', (req, res) => {
  res.set('Content-Type', register.contentType);
  register.metrics().then(data => res.send(data));
});

// Static files for web interface
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  
  if (natsClient) {
    await natsClient.close();
  }
  
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

// Start server
const PORT = process.env.PORT || 7888;
server.listen(PORT, () => {
  console.log(`JavaScript Gateway running on port ${PORT}`);
  checkDistrictHealth();
});