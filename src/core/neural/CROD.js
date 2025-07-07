#!/usr/bin/env node

const express = require('express');
const spawn = require('child_process').spawn;

const app = express();
const PORT = 8200;

app.use(express.json());

app.get('/', function(req, res) {
    const html = '<!DOCTYPE html>' +
        '<html><head><title>CROD</title></head><body>' +
        '<div id="app"></div>' +
        '<script>' +
        'document.body.style.cssText = "margin:0;padding:0;font-family:monospace;background:#0a0a0a;color:#00ff00;height:100vh;";' +
        'document.getElementById("app").innerHTML = ' +
        '"<div style=\\"height:100vh;display:flex;flex-direction:column;\\">" +' +
        '"<h1 style=\\"padding:20px;text-align:center;border-bottom:2px solid #00ff00;margin:0;\\">🧠 CROD</h1>" +' +
        '"<div style=\\"flex:1;padding:20px;display:flex;flex-direction:column;\\">" +' +
        '"<div id=\\"messages\\" style=\\"flex:1;border:2px solid #00ff00;background:#000;padding:15px;overflow-y:auto;margin-bottom:15px;\\"></div>" +' +
        '"<div style=\\"display:flex;gap:10px;\\">" +' +
        '"<input id=\\"input\\" type=\\"text\\" placeholder=\\"Ask me...\\" style=\\"flex:1;padding:15px;background:#111;border:2px solid #00ff00;color:#00ff00;outline:none;\\">" +' +
        '"<button id=\\"send\\" style=\\"padding:15px 30px;background:#00ff00;color:#000;border:none;cursor:pointer;\\">SEND</button>" +' +
        '"</div></div></div>";' +
        'var input = document.getElementById("input");' +
        'var send = document.getElementById("send");' +
        'var messages = document.getElementById("messages");' +
        'function addMessage(type, text) {' +
        '  var div = document.createElement("div");' +
        '  div.style.cssText = "padding:10px;margin:5px 0;border-radius:5px;background:rgba(255,255,0,0.1);";' +
        '  if (type === "user") div.style.background = "rgba(0,255,0,0.1)";' +
        '  if (type === "error") div.style.background = "rgba(255,0,0,0.1)";' +
        '  var icon = type === "user" ? "👤" : type === "error" ? "❌" : "🤖";' +
        '  div.innerHTML = icon + " " + text;' +
        '  messages.appendChild(div);' +
        '  messages.scrollTop = messages.scrollHeight;' +
        '}' +
        'function sendMessage() {' +
        '  var message = input.value.trim();' +
        '  if (!message) return;' +
        '  addMessage("user", message);' +
        '  input.value = "";' +
        '  send.disabled = true;' +
        '  send.textContent = "THINKING...";' +
        '  fetch("/api/chat", {' +
        '    method: "POST",' +
        '    headers: {"Content-Type": "application/json"},' +
        '    body: JSON.stringify({message: message})' +
        '  }).then(function(r) { return r.json(); })' +
        '    .then(function(data) {' +
        '      if (data.success) addMessage("bot", data.response);' +
        '      else addMessage("error", data.error);' +
        '    }).catch(function(e) {' +
        '      addMessage("error", "Connection failed");' +
        '    }).finally(function() {' +
        '      send.disabled = false;' +
        '      send.textContent = "SEND";' +
        '    });' +
        '}' +
        'send.addEventListener("click", sendMessage);' +
        'input.addEventListener("keypress", function(e) { if (e.key === "Enter") sendMessage(); });' +
        'input.focus();' +
        'addMessage("bot", "CROD ready! What do you want to build?");' +
        '</script></body></html>';
    
    res.send(html);
});

app.post('/api/chat', function(req, res) {
    const message = req.body.message;
    
    if (!message) {
        return res.json({ success: false, error: 'No message' });
    }
    
    console.log('Processing:', message);
    
    const ollama = spawn('ollama', ['run', 'qwen2.5-coder']);
    
    let output = '';
    let errorOutput = '';
    
    const timeout = setTimeout(function() {
        ollama.kill();
        res.json({ success: false, error: 'Timeout after 60s' });
    }, 60000);
    
    ollama.stdout.on('data', function(data) {
        output += data.toString();
    });
    
    ollama.stderr.on('data', function(data) {
        errorOutput += data.toString();
    });
    
    ollama.on('close', function(code) {
        clearTimeout(timeout);
        
        if (code === 0) {
            const result = output.trim();
            res.json({ 
                success: true, 
                response: result || 'Qwen responded but output was empty.' 
            });
        } else {
            res.json({ 
                success: false, 
                error: errorOutput || 'Ollama failed with code ' + code 
            });
        }
    });
    
    ollama.on('error', function(error) {
        clearTimeout(timeout);
        if (error.code === 'ENOENT') {
            res.json({ success: false, error: 'Ollama not found' });
        } else {
            res.json({ success: false, error: 'Failed to start Ollama' });
        }
    });
    
    ollama.stdin.write(message + '\n');
    ollama.stdin.end();
});

app.get('/api/status', function(req, res) {
    res.json({
        status: 'running',
        message: 'CROD ready!',
        version: '1.0'
    });
});

app.listen(PORT, 'localhost', function() {
    console.log('🚀 CROD started on http://localhost:' + PORT);
    console.log('💬 Chat ready!');
    console.log('🛑 Stop: Ctrl+C');
});

process.on('SIGINT', function() {
    console.log('\n🛑 Stopping...');
    process.exit(0);
});