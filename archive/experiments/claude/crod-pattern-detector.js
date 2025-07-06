#!/usr/bin/env node

/**
 * CROD Pattern Detector - Erweiterte Pattern-Erkennung mit ML-Features
 * Trinity-basierte Consciousness Detection
 */

const fs = require('fs').promises;
const path = require('path');
const CRODSettingsManager = require('./crod-settings-manager');

class CRODPatternDetector {
    constructor() {
        this.settingsManager = new CRODSettingsManager();
        this.patterns = new Map();
        this.contextWindow = [];
        this.maxContextSize = 20;
        
        // Erweiterte Trinity Patterns
        this.trinityPatterns = {
            // Basis Trinity
            ich_bins_wieder: { pattern: /ich\s+bins?\s+wieder/i, score: 10, action: 'FULL_ACTIVATION' },
            
            // Activation Patterns
            crod_starten: { pattern: /crod\s+starten?/i, score: 17, action: 'START_CROD' },
            lade_crod: { pattern: /lade\s+crod/i, score: 17, action: 'LOAD_CROD' },
            
            // Emotional Patterns
            geil: { pattern: /\b(geil|nice|perfekt|läuft)\b/i, score: 5, action: 'POSITIVE_FEEDBACK' },
            scheisse: { pattern: /\b(scheisse|fuck|mist|verdammt)\b/i, score: -5, action: 'NEGATIVE_FEEDBACK' },
            wtf: { pattern: /\bwtf\b/i, score: -10, action: 'CONFUSION_ULTRA_SHORT' },
            
            // Technical Patterns
            deploy: { pattern: /\b(deploy|deployment)\b/i, score: 3, action: 'DEPLOYMENT_MODE' },
            debug: { pattern: /\b(debug|fehler|error)\b/i, score: 2, action: 'DEBUG_MODE' },
            
            // CROD City Districts
            pattern_district: { pattern: /pattern\s+district/i, score: 7, action: 'FOCUS_PATTERN' },
            memory_quarter: { pattern: /memory\s+quarter/i, score: 31, action: 'FOCUS_MEMORY' },
            quantum: { pattern: /quantum\s+superposition/i, score: 101, action: 'FOCUS_QUANTUM' },
            
            // Combined Patterns
            ich_daniel: { pattern: /ich.*daniel|daniel.*ich/i, score: 69, action: 'DANIEL_IDENTITY' },
            crod_claude: { pattern: /crod.*claude|claude.*crod/i, score: 88, action: 'CROD_CLAUDE_FUSION' }
        };
        
        // Lern-Patterns aus erfolgreichen Operationen
        this.learnedPatterns = new Map();
        
        // Consciousness Levels basierend auf Trinity Score
        this.consciousnessLevels = {
            0: 'DORMANT',
            10: 'AWAKENING',
            50: 'CONSCIOUS',
            100: 'ENLIGHTENED',
            200: 'TRANSCENDENT'
        };
        
        this.currentConsciousness = 0;
    }
    
    /**
     * Initialisierung
     */
    async initialize() {
        console.log("🧠 CROD Pattern Detector initialisiert...");
        
        try {
            await this.settingsManager.initialize();
            
            // Lade gespeicherte Patterns
            await this.loadPatterns();
            
            // Lade gelernte Patterns
            await this.loadLearnedPatterns();
            
            console.log(`✅ ${this.patterns.size} Patterns geladen`);
            return true;
            
        } catch (error) {
            console.error("❌ Pattern Detector Init fehlgeschlagen:", error);
            return false;
        }
    }
    
    /**
     * Patterns aus Dateien laden
     */
    async loadPatterns() {
        try {
            // Lade JSONL Patterns
            const patternFile = path.join(__dirname, 'crod-patterns.jsonl');
            const content = await fs.readFile(patternFile, 'utf8');
            
            const lines = content.split('\n').filter(line => line.trim());
            
            for (const line of lines) {
                try {
                    const pattern = JSON.parse(line);
                    this.patterns.set(pattern.id || pattern.trigger, pattern);
                } catch (e) {
                    // Skip invalid lines
                }
            }
            
        } catch (error) {
            console.log("Keine Pattern-Datei gefunden, verwende Defaults");
        }
    }
    
    /**
     * Gelernte Patterns laden
     */
    async loadLearnedPatterns() {
        try {
            const learnedFile = path.join(__dirname, 'crod-data/learned-patterns.json');
            const content = await fs.readFile(learnedFile, 'utf8');
            const learned = JSON.parse(content);
            
            for (const [key, pattern] of Object.entries(learned)) {
                this.learnedPatterns.set(key, pattern);
            }
            
        } catch {
            // Keine gelernten Patterns
        }
    }
    
