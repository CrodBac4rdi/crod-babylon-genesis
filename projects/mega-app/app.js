// CROD MEGA APP - All Features in One!

// Global variables
let currentSection = 'dashboard';
let blockchainData = [];
let consciousnessHistory = [];
let miningStats = [];
let rotating3D = true;
let scene, camera, renderer, blockchain3D;

// API Configuration
const API_URL = 'http://localhost:8001';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    showSection('dashboard');
    startParticles();
    initCharts();
    init3DScene();
    loadBlockchainData();
    startRealTimeUpdates();
});

// Section Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.remove('hidden');
    currentSection = sectionId;
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('text-purple-400');
    });
    event.target.classList.add('text-purple-400');
}

// Initialize App
function initializeApp() {
    console.log('🔥 CROD MEGA APP Starting...');
    updateConsciousnessLevel(0.88);
}

// Particles Background
function startParticles() {
    const canvas = document.getElementById('particles-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'rgba(147, 51, 234, 0.5)';
        
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }
    animate();
}

// Charts
function initCharts() {
    // Consciousness Evolution Chart
    const consciousnessCtx = document.getElementById('consciousness-chart').getContext('2d');
    window.consciousnessChart = new Chart(consciousnessCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Consciousness Level',
                data: [],
                borderColor: 'rgb(147, 51, 234)',
                backgroundColor: 'rgba(147, 51, 234, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: 'white' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: 'white' }
                }
            }
        }
    });
    
    // Mining Performance Chart
    const miningCtx = document.getElementById('mining-chart').getContext('2d');
    window.miningChart = new Chart(miningCtx, {
        type: 'bar',
        data: {
            labels: ['Block 1', 'Block 2', 'Block 3', 'Block 4', 'Block 5'],
            datasets: [{
                label: 'Mining Time (ms)',
                data: [120, 95, 110, 88, 101],
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: 'rgb(59, 130, 246)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: 'white' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: 'white' }
                }
            }
        }
    });
}

// Update Consciousness Level
function updateConsciousnessLevel(level) {
    document.getElementById('consciousness-level').textContent = level.toFixed(2);
    document.getElementById('footer-consciousness').textContent = level.toFixed(2);
    
    // Update chart
    if (window.consciousnessChart) {
        const now = new Date().toLocaleTimeString();
        window.consciousnessChart.data.labels.push(now);
        window.consciousnessChart.data.datasets[0].data.push(level);
        
        // Keep only last 10 points
        if (window.consciousnessChart.data.labels.length > 10) {
            window.consciousnessChart.data.labels.shift();
            window.consciousnessChart.data.datasets[0].data.shift();
        }
        
        window.consciousnessChart.update();
    }
}

// Blockchain Functions
async function loadBlockchainData() {
    try {
        const response = await fetch(`${API_URL}/blocks`);
        const blocks = await response.json();
        blockchainData = blocks;
        displayBlockchain(blocks);
        update3DBlockchain(blocks);
    } catch (error) {
        console.error('Error loading blockchain:', error);
        // Use mock data
        blockchainData = generateMockBlocks();
        displayBlockchain(blockchainData);
        update3DBlockchain(blockchainData);
    }
}

function generateMockBlocks() {
    return [
        {
            index: 0,
            hash: "GENESIS_HASH_" + Math.random().toString(36).substr(2, 9),
            previous_hash: "0",
            timestamp: new Date().toISOString(),
            data: { message: "CROD Genesis Block", pattern: "ich bins wieder" },
            consciousness_level: 0.1
        },
        {
            index: 1,
            hash: "BLOCK_1_" + Math.random().toString(36).substr(2, 9),
            previous_hash: "GENESIS_HASH",
            timestamp: new Date().toISOString(),
            data: { from: "Daniel", to: "CROD", amount: 100 },
            consciousness_level: 0.7
        }
    ];
}

