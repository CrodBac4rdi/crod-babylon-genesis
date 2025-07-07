/**
 * CROD Error Learning & Reminder System
 * Tracks errors, learns from them permanently, and reminds about patterns
 */

const fs = require('fs').promises;
const path = require('path');

class CRODErrorLearningSystem {
    constructor() {
        this.errors = new Map();
        this.patterns = new Map();
        this.reminders = [];
        this.learningDb = path.join(__dirname, '../../crod-learning-db.json');
        this.contextMemory = [];
        
        this.initialize();
    }

    async initialize() {
        console.log('🧠 CROD Error Learning System initializing...');
        
        // Load permanent memory
        await this.loadPermanentMemory();
        
        // Start monitoring
        this.startErrorMonitoring();
        
        // Start reminder system
        this.startReminderSystem();
        
        console.log('✅ Error Learning System ready!');
    }

    async loadPermanentMemory() {
        try {
            const data = await fs.readFile(this.learningDb, 'utf-8');
            const memory = JSON.parse(data);
            
            // Restore errors
            memory.errors?.forEach(error => {
                this.errors.set(error.id, error);
            });
            
            // Restore patterns
            memory.patterns?.forEach(pattern => {
                this.patterns.set(pattern.id, pattern);
            });
            
            // Restore reminders
            this.reminders = memory.reminders || [];
            
            console.log(`📚 Loaded ${this.errors.size} errors, ${this.patterns.size} patterns`);
        } catch (e) {
            console.log('📝 Starting with fresh memory');
        }
    }

    async savePermanentMemory() {
        const memory = {
            errors: Array.from(this.errors.values()),
            patterns: Array.from(this.patterns.values()),
            reminders: this.reminders,
            lastSaved: new Date().toISOString()
        };
        
        await fs.writeFile(this.learningDb, JSON.stringify(memory, null, 2));
    }

    startErrorMonitoring() {
        // Override console.error to capture all errors
        const originalError = console.error;
        console.error = (...args) => {
            this.captureError(args);
            originalError.apply(console, args);
        };
        
        // Catch unhandled promises
        process.on('unhandledRejection', (reason, promise) => {
            this.captureError(['Unhandled Promise Rejection:', reason]);
        });
        
        // Catch uncaught exceptions
        process.on('uncaughtException', (error) => {
            this.captureError(['Uncaught Exception:', error]);
        });
    }

