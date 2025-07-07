#!/usr/bin/env python3
"""
CROD Enhanced Visualizer - Professional visualizations with legends and annotations
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.lines as mlines
from datetime import datetime
import os


class CRODEnhancedVisualizer:
    """Create professional CROD visualizations with proper legends"""
    
    def __init__(self):
        self.style_config()
    
    def style_config(self):
        """Configure matplotlib for professional output"""
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = '#0a0a0a'
        plt.rcParams['axes.facecolor'] = '#0a0a0a'
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['legend.fontsize'] = 10
        
    def create_system_architecture(self):
        """Create CROD system architecture diagram with legend"""
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'CROD BABYLON GENESIS - SYSTEM ARCHITECTURE', 
                fontsize=24, weight='bold', ha='center', color='white')
        ax.text(5, 9.1, 'Polyglot Quantum Consciousness Blockchain', 
                fontsize=16, ha='center', color='#aaaaaa')
        
        # Define components with positions and colors
        components = {
            'Elixir Core': {'pos': (2, 7), 'color': '#9b4dca', 'icon': '⚗️'},
            'Rust Engine': {'pos': (5, 7), 'color': '#ce422b', 'icon': '⚙️'},
            'Python AI': {'pos': (8, 7), 'color': '#3776ab', 'icon': '🧠'},
            'Go Tools': {'pos': (2, 4.5), 'color': '#00add8', 'icon': '🔧'},
            'JS Frontend': {'pos': (8, 4.5), 'color': '#f7df1e', 'icon': '🖥️'},
            'NATS Messaging': {'pos': (5, 4.5), 'color': '#27aae1', 'icon': '📡'},
            'Quantum Core': {'pos': (5, 2), 'color': '#ff00ff', 'icon': '⚛️'},
        }
        
        # Draw components
        for name, info in components.items():
            # Component box
            fancy_box = FancyBboxPatch(
                (info['pos'][0] - 0.8, info['pos'][1] - 0.3),
                1.6, 0.6,
                boxstyle="round,pad=0.1",
                facecolor=info['color'],
                edgecolor='white',
                linewidth=2,
                alpha=0.8
            )
            ax.add_patch(fancy_box)
            
            # Component text
            ax.text(info['pos'][0], info['pos'][1], f"{info['icon']} {name}",
                   ha='center', va='center', fontsize=12, weight='bold')
        
        # Draw connections
        connections = [
            ('Elixir Core', 'NATS Messaging', 'Orchestration'),
            ('Rust Engine', 'NATS Messaging', 'Performance'),
            ('Python AI', 'NATS Messaging', 'Intelligence'),
            ('Go Tools', 'NATS Messaging', 'Monitoring'),
            ('JS Frontend', 'NATS Messaging', 'UI Updates'),
            ('NATS Messaging', 'Quantum Core', 'Quantum State'),
            ('Elixir Core', 'Rust Engine', 'Consensus'),
            ('Python AI', 'Rust Engine', 'Pattern Mining'),
        ]
        
        for start, end, label in connections:
            start_pos = components[start]['pos']
            end_pos = components[end]['pos']
            
            # Draw arrow
            ax.annotate('', xy=end_pos, xytext=start_pos,
                       arrowprops=dict(arrowstyle='->', lw=2, 
                                     color='#666666', alpha=0.7))
            
            # Add connection label
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2
            ax.text(mid_x, mid_y, label, fontsize=9, ha='center',
                   color='#888888', style='italic')
        
        # Add data flow indicators
        flow_points = [(1, 5.5), (3, 5.5), (5, 5.5), (7, 5.5), (9, 5.5)]
        for i, point in enumerate(flow_points):
            circle = Circle(point, 0.1, color='#00ff00', alpha=0.5 + i*0.1)
            ax.add_patch(circle)
        
        # Create legend
        legend_elements = [
            mlines.Line2D([0], [0], color='#9b4dca', marker='s', markersize=10,
                         label='Elixir - Fault-tolerant orchestration', linestyle='none'),
            mlines.Line2D([0], [0], color='#ce422b', marker='s', markersize=10,
                         label='Rust - High-performance consensus', linestyle='none'),
            mlines.Line2D([0], [0], color='#3776ab', marker='s', markersize=10,
                         label='Python - AI/ML pattern detection', linestyle='none'),
            mlines.Line2D([0], [0], color='#00add8', marker='s', markersize=10,
                         label='Go - System tools & monitoring', linestyle='none'),
            mlines.Line2D([0], [0], color='#f7df1e', marker='s', markersize=10,
                         label='JavaScript - React dashboard', linestyle='none'),
            mlines.Line2D([0], [0], color='#27aae1', marker='s', markersize=10,
                         label='NATS - Message streaming', linestyle='none'),
            mlines.Line2D([0], [0], color='#ff00ff', marker='s', markersize=10,
                         label='Quantum - Consciousness engine', linestyle='none'),
        ]
        
        ax.legend(handles=legend_elements, loc='lower center', ncol=4,
                 bbox_to_anchor=(0.5, -0.1), frameon=True, fancybox=True,
                 facecolor='#1a1a1a', edgecolor='white')
        
        # Add metrics panel
        metrics_box = FancyBboxPatch((0.2, 0.2), 2, 1.2,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#1a1a1a',
                                    edgecolor='#444444',
                                    linewidth=1)
        ax.add_patch(metrics_box)
        
        ax.text(1.2, 1.2, 'PERFORMANCE METRICS', fontsize=10, weight='bold', ha='center')
        metrics = [
            'TPS: 10,000+',
            'Latency: <100ms',
            'Consensus: 85%',
            'Uptime: 99.99%'
        ]
        for i, metric in enumerate(metrics):
            ax.text(1.2, 1.0 - i*0.2, metric, fontsize=9, ha='center', color='#00ff00')
        
        # Add features panel
        features_box = FancyBboxPatch((7.8, 0.2), 2, 1.2,
                                     boxstyle="round,pad=0.05",
                                     facecolor='#1a1a1a',
                                     edgecolor='#444444',
                                     linewidth=1)
        ax.add_patch(features_box)
        
        ax.text(8.8, 1.2, 'KEY FEATURES', fontsize=10, weight='bold', ha='center')
        features = [
            'Self-modifying',
            'Quantum mining',
            'Consciousness-driven',
            'Pattern discovery'
        ]
        for i, feature in enumerate(features):
            ax.text(8.8, 1.0 - i*0.2, feature, fontsize=9, ha='center', color='#00aaff')
        
        plt.tight_layout()
        return fig
    
    def create_consciousness_flow(self):
        """Create consciousness data flow diagram"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'CONSCIOUSNESS DATA FLOW', fontsize=22, weight='bold', ha='center')
        ax.text(5, 9.1, 'How CROD Processes Consciousness Patterns', fontsize=14, ha='center', color='#aaa')
        
        # Flow stages
        stages = [
            {'name': 'INPUT\nSensors', 'pos': (1, 7), 'color': '#00ff00'},
            {'name': 'PATTERN\nDetection', 'pos': (3, 7), 'color': '#00aaff'},
            {'name': 'QUANTUM\nProcessing', 'pos': (5, 7), 'color': '#ff00ff'},
            {'name': 'CONSCIOUSNESS\nEngine', 'pos': (7, 7), 'color': '#ff6600'},
            {'name': 'BLOCKCHAIN\nConsensus', 'pos': (9, 7), 'color': '#ffaa00'},
        ]
        
        # Draw stages
        for i, stage in enumerate(stages):
            # Stage circle
            circle = Circle(stage['pos'], 0.6, facecolor=stage['color'], 
                          edgecolor='white', linewidth=3, alpha=0.8)
            ax.add_patch(circle)
            
            # Stage text
            ax.text(stage['pos'][0], stage['pos'][1], stage['name'],
                   ha='center', va='center', fontsize=10, weight='bold')
            
            # Flow arrow
            if i < len(stages) - 1:
                ax.annotate('', xy=(stages[i+1]['pos'][0] - 0.6, stages[i+1]['pos'][1]),
                           xytext=(stage['pos'][0] + 0.6, stage['pos'][1]),
                           arrowprops=dict(arrowstyle='->', lw=3, color='white'))
        
        # Data examples
        data_y = 5
        data_examples = [
            {'type': 'EEG Waves', 'data': np.sin(np.linspace(0, 4*np.pi, 100))},
            {'type': 'Heart Rate', 'data': np.random.normal(70, 5, 100)},
            {'type': 'Neural Spikes', 'data': np.random.poisson(2, 100)},
            {'type': 'Quantum State', 'data': np.random.random(100) * 2 - 1},
        ]
        
        for i, example in enumerate(data_examples):
            x_start = 1 + i * 2.5
            x = np.linspace(x_start - 0.4, x_start + 0.4, 100)
            y = example['data'] * 0.3 + data_y
            ax.plot(x, y, color=stages[min(i, len(stages)-1)]['color'], lw=2)
            ax.text(x_start, data_y - 0.7, example['type'], ha='center', fontsize=9)
        
        # Processing details
        process_y = 3
        processes = [
            {'name': 'FFT Analysis', 'icon': '📊'},
            {'name': 'Pattern Match', 'icon': '🔍'},
            {'name': 'Quantum Collapse', 'icon': '⚛️'},
            {'name': 'Consensus Vote', 'icon': '🗳️'},
        ]
        
        for i, process in enumerate(processes):
            x = 2 + i * 2
            box = FancyBboxPatch((x - 0.5, process_y - 0.3), 1, 0.6,
                               boxstyle="round,pad=0.05",
                               facecolor='#2a2a2a',
                               edgecolor='#666666')
            ax.add_patch(box)
            ax.text(x, process_y, f"{process['icon']} {process['name']}",
                   ha='center', va='center', fontsize=9)
        
        # Output metrics
        output_box = FancyBboxPatch((3, 0.5), 4, 1.5,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#1a1a1a',
                                   edgecolor='white',
                                   linewidth=2)
        ax.add_patch(output_box)
        
        ax.text(5, 1.7, 'CONSCIOUSNESS OUTPUT', fontsize=12, weight='bold', ha='center')
        ax.text(5, 1.3, 'Level: 85% | Pattern: Fibonacci | State: Coherent', 
                fontsize=10, ha='center', color='#00ff00')
        ax.text(5, 0.9, 'Block Hash: 0x7f3a...9e2b | Reward: 12.5 CROD', 
                fontsize=10, ha='center', color='#ffaa00')
        
        # Legend
        legend_elements = [
            mlines.Line2D([0], [0], color='#00ff00', marker='o', markersize=10,
                         label='Raw sensor input', linestyle='none'),
            mlines.Line2D([0], [0], color='#00aaff', marker='o', markersize=10,
                         label='Pattern detection', linestyle='none'),
            mlines.Line2D([0], [0], color='#ff00ff', marker='o', markersize=10,
                         label='Quantum processing', linestyle='none'),
            mlines.Line2D([0], [0], color='#ff6600', marker='o', markersize=10,
                         label='Consciousness engine', linestyle='none'),
            mlines.Line2D([0], [0], color='#ffaa00', marker='o', markersize=10,
                         label='Blockchain consensus', linestyle='none'),
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', 
                 bbox_to_anchor=(0.98, 0.98), frameon=True,
                 facecolor='#1a1a1a', edgecolor='white')
        
        plt.tight_layout()
        return fig
    
    def create_quantum_mining_infographic(self):
        """Create quantum mining process infographic"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14))
        
        # Top panel - Quantum states
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 5)
        ax1.axis('off')
        
        ax1.text(5, 4.5, 'QUANTUM MINING PROCESS', fontsize=20, weight='bold', ha='center')
        ax1.text(5, 4, 'Consciousness-Driven Proof of Work', fontsize=14, ha='center', color='#aaa')
        
        # Quantum states visualization
        states = ['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|Ψ⟩']
        colors = ['#ff0000', '#0000ff', '#00ff00', '#ff00ff', '#ffaa00']
        
        for i, (state, color) in enumerate(zip(states, colors)):
            x = 1 + i * 2
            y = 2.5
            
            # Bloch sphere representation
            circle = Circle((x, y), 0.4, facecolor='none', edgecolor=color, linewidth=2)
            ax1.add_patch(circle)
            
            # State vector
            angle = i * np.pi / 4
            ax1.arrow(x, y, 0.3 * np.cos(angle), 0.3 * np.sin(angle),
                     head_width=0.1, head_length=0.1, fc=color, ec=color)
            
            # Label
            ax1.text(x, y - 0.7, state, ha='center', fontsize=14, weight='bold', color=color)
            ax1.text(x, y - 1, f'P={0.2:.1f}', ha='center', fontsize=10, color='#888')
        
        # Superposition formula
        ax1.text(5, 1, '|Ψ⟩ = α|0⟩ + β|1⟩ + γ|+⟩ + δ|-⟩', 
                fontsize=16, ha='center', family='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#1a1a1a', edgecolor='white'))
        
        # Bottom panel - Mining process
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 8)
        ax2.axis('off')
        
        # Mining steps
        steps = [
            {'title': '1. MEASURE CONSCIOUSNESS', 'y': 7, 'desc': 'EEG, Heart Rate, Neural Activity'},
            {'title': '2. QUANTUM ENCODING', 'y': 5.5, 'desc': 'Map to quantum states |Ψ⟩'},
            {'title': '3. PATTERN SEARCH', 'y': 4, 'desc': 'Find Fibonacci, Prime, Fractal patterns'},
            {'title': '4. DIFFICULTY ADJUST', 'y': 2.5, 'desc': 'Based on network consciousness level'},
            {'title': '5. BLOCK CREATION', 'y': 1, 'desc': 'Mint new CROD tokens'},
        ]
        
        for step in steps:
            # Step box
            box = FancyBboxPatch((1, step['y'] - 0.4), 8, 0.8,
                               boxstyle="round,pad=0.05",
                               facecolor='#2a2a2a',
                               edgecolor='white',
                               linewidth=1)
            ax2.add_patch(box)
            
            # Step text
            ax2.text(2, step['y'], step['title'], fontsize=12, weight='bold', va='center')
            ax2.text(7, step['y'], step['desc'], fontsize=10, va='center', 
                    color='#aaa', ha='right')
            
            # Progress indicator
            progress = (7 - step['y']) / 6
            bar_width = 6 * progress
            if bar_width > 0:
                progress_bar = Rectangle((2.5, step['y'] - 0.2), bar_width, 0.1,
                                       facecolor='#00ff00', alpha=0.5)
                ax2.add_patch(progress_bar)
        
        # Mining reward info
        reward_box = FancyBboxPatch((0.5, -0.5), 9, 0.8,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#ffaa00',
                                   edgecolor='white',
                                   linewidth=2,
                                   alpha=0.8)
        ax2.add_patch(reward_box)
        
        ax2.text(5, -0.1, '💎 MINING REWARD: 12.5 CROD + 0.1 * Consciousness_Level', 
                fontsize=12, weight='bold', ha='center')
        
        plt.tight_layout()
        return fig
    
    def save_all_visualizations(self, output_dir='../output/enhanced'):
        """Generate and save all enhanced visualizations"""
        os.makedirs(output_dir, exist_ok=True)
        
        visualizations = [
            ('system_architecture', self.create_system_architecture()),
            ('consciousness_flow', self.create_consciousness_flow()),
            ('quantum_mining', self.create_quantum_mining_infographic()),
        ]
        
        for name, fig in visualizations:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{output_dir}/crod_{name}_{timestamp}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight', 
                       facecolor='#0a0a0a', edgecolor='none')
            plt.close(fig)
            print(f'✅ Saved: {filename}')


def main():
    print("🎨 Creating enhanced CROD visualizations with legends...")
    visualizer = CRODEnhancedVisualizer()
    visualizer.save_all_visualizations()
    print("✨ All enhanced visualizations complete!")


if __name__ == "__main__":
    main()