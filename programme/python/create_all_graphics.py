#!/usr/bin/env python3
"""
Master script to generate all CROD graphics
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("CROD Graphics Generation Suite")
print("=" * 60)

# Run all visualization generators
generators = [
    'generate_crod_graphics.py',
    'psychedelic_crod.py',
    'quantum_reality_bender.py',
    'consciousness_flow_generator.py',
    'interdimensional_architect.py',
    'cosmic_data_sculptor.py'
]

for generator in generators:
    script_path = os.path.join(os.path.dirname(__file__), generator)
    if os.path.exists(script_path):
        print(f"\nRunning {generator}...")
        try:
            exec(open(script_path).read())
        except Exception as e:
            print(f"Error in {generator}: {e}")
    else:
        print(f"Skipping {generator} - not found")

print("\n" + "=" * 60)
print("All graphics generation complete!")

# Count total images
total_images = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.png'):
            total_images += 1

print(f"Total images generated: {total_images}")
print(f"Check the following directories for graphics:")

# List output directories
output_dirs = []
for item in os.listdir('.'):
    if os.path.isdir(item) and item.startswith('crod_'):
        output_dirs.append(item)
        # Count images in this directory
        dir_images = len([f for f in os.listdir(item) if f.endswith('.png')])
        print(f"  - {item}/ ({dir_images} images)")

print("\nGraphics generation complete! 🎨✨")