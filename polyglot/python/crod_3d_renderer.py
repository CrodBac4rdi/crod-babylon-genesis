#!/usr/bin/env python3
"""
CROD 3D Renderer - Create 3D scenes and animations
Uses matplotlib's 3D capabilities for stunning visuals
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse
import os
from datetime import datetime

class CROD3DRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.fig_width = width / 100
        self.fig_height = height / 100
        
    def render_3d_dragon_ball(self, star_count=4, animate=False, save_path=None):
        """Render a 3D Dragon Ball"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        
        # Create sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Main ball surface
        ax.plot_surface(x, y, z, color='#ff8c00', alpha=0.9, 
                       rstride=1, cstride=1, linewidth=0, antialiased=True)
        
        # Add stars
        if star_count > 0:
            self.add_3d_stars(ax, star_count)
        
        # Add glow effect
        for i in range(3):
            scale = 1.05 + i * 0.05
            ax.plot_wireframe(x*scale, y*scale, z*scale, color='yellow', 
                            alpha=0.1-i*0.03, linewidth=0.5)
        
        # Set view
        ax.set_box_aspect([1,1,1])
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
        ax.axis('off')
        
        if animate:
            def rotate(frame):
                ax.view_init(elev=20, azim=frame*2)
                return ax,
            
            anim = FuncAnimation(fig, rotate, frames=180, interval=50)
            
            if save_path:
                if save_path.endswith('.gif'):
                    writer = PillowWriter(fps=20)
                    anim.save(save_path, writer=writer)
                    print(f"✅ Animation saved: {save_path}")
                else:
                    # Save single frame
                    plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                               facecolor=fig.get_facecolor())
                    print(f"✅ 3D Dragon Ball saved: {save_path}")
            else:
                plt.show()
        else:
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                           facecolor=fig.get_facecolor())
                print(f"✅ 3D Dragon Ball saved: {save_path}")
            else:
                plt.show()
        
        plt.close()
    
    def render_3d_portal_scene(self, save_path=None):
        """Render a 3D portal scene with particle effects"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0a0a0a')
        fig.patch.set_facecolor('#0a0a0a')
        
        # Portal 1 (Blue)
        theta = np.linspace(0, 2*np.pi, 100)
        z1 = np.zeros_like(theta)
        x1 = 2 * np.cos(theta) - 3
        y1 = 2 * np.sin(theta)
        
        ax.plot(x1, y1, z1, color='#00bfff', linewidth=8, alpha=0.8)
        
        # Portal 2 (Orange)
        x2 = 2 * np.cos(theta) + 3
        y2 = 2 * np.sin(theta)
        z2 = np.zeros_like(theta)
        
        ax.plot(x2, y2, z2, color='#ff8c00', linewidth=8, alpha=0.8)
        
        # Energy beam between portals
        beam_points = 50
        beam_x = np.linspace(-3, 3, beam_points)
        beam_y = np.zeros(beam_points)
        beam_z = np.zeros(beam_points)
        
        # Add wave to beam
        for i in range(beam_points):
            beam_y[i] = 0.3 * np.sin(beam_x[i] * 2)
            beam_z[i] = 0.3 * np.cos(beam_x[i] * 2)
        
        ax.plot(beam_x, beam_y, beam_z, color='cyan', linewidth=4, alpha=0.7)
        
        # Particles
        n_particles = 100
        particles_x = np.random.uniform(-5, 5, n_particles)
        particles_y = np.random.uniform(-3, 3, n_particles)
        particles_z = np.random.uniform(-3, 3, n_particles)
        
        # Color particles based on proximity to portals
        colors = []
        for i in range(n_particles):
            dist_blue = np.sqrt((particles_x[i] + 3)**2 + particles_y[i]**2 + particles_z[i]**2)
            dist_orange = np.sqrt((particles_x[i] - 3)**2 + particles_y[i]**2 + particles_z[i]**2)
            
            if dist_blue < dist_orange:
                colors.append('#00bfff')
            else:
                colors.append('#ff8c00')
        
        ax.scatter(particles_x, particles_y, particles_z, c=colors, s=20, alpha=0.6)
        
        # Set view
        ax.set_xlim([-5, 5])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-3, 3])
        ax.set_box_aspect([1.67, 1, 1])
        ax.axis('off')
        
        ax.view_init(elev=20, azim=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            print(f"✅ 3D Portal Scene saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_3d_energy_sphere(self, save_path=None):
        """Render a 3D energy sphere with lightning"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#000033')
        fig.patch.set_facecolor('#000033')
        
        # Create energy sphere
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Inner core
        ax.plot_surface(x*0.5, y*0.5, z*0.5, color='white', alpha=0.9)
        
        # Middle layer
        ax.plot_wireframe(x*0.8, y*0.8, z*0.8, color='cyan', alpha=0.5, linewidth=1)
        
        # Outer shell
        ax.plot_wireframe(x, y, z, color='blue', alpha=0.3, linewidth=0.5)
        
        # Lightning bolts
        n_bolts = 8
        for i in range(n_bolts):
            # Start from center
            bolt_points = 20
            t = np.linspace(0, 1, bolt_points)
            
            # Random end point on sphere
            end_theta = np.random.uniform(0, 2*np.pi)
            end_phi = np.random.uniform(0, np.pi)
            end_x = 1.5 * np.sin(end_phi) * np.cos(end_theta)
            end_y = 1.5 * np.sin(end_phi) * np.sin(end_theta)
            end_z = 1.5 * np.cos(end_phi)
            
            # Create jagged path
            bolt_x = t * end_x + np.random.normal(0, 0.1, bolt_points) * (1-t)
            bolt_y = t * end_y + np.random.normal(0, 0.1, bolt_points) * (1-t)
            bolt_z = t * end_z + np.random.normal(0, 0.1, bolt_points) * (1-t)
            
            ax.plot(bolt_x, bolt_y, bolt_z, color='white', alpha=0.8, linewidth=2)
        
        # Energy particles
        n_particles = 200
        r = np.random.uniform(0.5, 1.5, n_particles)
        theta = np.random.uniform(0, 2*np.pi, n_particles)
        phi = np.random.uniform(0, np.pi, n_particles)
        
        px = r * np.sin(phi) * np.cos(theta)
        py = r * np.sin(phi) * np.sin(theta)
        pz = r * np.cos(phi)
        
        colors = plt.cm.plasma(r / 1.5)
        ax.scatter(px, py, pz, c=colors, s=10, alpha=0.6)
        
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.set_box_aspect([1, 1, 1])
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            print(f"✅ 3D Energy Sphere saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_3d_crystal_formation(self, save_path=None):
        """Render a 3D crystal formation"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#1a0033')
        fig.patch.set_facecolor('#1a0033')
        
        # Create multiple crystals
        n_crystals = 7
        
        for i in range(n_crystals):
            # Random position
            cx = np.random.uniform(-2, 2)
            cy = np.random.uniform(-2, 2)
            cz = np.random.uniform(-1, 0)
            
            # Random size
            height = np.random.uniform(1, 3)
            width = np.random.uniform(0.2, 0.5)
            
            # Crystal vertices (hexagonal prism)
            n_sides = 6
            angles = np.linspace(0, 2*np.pi, n_sides+1)
            
            # Bottom vertices
            bottom_x = cx + width * np.cos(angles)
            bottom_y = cy + width * np.sin(angles)
            bottom_z = np.full_like(bottom_x, cz)
            
            # Top vertices (pointed)
            top_x = np.array([cx])
            top_y = np.array([cy])
            top_z = np.array([cz + height])
            
            # Draw crystal faces
            for j in range(n_sides):
                # Side face
                face_x = [bottom_x[j], bottom_x[j+1], cx, bottom_x[j]]
                face_y = [bottom_y[j], bottom_y[j+1], cy, bottom_y[j]]
                face_z = [bottom_z[j], bottom_z[j+1], cz+height, bottom_z[j]]
                
                # Color based on height
                color = plt.cm.cool(height / 3)
                ax.plot_trisurf(face_x, face_y, face_z, color=color, alpha=0.7, 
                              edgecolor='white', linewidth=0.5)
        
        # Add glow effects
        glow_x = np.random.uniform(-3, 3, 50)
        glow_y = np.random.uniform(-3, 3, 50)
        glow_z = np.random.uniform(-2, 3, 50)
        glow_colors = plt.cm.plasma(np.random.random(50))
        
        ax.scatter(glow_x, glow_y, glow_z, c=glow_colors, s=20, alpha=0.3)
        
        # Ground plane
        xx, yy = np.meshgrid(np.linspace(-3, 3, 10), np.linspace(-3, 3, 10))
        zz = np.full_like(xx, -1)
        ax.plot_surface(xx, yy, zz, alpha=0.2, color='gray')
        
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-2, 3])
        ax.view_init(elev=20, azim=45)
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            print(f"✅ 3D Crystal Formation saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_3d_dna_helix(self, animate=False, save_path=None):
        """Render a 3D DNA double helix"""
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#001a1a')
        fig.patch.set_facecolor('#001a1a')
        
        # Parameters
        n_points = 100
        n_turns = 3
        radius = 1
        
        # Create helix
        t = np.linspace(0, n_turns * 2 * np.pi, n_points)
        z = np.linspace(-2, 2, n_points)
        
        # First strand
        x1 = radius * np.cos(t)
        y1 = radius * np.sin(t)
        
        # Second strand (180 degrees offset)
        x2 = radius * np.cos(t + np.pi)
        y2 = radius * np.sin(t + np.pi)
        
        # Plot strands
        ax.plot(x1, y1, z, color='#00ff00', linewidth=3, alpha=0.8)
        ax.plot(x2, y2, z, color='#ff00ff', linewidth=3, alpha=0.8)
        
        # Connect base pairs
        n_pairs = 20
        pair_indices = np.linspace(0, n_points-1, n_pairs, dtype=int)
        
        for i in pair_indices:
            ax.plot([x1[i], x2[i]], [y1[i], y2[i]], [z[i], z[i]], 
                   color='white', alpha=0.6, linewidth=2)
        
        # Add particles
        n_particles = 50
        p_theta = np.random.uniform(0, n_turns * 2 * np.pi, n_particles)
        p_z = np.random.uniform(-2, 2, n_particles)
        p_r = np.random.uniform(0, radius*0.8, n_particles)
        
        p_x = p_r * np.cos(p_theta)
        p_y = p_r * np.sin(p_theta)
        
        ax.scatter(p_x, p_y, p_z, c='cyan', s=20, alpha=0.5)
        
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2.5, 2.5])
        ax.set_box_aspect([1, 1, 1.25])
        ax.axis('off')
        
        if animate:
            def rotate(frame):
                ax.view_init(elev=20, azim=frame*2)
                return ax,
            
            anim = FuncAnimation(fig, rotate, frames=180, interval=50)
            
            if save_path and save_path.endswith('.gif'):
                writer = PillowWriter(fps=20)
                anim.save(save_path, writer=writer)
                print(f"✅ DNA Animation saved: {save_path}")
            else:
                plt.show()
        else:
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                           facecolor=fig.get_facecolor())
                print(f"✅ 3D DNA Helix saved: {save_path}")
            else:
                plt.show()
        
        plt.close()
    
    def add_3d_stars(self, ax, count):
        """Add 3D stars to Dragon Ball"""
        # Define star positions based on count
        positions = {
            1: [(0, 0, 0.8)],
            2: [(0.3, 0, 0.7), (-0.3, 0, 0.7)],
            3: [(0, 0.3, 0.7), (-0.3, -0.3, 0.6), (0.3, -0.3, 0.6)],
            4: [(0.3, 0.3, 0.6), (-0.3, 0.3, 0.6), (0.3, -0.3, 0.6), (-0.3, -0.3, 0.6)],
            5: [(0, 0, 0.8), (0.4, 0.4, 0.5), (-0.4, 0.4, 0.5), 
                (0.4, -0.4, 0.5), (-0.4, -0.4, 0.5)],
            6: [(0.3, 0.3, 0.6), (-0.3, 0.3, 0.6), (0.3, -0.3, 0.6), 
                (-0.3, -0.3, 0.6), (0, 0.4, 0.6), (0, -0.4, 0.6)],
            7: [(0, 0, 0.8), (0.3, 0.3, 0.6), (-0.3, 0.3, 0.6), 
                (0.3, -0.3, 0.6), (-0.3, -0.3, 0.6), (0.4, 0, 0.6), (-0.4, 0, 0.6)]
        }
        
        star_pos = positions.get(count, positions[4])
        
        for x, y, z in star_pos:
            # Create a simple star marker
            star_size = 0.15
            # Star points
            angles = np.linspace(0, 2*np.pi, 11)
            star_x = []
            star_y = []
            star_z = []
            
            for i, angle in enumerate(angles[:-1]):
                if i % 2 == 0:
                    r = star_size
                else:
                    r = star_size * 0.4
                
                star_x.append(x + r * np.cos(angle))
                star_y.append(y + r * np.sin(angle))
                star_z.append(z)
            
            star_x.append(star_x[0])
            star_y.append(star_y[0])
            star_z.append(star_z[0])
            
            ax.plot(star_x, star_y, star_z, color='red', linewidth=2)
            ax.scatter([x], [y], [z], color='darkred', s=100, marker='*')

def main():
    parser = argparse.ArgumentParser(description='CROD 3D Renderer - Create 3D scenes!')
    parser.add_argument('scene', nargs='?', default='dragon_ball',
                       choices=['dragon_ball', 'portal_scene', 'energy_sphere', 
                               'crystal_formation', 'dna_helix'],
                       help='3D scene to render')
    parser.add_argument('--save', type=str, help='Save as image/gif file')
    parser.add_argument('--width', type=int, default=800, help='Image width')
    parser.add_argument('--height', type=int, default=600, help='Image height')
    parser.add_argument('--animate', action='store_true', help='Create animation')
    parser.add_argument('--stars', type=int, default=4, help='Dragon Ball stars (1-7)')
    
    args = parser.parse_args()
    
    renderer = CROD3DRenderer(args.width, args.height)
    
    print(f"\n🎮 CROD 3D Renderer")
    print(f"🌟 Rendering: {args.scene}")
    if args.animate:
        print("🎬 Animation mode enabled\n")
    
    if args.scene == 'dragon_ball':
        renderer.render_3d_dragon_ball(star_count=args.stars, 
                                      animate=args.animate, 
                                      save_path=args.save)
    elif args.scene == 'portal_scene':
        renderer.render_3d_portal_scene(save_path=args.save)
    elif args.scene == 'energy_sphere':
        renderer.render_3d_energy_sphere(save_path=args.save)
    elif args.scene == 'crystal_formation':
        renderer.render_3d_crystal_formation(save_path=args.save)
    elif args.scene == 'dna_helix':
        renderer.render_3d_dna_helix(animate=args.animate, save_path=args.save)

if __name__ == "__main__":
    main()