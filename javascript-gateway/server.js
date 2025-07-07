import express from 'express';
import { WebSocketServer } from 'ws';
import { connect, StringCodec } from 'nats';
import { createClient } from 'redis';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { register, collectDefaultMetrics, Counter, Gauge } from 'prom-client';
import winston from 'winston';
import http from 'http';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Logger setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
});

// Metrics
collectDefaultMetrics();
const httpRequestsTotal = new Counter({
  name: 'gateway_http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});

const wsConnectionsGauge = new Gauge({
  name: 'gateway_websocket_connections',
  help: 'Number of active WebSocket connections'
});

class Gateway {
  constructor() {
    this.app = express();
    this.server = http.createServer(this.app);
    this.wss = new WebSocketServer({ server: this.server });
    this.nc = null;
    this.redis = null;
    this.sc = StringCodec();
    this.districts = new Map();
    this.wsClients = new Set();
  }

  async initialize() {
    // Connect to NATS
    const natsHost = process.env.NATS_HOST || 'localhost';
    try {
      this.nc = await connect({ servers: `${natsHost}:4222` });
      logger.info(`🔌 Connected to NATS at ${natsHost}`);
    } catch (err) {
      logger.error('Failed to connect to NATS:', err);
      process.exit(1);
    }

    // Connect to Redis
    const redisHost = process.env.REDIS_HOST || 'localhost';
    this.redis = createClient({ url: `redis://${redisHost}:6379` });
    this.redis.on('error', err => logger.error('Redis Client Error', err));
    await this.redis.connect();
    logger.info(`🔌 Connected to Redis at ${redisHost}`);

    // Setup subscriptions
    await this.setupSubscriptions();

    // Announce to Phoenix Rathaus
    await this.announceDistrict();

    // Setup middleware
    this.setupMiddleware();

    // Setup routes
    this.setupRoutes();

    // Setup WebSocket
    this.setupWebSocket();
  }

  async setupSubscriptions() {
    // Subscribe to district announcements
    const districtSub = this.nc.subscribe('district.announce');
    (async () => {
      for await (const msg of districtSub) {
        try {
          const announcement = JSON.parse(this.sc.decode(msg.data));
          this.handleDistrictAnnouncement(announcement);
        } catch (err) {
          logger.error('Error handling district announcement:', err);
        }
      }
    })();

    // Subscribe to pattern results
    const patternSub = this.nc.subscribe('pattern.result');
    (async () => {
      for await (const msg of patternSub) {
        try {
          const result = JSON.parse(this.sc.decode(msg.data));
          this.broadcastToClients({
            type: 'pattern_result',
            data: result
          });
        } catch (err) {
          logger.error('Error handling pattern result:', err);
        }
      }
    })();

    logger.info('📡 Gateway subscriptions setup complete');
  }

  async announceDistrict() {
    const announcement = {
      district: 'js_gateway',
      status: 'online',
      port: 7888,
      capabilities: ['api_gateway', 'websocket', 'proxy', 'monitoring']
    };

    await this.nc.publish('district.announce', this.sc.encode(JSON.stringify(announcement)));
    logger.info('📢 Announced JavaScript Gateway to Phoenix Rathaus');
  }

  handleDistrictAnnouncement(announcement) {
    const { district, status, port, capabilities } = announcement;
    
    if (status === 'online') {
      this.districts.set(district, { port, capabilities, status });
      logger.info(`✅ District ${district} is online on port ${port}`);
    } else {
      this.districts.delete(district);
      logger.info(`❌ District ${district} is offline`);
    }

    // Broadcast update to WebSocket clients
    this.broadcastToClients({
      type: 'district_update',
      data: { district, status, port, capabilities }
    });
  }

  setupMiddleware() {
    // Security
    this.app.use(helmet());
    
    // CORS
    this.app.use(cors({
      origin: process.env.CORS_ORIGIN || '*',
      credentials: true
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100 // limit each IP to 100 requests per windowMs
    });
    this.app.use('/api/', limiter);

    // Body parsing
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Request logging
    this.app.use((req, res, next) => {
      const start = Date.now();
      res.on('finish', () => {
        const duration = Date.now() - start;
        logger.info(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
        httpRequestsTotal.inc({
          method: req.method,
          route: req.path,
          status: res.statusCode
        });
      });
      next();
    });
  }

  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: new Date() });
    });

    // Root endpoint
    this.app.get('/', (req, res) => {
      res.json({
        service: 'JavaScript Gateway',
        version: '1.0.0',
        status: 'operational',
        districts: Array.from(this.districts.entries()).map(([name, info]) => ({
          name,
          ...info
        }))
      });
    });

    // Districts info
    this.app.get('/api/districts', (req, res) => {
      const districts = Array.from(this.districts.entries()).map(([name, info]) => ({
        name,
        ...info
      }));
      res.json(districts);
    });

    // Pattern analysis proxy
    this.app.post('/api/pattern/analyze', async (req, res) => {
      try {
        const { text, context } = req.body;
        
        // Publish to NATS and wait for response
        const response = await this.nc.request(
          'pattern.analyze',
          this.sc.encode(JSON.stringify({ text, context })),
          { timeout: 5000 }
        );
        
        const result = JSON.parse(this.sc.decode(response.data));
        res.json(result);
      } catch (err) {
        logger.error('Pattern analysis error:', err);
        res.status(500).json({ error: 'Pattern analysis failed' });
      }
    });

    // Memory operations
    this.app.post('/api/memory/:store/set', async (req, res) => {
      try {
        const { store } = req.params;
        const { key, value, ttl } = req.body;
        
        const response = await this.nc.request(
          'memory.set',
          this.sc.encode(JSON.stringify({ store, key, value, ttl })),
          { timeout: 2000 }
        );
        
        const result = JSON.parse(this.sc.decode(response.data));
        res.json(result);
      } catch (err) {
        logger.error('Memory set error:', err);
        res.status(500).json({ error: 'Memory operation failed' });
      }
    });

    this.app.get('/api/memory/:store/get/:key', async (req, res) => {
      try {
        const { store, key } = req.params;
        
        const response = await this.nc.request(
          'memory.get',
          this.sc.encode(JSON.stringify({ store, key })),
          { timeout: 2000 }
        );
        
        const result = JSON.parse(this.sc.decode(response.data));
        res.json(result);
      } catch (err) {
        logger.error('Memory get error:', err);
        res.status(500).json({ error: 'Memory operation failed' });
      }
    });

    // Metrics endpoint
    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', register.contentType);
      res.end(await register.metrics());
    });

    // Setup proxies for direct district access
    this.setupProxies();

    // Serve static files
    this.app.use(express.static(join(__dirname, 'public')));
  }

  setupProxies() {
    // Phoenix Rathaus proxy
    this.app.use('/rathaus', createProxyMiddleware({
      target: 'http://localhost:4000',
      changeOrigin: true,
      pathRewrite: { '^/rathaus': '' }
    }));

    // Python Parasit proxy
    this.app.use('/parasit', createProxyMiddleware({
      target: 'http://localhost:6666',
      changeOrigin: true,
      pathRewrite: { '^/parasit': '' }
    }));

    // Rust Pattern District proxy
    this.app.use('/pattern', createProxyMiddleware({
      target: 'http://localhost:7007',
      changeOrigin: true,
      pathRewrite: { '^/pattern': '' }
    }));

    // Go Memory Quarter proxy
    this.app.use('/memory', createProxyMiddleware({
      target: 'http://localhost:7031',
      changeOrigin: true,
      pathRewrite: { '^/memory': '' }
    }));
  }

  setupWebSocket() {
    this.wss.on('connection', (ws, req) => {
      const clientId = `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      ws.id = clientId;
      this.wsClients.add(ws);
      wsConnectionsGauge.inc();

      logger.info(`🔌 WebSocket client connected: ${clientId}`);

      // Send initial state
      ws.send(JSON.stringify({
        type: 'connected',
        clientId,
        districts: Array.from(this.districts.entries()).map(([name, info]) => ({
          name,
          ...info
        }))
      }));

      // Handle messages
      ws.on('message', async (message) => {
        try {
          const data = JSON.parse(message);
          await this.handleWebSocketMessage(ws, data);
        } catch (err) {
          logger.error('WebSocket message error:', err);
          ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
        }
      });

      // Handle disconnect
      ws.on('close', () => {
        this.wsClients.delete(ws);
        wsConnectionsGauge.dec();
        logger.info(`🔌 WebSocket client disconnected: ${clientId}`);
      });

      // Handle errors
      ws.on('error', (err) => {
        logger.error(`WebSocket error for client ${clientId}:`, err);
      });
    });
  }

  async handleWebSocketMessage(ws, data) {
    const { type, payload } = data;

    switch (type) {
      case 'ping':
        ws.send(JSON.stringify({ type: 'pong' }));
        break;

      case 'pattern_analyze':
        const result = await this.nc.request(
          'pattern.analyze',
          this.sc.encode(JSON.stringify(payload)),
          { timeout: 5000 }
        );
        ws.send(JSON.stringify({
          type: 'pattern_result',
          data: JSON.parse(this.sc.decode(result.data))
        }));
        break;

      case 'subscribe':
        // Handle topic subscriptions
        ws.topics = payload.topics || [];
        ws.send(JSON.stringify({ type: 'subscribed', topics: ws.topics }));
        break;

      default:
        ws.send(JSON.stringify({ type: 'error', message: 'Unknown message type' }));
    }
  }

  broadcastToClients(message) {
    const messageStr = JSON.stringify(message);
    this.wsClients.forEach(client => {
      if (client.readyState === 1) { // WebSocket.OPEN
        client.send(messageStr);
      }
    });
  }

  async start() {
    await this.initialize();
    
    const port = process.env.PORT || 7888;
    this.server.listen(port, () => {
      logger.info(`🌐 JavaScript Gateway running on port ${port}`);
    });
  }
}

// Start the gateway
const gateway = new Gateway();
gateway.start().catch(err => {
  logger.error('Failed to start gateway:', err);
  process.exit(1);
});