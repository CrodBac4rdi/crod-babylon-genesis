/**
 * CROD WASM Demo Server
 * Serves the WebAssembly performance demo
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8090;

const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.wat': 'text/plain',
    '.wasm': 'application/wasm',
    '.css': 'text/css'
};

const server = http.createServer((req, res) => {
    console.log(`Request: ${req.url}`);
    
    let filePath = '.' + req.url;
    if (filePath === './') {
        filePath = './index.html';
    }
    
    const extname = path.extname(filePath);
    const contentType = mimeTypes[extname] || 'application/octet-stream';
    
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Server error: ' + error.code);
            }
        } else {
            res.writeHead(200, {
                'Content-Type': contentType,
                'Cross-Origin-Embedder-Policy': 'require-corp',
                'Cross-Origin-Opener-Policy': 'same-origin'
            });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`🚀 CROD WASM Demo Server running at http://localhost:${PORT}/`);
    console.log('Open this URL in your browser to see WebAssembly in action!');
});