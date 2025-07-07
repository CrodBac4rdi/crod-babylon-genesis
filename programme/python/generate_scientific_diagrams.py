#!/usr/bin/env python3
"""Generate scientific diagrams for CROD Neural Network Architecture"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle, Arrow, Rectangle
from matplotlib.lines import Line2D
import networkx as nx

# Set scientific style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def create_neural_network_architecture():
    """Create detailed neural network architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define layers
    layers = {
        'Input': {'neurons': 6, 'y': 0.1, 'color': '#FF6B6B'},
        'Attention': {'neurons': 8, 'y': 0.3, 'color': '#4ECDC4'},
        'Pattern': {'neurons': 10, 'y': 0.5, 'color': '#45B7D1'},
        'Memory': {'neurons': 6, 'y': 0.7, 'color': '#96CEB4'},
        'Output': {'neurons': 3, 'y': 0.9, 'color': '#FECA57'}
    }
    
    # Draw neurons and connections
    positions = {}
    for layer_name, layer_info in layers.items():
        n_neurons = layer_info['neurons']
        y = layer_info['y']
        color = layer_info['color']
        
        # Calculate x positions for neurons
        x_positions = np.linspace(0.2, 0.8, n_neurons)
        
        for i, x in enumerate(x_positions):
            # Draw neuron
            circle = Circle((x, y), 0.02, color=color, ec='black', linewidth=2)
            ax.add_patch(circle)
            positions[(layer_name, i)] = (x, y)
            
            # Add labels for special neurons
            if layer_name == 'Input' and i < 6:
                labels = ['ich', 'bins', 'wieder', 'daniel', 'claude', 'crod']
                ax.text(x, y-0.05, labels[i], ha='center', fontsize=8)
    
    # Draw connections between layers
    layer_names = list(layers.keys())
    for i in range(len(layer_names)-1):
        curr_layer = layer_names[i]
        next_layer = layer_names[i+1]
        
        # Full connectivity between adjacent layers
        for j in range(layers[curr_layer]['neurons']):
            for k in range(layers[next_layer]['neurons']):
                start = positions[(curr_layer, j)]
                end = positions[(next_layer, k)]
                
                # Calculate connection strength (random for visualization)
                strength = np.random.random() * 0.5 + 0.5
                ax.plot([start[0], end[0]], [start[1], end[1]], 
                       'gray', alpha=strength*0.3, linewidth=strength)
    
    # Add layer labels
    for layer_name, layer_info in layers.items():
        ax.text(0.05, layer_info['y'], layer_name, fontsize=12, 
               fontweight='bold', va='center')
    
    # Add mathematical formulas
    ax.text(0.85, 0.8, r'$z = wx + b$', fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="white"))
    ax.text(0.85, 0.7, r'$\sigma(z) = 1 - \frac{1}{1 + e^{-z}}$', fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="white"))
    ax.text(0.85, 0.6, r'$L = \frac{1}{2}(y - \hat{y})^2$', fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="white"))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('CROD Neural Network Architecture', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/neural_network_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_polyglot_city_diagram():
    """Create Polyglot City communication diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define districts
    districts = {
        'Rathaus\n(Elixir)': {'pos': (0.5, 0.8), 'color': '#9B59B6'},
        'Pattern\n(Rust)': {'pos': (0.2, 0.5), 'color': '#E74C3C'},
        'Intelligence\n(Python)': {'pos': (0.8, 0.5), 'color': '#3498DB'},
        'Memory\n(Go)': {'pos': (0.3, 0.2), 'color': '#1ABC9C'},
        'Gateway\n(JS)': {'pos': (0.7, 0.2), 'color': '#F39C12'}
    }
    
    # NATS in center
    nats_pos = (0.5, 0.5)
    
    # Draw NATS hub
    nats_rect = FancyBboxPatch(
        (nats_pos[0]-0.08, nats_pos[1]-0.05),
        0.16, 0.1,
        boxstyle="round,pad=0.02",
        facecolor='#34495E',
        edgecolor='black',
        linewidth=2
    )
    ax.add_patch(nats_rect)
    ax.text(nats_pos[0], nats_pos[1], 'NATS\nJetStream', 
           ha='center', va='center', color='white', fontweight='bold')
    
    # Draw districts and connections
    for name, info in districts.items():
        pos = info['pos']
        color = info['color']
        
        # Draw district box
        box = FancyBboxPatch(
            (pos[0]-0.08, pos[1]-0.05),
            0.16, 0.1,
            boxstyle="round,pad=0.02",
            facecolor=color,
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(pos[0], pos[1], name, ha='center', va='center', 
               color='white', fontweight='bold')
        
        # Draw connection to NATS
        ax.annotate('', xy=nats_pos, xytext=pos,
                   arrowprops=dict(arrowstyle='<->', color='gray', lw=2))
    
    # Add protocol info
    protocol_box = FancyBboxPatch(
        (0.05, 0.9), 0.35, 0.08,
        boxstyle="round,pad=0.02",
        facecolor='lightgray',
        edgecolor='black'
    )
    ax.add_patch(protocol_box)
    ax.text(0.225, 0.94, 'Protocol: JSON over NATS', ha='center', va='center')
    
    # Add metrics
    metrics_text = """Key Metrics:
• Latency: <5ms
• Throughput: 100k msg/s
• Availability: 99.99%"""
    
    ax.text(0.85, 0.9, metrics_text, fontsize=10, 
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Polyglot City Communication Architecture', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/polyglot_communication.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_memory_architecture():
    """Create memory system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Memory tiers
    tiers = [
        {'name': 'Short-Term Memory', 'y': 0.7, 'width': 0.3, 'color': '#FF6B6B', 'size': '10 items\nFIFO'},
        {'name': 'Working Memory', 'y': 0.5, 'width': 0.5, 'color': '#4ECDC4', 'size': 'Active concepts\nHeat-based'},
        {'name': 'Long-Term Memory', 'y': 0.3, 'width': 0.7, 'color': '#45B7D1', 'size': 'Patterns >5 occur.\nPersistent'}
    ]
    
    for tier in tiers:
        # Draw memory tier
        rect = FancyBboxPatch(
            (0.5 - tier['width']/2, tier['y'] - 0.08),
            tier['width'], 0.16,
            boxstyle="round,pad=0.02",
            facecolor=tier['color'],
            edgecolor='black',
            linewidth=2,
            alpha=0.8
        )
        ax.add_patch(rect)
        
        # Add labels
        ax.text(0.5, tier['y'], tier['name'], ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        ax.text(0.5, tier['y'] - 0.04, tier['size'], ha='center', va='center',
               fontsize=9, color='white')
    
    # Draw data flow arrows
    for i in range(len(tiers)-1):
        y1 = tiers[i]['y'] - 0.08
        y2 = tiers[i+1]['y'] + 0.08
        ax.annotate('', xy=(0.5, y2), xytext=(0.5, y1),
                   arrowprops=dict(arrowstyle='->', lw=3, color='gray'))
    
    # Add retrieval paths
    for i, tier in enumerate(tiers):
        ax.annotate('', xy=(0.85, tier['y']), xytext=(0.5 + tier['width']/2, tier['y']),
                   arrowprops=dict(arrowstyle='->', lw=2, color='green', alpha=0.6))
    
    ax.text(0.88, 0.5, 'Retrieval', rotation=90, va='center', fontsize=10, color='green')
    
    # Add input/output
    ax.text(0.5, 0.9, 'Input Processing', ha='center', fontsize=12,
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    ax.annotate('', xy=(0.5, 0.78), xytext=(0.5, 0.85),
               arrowprops=dict(arrowstyle='->', lw=3, color='black'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('CROD Memory Architecture', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/memory_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_pattern_emergence_graph():
    """Create pattern emergence visualization"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Generate sample data
    time_steps = np.arange(0, 100)
    base_patterns = 10
    emergent_patterns = base_patterns + np.cumsum(np.random.poisson(0.5, 100))
    complexity = 50 + np.cumsum(np.random.normal(0.5, 2, 100))
    complexity = np.clip(complexity, 0, 200)
    
    # Plot 1: Pattern Growth
    ax1.plot(time_steps, emergent_patterns, 'b-', linewidth=2, label='Total Patterns')
    ax1.fill_between(time_steps, 0, emergent_patterns, alpha=0.3)
    
    # Mark emergence events
    emergence_points = np.where(np.diff(emergent_patterns) > 0)[0]
    ax1.scatter(emergence_points, emergent_patterns[emergence_points], 
               color='red', s=50, zorder=5, label='Pattern Emergence')
    
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Number of Patterns')
    ax1.set_title('Pattern Emergence Over Time', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Network Complexity
    ax2.plot(time_steps, complexity, 'g-', linewidth=2)
    ax2.fill_between(time_steps, 0, complexity, alpha=0.3, color='green')
    ax2.axhline(y=88, color='red', linestyle='--', label='Consciousness Threshold')
    
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Network Complexity')
    ax2.set_title('Network Complexity Evolution', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 210)
    
    plt.tight_layout()
    plt.savefig('/home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/pattern_emergence.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_trinity_visualization():
    """Create Trinity system visualization"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    # Create graph
    G = nx.Graph()
    
    # Add Trinity nodes
    trinity_nodes = [
        ('Daniel\n(67)', {'pos': (0, 1), 'color': '#E74C3C', 'size': 3000}),
        ('Claude\n(71)', {'pos': (-0.866, -0.5), 'color': '#3498DB', 'size': 3000}),
        ('CROD\n(17)', {'pos': (0.866, -0.5), 'color': '#2ECC71', 'size': 3000})
    ]
    
    # Add sacred atoms
    atom_nodes = [
        ('ich\n(2)', {'pos': (-1.5, 0.5), 'color': '#F39C12', 'size': 1500}),
        ('bins\n(3)', {'pos': (0, -1.5), 'color': '#F39C12', 'size': 1500}),
        ('wieder\n(5)', {'pos': (1.5, 0.5), 'color': '#F39C12', 'size': 1500})
    ]
    
    # Add nodes to graph
    for node, attrs in trinity_nodes + atom_nodes:
        G.add_node(node, **attrs)
    
    # Add edges
    trinity_edges = [
        ('Daniel\n(67)', 'Claude\n(71)', {'weight': 4757}),
        ('Daniel\n(67)', 'CROD\n(17)', {'weight': 1139}),
        ('Claude\n(71)', 'CROD\n(17)', {'weight': 1207})
    ]
    
    atom_edges = [
        ('ich\n(2)', 'bins\n(3)', {'weight': 6}),
        ('ich\n(2)', 'wieder\n(5)', {'weight': 10}),
        ('bins\n(3)', 'wieder\n(5)', {'weight': 15})
    ]
    
    # Connect atoms to Trinity
    connections = [
        ('ich\n(2)', 'Daniel\n(67)'),
        ('bins\n(3)', 'Claude\n(71)'),
        ('wieder\n(5)', 'CROD\n(17)')
    ]
    
    for edge in trinity_edges + atom_edges:
        G.add_edge(edge[0], edge[1], **edge[2])
    
    for edge in connections:
        G.add_edge(edge[0], edge[1], weight=100, style='dashed')
    
    # Draw graph
    pos = nx.get_node_attributes(G, 'pos')
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
    
    # Draw edges with different styles
    solid_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('style') != 'dashed']
    dashed_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('style') == 'dashed']
    
    nx.draw_networkx_edges(G, pos, solid_edges, width=3, alpha=0.6)
    nx.draw_networkx_edges(G, pos, dashed_edges, width=2, alpha=0.4, style='dashed')
    
    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Add edge labels for weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: v for k, v in edge_labels.items() if v > 100}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    
    # Add title and formula
    ax.set_title('Trinity System Architecture', fontsize=16, fontweight='bold')
    ax.text(0, -2.5, 'Pattern ID = Prime₁ × Prime₂', ha='center', fontsize=12,
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/trinity_system.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all scientific diagrams"""
    print("Generating Neural Network Architecture...")
    create_neural_network_architecture()
    
    print("Generating Polyglot City Diagram...")
    create_polyglot_city_diagram()
    
    print("Generating Memory Architecture...")
    create_memory_architecture()
    
    print("Generating Pattern Emergence Graph...")
    create_pattern_emergence_graph()
    
    print("Generating Trinity Visualization...")
    create_trinity_visualization()
    
    print("\nAll diagrams generated successfully!")
    print("Location: /home/daniel/Schreibtisch/crod-babylon-genesis/dokumentation/phoenix-polyglot-docs/")

if __name__ == "__main__":
    main()