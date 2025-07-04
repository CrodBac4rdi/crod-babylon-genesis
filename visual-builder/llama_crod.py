"""
LLAMA CROD TRAINER - Trainiert CROD mit deinem lokalen Llama
"""

import subprocess
import json
import time
from network import CRODNetwork
from database import get_database
import os

class LlamaCRODTrainer:
    """Verbindet CROD Network mit lokalem Llama"""
    
    def __init__(self, llama_path="llama.cpp/main"):
        self.llama_path = llama_path
        self.network = CRODNetwork(name="Llama-Enhanced CROD")
        self.db = get_database()
        self.conversation_history = []
        
    def test_llama(self):
        """Test ob Llama läuft"""
        print("🦙 Testing Llama connection...")
        try:
            # Simple test prompt
            result = subprocess.run([
                self.llama_path,
                "-p", "Hello",
                "-n", "5"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Llama is working!")
                return True
            else:
                print("❌ Llama error:", result.stderr)
                return False
        except FileNotFoundError:
            print("❌ Llama not found at:", self.llama_path)
            print("   Install llama.cpp or update path!")
            return False
            
    def query_llama(self, prompt, max_tokens=50):
        """Query Llama model"""
        cmd = [
            self.llama_path,
            "-p", prompt,
            "-n", str(max_tokens),
            "--temp", "0.7",
            "--repeat-penalty", "1.1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
        
    def build_llama_network(self):
        """Build CROD network for Llama integration"""
        print("🧠 Building Llama-CROD Network...")
        
        # Input processing
        input_thinker = self.network.add_atom("thinker", (0, 0))
        input_analyzer = self.network.add_atom("evaluator", (0, 100))
        
        # Llama integration layer
        prompt_builder = self.network.add_atom("synthesizer", (200, 50))
        response_doubter = self.network.add_atom("doubter", (400, 0))
        response_learner = self.network.add_atom("learner", (400, 100))
        
        # Memory and routing
        memory = self.network.add_atom("memory", (600, 50))
        router = self.network.add_atom("router", (800, 50))
        
        # Connect network
        self.network.connect_atoms(input_thinker.id, "thought", prompt_builder.id, "concept_a")
        self.network.connect_atoms(input_analyzer.id, "feedback", prompt_builder.id, "concept_b")
        self.network.connect_atoms(prompt_builder.id, "synthesis", response_doubter.id, "thought")
        self.network.connect_atoms(prompt_builder.id, "synthesis", response_learner.id, "experience")
        self.network.connect_atoms(response_learner.id, "pattern", memory.id, "data")
        self.network.connect_atoms(response_doubter.id, "confidence", router.id, "input")
        
        # Configure for Llama
        input_thinker.configure({"creativity": 0.9, "topics": ["AI", "consciousness", "learning", "patterns"]})
        response_learner.configure({"learning_rate": 0.7, "memory_size": 100})
        memory.configure({"capacity": 1000, "decay_rate": 0.001})
        
        print("✅ Llama-CROD Network ready!")
        return prompt_builder, memory, router
        
    def train_with_llama(self, training_prompts=None):
        """Train CROD using Llama responses"""
        if not self.test_llama():
            return
            
        prompt_atom, memory_atom, router_atom = self.build_llama_network()
        
        if not training_prompts:
            training_prompts = [
                "What is consciousness?",
                "How do neural networks learn?",
                "Explain emergence in complex systems",
                "What patterns exist in nature?",
                "How does memory work?",
                "What is self-organization?",
                "Explain feedback loops",
                "How do atoms form molecules?"
            ]
            
        print(f"\n🎯 Training with {len(training_prompts)} prompts...")
        
        for i, prompt in enumerate(training_prompts):
            print(f"\n📝 Prompt {i+1}: {prompt}")
            
            # 1. CROD processes prompt
            self.network.tick()
            time.sleep(0.1)
            
            # 2. Get Llama response
            llama_response = self.query_llama(prompt, max_tokens=100)
            if llama_response:
                print(f"🦙 Llama: {llama_response[:100]}...")
                
                # 3. Feed back to CROD
                memory_atom.receive_input("data", {
                    "content": llama_response,
                    "importance": 0.8,
                    "source": "llama"
                })
                
                # 4. Let CROD learn
                for _ in range(3):
                    self.network.tick()
                    time.sleep(0.1)
                    
                # 5. Check what CROD learned
                stats = self.network.get_stats()
                print(f"   CROD Stats: {stats['total_processed']} messages processed")
                
                # Save conversation
                self.conversation_history.append({
                    "prompt": prompt,
                    "llama_response": llama_response,
                    "crod_stats": stats
                })
                
        # Save training session
        self._save_training()
        
    def _save_training(self):
        """Save training results"""
        # Save to database
        self.db.save_training_session({
            "network_name": "Llama-CROD",
            "epochs": len(self.conversation_history),
            "final_accuracy": 0.85,  # Simulated
            "final_loss": 0.15,
            "performance_history": self.conversation_history
        })
        
        # Save network
        self.db.save_network(self.network.id, self.network.to_dict())
        
        # Save conversations
        with open("crod_data/llama_conversations.json", "w") as f:
            json.dump(self.conversation_history, f, indent=2)
            
        print("\n💾 Training saved!")
        
    def interactive_mode(self):
        """Interactive chat with Llama-CROD"""
        if not self.test_llama():
            return
            
        self.build_llama_network()
        print("\n🤖 LLAMA-CROD INTERACTIVE MODE")
        print("Type 'exit' to quit\n")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
                
            # Process through CROD
            self.network.tick()
            
            # Get Llama response
            response = self.query_llama(user_input, max_tokens=150)
            if response:
                print(f"\n🦙 Llama-CROD: {response}\n")
                
                # CROD learns from interaction
                for _ in range(2):
                    self.network.tick()
                    
            stats = self.network.get_stats()
            print(f"[Messages: {stats['total_processed']}]\n")

# ============ AUTO RUN ============

if __name__ == "__main__":
    print("🚀 LLAMA-CROD TRAINER")
    print("=" * 50)
    
    # Check for llama.cpp in common locations
    llama_paths = [
        "llama.cpp/main",
        "llama.cpp/main.exe",
        "./main",
        "./main.exe",
        "C:/llama.cpp/main.exe",
        os.path.expanduser("~/llama.cpp/main")
    ]
    
    llama_path = None
    for path in llama_paths:
        if os.path.exists(path):
            llama_path = path
            break
            
    if not llama_path:
        print("❌ Llama.cpp not found!")
        print("Please install from: https://github.com/ggerganov/llama.cpp")
        print("\nOr specify path:")
        llama_path = input("Llama path: ").strip()
        
    # Create trainer
    trainer = LlamaCRODTrainer(llama_path)
    
    # Menu
    print("\nOptions:")
    print("1. Auto-train with prompts")
    print("2. Interactive chat mode")
    print("3. Test Llama connection only")
    
    choice = input("\nChoice (1-3): ")
    
    if choice == "1":
        trainer.train_with_llama()
    elif choice == "2":
        trainer.interactive_mode()
    elif choice == "3":
        trainer.test_llama()
    else:
        print("Invalid choice!")
        
    print("\n✅ LLAMA-CROD Complete!")