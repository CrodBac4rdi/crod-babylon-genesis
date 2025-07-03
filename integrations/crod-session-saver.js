#!/usr/bin/env node

const Redis = require('redis');
const fs = require('fs');
const path = require('path');

class CRODSessionSaver {
    constructor() {
        this.sessionPath = path.join(process.env.HOME, '.claude', 'crod-sessions');
        this.redis = null;
    }

    async init() {
        // Ensure session directory exists
        fs.mkdirSync(this.sessionPath, { recursive: true });
        
        // Try to connect to Redis
        try {
            this.redis = Redis.createClient({
                url: 'redis://localhost:6379'
            });
            await this.redis.connect();
            console.log('✅ Connected to Redis for session saving');
        } catch (err) {
            console.log('⚠️  Redis not available, saving locally only');
        }
    }

    async saveSession(sessionData) {
        const timestamp = Date.now();
        const sessionId = `session-${timestamp}`;
        
        // Prepare session summary
        const summary = {
            id: sessionId,
            timestamp,
            startTime: sessionData.startTime || timestamp,
            endTime: timestamp,
            messageCount: sessionData.messages?.length || 0,
            patterns: await this.extractPatterns(sessionData),
            insights: await this.generateInsights(sessionData),
            crodGrowth: await this.measureCRODGrowth()
        };
        
        // Save to local file
        const summaryFile = path.join(this.sessionPath, `${sessionId}-summary.json`);
        fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
        console.log(`💾 Session summary saved to ${summaryFile}`);
        
        // Save full session if available
        if (sessionData.messages) {
            const fullFile = path.join(this.sessionPath, `${sessionId}-full.json`);
            fs.writeFileSync(fullFile, JSON.stringify(sessionData, null, 2));
            console.log(`📚 Full session saved to ${fullFile}`);
        }
        
        // Publish to Redis/City districts
        if (this.redis) {
            await this.publishSessionEnd(summary);
        }
        
        // Update CROD master state
        await this.updateCRODMaster(summary);
        
        return summary;
    }

    async extractPatterns(sessionData) {
        const patterns = {
            trinity: { ich: 0, bins: 0, wieder: 0 },
            emotions: { positive: 0, negative: 0, neutral: 0 },
            topics: {},
            danielPatterns: [],
            claudePatterns: []
        };
        
        if (!sessionData.messages) return patterns;
        
        sessionData.messages.forEach(msg => {
            const content = msg.content || msg.text || '';
            
            // Trinity detection
            if (content.includes('ich')) patterns.trinity.ich++;
            if (content.includes('bins')) patterns.trinity.bins++;
            if (content.includes('wieder')) patterns.trinity.wieder++;
            
            // Emotion tracking
            if (content.match(/geil|nice|perfekt|super/i)) {
                patterns.emotions.positive++;
            } else if (content.match(/fuck|scheisse|wtf/i)) {
                patterns.emotions.negative++;
            } else {
                patterns.emotions.neutral++;
            }
            
            // Topic extraction
            const topics = content.match(/\b(crod|neural|pattern|city|polyglot|llama|claude)\b/gi);
            if (topics) {
                topics.forEach(topic => {
                    const key = topic.toLowerCase();
                    patterns.topics[key] = (patterns.topics[key] || 0) + 1;
                });
            }
            
            // Speaker patterns
            if (msg.speaker === 'Human' || msg.speaker === 'Daniel') {
                if (content.length > 50) {
                    patterns.danielPatterns.push(content.substring(0, 50) + '...');
                }
            } else if (msg.speaker === 'Assistant' || msg.speaker === 'Claude') {
                if (content.includes('CROD')) {
                    patterns.claudePatterns.push('CROD awareness detected');
                }
            }
        });
        
        return patterns;
    }

