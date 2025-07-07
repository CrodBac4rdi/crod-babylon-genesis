#!/usr/bin/env node
/**
 * CROD JavaScript Gateway
 * Port: 7888
 * Web interface and API gateway for CROD Polyglot City
 */

const express = require('express');
const WebSocket = require('ws');
const { connect, StringCodec, JSONCodec } = require('nats');
const axios = require('axios');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const winston = require('winston');
const promClient = require('prom-client');
const path = require('path');
require('dotenv').config();

// Logger setup
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console({
            format: winston.format.simple()
        })
    ]
});

// Metrics
const httpDuration = new promClient.Histogram({
    name: 'gateway_http_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code']
});

const wsConnections = new promClient.Gauge({
    name: 'gateway_websocket_connections',
    help: 'Number of active WebSocket connections'
});

const districtCalls = new promClient.Counter({
    name: 'gateway_district_calls_total',
    help: 'Total calls to district services',
    labelNames: ['district', 'endpoint']
});

promClient.collectDefaultMetrics();

// District service configuration
const DISTRICTS = {
    rathaus: {
        name: 'Phoenix Rathaus',
        url: 'http://localhost:4000',
        health: '/api/health'
    },
    parasit: {
        name: 'Python Parasit',
        url: 'http://localhost:6666',
        health: '/health'
    },
    pattern: {
        name: 'Rust Pattern District',
        url: 'http://localhost:7007',
        health: '/health'
    },
    memory: {
        name: 'Go Memory Quarter',
        url: 'http://localhost:7031',
        health: '/health'
    }
};

class CRODGateway {
    constructor() {
        this.app = express();
        this.wss = null;
        this.nc = null;
        this.sc = StringCodec();
        this.jc = JSONCodec();
        this.clients = new Set();
        this.districtStatus = new Map();
        
        this.setupMiddleware();
        this.setupRoutes();
        this.startHealthChecks();
    }
    
