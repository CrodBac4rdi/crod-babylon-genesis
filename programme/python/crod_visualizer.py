#!/usr/bin/env python3
"""
CROD Scientific Visualizer - EIN Programm für ALLE Visualisierungen
Erstellt wissenschaftliche, aussagekräftige Diagramme basierend auf JSON Input
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import os
from datetime import datetime
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import matplotlib.patheffects as path_effects

class CRODVisualizer:
    def __init__(self):
        # Professional dark theme
        plt.style.use('dark_background')
        self.colors = {
            'primary': '#00ff41',    # Matrix green
            'secondary': '#00b4d8',  # Cyan
            'tertiary': '#f72585',   # Pink
            'warning': '#ffaa00',    # Amber
            'success': '#00ff41',    # Green
            'danger': '#ff0040',     # Red
            'info': '#0080ff',       # Blue
            'dark': '#1a1a1a',
            'light': '#ffffff'
        }
        
    def visualize_from_json(self, json_path):
        """Main entry point - creates visualization from JSON config"""
        with open(json_path, 'r') as f:
            config = json.load(f)
        
        viz_type = config.get('type', 'performance')
        data = config.get('data', {})
        options = config.get('options', {})
        
        # Route to appropriate visualization
        if viz_type == 'performance':
            return self.create_performance_chart(data, options)
        elif viz_type == 'network':
            return self.create_network_topology(data, options)
        elif viz_type == 'consciousness':
            return self.create_consciousness_flow(data, options)
        elif viz_type == 'comparison':
            return self.create_comparison_chart(data, options)
        elif viz_type == 'timeline':
            return self.create_timeline_chart(data, options)
        else:
            raise ValueError(f"Unknown visualization type: {viz_type}")
    
    def create_performance_chart(self, data, options):
        """Performance metrics visualization"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(options.get('title', 'CROD Performance Metrics'), fontsize=20, y=0.98)
        
        # 1. TPS/Throughput
        if 'throughput' in data:
            time = np.array(data['throughput'].get('time', list(range(len(data['throughput']['values'])))), dtype=float)
            values = np.array(data['throughput']['values'], dtype=float)
            ax1.plot(time, values, color=self.colors['primary'], linewidth=2)
            ax1.fill_between(time, values, alpha=0.3, color=self.colors['primary'])
            ax1.set_title('Network Throughput')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Transactions/sec')
            ax1.grid(True, alpha=0.3)
        
        # 2. Latency Distribution
        if 'latency' in data and data['latency']:
            latencies = np.array(data['latency'], dtype=float)
            ax2.hist(latencies, bins=30, color=self.colors['secondary'], alpha=0.7, edgecolor='white')
            ax2.set_title('Latency Distribution')
            ax2.set_xlabel('Latency (ms)')
            ax2.set_ylabel('Frequency')
            mean_lat = np.mean(latencies)
            ax2.axvline(mean_lat, color=self.colors['warning'], linestyle='--', 
                       label=f'Mean: {mean_lat:.1f}ms')
            ax2.legend()
        else:
            ax2.text(0.5, 0.5, 'No latency data', ha='center', va='center', transform=ax2.transAxes)
        
        # 3. Node Status
        if 'nodes' in data:
            node_types = list(data['nodes'].keys())
            node_counts = list(data['nodes'].values())
            colors = [self.colors[c] for c in ['primary', 'secondary', 'tertiary', 'info']][:len(node_types)]
            bars = ax3.bar(node_types, node_counts, color=colors)
            ax3.set_title('Network Nodes')
            ax3.set_ylabel('Count')
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
        
        # 4. Custom Metric
        if 'custom' in data and 'y' in data['custom']:
            custom_data = data['custom']
            y = np.array(custom_data['y'], dtype=float)
            x = np.array(custom_data.get('x', list(range(len(y)))), dtype=float)
            ax4.plot(x, y, color=self.colors['tertiary'], linewidth=3)
            ax4.set_title(custom_data.get('title', 'Custom Metric'))
            ax4.set_xlabel(custom_data.get('xlabel', 'X'))
            ax4.set_ylabel(custom_data.get('ylabel', 'Y'))
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'No custom data', ha='center', va='center', transform=ax4.transAxes)
        
        plt.tight_layout()
        return self._save_figure(fig, 'performance', options)
    
    def create_network_topology(self, data, options):
        """Network topology visualization"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(-10, 10)
        ax.set_ylim(-8, 8)
        
        # Title
        title = options.get('title', 'CROD Network Topology')
        ax.text(0, 7.5, title, fontsize=18, ha='center', weight='bold')
        
        # Regions/Clusters
        regions = data.get('regions', {})
        connections = data.get('connections', [])
        
        # Draw regions
        region_positions = {}
        angle_step = 2 * np.pi / max(len(regions), 1)
        
        for i, (name, region_data) in enumerate(regions.items()):
            angle = i * angle_step
            radius = 5
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            region_positions[name] = (x, y)
            
            # Draw region circle
            size = region_data.get('size', 2)
            color = self.colors.get(region_data.get('color', 'primary'))
            circle = Circle((x, y), size, color=color, alpha=0.3)
            ax.add_patch(circle)
            
            # Label
            ax.text(x, y+size+0.5, name, ha='center', fontsize=12, weight='bold')
            ax.text(x, y, f"{region_data.get('nodes', 0)} nodes", 
                   ha='center', fontsize=10, color='gray')
        
        # Draw connections
        for conn in connections:
            if conn['from'] in region_positions and conn['to'] in region_positions:
                start = region_positions[conn['from']]
                end = region_positions[conn['to']]
                
                # Connection line
                ax.plot([start[0], end[0]], [start[1], end[1]], 
                       color='white', alpha=0.3, linewidth=conn.get('weight', 1))
                
                # Latency label
                mid_x = (start[0] + end[0]) / 2
                mid_y = (start[1] + end[1]) / 2
                ax.text(mid_x, mid_y, f"{conn.get('latency', 0)}ms", 
                       fontsize=8, ha='center',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        # Stats box
        stats = data.get('stats', {})
        stats_text = '\n'.join([f"{k}: {v}" for k, v in stats.items()])
        ax.text(-9, -7, stats_text, fontsize=10, family='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='black', alpha=0.8))
        
        ax.set_aspect('equal')
        ax.axis('off')
        
        return self._save_figure(fig, 'network', options)
    
    def create_consciousness_flow(self, data, options):
        """Consciousness/data flow visualization"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Flow field
        if 'field' in data:
            field_data = data['field']
            x = np.linspace(-5, 5, 20)
            y = np.linspace(-5, 5, 20)
            X, Y = np.meshgrid(x, y)
            
            # Default flow pattern
            U = -Y + np.sin(X)
            V = X + np.cos(Y)
            
            # Stream plot
            stream = ax.streamplot(X, Y, U, V, color=np.sqrt(U**2 + V**2), 
                                  cmap='plasma', linewidth=2, density=1.5)
        
        # Nodes
        nodes = data.get('nodes', [])
        for node in nodes:
            x, y = node.get('position', [0, 0])
            size = node.get('size', 0.5)
            color = self.colors.get(node.get('color', 'primary'))
            circle = Circle((x, y), size, color=color, alpha=0.8, zorder=10)
            ax.add_patch(circle)
            ax.text(x, y+size+0.2, node.get('label', ''), ha='center', fontsize=10)
        
        # Title and labels
        ax.set_title(options.get('title', 'Consciousness Flow Dynamics'), fontsize=16, pad=20)
        ax.set_xlabel('Network Space X')
        ax.set_ylabel('Network Space Y')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        
        return self._save_figure(fig, 'consciousness', options)
    
    def create_comparison_chart(self, data, options):
        """Comparison/radar chart"""
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        # Categories
        categories = data.get('categories', [])
        N = len(categories)
        
        if N == 0:
            return None
        
        # Angles
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Plot each dataset
        datasets = data.get('datasets', {})
        colors = list(self.colors.values())
        
        for i, (name, values) in enumerate(datasets.items()):
            values = values + values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=name, color=colors[i % len(colors)])
            ax.fill(angles, values, alpha=0.15, color=colors[i % len(colors)])
        
        # Fix axis
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        
        # Title and legend
        plt.title(options.get('title', 'Comparison Chart'), size=16, y=1.08)
        plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
        
        return self._save_figure(fig, 'comparison', options)
    
    def create_timeline_chart(self, data, options):
        """Timeline/sequence visualization"""
        fig, ax = plt.subplots(figsize=(16, 8))
        
        events = data.get('events', [])
        
        # Sort events by time
        events.sort(key=lambda x: x.get('time', 0))
        
        # Plot timeline
        for i, event in enumerate(events):
            time = event.get('time', i)
            value = event.get('value', 1)
            event_type = event.get('type', 'normal')
            
            color = self.colors.get(event_type, self.colors['primary'])
            
            # Bar for event
            rect = Rectangle((time, 0), 1, value, 
                           facecolor=color, edgecolor='white', 
                           linewidth=1, alpha=0.8)
            ax.add_patch(rect)
            
            # Label
            if 'label' in event:
                ax.text(time + 0.5, value + 0.1, event['label'], 
                       ha='center', fontsize=8, rotation=45)
        
        # Current time indicator
        if 'current_time' in data:
            current = data['current_time']
            ax.axvline(current, color=self.colors['danger'], 
                      linestyle='--', linewidth=2)
            ax.text(current, ax.get_ylim()[1]*0.9, 'NOW', 
                   color=self.colors['danger'], ha='center', weight='bold')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title(options.get('title', 'Timeline'), fontsize=16)
        ax.set_xlim(0, max([e.get('time', 0) for e in events]) + 2)
        
        return self._save_figure(fig, 'timeline', options)
    
    def _save_figure(self, fig, viz_type, options):
        """Save figure with proper naming"""
        output_dir = options.get('output_dir', 'output/scientific')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/crod_{viz_type}_{timestamp}.png"
        
        fig.savefig(filename, dpi=300, bbox_inches='tight',
                   facecolor='black', edgecolor='none')
        plt.close(fig)
        
        print(f"✅ Saved: {filename}")
        return filename

def main():
    """Main function to run visualizer"""
    if len(sys.argv) < 2:
        print("""
Usage: python crod_visualizer.py <config.json>

Example config.json:
{
    "type": "performance",
    "data": {
        "throughput": {
            "values": [8000, 8500, 9000, 8700, 9200],
            "time": [0, 1, 2, 3, 4]
        },
        "latency": [1.2, 1.5, 1.1, 1.3, 1.4, 1.6],
        "nodes": {
            "Validators": 100,
            "Full Nodes": 500,
            "Light Clients": 2000
        }
    },
    "options": {
        "title": "CROD Network Performance",
        "output_dir": "output/charts"
    }
}
        """)
        return
    
    visualizer = CRODVisualizer()
    visualizer.visualize_from_json(sys.argv[1])

if __name__ == "__main__":
    main()