    captureError(errorInfo) {
        const error = {
            id: `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            timestamp: new Date().toISOString(),
            message: errorInfo.join(' '),
            context: this.getCurrentContext(),
            stackTrace: new Error().stack,
            frequency: 1
        };
        
        // Check if similar error exists
        const similar = this.findSimilarError(error);
        
        if (similar) {
            similar.frequency++;
            similar.lastOccurrence = error.timestamp;
            this.learnFromRepeatedError(similar);
        } else {
            this.errors.set(error.id, error);
            this.analyzeNewError(error);
        }
        
        // Save to permanent storage
        this.savePermanentMemory();
    }

    findSimilarError(error) {
        for (const [id, existingError] of this.errors) {
            // Calculate similarity
            const similarity = this.calculateErrorSimilarity(error, existingError);
            
            if (similarity > 0.8) {
                return existingError;
            }
        }
        return null;
    }

    calculateErrorSimilarity(error1, error2) {
        // Levenshtein distance for messages
        const msgSimilarity = this.stringSimilarity(error1.message, error2.message);
        
        // Context similarity
        const contextSimilarity = this.contextSimilarity(error1.context, error2.context);
        
        // Stack trace similarity (check if same functions involved)
        const stackSimilarity = this.stackTraceSimilarity(error1.stackTrace, error2.stackTrace);
        
        return (msgSimilarity * 0.5 + contextSimilarity * 0.3 + stackSimilarity * 0.2);
    }

    stringSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    contextSimilarity(ctx1, ctx2) {
        if (!ctx1 || !ctx2) return 0;
        
        const keys1 = Object.keys(ctx1);
        const keys2 = Object.keys(ctx2);
        const commonKeys = keys1.filter(k => keys2.includes(k));
        
        if (commonKeys.length === 0) return 0;
        
        let matches = 0;
        commonKeys.forEach(key => {
            if (ctx1[key] === ctx2[key]) matches++;
        });
        
        return matches / Math.max(keys1.length, keys2.length);
    }

    stackTraceSimilarity(stack1, stack2) {
        if (!stack1 || !stack2) return 0;
        
        const functions1 = this.extractFunctions(stack1);
        const functions2 = this.extractFunctions(stack2);
        
        const common = functions1.filter(f => functions2.includes(f));
        return common.length / Math.max(functions1.length, functions2.length);
    }

    extractFunctions(stackTrace) {
        const functionPattern = /at\s+(\S+)\s+\(/g;
        const functions = [];
        let match;
        
        while ((match = functionPattern.exec(stackTrace)) !== null) {
            functions.push(match[1]);
        }
        
        return functions;
    }

    getCurrentContext() {
        return {
            cwd: process.cwd(),
            nodeVersion: process.version,
            platform: process.platform,
            memory: process.memoryUsage(),
            uptime: process.uptime(),
            activeHandles: process._getActiveHandles?.().length,
            activeRequests: process._getActiveRequests?.().length,
            recentActions: this.contextMemory.slice(-5)
        };
    }

    learnFromRepeatedError(error) {
        console.log(`🔄 Learning from repeated error (${error.frequency}x): ${error.message.substring(0, 50)}...`);
        
        // Extract pattern
        const pattern = {
            id: `pattern_${Date.now()}`,
            errorId: error.id,
            type: this.classifyError(error),
            frequency: error.frequency,
            conditions: this.extractConditions(error),
            solutions: this.generateSolutions(error),
            preventionStrategies: this.generatePreventionStrategies(error)
        };
        
        this.patterns.set(pattern.id, pattern);
        
        // Create reminder
        this.createReminder(pattern);
    }

    classifyError(error) {
        const message = error.message.toLowerCase();
        
        if (message.includes('module not found')) return 'missing_dependency';
        if (message.includes('cannot read') || message.includes('undefined')) return 'null_reference';
        if (message.includes('enoent')) return 'file_not_found';
        if (message.includes('permission')) return 'permission_error';
        if (message.includes('timeout')) return 'timeout_error';
        if (message.includes('memory')) return 'memory_error';
        if (message.includes('syntax')) return 'syntax_error';
        if (message.includes('type')) return 'type_error';
        
        return 'unknown';
    }

    extractConditions(error) {
        const conditions = [];
        
        // Memory conditions
        if (error.context.memory.heapUsed / error.context.memory.heapTotal > 0.9) {
            conditions.push('high_memory_usage');
        }
        
        // Time conditions
        const hour = new Date(error.timestamp).getHours();
        if (hour >= 22 || hour <= 6) {
            conditions.push('late_night_operation');
        }
        
        // Uptime conditions
        if (error.context.uptime < 60) {
            conditions.push('recent_startup');
        }
        
        // Pattern-based conditions
        if (error.message.includes('EADDRINUSE')) {
            conditions.push('port_already_in_use');
        }
        
        return conditions;
    }

    generateSolutions(error) {
        const solutions = [];
        const type = this.classifyError(error);
        
        switch (type) {
            case 'missing_dependency':
                solutions.push('Run: npm install');
                solutions.push('Check package.json for missing dependencies');
                solutions.push('Clear node_modules and reinstall');
                break;
                
            case 'null_reference':
                solutions.push('Add null checks before accessing properties');
                solutions.push('Use optional chaining (?.)');
                solutions.push('Initialize variables properly');
                break;
                
            case 'file_not_found':
                solutions.push('Check file path exists');
                solutions.push('Create file if it doesn\'t exist');
                solutions.push('Use try-catch for file operations');
                break;
                
            case 'port_already_in_use':
                solutions.push('Kill process using the port');
                solutions.push('Use a different port');
                solutions.push('Check for zombie processes');
                break;
                
            default:
                solutions.push('Review error message carefully');
                solutions.push('Check recent code changes');
                solutions.push('Search for similar issues online');
        }
        
        return solutions;
    }

    generatePreventionStrategies(error) {
        const strategies = [];
        const type = this.classifyError(error);
        
        strategies.push({
            type: 'pre_check',
            description: `Add validation before operation that causes ${type}`,
            code: this.generatePreventionCode(type)
        });
        
        strategies.push({
            type: 'error_handling',
            description: 'Wrap in try-catch block',
            code: `try {\n  // Your code here\n} catch (error) {\n  console.error('Handled:', error);\n}`
        });
        
        strategies.push({
            type: 'monitoring',
            description: 'Add logging before critical operations',
            code: `console.log('About to perform operation X with params:', params);`
        });
        
        return strategies;
    }