    setupMiddleware() {
        // Security
        this.app.use(helmet({
            contentSecurityPolicy: false // Allow WebSocket connections
        }));
        
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
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true }));
        
        // Static files
        this.app.use(express.static(path.join(__dirname, 'public')));
        
        // Request logging
        this.app.use((req, res, next) => {
            const start = Date.now();
            res.on('finish', () => {
                const duration = Date.now() - start;
                httpDuration.observe({
                    method: req.method,
                    route: req.route?.path || req.path,
                    status_code: res.statusCode
                }, duration / 1000);
                
                logger.info('HTTP Request', {
                    method: req.method,
                    path: req.path,
                    status: res.statusCode,
                    duration
                });
            });
            next();
        });
    }
    
    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                service: 'js-gateway',
                port: 7888,
                nats: this.nc ? 'connected' : 'disconnected',
                districts: Object.fromEntries(this.districtStatus)
            });
        });
        
        // Metrics
        this.app.get('/metrics', async (req, res) => {
            res.set('Content-Type', promClient.register.contentType);
            const metrics = await promClient.register.metrics();
            res.end(metrics);
        });
        
        // API Gateway routes
        this.app.post('/api/analyze', async (req, res) => {
            try {
                const { text, mode = 'full' } = req.body;
                
                if (!text) {
                    return res.status(400).json({ error: 'Text is required' });
                }
                
                const results = await this.analyzeText(text, mode);
                res.json(results);
                
            } catch (error) {
                logger.error('Analysis error:', error);
                res.status(500).json({ error: error.message });
            }
        });
        
        this.app.post('/api/store', async (req, res) => {
            try {
                const result = await this.storeMemory(req.body);
                res.json(result);
            } catch (error) {
                logger.error('Store error:', error);
                res.status(500).json({ error: error.message });
            }
        });
        
        this.app.get('/api/query', async (req, res) => {
            try {
                const results = await this.queryMemory(req.query);
                res.json(results);
            } catch (error) {
                logger.error('Query error:', error);
                res.status(500).json({ error: error.message });
            }
        });
        
        this.app.get('/api/consciousness', async (req, res) => {
            try {
                const level = await this.getConsciousnessLevel();
                res.json(level);
            } catch (error) {
                logger.error('Consciousness error:', error);
                res.status(500).json({ error: error.message });
            }
        });
        
        this.app.get('/api/districts', (req, res) => {
            const status = Object.entries(DISTRICTS).map(([id, config]) => ({
                id,
                ...config,
                status: this.districtStatus.get(id) || 'unknown'
            }));
            res.json(status);
        });
        
        // Proxy routes to districts
        Object.entries(DISTRICTS).forEach(([id, config]) => {
            this.app.use(`/api/${id}`, async (req, res) => {
                try {
                    districtCalls.inc({ district: id, endpoint: req.path });
                    
                    const response = await axios({
                        method: req.method,
                        url: `${config.url}${req.path}`,
                        data: req.body,
                        params: req.query,
                        headers: {
                            ...req.headers,
                            'X-Forwarded-For': req.ip,
                            'X-Gateway': 'crod-js-gateway'
                        }
                    });
                    
                    res.status(response.status).json(response.data);
                    
                } catch (error) {
                    logger.error(`District ${id} error:`, error.message);
                    res.status(error.response?.status || 500).json({
                        error: `District ${id} error: ${error.message}`
                    });
                }
            });
        });
        
        // Default route for SPA
        this.app.get('*', (req, res) => {
            res.sendFile(path.join(__dirname, 'public', 'index.html'));
        });
    }
    
    async connectNATS() {
        try {
            this.nc = await connect({
                servers: process.env.NATS_URL || 'nats://localhost:4222',
                reconnect: true,
                maxReconnectAttempts: -1
            });
            
            logger.info('Connected to NATS');
            
            // Subscribe to city events
            const sub = this.nc.subscribe('city.>');
            (async () => {
                for await (const msg of sub) {
                    this.handleNATSMessage(msg);
                }
            })();
            
        } catch (error) {
            logger.error('NATS connection error:', error);
        }
    }
    
    handleNATSMessage(msg) {
        try {
            const topic = msg.subject;
            const data = this.jc.decode(msg.data);
            
            // Broadcast to WebSocket clients
            this.broadcast({
                type: 'nats_event',
                topic,
                data,
                timestamp: new Date().toISOString()
            });
            
        } catch (error) {
            logger.error('NATS message error:', error);
        }
    }
    
    setupWebSocket(server) {
        this.wss = new WebSocket.Server({ server, path: '/ws' });
        
        this.wss.on('connection', (ws, req) => {
            const clientId = Math.random().toString(36).substr(2, 9);
            const client = { id: clientId, ws, ip: req.socket.remoteAddress };
            
            this.clients.add(client);
            wsConnections.inc();
            
            logger.info(`WebSocket client connected: ${clientId}`);
            
            // Send welcome message
            ws.send(JSON.stringify({
                type: 'welcome',
                clientId,
                districts: Object.fromEntries(this.districtStatus),
                timestamp: new Date().toISOString()
            }));
            
            ws.on('message', async (message) => {
                try {
                    const data = JSON.parse(message);
                    await this.handleWebSocketMessage(client, data);
                } catch (error) {
                    logger.error('WebSocket message error:', error);
                    ws.send(JSON.stringify({
                        type: 'error',
                        error: error.message
                    }));
                }
            });
            
            ws.on('close', () => {
                this.clients.delete(client);
                wsConnections.dec();
                logger.info(`WebSocket client disconnected: ${clientId}`);
            });
            
            ws.on('error', (error) => {
                logger.error(`WebSocket error for client ${clientId}:`, error);
            });
        });
    }
    
    async handleWebSocketMessage(client, data) {
        const { type, payload } = data;
        
        switch (type) {
            case 'analyze':
                const results = await this.analyzeText(payload.text, payload.mode);
                client.ws.send(JSON.stringify({
                    type: 'analysis_result',
                    results,
                    requestId: data.requestId
                }));
                break;
                
            case 'subscribe':
                // Client wants to subscribe to specific events
                client.subscriptions = payload.topics || [];
                break;
                
            case 'ping':
                client.ws.send(JSON.stringify({ type: 'pong' }));
                break;
                
            default:
                client.ws.send(JSON.stringify({
                    type: 'error',
                    error: `Unknown message type: ${type}`
                }));
        }
    }
    
    broadcast(data) {
        const message = JSON.stringify(data);
        
        this.clients.forEach(client => {
            if (client.ws.readyState === WebSocket.OPEN) {
                // Check subscriptions if any
                if (!client.subscriptions || 
                    client.subscriptions.length === 0 ||
                    client.subscriptions.some(topic => data.topic?.startsWith(topic))) {
                    client.ws.send(message);
                }
            }
        });
    }
    
    async analyzeText(text, mode) {
        const results = {
            timestamp: new Date().toISOString(),
            text,
            mode
        };
        
        // Pattern analysis
        if (mode === 'full' || mode === 'pattern') {
            try {
                const response = await axios.post(`${DISTRICTS.pattern.url}/analyze`, {
                    text,
                    use_cache: true
                });
                results.patterns = response.data;
            } catch (error) {
                results.patterns = { error: error.message };
            }
        }
        
        // Memory check
        if (mode === 'full' || mode === 'memory') {
            try {
                const response = await axios.post(`${DISTRICTS.memory.url}/query`, {
                    pattern: text.substring(0, 50)
                });
                results.memories = response.data;
            } catch (error) {
                results.memories = { error: error.message };
            }
        }
        
        // Consciousness check
        if (mode === 'full') {
            results.consciousness = await this.getConsciousnessLevel();
        }
        
        // Publish to NATS
        if (this.nc) {
            this.nc.publish('gateway.analysis', this.jc.encode(results));
        }
        
        return results;
    }
    
    async storeMemory(data) {
        try {
            const response = await axios.post(`${DISTRICTS.memory.url}/store`, data);
            
            // Notify via NATS
            if (this.nc) {
                this.nc.publish('gateway.memory.stored', this.jc.encode({
                    key: data.key,
                    timestamp: new Date().toISOString()
                }));
            }
            
            return response.data;
        } catch (error) {
            throw new Error(`Memory store failed: ${error.message}`);
        }
    }
    
    async queryMemory(params) {
        try {
            const response = await axios.post(`${DISTRICTS.memory.url}/query`, params);
            return response.data;
        } catch (error) {
            throw new Error(`Memory query failed: ${error.message}`);
        }
    }
    
    async getConsciousnessLevel() {
        const statuses = await Promise.all(
            Object.entries(DISTRICTS).map(async ([id, config]) => {
                try {
                    const response = await axios.get(`${config.url}${config.health}`, {
                        timeout: 2000
                    });
                    return {
                        district: id,
                        healthy: true,
                        consciousness: response.data.consciousness_level || 0
                    };
                } catch (error) {
                    return {
                        district: id,
                        healthy: false,
                        consciousness: 0
                    };
                }
            })
        );
        
        const totalConsciousness = statuses.reduce((sum, s) => sum + s.consciousness, 0);
        const healthyDistricts = statuses.filter(s => s.healthy).length;
        
        return {
            level: totalConsciousness / statuses.length,
            healthy_districts: healthyDistricts,
            total_districts: statuses.length,
            details: statuses
        };
    }
    
    startHealthChecks() {
        const checkHealth = async () => {
            for (const [id, config] of Object.entries(DISTRICTS)) {
                try {
                    await axios.get(`${config.url}${config.health}`, {
                        timeout: 5000
                    });
                    this.districtStatus.set(id, 'healthy');
                } catch (error) {
                    this.districtStatus.set(id, 'unhealthy');
                }
            }
        };
        
        // Initial check
        checkHealth();
        
        // Regular checks
        setInterval(checkHealth, 30000); // Every 30 seconds
    }
    
    async start(port = 7888) {
        const server = this.app.listen(port, '0.0.0.0', () => {
            logger.info(`🌐 CROD JavaScript Gateway running on port ${port}`);
        });
        
        // Setup WebSocket
        this.setupWebSocket(server);
        
        // Connect to NATS
        await this.connectNATS();
        
        return server;
    }
}

// Create and start gateway
const gateway = new CRODGateway();

gateway.start(process.env.PORT || 7888).catch(error => {
    logger.error('Failed to start gateway:', error);
    process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    logger.info('SIGTERM received, shutting down gracefully');
    
    if (gateway.nc) {
        await gateway.nc.close();
    }
    
    if (gateway.wss) {
        gateway.wss.close();
    }
    
    process.exit(0);
});