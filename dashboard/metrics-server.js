#!/usr/bin/env node

const http = require('http');
const { exec } = require('child_process');
const WebSocket = require('ws');
const path = require('path');

const PORT = 8889;

// Check if kubectl is available
exec('kubectl version --short 2>/dev/null', (error) => {
    if (error) {
        console.error('⚠️  kubectl not found or not configured!');
        console.error('   Dashboard will show "No Data" until K8s is accessible');
    } else {
        console.log('✅ kubectl found');
    }
});

// K8s metrics collection
async function getK8sMetrics() {
    return new Promise((resolve) => {
        exec('kubectl top pods -n crod-polyglot --no-headers 2>/dev/null', (error, stdout, stderr) => {
            if (error) {
                resolve({});
                return;
            }
            
            const metrics = {};
            stdout.split('\n').filter(line => line.trim()).forEach(line => {
                const [name, cpu, memory] = line.split(/\s+/);
                metrics[name] = {
                    cpu: parseInt(cpu) || 0,
                    memory: parseInt(memory) || 0,
                    status: 'Running'
                };
            });
            
            resolve(metrics);
        });
    });
}

// Get pod status
async function getPodStatus() {
    return new Promise((resolve) => {
        exec('kubectl get pods -n crod-polyglot -o json', (error, stdout) => {
            if (error) {
                resolve({});
                return;
            }
            
            try {
                const data = JSON.parse(stdout);
                const status = {};
                
                data.items.forEach(pod => {
                    status[pod.metadata.name] = {
                        phase: pod.status.phase,
                        ready: pod.status.conditions?.find(c => c.type === 'Ready')?.status === 'True',
                        restarts: pod.status.containerStatuses?.[0]?.restartCount || 0,
                        startTime: pod.status.startTime
                    };
                });
                
                resolve(status);
            } catch (e) {
                resolve({});
            }
        });
    });
}

// Create HTTP server for dashboard
const server = http.createServer((req, res) => {
    if (req.url === '/') {
        res.writeHead(302, { Location: '/dashboard' });
        res.end();
    } else if (req.url === '/dashboard') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`
            <html>
            <head>
                <title>CROD Metrics Redirect</title>
                <meta http-equiv="refresh" content="0; url=file://${__dirname}/crod-live-metrics.html">
            </head>
            <body>
                <p>Opening dashboard...</p>
                <p>If not redirected, open: <a href="file://${__dirname}/crod-live-metrics.html">CROD Live Metrics</a></p>
            </body>
            </html>
        `);
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

// WebSocket server for real-time metrics
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('Dashboard connected');
    
    const interval = setInterval(async () => {
        try {
            const [metrics, status] = await Promise.all([
                getK8sMetrics(),
                getPodStatus()
            ]);
            
            // Only send if we have actual data
            if (Object.keys(metrics).length === 0 && Object.keys(status).length === 0) {
                console.log('No K8s metrics available');
                return;
            }
            
            const data = {
                timestamp: new Date().toISOString(),
                pods: { ...metrics },
                status: { ...status }
            };
            
            ws.send(JSON.stringify(data));
        } catch (error) {
            console.error('Error collecting metrics:', error);
        }
    }, 1000);
    
    ws.on('close', () => {
        clearInterval(interval);
        console.log('Dashboard disconnected');
    });
});

server.listen(PORT, () => {
    console.log(`
🚀 CROD Metrics Server running on http://localhost:${PORT}
📊 Dashboard: http://localhost:${PORT}/dashboard
🔌 WebSocket: ws://localhost:${PORT}/metrics

Open dashboard: xdg-open http://localhost:${PORT}/dashboard
    `);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down metrics server...');
    server.close();
    process.exit(0);
});