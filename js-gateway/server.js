const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { connect } = require('nats');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 7888;
const natsUrl = process.env.NATS_URL || 'nats://localhost:4222';

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Service endpoints
const services = {
    phoenix: 'http://phoenix-rathaus:4000',
    python: 'http://python-parasit:6666',
    rust: 'http://rust-pattern:7007',
    go: 'http://go-memory:7031'
};

let nc = null;

// Connect to NATS
async function connectNATS() {
    try {
        nc = await connect({ servers: natsUrl });
        console.log(`Connected to NATS at ${natsUrl}`);
        
        // Announce presence
        await nc.publish('crod.district.online', JSON.stringify({
            district: 'js-gateway',
            port: port
        }));

        // Subscribe to gateway messages
        const sub = nc.subscribe('crod.gateway.>');
        (async () => {
            for await (const msg of sub) {
                console.log(`Received message on ${msg.subject}`);
            }
        })();
    } catch (err) {
        console.error('Failed to connect to NATS:', err);
        setTimeout(connectNATS, 5000);
    }
}

connectNATS();

// Routes
app.get('/', (req, res) => {
    res.json({
        service: 'CROD JavaScript Gateway',
        port: port,
        status: 'routing',
        endpoints: Object.keys(services)
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Service discovery
app.get('/api/services', async (req, res) => {
    const serviceStatus = {};
    
    for (const [name, url] of Object.entries(services)) {
        try {
            const response = await axios.get(url, { timeout: 2000 });
            serviceStatus[name] = {
                status: 'online',
                url: url,
                info: response.data
            };
        } catch (err) {
            serviceStatus[name] = {
                status: 'offline',
                url: url,
                error: err.message
            };
        }
    }
    
    res.json(serviceStatus);
});

// Proxy requests to services
app.all('/api/:service/*', async (req, res) => {
    const { service } = req.params;
    const path = req.params[0];
    
    if (!services[service]) {
        return res.status(404).json({ error: 'Service not found' });
    }
    
    try {
        const url = `${services[service]}/${path}`;
        const response = await axios({
            method: req.method,
            url: url,
            data: req.body,
            headers: req.headers,
            timeout: 10000
        });
        
        res.status(response.status).json(response.data);
    } catch (err) {
        res.status(err.response?.status || 500).json({
            error: 'Service request failed',
            message: err.message
        });
    }
});

// WebSocket support for real-time updates
const server = app.listen(port, '0.0.0.0', () => {
    console.log(`JavaScript Gateway listening on port ${port}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    console.log('SIGTERM received, shutting down gracefully');
    if (nc) await nc.close();
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});