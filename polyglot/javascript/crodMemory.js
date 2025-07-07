"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.CRODMemoryManager = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class CRODMemoryManager {
    memoryPath;
    memory;
    constructor(context) {
        const storagePath = context.globalStorageUri.fsPath;
        this.memoryPath = path.join(storagePath, 'crod-memory', 'memory.json');
        this.memory = this.loadMemory();
    }
    loadMemory() {
        try {
            if (fs.existsSync(this.memoryPath)) {
                const data = fs.readFileSync(this.memoryPath, 'utf8');
                return JSON.parse(data);
            }
        }
        catch (error) {
            console.error('Failed to load CROD memory:', error);
        }
        // Return default memory structure
        return {
            patterns: [],
            insights: [],
            statistics: {
                totalConversations: 0,
                totalTokensProcessed: 0,
                averageResponseLength: 0,
                mostCommonTopics: []
            }
        };
    }
    saveMemory() {
        try {
            const dir = path.dirname(this.memoryPath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(this.memoryPath, JSON.stringify(this.memory, null, 2));
            console.log('CROD memory saved successfully');
        }
        catch (error) {
            console.error('Failed to save CROD memory:', error);
        }
    }
    addPattern(input, output, context) {
        this.memory.patterns.push({
            input,
            output,
            timestamp: Date.now(),
            context
        });
        // Keep only recent patterns (last 1000)
        if (this.memory.patterns.length > 1000) {
            this.memory.patterns = this.memory.patterns.slice(-1000);
        }
        this.updateStatistics();
        this.saveMemory();
    }
    addInsight(type, content, confidence) {
        this.memory.insights.push({
            type,
            content,
            confidence,
            timestamp: Date.now()
        });
        // Keep only recent insights (last 100)
        if (this.memory.insights.length > 100) {
            this.memory.insights = this.memory.insights.slice(-100);
        }
        this.saveMemory();
    }
    updateStatistics() {
        const stats = this.memory.statistics;
        stats.totalConversations = this.memory.patterns.length;
        // Calculate average response length
        if (this.memory.patterns.length > 0) {
            const totalLength = this.memory.patterns.reduce((sum, p) => sum + p.output.length, 0);
            stats.averageResponseLength = Math.round(totalLength / this.memory.patterns.length);
        }
        // Extract common topics (simple keyword extraction)
        const wordFrequency = new Map();
        this.memory.patterns.forEach(pattern => {
            const words = pattern.input.toLowerCase().split(/\s+/);
            words.forEach(word => {
                if (word.length > 4) { // Only consider words longer than 4 chars
                    wordFrequency.set(word, (wordFrequency.get(word) || 0) + 1);
                }
            });
        });
        // Get top 10 most common words
        const sortedWords = Array.from(wordFrequency.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([word]) => word);
        stats.mostCommonTopics = sortedWords;
    }
    getMemory() {
        return this.memory;
    }
    getRecentPatterns(count = 10) {
        return this.memory.patterns.slice(-count);
    }
    getInsights(type) {
        if (type) {
            return this.memory.insights.filter(i => i.type === type);
        }
        return this.memory.insights;
    }
    getStatistics() {
        return this.memory.statistics;
    }
}
exports.CRODMemoryManager = CRODMemoryManager;
//# sourceMappingURL=crodMemory.js.map