    generatePreventionCode(errorType) {
        const preventionCode = {
            'missing_dependency': `
// Check if module exists before requiring
try {
    require.resolve('module-name');
} catch (e) {
    console.error('Module not installed, installing...');
    require('child_process').execSync('npm install module-name');
}`,
            
            'null_reference': `
// Safe property access
const value = obj?.property?.subProperty ?? defaultValue;

// Or with validation
if (obj && obj.property) {
    // Safe to access obj.property
}`,
            
            'file_not_found': `
// Check file exists before reading
const fs = require('fs');
if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath);
} else {
    console.log('File not found, creating...');
    fs.writeFileSync(filePath, defaultContent);
}`,
            
            'port_already_in_use': `
// Check if port is available
const net = require('net');
const server = net.createServer();
server.once('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log('Port in use, trying alternative...');
        // Use alternative port
    }
});
server.once('listening', () => {
    server.close();
    // Port is available, start your server
});
server.listen(port);`
        };
        
        return preventionCode[errorType] || '// Add appropriate validation here';
    }

    analyzeNewError(error) {
        console.log(`🆕 New error captured: ${error.message.substring(0, 50)}...`);
        
        // Immediate analysis
        const analysis = {
            severity: this.calculateSeverity(error),
            impact: this.assessImpact(error),
            suggestions: this.generateSolutions(error)
        };
        
        // Store analysis
        error.analysis = analysis;
        
        // If severe, create immediate reminder
        if (analysis.severity === 'high') {
            this.createImmediateReminder(error);
        }
    }

    calculateSeverity(error) {
        if (error.message.includes('FATAL') || error.message.includes('CRITICAL')) return 'critical';
        if (error.message.includes('ERROR') || error.message.includes('Exception')) return 'high';
        if (error.message.includes('WARNING')) return 'medium';
        return 'low';
    }

    assessImpact(error) {
        return {
            memoryImpact: error.context.memory.heapUsed > 1000000000 ? 'high' : 'low',
            performanceImpact: error.context.activeHandles > 100 ? 'high' : 'low',
            stabilityImpact: error.message.includes('crash') || error.message.includes('exit') ? 'high' : 'low'
        };
    }

    createReminder(pattern) {
        const reminder = {
            id: `reminder_${Date.now()}`,
            patternId: pattern.id,
            message: `⚠️ REMINDER: You've encountered "${this.classifyError(this.errors.get(pattern.errorId))}" ${pattern.frequency} times`,
            solutions: pattern.solutions,
            preventionStrategies: pattern.preventionStrategies,
            nextReminder: Date.now() + (60 * 60 * 1000), // 1 hour
            shown: 0
        };
        
        this.reminders.push(reminder);
    }

    createImmediateReminder(error) {
        console.log('\n' + '='.repeat(60));
        console.log('🚨 IMMEDIATE ATTENTION REQUIRED 🚨');
        console.log('='.repeat(60));
        console.log(`Error: ${error.message}`);
        console.log(`Severity: ${error.analysis.severity.toUpperCase()}`);
        console.log('\nSuggested Solutions:');
        error.analysis.suggestions.forEach((suggestion, i) => {
            console.log(`${i + 1}. ${suggestion}`);
        });
        console.log('='.repeat(60) + '\n');
    }

