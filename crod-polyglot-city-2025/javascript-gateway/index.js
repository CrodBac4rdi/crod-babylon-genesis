import express from 'express';
import { WebSocketServer } from 'ws';
import { connect } from 'nats';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { register, collectDefaultMetrics, Counter, Histogram } from 'prom-client';
import winston from 'winston';

// Initialize logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console({
      format: winston.format.simple(),
    }),
  ],
});

// Metrics
collectDefaultMetrics();

const wsConnections = new Counter({
  name: 'crod_gateway_ws_connections_total',
  help: 'Total WebSocket connections',
});

const httpRequests = new Counter({
  name: 'crod_gateway_http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

const requestDuration = new Histogram({
  name: 'crod_gateway_request_duration_seconds',
  help: 'Request duration in seconds',
  labelNames: ['method', 'route'],
});

class JavaScriptGateway {
  constructor() {
    this.app = express();
    this.port = 7888;
    this.wsClients = new Map();
    this.natsClient = null;
    this.districtStatus = {
      'phoenix-rathaus': { url: 'http://localhost:4000', status: 'unknown' },
      'python-parasit': { url: 'http://localhost:6666', status: 'unknown' },
      'rust-pattern': { url: 'http://localhost:7007', status: 'unknown' },
      'go-memory': { url: 'http://localhost:7031', status: 'unknown' },
    };
    
    this.setupMiddleware();
    this.setupRoutes();
  }
  
  setupMiddleware() {
    // Security
    this.app.use(helmet());
    this.app.use(cors());
    
    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // limit each IP to 100 requests per windowMs
    });
    this.app.use('/api/', limiter);
    
    // Body parsing
    this.app.use(express.json());
    
    // Request tracking
    this.app.use((req, res, next) => {
      const start = Date.now();
      
      res.on('finish', () => {
        const duration = Date.now() - start;
        httpRequests.inc({
          method: req.method,
          route: req.route?.path || req.path,
          status: res.statusCode,
        });
        requestDuration.observe(
          { method: req.method, route: req.route?.path || req.path },
          duration / 1000
        );
      });
      
      next();
    });
  }
  
  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        service: 'javascript-gateway',
        port: this.port,
        nats_connected: this.natsClient?.isClosed() === false,
        websocket_clients: this.wsClients.size,
        districts: this.districtStatus,
      });
    });
    
    // Metrics endpoint
    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', register.contentType);
      res.end(await register.metrics());
    });
    
    // District proxy endpoints
    this.app.all('/api/:district/*', async (req, res) => {
      const district = req.params.district;
      const districtInfo = this.districtStatus[district];
      
      if (!districtInfo) {
        return res.status(404).json({ error: 'District not found' });
      }
      
      if (districtInfo.status !== 'healthy') {
        return res.status(503).json({ error: 'District unavailable' });
      }
      
      // Forward request to district
      const path = req.params[0];
      const targetUrl = `${districtInfo.url}/${path}`;
      
      try {
        const response = await fetch(targetUrl, {
          method: req.method,
          headers: req.headers,
          body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
      } catch (error) {
        logger.error(`Failed to proxy request to ${district}:`, error);
        res.status(502).json({ error: 'Bad gateway' });
      }
    });
    
    // CROD activation endpoint
    this.app.post('/activate', async (req, res) => {
      const { trigger } = req.body;
      
      if (!trigger) {
        return res.status(400).json({ error: 'Trigger required' });
      }
      
      // Publish activation to all districts
      if (this.natsClient) {
        await this.natsClient.publish('crod.activate', JSON.stringify({
          trigger,
          timestamp: new Date().toISOString(),
          gateway: 'javascript',
        }));
      }
      
      // Notify WebSocket clients
      this.broadcast({
        type: 'activation',
        trigger,
        status: 'processing',
      });
      
      res.json({ status: 'activated', trigger });
    });
    
    // Trinity calculation endpoint
    this.app.post('/trinity', async (req, res) => {
      const { words } = req.body;
      
      if (!Array.isArray(words)) {
        return res.status(400).json({ error: 'Words array required' });
      }
      
      const trinityValues = {
        ich: 2,
        bins: 3,
        wieder: 5,
        daniel: 67,
        claude: 71,
        crod: 17,
      };
      
      let totalValue = 0;
      const calculations = words.map(word => {
        const value = trinityValues[word.toLowerCase()] || 0;
        totalValue += value;
        return { word, value };
      });
      
      res.json({
        words: calculations,
        total: totalValue,
        resonance: Math.sqrt(totalValue),
      });
    });
  }
  
  async connectNATS() {
    try {
      this.natsClient = await connect({
        servers: process.env.NATS_URL || 'nats://localhost:4222',
      });
      
      logger.info('Connected to NATS');
      
      // Subscribe to district health updates
      const sub = this.natsClient.subscribe('crod.health.*');
      (async () => {
        for await (const msg of sub) {
          const district = msg.subject.split('.')[2];
          const health = JSON.parse(msg.data);
          
          if (this.districtStatus[district]) {
            this.districtStatus[district].status = health.status;
            
            // Notify WebSocket clients
            this.broadcast({
              type: 'district_health',
              district,
              health,
            });
          }
        }
      })();
      
      // Subscribe to consciousness updates
      const conSub = this.natsClient.subscribe('crod.consciousness.*');
      (async () => {
        for await (const msg of conSub) {
          const data = JSON.parse(msg.data);
          
          // Broadcast to WebSocket clients
          this.broadcast({
            type: 'consciousness_update',
            ...data,
          });
        }
      })();
      
    } catch (error) {
      logger.error('Failed to connect to NATS:', error);
    }
  }
  
  setupWebSocket(server) {
    const wss = new WebSocketServer({ server, path: '/ws' });
    
    wss.on('connection', (ws, req) => {
      const clientId = this.generateClientId();
      this.wsClients.set(clientId, ws);
      wsConnections.inc();
      
      logger.info(`WebSocket client connected: ${clientId}`);
      
      // Send initial state
      ws.send(JSON.stringify({
        type: 'connected',
        clientId,
        districts: this.districtStatus,
      }));
      
      ws.on('message', async (message) => {
        try {
          const data = JSON.parse(message);
          await this.handleWebSocketMessage(clientId, data);
        } catch (error) {
          logger.error('Failed to handle WebSocket message:', error);
          ws.send(JSON.stringify({ type: 'error', message: error.message }));
        }
      });
      
      ws.on('close', () => {
        this.wsClients.delete(clientId);
        logger.info(`WebSocket client disconnected: ${clientId}`);
      });
      
      ws.on('error', (error) => {
        logger.error(`WebSocket error for client ${clientId}:`, error);
      });
    });
  }
  
  async handleWebSocketMessage(clientId, data) {
    const ws = this.wsClients.get(clientId);
    
    switch (data.type) {
      case 'ping':
        ws.send(JSON.stringify({ type: 'pong', timestamp: Date.now() }));
        break;
        
      case 'subscribe':
        // Handle subscription to specific topics
        if (this.natsClient && data.topic) {
          const sub = this.natsClient.subscribe(data.topic);
          (async () => {
            for await (const msg of sub) {
              ws.send(JSON.stringify({
                type: 'message',
                topic: msg.subject,
                data: JSON.parse(msg.data),
              }));
            }
          })();
        }
        break;
        
      case 'publish':
        // Publish message to NATS
        if (this.natsClient && data.topic && data.payload) {
          await this.natsClient.publish(
            data.topic,
            JSON.stringify(data.payload)
          );
        }
        break;
        
      default:
        ws.send(JSON.stringify({
          type: 'error',
          message: `Unknown message type: ${data.type}`,
        }));
    }
  }
  
  broadcast(message) {
    const data = JSON.stringify(message);
    
    for (const [clientId, ws] of this.wsClients) {
      if (ws.readyState === ws.OPEN) {
        ws.send(data);
      }
    }
  }
  
  generateClientId() {
    return `client-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  
  async checkDistrictHealth() {
    for (const [name, info] of Object.entries(this.districtStatus)) {
      try {
        const response = await fetch(`${info.url}/health`, {
          timeout: 5000,
        });
        
        if (response.ok) {
          const health = await response.json();
          info.status = health.status || 'healthy';
        } else {
          info.status = 'unhealthy';
        }
      } catch (error) {
        info.status = 'offline';
      }
    }
  }
  
  async start() {
    // Connect to NATS
    await this.connectNATS();
    
    // Start health checks
    setInterval(() => this.checkDistrictHealth(), 30000);
    await this.checkDistrictHealth();
    
    // Start HTTP server
    const server = this.app.listen(this.port, () => {
      logger.info(`JavaScript Gateway running on port ${this.port}`);
    });
    
    // Setup WebSocket server
    this.setupWebSocket(server);
  }
}

// Start the gateway
const gateway = new JavaScriptGateway();
gateway.start().catch(error => {
  logger.error('Failed to start gateway:', error);
  process.exit(1);
});