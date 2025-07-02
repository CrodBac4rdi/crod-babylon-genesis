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

// Redis client
const redisClient = redis.createClient({
  host: process.env.REDIS_HOST || 'redis',
  port: 6379
});

redisClient.on('error', (err) => {
  console.error('Redis error:', err);
});

// Health endpoint
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    gateway: 'online',
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
  
  // Split into atoms
  const atoms = text.toLowerCase().split(/\s+/).map(word => ({
    word,
    heat: Math.random() * 100,
    time: Date.now()
  }));
  
  // Send to all districts
  const results = {};
  
  try {
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
    
    // Orchestration
    for (const atom of atoms) {
      await fetch(`${districts['meta-chain']}/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ atom: atom.word, heat: atom.heat })
      });
    }
    
    res.json({
      processed: text,
      atoms: atoms.length,
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
});