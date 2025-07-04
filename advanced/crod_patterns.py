# crod_patterns.py - Pattern Detection Module
# Version 1.1 - Enhanced with more patterns

class CRODPatterns:
    def __init__(self):
        """Initialize pattern dictionaries"""
        # Error patterns (will grow to 73)
        self.locked_patterns = {
            "JSON_001": "JSON syntax error",
            "DOM_001": "DOM access null", 
            "TYPE_001": "Type mismatch",
            "ASYNC_001": "Async without await",
            "VAR_001": "Variable undefined",
            "ARR_001": "Array index out of bounds",
            "SEC_001": "Security vulnerability",
            "STORE_001": "Storage access error"
        }
        
        # Daniel's speech patterns
        self.daniel_patterns = {
            "...": "THINKING",
            "ich halt": "SIGNATURE",
            "bruh": "FRUSTRATION",
            "yes yes yes": "EXCITEMENT",
            "ach scheiße": "REALIZATION",
            "meh": "EVALUATION",
            "hmm": "PONDERING",
            "idk": "UNCERTAINTY",
            "tbh": "HONESTY",
            "lol": "AMUSEMENT",
            "wtf": "CONFUSION",
            "holy shit": "SURPRISE"
        }
        
        # ML/Game card patterns
        self.game_cards = {
            "RECURRENT_LOOP": "RNN Pattern",
            "VEIL_OF_VANISHING": "Vanishing Gradient",
            "MIRROR_OF_GRADIENTS": "Backpropagation",
            "CRYPT_OF_NUMERICAL_TRUTH": "Numerical Verification",
            "FORWARD_ECHOES": "Forward Pass"
        }
        
        # Technical patterns
        self.tech_patterns = {
            "gradient": "ML_GRADIENT",
            "backpropagation": "ML_BACKPROP",
            "neural": "ML_NEURAL",
            "SELECT": "SQL_QUERY",
            "INSERT": "SQL_INSERT",
            "UPDATE": "SQL_UPDATE",
            "DELETE": "SQL_DELETE"
        }
        
    def detect(self, text):
        """Detect all patterns in text"""
        found = []
        text_lower = text.lower()
        
        # Check Daniel patterns
        for pattern, name in self.daniel_patterns.items():
            if pattern.lower() in text_lower:
                found.append(f"DANIEL_{name}")
                
        # Check error patterns (case sensitive)
        for pattern_id in self.locked_patterns:
            if pattern_id in text:
                found.append(pattern_id)
                
        # Check game cards
        for card in self.game_cards:
            if card in text.upper():
                found.append(f"GAME_CARD_{card}")
                
        # Check technical patterns
        for pattern, name in self.tech_patterns.items():
            if pattern.lower() in text_lower:
                found.append(name)
                
        return found
    
    def get_pattern_info(self, pattern_id):
        """Get information about a specific pattern"""
        # Check all dictionaries
        if pattern_id in self.locked_patterns:
            return {
                'type': 'error_pattern',
                'description': self.locked_patterns[pattern_id],
                'locked': True
            }
        
        # Check Daniel patterns
        for pattern, name in self.daniel_patterns.items():
            if f"DANIEL_{name}" == pattern_id:
                return {
                    'type': 'daniel_speech',
                    'trigger': pattern,
                    'meaning': name
                }
                
        # Check game cards
        for card, desc in self.game_cards.items():
            if f"GAME_CARD_{card}" == pattern_id:
                return {
                    'type': 'game_card',
                    'card': card,
                    'description': desc
                }
                
        return None
    
    def get_stats(self):
        """Get pattern statistics"""
        return {
            'locked_patterns': len(self.locked_patterns),
            'daniel_patterns': len(self.daniel_patterns),
            'game_cards': len(self.game_cards),
            'tech_patterns': len(self.tech_patterns),
            'total': len(self.locked_patterns) + len(self.daniel_patterns) + 
                    len(self.game_cards) + len(self.tech_patterns)
        }

# Test functionality
if __name__ == "__main__":
    patterns = CRODPatterns()
    
    # Test detection
    test_texts = [
        "ich halt... bruh JSON_001",
        "SELECT * FROM atoms WHERE gradient > 0",
        "RECURRENT_LOOP activated, yes yes yes!",
        "wtf is this ASYNC_001 error?"
    ]
    
    for text in test_texts:
        found = patterns.detect(text)
        print(f"\nText: '{text}'")
        print(f"Patterns: {found}")
        
    # Show stats
    stats = patterns.get_stats()
    print(f"\nPattern Stats: {stats}")