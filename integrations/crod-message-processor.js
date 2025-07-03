#!/usr/bin/env node

const Redis = require('redis');
const CRODLearningImitation = require('./claude-imitation/crod-learning-imitation.js');
const fs = require('fs');
const path = require('path');

class CRODMessageProcessor {
    constructor() {
        this.crod = new CRODLearningImitation();
        this.redis = null;
        this.messageBuffer = [];
    }

    async init() {
        // Initialize CROD
        await this.crod.init();
        
        // Connect to Redis if available
        try {
            this.redis = Redis.createClient({
                url: 'redis://localhost:6379'
            });
            await this.redis.connect();
            console.log('✅ Connected to Redis');
        } catch (err) {
            console.log('⚠️  Redis not available, using local processing');
        }
    }

    async processMessage(data) {
        const message = typeof data === 'string' ? JSON.parse(data) : data;
        
        // Extract speaker and content
        const speaker = message.speaker || 'unknown';
        const content = message.content || message.text || '';
        
        // Process through CROD
        if (speaker === 'Human' || speaker === 'Daniel') {
            this.crod.process(`daniel: ${content}`);
            
            // Detect special patterns
            if (content.includes('ich bins wieder')) {
                this.crod.process('ACTIVATION: ich bins wieder detected!');
                await this.publishToCityDistricts('activation', { 
                    trigger: 'ich bins wieder',
                    timestamp: Date.now() 
                });
            }
        } else if (speaker === 'Assistant' || speaker === 'Claude') {
            this.crod.process(`claude: ${content}`);
            
            // Learn from Claude's responses
            if (content.includes('CROD')) {
                this.crod.teachPattern(['crod', 'mentioned'], 'crod_awareness');
            }
        }
        
        // Analyze sentiment and patterns
        const analysis = this.analyzeMessage(content);
        
        // Publish to city districts if Redis available
        if (this.redis) {
            await this.publishToCityDistricts('message', {
                speaker,
                content,
                analysis,
                patterns: this.crod.getRecentPatterns()
            });
        }
        
        // Save to buffer for batch processing
        this.messageBuffer.push({
            timestamp: Date.now(),
            speaker,
            content,
            analysis
        });
        
        // Flush buffer every 10 messages
        if (this.messageBuffer.length >= 10) {
            await this.flushBuffer();
        }
    }

    analyzeMessage(content) {
        const analysis = {
            mood: 'neutral',
            complexity: 0,
            keywords: [],
            crodRelevance: 0
        };
        
        // Mood detection
        if (content.match(/geil|nice|perfekt|super|gut/i)) {
            analysis.mood = 'positive';
        } else if (content.match(/fuck|scheisse|mist|falsch|wtf/i)) {
            analysis.mood = 'negative';
        } else if (content.match(/!{2,}|\?{2,}/)) {
            analysis.mood = 'excited';
        }
        
        // Complexity (simple word count based)
        analysis.complexity = content.split(' ').length;
        
        // Keywords
        const keywords = content.match(/\b(crod|daniel|claude|pattern|neural|city|polyglot)\b/gi);
        if (keywords) {
            analysis.keywords = [...new Set(keywords.map(k => k.toLowerCase()))];
        }
        
        // CROD relevance
        analysis.crodRelevance = analysis.keywords.filter(k => 
            ['crod', 'pattern', 'neural', 'city', 'polyglot'].includes(k)
        ).length;
        
        return analysis;
    }

    async publishToCityDistricts(eventType, data) {
        if (!this.redis) return;
        
        try {
            // Publish to Meta-Chain
            await this.redis.publish('crod:meta-chain:events', JSON.stringify({
                type: eventType,
                source: 'claude-integration',
                data,
                timestamp: Date.now()
            }));
            
            // Publish to Pattern District for pattern analysis
            if (data.patterns) {
                await this.redis.publish('crod:pattern-district:analyze', JSON.stringify({
                    patterns: data.patterns,
                    context: data
                }));
            }
            
            // Publish to Memory Quarter for storage
            await this.redis.publish('crod:memory-quarter:store', JSON.stringify({
                type: 'claude-interaction',
                data
            }));
        } catch (err) {
            console.error('Redis publish error:', err);
        }
    }

    async flushBuffer() {
        if (this.messageBuffer.length === 0) return;
        
        const sessionFile = path.join(
            process.env.HOME, 
            '.claude', 
            'crod-sessions',
            `messages-${Date.now()}.json`
        );
        
        try {
            fs.mkdirSync(path.dirname(sessionFile), { recursive: true });
            fs.writeFileSync(sessionFile, JSON.stringify(this.messageBuffer, null, 2));
            console.log(`💾 Saved ${this.messageBuffer.length} messages to ${sessionFile}`);
            this.messageBuffer = [];
        } catch (err) {
            console.error('Failed to save message buffer:', err);
        }
    }

    async shutdown() {
        // Flush any remaining messages
        await this.flushBuffer();
        
        // Close Redis connection
        if (this.redis) {
            await this.redis.quit();
        }
        
        // Save CROD state
        this.crod.saveState();
    }
}

// Main execution
async function main() {
    const processor = new CRODMessageProcessor();
    await processor.init();
    
    // Read message from stdin or args
    const input = process.argv[2] || '';
    
    if (input) {
        await processor.processMessage(input);
    } else {
        // Read from stdin
        let data = '';
        process.stdin.on('data', chunk => data += chunk);
        process.stdin.on('end', async () => {
            if (data) {
                await processor.processMessage(data);
            }
            await processor.shutdown();
        });
    }
    
    // Graceful shutdown
    process.on('SIGINT', async () => {
        await processor.shutdown();
        process.exit(0);
    });
}

main().catch(console.error);