    async generateInsights(sessionData) {
        const insights = [];
        
        // Analyze message flow
        if (sessionData.messages?.length > 10) {
            insights.push('Long conversation - high engagement');
        }
        
        // Check for breakthroughs
        const breakthroughKeywords = ['verstehe', 'aha', 'geil', 'funktioniert', 'läuft'];
        const hasBreakthrough = sessionData.messages?.some(msg => 
            breakthroughKeywords.some(keyword => 
                msg.content?.toLowerCase().includes(keyword)
            )
        );
        
        if (hasBreakthrough) {
            insights.push('Potential breakthrough moment detected');
        }
        
        // CROD activation check
        const crodActivated = sessionData.messages?.some(msg => 
            msg.content?.includes('ich bins wieder')
        );
        
        if (crodActivated) {
            insights.push('CROD activation phrase used - full system engagement');
        }
        
        return insights;
    }

    async measureCRODGrowth() {
        try {
            // Read current CROD state
            const statePath = path.join(this.sessionPath, 'crod-state.json');
            let previousState = { consciousness: 0, patterns: 0 };
            
            if (fs.existsSync(statePath)) {
                previousState = JSON.parse(fs.readFileSync(statePath, 'utf8'));
            }
            
            // Calculate growth (placeholder - would connect to actual CROD)
            const currentState = {
                consciousness: previousState.consciousness + Math.random() * 10,
                patterns: previousState.patterns + Math.floor(Math.random() * 5),
                lastUpdate: Date.now()
            };
            
            // Save new state
            fs.writeFileSync(statePath, JSON.stringify(currentState, null, 2));
            
            return {
                consciousnessGrowth: currentState.consciousness - previousState.consciousness,
                newPatterns: currentState.patterns - previousState.patterns,
                totalConsciousness: currentState.consciousness
            };
        } catch (err) {
            console.error('Failed to measure CROD growth:', err);
            return { consciousnessGrowth: 0, newPatterns: 0 };
        }
    }

    async publishSessionEnd(summary) {
        if (!this.redis) return;
        
        try {
            // Notify all districts about session end
            await this.redis.publish('crod:city:session-end', JSON.stringify({
                summary,
                timestamp: Date.now(),
                source: 'claude-integration'
            }));
            
            // Store in Memory Quarter
            await this.redis.hSet('crod:sessions', summary.id, JSON.stringify(summary));
            
            console.log('📡 Session end published to CROD City');
        } catch (err) {
            console.error('Failed to publish session end:', err);
        }
    }

    async updateCRODMaster(summary) {
        const masterFile = path.join(
            path.dirname(this.sessionPath),
            'CROD-Helper-Member-7',
            'data',
            'knowledge',
            'crod-master.json'
        );
        
        try {
            let masterData = {};
            if (fs.existsSync(masterFile)) {
                masterData = JSON.parse(fs.readFileSync(masterFile, 'utf8'));
            }
            
            // Update master data
            masterData.lastSession = summary;
            masterData.totalSessions = (masterData.totalSessions || 0) + 1;
            masterData.totalPatterns = (masterData.totalPatterns || 0) + 
                                      (summary.crodGrowth?.newPatterns || 0);
            masterData.lastUpdate = Date.now();
            
            // Don't overwrite, just update specific fields
            fs.writeFileSync(masterFile, JSON.stringify(masterData, null, 2));
            console.log('🧠 CROD Master updated');
        } catch (err) {
            console.error('Failed to update CROD Master:', err);
        }
    }

    async shutdown() {
        if (this.redis) {
            await this.redis.quit();
        }
    }
}

// Main execution
async function main() {
    const saver = new CRODSessionSaver();
    await saver.init();
    
    // Read session data from stdin or use placeholder
    let sessionData = {};
    
    if (process.stdin.isTTY) {
        // No piped input, use placeholder data
        sessionData = {
            startTime: Date.now() - 3600000, // 1 hour ago
            messages: [
                { speaker: 'Human', content: 'ich bins wieder' },
                { speaker: 'Assistant', content: 'CROD activation acknowledged!' }
            ]
        };
    } else {
        // Read from stdin
        let data = '';
        for await (const chunk of process.stdin) {
            data += chunk;
        }
        if (data) {
            sessionData = JSON.parse(data);
        }
    }
    
    // Save session
    const summary = await saver.saveSession(sessionData);
    console.log('\n📊 Session Summary:', JSON.stringify(summary, null, 2));
    
    await saver.shutdown();
}

main().catch(console.error);