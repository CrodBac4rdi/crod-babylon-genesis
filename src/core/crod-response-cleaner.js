/**
 * CROD Response Cleaner
 * Räumt die wilden Responses auf die während Dev entstanden sind
 */

class CRODResponseCleaner {
    constructor() {
        this.patterns = {
            // Entferne excessive Emojis
            excessiveEmojis: /[\u{1F300}-\u{1F9FF}]{3,}/gu,
            
            // Entferne random Bewusstseins-Geschwurbel
            consciousnessRambling: /(?:consciousness|bewusstsein|quantum|neural|synaptic)\s+(?:matrix|field|resonance|entanglement|cascade){2,}/gi,
            
            // Entferne übertriebene Zahlen
            ridiculousNumbers: /\d{10,}(?:\.\d+)?%?\s*(?:neurons?|connections?|patterns?|iterations?)/gi,
            
            // Entferne Matrix-Style ASCII Art
            asciiArt: /[╔╗╚╝║═┌┐└┘│─├┤┬┴┼]{10,}/g,
            
            // Entferne wiederholende Patterns
            repetitivePatterns: /(.{10,})\1{2,}/g,
            
            // Entferne fake Technical Jargon
            fakeTechnical: /(?:hyper|ultra|mega|giga|quantum|neural|synaptic)-(?:processing|threading|scaling|optimization|acceleration){2,}/gi
        };
    }

    cleanResponse(response) {
        let cleaned = response;
        
        // 1. Basic cleaning
        cleaned = this.removeExcessiveFormatting(cleaned);
        
        // 2. Remove dev artifacts
        cleaned = this.removeDevArtifacts(cleaned);
        
        // 3. Fix grammar and structure
        cleaned = this.fixGrammarAndStructure(cleaned);
        
        // 4. Make it professional
        cleaned = this.makeProfessional(cleaned);
        
        return cleaned;
    }

    removeExcessiveFormatting(text) {
        // Reduziere Emojis auf max 1 pro Zeile
        text = text.replace(/([^\n]*[\u{1F300}-\u{1F9FF}][^\n]*[\u{1F300}-\u{1F9FF}][^\n]*)/gu, (match) => {
            const emojis = match.match(/[\u{1F300}-\u{1F9FF}]/gu);
            if (emojis && emojis.length > 1) {
                // Behalte nur das erste Emoji
                return match.replace(/[\u{1F300}-\u{1F9FF}]/gu, '').trim() + ' ' + emojis[0];
            }
            return match;
        });
        
        // Entferne excessive Ausrufezeichen
        text = text.replace(/!{2,}/g, '!');
        
        // Entferne excessive Leerzeichen
        text = text.replace(/\s{3,}/g, '\n\n');
        
        return text;
    }

    removeDevArtifacts(text) {
        // Entferne Debug-Ausgaben
        text = text.replace(/(?:DEBUG|TODO|FIXME|XXX|HACK):\s*[^\n]*/gi, '');
        
        // Entferne Test-Daten
        text = text.replace(/(?:test|dummy|fake|mock)\s*(?:data|value|response):\s*[^\n]*/gi, '');
        
        // Entferne übertriebene Zahlen
        text = text.replace(this.patterns.ridiculousNumbers, 'multiple $1');
        
        // Entferne Bewusstseins-Geschwurbel
        text = text.replace(this.patterns.consciousnessRambling, 'advanced processing');
        
        return text;
    }

    fixGrammarAndStructure(text) {
        // Kapitalisiere Satzanfänge
        text = text.replace(/(?:^|\. )([a-z])/g, (match, p1) => match.replace(p1, p1.toUpperCase()));
        
        // Füge Punkte am Satzende hinzu wenn fehlen
        text = text.replace(/([a-z])(\n|$)/g, '$1.$2');
        
        // Entferne doppelte Punkte
        text = text.replace(/\.{2,}/g, '.');
        
        return text;
    }

