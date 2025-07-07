/**
 * CROD Complete System - A self-growing neural network that learns from Claude conversations
 * Starting with 88 parameters and growing based on learning needs
 */

import * as vscode from 'vscode';
import { CRODNeuralNetwork } from './crodNeuralNetwork';
import { CRODChatProvider } from './crodChatProvider';
import { CRODMemoryManager } from './crodMemory';

export class CRODComplete {
    private neuralNetwork: CRODNeuralNetwork;
    private chatProvider: CRODChatProvider;
    private memoryManager: CRODMemoryManager;
    private isActive: boolean = true;
    private growthRate: number = 0.1;
    private learningCycles: number = 0;

    constructor(private context: vscode.ExtensionContext) {
        this.neuralNetwork = new CRODNeuralNetwork(context);
        this.chatProvider = new CRODChatProvider(context);
        this.memoryManager = new CRODMemoryManager(context);
        
        this.initialize();
    }

    private initialize(): void {
        // Show initialization message
        vscode.window.showInformationMessage(
            'CROD Neural Network initialized with 88 parameters. Ready to learn from Claude conversations!'
        );

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
    public async processConversation(
        userInput: string, 
        claudeResponse: string, 
        context: any
    ): Promise<void> {
        if (!this.isActive) return;

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
            vscode.window.showInformationMessage(
                `🧠 CROD has grown to ${stats.parameters} parameters! Learning from ${stats.patterns} patterns.`
            );
        }
    }

    /**
     * Generate insights from learned patterns
     */
    private generateInsights(): void {
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
    private consolidateMemory(): void {
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
    public async getSuggestion(input: string): Promise<string | null> {
        return await this.chatProvider.getSuggestion(input);
    }

    /**
     * Get complete system status
     */
    public getSystemStatus(): {
        neuralNetwork: any;
        memory: any;
        insights: any[];
        isActive: boolean;
        learningCycles: number;
    } {
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
    public toggleActive(): boolean {
        this.isActive = !this.isActive;
        const status = this.isActive ? 'activated' : 'deactivated';
        
        vscode.window.showInformationMessage(
            `CROD Neural Network ${status}`
        );

        return this.isActive;
    }

    /**
     * Export CROD knowledge
     */
    public exportKnowledge(): string {
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
    public getVisualization(): string {
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