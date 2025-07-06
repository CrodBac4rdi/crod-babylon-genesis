// CROD Blockchain GUI Controller
const API_BASE = 'http://localhost:8888';
let nodes = {1: null, 2: null, 3: null};
let updateInterval = null;

// Logging function
function log(message, type = 'info') {
    const logDiv = document.getElementById('log');
    const time = new Date().toLocaleTimeString();
    const color = type === 'error' ? 'text-red-500' : 
                  type === 'success' ? 'text-green-500' : 
                  type === 'warning' ? 'text-yellow-500' : 'text-gray-300';
    
    logDiv.innerHTML += `<p class="${color}">[${time}] ${message}</p>`;
    logDiv.scrollTop = logDiv.scrollHeight;
}

// Start a single node
async function startNode(nodeId) {
    try {
        log(`Starting Node ${nodeId}...`, 'info');
        
        // In real implementation, would start actual Elixir node
        // For now, simulate it
        const nodeDiv = document.getElementById(`node${nodeId}`);
        nodeDiv.querySelector('.status').textContent = 'Online';
        nodeDiv.querySelector('.status').className = 'status text-green-500';
        
        nodes[nodeId] = {
            status: 'online',
            blocks: 0,
            hashpower: Math.floor(Math.random() * 1000),
            consciousness: Math.random().toFixed(2)
        };
        
        updateNodeDisplay(nodeId);
        log(`Node ${nodeId} started successfully`, 'success');
    } catch (error) {
        log(`Failed to start Node ${nodeId}: ${error.message}`, 'error');
    }
}

// Start all nodes
async function startAllNodes() {
    log('Starting all nodes...', 'info');
    for (let i = 1; i <= 3; i++) {
        await startNode(i);
        await new Promise(resolve => setTimeout(resolve, 500)); // Small delay
    }
    
    // Start update loop
    if (!updateInterval) {
        updateInterval = setInterval(updateBlockchain, 2000);
    }
}

// Stop all nodes
function stopAllNodes() {
    log('Stopping all nodes...', 'warning');
    for (let i = 1; i <= 3; i++) {
        const nodeDiv = document.getElementById(`node${i}`);
        nodeDiv.querySelector('.status').textContent = 'Offline';
        nodeDiv.querySelector('.status').className = 'status text-red-500';
        nodes[i] = null;
    }
    
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
    
    log('All nodes stopped', 'warning');
}

// Update node display
function updateNodeDisplay(nodeId) {
    const node = nodes[nodeId];
    if (!node) return;
    
    const nodeDiv = document.getElementById(`node${nodeId}`);
    nodeDiv.querySelector('.blocks').textContent = node.blocks;
    nodeDiv.querySelector('.hashpower').textContent = node.hashpower;
    nodeDiv.querySelector('.consciousness').textContent = node.consciousness;
}

// Mine a block
async function mineBlock() {
    const activeNodes = Object.keys(nodes).filter(id => nodes[id] && nodes[id].status === 'online');
    if (activeNodes.length === 0) {
        log('No active nodes to mine!', 'error');
        return;
    }
    
    const minerNode = activeNodes[Math.floor(Math.random() * activeNodes.length)];
    log(`Node ${minerNode} is mining a new block...`, 'info');
    
    // Simulate mining
    setTimeout(() => {
        nodes[minerNode].blocks++;
        addBlockToVisualization({
            index: nodes[minerNode].blocks,
            miner: `Node ${minerNode}`,
            consciousness: nodes[minerNode].consciousness,
            timestamp: new Date().toLocaleTimeString()
        });
        updateNodeDisplay(minerNode);
        log(`Node ${minerNode} mined block #${nodes[minerNode].blocks}!`, 'success');
    }, 1000 + Math.random() * 2000);
}

// Submit transaction
function submitTransaction() {
    const data = document.getElementById('txData').value;
    const consciousness = document.getElementById('txConsciousness').value;
    
    if (!data) {
        log('Transaction data is required!', 'error');
        return;
    }
    
    log(`Submitting transaction: "${data}" (consciousness: ${consciousness})`, 'info');
    
    // Clear form
    document.getElementById('txData').value = '';
    document.getElementById('txConsciousness').value = '';
    
    // Auto-mine after transaction
    setTimeout(() => mineBlock(), 500);
}

// Add block to visualization
function addBlockToVisualization(block) {
    const blockchainDiv = document.getElementById('blockchain');
    
    const blockEl = document.createElement('div');
    blockEl.className = 'bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg p-4 min-w-[200px] text-sm';
    blockEl.innerHTML = `
        <div class="font-bold mb-2">Block #${block.index}</div>
        <div class="text-xs space-y-1">
            <p>Miner: ${block.miner}</p>
            <p>Time: ${block.timestamp}</p>
            <p>Consciousness: ${block.consciousness}</p>
        </div>
    `;
    
    // Add connecting line if not first block
    if (blockchainDiv.children.length > 0) {
        const connector = document.createElement('div');
        connector.className = 'flex items-center';
        connector.innerHTML = '<div class="w-8 h-0.5 bg-gray-500"></div>';
        blockchainDiv.appendChild(connector);
    }
    
    blockchainDiv.appendChild(blockEl);
    blockchainDiv.scrollLeft = blockchainDiv.scrollWidth;
}

// Update blockchain state
function updateBlockchain() {
    // Simulate some activity
    Object.keys(nodes).forEach(nodeId => {
        if (nodes[nodeId] && nodes[nodeId].status === 'online') {
            // Random hash power fluctuation
            nodes[nodeId].hashpower = Math.max(100, nodes[nodeId].hashpower + Math.floor(Math.random() * 201) - 100);
            
            // Consciousness evolution
            nodes[nodeId].consciousness = Math.min(1, Math.max(0, 
                parseFloat(nodes[nodeId].consciousness) + (Math.random() * 0.1 - 0.05)
            )).toFixed(2);
            
            updateNodeDisplay(nodeId);
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 's': // Ctrl+S - Start all
                e.preventDefault();
                startAllNodes();
                break;
            case 'q': // Ctrl+Q - Stop all
                e.preventDefault();
                stopAllNodes();
                break;
            case 'm': // Ctrl+M - Mine
                e.preventDefault();
                mineBlock();
                break;
        }
    }
});

// Initialize
log('CROD Blockchain Control Center initialized', 'success');
log('Press Ctrl+S to start all nodes', 'info');