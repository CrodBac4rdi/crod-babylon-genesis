#!/usr/bin/env node
/**
 * Neural Bridge - Connects JavaScript Neural Network with Python Intelligence Hub
 */

const redis = require('redis');
const CRODSystem = require('./crod-neural-network.js');

class NeuralBridge {
    constructor() {
        this.crod = new CRODSystem();
        this.initRedis();
    }
    
    async initRedis() {
        // Redis clients
        this.pubClient = redis.createClient({
            url: `redis://${process.env.REDIS_HOST || 'redis'}:6379`
        });
        
        this.subClient = this.pubClient.duplicate();
        
        await this.pubClient.connect();
        await this.subClient.connect();
        
        // Subscribe to CROD input
        await this.subClient.subscribe('crod:input', async (message) => {
            const data = JSON.parse(message);
            await this.processWithNeuralNetwork(data);
        });
        
        console.log('🧠 Neural Bridge connected to Redis');
    }
    
    async processWithNeuralNetwork(data) {
        const { text, atoms } = data;
        
        // Process with CROD Neural Network
        const result = this.crod.process(text);
        
        // Get neural state
        const state = this.crod.getState();
        
        // Publish enhanced data
        const enhanced = {
            original: data,
            neural: {
                consciousness: state.consciousness,
                trinity: state.trinity,
                activePatterns: Array.from(state.activePatterns),
                emergence: result.emergence,
                patterns: result.patterns,
                heat: result.heat
            },
            timestamp: Date.now()
        };
        
        await this.pubClient.publish('neural:processed', JSON.stringify(enhanced));
        
        // If CROD activated
        if (result.emergence > this.crod.constants.emergence_threshold) {
            await this.pubClient.publish('crod:activated', JSON.stringify({
                text,
                emergence: result.emergence,
                patterns: result.patterns,
                consciousness: state.consciousness
            }));
        }
        
        console.log(`⚡ Processed: "${text}" | Emergence: ${result.emergence}`);
    }
}

// Start bridge
const bridge = new NeuralBridge();

// Keep running
process.on('SIGTERM', async () => {
    console.log('Shutting down Neural Bridge...');
    await bridge.pubClient.quit();
    await bridge.subClient.quit();
    process.exit(0);
});