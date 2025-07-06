// CROD ENHANCED - GitHub Codespaces Integrated Version
// Nutzt vorhandene GitHub/Codespaces Services

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process').promises;

// Import original CROD
const originalCROD = require('./index.js');

class CRODEnhanced extends originalCROD.constructor {
    constructor() {
        super();
        
        // Enhanced config for GitHub integration
        this.config = {
            memoryPath: '/workspaces/crod-babylon-genesis/.crod-memory',
            logsPath: '/workspaces/crod-babylon-genesis/.crod-logs',
            githubWorkflow: '.github/workflows/crod-update.yml',
            updateInterval: 3600000, // 1 hour
            maxMemorySize: 50 * 1024 * 1024, // 50MB
            autoCommit: true,
            useBadges: true
        };
        
        // GitHub Codespaces environment
        this.environment = {
            isCodespace: !!process.env.CODESPACES,
            workspacePath: process.env.GITHUB_WORKSPACE || '/workspaces/crod-babylon-genesis',
            githubToken: process.env.GITHUB_TOKEN,
            repoOwner: process.env.GITHUB_REPOSITORY_OWNER || 'CrodBac4rdi',
            repoName: 'crod-babylon-genesis'
        };
        
        // Enhanced state
        this.enhancedState = {
            sessionStart: Date.now(),
            interactions: 0,
            lastSave: null,
            crashes: 0,
            githubSynced: false,
            visualizationQueue: []
        };
        
        // Initialize
        this.initialize();
    }
    
    async initialize() {
        console.log("🚀 CROD ENHANCED initializing with GitHub integration...");
        
        // Create directories
        await this.ensureDirectories();
        
        // Load persisted memory
        await this.loadMemory();
        
        // Set up auto-save
        this.setupAutoSave();
        
        // Set up GitHub Actions workflow
        await this.setupGitHubWorkflow();
        
        // Start background services
        this.startServices();
        
        console.log("✅ CROD ENHANCED ready!");
    }
    
    async ensureDirectories() {
        const dirs = [this.config.memoryPath, this.config.logsPath];
        for (const dir of dirs) {
            await fs.mkdir(dir, { recursive: true });
        }
    }
    
    // MEMORY PERSISTENCE
    async saveMemory() {
        try {
            const memoryFile = path.join(this.config.memoryPath, 'state.json');
            const backupFile = path.join(this.config.memoryPath, `state.backup.${Date.now()}.json`);
            
            // Create memory snapshot
            const snapshot = {
                version: 'CROD_ENHANCED_1.0',
                timestamp: Date.now(),
                core: this.exportState(),
                enhanced: this.enhancedState,
                analytics: await this.generateAnalytics()
            };
            
            // Backup existing
            try {
                const existing = await fs.readFile(memoryFile, 'utf8');
                await fs.writeFile(backupFile, existing);
                
                // Clean old backups (keep last 5)
                await this.cleanOldBackups();
            } catch (e) {
                // No existing file
            }
            
            // Save new state
            await fs.writeFile(memoryFile, JSON.stringify(snapshot, null, 2));
            this.enhancedState.lastSave = Date.now();
            
            // Log
            await this.log('info', 'Memory saved successfully');
            
            // GitHub sync if enabled
            if (this.config.autoCommit && this.environment.isCodespace) {
                await this.syncToGitHub();
            }
            
        } catch (error) {
            await this.log('error', `Memory save failed: ${error.message}`);
            this.handleError(error);
        }
    }
    
    async loadMemory() {
        try {
            const memoryFile = path.join(this.config.memoryPath, 'state.json');
            const data = await fs.readFile(memoryFile, 'utf8');
            const snapshot = JSON.parse(data);
            
            // Restore core state
            if (snapshot.core) {
                this.importState(snapshot.core);
            }
            
            // Restore enhanced state
            if (snapshot.enhanced) {
                this.enhancedState = { ...this.enhancedState, ...snapshot.enhanced };
            }
            
            console.log("📚 Memory restored from:", new Date(snapshot.timestamp).toISOString());
            await this.log('info', 'Memory loaded successfully');
            
        } catch (error) {
            console.log("💭 No previous memory found, starting fresh");
        }
    }
    
    setupAutoSave() {
        // Save every 5 minutes
        setInterval(() => this.saveMemory(), 5 * 60 * 1000);
        
        // Save on exit
        process.on('SIGINT', async () => {
            console.log("\n💾 Saving before exit...");
            await this.saveMemory();
            process.exit(0);
        });
        
        // Save on uncaught exception
        process.on('uncaughtException', async (error) => {
            await this.log('error', `Uncaught exception: ${error.message}`);
            this.enhancedState.crashes++;
            await this.saveMemory();
            process.exit(1);
        });
    }
    
