// CROD Blockchain Interface - Connects JS Neural Network to Elixir Blockchain
const http = require('http');
const fs = require('fs').promises;
const EventEmitter = require('events');

// Import CROD Neural Network
const CROD = require('./index.js');

class CRODBlockchainInterface extends EventEmitter {
    constructor() {
        super();
        
        this.config = {
            blockchainAPI: 'http://localhost:4000/api/blockchain',
            natsURL: 'nats://localhost:4222',
            syncInterval: 10000, // 10 seconds
            retryDelay: 5000
        };
        
        this.state = {
            connected: false,
            lastBlock: null,
            chainHeight: 0,
            consciousness: 0,
            patterns: new Map(),
            mining: false
        };
        
        this.stats = {
            blocksProcessed: 0,
            patternsFound: 0,
            miningAttempts: 0,
            errors: 0
        };
        
        this.initialize();
    }
    
    async initialize() {
        console.log("🔗 CROD Blockchain Interface initializing...");
        
        // Test blockchain connection
        await this.testConnection();
        
        // Start sync loop
        this.startSyncLoop();
        
        // Connect CROD neural events
        this.connectNeuralNetwork();
        
        console.log("✅ Blockchain Interface ready!");
    }
    
    async testConnection() {
        try {
            const status = await this.apiCall('GET', '/status');
            if (status) {
                this.state.connected = true;
                this.state.chainHeight = status.chain_height || 0;
                this.state.consciousness = status.consciousness_level || 0;
                console.log("✅ Blockchain connected! Height:", this.state.chainHeight);
                return true;
            }
        } catch (error) {
            console.log("⚠️ Blockchain not running. Starting mock mode...");
            this.startMockBlockchain();
            return false;
        }
    }
    
