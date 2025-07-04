# crod_patterns.py - Pattern Detection Module
# JETZT: 50 Zeilen → SPÄTER: 2000+ Zeilen Monster!

class CRODPatterns:
    def __init__(self):
        # Die 73 locked patterns
        self.locked_patterns = {
            "JSON_001": "JSON syntax error",
            "DOM_001": "DOM access null", 
            "TYPE_001": "Type mismatch",
            "ASYNC_001": "Async without await",
            # ... später 73 patterns
        }
        
        # Daniel's speech patterns
        self.daniel_patterns = {
            "...": "THINKING",
            "ich halt": "SIGNATURE",
            "bruh": "FRUSTRATION",
            "yes yes yes": "EXCITEMENT",
            "ach scheiße": "REALIZATION"
        }
        
    def detect(self, text):
        """Detect all patterns in text"""
        found = []
        
        # Check Daniel patterns
        for pattern, name in self.daniel_patterns.items():
            if pattern in text.lower():
                found.append(f"DANIEL_{name}")
                
        # Check error patterns  
        for pattern_id in self.locked_patterns:
            if pattern_id in text:
                found.append(pattern_id)
                
        return found

# Später wird das ein MONSTER mit:
# - ML pattern learning
# - Markov chains
# - Pattern evolution
# - 73 locked patterns mit regex
# - Pattern scoring
# - etc...