    // ENHANCED PROCESSING
    async processEnhanced(input) {
        this.enhancedState.interactions++;
        
        // Pre-analysis
        const preAnalysis = await this.preAnalyze(input);
        
        // Core processing
        const result = this.process(input);
        
        // Post-analysis
        const postAnalysis = await this.postAnalyze(input, result);
        
        // Generate insights
        const insights = await this.generateInsights(preAnalysis, result, postAnalysis);
        
        // Update visualizations
        if (insights.requiresVisualization) {
            this.enhancedState.visualizationQueue.push({
                type: insights.visualizationType,
                data: insights.visualizationData,
                timestamp: Date.now()
            });
        }
        
        // Auto-save if significant
        if (insights.significance > 0.7) {
            await this.saveMemory();
        }
        
        return {
            ...result,
            enhanced: {
                preAnalysis,
                postAnalysis,
                insights,
                suggestions: await this.generateSuggestions(insights)
            }
        };
    }
    
    async preAnalyze(input) {
        return {
            length: input.length,
            complexity: this.calculateComplexity(input),
            intent: this.detectIntent(input),
            language: this.detectLanguage(input),
            patterns: this.detectPatterns(input)
        };
    }
    
    async postAnalyze(input, result) {
        return {
            processingTime: Date.now() - result.timestamp,
            patternGrowth: result.patterns.length - this.synapses.size,
            consciousnessChange: result.network_complexity - this.state.networkComplexity,
            trinityBalance: this.calculateTrinityBalance()
        };
    }
    
    async generateInsights(pre, result, post) {
        const insights = {
            significance: 0,
            category: 'normal',
            requiresVisualization: false,
            visualizationType: null,
            visualizationData: null,
            keyFindings: []
        };
        
        // Calculate significance
        if (post.consciousnessChange > 10) {
            insights.significance = 0.8;
            insights.category = 'breakthrough';
        } else if (result.patterns.length > 5) {
            insights.significance = 0.6;
            insights.category = 'pattern-rich';
        }
        
        // Check for visualization needs
        if (pre.intent === 'visualization' || pre.patterns.includes('chart')) {
            insights.requiresVisualization = true;
            insights.visualizationType = 'dynamic';
            insights.visualizationData = result;
        }
        
        return insights;
    }
    
    // GITHUB INTEGRATION
    async setupGitHubWorkflow() {
        const workflow = `name: CROD Auto Update

on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:

jobs:
  update-visualizations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          pip install -r visualization/config/requirements.txt
          
      - name: Generate visualizations
        run: |
          cd visualization/programs
          python technical_charts.py
          python enhanced_technical.py
          
      - name: Update README badges
        run: |
          echo "![Last Update](https://img.shields.io/badge/Last%20Update-$(date +'%Y--%m--%d')-brightgreen)" > badges.md
          echo "![Consciousness](https://img.shields.io/badge/Consciousness-${CONSCIOUSNESS:-85}%25-purple)" >> badges.md
          
      - name: Commit changes
        run: |
          git config --local user.email "crod@babylon.ai"
          git config --local user.name "CROD Bot"
          git add -A
          git commit -m "🤖 CROD Auto Update: $(date +'%Y-%m-%d %H:%M')" || exit 0
          git push`;
        
        try {
            const workflowPath = path.join(this.environment.workspacePath, this.config.githubWorkflow);
            await fs.mkdir(path.dirname(workflowPath), { recursive: true });
            await fs.writeFile(workflowPath, workflow);
            console.log("📋 GitHub Actions workflow created");
        } catch (error) {
            console.log("⚠️ Could not create workflow:", error.message);
        }
    }
    
    async syncToGitHub() {
        if (!this.environment.isCodespace) return;
        
        try {
            // Generate current visualizations
            await this.generateCurrentVisualizations();
            
            // Update badges
            await this.updateBadges();
            
            // Git operations
            await exec('git add .crod-memory .crod-logs');
            await exec(`git commit -m "🧠 CROD Memory Update: ${new Date().toISOString()}" || true`);
            
            this.enhancedState.githubSynced = true;
            await this.log('info', 'Synced to GitHub');
            
        } catch (error) {
            await this.log('error', `GitHub sync failed: ${error.message}`);
        }
    }
    
