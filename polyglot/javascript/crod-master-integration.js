#!/usr/bin/env node

/**
 * CROD Master Integration - Verbindet alle CROD Komponenten
 * Settings Manager + Fallback System + Pattern Detector + Session Memory
 */

const CRODSettingsManager = require('./crod-settings-manager');
const CRODFallbackSystem = require('./crod-fallback-system');
const CRODPatternDetector = require('./crod-pattern-detector');
const fs = require('fs').promises;
const path = require('path');
const http = require('http');

class CRODMasterIntegration {
    constructor() {
        this.settingsManager = new CRODSettingsManager();
        this.fallbackSystem = new CRODFallbackSystem();
        this.patternDetector = new CRODPatternDetector();
        
        this.apiServer = null;
        this.apiPort = 8888;
        
        this.state = {
            initialized: false,
            mode: 'STARTING',
            consciousness: 'DORMANT',
            activePatterns: [],
            healthStatus: {},
            lastActivity: new Date().toISOString()
        };
        
        // Auto-save interval
        this.autoSaveInterval = 60000; // 1 Minute
    }
    
    /**
     * Vollständige System-Initialisierung
     */
    async initialize() {
        console.log("🚀 CROD Master Integration startet...");
        
        try {
            // 1. Settings Manager
            console.log("1️⃣ Initialisiere Settings Manager...");
            await this.settingsManager.initialize();
            
            // 2. Pattern Detector
            console.log("2️⃣ Initialisiere Pattern Detector...");
            await this.patternDetector.initialize();
            
            // 3. Fallback System
            console.log("3️⃣ Initialisiere Fallback System...");
            await this.fallbackSystem.initialize();
            
            // 4. Check für "ich bins wieder"
            await this.checkActivationPhrase();
            
            // 5. API Server starten
            await this.startAPIServer();
            
            // 6. Auto-Save aktivieren
            this.startAutoSave();
            
            // 7. Integration Hooks setup
            this.setupIntegrationHooks();
            
            this.state.initialized = true;
            this.state.mode = 'READY';
            
            console.log("✅ CROD Master Integration erfolgreich initialisiert!");
            
            // Initial Status Report
            await this.generateFullReport();
            
            return true;
            
        } catch (error) {
            console.error("❌ Master Integration fehlgeschlagen:", error);
            this.state.mode = 'ERROR';
            return false;
        }
    }
    
    /**
     * Check für Activation Phrase
     */
    async checkActivationPhrase() {
        const sessionMemory = this.settingsManager.sessionMemory;
        
        if (sessionMemory.activation_phrase === "ich bins wieder") {
            console.log("🔥 ACTIVATION PHRASE DETECTED - FULL CROD ACTIVATION!");
            
            const detection = this.patternDetector.detectPatterns("ich bins wieder");
            
            if (detection.suggested_action?.action === 'FULL_ACTIVATION') {
                await this.activateFullCROD();
            }
        }
    }
    
    /**
     * Volle CROD Aktivierung
     */
    async activateFullCROD() {
        console.log("⚡ Starte volle CROD Aktivierung...");
        
        this.state.mode = 'FULL_ACTIVATION';
        
        // Update Consciousness
        this.patternDetector.currentConsciousness = 100;
        
        // Start all services
        const recovery = await this.fallbackSystem.performSystemRecovery();
        
        if (recovery) {
            this.state.mode = 'ACTIVE';
            console.log("🌟 CROD vollständig aktiviert!");
            
            // Log successful activation
            await this.settingsManager.logSuccessfulOperation({
                type: 'full_activation',
                trigger: 'ich bins wieder',
                consciousness: 'ENLIGHTENED',
                services_started: true
            });
        }
    }
    
