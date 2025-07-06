#!/usr/bin/env python3
"""
CROD Architecture Visualizer - Creates beautiful SVG visualizations of the CROD architecture
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import argparse
from datetime import datetime

class CRODVisualizer:
    def __init__(self, output_dir="../assets/generated", width=1200, height=800, dark_mode=True):
        self.output_dir = output_dir
        self.width = width
        self.height = height
        self.fig_width = width / 100
        self.fig_height = height / 100
        self.dark_mode = dark_mode
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup colors based on mode
        if dark_mode:
            self.bg_color = '#0a0a0a'
            self.text_color = '#ffffff'
            self.accent_color = '#4a6cf7'
            self.highlight_color = '#f7774a'
            self.success_color = '#2ecc71'
        else:
            self.bg_color = '#ffffff'
            self.text_color = '#333333'
            self.accent_color = '#4a6cf7'
            self.highlight_color = '#f7774a'
            self.success_color = '#2ecc71'
    
    def create_architecture_3d(self, save=True):
        """Create a 3D visualization of the CROD architecture"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set background color
        ax.set_facecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)
        
        # Create layers
        layers = [
            {"name": "Client Layer", "height": 4, "color": self.accent_color, "z": 4},
            {"name": "Frontend Layer", "height": 3, "color": self.highlight_color, "z": 3},
            {"name": "Service Layer", "height": 2, "color": self.success_color, "z": 2},
            {"name": "Data Layer", "height": 1, "color": "#9b59b6", "z": 1}
        ]
        
        # Create connections between layers
        connections = []
        
        # Draw layers
        for layer in layers:
            self._draw_layer(ax, layer, connections)
        
        # Draw connections
        for conn in connections:
            self._draw_connection(ax, conn)
        
        # Set labels and title
        ax.set_xlabel('X', color=self.text_color)
        ax.set_ylabel('Y', color=self.text_color)
        ax.set_zlabel('Z', color=self.text_color)
        ax.set_title('CROD Clean Architecture', color=self.text_color, fontsize=20)
        
        # Remove grid and axes
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        
        # Hide axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Set view angle
        ax.view_init(elev=30, azim=45)
        
        # Save the figure
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/crod_architecture_3d_{timestamp}.svg"
            plt.savefig(filename, format='svg', bbox_inches='tight')
            print(f"Saved 3D architecture visualization to {filename}")
            
            # Also save as PNG for easy viewing
            png_filename = f"{self.output_dir}/crod_architecture_3d_{timestamp}.png"
            plt.savefig(png_filename, format='png', dpi=300, bbox_inches='tight')
            print(f"Saved 3D architecture visualization to {png_filename}")
        
        return fig
    
    def create_polyglot_visualization(self, save=True):
        """Create a visualization of the polyglot nature of CROD"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        
        # Set background color
        ax.set_facecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)
        
        # Languages and their sizes (relative importance)
        languages = [
            {"name": "Rust", "size": 25, "color": "#f74c00"},
            {"name": "Python", "size": 30, "color": "#3776ab"},
            {"name": "JavaScript", "size": 28, "color": "#f7df1e"},
            {"name": "TypeScript", "size": 22, "color": "#007acc"},
            {"name": "CSS", "size": 15, "color": "#264de4"},
            {"name": "HTML", "size": 15, "color": "#e34c26"},
            {"name": "SQL", "size": 18, "color": "#4479a1"}
        ]
        
        # Calculate positions (circular layout)
        n = len(languages)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        
        # Draw languages as circles
        for i, lang in enumerate(languages):
            x = 0.5 * np.cos(angles[i])
            y = 0.5 * np.sin(angles[i])
            size = lang["size"] * 100  # Scale for visualization
            
            circle = plt.Circle((x, y), size/1000, color=lang["color"], alpha=0.7)
            ax.add_patch(circle)
            
            # Add text label
            ax.text(x, y, lang["name"], ha='center', va='center', color=self.text_color, 
                   fontsize=12, fontweight='bold')
            
            # Connect to center
            ax.plot([0, x], [0, y], color=lang["color"], alpha=0.5, linewidth=2)
        
        # Add CROD at center
        center_circle = plt.Circle((0, 0), 0.1, color=self.accent_color, alpha=0.9)
        ax.add_patch(center_circle)
        ax.text(0, 0, "CROD", ha='center', va='center', color=self.text_color, 
               fontsize=14, fontweight='bold')
        
        # Set title
        ax.set_title('CROD Polyglot Architecture', color=self.text_color, fontsize=20)
        
        # Set limits and remove axes
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')
        
        # Save the figure
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/crod_polyglot_{timestamp}.svg"
            plt.savefig(filename, format='svg', bbox_inches='tight')
            print(f"Saved polyglot visualization to {filename}")
            
            # Also save as PNG for easy viewing
            png_filename = f"{self.output_dir}/crod_polyglot_{timestamp}.png"
            plt.savefig(png_filename, format='png', dpi=300, bbox_inches='tight')
            print(f"Saved polyglot visualization to {png_filename}")
        
        return fig
    
    def create_dataflow_visualization(self, save=True):
        """Create a visualization of the data flow in CROD"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        
        # Set background color
        ax.set_facecolor(self.bg_color)
        fig.patch.set_facecolor(self.bg_color)
        
        # Define components and their positions
        components = [
            {"name": "Client", "x": 0.1, "y": 0.9, "color": "#3498db"},
            {"name": "API Gateway", "x": 0.3, "y": 0.7, "color": "#2ecc71"},
            {"name": "Chat Service", "x": 0.2, "y": 0.5, "color": "#f1c40f"},
            {"name": "Code Service", "x": 0.3, "y": 0.3, "color": "#e74c3c"},
            {"name": "Image Service", "x": 0.4, "y": 0.5, "color": "#9b59b6"},
            {"name": "Chat DB", "x": 0.2, "y": 0.1, "color": "#34495e"},
            {"name": "Code DB", "x": 0.3, "y": 0.1, "color": "#34495e"},
            {"name": "Image DB", "x": 0.4, "y": 0.1, "color": "#34495e"},
            {"name": "Cache", "x": 0.6, "y": 0.5, "color": "#e67e22"},
            {"name": "File Storage", "x": 0.7, "y": 0.3, "color": "#16a085"},
            {"name": "ML Models", "x": 0.8, "y": 0.5, "color": "#8e44ad"}
        ]
        
        # Define data flows
        flows = [
            {"from": "Client", "to": "API Gateway", "color": "#3498db", "width": 2},
            {"from": "API Gateway", "to": "Chat Service", "color": "#2ecc71", "width": 1.5},
            {"from": "API Gateway", "to": "Code Service", "color": "#2ecc71", "width": 1.5},
            {"from": "API Gateway", "to": "Image Service", "color": "#2ecc71", "width": 1.5},
            {"from": "Chat Service", "to": "Chat DB", "color": "#f1c40f", "width": 1},
            {"from": "Code Service", "to": "Code DB", "color": "#e74c3c", "width": 1},
            {"from": "Image Service", "to": "Image DB", "color": "#9b59b6", "width": 1},
            {"from": "API Gateway", "to": "Cache", "color": "#2ecc71", "width": 1.5},
            {"from": "Image Service", "to": "File Storage", "color": "#9b59b6", "width": 1},
            {"from": "Chat Service", "to": "ML Models", "color": "#f1c40f", "width": 1},
            {"from": "Image Service", "to": "ML Models", "color": "#9b59b6", "width": 1}
        ]
        
        # Draw components
        for comp in components:
            circle = plt.Circle((comp["x"], comp["y"]), 0.05, color=comp["color"], alpha=0.8)
            ax.add_patch(circle)
            ax.text(comp["x"], comp["y"] - 0.08, comp["name"], ha='center', va='center', 
                   color=self.text_color, fontsize=10)
        
        # Draw flows
        for flow in flows:
            from_comp = next(c for c in components if c["name"] == flow["from"])
            to_comp = next(c for c in components if c["name"] == flow["to"])
            
            # Get positions
            x1, y1 = from_comp["x"], from_comp["y"]
            x2, y2 = to_comp["x"], to_comp["y"]
            
            # Draw arrow
            ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.02, head_length=0.02, 
                    fc=flow["color"], ec=flow["color"], width=flow["width"]/1000, 
                    length_includes_head=True, alpha=0.7)
        
        # Set title
        ax.set_title('CROD Data Flow', color=self.text_color, fontsize=20)
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Save the figure
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/crod_dataflow_{timestamp}.svg"
            plt.savefig(filename, format='svg', bbox_inches='tight')
            print(f"Saved data flow visualization to {filename}")
            
            # Also save as PNG for easy viewing
            png_filename = f"{self.output_dir}/crod_dataflow_{timestamp}.png"
            plt.savefig(png_filename, format='png', dpi=300, bbox_inches='tight')
            print(f"Saved data flow visualization to {png_filename}")
        
        return fig
    
    def _draw_layer(self, ax, layer, connections):
        """Helper method to draw a layer in the 3D architecture"""
        x = np.linspace(-5, 5, 2)
        y = np.linspace(-3, 3, 2)
        z = layer["z"]
        X, Y = np.meshgrid(x, y)
        Z = np.full_like(X, z)
        
        # Draw the layer
        surf = ax.plot_surface(X, Y, Z, color=layer["color"], alpha=0.7, 
                              edgecolor=self.text_color, linewidth=0.5)
        
        # Add layer name
        ax.text(0, 0, z + 0.1, layer["name"], color=self.text_color, 
               ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Add connections to the list
        if layer["z"] > 1:
            connections.append({
                "x": 0,
                "y": 0,
                "z_from": layer["z"],
                "z_to": layer["z"] - 1,
                "color": layer["color"]
            })
    
    def _draw_connection(self, ax, conn):
        """Helper method to draw a connection between layers"""
        ax.plot([conn["x"], conn["x"]], [conn["y"], conn["y"]], 
                [conn["z_from"], conn["z_to"]], color=conn["color"], 
                linewidth=2, alpha=0.8)

def main():
    parser = argparse.ArgumentParser(description='CROD Architecture Visualizer')
    parser.add_argument('--output-dir', default='../assets/generated',
                        help='Directory where generated SVGs will be saved')
    parser.add_argument('--width', type=int, default=1200,
                        help='Width of the output SVG')
    parser.add_argument('--height', type=int, default=800,
                        help='Height of the output SVG')
    parser.add_argument('--light-mode', action='store_true',
                        help='Use light mode instead of dark mode')
    
    args = parser.parse_args()
    
    visualizer = CRODVisualizer(
        output_dir=args.output_dir,
        width=args.width,
        height=args.height,
        dark_mode=not args.light_mode
    )
    
    print("Generating CROD architecture visualizations...")
    visualizer.create_architecture_3d()
    visualizer.create_polyglot_visualization()
    visualizer.create_dataflow_visualization()
    print("All visualizations generated successfully!")

if __name__ == "__main__":
    main()