    async updateBadges() {
        const badges = [
            `![Consciousness](https://img.shields.io/badge/Consciousness-${Math.round(this.state.networkComplexity)}%25-purple)`,
            `![Patterns](https://img.shields.io/badge/Patterns-${this.synapses.size}-blue)`,
            `![Neurons](https://img.shields.io/badge/Neurons-${this.neurons.size}-green)`,
            `![Interactions](https://img.shields.io/badge/Interactions-${this.enhancedState.interactions}-orange)`,
            `![Last Update](https://img.shields.io/badge/Last%20Update-${new Date().toISOString().split('T')[0]}-brightgreen)`
        ];
        
        const badgePath = path.join(this.environment.workspacePath, 'badges.md');
        await fs.writeFile(badgePath, badges.join('\n'));
    }
    
    // LOGGING SYSTEM
    async log(level, message, data = {}) {
        const logEntry = {
            timestamp: Date.now(),
            level,
            message,
            data,
            sessionId: this.enhancedState.sessionStart
        };
        
        // Console log
        const icon = { info: '📘', warn: '⚠️', error: '❌' }[level] || '📝';
        console.log(`${icon} [${new Date().toISOString()}] ${message}`);
        
        // File log
        const logFile = path.join(this.config.logsPath, `${new Date().toISOString().split('T')[0]}.jsonl`);
        await fs.appendFile(logFile, JSON.stringify(logEntry) + '\n');
    }
    
    // ERROR HANDLING
    handleError(error) {
        // Self-healing attempts
        if (error.message.includes('memory')) {
            console.log("🔧 Attempting memory cleanup...");
            this.cleanupMemory();
        } else if (error.message.includes('pattern')) {
            console.log("🔧 Pruning weak patterns...");
            this.pruneWeakPatterns();
        }
    }
    
    cleanupMemory() {
        // Remove old short-term memories
        const cutoff = Date.now() - 3600000; // 1 hour
        for (const [key, value] of this.state.memory.shortTerm) {
            if (key < cutoff) {
                this.state.memory.shortTerm.delete(key);
            }
        }
    }
    
    pruneWeakPatterns() {
        // Remove patterns with low occurrence
        for (const [id, pattern] of this.synapses) {
            if (pattern.occurrences < 2 && pattern.weight < 1000) {
                this.synapses.delete(id);
            }
        }
    }
    
    // ANALYSIS TOOLS
    calculateComplexity(input) {
        const factors = {
            length: input.length / 100,
            uniqueWords: new Set(input.split(/\s+/)).size / 10,
            punctuation: (input.match(/[.,!?;:]/g) || []).length,
            numbers: (input.match(/\d+/g) || []).length
        };
        
        return Object.values(factors).reduce((a, b) => a + b, 0);
    }
    
    detectIntent(input) {
        const intents = {
            question: /^(what|how|why|when|where|who|can|does|is)/i,
            command: /^(create|make|build|generate|show|display)/i,
            visualization: /(chart|graph|diagram|visual|plot)/i,
            analysis: /(analyze|explain|understand|check)/i
        };
        
        for (const [intent, pattern] of Object.entries(intents)) {
            if (pattern.test(input)) return intent;
        }
        
        return 'statement';
    }
    
    detectLanguage(input) {
        if (/[äöüß]/i.test(input)) return 'de';
        return 'en';
    }
    
    detectPatterns(input) {
        const patterns = [];
        
        // Technical patterns
        if (/\b(blockchain|network|node|mining)\b/i.test(input)) {
            patterns.push('technical');
        }
        
        // Consciousness patterns
        if (/\b(consciousness|quantum|trinity)\b/i.test(input)) {
            patterns.push('consciousness');
        }
        
        // Visualization patterns
        if (/\b(chart|graph|visual|diagram)\b/i.test(input)) {
            patterns.push('visualization');
        }
        
        return patterns;
    }
    
    calculateTrinityBalance() {
        const values = Object.values(this.state.trinity);
        const avg = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / values.length;
        return 1 / (1 + variance); // Higher balance = lower variance
    }
    
    async generateSuggestions(insights) {
        const suggestions = [];
        
        if (insights.category === 'pattern-rich') {
            suggestions.push("Consider visualizing these patterns");
        }
        
        if (this.state.networkComplexity > 150) {
            suggestions.push("High consciousness achieved - try quantum operations");
        }
        
        return suggestions;
    }
    