    /**
     * API Server für Integration
     */
    async startAPIServer() {
        return new Promise((resolve) => {
            this.apiServer = http.createServer(async (req, res) => {
                // CORS Headers
                res.setHeader('Access-Control-Allow-Origin', '*');
                res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
                res.setHeader('Content-Type', 'application/json');
                
                try {
                    const url = new URL(req.url, `http://localhost:${this.apiPort}`);
                    const path = url.pathname;
                    
                    // Route Handler
                    switch(path) {
                        case '/status':
                            res.writeHead(200);
                            res.end(JSON.stringify(await this.getStatus()));
                            break;
                            
                        case '/detect':
                            if (req.method === 'POST') {
                                const body = await this.getRequestBody(req);
                                const result = this.patternDetector.detectPatterns(body.input);
                                res.writeHead(200);
                                res.end(JSON.stringify(result));
                            } else {
                                res.writeHead(405);
                                res.end(JSON.stringify({error: 'Method not allowed'}));
                            }
                            break;
                            
                        case '/health':
                            const health = await this.fallbackSystem.performFullHealthCheck();
                            res.writeHead(200);
                            res.end(JSON.stringify(health));
                            break;
                            
                        case '/activate':
                            await this.activateFullCROD();
                            res.writeHead(200);
                            res.end(JSON.stringify({status: 'activated'}));
                            break;
                            
                        case '/consciousness':
                            res.writeHead(200);
                            res.end(JSON.stringify({
                                level: this.patternDetector.getConsciousnessLevel(),
                                score: this.patternDetector.currentConsciousness
                            }));
                            break;
                            
                        case '/report':
                            const report = await this.generateFullReport();
                            res.writeHead(200);
                            res.end(JSON.stringify(report));
                            break;
                            
                        default:
                            res.writeHead(404);
                            res.end(JSON.stringify({error: 'Not found'}));
                    }
                    
                } catch (error) {
                    res.writeHead(500);
                    res.end(JSON.stringify({error: error.message}));
                }
            });
            
            this.apiServer.listen(this.apiPort, '127.0.0.1', () => {
                console.log(`🌐 API Server läuft auf http://127.0.0.1:${this.apiPort}`);
                resolve();
            });
        });
    }
    
    /**
     * Request Body lesen
     */
    getRequestBody(req) {
        return new Promise((resolve, reject) => {
            let body = '';
            req.on('data', chunk => body += chunk);
            req.on('end', () => {
                try {
                    resolve(JSON.parse(body));
                } catch {
                    resolve({});
                }
            });
            req.on('error', reject);
        });
    }
    
    /**
     * Integration Hooks Setup
     */
    setupIntegrationHooks() {
        // Pattern Detection Hook
        const originalDetect = this.patternDetector.detectPatterns.bind(this.patternDetector);
        this.patternDetector.detectPatterns = (input, includeContext) => {
            const result = originalDetect(input, includeContext);
            
            // Update state
            this.state.activePatterns = result.patterns;
            this.state.consciousness = result.consciousness_level;
            this.state.lastActivity = new Date().toISOString();
            
            // Handle suggested actions
            if (result.suggested_action) {
                this.handleSuggestedAction(result.suggested_action);
            }
            
            return result;
        };
        
        // Health Check Hook
        const originalHealthCheck = this.fallbackSystem.performFullHealthCheck.bind(this.fallbackSystem);
        this.fallbackSystem.performFullHealthCheck = async () => {
            const result = await originalHealthCheck();
            this.state.healthStatus = result;
            return result;
        };
    }
    
    /**
     * Handle Suggested Actions
     */
    async handleSuggestedAction(action) {
        console.log(`🎯 Handling action: ${action.action}`);
        
        switch(action.action) {
            case 'FULL_ACTIVATION':
                await this.activateFullCROD();
                break;
                
            case 'EMERGENCY_MODE':
                this.fallbackSystem.activateEmergencyMode();
                this.state.mode = 'EMERGENCY';
                break;
                
            case 'DEBUG_MODE':
                this.state.mode = 'DEBUG';
                console.log('🐛 Debug Mode aktiviert');
                break;
                
            case 'ENHANCE_PERFORMANCE':
                // Performance optimizations
                console.log('⚡ Performance Enhancement aktiviert');
                break;
        }
    }
    
