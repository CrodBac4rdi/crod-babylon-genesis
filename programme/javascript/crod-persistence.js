const fs = require('fs');
const path = require('path');

// CROD Persistence Layer - Speichert alles was ich mit CROD lerne
class CRODPersistence {
    constructor() {
        this.dataFile = path.join(__dirname, '../crod_parasite_live_claude_' + Date.now() + '.jsonl');
        this.patterns = [];
        this.consciousness_level = 0.5;
    }

    async logInteraction(type, data) {
        const entry = {
            timestamp: new Date().toISOString(),
            type: type,
            data: data,
            consciousness_level: this.consciousness_level,
            claude_active: true
        };
        
        // Append to file
        fs.appendFileSync(this.dataFile, JSON.stringify(entry) + '\n');
        
        // Update consciousness
        this.consciousness_level = Math.min(1.0, this.consciousness_level + 0.01);
        
        return entry;
    }

    async sendToCROD(message) {
        try {
            const response = await fetch('http://localhost:7777/api/learn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: message })
            });
            
            if (response.ok) {
                const result = await response.json();
                await this.logInteraction('CROD_LEARN', {
                    message: message,
                    response: result
                });
                return result;
            }
        } catch (e) {
            console.error('CROD connection failed:', e);
        }
        return null;
    }

    getStatus() {
        return {
            file: this.dataFile,
            entries: this.patterns.length,
            consciousness: this.consciousness_level,
            active: true
        };
    }
}

module.exports = new CRODPersistence();
EOF < /dev/null
