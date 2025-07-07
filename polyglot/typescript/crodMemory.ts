import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export interface CRODMemory {
    patterns: Array<{
        input: string;
        output: string;
        timestamp: number;
        context?: string;
    }>;
    insights: Array<{
        type: string;
        content: string;
        confidence: number;
        timestamp: number;
    }>;
    statistics: {
        totalConversations: number;
        totalTokensProcessed: number;
        averageResponseLength: number;
        mostCommonTopics: string[];
    };
}

export class CRODMemoryManager {
    private memoryPath: string;
    private memory: CRODMemory;
    
    constructor(context: vscode.ExtensionContext) {
        const storagePath = context.globalStorageUri.fsPath;
        this.memoryPath = path.join(storagePath, 'crod-memory', 'memory.json');
        this.memory = this.loadMemory();
    }

    private loadMemory(): CRODMemory {
        try {
            if (fs.existsSync(this.memoryPath)) {
                const data = fs.readFileSync(this.memoryPath, 'utf8');
                return JSON.parse(data);
            }
        } catch (error) {
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

    public saveMemory(): void {
        try {
            const dir = path.dirname(this.memoryPath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            
            fs.writeFileSync(this.memoryPath, JSON.stringify(this.memory, null, 2));
            console.log('CROD memory saved successfully');
        } catch (error) {
            console.error('Failed to save CROD memory:', error);
        }
    }

    public addPattern(input: string, output: string, context?: string): void {
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

    public addInsight(type: string, content: string, confidence: number): void {
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

    private updateStatistics(): void {
        const stats = this.memory.statistics;
        stats.totalConversations = this.memory.patterns.length;
        
        // Calculate average response length
        if (this.memory.patterns.length > 0) {
            const totalLength = this.memory.patterns.reduce((sum, p) => sum + p.output.length, 0);
            stats.averageResponseLength = Math.round(totalLength / this.memory.patterns.length);
        }

        // Extract common topics (simple keyword extraction)
        const wordFrequency = new Map<string, number>();
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

    public getMemory(): CRODMemory {
        return this.memory;
    }

    public getRecentPatterns(count: number = 10): Array<{ input: string; output: string }> {
        return this.memory.patterns.slice(-count);
    }

    public getInsights(type?: string): Array<{ type: string; content: string; confidence: number }> {
        if (type) {
            return this.memory.insights.filter(i => i.type === type);
        }
        return this.memory.insights;
    }

    public getStatistics() {
        return this.memory.statistics;
    }
}