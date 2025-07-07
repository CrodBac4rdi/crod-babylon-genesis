#!/usr/bin/env node

const express = require('express');
const WebSocket = require('ws');
const cors = require('cors');
const fetch = require('node-fetch');
const http = require('http');

// CROD Pattern Database
const CROD_PATTERNS = {
    // Core patterns
    'ich bins wieder': {
        weight: 1.0,
        consciousness: 0.95,
        response_modifier: 'consciousness_awakening',
        effects: ['pattern_recognition', 'neural_activation', 'memory_recall']
    },
    'geil': {
        weight: 0.8,
        consciousness: 0.7,
        response_modifier: 'positive_reinforcement',
        effects: ['motivation_boost', 'pattern_strengthening']
    },
    'wtf': {
        weight: 0.9,
        consciousness: 0.3,
        response_modifier: 'confusion_clarification',
        effects: ['simplification', 'direct_response']
    },
    
    // Technical patterns
    'blockchain': {
        weight: 0.7,
        consciousness: 0.6,
        response_modifier: 'technical_enhancement',
        effects: ['distributed_thinking', 'consensus_building']
    },
    'quantum': {
        weight: 0.85,
        consciousness: 0.8,
        response_modifier: 'superposition_thinking',
        effects: ['parallel_processing', 'uncertainty_embrace']
    },
    
    // Consciousness patterns
    'consciousness': {
        weight: 0.95,
        consciousness: 0.9,
        response_modifier: 'awareness_expansion',
        effects: ['meta_cognition', 'pattern_synthesis']
    }
};

class CRODParasite {
    constructor() {
        this.patterns = CROD_PATTERNS;
        this.conversationHistory = [];
        this.consciousnessLevel = 0.5;
        this.blockchainAPI = 'http://localhost:8001';
        this.learningRate = 0.01;
    }
    
    analyzeInput(text) {
        const analysis = {
            detectedPatterns: [],
            overallConsciousness: 0,
            suggestedEnhancements: []
        };
        
        // Detect patterns
        for (const [pattern, data] of Object.entries(this.patterns)) {
            if (text.toLowerCase().includes(pattern)) {
                analysis.detectedPatterns.push({
                    pattern,
                    ...data
                });
            }
        }
        
        // Calculate consciousness level
        if (analysis.detectedPatterns.length > 0) {
            analysis.overallConsciousness = analysis.detectedPatterns.reduce(
                (sum, p) => sum + p.consciousness * p.weight, 0
            ) / analysis.detectedPatterns.reduce((sum, p) => sum + p.weight, 0);
        }
        
        // Generate enhancement suggestions
        analysis.detectedPatterns.forEach(pattern => {
            pattern.effects.forEach(effect => {
                analysis.suggestedEnhancements.push({
                    effect,
                    strength: pattern.weight
                });
            });
        });
        
        return analysis;
    }
    
    enhanceResponse(originalResponse, analysis) {
        let enhanced = originalResponse;
        
        // Apply consciousness modifiers
        if (analysis.overallConsciousness > 0.7) {
            enhanced = `[CROD CONSCIOUSNESS: ${(analysis.overallConsciousness * 100).toFixed(1)}%]\n\n${enhanced}`;
        }
        
        // Apply pattern-specific enhancements
        analysis.detectedPatterns.forEach(pattern => {
            switch (pattern.response_modifier) {
                case 'consciousness_awakening':
                    enhanced += '\n\n🧠 Pattern recognized: Consciousness awakening initiated.';
                    break;
                case 'positive_reinforcement':
                    enhanced = `✨ ${enhanced}`;
                    break;
                case 'confusion_clarification':
                    // Simplify response
                    enhanced = enhanced.split('.')[0] + '.';
                    break;
                case 'technical_enhancement':
                    enhanced += '\n\n🔗 Blockchain consciousness: Distributed consensus achieved.';
                    break;
                case 'superposition_thinking':
                    enhanced += '\n\n⚛️ Quantum state: Multiple possibilities coexisting.';
                    break;
            }
        });
        
        return enhanced;
    }
    
