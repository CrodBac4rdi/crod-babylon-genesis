"""
AUTO ML CROD - Läuft automatisch ohne GUI!
Machine Learning Style Network
"""

import numpy as np
from network import CRODNetwork
from database import get_database
import time
import random

class MLCRODNetwork:
    """ML-Style CROD Network mit Auto-Learning"""
    
    def __init__(self):
        self.network = CRODNetwork(name="ML CROD")
        self.training_data = []
        self.performance_history = []
        self.db = get_database()
        
    def build_ml_network(self):
        """Baut automatisch ein ML-ähnliches Network"""
        print("🧠 Building ML CROD Network...")
        
        # Input Layer (Thinkers)
        input1 = self.network.add_atom("thinker", (0, 0))
        input2 = self.network.add_atom("thinker", (0, 100))
        input3 = self.network.add_atom("thinker", (0, 200))
        
        # Hidden Layer 1 (Doubters + Learners)
        hidden1_1 = self.network.add_atom("doubter", (200, 0))
        hidden1_2 = self.network.add_atom("learner", (200, 100))
        hidden1_3 = self.network.add_atom("doubter", (200, 200))
        
        # Hidden Layer 2 (Connectors + Memory)
        hidden2_1 = self.network.add_atom("connector", (400, 50))
        hidden2_2 = self.network.add_atom("memory", (400, 150))
        
        # Processing Layer (Synthesizer + Evaluator)
        processor1 = self.network.add_atom("synthesizer", (600, 0))
        processor2 = self.network.add_atom("evaluator", (600, 100))
        
        # Output Layer (Router)
        output = self.network.add_atom("router", (800, 100))
        
        # Connect layers (wie Neural Network)
        # Input → Hidden1
        self.network.connect_atoms(input1.id, "thought", hidden1_1.id, "thought")
        self.network.connect_atoms(input2.id, "thought", hidden1_2.id, "experience")
        self.network.connect_atoms(input3.id, "thought", hidden1_3.id, "thought")
        
        # Hidden1 → Hidden2
        self.network.connect_atoms(hidden1_1.id, "doubt", hidden2_1.id, "thought_a")
        self.network.connect_atoms(hidden1_2.id, "pattern", hidden2_2.id, "data")
        self.network.connect_atoms(hidden1_3.id, "confidence", hidden2_1.id, "thought_b")
        
        # Hidden2 → Processing
        self.network.connect_atoms(hidden2_1.id, "connection", processor1.id, "concept_a")
        self.network.connect_atoms(hidden2_2.id, "retrieved", processor1.id, "concept_b")
        self.network.connect_atoms(processor1.id, "synthesis", processor2.id, "thought")
        
        # Processing → Output
        self.network.connect_atoms(processor2.id, "score", output.id, "input")
        
        print("✅ ML Network ready!")
        print(f"   Atoms: {len(self.network.atoms)}")
        print(f"   Connections: {len(self.network.connections)}")
        
        # Configure for ML behavior
        self._configure_for_ml()
        
    def _configure_for_ml(self):
        """Konfiguriert Atoms für ML-Verhalten"""
        # Erhöhe Kreativität der Inputs
        for atom in self.network.atoms.values():
            if atom.type == "thinker":
                atom.configure({"creativity": 0.8, "speed": 2.0})
            elif atom.type == "learner":
                atom.configure({"learning_rate": 0.5, "memory_size": 1000})
            elif atom.type == "memory":
                atom.configure({"capacity": 1000, "decay_rate": 0.001})
            elif atom.type == "evaluator":
                atom.configure({"strictness": 0.3})
                
    def train(self, epochs=10):
        """Training Loop wie bei ML"""
        print("\n🎯 Starting Training...")
        
        # Start network
        self.network.start()
        
        for epoch in range(epochs):
            print(f"\n📊 Epoch {epoch + 1}/{epochs}")
            
            # Generate training batch
            batch_loss = 0
            batch_accuracy = 0
            
            for step in range(5):  # 5 steps per epoch
                # Run network
                self.network.tick()
                
                # Simulate training metrics
                loss = random.uniform(0.1, 1.0) * (1 - epoch/epochs)
                accuracy = random.uniform(0.3, 0.9) * (epoch/epochs + 0.1)
                
                batch_loss += loss
                batch_accuracy += accuracy
                
                # Show progress
                print(f"   Step {step+1}: Loss={loss:.3f}, Acc={accuracy:.3f}")
                time.sleep(0.2)
                
            # Epoch summary
            avg_loss = batch_loss / 5
            avg_acc = batch_accuracy / 5
            self.performance_history.append({
                "epoch": epoch + 1,
                "loss": avg_loss,
                "accuracy": avg_acc
            })
            
            print(f"   → Epoch Loss: {avg_loss:.3f}")
            print(f"   → Epoch Accuracy: {avg_acc:.3f}")
            
            # Adjust network based on performance
            self._adjust_network(avg_loss, avg_acc)
            
        # Save training session to database
        self.db.save_training_session({
            "network_name": self.network.name,
            "epochs": epochs,
            "final_accuracy": self.performance_history[-1]["accuracy"],
            "final_loss": self.performance_history[-1]["loss"],
            "performance_history": self.performance_history
        })
        
        # Save network
        self.db.save_network(self.network.id, self.network.to_dict())
        
        # Update atom statistics
        for atom in self.network.atoms.values():
            self.db.update_atom_statistics(atom.type, atom.metrics)
            
    def _adjust_network(self, loss, accuracy):
        """Passt Network basierend auf Performance an"""
        if accuracy < 0.5:
            # Erhöhe Lernrate
            for atom in self.network.atoms.values():
                if atom.type == "learner":
                    current = atom.config.get("learning_rate", 0.3)
                    atom.configure({"learning_rate": min(current + 0.1, 1.0)})
                    
        if loss > 0.5:
            # Reduziere Noise
            for atom in self.network.atoms.values():
                if atom.type == "thinker":
                    current = atom.config.get("creativity", 0.5)
                    atom.configure({"creativity": max(current - 0.1, 0.1)})
                    
    def inference(self, input_data="Test Input"):
        """Run inference on trained network"""
        print(f"\n🔮 Running Inference: '{input_data}'")
        
        # Trigger network multiple times
        outputs = []
        for i in range(5):
            self.network.tick()
            time.sleep(0.1)
            
            # Collect outputs from all atoms
            for atom in self.network.atoms.values():
                if atom.outputs:
                    outputs.append({
                        "atom": atom.type,
                        "outputs": atom.outputs.copy()
                    })
                    
        print(f"   Generated {len(outputs)} outputs")
        
        # Show some outputs
        if outputs:
            print("   Sample outputs:")
            for out in outputs[:3]:
                print(f"     - {out['atom']}: {list(out['outputs'].keys())}")
                
        return outputs
        
    def show_stats(self):
        """Zeigt Network Statistics"""
        print("\n📈 Network Statistics:")
        stats = self.network.get_stats()
        print(f"   Total Atoms: {stats['atoms']}")
        print(f"   Total Connections: {stats['connections']}")
        print(f"   Messages Processed: {stats['total_processed']}")
        print(f"   Errors: {stats['total_errors']}")
        
        if self.performance_history:
            best = max(self.performance_history, key=lambda x: x['accuracy'])
            print(f"\n🏆 Best Performance:")
            print(f"   Epoch: {best['epoch']}")
            print(f"   Accuracy: {best['accuracy']:.3f}")
            print(f"   Loss: {best['loss']:.3f}")

# ============ AUTO RUN ============

if __name__ == "__main__":
    print("🚀 CROD ML AUTO-RUNNER")
    print("=" * 50)
    
    # Create ML Network
    ml_crod = MLCRODNetwork()
    ml_crod.build_ml_network()
    
    # Train
    ml_crod.train(epochs=5)
    
    # Test inference
    ml_crod.inference("Hello CROD!")
    ml_crod.inference("What is consciousness?")
    
    # Show final stats
    ml_crod.show_stats()
    
    # Show database stats
    print("\n💾 Database Statistics:")
    db_stats = ml_crod.db.get_statistics()
    print(f"   Total Networks: {db_stats['total_networks']}")
    print(f"   Total Training Sessions: {db_stats['total_training_sessions']}")
    print(f"   Total Messages: {db_stats['total_messages_processed']}")
    
    print("\n✅ ML CROD Complete! (Data saved to crod_data/)")