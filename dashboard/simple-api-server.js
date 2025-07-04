#!/usr/bin/env node

const http = require('http');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = 8890;

// Get K8s data
async function getPodsData() {
    return new Promise((resolve) => {
        exec('export KUBECONFIG=~/.kube/config && kubectl get pods -n crod-polyglot -o wide --no-headers && echo "---METRICS---" && kubectl top pods -n crod-polyglot --no-headers', (error, stdout) => {
            if (error) {
                resolve({ pods: [] });
                return;
            }
            
            const [podInfo, metrics] = stdout.split('---METRICS---');
            const pods = [];
            const metricsMap = {};
            
            // Parse metrics first
            metrics.split('\n').filter(l => l.trim()).forEach(line => {
                const [name, cpu, memory] = line.trim().split(/\s+/);
                metricsMap[name] = { cpu, memory };
            });
            
            // Parse pod info
            podInfo.split('\n').filter(l => l.trim()).forEach(line => {
                const parts = line.trim().split(/\s+/);
                const name = parts[0];
                const ready = parts[1];
                const status = parts[2];
                const restarts = parts[3];
                const age = parts[4];
                const ip = parts[5];
                
                pods.push({
                    name,
                    ready: ready === '1/1',
                    status,
                    restarts,
                    age,
                    ip,
                    cpu: metricsMap[name]?.cpu || 'N/A',
                    memory: metricsMap[name]?.memory || 'N/A'
                });
            });
            
            resolve({ pods });
        });
    });
}

// HTTP server
const server = http.createServer(async (req, res) => {
    if (req.url === '/') {
        const html = fs.readFileSync(path.join(__dirname, 'simple-metrics.html'), 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(html);
    } else if (req.url === '/api/metrics') {
        const data = await getPodsData();
        res.writeHead(200, { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(data));
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log(`
🚀 SIMPLE METRICS SERVER (NO WEBSOCKET BS)
   http://localhost:${PORT}/
   
   Just HTTP polling every 2 seconds.
    `);
});