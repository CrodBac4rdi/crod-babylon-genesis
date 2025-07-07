const { ipcRenderer } = require('electron');
const axios = require('axios');

let currentTab = 'blockchain';
const API_URL = 'http://localhost:8001';

// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
    currentTab = tabName;
    
    if (tabName === 'blockchain') {
        loadBlockchain();
    }
}

// Load blockchain data
async function loadBlockchain() {
    try {
        // Load from API
        const response = await axios.get(`${API_URL}/blocks`);
        const blocks = response.data;
        
        // Save to local database
        for (const block of blocks) {
            await ipcRenderer.invoke('save-block', block);
        }
        
        // Display blocks
        displayBlocks(blocks);
        
        // Update stats
        const statsResponse = await axios.get(`${API_URL}/stats`);
        updateStats(statsResponse.data);
        
    } catch (error) {
        console.error('Error loading blockchain:', error);
        // Load from local database if API fails
        const blocks = await ipcRenderer.invoke('get-blocks');
        displayBlocks(blocks);
        
        const stats = await ipcRenderer.invoke('get-stats');
        updateStats(stats);
    }
}

function displayBlocks(blocks) {
    const container = document.getElementById('blocks-container');
    container.innerHTML = '';
    
    blocks.forEach(block => {
        const blockEl = document.createElement('div');
        blockEl.className = 'block';
        blockEl.innerHTML = `
            <h3>Block #${block.index || block.block_index}</h3>
            <p><strong>Hash:</strong> ${block.hash}</p>
            <p><strong>Previous Hash:</strong> ${block.previous_hash}</p>
            <p><strong>Timestamp:</strong> ${block.timestamp}</p>
            <p><strong>Consciousness:</strong> ${block.consciousness_level}</p>
            <p><strong>Data:</strong> <pre>${JSON.stringify(JSON.parse(block.data || '{}'), null, 2)}</pre></p>
        `;
        container.appendChild(blockEl);
    });
}

function updateStats(stats) {
    document.getElementById('total-blocks').textContent = stats.height || stats.blockCount || 0;
    document.getElementById('total-consciousness').textContent = (stats.total_consciousness || stats.totalConsciousness || 0).toFixed(2);
    document.getElementById('avg-consciousness').textContent = (stats.average_consciousness || stats.avgConsciousness || 0).toFixed(3);
}

// Mining
document.getElementById('consciousness-slider').addEventListener('input', (e) => {
    document.getElementById('consciousness-value').textContent = e.target.value;
});

async function mineBlock() {
    const data = document.getElementById('block-data').value;
    const consciousness = parseFloat(document.getElementById('consciousness-slider').value);
    
    try {
        const response = await axios.post(`${API_URL}/blocks/add`, {
            data: { content: data, timestamp: new Date().toISOString() },
            consciousness_level: consciousness
        });
        
        alert('Block mined successfully!');
        document.getElementById('block-data').value = '';
        
        if (currentTab === 'blockchain') {
            loadBlockchain();
        }
    } catch (error) {
        alert('Error mining block: ' + error.message);
    }
}

// LLaMA Integration
async function askLLaMA() {
    const input = document.getElementById('llama-input');
    const prompt = input.value;
    if (!prompt) return;
    
    const messagesDiv = document.getElementById('chat-messages');
    
    // Add user message
    messagesDiv.innerHTML += `<div class="message user">${prompt}</div>`;
    input.value = '';
    
    try {
        const response = await ipcRenderer.invoke('query-llama', prompt);
        messagesDiv.innerHTML += `<div class="message assistant">${response}</div>`;
    } catch (error) {
        messagesDiv.innerHTML += `<div class="message assistant">Error: ${error.message}</div>`;
    }
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// 3D Visualization
function start3D() {
    const canvas = document.getElementById('canvas3d');
    const ctx = canvas.getContext('2d');
    
    // Simple 3D blockchain visualization
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    let rotation = 0;
    
    function draw() {
        ctx.fillStyle = '#111';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw rotating blocks
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        
        for (let i = 0; i < 5; i++) {
            const angle = (rotation + i * 72) * Math.PI / 180;
            const x = centerX + Math.cos(angle) * 100;
            const y = centerY + Math.sin(angle) * 100;
            
            ctx.fillStyle = `hsl(${i * 60}, 70%, 50%)`;
            ctx.fillRect(x - 30, y - 30, 60, 60);
            
            ctx.strokeStyle = '#fff';
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.stroke();
        }
        
        rotation += 1;
        requestAnimationFrame(draw);
    }
    
    draw();
}

// Database operations
async function exportDatabase() {
    alert('Database export feature coming soon!');
}

async function clearDatabase() {
    if (confirm('Are you sure you want to clear all data?')) {
        // Implement database clear
        alert('Database cleared!');
    }
}

// Settings
function saveSettings() {
    const apiUrl = document.getElementById('api-url').value;
    const llamaPath = document.getElementById('llama-path').value;
    
    localStorage.setItem('api-url', apiUrl);
    localStorage.setItem('llama-path', llamaPath);
    
    alert('Settings saved!');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadBlockchain();
    setInterval(loadBlockchain, 5000); // Refresh every 5 seconds
    
    // Load settings
    const savedApiUrl = localStorage.getItem('api-url');
    if (savedApiUrl) {
        document.getElementById('api-url').value = savedApiUrl;
    }
});

// Make functions global
window.switchTab = switchTab;
window.mineBlock = mineBlock;
window.askLLaMA = askLLaMA;
window.start3D = start3D;
window.exportDatabase = exportDatabase;
window.clearDatabase = clearDatabase;
window.saveSettings = saveSettings;