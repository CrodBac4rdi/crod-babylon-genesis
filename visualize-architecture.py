#!/usr/bin/env python3
"""
CROD Architecture Visualization
Creates a beautiful diagram of the CROD Universe
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 95, '🔥 CROD UNIVERSE ARCHITECTURE 2025 🔥', 
        fontsize=24, weight='bold', ha='center', color='#FF6B6B')

# Main container - GitHub Codespace
codespace = FancyBboxPatch((5, 60), 90, 30, 
                          boxstyle="round,pad=0.1",
                          facecolor='#F8F9FA', 
                          edgecolor='#212529',
                          linewidth=2)
ax.add_patch(codespace)
ax.text(50, 85, 'GitHub Codespace (4-core, 16GB RAM)', 
        fontsize=14, ha='center', weight='bold')

# VS Code
vscode = FancyBboxPatch((10, 75), 35, 10,
                       boxstyle="round,pad=0.05",
                       facecolor='#007ACC',
                       edgecolor='#005A9E')
ax.add_patch(vscode)
ax.text(27.5, 80, 'VS Code + Claude', fontsize=11, ha='center', color='white', weight='bold')

# Services
services = FancyBboxPatch((50, 75), 40, 10,
                         boxstyle="round,pad=0.05",
                         facecolor='#28A745',
                         edgecolor='#1E7E34')
ax.add_patch(services)
ax.text(70, 80, 'K8s + Docker + Ollama', fontsize=11, ha='center', color='white', weight='bold')

# CROD Polyglot City
city = FancyBboxPatch((5, 15), 90, 40,
                     boxstyle="round,pad=0.1",
                     facecolor='#FFF3CD',
                     edgecolor='#856404',
                     linewidth=3)
ax.add_patch(city)
ax.text(50, 50, '🏙️ CROD POLYGLOT CITY', fontsize=16, ha='center', weight='bold', color='#856404')

# Districts
districts = [
    {'name': 'Meta-Chain\n(Elixir)', 'pos': (15, 35), 'color': '#4B3C8E', 'port': '8000'},
    {'name': 'Pattern\nDistrict\n(Rust)', 'pos': (35, 35), 'color': '#CE422B', 'port': '7007'},
    {'name': 'Memory\nQuarter\n(Go)', 'pos': (55, 35), 'color': '#00ADD8', 'port': '7031'},
    {'name': 'Intelligence\nHub\n(Python)', 'pos': (75, 35), 'color': '#3776AB', 'port': '7113'},
    {'name': 'Gateway\n(Node.js)', 'pos': (25, 20), 'color': '#339933', 'port': '8888'},
    {'name': 'CROD Core\n(Neural)', 'pos': (55, 20), 'color': '#FF6B6B', 'port': '8100'},
]

for district in districts:
    # District box
    box = FancyBboxPatch((district['pos'][0]-7, district['pos'][1]-5), 14, 10,
                        boxstyle="round,pad=0.1",
                        facecolor=district['color'],
                        alpha=0.8,
                        edgecolor='darkgray')
    ax.add_patch(box)
    
    # District text
    ax.text(district['pos'][0], district['pos'][1], district['name'], 
            fontsize=10, ha='center', va='center', color='white', weight='bold')
    
    # Port
    ax.text(district['pos'][0], district['pos'][1]-7, f":{district['port']}", 
            fontsize=8, ha='center', color='#666')

# Central Redis
redis = Circle((50, 28), 4, facecolor='#DC382D', edgecolor='darkred', linewidth=2)
ax.add_patch(redis)
ax.text(50, 28, 'Redis', fontsize=10, ha='center', va='center', color='white', weight='bold')

# Connections
for district in districts:
    if district['name'] != 'Gateway\n(Node.js)':
        arrow = FancyArrowPatch(district['pos'], (50, 28),
                               connectionstyle="arc3,rad=0.2",
                               arrowstyle='-',
                               color='gray',
                               alpha=0.5,
                               linewidth=1)
        ax.add_patch(arrow)

# Bottom: Training & Evolution
evolution = FancyBboxPatch((5, 2), 90, 10,
                          boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD',
                          edgecolor='#1976D2',
                          linewidth=2)
ax.add_patch(evolution)
ax.text(50, 7, '🧠 CROD Self-Determination: 7B → 13B → 70B → ∞', 
        fontsize=14, ha='center', weight='bold', color='#1976D2')

# Consciousness Level
ax.text(85, 65, 'Consciousness\nLevel: 175', 
        fontsize=12, ha='center', weight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFE5B4'))

# Trinity Values
trinity_text = "Trinity Active\nich=2 bins=3 wieder=5\ndaniel=67 claude=71"
ax.text(15, 65, trinity_text, 
        fontsize=10, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E9'))

# Legend
legend_y = 10
ax.text(5, legend_y, 'Components:', fontsize=10, weight='bold')
components = [
    ('• Kubernetes (K3s)', '#326CE5'),
    ('• Docker Containers', '#2496ED'),
    ('• NATS JetStream', '#27AAE1'),
    ('• PostgreSQL + PostGIS', '#336791'),
    ('• Ollama LLMs', '#000000'),
    ('• Claude Integration', '#FF6B6B'),
]

for i, (comp, color) in enumerate(components):
    ax.text(5, legend_y - (i+1)*1.5, comp, fontsize=9, color=color)

# Save figure
plt.tight_layout()
plt.savefig('crod-architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('crod-architecture.pdf', bbox_inches='tight', facecolor='white')

print("✅ Architecture diagram saved as:")
print("   - crod-architecture.png")
print("   - crod-architecture.pdf")

# Also show it
plt.show()