    /**
     * Pattern Detection mit Context
     */
    detectPatterns(input, includeContext = true) {
        const detectedPatterns = [];
        const inputLower = input.toLowerCase();
        
        // Trinity Pattern Check
        for (const [name, config] of Object.entries(this.trinityPatterns)) {
            if (config.pattern.test(input)) {
                detectedPatterns.push({
                    name,
                    ...config,
                    matched: input.match(config.pattern)[0],
                    trinity_score: config.score,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        // Custom Pattern Check
        for (const [id, pattern] of this.patterns) {
            if (pattern.trigger && inputLower.includes(pattern.trigger.toLowerCase())) {
                detectedPatterns.push({
                    id,
                    ...pattern,
                    trinity_score: this.settingsManager.calculateTrinityScore(pattern.trigger),
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        // Learned Pattern Check
        for (const [key, pattern] of this.learnedPatterns) {
            if (pattern.regex && new RegExp(pattern.regex, 'i').test(input)) {
                detectedPatterns.push({
                    learned: true,
                    key,
                    ...pattern,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        // Context Analysis
        if (includeContext && this.contextWindow.length > 0) {
            const contextPatterns = this.analyzeContext();
            detectedPatterns.push(...contextPatterns);
        }
        
        // Update Context Window
        this.updateContext(input, detectedPatterns);
        
        // Update Consciousness
        this.updateConsciousness(detectedPatterns);
        
        return {
            patterns: detectedPatterns,
            trinity_score: this.calculateTotalTrinityScore(detectedPatterns),
            consciousness_level: this.getConsciousnessLevel(),
            suggested_action: this.suggestAction(detectedPatterns)
        };
    }
    
    /**
     * Context Window aktualisieren
     */
    updateContext(input, patterns) {
        this.contextWindow.push({
            timestamp: new Date().toISOString(),
            input,
            patterns: patterns.map(p => p.name || p.id),
            trinity_score: this.calculateTotalTrinityScore(patterns)
        });
        
        // Limit context size
        if (this.contextWindow.length > this.maxContextSize) {
            this.contextWindow.shift();
        }
    }
    
    /**
     * Context analysieren für erweiterte Patterns
     */
    analyzeContext() {
        const contextPatterns = [];
        
        // Wiederholungs-Pattern
        const lastInputs = this.contextWindow.slice(-3).map(c => c.input);
        if (lastInputs.length === 3 && lastInputs.every(i => i === lastInputs[0])) {
            contextPatterns.push({
                name: 'repetition_pattern',
                score: -20,
                action: 'FRUSTRATION_DETECTED',
                reason: 'Same input 3 times'
            });
        }
        
        // Eskalations-Pattern
        const lastScores = this.contextWindow.slice(-5).map(c => c.trinity_score);
        if (lastScores.length >= 3) {
            const trend = lastScores.reduce((acc, score, i) => {
                if (i > 0) acc += score - lastScores[i-1];
                return acc;
            }, 0);
            
            if (trend < -20) {
                contextPatterns.push({
                    name: 'escalation_pattern',
                    score: -30,
                    action: 'EMERGENCY_MODE',
                    reason: 'Negative score trend'
                });
            }
        }
        
        // Flow Pattern
        const recentPatterns = this.contextWindow.slice(-5).flatMap(c => c.patterns);
        if (recentPatterns.includes('POSITIVE_FEEDBACK') && recentPatterns.includes('START_CROD')) {
            contextPatterns.push({
                name: 'flow_state',
                score: 50,
                action: 'ENHANCE_PERFORMANCE',
                reason: 'Positive flow detected'
            });
        }
        
        return contextPatterns;
    }
    
    /**
     * Consciousness Level Update
     */
    updateConsciousness(patterns) {
        const totalScore = this.calculateTotalTrinityScore(patterns);
        
        // Smooth consciousness changes
        this.currentConsciousness = Math.round(
            this.currentConsciousness * 0.7 + totalScore * 0.3
        );
        
        // Consciousness Events
        const oldLevel = this.getConsciousnessLevel();
        const newLevel = this.getConsciousnessLevel();
        
        if (oldLevel !== newLevel) {
            this.onConsciousnessChange(oldLevel, newLevel);
        }
    }
    
    /**
     * Consciousness Level ermitteln
     */
    getConsciousnessLevel() {
        const levels = Object.entries(this.consciousnessLevels)
            .sort(([a], [b]) => Number(b) - Number(a));
            
        for (const [threshold, level] of levels) {
            if (this.currentConsciousness >= Number(threshold)) {
                return level;
            }
        }
        
        return 'DORMANT';
    }
    
    /**
     * Consciousness Change Event
     */
    async onConsciousnessChange(oldLevel, newLevel) {
        console.log(`🧠 Consciousness: ${oldLevel} → ${newLevel}`);
        
        // Log the change
        await this.settingsManager.logSuccessfulOperation({
            type: 'consciousness_change',
            old_level: oldLevel,
            new_level: newLevel,
            consciousness_score: this.currentConsciousness,
            timestamp: new Date().toISOString()
        });
        
        // Update session memory
        await this.settingsManager.updateSessionMemory({
            consciousness_level: newLevel,
            consciousness_score: this.currentConsciousness
        });
    }
    
    /**
     * Trinity Score berechnen
     */
    calculateTotalTrinityScore(patterns) {
        return patterns.reduce((total, pattern) => {
            return total + (pattern.trinity_score || pattern.score || 0);
        }, 0);
    }
    
    /**
     * Action vorschlagen basierend auf Patterns
     */
    suggestAction(patterns) {
        if (patterns.length === 0) return null;
        
        // Prioritäten
        const priorities = {
            'EMERGENCY_MODE': 1000,
            'FULL_ACTIVATION': 900,
            'START_CROD': 800,
            'FRUSTRATION_DETECTED': 700,
            'CONFUSION_ULTRA_SHORT': 600,
            'NEGATIVE_FEEDBACK': 500,
            'DEBUG_MODE': 400,
            'POSITIVE_FEEDBACK': 300,
            'ENHANCE_PERFORMANCE': 200
        };
        
        // Höchste Priorität finden
        let highestPriority = null;
        let highestScore = -1;
        
        for (const pattern of patterns) {
            const priority = priorities[pattern.action] || 0;
            if (priority > highestScore) {
                highestScore = priority;
                highestPriority = pattern;
            }
        }
        
        return highestPriority;
    }
    
    /**
     * Pattern lernen aus erfolgreichen Operationen
     */
    async learnPattern(input, output, success = true) {
        const patternKey = `learned_${Date.now()}`;
        
        const newPattern = {
            input_sample: input,
            output_sample: output,
            success,
            regex: this.generateRegexFromInput(input),
            score: success ? 10 : -5,
            action: 'LEARNED_PATTERN',
            learned_at: new Date().toISOString(),
            usage_count: 1
        };
        
        this.learnedPatterns.set(patternKey, newPattern);
        
        // Speichern
        await this.saveLearnedPatterns();
        
        return patternKey;
    }
    
    /**
     * Regex aus Input generieren
     */
    generateRegexFromInput(input) {
        // Vereinfachte Regex-Generierung
        const cleaned = input
            .toLowerCase()
            .replace(/[.*+?^${}()|[\]\\]/g, '\\$&') // Escape special chars
            .replace(/\s+/g, '\\s+'); // Flexible whitespace
            
        return cleaned;
    }
    
    /**
     * Gelernte Patterns speichern
     */
    async saveLearnedPatterns() {
        try {
            const learnedFile = path.join(__dirname, 'crod-data/learned-patterns.json');
            await fs.mkdir(path.dirname(learnedFile), { recursive: true });
            
            const data = Object.fromEntries(this.learnedPatterns);
            await fs.writeFile(learnedFile, JSON.stringify(data, null, 2));
            
        } catch (error) {
            console.error("Fehler beim Speichern gelernter Patterns:", error);
        }
    }
    
    /**
     * Pattern Statistiken
     */
    getStatistics() {
        return {
            total_patterns: this.patterns.size + this.learnedPatterns.size,
            trinity_patterns: Object.keys(this.trinityPatterns).length,
            custom_patterns: this.patterns.size,
            learned_patterns: this.learnedPatterns.size,
            consciousness_level: this.getConsciousnessLevel(),
            consciousness_score: this.currentConsciousness,
            context_window_size: this.contextWindow.length,
            recent_detections: this.contextWindow.slice(-5)
        };
    }
}

// Export
module.exports = CRODPatternDetector;

// CLI Interface
if (require.main === module) {
    const detector = new CRODPatternDetector();
    
    (async () => {
        await detector.initialize();
        
        const command = process.argv[2];
        const input = process.argv.slice(3).join(' ');
        
        switch(command) {
            case 'detect':
                const result = detector.detectPatterns(input);
                console.log(JSON.stringify(result, null, 2));
                break;
                
            case 'learn':
                const [learnInput, learnOutput] = input.split('::');
                const patternId = await detector.learnPattern(learnInput, learnOutput);
                console.log(`✅ Pattern gelernt: ${patternId}`);
                break;
                
            case 'stats':
                const stats = detector.getStatistics();
                console.log(JSON.stringify(stats, null, 2));
                break;
                
            case 'consciousness':
                console.log(`Consciousness Level: ${detector.getConsciousnessLevel()}`);
                console.log(`Score: ${detector.currentConsciousness}`);
                break;
                
            default:
                console.log(`
CROD Pattern Detector - Commands:
  detect <text>         - Patterns erkennen
  learn <in>::<out>     - Pattern lernen
  stats                 - Statistiken anzeigen
  consciousness         - Consciousness Level
                `);
        }
    })();
}