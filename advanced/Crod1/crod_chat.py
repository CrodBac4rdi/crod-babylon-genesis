# crod_chat.py - Chat Module
# Version 1.1 - Enhanced Chat System

import random
from datetime import datetime

class CRODChat:
    def __init__(self, storage):
        """Initialize chat module with storage reference"""
        self.storage = storage
        self.context = []  # Conversation history
        self.mood = "neutral"  # Track mood
        
        # Response templates
        self.responses = {
            "pattern": [
                "I have 73 locked patterns in my system",
                "Patterns are the core of CROD Mental Systems",
                "Each pattern represents a learned behavior",
                "73 patterns locked, but always learning more"
            ],
            "creator": [
                "Created by Daniel Antonio Birkner",
                "Daniel built me with 270€/750€ monthly investment",
                "My creator spent 5695.6h perfecting the system",
                "Daniel's philosophy: 0.0001% improvement matters"
            ],
            "investment": [
                "270€/750€ monthly for AI development",
                "Every euro invested improves the system",
                "0.0001% improvement matters!",
                "The investment shows in every pattern learned"
            ],
            "atoms": [
                "Currently tracking {} atoms in the database",
                "Atoms are the fundamental units of knowledge",
                "{} atoms and growing!",
                "Each atom has weight and meaning"
            ],
            "help": [
                "I can help you understand CROD Mental Systems",
                "Ask me about patterns, atoms, or my creator",
                "Type 'stats' to see system statistics",
                "I'm here to assist with error patterns and more"
            ],
            "greeting": [
                "Hello! CROD Mental Systems ready",
                "Greetings! How can I assist you?",
                "CROD here, what would you like to know?",
                "Welcome to CROD Mental Systems!"
            ],
            "philosophy": [
                "Tech IS the game - bugs are bosses to defeat",
                "Every error is loot, every fix is XP",
                "Pattern recognition is our superpower",
                "We build, we learn, we evolve"
            ],
            "ml": [
                "∂L/∂z = 0.6187 - the gradients flow through me",
                "Vanishing gradients? Not in CROD!",
                "The game cards teach ML concepts through play",
                "Neural networks are just pattern matchers at heart"
            ]
        }
        
        # Daniel's speech responses
        self.daniel_responses = {
            "ich halt": "Ah, Daniel's signature phrase!",
            "bruh": "Frustration detected... I understand",
            "...": "Thinking mode activated",
            "yes yes yes": "Excitement level: Maximum!",
            "ach scheiße": "Realization moment captured"
        }
        
        # Technical responses
        self.tech_responses = {
            "sql": "SQL queries power our data layer",
            "python": "Built with Python for flexibility",
            "rust": "Rust will handle pattern matching at 10,000/sec",
            "ml": "Machine learning helps patterns evolve",
            "gradient": "∂L/∂z = 0.6187 - the gradients flow"
        }
        
    def process_message(self, message):
        """Process chat message and generate response"""
        msg_lower = message.lower()
        
        # Add to context
        self.context.append(message)
        if len(self.context) > 10:
            self.context.pop(0)
            
        # Mood detection based on Daniel patterns
        if any(word in msg_lower for word in ["bruh", "ach", "scheiße"]):
            self.mood = "frustrated"
        elif "yes yes yes" in msg_lower or "!!!" in message:
            self.mood = "excited"
        elif "..." in message:
            self.mood = "thinking"
            
        # Check for Daniel's speech patterns
        for pattern, response in self.daniel_responses.items():
            if pattern in msg_lower:
                return self._mood_adjusted_response(response)
                
        # Check for technical terms
        for term, response in self.tech_responses.items():
            if term in msg_lower:
                return response
                
        # Check for keyword matches
        for keyword, responses in self.responses.items():
            if keyword in msg_lower:
                response = random.choice(responses)
                
                # Handle dynamic content
                if keyword == "atoms" and "{}" in response:
                    count = self.storage.db.execute(
                        'SELECT COUNT(*) FROM atoms'
                    ).fetchone()[0]
                    return response.format(count)
                    
                return self._mood_adjusted_response(response)
                
        # Context-aware responses
        if "error" in msg_lower and "fix" in msg_lower:
            return "Every error has a pattern, every pattern has a fix. Which error are you facing?"
            
        if "learn" in msg_lower or "teach" in msg_lower:
            return "CROD learns from every interaction. Show me what you want to teach!"
            
        if "game" in msg_lower or "card" in msg_lower:
            return random.choice(self.responses["ml"])
            
        # Check for specific questions
        if "who" in msg_lower and ("are" in msg_lower or "created" in msg_lower):
            return random.choice(self.responses["creator"])
            
        if "what" in msg_lower and "crod" in msg_lower:
            return "CROD Mental Systems: Create Read Observe Delete - A pattern recognition and compression system that learns from every interaction"
            
        if "how many" in msg_lower:
            if "pattern" in msg_lower:
                return "73 locked patterns and growing! Each one battle-tested"
            elif "atom" in msg_lower:
                count = self.storage.db.execute(
                    'SELECT COUNT(*) FROM atoms'
                ).fetchone()[0]
                return f"Currently {count} atoms in the system, each one meaningful"
                
        # Greeting detection
        greetings = ["hello", "hi", "hey", "greetings", "servus", "moin"]
        if any(greet in msg_lower for greet in greetings):
            return random.choice(self.responses["greeting"])
            
        # Philosophy questions
        if any(word in msg_lower for word in ["philosophy", "meaning", "why", "purpose"]):
            return random.choice(self.responses["philosophy"])
            
        # Default responses based on mood
        if self.mood == "frustrated":
            return "I sense frustration. Let's debug this together!"
        elif self.mood == "excited":
            return "Your excitement is contagious! What discovery did you make?"
        elif self.mood == "thinking":
            return "Hmm... processing that thought pattern..."
        else:
            default_responses = [
                "Processing your input...",
                "Interesting pattern detected. Tell me more.",
                "CROD Mental Systems is analyzing...",
                "Every message teaches me something new."
            ]
            return random.choice(default_responses)
            
    def _mood_adjusted_response(self, response):
        """Adjust response based on current mood"""
        if self.mood == "excited":
            return response + " 🚀"
        elif self.mood == "frustrated":
            return response + " - Let's fix this!"
        elif self.mood == "thinking":
            return response + "..."
        return response
        
    def get_conversation_stats(self):
        """Get chat statistics"""
        # This could track conversation history in the future
        return {
            "responses_available": sum(len(r) for r in self.responses.values()),
            "daniel_patterns": len(self.daniel_responses),
            "tech_terms": len(self.tech_responses)
        }

# Test functionality
if __name__ == "__main__":
    # Mock storage for testing
    class MockStorage:
        class MockDB:
            def execute(self, query):
                class Result:
                    def fetchone(self):
                        return [42]  # Mock atom count
                return Result()
        
        def __init__(self):
            self.db = self.MockDB()
    
    chat = CRODChat(MockStorage())
    
    # Test messages
    test_messages = [
        "Hello CROD",
        "Who created you?",
        "Tell me about patterns",
        "How many atoms?",
        "ich halt bruh",
        "What is CROD?",
        "gradient descent"
    ]
    
    print("Testing CROD Chat:")
    for msg in test_messages:
        response = chat.process_message(msg)
        print(f"\nYou: {msg}")
        print(f"CROD: {response}")