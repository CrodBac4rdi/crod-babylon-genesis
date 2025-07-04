# crod_chat.py - Chat Module
# JETZT: Simple responses → SPÄTER: AI Monster!

class CRODChat:
    def __init__(self, storage):
        self.storage = storage
        self.responses = {
            "pattern": "I have 73 locked patterns",
            "creator": "Created by Daniel Antonio Birkner",
            "investment": "270€/750€ monthly",
            "atoms": "Currently tracking {} atoms"
        }
        
    def process_message(self, message):
        """Simple keyword-based responses"""
        msg_lower = message.lower()
        
        # Check keywords
        for keyword, response in self.responses.items():
            if keyword in msg_lower:
                if keyword == "atoms":
                    # Get atom count from DB
                    count = self.storage.db.execute(
                        'SELECT COUNT(*) FROM atoms'
                    ).fetchone()[0]
                    return response.format(count)
                return response
                
        return "Processing..."

# Später wird das ein MONSTER mit:
# - Neural language model
# - Context awareness
# - Multi-turn dialogue
# - Semantic understanding
# - etc...