"use strict";
/**
 * CROD Complete System - A self-growing neural network that learns from Claude conversations
 * Starting with 88 parameters and growing based on learning needs
 */
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
exports.CRODComplete = void 0;
const vscode = __importStar(require("vscode"));
const crodNeuralNetwork_1 = require("./crodNeuralNetwork");
const crodChatProvider_1 = require("./crodChatProvider");
const crodMemory_1 = require("./crodMemory");
class CRODComplete {
    context;
    neuralNetwork;
    chatProvider;
    memoryManager;
    isActive = true;
    growthRate = 0.1;
    learningCycles = 0;
    constructor(context) {
        this.context = context;
        this.neuralNetwork = new crodNeuralNetwork_1.CRODNeuralNetwork(context);
        this.chatProvider = new crodChatProvider_1.CRODChatProvider(context);
        this.memoryManager = new crodMemory_1.CRODMemoryManager(context);
        this.initialize();
    }
    initialize() {
        // Show initialization message
        vscode.window.showInformationMessage('CROD Neural Network initialized with 88 parameters. Ready to learn from Claude conversations!');
        // Set up periodic memory consolidation
        setInterval(() => {
            if (this.isActive) {
                this.consolidateMemory();
            }
        }, 300000); // Every 5 minutes
    }
    /**
     * Process a conversation between user and Claude
     */
    async processConversation(userInput, claudeResponse, context) {
        if (!this.isActive)
            return;
        this.learningCycles++;
        // Add to memory
        this.memoryManager.addPattern(userInput, claudeResponse, JSON.stringify(context));
        // Neural network learning
        await this.chatProvider.processConversation(userInput, claudeResponse, context);
        // Check if we should generate insights
        if (this.learningCycles % 10 === 0) {
            this.generateInsights();
        }
        // Show growth notification periodically
        const stats = this.neuralNetwork.getNetworkStats();
        if (stats.parameters > 88 && stats.parameters % 50 === 0) {
            vscode.window.showInformationMessage(`🧠 CROD has grown to ${stats.parameters} parameters! Learning from ${stats.patterns} patterns.`);
        }
    }
    /**
     * Generate insights from learned patterns
     */
    generateInsights() {
        const memory = this.memoryManager.getMemory();
        const stats = this.memoryManager.getStatistics();
        // Analyze conversation patterns
        if (stats.mostCommonTopics.length > 0) {
            const insight = `Common topics: ${stats.mostCommonTopics.slice(0, 5).join(', ')}`;
            this.memoryManager.addInsight('topics', insight, 0.8);
        }
        // Analyze response patterns
        if (stats.averageResponseLength > 0) {
            const insight = `Average Claude response length: ${stats.averageResponseLength} characters`;
            this.memoryManager.addInsight('patterns', insight, 0.9);
        }
        console.log('CROD insights generated');
    }
    /**
     * Consolidate and optimize memory
     */
    consolidateMemory() {
        const stats = this.neuralNetwork.getNetworkStats();
        console.log(`CROD Memory consolidation: ${stats.parameters} parameters, ${stats.patterns} patterns`);
        // Save current state
        this.memoryManager.saveMemory();
        // Generate summary insight
        const insight = `Consolidated ${stats.patterns} patterns with ${stats.parameters} parameters`;
        this.memoryManager.addInsight('consolidation', insight, 1.0);
    }
    /**
     * Get a suggestion based on user input
     */
    async getSuggestion(input) {
        return await this.chatProvider.getSuggestion(input);
    }
    /**
     * Get complete system status
     */
    getSystemStatus() {
        const networkStats = this.neuralNetwork.getNetworkStats();
        const memoryStats = this.memoryManager.getStatistics();
        const recentInsights = this.memoryManager.getInsights().slice(-5);
        return {
            neuralNetwork: networkStats,
            memory: memoryStats,
            insights: recentInsights,
            isActive: this.isActive,
            learningCycles: this.learningCycles
        };
    }
    /**
     * Toggle system active state
     */
    toggleActive() {
        this.isActive = !this.isActive;
        const status = this.isActive ? 'activated' : 'deactivated';
        vscode.window.showInformationMessage(`CROD Neural Network ${status}`);
        return this.isActive;
    }
    /**
     * Export CROD knowledge
     */
    exportKnowledge() {
        const status = this.getSystemStatus();
        const networkViz = this.neuralNetwork.visualizeNetwork();
        return JSON.stringify({
            timestamp: new Date().toISOString(),
            status: status,
            visualization: networkViz,
            version: '1.0.0'
        }, null, 2);
    }
    /**
     * Get visualization for UI
     */
    getVisualization() {
        const stats = this.neuralNetwork.getNetworkStats();
        const memStats = this.memoryManager.getStatistics();
        let viz = '🧠 CROD Neural Network Status\n';
        viz += '================================\n\n';
        viz += `Parameters: ${stats.parameters} (started with 88)\n`;
        viz += `Growth: +${stats.parameters - 88} parameters\n`;
        viz += `Patterns Learned: ${stats.patterns}\n`;
        viz += `Network Layers: ${stats.layers}\n`;
        viz += `Learning Cycles: ${this.learningCycles}\n\n`;
        viz += '📊 Memory Statistics\n';
        viz += '-------------------\n';
        viz += `Total Conversations: ${memStats.totalConversations}\n`;
        viz += `Average Response Length: ${memStats.averageResponseLength} chars\n`;
        viz += `Common Topics: ${memStats.mostCommonTopics.slice(0, 3).join(', ')}\n\n`;
        viz += '💡 Recent Insights\n';
        viz += '-----------------\n';
        const insights = this.memoryManager.getInsights().slice(-3);
        insights.forEach(insight => {
            viz += `• ${insight.content} (confidence: ${Math.round(insight.confidence * 100)}%)\n`;
        });
        return viz;
    }
}
exports.CRODComplete = CRODComplete;
//# sourceMappingURL=crodComplete.js.map