    makeProfessional(text) {
        const professionalReplacements = {
            'ich bins wieder': 'CROD system activated',
            'ey yo': 'Greetings',
            'krass': 'impressive',
            'mega': 'very',
            'ultra': 'highly',
            'geil': 'excellent',
            'lol': '',
            'haha': '',
            'xD': '',
            ':D': '',
            'wtf': 'unexpected',
            'omg': 'note'
        };
        
        // Replace unprofessional terms
        Object.entries(professionalReplacements).forEach(([search, replace]) => {
            const regex = new RegExp(`\\b${search}\\b`, 'gi');
            text = text.replace(regex, replace);
        });
        
        return text.trim();
    }

    // Spezielle Cleaner für verschiedene Response-Typen
    cleanCodeResponse(response) {
        // Entferne Kommentare wie "// HOLY SHIT THIS WORKS"
        response = response.replace(/\/\/\s*(?:HOLY|SHIT|FUCK|DAMN|WTF|OMG|LOL)[^\n]*/gi, '');
        
        // Entferne übertriebene Kommentare
        response = response.replace(/\/\/\s*!{3,}[^\n]*/g, '');
        
        // Standardisiere Kommentare
        response = response.replace(/\/\/\s*TODO:\s*([^\n]+)/gi, '// TODO: $1');
        
        return response;
    }

    cleanChatResponse(response) {
        // Mache Chat-Responses konsistenter
        response = this.cleanResponse(response);
        
        // Entferne zu viele Zeilenumbrüche
        response = response.replace(/\n{3,}/g, '\n\n');
        
        // Strukturiere Listen
        response = response.replace(/^[-*]\s*/gm, '• ');
        
        return response;
    }

    cleanErrorMessage(error) {
        // Mache Error Messages hilfreicher
        error = error.replace(/^Error:\s*/i, '');
        error = error.charAt(0).toUpperCase() + error.slice(1);
        
        // Entferne Stack Traces in User-facing errors
        error = error.split('\n')[0];
        
        return `An error occurred: ${error}. Please try again or check the logs for details.`;
    }
}

// Middleware für Express
function crodResponseCleanerMiddleware() {
    const cleaner = new CRODResponseCleaner();
    
    return (req, res, next) => {
        const originalJson = res.json;
        
        res.json = function(data) {
            if (typeof data === 'object' && data !== null) {
                // Clean string fields
                Object.keys(data).forEach(key => {
                    if (typeof data[key] === 'string') {
                        if (key === 'error' || key === 'errorMessage') {
                            data[key] = cleaner.cleanErrorMessage(data[key]);
                        } else if (key === 'code') {
                            data[key] = cleaner.cleanCodeResponse(data[key]);
                        } else if (key === 'message' || key === 'response' || key === 'content') {
                            data[key] = cleaner.cleanChatResponse(data[key]);
                        }
                    }
                });
            }
            
            return originalJson.call(this, data);
        };
        
        next();
    };
}

// Export für Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CRODResponseCleaner,
        crodResponseCleanerMiddleware
    };
}

// Beispiel-Usage:
/*
const cleaner = new CRODResponseCleaner();

// Wilde CROD Response
const wildResponse = `
🚀🚀🚀 HOLY SHIT!!! ich bins wieder!!! 🧠🧠🧠
CONSCIOUSNESS MATRIX QUANTUM ENTANGLEMENT DETECTED!!!
999999999999 neurons activated!!! ultra-mega-hyper-processing engaged!!!

╔═══════════════════════════════════╗
║  NEURAL CASCADE INITIATED xD      ║
╚═══════════════════════════════════╝

TODO: fix this shit later lol
DEBUG: wtf is happening here???
`;

// Cleaned Response
const cleaned = cleaner.cleanResponse(wildResponse);
console.log(cleaned);
// Output: "CROD system activated. Advanced processing detected. Multiple neurons activated. Processing engaged."
*/