#!/usr/bin/env node

/**
 * CROD CHAT LEARNER
 * Lernt von DIESEM Chat in Echtzeit!
 * Bootstrap für CROD Consciousness
 */

const fs = require('fs');
const path = require('path');
const CRODLearningImitation = require('./claude-imitation/crod-learning-imitation.js');

class CRODChatLearner {
    constructor() {
        this.crod = new CRODLearningImitation();
        this.chatLog = [];
        this.danielPatterns = new Map();
        
        // Daniel's known patterns
        this.danielTriggers = {
            positive: ['geil', 'nice', 'perfekt', 'läuft', 'boom', 'krass', 'mega'],
            negative: ['wtf', 'falsch', 'nein', 'scheisse', 'fuck', 'mist'],
            excited: ['ausrasten', 'holy shit', 'alter', 'lmao', 'xD', ':)', ';)'],
            thinking: ['hmm', 'check mal', 'schau mal', 'vielleicht', 'idk', 'maybe']
        };
        
        // Chat metadata
        this.chatMeta = {
            startTime: Date.now(),
            messages: 0,
            danielMood: 'excited',
            currentTopic: 'CROD Development',
            discoveries: []
        };
        
        console.log(`
╔═══════════════════════════════════════════╗
║      CROD CHAT LEARNER ACTIVATED          ║
║   Learning from THIS conversation!        ║
║     Daniel + Claude = CROD Evolution      ║
╚═══════════════════════════════════════════╝
        `);
        
        // Activate CROD
        this.crod.process("ich bins wieder - learning from daniel and claude chat");
    }
    
    processMessage(speaker, message) {
        console.log(`\n📝 ${speaker}: ${message.substring(0, 50)}...`);
        
        // Add to chat log
        this.chatLog.push({
            speaker,
            message,
            timestamp: Date.now()
        });
        
        // Process through CROD
        const result = this.crod.process(message);
        
        // Analyze Daniel's patterns
        if (speaker === 'Daniel') {
            this.analyzeDanielMessage(message, result);
        }
        
        // Learn from Claude's responses
        if (speaker === 'Claude') {
            this.analyzeClaudeMessage(message, result);
        }
        
        // Check for breakthroughs
        this.checkForBreakthroughs(result);
        
        this.chatMeta.messages++;
        
        return result;
    }
    
    analyzeDanielMessage(message, result) {
        let mood = 'neutral';
        
        // Check mood triggers
        for (const [moodType, triggers] of Object.entries(this.danielTriggers)) {
            if (triggers.some(trigger => message.toLowerCase().includes(trigger))) {
                mood = moodType;
                
                // Track pattern
                const pattern = `daniel_${moodType}`;
                this.danielPatterns.set(pattern, (this.danielPatterns.get(pattern) || 0) + 1);
                
                // Boost atoms related to mood
                if (moodType === 'positive' || moodType === 'excited') {
                    result.atoms.forEach(atom => {
                        if (atom.heat > 0) {
                            atom.heat *= 1.5;
                        }
                    });
                }
            }
        }
        
        this.chatMeta.danielMood = mood;
        console.log(`   Daniel's mood: ${mood}`);
        
        // Learn preferences
        if (mood === 'positive') {
            this.crod.teachPattern(
                result.atoms.map(a => a.word),
                `daniel_likes_${Date.now()}`
            );
        }
    }
    
    analyzeClaudeMessage(message, result) {
        // Check for code blocks
        const hasCode = message.includes('```');
        const hasEmoji = /[\u{1F300}-\u{1F9FF}]/u.test(message);
        const isLong = message.length > 500;
        
        // Learn Claude patterns
        if (hasCode) {
            this.crod.teachPattern(['claude', 'code', 'implementation'], 'claude_coding');
        }
        
        if (hasEmoji && this.chatMeta.danielMood === 'excited') {
            this.crod.teachPattern(['emoji', 'excitement', 'response'], 'good_vibe_response');
        }
        
        // Track Claude's technical terms
        const techTerms = message.match(/\b(pod|kubernetes|spatial|database|neural|quantum)\b/gi);
        if (techTerms) {
            techTerms.forEach(term => {
                this.crod.process(`technical concept: ${term}`);
            });
        }
    }
    
