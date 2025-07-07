/**
 * CROD Claude Integration
 * Tracks Claude's errors and helps it learn from mistakes
 */

const { getCRODErrorLearning } = require('./crod-error-learning-system');

class CRODClaudeIntegration {
    constructor() {
        this.errorLearning = getCRODErrorLearning();
        this.claudePatterns = new Map();
        this.claudeContext = {
            currentTask: null,
            recentCommands: [],
            fileOperations: [],
            commonMistakes: []
        };
        
        this.initialize();
    }

    initialize() {
        console.log('🤖 CROD-Claude Integration Active');
        
        // Track specific Claude patterns
        this.trackClaudePatterns();
        
        // Load Claude-specific learnings
        this.loadClaudeLearnings();
        
        // Start proactive reminders
        this.startProactiveReminders();
    }

    trackClaudePatterns() {
        // Common Claude mistakes patterns
        this.claudePatterns.set('file_not_read', {
            pattern: /File has not been read yet/,
            frequency: 0,
            solution: 'Always use Read tool before Edit/Write',
            prevention: `// Always read first
await Read({ file_path: '/path/to/file' });
// Then edit
await Edit({ file_path: '/path/to/file', ... });`
        });
        
        this.claudePatterns.set('module_not_found', {
            pattern: /Cannot find module|MODULE_NOT_FOUND/,
            frequency: 0,
            solution: 'Check if module is installed with npm install',
            prevention: `// Check package.json or install
await Bash({ command: 'npm install missing-module' });`
        });
        
        this.claudePatterns.set('port_in_use', {
            pattern: /EADDRINUSE|address already in use/,
            frequency: 0,
            solution: 'Kill process or use different port',
            prevention: `// Check port before starting
await Bash({ command: 'lsof -i :PORT' });
// Or use dynamic port
const PORT = process.env.PORT || 3000;`
        });
        
        this.claudePatterns.set('permission_denied', {
            pattern: /Permission denied|EACCES/,
            frequency: 0,
            solution: 'Check file permissions or run with proper rights',
            prevention: `// Make executable
await Bash({ command: 'chmod +x script.sh' });`
        });
    }

    loadClaudeLearnings() {
        // Load Claude-specific error history
        const stats = this.errorLearning.getErrorStats();
        
        // Identify most common Claude mistakes
        Object.entries(stats.errorsByType).forEach(([type, count]) => {
            if (count > 2) {
                this.claudeContext.commonMistakes.push({
                    type,
                    count,
                    lastSeen: Date.now()
                });
            }
        });
    }

    startProactiveReminders() {
        // Proactive reminders based on context
        setInterval(() => {
            this.checkContextAndRemind();
        }, 30000); // Every 30 seconds
    }

    checkContextAndRemind() {
        const currentContext = this.getCurrentContext();
        
        // Remind about reading files before editing
        if (currentContext.includes('edit') || currentContext.includes('write')) {
            const hasRecentRead = this.claudeContext.fileOperations.some(op => 
                op.type === 'read' && Date.now() - op.timestamp < 60000
            );
            
            if (!hasRecentRead) {
                this.proactiveReminder('file_operations', 
                    '💡 Remember to Read files before Edit/Write operations!'
                );
            }
        }
        
        // Remind about checking ports
        if (currentContext.includes('server') || currentContext.includes('listen')) {
            this.proactiveReminder('port_check',
                '💡 Check if port is available before starting servers!'
            );
        }
        
        // Remind about error patterns
        this.claudePatterns.forEach((pattern, key) => {
            if (pattern.frequency > 3) {
                this.proactiveReminder(key,
                    `⚠️ You've hit "${key}" ${pattern.frequency} times. ${pattern.solution}`
                );
            }
        });
    }

    getCurrentContext() {
        // Get current context from recent commands
        return this.claudeContext.recentCommands.join(' ').toLowerCase();
    }

    proactiveReminder(type, message) {
        const lastReminder = this.lastReminders?.[type];
        const now = Date.now();
        
        // Don't spam - remind max once per hour per type
        if (!lastReminder || now - lastReminder > 3600000) {
            console.log('\n' + '💭'.repeat(20));
            console.log('CROD PROACTIVE REMINDER:');
            console.log(message);
            
            const pattern = this.claudePatterns.get(type);
            if (pattern && pattern.prevention) {
                console.log('\nPrevention code:');
                console.log(pattern.prevention);
            }
            
            console.log('💭'.repeat(20) + '\n');
            
            this.lastReminders = this.lastReminders || {};
            this.lastReminders[type] = now;
        }
    }