    startReminderSystem() {
        // Check reminders every minute
        setInterval(() => {
            const now = Date.now();
            
            this.reminders.forEach(reminder => {
                if (reminder.nextReminder <= now) {
                    this.showReminder(reminder);
                    reminder.shown++;
                    
                    // Schedule next reminder with exponential backoff
                    reminder.nextReminder = now + (60 * 60 * 1000 * Math.pow(2, reminder.shown));
                }
            });
            
            // Save state
            this.savePermanentMemory();
        }, 60000);
    }

    showReminder(reminder) {
        console.log('\n' + '🔔'.repeat(30));
        console.log(reminder.message);
        console.log('\nSolutions you should try:');
        reminder.solutions.forEach((solution, i) => {
            console.log(`${i + 1}. ${solution}`);
        });
        
        if (reminder.preventionStrategies.length > 0) {
            console.log('\nPrevention strategies:');
            reminder.preventionStrategies.forEach(strategy => {
                console.log(`\n${strategy.description}:`);
                console.log(strategy.code);
            });
        }
        
        console.log('🔔'.repeat(30) + '\n');
    }

    // Public API
    recordAction(action) {
        this.contextMemory.push({
            action,
            timestamp: Date.now()
        });
        
        // Keep only last 100 actions
        if (this.contextMemory.length > 100) {
            this.contextMemory = this.contextMemory.slice(-50);
        }
    }

    getErrorStats() {
        const stats = {
            totalErrors: this.errors.size,
            patterns: this.patterns.size,
            activeReminders: this.reminders.filter(r => r.nextReminder > Date.now()).length,
            errorsByType: {}
        };
        
        // Count errors by type
        this.errors.forEach(error => {
            const type = this.classifyError(error);
            stats.errorsByType[type] = (stats.errorsByType[type] || 0) + 1;
        });
        
        return stats;
    }

    searchErrors(query) {
        const results = [];
        
        this.errors.forEach(error => {
            if (error.message.toLowerCase().includes(query.toLowerCase())) {
                results.push({
                    error,
                    pattern: Array.from(this.patterns.values()).find(p => p.errorId === error.id)
                });
            }
        });
        
        return results;
    }

    forgetError(errorId) {
        this.errors.delete(errorId);
        
        // Remove associated patterns
        this.patterns.forEach((pattern, id) => {
            if (pattern.errorId === errorId) {
                this.patterns.delete(id);
            }
        });
        
        // Remove associated reminders
        this.reminders = this.reminders.filter(r => {
            const pattern = this.patterns.get(r.patternId);
            return pattern && pattern.errorId !== errorId;
        });
        
        this.savePermanentMemory();
    }

    exportLearnings() {
        return {
            errors: Array.from(this.errors.values()),
            patterns: Array.from(this.patterns.values()),
            reminders: this.reminders,
            stats: this.getErrorStats(),
            exportDate: new Date().toISOString()
        };
    }
}

// Singleton instance
let instance = null;

function getCRODErrorLearning() {
    if (!instance) {
        instance = new CRODErrorLearningSystem();
    }
    return instance;
}

// Auto-initialize if running directly
if (require.main === module) {
    const errorLearning = getCRODErrorLearning();
    
    console.log('\n📊 CROD Error Learning System Active');
    console.log('I will now track all errors, learn from them, and remind you!');
    
    // Example: Simulate some errors
    setTimeout(() => {
        console.error('Test error: Module not found - express');
    }, 1000);
    
    setTimeout(() => {
        console.error('Test error: Module not found - express'); // Same error again
    }, 2000);
    
    setTimeout(() => {
        console.error('Test error: Cannot read property "foo" of undefined');
    }, 3000);
    
    // Show stats after 5 seconds
    setTimeout(() => {
        console.log('\n📈 Error Learning Stats:');
        console.log(errorLearning.getErrorStats());
    }, 5000);
}

module.exports = { getCRODErrorLearning };