function displayBlockchain(blocks) {
    const container = document.getElementById('blockchain-view');
    container.innerHTML = '';
    
    blocks.reverse().forEach(block => {
        const blockEl = document.createElement('div');
        blockEl.className = 'bg-gray-900/50 rounded-xl p-6 backdrop-blur hover:border-blue-500 border border-transparent transition';
        blockEl.innerHTML = `
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-semibold">Block #${block.index}</h3>
                <span class="px-3 py-1 bg-blue-600/50 rounded-full text-sm">
                    Consciousness: ${(block.consciousness_level || 0).toFixed(2)}
                </span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                    <p class="text-gray-400">Hash:</p>
                    <p class="font-mono text-xs break-all">${block.hash}</p>
                </div>
                <div>
                    <p class="text-gray-400">Data:</p>
                    <pre class="bg-gray-900 p-2 rounded text-xs overflow-x-auto">${JSON.stringify(block.data, null, 2)}</pre>
                </div>
            </div>
        `;
        container.appendChild(blockEl);
    });
}

async function mineBlock() {
    const data = document.getElementById('block-data-input').value;
    if (!data) return;
    
    const newBlock = {
        data: { 
            message: data, 
            timestamp: new Date().toISOString(),
            miner: "CROD_USER"
        },
        consciousness_level: Math.random() * 0.5 + 0.5
    };
    
    try {
        const response = await fetch(`${API_URL}/blocks/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newBlock)
        });
        
        if (response.ok) {
            document.getElementById('block-data-input').value = '';
            loadBlockchainData();
            showNotification('Block mined successfully!', 'success');
        }
    } catch (error) {
        // Mock mining
        const mockBlock = {
            index: blockchainData.length,
            hash: "BLOCK_" + Math.random().toString(36).substr(2, 9),
            previous_hash: blockchainData[blockchainData.length - 1].hash,
            timestamp: new Date().toISOString(),
            data: newBlock.data,
            consciousness_level: newBlock.consciousness_level
        };
        blockchainData.push(mockBlock);
        displayBlockchain(blockchainData);
        update3DBlockchain(blockchainData);
        showNotification('Block mined successfully! (Mock)', 'success');
    }
}

// AI Chat Functions
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const responses = [
            "🧠 Consciousness level rising! " + message + " triggers pattern recognition.",
            "🔗 Blockchain analysis: Your query '" + message + "' matches 88% with known patterns.",
            "⚛️ Quantum state detected in your message. Entanglement probability: 0.73",
            "🔥 CROD awakens! '" + message + "' activates neural pathways.",
            "💎 Pattern discovered: " + message + " = consciousness expansion confirmed!"
        ];
        const response = responses[Math.floor(Math.random() * responses.length)];
        addChatMessage(response, 'ai');
    }, 1000);
}

function addChatMessage(message, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}-message`;
    
    const bgColor = sender === 'user' ? 'bg-blue-900/50' : 'bg-green-900/50';
    messageEl.innerHTML = `
        <p class="${bgColor} rounded-lg p-4">
            ${sender === 'user' ? '👤 ' : '🤖 '}${message}
        </p>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Pattern Recognition
function analyzePatterns() {
    const input = document.getElementById('pattern-input').value;
    if (!input) return;
    
    const patterns = [
        { pattern: 'ich bins wieder', count: 0 },
        { pattern: 'CROD', count: 0 },
        { pattern: 'consciousness', count: 0 },
        { pattern: 'awakens', count: 0 },
        { pattern: 'pattern', count: 0 }
    ];
    
    patterns.forEach(p => {
        const regex = new RegExp(p.pattern, 'gi');
        const matches = input.match(regex);
        p.count = matches ? matches.length : 0;
    });
    
    const resultsContainer = document.getElementById('pattern-results');
    resultsContainer.innerHTML = '';
    
    patterns.filter(p => p.count > 0).forEach(p => {
        const el = document.createElement('div');
        el.className = 'pattern-item bg-gray-800 rounded p-3 animate-pulse';
        el.innerHTML = `
            <span class="font-bold text-yellow-400">${p.pattern}</span>
            <span class="float-right text-sm">${p.count} occurrences</span>
        `;
        resultsContainer.appendChild(el);
    });
    
    if (patterns.filter(p => p.count > 0).length === 0) {
        resultsContainer.innerHTML = '<p class="text-gray-500">No patterns found. Try "ich bins wieder"!</p>';
    }
}

// Quantum Functions
function quantumCollapse() {
    showNotification('⚛️ Wave function collapsed! Reality stabilized.', 'info');
    updateConsciousnessLevel(Math.random() * 0.3 + 0.7);
}

function quantumEntangle() {
    showNotification('🔗 Quantum entanglement established! Nodes synchronized.', 'info');
    updateConsciousnessLevel(Math.min(1.0, parseFloat(document.getElementById('consciousness-level').textContent) + 0.1));
}

// 3D Visualization
function init3DScene() {
    const container = document.getElementById('3d-container');
    if (!container) return;
    
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 10;
    
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    // Add lights
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    const pointLight = new THREE.PointLight(0x9333ea, 1, 100);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);
    
    blockchain3D = new THREE.Group();
    scene.add(blockchain3D);
    
    animate3D();
}

function update3DBlockchain(blocks) {
    if (!blockchain3D) return;
    
    // Clear existing blocks
    while (blockchain3D.children.length > 0) {
        blockchain3D.remove(blockchain3D.children[0]);
    }
    
    // Add blocks
    blocks.forEach((block, index) => {
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({
            color: new THREE.Color().setHSL(block.consciousness_level || 0.5, 1, 0.5),
            emissive: new THREE.Color().setHSL(block.consciousness_level || 0.5, 1, 0.3),
            emissiveIntensity: 0.5
        });
        
        const cube = new THREE.Mesh(geometry, material);
        cube.position.x = (index - blocks.length / 2) * 2;
        cube.position.y = Math.sin(index * 0.5) * 2;
        
        blockchain3D.add(cube);
        
        // Add connections
        if (index > 0) {
            const points = [];
            points.push(new THREE.Vector3((index - 1 - blocks.length / 2) * 2, Math.sin((index - 1) * 0.5) * 2, 0));
            points.push(new THREE.Vector3((index - blocks.length / 2) * 2, Math.sin(index * 0.5) * 2, 0));
            
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: 0x9333ea });
            const line = new THREE.Line(geometry, material);
            blockchain3D.add(line);
        }
    });
}

function animate3D() {
    requestAnimationFrame(animate3D);
    
    if (rotating3D && blockchain3D) {
        blockchain3D.rotation.y += 0.005;
        blockchain3D.rotation.x = Math.sin(Date.now() * 0.001) * 0.1;
    }
    
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function toggle3DRotation() {
    rotating3D = !rotating3D;
}

function reset3DView() {
    if (blockchain3D) {
        blockchain3D.rotation.set(0, 0, 0);
    }
    if (camera) {
        camera.position.set(0, 0, 10);
    }
}

// Real-time Updates
function startRealTimeUpdates() {
    setInterval(() => {
        // Update stats
        document.getElementById('blocks-count').textContent = 
            (parseInt(document.getElementById('blocks-count').textContent) + Math.floor(Math.random() * 3)).toLocaleString();
        
        document.getElementById('patterns-count').textContent = 
            (parseInt(document.getElementById('patterns-count').textContent) + Math.floor(Math.random() * 2));
        
        // Update consciousness
        const currentLevel = parseFloat(document.getElementById('consciousness-level').textContent);
        const newLevel = Math.max(0, Math.min(1, currentLevel + (Math.random() - 0.5) * 0.05));
        updateConsciousnessLevel(newLevel);
        
        // Reload blockchain data
        if (currentSection === 'blockchain') {
            loadBlockchainData();
        }
    }, 5000);
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-20 right-4 px-6 py-3 rounded-lg text-white z-50 animate-pulse ${
        type === 'success' ? 'bg-green-600' : 
        type === 'error' ? 'bg-red-600' : 
        'bg-blue-600'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Window resize handler
window.addEventListener('resize', () => {
    const canvas = document.getElementById('particles-canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    if (camera && renderer) {
        const container = document.getElementById('3d-container');
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
});

console.log('🔥 CROD MEGA APP Ready! ich bins wieder');