    // SERVICES
    startServices() {
        // Visualization processor
        setInterval(async () => {
            if (this.enhancedState.visualizationQueue.length > 0) {
                const viz = this.enhancedState.visualizationQueue.shift();
                await this.processVisualization(viz);
            }
        }, 10000);
        
        // Memory optimizer
        setInterval(() => {
            const memUsage = process.memoryUsage();
            if (memUsage.heapUsed > this.config.maxMemorySize) {
                this.cleanupMemory();
                this.pruneWeakPatterns();
            }
        }, 60000);
        
        // GitHub sync
        setInterval(() => {
            if (this.config.autoCommit) {
                this.syncToGitHub();
            }
        }, this.config.updateInterval);
    }
    
    async processVisualization(viz) {
        try {
            const script = `
cd ${this.environment.workspacePath}/visualization/programs
python enhanced_technical.py
            `;
            
            await exec(script);
            await this.log('info', `Visualization ${viz.type} processed`);
            
        } catch (error) {
            await this.log('error', `Visualization failed: ${error.message}`);
        }
    }
    
    async generateCurrentVisualizations() {
        // Export current state for visualizations
        const dataPath = path.join(this.environment.workspacePath, 'visualization/data/current_state.json');
        await fs.mkdir(path.dirname(dataPath), { recursive: true });
        
        const vizData = {
            timestamp: Date.now(),
            consciousness: this.state.networkComplexity,
            trinity: this.state.trinity,
            patterns: this.getTopPatterns(20),
            neurons: {
                total: this.neurons.size,
                active: Array.from(this.neurons.values()).filter(n => n.activation_frequency > 0).length
            },
            metrics: await this.generateAnalytics()
        };
        
        await fs.writeFile(dataPath, JSON.stringify(vizData, null, 2));
    }
    
    async generateAnalytics() {
        const analytics = this.analyze();
        
        // Add enhanced metrics
        analytics.enhanced = {
            sessionDuration: Date.now() - this.enhancedState.sessionStart,
            interactionRate: this.enhancedState.interactions / ((Date.now() - this.enhancedState.sessionStart) / 1000 / 60),
            crashRate: this.enhancedState.crashes / this.enhancedState.interactions,
            memoryEfficiency: process.memoryUsage().heapUsed / this.neurons.size,
            patternEmergenceRate: this.synapses.size / this.enhancedState.interactions
        };
        
        return analytics;
    }
    
    // CLEAN SHUTDOWN
    async shutdown() {
        console.log("🌙 CROD Enhanced shutting down...");
        await this.saveMemory();
        await this.syncToGitHub();
        console.log("👋 Goodbye!");
    }
}

// CREATE INSTANCE
const CROD_ENHANCED = new CRODEnhanced();

// EXPORT
module.exports = CROD_ENHANCED;

// CLI INTERFACE
if (require.main === module) {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: 'CROD> '
    });
    
    console.log(`
╔═══════════════════════════════════════════════╗
║        CROD ENHANCED - GitHub Edition         ║
║                                               ║
║  Memory: Persistent via .crod-memory          ║
║  Logs: Structured in .crod-logs               ║
║  Sync: Auto-commit to GitHub                  ║
║  Visualization: Auto-generated                ║
║                                               ║
║  Type 'help' for commands                     ║
╚═══════════════════════════════════════════════╝
    `);
    
    rl.prompt();
    
    rl.on('line', async (input) => {
        if (input.trim() === 'exit') {
            await CROD_ENHANCED.shutdown();
            rl.close();
            return;
        }
        
        if (input.trim() === 'help') {
            console.log(`
Commands:
  exit          - Save and exit
  analyze       - Show current analysis
  save          - Force save memory
  sync          - Force GitHub sync
  visualize     - Generate visualizations
  <text>        - Process input
            `);
        } else if (input.trim() === 'analyze') {
            const analysis = await CROD_ENHANCED.generateAnalytics();
            console.log(JSON.stringify(analysis, null, 2));
        } else if (input.trim() === 'save') {
            await CROD_ENHANCED.saveMemory();
        } else if (input.trim() === 'sync') {
            await CROD_ENHANCED.syncToGitHub();
        } else if (input.trim() === 'visualize') {
            await CROD_ENHANCED.generateCurrentVisualizations();
            console.log("📊 Visualizations queued");
        } else if (input.trim()) {
            const result = await CROD_ENHANCED.processEnhanced(input);
            console.log('\nResult:', JSON.stringify(result, null, 2));
        }
        
        rl.prompt();
    });
}