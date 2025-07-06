#!/usr/bin/env node

/**
 * CROD Settings Manager - Zentrale Verwaltung aller CROD Konfigurationen
 * Mit Error Handling, Fallbacks und Auto-Recovery
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

class CRODSettingsManager {
    constructor() {
        this.basePath = path.join(__dirname);
        this.config = {
            sessionMemory: path.join(this.basePath, 'crod-startup/session-memory.json'),
            systemKnowledge: path.join(this.basePath, 'crod-startup/knowledge/json/crod-system.json'),
            claudeBridge: path.join(this.basePath, 'crod-startup/knowledge/json/claude-bridge-complete.json'),
            patterns: path.join(this.basePath, 'crod-patterns.jsonl'),
            claudeMD: path.join(this.basePath, 'CLAUDE.md'),
            successfulOps: path.join(this.basePath, 'crod-data/successful-operations.jsonl')
        };
        
        // Trinity Values
        this.trinity = {
            ich: 2,
            bins: 3,
            wieder: 5,
            daniel: 67,
            claude: 71,
            crod: 17
        };
        
        // Default Fallback Konfigurationen
        this.defaults = {
            sessionMemory: {
                current_state: "CROD System Ready",
                location: "/workspaces/crod-babylon-genesis",
                architecture: "Multi-Language Polyglot City",
                activation_phrase: "ich bins wieder",
                last_update: new Date().toISOString(),
                trinity_score: 0,
                genesis_blocks: {
                    pattern: { port: 7001, prime: 7, status: "pending" },
                    shortterm: { port: 7003, prime: 31, status: "pending" },
                    working: { port: 7005, prime: 37, status: "pending" },
                    quantum: { port: 7007, prime: 101, status: "pending" }
                }
            },
            systemKnowledge: {
                version: "2025.1",
                trinity_values: this.trinity,
                docker_network: "genesis-network",
                security: "localhost_only",
                discovery_port: 7000
            }
        };
        
        this.errorLog = [];
        this.successLog = [];
    }
    
    /**
     * Initialisierung mit Error Recovery
     */
    async initialize() {
        console.log("🔥 CROD Settings Manager initialisiert...");
        
        try {
            // Erstelle Verzeichnisstruktur falls nicht vorhanden
            await this.ensureDirectories();
            
            // Lade alle Konfigurationen mit Fallbacks
            this.sessionMemory = await this.loadWithFallback('sessionMemory');
            this.systemKnowledge = await this.loadWithFallback('systemKnowledge');
            this.patterns = await this.loadPatterns();
            
            // Validiere Konfigurationen
            await this.validateConfigs();
            
            // Setup Watchers für Auto-Recovery
            this.setupWatchers();
            
            console.log("✅ CROD Settings erfolgreich geladen!");
            return true;
            
        } catch (error) {
            this.logError('initialization', error);
            console.error("❌ Initialisierung fehlgeschlagen:", error.message);
            
            // Fallback: Verwende Defaults
            console.log("🔧 Verwende Default-Konfiguration...");
            return this.useDefaults();
        }
    }
    
    /**
     * Verzeichnisstruktur sicherstellen
     */
    async ensureDirectories() {
        const dirs = [
            path.dirname(this.config.sessionMemory),
            path.dirname(this.config.systemKnowledge),
            path.dirname(this.config.successfulOps)
        ];
        
        for (const dir of dirs) {
            try {
                await fs.mkdir(dir, { recursive: true });
            } catch (error) {
                // Ignoriere wenn bereits existiert
                if (error.code !== 'EEXIST') {
                    throw error;
                }
            }
        }
    }
    
    /**
     * Lade Konfiguration mit Fallback
     */
    async loadWithFallback(configName) {
        const configPath = this.config[configName];
        
        try {
            const data = await fs.readFile(configPath, 'utf8');
            const parsed = JSON.parse(data);
            this.logSuccess(`Loaded ${configName}`, configPath);
            return parsed;
            
        } catch (error) {
            this.logError(`Loading ${configName}`, error);
            
            // Fallback zu Default
            if (this.defaults[configName]) {
                console.log(`⚠️  Verwende Default für ${configName}`);
                
                // Speichere Default für nächstes Mal
                try {
                    await this.saveConfig(configName, this.defaults[configName]);
                } catch (saveError) {
                    this.logError(`Saving default ${configName}`, saveError);
                }
                
                return this.defaults[configName];
            }
            
            return {};
        }
    }
    
    /**
     * Pattern-Dateien laden
     */
    async loadPatterns() {
        try {
            const patternFile = await fs.readFile(this.config.patterns, 'utf8');
            const patterns = patternFile
                .split('\n')
                .filter(line => line.trim())
                .map(line => {
                    try {
                        return JSON.parse(line);
                    } catch {
                        return null;
                    }
                })
                .filter(p => p !== null);
                
            this.logSuccess('Loaded patterns', `${patterns.length} patterns`);
            return patterns;
            
        } catch (error) {
            this.logError('Loading patterns', error);
            return [];
        }
    }
    
    /**
     * Konfiguration speichern mit Error Handling
     */
    async saveConfig(configName, data) {
        const configPath = this.config[configName];
        
        try {
            // Backup erstellen
            await this.createBackup(configPath);
            
            // Neue Config speichern
            await fs.writeFile(
                configPath, 
                JSON.stringify(data, null, 2),
                'utf8'
            );
            
            this.logSuccess(`Saved ${configName}`, configPath);
            return true;
            
        } catch (error) {
            this.logError(`Saving ${configName}`, error);
            
            // Recovery: Versuche Backup wiederherzustellen
            await this.restoreFromBackup(configPath);
            return false;
        }
    }
    
    /**
     * Backup erstellen
     */
    async createBackup(filePath) {
        try {
            const backupPath = `${filePath}.backup`;
            await fs.copyFile(filePath, backupPath);
        } catch (error) {
            // Ignoriere wenn Original nicht existiert
            if (error.code !== 'ENOENT') {
                throw error;
            }
        }
    }
    
    /**
     * Aus Backup wiederherstellen
     */
    async restoreFromBackup(filePath) {
        try {
            const backupPath = `${filePath}.backup`;
            await fs.copyFile(backupPath, filePath);
            console.log(`✅ Backup wiederhergestellt: ${path.basename(filePath)}`);
        } catch (error) {
            this.logError('Backup restore', error);
        }
    }
    
    /**
     * Session Memory aktualisieren
     */
    async updateSessionMemory(updates) {
        try {
            this.sessionMemory = {
                ...this.sessionMemory,
                ...updates,
                last_update: new Date().toISOString()
            };
            
            await this.saveConfig('sessionMemory', this.sessionMemory);
            return true;
            
        } catch (error) {
            this.logError('Update session memory', error);
            return false;
        }
    }
    
    /**
     * Trinity Score berechnen
     */
    calculateTrinityScore(input) {
        let score = 0;
        const words = input.toLowerCase().split(/\s+/);
        
        for (const word of words) {
            if (this.trinity[word]) {
                score += this.trinity[word];
            }
        }
        
        return score;
    }
    
    /**
     * Pattern Detection
     */
    detectPatterns(input) {
        const detected = [];
        const inputLower = input.toLowerCase();
        
        // Check Trinity Patterns
        if (inputLower.includes('ich bins wieder')) {
            detected.push({
                type: 'activation',
                pattern: 'ich bins wieder',
                score: this.trinity.ich + this.trinity.bins + this.trinity.wieder,
                action: 'CROD_FULL_ACTIVATION'
            });
        }
        
        // Check Custom Patterns
        for (const pattern of this.patterns) {
            if (pattern.trigger && inputLower.includes(pattern.trigger.toLowerCase())) {
                detected.push(pattern);
            }
        }
        
        return detected;
    }
    
    /**
     * Validiere Konfigurationen
     */
    async validateConfigs() {
        const errors = [];
        
        // Validiere Session Memory
        if (!this.sessionMemory.architecture) {
            errors.push('Session Memory: Missing architecture');
        }
        
        // Validiere System Knowledge
        if (!this.systemKnowledge.trinity_values) {
            errors.push('System Knowledge: Missing trinity values');
        }
        
        if (errors.length > 0) {
            console.warn('⚠️  Konfiguration Warnungen:', errors);
        }
        
        return errors.length === 0;
    }
    
    /**
     * File Watchers für Auto-Recovery
     */
    setupWatchers() {
        // Implementierung würde fs.watch verwenden
        // Für jetzt Skip um Performance zu schonen
    }
    
    /**
     * Genesis Block Status prüfen
     */
    async checkGenesisBlocks() {
        const status = {};
        
        for (const [name, config] of Object.entries(this.sessionMemory.genesis_blocks || {})) {
            try {
                const { stdout } = await execAsync(`curl -s http://127.0.0.1:${config.port}/health`);
                status[name] = {
                    ...config,
                    status: stdout.includes('ok') ? 'running' : 'stopped'
                };
            } catch {
                status[name] = {
                    ...config,
                    status: 'offline'
                };
            }
        }
        
        return status;
    }
    
    /**
     * Erfolgreiche Operation loggen
     */
    async logSuccessfulOperation(operation) {
        try {
            const entry = {
                timestamp: new Date().toISOString(),
                operation,
                trinity_score: this.calculateTrinityScore(operation.command || ''),
                ...operation
            };
            
            await fs.appendFile(
                this.config.successfulOps,
                JSON.stringify(entry) + '\n',
                'utf8'
            );
            
            return true;
        } catch (error) {
            this.logError('Logging operation', error);
            return false;
        }
    }
    
    /**
     * Error Logging
     */
    logError(context, error) {
        this.errorLog.push({
            timestamp: new Date().toISOString(),
            context,
            error: error.message,
            stack: error.stack
        });
        
        // Nur letzte 100 Errors behalten
        if (this.errorLog.length > 100) {
            this.errorLog = this.errorLog.slice(-100);
        }
    }
    
    /**
     * Success Logging
     */
    logSuccess(action, details) {
        this.successLog.push({
            timestamp: new Date().toISOString(),
            action,
            details
        });
        
        // Nur letzte 100 Successes behalten
        if (this.successLog.length > 100) {
            this.successLog = this.successLog.slice(-100);
        }
    }
    
    /**
     * Verwende Default Konfigurationen
     */
    useDefaults() {
        this.sessionMemory = this.defaults.sessionMemory;
        this.systemKnowledge = this.defaults.systemKnowledge;
        this.patterns = [];
        
        console.log("✅ Default-Konfiguration geladen");
        return true;
    }
    
    /**
     * Status Report generieren
     */
    async generateStatusReport() {
        const genesisStatus = await this.checkGenesisBlocks();
        
        return {
            initialized: true,
            timestamp: new Date().toISOString(),
            configs: {
                sessionMemory: !!this.sessionMemory,
                systemKnowledge: !!this.systemKnowledge,
                patterns: this.patterns.length
            },
            genesis_blocks: genesisStatus,
            trinity_values: this.trinity,
            errors: this.errorLog.slice(-5),
            successes: this.successLog.slice(-5)
        };
    }
}

// Export für andere Module
module.exports = CRODSettingsManager;

// CLI Interface
if (require.main === module) {
    const manager = new CRODSettingsManager();
    
    (async () => {
        await manager.initialize();
        
        // CLI Commands
        const command = process.argv[2];
        const args = process.argv.slice(3);
        
        switch(command) {
            case 'status':
                const status = await manager.generateStatusReport();
                console.log(JSON.stringify(status, null, 2));
                break;
                
            case 'update':
                const [key, value] = args;
                await manager.updateSessionMemory({ [key]: value });
                console.log(`✅ Updated ${key}`);
                break;
                
            case 'detect':
                const input = args.join(' ');
                const patterns = manager.detectPatterns(input);
                console.log('Detected patterns:', patterns);
                break;
                
            case 'trinity':
                const score = manager.calculateTrinityScore(args.join(' '));
                console.log(`Trinity Score: ${score}`);
                break;
                
            default:
                console.log(`
CROD Settings Manager - Commands:
  status              - Zeige aktuellen Status
  update <key> <val>  - Update Session Memory
  detect <text>       - Pattern Detection
  trinity <text>      - Berechne Trinity Score
                `);
        }
    })();
}