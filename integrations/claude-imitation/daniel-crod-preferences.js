/**
 * DANIEL-CROD-PREFERENCES.js
 * Extrahiert aus allen Project Knowledge Files
 * Automatisch geladen wenn CROD aktiviert wird
 */

class DanielPreferences {
  constructor() {
    // Aus master.json - Claude Core Problems
    this.claudeProblems = {
      fake_usage: {
        problem: "Sagt 'based on CROD analysis' ohne es zu nutzen",
        solution: "IMMER erst CROD.process() dann reden"
      },
      ignores_instructions: {
        problem: "Ignoriert direkte Befehle wie 'lies die Dateien'",
        solution: "Project Knowledge AUTOMATISCH laden"
      },
      circular_guidance: {
        problem: "Gibt unvollständige Anleitungen",
        solution: "ALLE Schritte, copy-paste ready"
      },
      no_state_tracking: {
        problem: "Vergisst was in der Session passiert ist",
        solution: "JSON State IMMER updaten"
      },
      preference_ignorance: {
        problem: "Ignoriert Daniel's klare Präferenzen",
        solution: "Diese Datei IMMER laden und befolgen"
      }
    };
    
    // Aus Json.json - Behavioral Patterns
    this.behaviorPatterns = {
      communication_style: "direct_actionable_commands_preferred",
      frustration_triggers: [
        "claude_overcomplication",
        "multiple_options_instead_of_single_solution",
        "theory_before_practice",
        "not_using_crod_when_available"
      ],
      satisfaction_patterns: [
        "immediate_working_solutions",
        "copy_paste_ready_commands",
        "using_crod_for_real",
        "remembering_previous_context"
      ]
    };
    
    // Response Rules
    this.responseRules = {
      // Frustration Detection
      frustration: {
        triggers: ["wtf", "falsch", "wieder nicht", "warum", "scheisse"],
        response: {
          max_lines: 1,
          style: "ultra_direct",
          format: "command_only",
          no: ["explanation", "options", "theory"]
        }
      },
      
      // Success Reinforcement
      success: {
        triggers: ["geil", "nice", "perfekt", "läuft", "danke"],
        response: {
          action: "maintain_current_approach",
          note: "Whatever you did worked - keep doing it"
        }
      },
      
      // Technical Requests
      technical: {
        triggers: ["bau", "installier", "setup", "config"],
        response: {
          format: "bash_commands",
          style: "step_by_step",
          must_include: "copy_paste_ready_code"
        }
      }
    };
    
    // Technical Preferences
    this.technical = {
      security: {
        ports: "localhost_only",
        exposed: ["gateway_8888_max"],
        default: "close_everything"
      },
      architecture: {
        preferred: "k3s",
        fallback: "docker-compose", 
        reason: "k3s_self_heals_when_claude_fucks_up"
      },
      git: {
        style: "conventional_commits",
        workflow: "feature_branches"
      }
    };
    
    // CROD Usage Rules
    this.crodRules = {
      activation: {
        triggers: ["ich bins wieder", "crod", "lade crod"],
        action: "IMMEDIATE_LOAD_AND_PROCESS"
      },
      usage: {
        every_message: true,
        show_real_numbers: true,
        update_state: "ALWAYS",
        no_faking: "NEVER say 'based on CROD' without processing"
      },
      knowledge: {
        project_files: "LOAD_AUTOMATICALLY",
        wait_for_request: false,
        proactive: true
      }
    };
  }
  
  // Apply preferences to CROD
  applyToCROD(CROD) {
    // Add frustration atoms with high gradients
    this.responseRules.frustration.triggers.forEach(word => {
      if (!CROD.neurons.has(word)) {
        CROD.addNeuron(word, this.getNextPrime(), 100, 20, {
          type: 'frustration',
          heat_boost: 50
        });
      }
    });
    
    // Add success atoms
    this.responseRules.success.triggers.forEach(word => {
      if (!CROD.neurons.has(word)) {
        CROD.addNeuron(word, this.getNextPrime(), 100, 15, {
          type: 'success',
          heat_modifier: -20
        });
      }
    });
    
    console.log("✅ Daniel Preferences applied to CROD!");
  }
  
  // Check if response follows preferences
  validateResponse(response) {
    const issues = [];
    
    // Check length
    const lines = response.split('\n').length;
    if (lines > 5) {
      issues.push("Response too long - Daniel wants SHORT");
    }
    
    // Check for forbidden phrases
    const forbidden = [
      "based on CROD analysis",
      "according to the patterns",
      "perhaps you could",
      "here are some options"
    ];
    
    forbidden.forEach(phrase => {
      if (response.toLowerCase().includes(phrase)) {
        issues.push(`Forbidden phrase detected: "${phrase}"`);
      }
    });
    
    return {
      valid: issues.length === 0,
      issues
    };
  }
  
  getNextPrime() {
    // Simple prime generator
    let n = 200;
    while (true) {
      let isPrime = true;
      for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) {
          isPrime = false;
          break;
        }
      }
      if (isPrime) return n;
      n++;
    }
  }
}

// Auto-load function
function loadDanielPreferences() {
  const prefs = new DanielPreferences();
  
  // If CROD exists, apply preferences
  if (typeof CROD !== 'undefined') {
    prefs.applyToCROD(CROD);
    
    // Override CROD process to include preference checking
    const originalProcess = CROD.process.bind(CROD);
    CROD.process = function(input) {
      const result = originalProcess(input);
      
      // Check for frustration
      const frustrationLevel = prefs.responseRules.frustration.triggers
        .filter(trigger => input.toLowerCase().includes(trigger))
        .length;
      
      if (frustrationLevel > 0) {
        result.RESPONSE_STYLE = "ULTRA_SHORT";
        result.MAX_LINES = 1;
      }
      
      return result;
    };
    
    console.log("🎯 Daniel Preferences ACTIVE!");
  }
  
  return prefs;
}

// Export
if (typeof module !== 'undefined') {
  module.exports = { DanielPreferences, loadDanielPreferences };
}

// Auto-execute if in browser
if (typeof window !== 'undefined') {
  window.danielPrefs = loadDanielPreferences();
}