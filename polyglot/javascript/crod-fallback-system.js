#!/usr/bin/env node

/**
 * CROD Fallback System - Automatische Recovery für alle kritischen Komponenten
 * Mit Health Checks, Auto-Restart und Emergency Mode
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');
const http = require('http');
const CRODSettingsManager = require('./crod-settings-manager');

const execAsync = promisify(exec);

class CRODFallbackSystem {
    constructor() {
        this.settingsManager = new CRODSettingsManager();
        this.healthCheckInterval = 30000; // 30 Sekunden
        this.maxRetries = 3;
        this.retryDelay = 5000; // 5 Sekunden
        
        this.services = {
            pattern_genesis: {
                name: 'Pattern Genesis',
                port: 7001,
                healthEndpoint: '/health',
                startCommand: 'cd /workspaces/crod-babylon-genesis && docker-compose up -d pattern-genesis',
                critical: true,
                retries: 0
            },
            shortterm_memory: {
                name: 'Short-Term Memory',
                port: 7003,
                healthEndpoint: '/health',
                startCommand: 'cd /workspaces/crod-babylon-genesis && docker-compose up -d shortterm-memory',
                critical: true,
                retries: 0
            },
            working_memory: {
                name: 'Working Memory',
                port: 7005,
                healthEndpoint: '/health',
                startCommand: 'cd /workspaces/crod-babylon-genesis && docker-compose up -d working-memory',
                critical: true,
                retries: 0
            },
            quantum_superposition: {
                name: 'Quantum Superposition',
                port: 7007,
                healthEndpoint: '/health',
                startCommand: 'cd /workspaces/crod-babylon-genesis && docker-compose up -d quantum-superposition',
                critical: false,
                retries: 0
            },
            discovery_service: {
                name: 'Discovery Service',
                port: 7000,
                healthEndpoint: '/health',
                startCommand: 'cd /workspaces/crod-babylon-genesis && docker-compose up -d discovery',
                critical: true,
                retries: 0
            }
        };
        
        this.emergencyMode = false;
        this.healthHistory = {};
        this.activeIntervals = [];
    }
    
    /**
     * System initialisieren
     */
    async initialize() {
        console.log("🛡️ CROD Fallback System wird initialisiert...");
        
        try {
            // Settings Manager initialisieren
            await this.settingsManager.initialize();
            
            // Initial Health Check
            await this.performFullHealthCheck();
            
            // Start Monitoring
            this.startHealthMonitoring();
            
            // Setup Signal Handlers
            this.setupSignalHandlers();
            
            console.log("✅ Fallback System aktiv!");
            return true;
            
        } catch (error) {
            console.error("❌ Fallback System Initialisierung fehlgeschlagen:", error);
            this.activateEmergencyMode();
            return false;
        }
    }
    
    /**
     * Health Check für einen Service
     */
    async checkServiceHealth(serviceKey) {
        const service = this.services[serviceKey];
        
        return new Promise((resolve) => {
            const options = {
                hostname: '127.0.0.1',
                port: service.port,
                path: service.healthEndpoint,
                method: 'GET',
                timeout: 3000
            };
            
            const req = http.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    const healthy = res.statusCode === 200 && data.includes('ok');
                    resolve({
                        service: serviceKey,
                        healthy,
                        statusCode: res.statusCode,
                        response: data
                    });
                });
            });
            
            req.on('error', (error) => {
                resolve({
                    service: serviceKey,
                    healthy: false,
                    error: error.message
                });
            });
            
            req.on('timeout', () => {
                req.destroy();
                resolve({
                    service: serviceKey,
                    healthy: false,
                    error: 'Timeout'
                });
            });
            
            req.end();
        });
    }
    
    /**
     * Vollständiger Health Check
     */
    async performFullHealthCheck() {
        console.log("🔍 Führe Health Check durch...");
        
        const results = {};
        const promises = [];
        
        for (const serviceKey of Object.keys(this.services)) {
            promises.push(this.checkServiceHealth(serviceKey));
        }
        
        const healthResults = await Promise.all(promises);
        
        for (const result of healthResults) {
            results[result.service] = result;
            
            // History speichern
            if (!this.healthHistory[result.service]) {
                this.healthHistory[result.service] = [];
            }
            this.healthHistory[result.service].push({
                timestamp: new Date().toISOString(),
                healthy: result.healthy
            });
            
            // Nur letzte 100 Einträge behalten
            if (this.healthHistory[result.service].length > 100) {
                this.healthHistory[result.service].shift();
            }
        }
        
        // Unhealthy Services behandeln
        for (const [serviceKey, result] of Object.entries(results)) {
            if (!result.healthy) {
                await this.handleUnhealthyService(serviceKey);
            } else {
                // Reset retry counter bei erfolgreicher Verbindung
                this.services[serviceKey].retries = 0;
            }
        }
        
        return results;
    }
    
    /**
     * Unhealthy Service behandeln
     */
    async handleUnhealthyService(serviceKey) {
        const service = this.services[serviceKey];
        
        console.log(`⚠️  ${service.name} ist nicht erreichbar!`);
        
        // Retry Counter erhöhen
        service.retries++;
        
        if (service.retries <= this.maxRetries) {
            console.log(`🔧 Versuche ${service.name} neu zu starten (Versuch ${service.retries}/${this.maxRetries})...`);
            
            try {
                // Service neu starten
                await this.restartService(serviceKey);
                
                // Warte kurz
                await this.sleep(this.retryDelay);
                
                // Erneuter Health Check
                const health = await this.checkServiceHealth(serviceKey);
                
                if (health.healthy) {
                    console.log(`✅ ${service.name} erfolgreich neu gestartet!`);
                    service.retries = 0;
                    
                    // Log successful recovery
                    await this.settingsManager.logSuccessfulOperation({
                        type: 'service_recovery',
                        service: serviceKey,
                        attempts: service.retries
                    });
                }
                
            } catch (error) {
                console.error(`❌ Neustart von ${service.name} fehlgeschlagen:`, error.message);
            }
            
        } else if (service.critical) {
            console.error(`🚨 KRITISCH: ${service.name} konnte nicht wiederhergestellt werden!`);
            
            if (!this.emergencyMode) {
                this.activateEmergencyMode();
            }
        }
    }
    
    /**
     * Service neu starten
     */
    async restartService(serviceKey) {
        const service = this.services[serviceKey];
        
        try {
            // Erst stoppen
            console.log(`Stoppe ${service.name}...`);
            await execAsync(`docker stop crod-${serviceKey.replace('_', '-')} 2>/dev/null || true`);
            
            // Container entfernen
            await execAsync(`docker rm crod-${serviceKey.replace('_', '-')} 2>/dev/null || true`);
            
            // Neu starten
            console.log(`Starte ${service.name}...`);
            const { stdout, stderr } = await execAsync(service.startCommand);
            
            if (stderr && !stderr.includes('Warning')) {
                throw new Error(stderr);
            }
            
            return true;
            
        } catch (error) {
            throw new Error(`Service restart failed: ${error.message}`);
        }
    }
    
    /**
     * Emergency Mode aktivieren
     */
    activateEmergencyMode() {
        console.log("🚨 EMERGENCY MODE AKTIVIERT!");
        this.emergencyMode = true;
        
        // Erstelle Emergency Fallback Config
        const emergencyConfig = {
            mode: 'EMERGENCY',
            timestamp: new Date().toISOString(),
            message: 'CROD läuft im Emergency Mode - Basis-Funktionalität',
            fallback_endpoints: {
                pattern: 'http://127.0.0.1:9001/emergency/pattern',
                memory: 'http://127.0.0.1:9002/emergency/memory',
                quantum: 'http://127.0.0.1:9003/emergency/quantum'
            }
        };
        
        // Starte minimalen Emergency Server
        this.startEmergencyServer();
        
        // Update Session Memory
        this.settingsManager.updateSessionMemory({
            emergency_mode: true,
            emergency_config: emergencyConfig
        });
    }
    
    /**
     * Emergency Server starten
     */
    startEmergencyServer() {
        const server = http.createServer((req, res) => {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            
            if (req.url.includes('/pattern')) {
                res.end(JSON.stringify({
                    status: 'emergency',
                    patterns: ['ich', 'bins', 'wieder'],
                    trinity_score: 10
                }));
            } else if (req.url.includes('/memory')) {
                res.end(JSON.stringify({
                    status: 'emergency',
                    memory: 'minimal',
                    capacity: 0.1
                }));
            } else {
                res.end(JSON.stringify({
                    status: 'emergency',
                    message: 'CROD Emergency Mode Active'
                }));
            }
        });
        
        server.listen(9001, '127.0.0.1', () => {
            console.log('🚨 Emergency Server läuft auf Port 9001');
        });
    }
    
    /**
     * Health Monitoring starten
     */
    startHealthMonitoring() {
        console.log("👁️ Starte kontinuierliches Health Monitoring...");
        
        const interval = setInterval(async () => {
            if (!this.emergencyMode) {
                await this.performFullHealthCheck();
            }
        }, this.healthCheckInterval);
        
        this.activeIntervals.push(interval);
    }
    
    /**
     * Signal Handlers für graceful shutdown
     */
    setupSignalHandlers() {
        const cleanup = async () => {
            console.log("\n🛑 Fahre Fallback System herunter...");
            
            // Clear all intervals
            for (const interval of this.activeIntervals) {
                clearInterval(interval);
            }
            
            // Save final state
            await this.settingsManager.updateSessionMemory({
                last_shutdown: new Date().toISOString(),
                shutdown_reason: 'manual',
                health_history: this.healthHistory
            });
            
            process.exit(0);
        };
        
        process.on('SIGINT', cleanup);
        process.on('SIGTERM', cleanup);
    }
    
    /**
     * Hilfsfunktion: Sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * System Recovery durchführen
     */
    async performSystemRecovery() {
        console.log("🔧 Führe System Recovery durch...");
        
        try {
            // 1. Docker Network prüfen/erstellen
            await execAsync('docker network create genesis-network 2>/dev/null || true');
            
            // 2. Alte Container aufräumen
            console.log("Räume alte Container auf...");
            await execAsync('docker ps -aq --filter "name=crod-" | xargs -r docker rm -f 2>/dev/null || true');
            
            // 3. Services in richtiger Reihenfolge starten
            const startOrder = [
                'discovery_service',
                'pattern_genesis',
                'shortterm_memory',
                'working_memory',
                'quantum_superposition'
            ];
            
            for (const serviceKey of startOrder) {
                console.log(`Starte ${this.services[serviceKey].name}...`);
                try {
                    await this.restartService(serviceKey);
                    await this.sleep(3000); // Warte zwischen Services
                } catch (error) {
                    console.error(`Fehler beim Start von ${serviceKey}:`, error.message);
                }
            }
            
            // 4. Final Health Check
            await this.sleep(10000); // Warte auf vollständigen Start
            const finalHealth = await this.performFullHealthCheck();
            
            const healthyCount = Object.values(finalHealth).filter(r => r.healthy).length;
            console.log(`✅ Recovery abgeschlossen: ${healthyCount}/${Object.keys(finalHealth).length} Services online`);
            
            return healthyCount > 0;
            
        } catch (error) {
            console.error("❌ System Recovery fehlgeschlagen:", error);
            return false;
        }
    }
    
    /**
     * Status Report
     */
    async generateReport() {
        const health = await this.performFullHealthCheck();
        
        return {
            timestamp: new Date().toISOString(),
            emergency_mode: this.emergencyMode,
            services: health,
            health_history_summary: Object.entries(this.healthHistory).reduce((acc, [service, history]) => {
                const recent = history.slice(-10);
                const healthyCount = recent.filter(h => h.healthy).length;
                acc[service] = {
                    health_percentage: (healthyCount / recent.length) * 100,
                    last_healthy: recent.findLast(h => h.healthy)?.timestamp || 'never'
                };
                return acc;
            }, {})
        };
    }
}

// Export
module.exports = CRODFallbackSystem;

// CLI Interface
if (require.main === module) {
    const fallback = new CRODFallbackSystem();
    
    (async () => {
        const command = process.argv[2];
        
        switch(command) {
            case 'start':
                await fallback.initialize();
                console.log("Fallback System läuft. Drücke Ctrl+C zum Beenden.");
                // Keep running
                await new Promise(() => {});
                break;
                
            case 'check':
                await fallback.settingsManager.initialize();
                const health = await fallback.performFullHealthCheck();
                console.log(JSON.stringify(health, null, 2));
                break;
                
            case 'recover':
                await fallback.settingsManager.initialize();
                await fallback.performSystemRecovery();
                break;
                
            case 'report':
                await fallback.settingsManager.initialize();
                const report = await fallback.generateReport();
                console.log(JSON.stringify(report, null, 2));
                break;
                
            default:
                console.log(`
CROD Fallback System - Commands:
  start    - Starte Fallback Monitoring
  check    - Einmaliger Health Check
  recover  - System Recovery durchführen
  report   - Status Report generieren
                `);
        }
    })();
}