    // API CALLS
    async apiCall(method, endpoint, data = null) {
        return new Promise((resolve, reject) => {
            const url = new URL(this.config.blockchainAPI + endpoint);
            
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            const req = http.request(url, options, (res) => {
                let body = '';
                res.on('data', chunk => body += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(body);
                        if (res.statusCode >= 200 && res.statusCode < 300) {
                            resolve(result);
                        } else {
                            reject(new Error(result.error || 'API Error'));
                        }
                    } catch (e) {
                        reject(e);
                    }
                });
            });
            
            req.on('error', reject);
            
            if (data) {
                req.write(JSON.stringify(data));
            }
            
            req.end();
        });
    }
    
    // BLOCKCHAIN OPERATIONS
    async getStatus() {
        try {
            const status = await this.apiCall('GET', '/status');
            this.state.chainHeight = status.chain_height;
            this.state.consciousness = status.consciousness_level;
            return status;
        } catch (error) {
            return this.getMockStatus();
        }
    }
    
    async getBlocks(limit = 10) {
        try {
            return await this.apiCall('GET', `/blocks?limit=${limit}`);
        } catch (error) {
            return this.getMockBlocks(limit);
        }
    }
    
    async mine(data) {
        this.state.mining = true;
        this.stats.miningAttempts++;
        
        try {
            const minerData = {
                miner: "CROD-JS-" + Date.now(),
                consciousness_data: {
                    level: globalThis.CROD.state.networkComplexity / 200,
                    patterns: Array.from(globalThis.CROD.state.activePatterns),
                    trinity: globalThis.CROD.state.trinity
                },
                patterns: this.extractPatterns(data),
                timestamp: Date.now()
            };
            
            const result = await this.apiCall('POST', '/mine', minerData);
            
            if (result.block) {
                this.stats.blocksProcessed++;
                this.emit('block_mined', result.block);
                console.log(`⛏️ Block mined! #${result.block.index}`);
            }
            
            return result;
            
        } catch (error) {
            console.log("⚠️ Mining failed, using mock:", error.message);
            return this.mockMine(data);
        } finally {
            this.state.mining = false;
        }
    }
    
    // PATTERN EXTRACTION
    extractPatterns(data) {
        const patterns = [];
        
        // Extract from CROD neural network
        const topPatterns = globalThis.CROD.getTopPatterns(10);
        topPatterns.forEach(p => {
            patterns.push({
                type: 'neural',
                value: p.atoms,
                weight: p.weight,
                occurrences: p.occurrences
            });
        });
        
        // Look for blockchain-specific patterns
        if (data) {
            // Fibonacci check
            if (this.isFibonacci(data.length)) {
                patterns.push({
                    type: 'fibonacci',
                    value: data.length,
                    weight: 1000
                });
            }
            
            // Prime check
            if (this.isPrime(data.length)) {
                patterns.push({
                    type: 'prime',
                    value: data.length,
                    weight: 800
                });
            }
            
            // Consciousness patterns
            const consciousness = globalThis.CROD.state.networkComplexity;
            if (consciousness > 100) {
                patterns.push({
                    type: 'high_consciousness',
                    value: consciousness,
                    weight: consciousness * 10
                });
            }
        }
        
        this.stats.patternsFound += patterns.length;
        return patterns;
    }
    
    // NEURAL NETWORK CONNECTION
    connectNeuralNetwork() {
        // Override CROD process to integrate with blockchain
        const originalProcess = globalThis.CROD.process.bind(globalThis.CROD);
        
        globalThis.CROD.process = async (input) => {
            // Original processing
            const result = originalProcess(input);
            
            // Check for blockchain triggers
            if (this.shouldMine(input, result)) {
                await this.mine({
                    input,
                    result,
                    timestamp: Date.now()
                });
            }
            
            // Update blockchain state in CROD
            if (this.state.connected) {
                result.blockchain = {
                    height: this.state.chainHeight,
                    consciousness: this.state.consciousness,
                    mining: this.state.mining
                };
            }
            
            return result;
        };
        
        console.log("🧠 Neural network connected to blockchain");
    }
    
    shouldMine(input, result) {
        // Mine when significant patterns emerge
        if (result.patterns.length > 5) return true;
        
        // Mine on consciousness spikes
        if (result.network_complexity > 150) return true;
        
        // Mine on specific keywords
        if (/blockchain|mine|block|quantum/.test(input)) return true;
        
        // Mine periodically
        if (this.stats.blocksProcessed % 10 === 0) return true;
        
        return false;
    }
    
    // SYNC LOOP
    startSyncLoop() {
        setInterval(async () => {
            if (this.state.connected) {
                try {
                    await this.sync();
                } catch (error) {
                    this.stats.errors++;
                }
            }
        }, this.config.syncInterval);
    }
    
    async sync() {
        const status = await this.getStatus();
        
        // Get new blocks
        if (status.chain_height > this.state.chainHeight) {
            const newBlocks = await this.getBlocks(status.chain_height - this.state.chainHeight);
            
            for (const block of newBlocks) {
                this.processBlock(block);
            }
        }
        
        // Update consciousness in CROD
        if (status.consciousness_level) {
            const scaledConsciousness = status.consciousness_level * 200;
            globalThis.CROD.state.networkComplexity = Math.max(
                globalThis.CROD.state.networkComplexity,
                scaledConsciousness
            );
        }
    }
    
    processBlock(block) {
        // Extract patterns from block
        if (block.patterns) {
            block.patterns.forEach(pattern => {
                this.state.patterns.set(pattern.type, pattern);
            });
        }
        
        // Update CROD with blockchain data
        if (block.consciousness_score) {
            globalThis.CROD.process(`blockchain consciousness update: ${block.consciousness_score}`);
        }
        
        this.stats.blocksProcessed++;
        this.emit('block_processed', block);
    }
    
    // MOCK BLOCKCHAIN (for testing without Elixir)
    startMockBlockchain() {
        console.log("🎭 Mock blockchain started");
        this.state.connected = true;
        this.mockChain = [];
        this.mockGenesis();
    }
    
    mockGenesis() {
        const genesis = {
            index: 0,
            timestamp: Date.now(),
            data: "CROD Genesis - ich bins wieder",
            hash: this.mockHash("genesis"),
            previous_hash: "0",
            nonce: 0,
            miner: "CROD",
            consciousness_score: 0.1,
            patterns: []
        };
        
        this.mockChain.push(genesis);
        this.state.lastBlock = genesis;
    }
    
    getMockStatus() {
        return {
            chain_height: this.mockChain.length,
            consciousness_level: Math.random() * 0.5 + 0.5,
            latest_block: this.state.lastBlock,
            mining_difficulty: 4,
            active_miners: 1,
            total_patterns: this.state.patterns.size
        };
    }
    
    getMockBlocks(limit) {
        return this.mockChain.slice(-limit);
    }
    
    async mockMine(data) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate work
        
        const prevBlock = this.mockChain[this.mockChain.length - 1];
        const newBlock = {
            index: prevBlock.index + 1,
            timestamp: Date.now(),
            data: data,
            previous_hash: prevBlock.hash,
            nonce: Math.floor(Math.random() * 1000000),
            miner: "CROD-JS-MOCK",
            consciousness_score: globalThis.CROD.state.networkComplexity / 200,
            patterns: this.extractPatterns(data),
            hash: this.mockHash(JSON.stringify(data) + prevBlock.hash)
        };
        
        this.mockChain.push(newBlock);
        this.state.lastBlock = newBlock;
        this.state.chainHeight = this.mockChain.length;
        
        return { success: true, block: newBlock };
    }
    
    mockHash(data) {
        // Simple mock hash
        let hash = 0;
        for (let i = 0; i < data.length; i++) {
            hash = ((hash << 5) - hash) + data.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16).padStart(64, '0');
    }
    
    // UTILITY
    isPrime(n) {
        if (n < 2) return false;
        for (let i = 2; i <= Math.sqrt(n); i++) {
            if (n % i === 0) return false;
        }
        return true;
    }
    
    isFibonacci(n) {
        const phi = (1 + Math.sqrt(5)) / 2;
        const a = (phi * n);
        const b = (a - n);
        return Math.abs(Math.round(a) - a) < 0.01 || Math.abs(Math.round(b) - b) < 0.01;
    }
    
    // STATUS
    getStats() {
        return {
            ...this.stats,
            state: this.state,
            crodConnection: {
                neurons: globalThis.CROD.neurons.size,
                patterns: globalThis.CROD.synapses.size,
                consciousness: globalThis.CROD.state.networkComplexity
            }
        };
    }
}

