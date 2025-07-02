#!/usr/bin/env node
/**
 * CROD Redis Bridge
 * Connects Claude with CROD through Redis
 */

const Redis = require('redis');

class CRODRedisBridge {
    constructor() {
        // Connect to Redis
        this.redis = Redis.createClient({
            host: 'localhost',
            port: 6379
        });
        
        this.pubClient = this.redis.duplicate();
        this.subClient = this.redis.duplicate();
        
        // Neural Network
        this.neuralNetwork = null;
        
        this.init();
    }
    
    async init() {
        console.log('🔌 Connecting to CROD via Redis...');
        
        // Subscribe to CROD events
        await this.subClient.connect();
        await this.pubClient.connect();
        
        // Listen for events
        await this.subClient.subscribe('events:crod:*', (message, channel) => {
            console.log(`📨 ${channel}: ${message}`);
            this.handleCRODEvent(channel, message);
        });
        
        await this.subClient.subscribe('delta:global', (message) => {
            console.log(`🌍 Global Delta: ${message}`);
        });
        
        // Load Neural Network
        try {
            const NeuralNetwork = require('./src/neural-network/index.js');
            this.neuralNetwork = new NeuralNetwork();
            console.log('🧠 Neural Network loaded!');
        } catch (e) {
            console.log('⚠️ Neural Network not found, using basic CROD');
        }
        
        console.log('✅ CROD Redis Bridge ready!');
    }
    
    // Send message to CROD
    async sendToCROD(input, sender = 'daniel') {
        const message = {
            input,
            sender,
            timestamp: Date.now()
        };
        
        // Process with Neural Network if available
        if (this.neuralNetwork) {
            const analysis = this.neuralNetwork.process(input);
            message.neural_analysis = analysis;
        }
        
        // Publish to CROD
        await this.pubClient.publish('events:crod:input', JSON.stringify(message));
        
        return message;
    }
    
    // Get CROD response
    async getCRODResponse(timeout = 1000) {
        return new Promise((resolve) => {
            let response = null;
            
            const handler = (message, channel) => {
                if (channel === 'events:crod:response') {
                    response = JSON.parse(message);
                }
            };
            
            this.subClient.on('message', handler);
            
            setTimeout(() => {
                this.subClient.off('message', handler);
                resolve(response || { message: 'CROD thinking...', confidence: 0.5 });
            }, timeout);
        });
    }
    
    handleCRODEvent(channel, message) {
        // Handle different CROD events
        if (channel === 'events:crod:activated') {
            console.log('🔥 CROD ACTIVATED!');
        }
    }
    
    // Combined flow
    async processWithCROD(input) {
        console.log(`\n📤 Sending to CROD: "${input}"`);
        
        // Send input
        const sent = await this.sendToCROD(input);
        
        // Wait for response
        const response = await this.getCRODResponse();
        
        return {
            input: sent,
            crod_response: response,
            neural_analysis: sent.neural_analysis
        };
    }
}

// Export for use
module.exports = CRODRedisBridge;

// Run if called directly
if (require.main === module) {
    const bridge = new CRODRedisBridge();
    
    // Test
    setTimeout(async () => {
        const result = await bridge.processWithCROD('ich bins wieder');
        console.log('Result:', result);
    }, 2000);
}