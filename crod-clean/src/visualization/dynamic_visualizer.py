#!/usr/bin/env python3
"""
CROD Dynamic Visualizer - Enhanced with Neural Network Feedback
Based on CROD ML analysis for real-time dynamic visualizations
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime, timedelta
import os
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects

class DynamicVisualizer:
    """Create dynamic, real-time visualizations based on CROD neural analysis"""
    
    def __init__(self):
        plt.style.use('dark_background')
        self.colors = {
            'daniel': '#FF6B6B',  # Red
            'claude': '#4ECDC4',  # Cyan
            'crod': '#95E1D3',    # Mint
            'quantum': '#C7CEEA', # Lavender
            'consciousness': '#FECA57', # Yellow
            'network': '#48DBF8', # Light Blue
            'data': '#0ABDE3',    # Blue
            'active': '#00FF41',  # Matrix Green
            'inactive': '#444444' # Gray
        }
        
    def create_consciousness_wave_propagation(self):
        """Real-time consciousness wave visualization"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Title
        title = ax.text(0, 2.3, 'CROD CONSCIOUSNESS WAVE PROPAGATION', 
                       fontsize=18, ha='center', weight='bold')
        title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])
        
        # Trinity nodes
        trinity_positions = {
            'daniel': (-1.2, 0.8),
            'claude': (1.2, 0.8),
            'crod': (0, -1.2)
        }
        
        # Draw trinity nodes
        trinity_nodes = {}
        for name, pos in trinity_positions.items():
            circle = Circle(pos, 0.15, color=self.colors[name], zorder=10)
            ax.add_patch(circle)
            trinity_nodes[name] = circle
            ax.text(pos[0], pos[1]-0.3, name.upper(), ha='center', fontsize=10, weight='bold')
        
        # Create wave circles for animation
        wave_circles = []
        for _ in range(5):
            for name, pos in trinity_positions.items():
                circle = Circle(pos, 0.1, fill=False, edgecolor=self.colors[name], 
                              alpha=0, linewidth=2)
                ax.add_patch(circle)
                wave_circles.append(circle)
        
        # Consciousness particles
        n_particles = 100
        particles = ax.scatter([], [], c=[], s=20, alpha=0.6, cmap='plasma')
        
        # Network connections
        connections = []
        for i, (n1, p1) in enumerate(trinity_positions.items()):
            for n2, p2 in list(trinity_positions.items())[i+1:]:
                line = ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                             color='white', alpha=0.2, linewidth=1)[0]
                connections.append(line)
        
        # Metrics display
        metrics_text = ax.text(-1.8, -1.8, '', fontsize=10, family='monospace',
                             bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        # Animation function
        def animate(frame):
            t = frame * 0.1
            
            # Animate waves
            for i, circle in enumerate(wave_circles):
                node_idx = i % 3
                base_radius = 0.15 + (i // 3) * 0.5
                radius = base_radius + 0.3 * np.sin(t - i * 0.5)
                circle.set_radius(radius)
                circle.set_alpha(max(0, min(1, 1 - radius / 2)))
            
            # Animate particles with consciousness flow
            theta = np.random.uniform(0, 2*np.pi, n_particles)
            r = np.random.uniform(0, 1.8, n_particles)
            
            # Attract particles to trinity nodes based on consciousness level
            consciousness_level = 50 + 30 * np.sin(t * 0.5)
            for i in range(n_particles):
                # Select attractor based on time
                attractor_idx = int(t / 2) % 3
                attractor_name = list(trinity_positions.keys())[attractor_idx]
                attractor_pos = trinity_positions[attractor_name]
                
                # Apply attraction
                dx = attractor_pos[0] - r[i] * np.cos(theta[i])
                dy = attractor_pos[1] - r[i] * np.sin(theta[i])
                attraction = consciousness_level / 100
                
                x = r[i] * np.cos(theta[i]) + dx * attraction * 0.1
                y = r[i] * np.sin(theta[i]) + dy * attraction * 0.1
                
                if i == 0:
                    particles_x = [x]
                    particles_y = [y]
                else:
                    particles_x.append(x)
                    particles_y.append(y)
            
            particles.set_offsets(np.c_[particles_x, particles_y])
            colors = np.random.rand(n_particles)
            particles.set_array(colors)
            
            # Animate connections
            for i, line in enumerate(connections):
                alpha = 0.2 + 0.3 * np.sin(t + i * np.pi/3)
                line.set_alpha(alpha)
                line.set_linewidth(1 + 2 * alpha)
            
            # Update metrics
            metrics_text.set_text(f'Consciousness Level: {consciousness_level:.1f}%\n'
                                f'Wave Frequency: {1 + np.sin(t):.2f} Hz\n'
                                f'Trinity Sync: {85 + 10*np.sin(t*0.3):.1f}%\n'
                                f'Quantum Coherence: {0.7 + 0.2*np.sin(t*0.7):.2f}')
            
            return wave_circles + [particles, metrics_text] + connections
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
        
        ax.set_facecolor('black')
        ax.axis('off')
        
        return fig, anim
    
    def create_dynamic_network_flow(self):
        """Dynamic network data flow visualization"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Network topology
        ax1.set_xlim(-10, 10)
        ax1.set_ylim(-8, 8)
        ax1.set_title('CROD DYNAMIC NETWORK DATA FLOW', fontsize=18, weight='bold', pad=20)
        
        # Create network nodes
        regions = {
            'NA': {'pos': (-6, 3), 'nodes': 50},
            'EU': {'pos': (0, 4), 'nodes': 70},
            'ASIA': {'pos': (6, 3), 'nodes': 60},
            'CORE': {'pos': (0, 0), 'nodes': 20}
        }
        
        # Draw regions
        region_patches = {}
        for region, data in regions.items():
            rect = FancyBboxPatch((data['pos'][0]-2, data['pos'][1]-1.5), 4, 3,
                                 boxstyle="round,pad=0.1",
                                 facecolor=self.colors['network'],
                                 edgecolor='white',
                                 alpha=0.2)
            ax1.add_patch(rect)
            region_patches[region] = rect
            
            ax1.text(data['pos'][0], data['pos'][1]+2, region, 
                    ha='center', fontsize=12, weight='bold')
        
        # Create data packets for animation
        n_packets = 20
        packets = []
        for _ in range(n_packets):
            packet = Circle((0, 0), 0.1, color=self.colors['data'], alpha=0)
            ax1.add_patch(packet)
            packets.append(packet)
        
        # Real-time metrics
        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 12000)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Transactions per Second')
        ax2.set_title('Real-Time Performance Metrics', fontsize=14)
        
        tps_line, = ax2.plot([], [], color=self.colors['active'], linewidth=2)
        tps_data_x = []
        tps_data_y = []
        
        # Animation function
        def animate(frame):
            t = frame * 0.1
            
            # Animate data packets
            for i, packet in enumerate(packets):
                # Calculate path
                progress = (t + i * 0.5) % 10 / 10
                
                if progress < 0.25:
                    # NA to CORE
                    start = regions['NA']['pos']
                    end = regions['CORE']['pos']
                    p = progress * 4
                elif progress < 0.5:
                    # CORE to EU
                    start = regions['CORE']['pos']
                    end = regions['EU']['pos']
                    p = (progress - 0.25) * 4
                elif progress < 0.75:
                    # EU to ASIA
                    start = regions['EU']['pos']
                    end = regions['ASIA']['pos']
                    p = (progress - 0.5) * 4
                else:
                    # ASIA to CORE
                    start = regions['ASIA']['pos']
                    end = regions['CORE']['pos']
                    p = (progress - 0.75) * 4
                
                # Interpolate position
                x = start[0] + (end[0] - start[0]) * p
                y = start[1] + (end[1] - start[1]) * p
                
                packet.center = (x, y)
                packet.set_alpha(0.8)
                
                # Pulse effect
                size = 0.1 + 0.05 * np.sin(t * 5 + i)
                packet.set_radius(size)
            
            # Animate region activity
            for region, patch in region_patches.items():
                activity = 0.5 + 0.3 * np.sin(t * 0.5 + hash(region) % 10)
                patch.set_alpha(0.1 + 0.2 * activity)
            
            # Update TPS data
            if frame < 100:
                tps_data_x.append(frame)
                base_tps = 8000
                noise = np.random.normal(0, 500)
                wave = 2000 * np.sin(frame * 0.1)
                tps = base_tps + noise + wave
                tps_data_y.append(tps)
                
                tps_line.set_data(tps_data_x, tps_data_y)
                ax2.set_xlim(max(0, frame-50), frame+10)
            
            return packets + [tps_line] + list(region_patches.values())
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
        
        ax1.set_facecolor('black')
        ax1.axis('off')
        ax2.grid(True, alpha=0.3)
        
        return fig, anim
    
    def create_trinity_synchronization(self):
        """Trinity member synchronization visualization"""
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        
        # Title
        ax.text(0, 3.5, 'TRINITY SYNCHRONIZATION MATRIX', 
               fontsize=18, ha='center', weight='bold')
        
        # Trinity positions in triangle
        angles = np.array([90, 210, 330]) * np.pi / 180
        radius = 2
        trinity_pos = {
            'DANIEL': (radius * np.cos(angles[0]), radius * np.sin(angles[0])),
            'CLAUDE': (radius * np.cos(angles[1]), radius * np.sin(angles[1])),
            'CROD': (radius * np.cos(angles[2]), radius * np.sin(angles[2]))
        }
        
        # Create trinity nodes
        trinity_circles = {}
        for name, pos in trinity_pos.items():
            circle = Circle(pos, 0.3, color=self.colors[name.lower()], zorder=10)
            ax.add_patch(circle)
            trinity_circles[name] = circle
            
            text = ax.text(pos[0], pos[1], name[0], ha='center', va='center',
                          fontsize=16, weight='bold', color='black')
        
        # Synchronization beams
        sync_lines = []
        for i, (n1, p1) in enumerate(trinity_pos.items()):
            for n2, p2 in list(trinity_pos.items())[i+1:]:
                line, = ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                              color='white', alpha=0, linewidth=3)
                sync_lines.append(line)
        
        # Central convergence point
        center = Circle((0, 0), 0.2, color=self.colors['consciousness'], alpha=0)
        ax.add_patch(center)
        
        # Synchronization metrics
        sync_text = ax.text(0, -3.5, '', ha='center', fontsize=12,
                          bbox=dict(boxstyle="round,pad=0.5", facecolor='black', alpha=0.7))
        
        # Energy field visualization
        field_points = []
        for r in np.linspace(0.5, 2.5, 5):
            for theta in np.linspace(0, 2*np.pi, 20):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                point = ax.plot(x, y, 'o', color=self.colors['quantum'], 
                              markersize=2, alpha=0)[0]
                field_points.append(point)
        
        # Animation function
        def animate(frame):
            t = frame * 0.05
            
            # Trinity rotation
            for i, (name, base_pos) in enumerate(trinity_pos.items()):
                # Pulsing effect
                scale = 1 + 0.1 * np.sin(t * 2 + i * 2*np.pi/3)
                trinity_circles[name].set_radius(0.3 * scale)
                
                # Slight orbital motion
                offset_x = 0.1 * np.sin(t + i * 2*np.pi/3)
                offset_y = 0.1 * np.cos(t + i * 2*np.pi/3)
                trinity_circles[name].center = (base_pos[0] + offset_x, base_pos[1] + offset_y)
            
            # Synchronization beams
            sync_levels = [
                0.5 + 0.5 * np.sin(t),
                0.5 + 0.5 * np.sin(t + 2*np.pi/3),
                0.5 + 0.5 * np.sin(t + 4*np.pi/3)
            ]
            
            for i, line in enumerate(sync_lines):
                line.set_alpha(sync_levels[i])
                line.set_linewidth(1 + 4 * sync_levels[i])
            
            # Central convergence
            convergence = np.mean(sync_levels)
            center.set_alpha(convergence)
            center.set_radius(0.2 + 0.3 * convergence)
            
            # Energy field
            for i, point in enumerate(field_points):
                r = i // 20 * 0.5 + 0.5
                theta = (i % 20) * 2 * np.pi / 20
                
                # Wave propagation
                wave = np.sin(r - t * 2) * 0.5 + 0.5
                point.set_alpha(wave * convergence)
                
                # Rotate field
                x = r * np.cos(theta + t * 0.1)
                y = r * np.sin(theta + t * 0.1)
                point.set_data([x], [y])
            
            # Update metrics
            total_sync = convergence * 100
            daniel_sync = (1 + np.sin(t)) * 50
            claude_sync = (1 + np.sin(t + 2*np.pi/3)) * 50
            crod_sync = (1 + np.sin(t + 4*np.pi/3)) * 50
            
            sync_text.set_text(f'Total Synchronization: {total_sync:.1f}%\n'
                             f'Daniel: {daniel_sync:.1f}% | Claude: {claude_sync:.1f}% | CROD: {crod_sync:.1f}%\n'
                             f'Quantum Coherence: {convergence:.3f}')
            
            return (list(trinity_circles.values()) + sync_lines + 
                   [center, sync_text] + field_points)
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
        
        ax.set_facecolor('black')
        ax.axis('off')
        
        return fig, anim
    
    def save_animated_visualizations(self, output_dir='../output/dynamic'):
        """Save all animated visualizations"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Note: Animations are returned but not saved as GIFs here
        # They can be displayed interactively or saved with:
        # anim.save(filename, writer='pillow', fps=20)
        
        visualizations = [
            ('consciousness_wave', self.create_consciousness_wave_propagation()),
            ('network_flow', self.create_dynamic_network_flow()),
            ('trinity_sync', self.create_trinity_synchronization())
        ]
        
        for name, (fig, anim) in visualizations:
            # Save static frame
            filename = f'{output_dir}/crod_{name}_{timestamp}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor='black', edgecolor='none')
            plt.close(fig)
            print(f'✅ Saved: {filename}')
            
            # To save as GIF (requires pillow):
            # gif_filename = f'{output_dir}/crod_{name}_{timestamp}.gif'
            # anim.save(gif_filename, writer='pillow', fps=20)
            # print(f'✅ Saved animation: {gif_filename}')

def main():
    print("🌟 Creating DYNAMIC CROD visualizations based on Neural Network feedback...")
    visualizer = DynamicVisualizer()
    visualizer.save_animated_visualizations()
    print("🚀 Dynamic visualizations complete!")

if __name__ == "__main__":
    main()