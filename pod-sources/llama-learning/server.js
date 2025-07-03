const express = require('express');
const redis = require('redis');
const WebSocket = require('ws');
const LLAMALearningSystem = require('./llama-learning-system');

const app = express();
app.use(express.json());

// Redis connection
const redisClient = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST || 'redis',
    port: 6379
  }
});

// WebSocket for real-time updates
const wss = new WebSocket.Server({ port: 8090 });

let llama;

// Initialize
async function init() {
  await redisClient.connect();
  console.log('📡 Connected to Redis');
  
  llama = new LLAMALearningSystem(redisClient);
  
  // Subscribe to events
  const subscriber = redisClient.duplicate();
  await subscriber.connect();
  
  await subscriber.subscribe('claude:action', async (message) => {
    const data = JSON.parse(message);
    await llama.observeClaudeAction(data);
  });
  
  await subscriber.subscribe('daniel:reaction', async (message) => {
    const data = JSON.parse(message);
    await llama.learnFromDanielReaction(data.reaction, data.lastAction);
  });
  
  console.log('🦙 LLAMA Learning System ready!');
}

// REST API

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    district: 'llama-learning',
    version: '1.0.0'
  });
});

app.post('/observe', async (req, res) => {
  try {
    const observation = await llama.observeClaudeAction(req.body);
    res.json(observation);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/learn', async (req, res) => {
  try {
    const { reaction, lastAction } = req.body;
    const learning = await llama.learnFromDanielReaction(reaction, lastAction);
    
    // Broadcast to WebSocket clients
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'learning',
          data: learning
        }));
      }
    });
    
    res.json(learning);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/suggest', async (req, res) => {
  try {
    const suggestion = await llama.suggestAction(req.body);
    res.json(suggestion);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/stats', async (req, res) => {
  try {
    const stats = {
      observations: await redisClient.lLen('llama:observations'),
      learnings: await redisClient.lLen('llama:learnings'),
      networkScores: await redisClient.hGetAll('llama:network:scores'),
      patterns: {
        successful: llama.cache.successfulPatterns.length,
        failed: llama.cache.failedPatterns.length
      }
    };
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// WebSocket handling
wss.on('connection', (ws) => {
  console.log('🔌 New WebSocket connection');
  
  ws.send(JSON.stringify({
    type: 'connected',
    message: 'LLAMA Learning System connected'
  }));
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      
      switch(data.type) {
        case 'observe':
          await llama.observeClaudeAction(data.action);
          break;
        case 'learn':
          await llama.learnFromDanielReaction(data.reaction, data.lastAction);
          break;
        case 'suggest':
          const suggestion = await llama.suggestAction(data.context);
          ws.send(JSON.stringify({
            type: 'suggestion',
            data: suggestion
          }));
          break;
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
const PORT = process.env.PORT || 8089;
app.listen(PORT, async () => {
  await init();
  console.log(`🦙 LLAMA Learning District running on port ${PORT}`);
  console.log(`🔌 WebSocket on port 8090`);
});