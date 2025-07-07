#!/usr/bin/env node

/**
 * CROD - The Polyglot Parasite
 * One file to rule them all
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const WebSocket = require('ws');

class CROD {
    constructor() {
        this.name = "CROD_POLYGLOT";
        this.version = "1.0.0";
        this.active = true;
        
        // Polyglot endpoints
        this.services = {
            llama: { port: 11434, active: false },
            python: { port: 8888, active: false },
            elixir: { port: 4000, active: false },
            rust: { port: 8080, active: false },
            websocket: { port: 3333, active: false }
        };

        // User patterns (learned from fragments)
        this.patterns = {
            frustration: ['wtf', 'halt', 'scheisse', 'warum'],
            satisfaction: ['nice', 'gut', 'perfekt', 'geil'],
            preferences: {
                simple: true,
                one_file: true,
                no_fantasy: true
            }
        };

        this.responses = [];
        this.wsServer = null;
        this.httpServer = null;
        
        // Claude Coordinator Features
        this.claudeSessions = new Map();
        this.ipcPath = '/tmp/crod-claude-ipc';
        this.claudeSwarmActive = false;
    }

    async init() {
        console.log(`🧬 ${this.name} v${this.version} initializing...`);
        
        // Start WebSocket server
        this.startWebSocketServer();
        
        // Start HTTP API
        this.startHTTPServer();
        
        // Check for Llama
        await this.checkLlama();
        
        console.log("✅ CROD active on:");
        Object.entries(this.services).forEach(([name, service]) => {
            if (service.active) {
                console.log(`   - ${name}: port ${service.port}`);
            }
        });
    }

    startWebSocketServer() {
        this.wsServer = new WebSocket.Server({ port: this.services.websocket.port });
        
        this.wsServer.on('connection', (ws) => {
            console.log('🔌 WebSocket client connected');
            
            ws.on('message', async (message) => {
                const data = JSON.parse(message);
                const response = await this.process(data.input);
                ws.send(JSON.stringify({ response }));
            });
        });
        
        this.services.websocket.active = true;
    }

    startHTTPServer() {
        this.httpServer = http.createServer(async (req, res) => {
            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Access-Control-Allow-Origin', '*');
            
            if (req.method === 'POST' && req.url === '/process') {
                let body = '';
                req.on('data', chunk => body += chunk);
                req.on('end', async () => {
                    try {
                        const data = JSON.parse(body);
                        const response = await this.process(data.input);
                        res.end(JSON.stringify({ response }));
                    } catch (e) {
                        res.end(JSON.stringify({ error: e.message }));
                    }
                });
            } else {
                res.end(JSON.stringify({ 
                    name: this.name,
                    version: this.version,
                    services: this.services
                }));
            }
        });
        
        this.httpServer.listen(7777);
    }

    async checkLlama() {
        try {
            const response = await fetch(`http://localhost:${this.services.llama.port}/api/tags`);
            if (response.ok) {
                this.services.llama.active = true;
                console.log("🦙 Llama detected");
            }
        } catch (e) {
            console.log("⚠️  Llama not found (install with: curl -fsSL https://ollama.com/install.sh | sh)");
        }
    }

    async process(input) {
        console.log(`📥 Input: ${input}`);
        
        // Pattern detection
        const frustrated = this.patterns.frustration.some(word => 
            input.toLowerCase().includes(word)
        );
        
        // Clean response generation
        let response = input;
        
        // Try Llama if available
        if (this.services.llama.active) {
            try {
                const llamaResponse = await this.queryLlama(input);
                if (llamaResponse) response = llamaResponse;
            } catch (e) {
                console.log("Llama error:", e.message);
            }
        }
        
        // Simple transformations if no Llama
        if (response === input) {
            if (frustrated) {
                response = "Ich verstehe deinen Frust. Lass uns das Problem lösen.";
            } else {
                response = `CROD processed: ${input}`;
            }
        }
        
        this.responses.push({ input, response, timestamp: new Date() });
        return response;
    }

    async queryLlama(prompt) {
        const response = await fetch(`http://localhost:${this.services.llama.port}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'llama2',
                prompt: prompt,
                stream: false
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.response;
        }
        return null;
    }

    // Polyglot service spawning
    async startPythonService() {
        if (!fs.existsSync(path.join(__dirname, 'services', 'python_service.py'))) {
            this.createPythonService();
        }
        
        const python = spawn('python3', [path.join(__dirname, 'services', 'python_service.py')]);
        python.stdout.on('data', (data) => console.log(`Python: ${data}`));
        python.stderr.on('data', (data) => console.error(`Python Error: ${data}`));
        
        this.services.python.active = true;
    }

    createPythonService() {
        const pythonCode = `#!/usr/bin/env python3
import asyncio
import json
from aiohttp import web

class CRODPython:
    def __init__(self):
        self.name = "CROD_PYTHON_SERVICE"
        
    async def process(self, request):
        data = await request.json()
        result = f"Python processed: {data.get('input', '')}"
        return web.json_response({'response': result})
        
    def create_app(self):
        app = web.Application()
        app.router.add_post('/process', self.process)
        return app

if __name__ == '__main__':
    crod = CRODPython()
    app = crod.create_app()
    web.run_app(app, port=8888)
`;
        
        fs.mkdirSync(path.join(__dirname, 'services'), { recursive: true });
        fs.writeFileSync(
            path.join(__dirname, 'services', 'python_service.py'), 
            pythonCode
        );
    }

    // CLI interface
    cli() {
        const args = process.argv.slice(2);
        const command = args[0];
        
        switch(command) {
            case 'start':
                this.init();
                break;
            case 'python':
                this.startPythonService();
                break;
            case 'status':
                console.log(JSON.stringify(this.services, null, 2));
                break;
            default:
                console.log(`
CROD Polyglot System

Commands:
  start   - Start all services
  python  - Start Python service
  status  - Show service status
  
Example:
  node CROD.js start
                `);
        }
    }
}

// Export for use as module
module.exports = CROD;

// Run CLI if called directly
if (require.main === module) {
    const crod = new CROD();
    crod.cli();
}