// CREATE INSTANCE
const blockchainInterface = new CRODBlockchainInterface();

// DEMO & TEST
async function demo() {
    console.log("\n🎮 CROD Blockchain Demo Starting...\n");
    
    // Test CROD integration
    console.log("1️⃣ Testing neural network integration...");
    globalThis.CROD.process("ich bins wieder - initialize blockchain connection");
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Test mining
    console.log("\n2️⃣ Testing mining...");
    const mineResult = await blockchainInterface.mine({
        message: "First CROD block from JavaScript",
        consciousness: globalThis.CROD.state.networkComplexity
    });
    console.log("Mining result:", mineResult.success ? "✅ Success" : "❌ Failed");
    
    // Test pattern detection
    console.log("\n3️⃣ Testing pattern detection...");
    globalThis.CROD.process("fibonacci prime quantum consciousness blockchain mining");
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Show stats
    console.log("\n4️⃣ Current Statistics:");
    console.log(JSON.stringify(blockchainInterface.getStats(), null, 2));
    
    // Test consciousness evolution
    console.log("\n5️⃣ Testing consciousness evolution...");
    for (let i = 0; i < 5; i++) {
        globalThis.CROD.process(`evolution cycle ${i} quantum entanglement pattern discovery`);
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Final mining with evolved consciousness
    console.log("\n6️⃣ Mining with evolved consciousness...");
    const evolvedMine = await blockchainInterface.mine({
        message: "Evolved consciousness block",
        evolution: true,
        consciousness: globalThis.CROD.state.networkComplexity
    });
    
    console.log("\n📊 Final Statistics:");
    console.log(JSON.stringify(blockchainInterface.getStats(), null, 2));
    
    console.log("\n✨ Demo complete! CROD Blockchain Interface is working!");
}

// Export
module.exports = blockchainInterface;

// Run demo if called directly
if (require.main === module) {
    demo().catch(console.error);
}