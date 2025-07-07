const express = require('express');
const WebSocket = require('ws');
const { connect } = require('nats');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(express.static('public'));

let nc;
const clients = new Set();

// Connect to NATS
(async () => {
  try {
    nc = await connect({ servers: 'nats://nats:4222' });
    console.log('Connected to NATS');
    
    // Subscribe to all CROD events
    const sub = nc.subscribe('crod.>');
    for await (const msg of sub) {
      const event = {
        topic: msg.subject,
        data: msg.string(),
        timestamp: new Date().toISOString()
      };
      
      // Broadcast to all WebSocket clients
      for (const client of clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(event));
        }
      }
    }
  } catch (err) {
    console.error('NATS connection error:', err);
  }
})();

// WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log('New WebSocket client connected');
  
  ws.on('close', () => {
    clients.delete(ws);
  });
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      if (nc) {
        nc.publish(`crod.gateway.${data.type}`, JSON.stringify(data));
      }
    } catch (err) {
      console.error('Message error:', err);
    }
  });
});

// API Routes
app.get('/', (req, res) => {
  res.send('CROD Gateway Online');
});

app.get('/api/status', async (req, res) => {
  const status = {
    gateway: 'online',
    websocket_clients: clients.size,
    districts: {}
  };
  
  // Check district health
  const districts = [
    { name: 'rathaus', url: 'http://crod-rathaus:4000' },
    { name: 'pattern', url: 'http://crod-pattern:7007' },
    { name: 'memory', url: 'http://crod-memory:7031' },
    { name: 'parasit', url: 'http://crod-parasit:6666' }
  ];
  
  for (const district of districts) {
    try {
      await axios.get(district.url, { timeout: 1000 });
      status.districts[district.name] = 'online';
    } catch (err) {
      status.districts[district.name] = 'offline';
    }
  }
  
  res.json(status);
});

// Dashboard HTML
app.get('/dashboard', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html>
<head>
  <title>CROD Gateway Dashboard</title>
  <style>
    body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
    .event { margin: 5px 0; padding: 5px; border: 1px solid #0f0; }
    #status { margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>CROD POLYGLOT CITY 2025 - GATEWAY</h1>
  <div id="status"></div>
  <h2>Live Events</h2>
  <div id="events"></div>
  
  <script>
    const ws = new WebSocket('ws://localhost:8080');
    const eventsDiv = document.getElementById('events');
    const statusDiv = document.getElementById('status');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const eventDiv = document.createElement('div');
      eventDiv.className = 'event';
      eventDiv.textContent = \`[\${data.timestamp}] \${data.topic}: \${data.data}\`;
      eventsDiv.insertBefore(eventDiv, eventsDiv.firstChild);
      
      if (eventsDiv.children.length > 50) {
        eventsDiv.removeChild(eventsDiv.lastChild);
      }
    };
    
    setInterval(async () => {
      try {
        const res = await fetch('/api/status');
        const status = await res.json();
        statusDiv.innerHTML = '<h3>District Status:</h3>' + 
          Object.entries(status.districts)
            .map(([name, status]) => \`\${name}: \${status}\`)
            .join(' | ');
      } catch (err) {
        console.error(err);
      }
    }, 5000);
  </script>
</body>
</html>
  `);
});

const PORT = process.env.PORT || 7888;
app.listen(PORT, () => {
  console.log(`Gateway listening on port ${PORT}`);
});
