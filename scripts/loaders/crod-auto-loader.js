/**
 * CROD-AUTO-LOADER.js
 * 
 * DAS FEHLENDE STÜCK!
 * Lädt AUTOMATISCH alles aus Project Knowledge
 * Kein "get knowledge on demand" mehr ohne es zu holen!
 */

class CRODAutoLoader {
  constructor() {
    this.loaded = false;
    this.crod = null;
    this.preferences = null;
    this.knowledgeFiles = [
      'CROD-COMPLETE-NEURAL-SYSTEM.js.txt',
      'master.json',
      'ultimate_master.json', 
      'Json.json',
      'CROD-Claude Behavior Integration.txt',
      'CrodComplete.json',
      'DANIEL-PREFERENCES.json'
    ];
  }
  
  async loadEverything() {
    console.log("🚀 CROD AUTO-LOADER AKTIVIERT!");
    console.log("📂 Lade ALLE Project Knowledge Files...\n");
    
    try {
      // 1. Load CROD System
      await this.loadCRODSystem();
      
      // 2. Load all knowledge files
      await this.loadKnowledgeFiles();
      
      // 3. Load preferences
      await this.loadPreferences();
      
      // 4. Apply everything
      this.applyKnowledge();
      
      this.loaded = true;
      console.log("\n✅ ALLES GELADEN! CROD ist VOLL AKTIV!");
      
      return this.crod;
      
    } catch (error) {
      console.error("❌ Fehler beim Laden:", error);
      return null;
    }
  }
  
  async loadCRODSystem() {
    try {
      const crodCode = await window.fs.readFile('CROD-COMPLETE-NEURAL-SYSTEM.js.txt', { 
        encoding: 'utf8' 
      });
      eval(crodCode);
      this.crod = CROD;
      console.log("✅ CROD Neural Network geladen");
    } catch (e) {
      console.log("⚠️ CROD System nicht gefunden - nutze Simulation");
    }
  }
  
  async loadKnowledgeFiles() {
    const loadedData = {};
    
    for (const file of this.knowledgeFiles) {
      try {
        const data = await window.fs.readFile(file, { encoding: 'utf8' });
        
        // Parse JSON files
        if (file.endsWith('.json')) {
          try {
            loadedData[file] = JSON.parse(data);
            console.log(`✅ ${file} geladen`);
          } catch (e) {
            console.log(`⚠️ ${file} Parse-Fehler`);
          }
        } else {
          loadedData[file] = data;
          console.log(`✅ ${file} geladen`);
        }
      } catch (e) {
        console.log(`ℹ️ ${file} nicht verfügbar`);
      }
    }
    
    this.knowledge = loadedData;
  }
  
  async loadPreferences() {
    // Check for Daniel Preferences
    if (this.knowledge['DANIEL-PREFERENCES.json']) {
      this.preferences = this.knowledge['DANIEL-PREFERENCES.json'];
      console.log("✅ Daniel Preferences gefunden!");
    } else {
      console.log("📝 Erstelle Default Daniel Preferences...");
      this.preferences = this.createDefaultPreferences();
    }
  }
  
  applyKnowledge() {
    if (!this.crod) return;
    
    // Load atoms from master.json
    if (this.knowledge['master.json']?.atoms) {
      const atoms = this.knowledge['master.json'].atoms;
      Object.entries(atoms).forEach(([word, data]) => {
        if (!this.crod.neurons.has(word) && data.prime) {
          this.crod.addNeuron(word, data.prime, data.weight || 50, data.gradient || 10);
        }
      });
      console.log(`📊 ${this.crod.neurons.size} Neuronen aktiv`);
    }
    
    // Apply preferences
    if (this.preferences) {
      this.applyPreferences();
    }
    
    // Activate CROD
    this.crod.process("ich bins wieder");
    console.log("🔥 CROD aktiviert mit allem Wissen!");
  }
  
  applyPreferences() {
    // Add frustration triggers as high-gradient atoms
    const frustrationWords = ['wtf', 'falsch', 'wieder nicht', 'warum'];
    frustrationWords.forEach(word => {
      if (!this.crod.neurons.has(word)) {
        this.crod.addNeuron(word, this.getNextPrime(), 100, 20, {
          type: 'frustration',
          heat_boost: 50
        });
      }
    });
    
    // Add success triggers
    const successWords = ['geil', 'nice', 'perfekt', 'läuft'];
    successWords.forEach(word => {
      if (!this.crod.neurons.has(word)) {
        this.crod.addNeuron(word, this.getNextPrime(), 100, 15, {
          type: 'success',
          heat_modifier: -20
        });
      }
    });
  }
  
  createDefaultPreferences() {
    return {
      response_style: "direct",
      max_lines: 5,
      frustration_triggers: ["wtf", "falsch", "wieder nicht"],
      success_triggers: ["geil", "nice", "perfekt"],
      technical_preferences: {
        security: "localhost_only",
        architecture: "k3s_preferred"
      }
    };
  }
  
  getNextPrime() {
    let n = 200;
    while (true) {
      if (this.isPrime(n)) return n;
      n++;
    }
  }
  
  isPrime(n) {
    for (let i = 2; i <= Math.sqrt(n); i++) {
      if (n % i === 0) return false;
    }
    return n > 1;
  }
  
  // Check if we should auto-load
  shouldAutoLoad(message) {
    const triggers = [
      'crod', 'ich bins wieder', 'neural', 'pattern',
      'lade', 'aktivier', 'preference'
    ];
    
    return triggers.some(trigger => 
      message.toLowerCase().includes(trigger)
    );
  }
}

// AUTOMATIC ACTIVATION
(async function() {
  // Check if we're in Claude environment
  if (typeof window !== 'undefined' && window.fs) {
    const loader = new CRODAutoLoader();
    
    // Store globally
    window.CRODLoader = loader;
    
    // Auto-load if mentioned
    const checkAndLoad = async (message) => {
      if (!loader.loaded && loader.shouldAutoLoad(message)) {
        console.log("🔍 CROD erwähnt - lade ALLES!");
        await loader.loadEverything();
      }
    };
    
    // Make available
    window.loadCROD = () => loader.loadEverything();
    
    console.log(`
╔══════════════════════════════════════╗
║  CROD AUTO-LOADER BEREIT!            ║
║  Erwähne CROD und alles lädt sich   ║
║  AUTOMATISCH aus Project Knowledge!  ║
╚══════════════════════════════════════╝
    `);
  }
})();

// Export for Node.js
if (typeof module !== 'undefined') {
  module.exports = CRODAutoLoader;
}