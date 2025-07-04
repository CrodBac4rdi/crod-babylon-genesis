"""
TEST NETWORK FLOW - Findet wo Messages hängen bleiben
"""

from network import CRODNetwork
from atom_types import create_atom
import time

print("🔍 TESTING NETWORK MESSAGE FLOW\n")

# Create simple network
net = CRODNetwork("Test Network")

# Add two atoms
thinker = net.add_atom("thinker", (0, 0))
doubter = net.add_atom("doubter", (200, 0))

# Connect them
conn = net.connect_atoms(thinker.id, "thought", doubter.id, "thought")

print(f"✅ Network created:")
print(f"   Thinker ID: {thinker.id}")
print(f"   Doubter ID: {doubter.id}")
print(f"   Connection: {conn.id if conn else 'FAILED'}")

print("\n🧪 TESTING MESSAGE FLOW:")

# Test 1: Direct trigger
print("\n1. Direct thinker trigger:")
thinker.receive_input("trigger", {"test": "direct"})
print(f"   Thinker inputs: {thinker.inputs}")
print(f"   Thinker ready: {thinker.all_inputs_ready()}")

# Execute thinker
thinker.execute()
print(f"   Thinker outputs: {thinker.outputs}")

# Check doubter
print(f"   Doubter inputs: {doubter.inputs}")
print(f"   Doubter outputs: {doubter.outputs}")

# Test 2: Network tick
print("\n2. Network tick test:")
net.tick()
time.sleep(0.1)

print(f"   Network stats: {net.get_stats()}")
print(f"   Thinker metrics: {thinker.metrics}")
print(f"   Doubter metrics: {doubter.metrics}")

# Test 3: Multiple ticks
print("\n3. Multiple ticks:")
for i in range(3):
    net.tick()
    time.sleep(0.1)
    print(f"   Tick {i+1}: Processed={net.get_stats()['total_processed']}")

# Test 4: Check actual data flow
print("\n4. Data flow check:")
if thinker.outputs:
    print(f"   ✅ Thinker has outputs: {list(thinker.outputs.keys())}")
else:
    print(f"   ❌ Thinker has NO outputs!")
    
if doubter.outputs:
    print(f"   ✅ Doubter has outputs: {list(doubter.outputs.keys())}")
else:
    print(f"   ❌ Doubter has NO outputs!")

print("\n🏁 TEST COMPLETE!")