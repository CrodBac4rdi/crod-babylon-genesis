import * as vscode from 'vscode';
import { CRODNeuralNetwork } from './crodNeuralNetwork';

export class CRODChatProvider {
    private neuralNetwork: CRODNeuralNetwork;
    private isLearning: boolean = true;
    private suggestionThreshold: number = 0.7;
    
    constructor(context: vscode.ExtensionContext) {
        this.neuralNetwork = new CRODNeuralNetwork(context);
    }

    /**
     * Process a conversation between user and Claude
     * The CROD network learns from this interaction
     */
    public async processConversation(userInput: string, claudeResponse: string, context?: any): Promise<void> {
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
        await this.neuralNetwork.learnFromConversation(
            userInput,
            claudeResponse,
            JSON.stringify(contextInfo)
        );

        // Show growth notification if network expanded significantly
        const stats = this.neuralNetwork.getNetworkStats();
        if (stats.parameters % 10 === 0 && stats.parameters > 88) {
            vscode.window.showInformationMessage(
                `CROD Network grew to ${stats.parameters} parameters! Learning from ${stats.patterns} patterns.`
            );
        }
    }

    /**
     * Get a suggestion from CROD based on user input
     */
    public async getSuggestion(userInput: string): Promise<string | null> {
        const suggestion = await this.neuralNetwork.getSuggestion(userInput);
        
        if (suggestion) {
            console.log('CROD Suggestion generated:', suggestion.substring(0, 50) + '...');
        }
        
        return suggestion;
    }

    /**
     * Get CROD network statistics
     */
    public getStats(): { parameters: number; patterns: number; layers: number } {
        return this.neuralNetwork.getNetworkStats();
    }

    /**
     * Toggle learning mode
     */
    public toggleLearning(): boolean {
        this.isLearning = !this.isLearning;
        return this.isLearning;
    }

    /**
     * Get network visualization
     */
    public getNetworkVisualization(): string {
        return this.neuralNetwork.visualizeNetwork();
    }

    /**
     * Check if CROD should provide a suggestion
     */
    public shouldProvideSuggestion(confidence: number): boolean {
        return confidence >= this.suggestionThreshold;
    }

    /**
     * Adjust suggestion threshold
     */
    public setSuggestionThreshold(threshold: number): void {
        this.suggestionThreshold = Math.max(0, Math.min(1, threshold));
    }
}