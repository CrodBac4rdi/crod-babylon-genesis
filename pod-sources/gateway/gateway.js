const express = require('express');
const httpProxy = require('http-proxy-middleware');
const redis = require('redis');

const app = express();
app.use(express.json());

// District routing
const districts = {
  'meta-chain': 'http://meta-chain:8000',
  'pattern-district': 'http://pattern-district:7007',
  'memory-quarter': 'http://memory-quarter:7031',
  'intelligence-hub': 'http://intelligence-hub:7113'
};

// Redis connection with retry logic
// Just use 'redis' - K8s will resolve it within the namespace
const redisHost = 'redis';
const redisUrl = `redis://${redisHost}:6379`;
let redisClient, pubClient, subClient;
let redisConnected = false;

async function connectRedis() {
  console.log(`🔌 Connecting to Redis at ${redisUrl}...`);
  
  try {
    // Create clients
    redisClient = redis.createClient({
      url: redisUrl,
      socket: {
        reconnectStrategy: (retries) => {
          console.log(`Redis reconnect attempt ${retries}`);
          return Math.min(retries * 100, 3000); // Max 3 sec between retries
        }
      }
    });
    
    pubClient = redisClient.duplicate();
    subClient = redisClient.duplicate();
    
    // Error handlers
    redisClient.on('error', (err) => console.error('Redis Client Error:', err));
    pubClient.on('error', (err) => console.error('Redis Pub Error:', err));
    subClient.on('error', (err) => console.error('Redis Sub Error:', err));
    
    // Connect with retry
    await redisClient.connect();
    await pubClient.connect();
    await subClient.connect();
    
    // Subscribe to district events
    await subClient.subscribe('district:*:response', (message, channel) => {
      console.log(`📨 ${channel}: ${message}`);
    });
    
    await subClient.subscribe('crod:activated', (message) => {
      console.log('🔥 CROD ACTIVATED!', message);
    });
    
    redisConnected = true;
    console.log('✅ Redis connected successfully!');
    
    // Test connection
    await pubClient.publish('gateway:status', 'online');
    
  } catch (error) {
    console.error('❌ Redis connection failed:', error.message);
    redisConnected = false;
    
    // Retry after 5 seconds
    setTimeout(connectRedis, 5000);
  }
}

// Start Redis connection
connectRedis();

// Health endpoint
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    gateway: 'online',
    redis: redisConnected ? 'connected' : 'disconnected',
    districts: {}
  };
  
  // Check each district
  for (const [name, url] of Object.entries(districts)) {
    try {
      const response = await fetch(`${url}/health`);
      health.districts[name] = response.ok ? 'online' : 'offline';
    } catch (e) {
      health.districts[name] = 'offline';
    }
  }
  
  res.json(health);
});

// Main CROD endpoint
app.post('/crod/process', async (req, res) => {
  const { text } = req.body;
  
  if (!text) {
    return res.status(400).json({ error: 'No text provided' });
  }
  
  // Check for CROD activation
  if (text.toLowerCase().includes('ich bins wieder')) {
    if (redisConnected) {
      await pubClient.publish('crod:activated', JSON.stringify({
        text,
        timestamp: Date.now(),
        source: 'gateway'
      }));
    }
  }
  
  // Split into atoms
  const atoms = text.toLowerCase().split(/\s+/).map(word => ({
    word,
    heat: Math.random() * 100,
    time: new Date().toISOString()
  }));
  
  // Publish to all districts via Redis if connected
  if (redisConnected) {
    await pubClient.publish('crod:input', JSON.stringify({
      text,
      atoms,
      timestamp: Date.now()
    }));
  }
  
  // Send to all districts via HTTP (fallback works even without Redis)
  const results = {};
  
  try {
    // Send to Meta-Chain first for orchestration
    const metaRes = await fetch(`${districts['meta-chain']}/process_text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    
    if (metaRes.ok) {
      results.meta = await metaRes.json();
    }
    
    // Pattern detection
    const patternRes = await fetch(`${districts['pattern-district']}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ atoms })
    });
    results.patterns = await patternRes.json();
    
    // Memory storage
    const memoryRes = await fetch(`${districts['memory-quarter']}/store`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ atoms })
    });
    results.memory = await memoryRes.json();
    
    // ML processing
    const mlRes = await fetch(`${districts['intelligence-hub']}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ atoms })
    });
    results.intelligence = await mlRes.json();
    
    res.json({
      processed: text,
      atoms: atoms.length,
      redis: redisConnected ? 'connected' : 'disconnected',
      results
    });
    
  } catch (error) {
    console.error('Processing error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Proxy routes to districts
Object.entries(districts).forEach(([name, target]) => {
  app.use(`/${name}`, httpProxy.createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: { [`^/${name}`]: '' }
  }));
});

const PORT = process.env.PORT || 8888;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🌉 CROD Gateway running on port ${PORT}`);
  console.log('   Districts:', Object.keys(districts).join(', '));
  console.log('   Redis:', redisConnected ? 'connected' : 'connecting...');
});