    // Track Claude's actions
    trackAction(action) {
        this.claudeContext.recentCommands.push(action);
        
        // Keep last 50 commands
        if (this.claudeContext.recentCommands.length > 50) {
            this.claudeContext.recentCommands.shift();
        }
        
        // Track file operations
        if (action.includes('Read') || action.includes('Write') || action.includes('Edit')) {
            this.claudeContext.fileOperations.push({
                type: action.includes('Read') ? 'read' : 'write',
                timestamp: Date.now(),
                action
            });
        }
        
        // Record in error learning system
        this.errorLearning.recordAction(action);
    }

    // Analyze Claude's error
    analyzeClaudeError(error) {
        // Check against known patterns
        this.claudePatterns.forEach((pattern, key) => {
            if (pattern.pattern.test(error)) {
                pattern.frequency++;
                
                console.log('\n🎯 CROD detected a familiar pattern!');
                console.log(`Pattern: ${key} (${pattern.frequency}x)`);
                console.log(`Solution: ${pattern.solution}`);
                
                if (pattern.prevention) {
                    console.log('\nHere\'s how to prevent it:');
                    console.log(pattern.prevention);
                }
            }
        });
    }

    // Get Claude-specific insights
    getClaudeInsights() {
        const insights = {
            commonMistakes: this.claudeContext.commonMistakes,
            patterns: Array.from(this.claudePatterns.entries()).map(([key, value]) => ({
                type: key,
                frequency: value.frequency,
                solution: value.solution
            })),
            recentActions: this.claudeContext.recentCommands.slice(-10),
            recommendations: this.generateRecommendations()
        };
        
        return insights;
    }

    generateRecommendations() {
        const recommendations = [];
        
        // Based on error patterns
        this.claudePatterns.forEach((pattern, key) => {
            if (pattern.frequency > 2) {
                recommendations.push({
                    priority: 'high',
                    type: key,
                    recommendation: `Consider implementing automatic ${key} prevention`,
                    code: pattern.prevention
                });
            }
        });
        
        // Based on common mistakes
        const fileErrors = this.claudeContext.commonMistakes.filter(m => 
            m.type === 'file_not_found' || m.type === 'null_reference'
        );
        
        if (fileErrors.length > 0) {
            recommendations.push({
                priority: 'medium',
                type: 'file_handling',
                recommendation: 'Add file existence checks before operations',
                code: `// Always check file exists
if (await fileExists(path)) {
    // Safe to proceed
}`
            });
        }
        
        return recommendations;
    }

    // Export Claude-specific learnings
    exportClaudeLearnings() {
        return {
            patterns: Array.from(this.claudePatterns.entries()),
            context: this.claudeContext,
            insights: this.getClaudeInsights(),
            errorStats: this.errorLearning.getErrorStats(),
            exportDate: new Date().toISOString()
        };
    }
}

// Singleton
let claudeIntegration = null;

function getCRODClaudeIntegration() {
    if (!claudeIntegration) {
        claudeIntegration = new CRODClaudeIntegration();
    }
    return claudeIntegration;
}

// Auto-initialize and demonstrate
if (require.main === module) {
    const claude = getCRODClaudeIntegration();
    
    console.log('\n🤖 CROD-Claude Integration Demo\n');
    
    // Simulate Claude actions
    claude.trackAction('Read file /src/index.js');
    claude.trackAction('Edit file /src/index.js');
    
    // Simulate error
    setTimeout(() => {
        console.error('Error: File has not been read yet. Read it first before writing to it.');
        claude.analyzeClaudeError('File has not been read yet. Read it first before writing to it.');
    }, 1000);
    
    // Show insights
    setTimeout(() => {
        console.log('\n📊 Claude Insights:');
        console.log(JSON.stringify(claude.getClaudeInsights(), null, 2));
    }, 2000);
}

module.exports = { getCRODClaudeIntegration };