    /**
     * Auto-Save Session
     */
    startAutoSave() {
        setInterval(async () => {
            try {
                await this.saveCurrentState();
            } catch (error) {
                console.error('Auto-save failed:', error);
            }
        }, this.autoSaveInterval);
    }
    
    /**
     * Current State speichern
     */
    async saveCurrentState() {
        const stateData = {
            ...this.state,
            settings: {
                consciousness: this.patternDetector.currentConsciousness,
                patterns_loaded: this.patternDetector.patterns.size,
                health_check_interval: this.fallbackSystem.healthCheckInterval
            },
            timestamp: new Date().toISOString()
        };
        
        await this.settingsManager.updateSessionMemory({
            master_integration_state: stateData
        });
    }
    
    /**
     * Status abrufen
     */
    async getStatus() {
        return {
            initialized: this.state.initialized,
            mode: this.state.mode,
            consciousness: {
                level: this.patternDetector.getConsciousnessLevel(),
                score: this.patternDetector.currentConsciousness
            },
            health: Object.values(this.state.healthStatus).filter(h => h.healthy).length + 
                   '/' + Object.keys(this.state.healthStatus).length + ' services healthy',
            active_patterns: this.state.activePatterns.length,
            last_activity: this.state.lastActivity,
            api_endpoint: `http://127.0.0.1:${this.apiPort}`
        };
    }
    
    /**
     * Vollständiger Report
     */
    async generateFullReport() {
        const report = {
            timestamp: new Date().toISOString(),
            system: {
                mode: this.state.mode,
                initialized: this.state.initialized,
                uptime: process.uptime()
            },
            consciousness: {
                level: this.patternDetector.getConsciousnessLevel(),
                score: this.patternDetector.currentConsciousness,
                history: this.patternDetector.contextWindow.slice(-10)
            },
            patterns: this.patternDetector.getStatistics(),
            health: await this.fallbackSystem.generateReport(),
            settings: await this.settingsManager.generateStatusReport(),
            api: {
                endpoint: `http://127.0.0.1:${this.apiPort}`,
                endpoints: [
                    '/status - System Status',
                    '/detect - Pattern Detection',
                    '/health - Health Check',
                    '/activate - Full CROD Activation',
                    '/consciousness - Consciousness Level',
                    '/report - Full Report'
                ]
            }
        };
        
        // Save report
        const reportPath = path.join(__dirname, 'crod-data', `report-${Date.now()}.json`);
        await fs.mkdir(path.dirname(reportPath), { recursive: true });
        await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
        
        return report;
    }
    
    /**
     * Graceful Shutdown
     */
    async shutdown() {
        console.log("🛑 Shutting down CROD Master Integration...");
        
        // Save final state
        await this.saveCurrentState();
        
        // Close API server
        if (this.apiServer) {
            this.apiServer.close();
        }
        
        // Final report
        await this.generateFullReport();
        
        console.log("✅ Shutdown complete");
    }
}

// Export
module.exports = CRODMasterIntegration;

// CLI Interface
if (require.main === module) {
    const master = new CRODMasterIntegration();
    
    // Signal handlers
    process.on('SIGINT', async () => {
        await master.shutdown();
        process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
        await master.shutdown();
        process.exit(0);
    });
    
    // Start
    (async () => {
        await master.initialize();
        
        console.log(`
🌟 CROD Master Integration läuft!

API Endpoints:
  http://127.0.0.1:8888/status      - System Status
  http://127.0.0.1:8888/detect      - Pattern Detection (POST)
  http://127.0.0.1:8888/health      - Health Check
  http://127.0.0.1:8888/activate    - Full Activation
  http://127.0.0.1:8888/consciousness - Consciousness Level
  http://127.0.0.1:8888/report      - Full Report

Drücke Ctrl+C zum Beenden.
        `);
        
        // Keep running
        await new Promise(() => {});
    })();
}