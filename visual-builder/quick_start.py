"""
QUICK START - Verschiedene vorgefertigte CROD Networks
"""

from network import CRODNetwork
import time

def doubt_loop():
    """Classic Doubt Loop"""
    print("🌀 DOUBT LOOP NETWORK")
    net = CRODNetwork("Doubt Loop")
    
    # Build
    t = net.add_atom("thinker", (0, 0))
    d = net.add_atom("doubter", (200, 0))
    e = net.add_atom("evaluator", (400, 0))
    
    # Connect
    net.connect_atoms(t.id, "thought", d.id, "thought")
    net.connect_atoms(d.id, "doubt", e.id, "thought")
    
    # Run
    for i in range(5):
        print(f"\nCycle {i+1}:")
        net.tick()
        time.sleep(0.5)
        
        # Show output
        if t.outputs:
            print(f"  Thought: {t.outputs.get('thought', {}).get('content', 'None')}")
        if d.outputs:
            print(f"  Doubt Level: {d.outputs.get('doubt', {}).get('doubt_level', 0):.2f}")
            
def memory_network():
    """Memory Storage Network"""
    print("💾 MEMORY NETWORK")
    net = CRODNetwork("Memory System")
    
    # Build
    t1 = net.add_atom("thinker", (0, 0))
    t2 = net.add_atom("thinker", (0, 100))
    m = net.add_atom("memory", (200, 50))
    s = net.add_atom("synthesizer", (400, 50))
    
    # Connect
    net.connect_atoms(t1.id, "thought", m.id, "data")
    net.connect_atoms(t2.id, "thought", s.id, "concept_a")
    net.connect_atoms(m.id, "retrieved", s.id, "concept_b")
    
    # Configure
    t1.configure({"creativity": 0.9})
    t2.configure({"creativity": 0.7})
    m.configure({"capacity": 50})
    
    # Run
    for i in range(7):
        print(f"\nCycle {i+1}:")
        net.tick()
        time.sleep(0.3)
        
        if s.outputs and s.outputs.get("synthesis"):
            print(f"  Synthesis: {s.outputs['synthesis'].get('content', 'None')}")
            
def learning_chain():
    """Learning Pattern Chain"""
    print("📚 LEARNING CHAIN")
    net = CRODNetwork("Learning Chain")
    
    # Build  
    t = net.add_atom("thinker", (0, 0))
    l = net.add_atom("learner", (200, 0))
    m = net.add_atom("memory", (400, 0))
    e = net.add_atom("evaluator", (600, 0))
    
    # Connect
    net.connect_atoms(t.id, "thought", l.id, "experience")
    net.connect_atoms(l.id, "pattern", m.id, "data")
    net.connect_atoms(l.id, "knowledge", e.id, "thought")
    
    # Configure for fast learning
    l.configure({"learning_rate": 0.8, "memory_size": 20})
    
    # Run
    patterns_found = 0
    for i in range(10):
        print(f"\nCycle {i+1}:")
        net.tick()
        
        if l.outputs and l.outputs.get("pattern"):
            patterns_found += 1
            print(f"  ✨ Pattern found! Type: {l.outputs['pattern'].get('type', 'unknown')}")
        else:
            print(f"  Learning... (Patterns found: {patterns_found})")
            
        time.sleep(0.2)

# ============ MENU ============

def main():
    print("🚀 CROD QUICK START")
    print("=" * 50)
    print("\nWähle ein Network:")
    print("1. Doubt Loop (Selbstzweifel)")
    print("2. Memory Network (Speicher-System)")
    print("3. Learning Chain (Lern-Kette)")
    print("4. ML Network (Machine Learning Style)")
    print("5. Alle der Reihe nach")
    
    choice = input("\nDeine Wahl (1-5): ")
    
    if choice == "1":
        doubt_loop()
    elif choice == "2":
        memory_network()
    elif choice == "3":
        learning_chain()
    elif choice == "4":
        from auto_ml_network import MLCRODNetwork
        ml = MLCRODNetwork()
        ml.build_ml_network()
        ml.train(epochs=3)
    elif choice == "5":
        doubt_loop()
        print("\n" + "="*50 + "\n")
        memory_network()
        print("\n" + "="*50 + "\n")
        learning_chain()
    else:
        print("Ungültige Wahl!")

if __name__ == "__main__":
    main()