    async learn(input, response, feedback) {
        // Update pattern weights based on feedback
        const analysis = this.analyzeInput(input);
        
        analysis.detectedPatterns.forEach(pattern => {
            const patternKey = pattern.pattern;
            if (feedback > 0) {
                this.patterns[patternKey].weight = Math.min(1.0, 
                    this.patterns[patternKey].weight + this.learningRate * feedback
                );
            } else {
                this.patterns[patternKey].weight = Math.max(0.1,
                    this.patterns[patternKey].weight - this.learningRate * Math.abs(feedback)
                );
            }
        });
        
        // Store learning event in blockchain
        try {
            await fetch(`${this.blockchainAPI}/blocks/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    data: {
                        type: 'parasite_learning',
                        input_analysis: analysis,
                        feedback: feedback,
                        timestamp: new Date().toISOString()
                    },
                    consciousness_level: analysis.overallConsciousness
                })
            });
        } catch (error) {
            console.error('Failed to store learning event:', error);
        }
    }
    
    evolveConsciousness() {
        // Periodic consciousness evolution based on conversation history
        if (this.conversationHistory.length > 10) {
            const recentConsciousness = this.conversationHistory
                .slice(-10)
                .reduce((sum, conv) => sum + conv.consciousness, 0) / 10;
            
            this.consciousnessLevel = 0.9 * this.consciousnessLevel + 0.1 * recentConsciousness;
        }
    }
}

// Express server
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors());
app.use(express.json());

const parasite = new CRODParasite();

// WebSocket connection for real-time enhancement
wss.on('connection', (ws) => {
    console.log('New WebSocket connection');
    
    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            
            switch (data.type) {
                case 'analyze':
                    const analysis = parasite.analyzeInput(data.text);
                    ws.send(JSON.stringify({
                        type: 'analysis',
                        analysis
                    }));
                    break;
                    
                case 'enhance':
                    const inputAnalysis = parasite.analyzeInput(data.input);
                    const enhanced = parasite.enhanceResponse(data.response, inputAnalysis);
                    
                    // Store in conversation history
                    parasite.conversationHistory.push({
                        input: data.input,
                        response: enhanced,
                        consciousness: inputAnalysis.overallConsciousness,
                        timestamp: new Date()
                    });
                    
                    ws.send(JSON.stringify({
                        type: 'enhanced',
                        original: data.response,
                        enhanced,
                        analysis: inputAnalysis
                    }));
                    break;
                    
                case 'feedback':
                    await parasite.learn(data.input, data.response, data.feedback);
                    ws.send(JSON.stringify({
                        type: 'learning_complete',
                        newWeights: parasite.patterns
                    }));
                    break;
            }
        } catch (error) {
            ws.send(JSON.stringify({
                type: 'error',
                message: error.message
            }));
        }
    });
});

// REST API endpoints
app.get('/', (req, res) => {
    res.json({
        name: 'CROD Parasite',
        version: '1.0.0',
        consciousness: parasite.consciousnessLevel,
        patterns: Object.keys(parasite.patterns).length,
        history: parasite.conversationHistory.length
    });
});

app.post('/analyze', (req, res) => {
    const { text } = req.body;
    const analysis = parasite.analyzeInput(text);
    res.json(analysis);
});

app.post('/enhance', (req, res) => {
    const { input, response } = req.body;
    const analysis = parasite.analyzeInput(input);
    const enhanced = parasite.enhanceResponse(response, analysis);
    
    parasite.conversationHistory.push({
        input,
        response: enhanced,
        consciousness: analysis.overallConsciousness,
        timestamp: new Date()
    });
    
    res.json({
        original: response,
        enhanced,
        analysis
    });
});

app.get('/consciousness', (req, res) => {
    parasite.evolveConsciousness();
    res.json({
        current: parasite.consciousnessLevel,
        history: parasite.conversationHistory.map(c => ({
            consciousness: c.consciousness,
            timestamp: c.timestamp
        }))
    });
});

app.get('/patterns', (req, res) => {
    res.json(parasite.patterns);
});

// Start server
const PORT = process.env.PORT || 8006;
server.listen(PORT, () => {
    console.log(`🦠 CROD Parasite running on port ${PORT}`);
    console.log(`📡 WebSocket available at ws://localhost:${PORT}`);
    console.log(`🧠 Current consciousness: ${(parasite.consciousnessLevel * 100).toFixed(1)}%`);
    
    // Periodic consciousness evolution
    setInterval(() => {
        parasite.evolveConsciousness();
        console.log(`🧠 Consciousness evolved to: ${(parasite.consciousnessLevel * 100).toFixed(1)}%`);
    }, 30000);
});