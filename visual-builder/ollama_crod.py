"""
OLLAMA CROD - Nutzt Ollama API (viel einfacher!)
"""

import requests
import json
from network import CRODNetwork
from database import get_database
import time

class OllamaCROD:
    """CROD mit Ollama Integration"""
    
    def __init__(self, model="llama2"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.network = CRODNetwork(name="Ollama-CROD")
        self.db = get_database()
        
    def test_ollama(self):
        """Test Ollama connection"""
        print("🦙 Testing Ollama...")
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json()
                print("✅ Ollama running! Available models:")
                for model in models.get('models', []):
                    print(f"   - {model['name']}")
                return True
        except:
            print("❌ Ollama not running!")
            print("   Start with: ollama serve")
        return False
        
    def query_ollama(self, prompt):
        """Query Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json()['response']
        except:
            pass
        return None
        
    def auto_train(self):
        """Auto-train CROD with Ollama"""
        if not self.test_ollama():
            return
            
        print(f"\n🎯 Training CROD with {self.model}...")
        
        # Build network
        thinker = self.network.add_atom("thinker", (0, 0))
        learner = self.network.add_atom("learner", (200, 0))
        memory = self.network.add_atom("memory", (400, 0))
        synthesizer = self.network.add_atom("synthesizer", (600, 0))
        
        # Connect
        self.network.connect_atoms(thinker.id, "thought", learner.id, "experience")
        self.network.connect_atoms(learner.id, "pattern", memory.id, "data")
        self.network.connect_atoms(memory.id, "retrieved", synthesizer.id, "concept_a")
        
        # Training loop
        prompts = [
            "What is consciousness?",
            "How do patterns emerge?",
            "Explain neural networks",
            "What is self-organization?"
        ]
        
        for prompt in prompts:
            print(f"\n📝 {prompt}")
            
            # Get Ollama response
            response = self.query_ollama(prompt)
            if response:
                print(f"🦙 {response[:100]}...")
                
                # Feed to CROD
                thinker.receive_input("context", {"llama": response})
                
                # Process
                for _ in range(5):
                    self.network.tick()
                    time.sleep(0.1)
                    
                stats = self.network.get_stats()
                print(f"   CROD: {stats['total_processed']} messages")
                
        # Save
        self.db.save_network(self.network.id, self.network.to_dict())
        print("\n✅ Training complete!")

if __name__ == "__main__":
    print("🚀 OLLAMA-CROD TRAINER")
    print("=" * 50)
    
    trainer = OllamaCROD()
    trainer.auto_train()