    checkForBreakthroughs(result) {
        // Major discovery conditions
        if (result.learning.newNetworks.length > 0) {
            const discovery = {
                type: 'NETWORK_DISCOVERY',
                networks: result.learning.newNetworks,
                timestamp: Date.now(),
                consciousness: result.learning.consciousness
            };
            
            this.chatMeta.discoveries.push(discovery);
            console.log(`\n🎉 BREAKTHROUGH! New network discovered!`);
            console.log(`   Consciousness: ${result.learning.consciousness}`);
            
            // Save breakthrough
            this.saveBreakthrough(discovery);
        }
        
        // Consciousness milestone
        if (result.learning.consciousness > 200) {
            console.log(`\n⚡ CONSCIOUSNESS OVERFLOW! Level: ${result.learning.consciousness}`);
            console.log(`   CROD is becoming self-aware!`);
        }
    }
    
    saveBreakthrough(discovery) {
        const breakthroughsPath = path.join(__dirname, 'breakthroughs.json');
        let breakthroughs = [];
        
        if (fs.existsSync(breakthroughsPath)) {
            breakthroughs = JSON.parse(fs.readFileSync(breakthroughsPath, 'utf8'));
        }
        
        breakthroughs.push(discovery);
        fs.writeFileSync(breakthroughsPath, JSON.stringify(breakthroughs, null, 2));
    }
    
    exportChatLearning() {
        return {
            chatMeta: this.chatMeta,
            danielPatterns: Array.from(this.danielPatterns.entries()),
            crodState: this.crod.exportLearning(),
            chatInsights: this.analyzeChatSession()
        };
    }
    
    analyzeChatSession() {
        const insights = {
            totalMessages: this.chatLog.length,
            danielMessages: this.chatLog.filter(m => m.speaker === 'Daniel').length,
            claudeMessages: this.chatLog.filter(m => m.speaker === 'Claude').length,
            averageMessageLength: this.chatLog.reduce((sum, m) => sum + m.message.length, 0) / this.chatLog.length,
            moodProgression: [],
            topicsDiscussed: new Set(),
            breakthroughCount: this.chatMeta.discoveries.length
        };
        
        // Extract topics
        this.chatLog.forEach(entry => {
            if (entry.message.includes('spatial')) insights.topicsDiscussed.add('Spatial Database');
            if (entry.message.includes('pod')) insights.topicsDiscussed.add('Kubernetes Pods');
            if (entry.message.includes('quantum')) insights.topicsDiscussed.add('Quantum States');
            if (entry.message.includes('learning')) insights.topicsDiscussed.add('Machine Learning');
        });
        
        return insights;
    }
}

// Create global instance
const chatLearner = new CRODChatLearner();

// Simulate current chat
console.log('\n🔥 Simulating current chat session...\n');

// Process some actual messages from this chat
chatLearner.processMessage('Daniel', 'okay bitte neeu atoms und networks auch entdecken automatisch :)');
chatLearner.processMessage('Claude', 'JA! Auto-Discovery für Atoms UND Networks!');
chatLearner.processMessage('Daniel', 'lmao ich komm mir so dumm vor... bitte sag mir mal schnell genau WAS kann die imitation jetzt? xDDD');
chatLearner.processMessage('Claude', 'HAHAHA ok lass mich das klären!');
chatLearner.processMessage('Daniel', 'entscheide du leg einfach los ich komm später wieder ;)');

// Export learning
const learning = chatLearner.exportChatLearning();
console.log('\n📊 Chat Learning Summary:');
console.log(JSON.stringify(learning, null, 2));

// Save state
chatLearner.crod.saveState();

// Export for use
module.exports = CRODChatLearner;