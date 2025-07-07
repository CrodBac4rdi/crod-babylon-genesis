const express = require('express');
const cors = require('cors');
const WebSocket = require('ws');
const { connect, StringCodec } = require('nats');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 7888;
const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Service registry
const services = {
  rathaus: { name: 'Phoenix Rathaus', port: 4000, status: 'unknown', lastCheck: null },
  parasit: { name: 'Python Parasit', port: 6666, status: 'unknown', lastCheck: null },
  pattern: { name: 'Rust Pattern District', port: 7007, status: 'unknown', lastCheck: null },
  memory: { name: 'Go Memory Quarter', port: 7031, status: 'unknown', lastCheck: null },
  gateway: { name: 'JavaScript Gateway', port: 7888, status: 'active', lastCheck: Date.now() }
};

// NATS connection
let nc = null;
let sc = StringCodec();

async function connectNATS() {
  try {
    nc = await connect({ servers: NATS_URL });
    console.log('✅ Connected to NATS');
    
    // Subscribe to service health updates
    const sub = nc.subscribe('crod.health.*');
    (async () => {
      for await (const msg of sub) {
        const data = JSON.parse(sc.decode(msg.data));
        const service = msg.subject.split('.')[2];
        if (services[service]) {
          services[service].status = data.status;
          services[service].lastCheck = Date.now();
        }
      }
    })();
  } catch (err) {
    console.error('⚠️  NATS connection failed:', err.message);
  }
}

// WebSocket server for real-time updates
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('New WebSocket connection');
  
  // Send initial status
  ws.send(JSON.stringify({
    type: 'status',
    services: services,
    timestamp: Date.now()
  }));
  
  // Send updates every 2 seconds
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'status',
        services: services,
        timestamp: Date.now()
      }));
    }
  }, 2000);
  
  ws.on('close', () => {
    clearInterval(interval);
  });
});

// API Routes
app.get('/api/status', (req, res) => {
  res.json({
    gateway: 'CROD JavaScript Gateway',
    version: '1.0.0',
    services: services,
    nats: nc ? 'connected' : 'disconnected',
    websocket: `ws://localhost:8080`,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/services', (req, res) => {
  res.json(services);
});

app.post('/api/message', async (req, res) => {
  const { subject, data } = req.body;
  
  if (!nc) {
    return res.status(503).json({ error: 'NATS not connected' });
  }
  
  try {
    await nc.publish(subject, sc.encode(JSON.stringify(data)));
    res.json({ success: true, subject, data });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'crod-gateway-js' });
});

// Dashboard route
app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Check service health periodically
async function checkServiceHealth() {
  for (const [key, service] of Object.entries(services)) {
    if (key === 'gateway') continue;
    
    try {
      const response = await fetch(`http://localhost:${service.port}/health`);
      service.status = response.ok ? 'active' : 'error';
    } catch (err) {
      service.status = 'offline';
    }
    service.lastCheck = Date.now();
  }
}

// Create public directory and dashboard
const fs = require('fs');
if (!fs.existsSync('public')) {
  fs.mkdirSync('public');
}

// Create dashboard HTML
const dashboardHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CROD Polyglot City Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #0a0a0a;
            color: #fff;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #00ff88;
            margin-bottom: 40px;
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .service-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s;
        }
        .service-card:hover {
            transform: translateY(-2px);
            border-color: #00ff88;
        }
        .service-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .service-port {
            color: #888;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .service-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-active {
            background: #00ff88;
            color: #000;
        }
        .status-offline {
            background: #ff4444;
            color: #fff;
        }
        .status-unknown {
            background: #666;
            color: #fff;
        }
        .console {
            background: #0a0a0a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
        .console-line {
            margin-bottom: 5px;
        }
        .time {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ CROD Polyglot City 2025</h1>
        <div class="services-grid" id="services"></div>
        <h2>System Console</h2>
        <div class="console" id="console"></div>
    </div>

    <script>
        const ws = new WebSocket('ws://localhost:8080');
        const servicesDiv = document.getElementById('services');
        const consoleDiv = document.getElementById('console');

        function addConsoleMessage(message) {
            const time = new Date().toLocaleTimeString();
            const line = document.createElement('div');
            line.className = 'console-line';
            line.innerHTML = \`<span class="time">[\${time}]</span> \${message}\`;
            consoleDiv.appendChild(line);
            consoleDiv.scrollTop = consoleDiv.scrollHeight;
        }

        function updateServices(services) {
            servicesDiv.innerHTML = '';
            for (const [key, service] of Object.entries(services)) {
                const card = document.createElement('div');
                card.className = 'service-card';
                const statusClass = \`status-\${service.status}\`;
                card.innerHTML = \`
                    <div class="service-name">\${service.name}</div>
                    <div class="service-port">Port: \${service.port}</div>
                    <span class="service-status \${statusClass}">\${service.status.toUpperCase()}</span>
                \`;
                servicesDiv.appendChild(card);
            }
        }

        ws.onopen = () => {
            addConsoleMessage('✅ Connected to CROD Gateway WebSocket');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'status') {
                updateServices(data.services);
            }
        };

        ws.onerror = () => {
            addConsoleMessage('❌ WebSocket error');
        };

        ws.onclose = () => {
            addConsoleMessage('🔌 WebSocket disconnected');
        };

        // Initial fetch
        fetch('/api/status')
            .then(res => res.json())
            .then(data => {
                updateServices(data.services);
                addConsoleMessage('🚀 CROD Polyglot City Dashboard initialized');
            });
    </script>
</body>
</html>`;

fs.writeFileSync('public/dashboard.html', dashboardHTML);

// Start server
app.listen(PORT, async () => {
  console.log(`🌐 CROD Gateway running on port ${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}/dashboard`);
  console.log(`🔌 WebSocket: ws://localhost:8080`);
  
  await connectNATS();
  
  // Start health checks
  setInterval(checkServiceHealth, 5000);
  checkServiceHealth();
});