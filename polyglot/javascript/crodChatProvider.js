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
exports.CRODChatProvider = void 0;
const vscode = __importStar(require("vscode"));
const crodNeuralNetwork_1 = require("./crodNeuralNetwork");
class CRODChatProvider {
    neuralNetwork;
    isLearning = true;
    suggestionThreshold = 0.7;
    constructor(context) {
        this.neuralNetwork = new crodNeuralNetwork_1.CRODNeuralNetwork(context);
    }
    /**
     * Process a conversation between user and Claude
     * The CROD network learns from this interaction
     */
    async processConversation(userInput, claudeResponse, context) {
        if (!this.isLearning) {
            return;
        }
        // Extract context information
        const contextInfo = {
            sessionId: context?.sessionId,
            timestamp: Date.now(),
            model: context?.model || 'unknown',
            tools: context?.tools || []
        };
        // Learn from the conversation
        await this.neuralNetwork.learnFromConversation(userInput, claudeResponse, JSON.stringify(contextInfo));
        // Show growth notification if network expanded significantly
        const stats = this.neuralNetwork.getNetworkStats();
        if (stats.parameters % 10 === 0 && stats.parameters > 88) {
            vscode.window.showInformationMessage(`CROD Network grew to ${stats.parameters} parameters! Learning from ${stats.patterns} patterns.`);
        }
    }
    /**
     * Get a suggestion from CROD based on user input
     */
    async getSuggestion(userInput) {
        const suggestion = await this.neuralNetwork.getSuggestion(userInput);
        if (suggestion) {
            console.log('CROD Suggestion generated:', suggestion.substring(0, 50) + '...');
        }
        return suggestion;
    }
    /**
     * Get CROD network statistics
     */
    getStats() {
        return this.neuralNetwork.getNetworkStats();
    }
    /**
     * Toggle learning mode
     */
    toggleLearning() {
        this.isLearning = !this.isLearning;
        return this.isLearning;
    }
    /**
     * Get network visualization
     */
    getNetworkVisualization() {
        return this.neuralNetwork.visualizeNetwork();
    }
    /**
     * Check if CROD should provide a suggestion
     */
    shouldProvideSuggestion(confidence) {
        return confidence >= this.suggestionThreshold;
    }
    /**
     * Adjust suggestion threshold
     */
    setSuggestionThreshold(threshold) {
        this.suggestionThreshold = Math.max(0, Math.min(1, threshold));
    }
}
exports.CRODChatProvider = CRODChatProvider;
//# sourceMappingURL=crodChatProvider.js.map