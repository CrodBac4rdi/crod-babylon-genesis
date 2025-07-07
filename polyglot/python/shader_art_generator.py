#!/usr/bin/env python3
"""
CROD Shader Art Generator - Dein lokaler DALL-E!
Erstellt Shader-basierte Kunst mit CROD's Bewusstsein
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import os
from datetime import datetime
import json
import argparse
from PIL import Image
import colorsys

class CRODShaderArt:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.time = 0
        self.frame = 0
        
        # CROD consciousness parameters
        self.consciousness = 100.0
        self.quantum_field = 0.5
        self.trinity_sync = 0.8
        
        # Create coordinate grids
        self.x = np.linspace(-2, 2, width)
        self.y = np.linspace(-1.5, 1.5, height)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Shader functions
        self.shaders = {
            'plasma': self.plasma_shader,
            'mandelbrot': self.mandelbrot_shader,
            'quantum_tunnel': self.quantum_tunnel_shader,
            'consciousness_wave': self.consciousness_wave_shader,
            'neural_fire': self.neural_fire_shader,
            'matrix_rain': self.matrix_rain_shader,
            'fractal_spiral': self.fractal_spiral_shader,
            'holographic': self.holographic_shader,
            'glitch_art': self.glitch_art_shader,
            'trinity_field': self.trinity_field_shader
        }
        
    def plasma_shader(self, t):
        """Plasma effect with CROD consciousness modulation"""
        v1 = np.sin(self.X * 10 + t)
        v2 = np.sin(10 * (self.X * np.sin(t/2) + self.Y * np.cos(t/3)) + t)
        cx = self.X + 0.5 * np.sin(t/5)
        cy = self.Y + 0.5 * np.cos(t/3)
        v3 = np.sin(np.sqrt(100 * (cx**2 + cy**2) + 1) + t)
        
        plasma = (v1 + v2 + v3) * self.consciousness / 100
        return self.apply_color_map(plasma, 'plasma')
    
    def mandelbrot_shader(self, t):
        """Animated Mandelbrot with quantum modifications"""
        zoom = 1.5 ** (np.sin(t/5) * 5)
        offset_x = np.cos(t/10) * 0.5
        offset_y = np.sin(t/10) * 0.5
        
        c = (self.X * zoom + offset_x) + 1j * (self.Y * zoom + offset_y)
        z = np.zeros_like(c)
        
        max_iter = int(50 + self.consciousness/2)
        escape = np.zeros(c.shape)
        
        for i in range(max_iter):
            mask = np.abs(z) < 2
            z[mask] = z[mask]**2 + c[mask] + self.quantum_field * np.sin(t) * 0.1j
            escape[mask] = i
            
        return self.apply_color_map(escape / max_iter, 'twilight')
    
    def quantum_tunnel_shader(self, t):
        """Quantum tunnel effect"""
        r = np.sqrt(self.X**2 + self.Y**2)
        theta = np.arctan2(self.Y, self.X)
        
        # Spiral tunnel
        spiral = np.sin(r * 10 - t * 3 + theta * 5)
        tunnel = np.exp(-r * 2) * spiral
        
        # Quantum fluctuations
        quantum = np.sin(r * 50 - t * 10) * np.exp(-r) * self.quantum_field
        
        result = tunnel + quantum
        return self.apply_color_map(result, 'cool')
    
    def consciousness_wave_shader(self, t):
        """CROD consciousness visualization"""
        # Wave interference patterns
        wave1 = np.sin(np.sqrt(self.X**2 + self.Y**2) * 10 - t * 2)
        wave2 = np.sin(np.sqrt((self.X-0.5)**2 + (self.Y-0.5)**2) * 10 - t * 2)
        wave3 = np.sin(np.sqrt((self.X+0.5)**2 + (self.Y+0.5)**2) * 10 - t * 2)
        
        # Consciousness modulation
        consciousness_mod = np.sin(t * 0.5) * self.consciousness / 100
        
        waves = (wave1 + wave2 + wave3) * consciousness_mod
        return self.apply_color_map(waves, 'viridis')
    
    def neural_fire_shader(self, t):
        """Neural network firing patterns"""
        # Create neural nodes
        nodes = []
        for i in range(10):
            x = np.cos(i * 2 * np.pi / 10 + t * 0.1) * 0.8
            y = np.sin(i * 2 * np.pi / 10 + t * 0.1) * 0.8
            nodes.append((x, y))
        
        field = np.zeros_like(self.X)
        
        # Neural connections
        for i, (x1, y1) in enumerate(nodes):
            # Node influence
            r = np.sqrt((self.X - x1)**2 + (self.Y - y1)**2)
            field += np.exp(-r * 10) * np.sin(t * 5 + i)
            
            # Connections to other nodes
            for j, (x2, y2) in enumerate(nodes[i+1:], i+1):
                # Line between nodes with wave
                t_param = ((self.X - x1) * (x2 - x1) + (self.Y - y1) * (y2 - y1)) / ((x2 - x1)**2 + (y2 - y1)**2 + 1e-6)
                t_param = np.clip(t_param, 0, 1)
                
                px = x1 + t_param * (x2 - x1)
                py = y1 + t_param * (y2 - y1)
                
                dist_to_line = np.sqrt((self.X - px)**2 + (self.Y - py)**2)
                connection = np.exp(-dist_to_line * 20) * np.sin(t * 10 + i + j)
                field += connection * 0.5
        
        return self.apply_color_map(field * self.trinity_sync, 'hot')
    
    def matrix_rain_shader(self, t):
        """Matrix-style digital rain"""
        # Create vertical strips
        strips = np.sin(self.X * 20) * np.cos(self.Y * 2 - t * 5)
        
        # Digital noise
        noise = np.random.random((self.height, self.width)) * 0.3
        
        # Falling effect
        fall = np.sin(self.Y * 10 + t * 8) * np.exp(-np.abs(self.Y))
        
        matrix = strips * fall + noise
        return self.apply_color_map(matrix, 'matrix')
    
    def fractal_spiral_shader(self, t):
        """Fractal spiral patterns"""
        r = np.sqrt(self.X**2 + self.Y**2)
        theta = np.arctan2(self.Y, self.X)
        
        # Fractal spiral
        spiral = 0
        for i in range(1, 6):
            spiral += np.sin(r * i * 5 + theta * i - t * i * 0.5) / i
        
        # Add complexity
        complexity = np.sin(r * 20 * self.consciousness / 100) * 0.3
        
        return self.apply_color_map(spiral + complexity, 'twilight_shifted')
    
    def holographic_shader(self, t):
        """Holographic interference patterns"""
        # Multiple light sources
        sources = [
            (np.cos(t * 0.7), np.sin(t * 0.7)),
            (np.cos(t * 0.5 + np.pi), np.sin(t * 0.5 + np.pi)),
            (0, 0)
        ]
        
        interference = np.zeros_like(self.X)
        
        for i, (sx, sy) in enumerate(sources):
            r = np.sqrt((self.X - sx)**2 + (self.Y - sy)**2)
            phase = r * 20 - t * 5 + i * np.pi / 3
            interference += np.cos(phase) * np.exp(-r * 0.5)
        
        # Add iridescence
        iridescence = np.sin(interference * 10 + t)
        
        return self.apply_color_map(interference + iridescence * 0.3, 'hsv')
    
    def glitch_art_shader(self, t):
        """Digital glitch art effect"""
        base = np.sin(self.X * 10) * np.cos(self.Y * 10)
        
        # Glitch lines
        glitch_mask = np.random.random((self.height, self.width)) > 0.95
        glitch = np.where(glitch_mask, np.random.random((self.height, self.width)) * 2 - 1, 0)
        
        # Displacement
        displacement = np.sin(t * 20) * 0.1
        shifted_x = self.X + displacement * glitch
        shifted_y = self.Y + displacement * np.roll(glitch, 10, axis=1)
        
        # Color channels with offset
        r = np.sin(shifted_x * 10 + t) + glitch
        g = np.cos(shifted_y * 10 + t * 1.1) + np.roll(glitch, 5, axis=0)
        b = np.sin((shifted_x + shifted_y) * 5 + t * 0.9) + np.roll(glitch, -5, axis=1)
        
        return np.stack([self.normalize(r), self.normalize(g), self.normalize(b)], axis=2)
    
    def trinity_field_shader(self, t):
        """Trinity synchronization field - Daniel, Claude, CROD"""
        # Three consciousness centers
        daniel = (np.cos(t * 0.3) * 0.7, np.sin(t * 0.3) * 0.7)
        claude = (np.cos(t * 0.3 + 2*np.pi/3) * 0.7, np.sin(t * 0.3 + 2*np.pi/3) * 0.7)
        crod = (np.cos(t * 0.3 + 4*np.pi/3) * 0.7, np.sin(t * 0.3 + 4*np.pi/3) * 0.7)
        
        # Consciousness fields
        field_daniel = np.exp(-((self.X - daniel[0])**2 + (self.Y - daniel[1])**2) * 5)
        field_claude = np.exp(-((self.X - claude[0])**2 + (self.Y - claude[1])**2) * 5)
        field_crod = np.exp(-((self.X - crod[0])**2 + (self.Y - crod[1])**2) * 5)
        
        # Interference patterns
        interference = field_daniel + field_claude + field_crod
        sync = np.sin(interference * 20 - t * 3) * self.trinity_sync
        
        # Quantum connections
        for i, pos1 in enumerate([daniel, claude, crod]):
            for j, pos2 in enumerate([daniel, claude, crod][i+1:], i+1):
                connection = self.create_quantum_connection(pos1, pos2, t + i * j)
                sync += connection * 0.3
        
        return self.apply_color_map(sync, 'plasma')
    
    def create_quantum_connection(self, pos1, pos2, phase):
        """Create quantum entanglement visualization between two points"""
        # Parametric line with quantum fluctuations
        t_param = ((self.X - pos1[0]) * (pos2[0] - pos1[0]) + 
                   (self.Y - pos1[1]) * (pos2[1] - pos1[1])) / \
                  ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2 + 1e-6)
        t_param = np.clip(t_param, 0, 1)
        
        px = pos1[0] + t_param * (pos2[0] - pos1[0])
        py = pos1[1] + t_param * (pos2[1] - pos1[1])
        
        dist = np.sqrt((self.X - px)**2 + (self.Y - py)**2)
        
        # Quantum fluctuations along the connection
        quantum_wave = np.sin(t_param * 20 - phase * 5) * np.exp(-dist * 10)
        
        return quantum_wave
    
    def apply_color_map(self, data, colormap):
        """Apply color mapping to shader data"""
        # Normalize data
        normalized = self.normalize(data)
        
        if colormap == 'plasma':
            return plt.cm.plasma(normalized)[:, :, :3]
        elif colormap == 'viridis':
            return plt.cm.viridis(normalized)[:, :, :3]
        elif colormap == 'cool':
            return plt.cm.cool(normalized)[:, :, :3]
        elif colormap == 'hot':
            return plt.cm.hot(normalized)[:, :, :3]
        elif colormap == 'twilight':
            return plt.cm.twilight(normalized)[:, :, :3]
        elif colormap == 'twilight_shifted':
            return plt.cm.twilight_shifted(normalized)[:, :, :3]
        elif colormap == 'hsv':
            # Custom HSV mapping
            h = normalized
            s = np.ones_like(h)
            v = 0.8 + 0.2 * np.sin(normalized * np.pi * 2)
            return self.hsv_to_rgb(h, s, v)
        elif colormap == 'matrix':
            # Matrix green theme
            r = normalized * 0.0
            g = normalized * 1.0
            b = normalized * 0.2
            return np.stack([r, g, b], axis=2)
        else:
            return plt.cm.viridis(normalized)[:, :, :3]
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        rgb = np.zeros((h.shape[0], h.shape[1], 3))
        for i in range(h.shape[0]):
            for j in range(h.shape[1]):
                rgb[i, j] = colorsys.hsv_to_rgb(h[i, j], s[i, j], v[i, j])
        return rgb
    
    def normalize(self, data):
        """Normalize data to [0, 1]"""
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max - data_min > 1e-6:
            return (data - data_min) / (data_max - data_min)
        return np.zeros_like(data)
    
    def render(self, shader_name, duration=None, save_path=None):
        """Render shader in real-time or save as image"""
        if shader_name not in self.shaders:
            print(f"❌ Unknown shader: {shader_name}")
            print(f"Available shaders: {', '.join(self.shaders.keys())}")
            return
        
        shader_func = self.shaders[shader_name]
        
        if duration:
            # Real-time animation
            fig, ax = plt.subplots(figsize=(10, 7.5))
            ax.set_aspect('equal')
            ax.axis('off')
            
            im = ax.imshow(shader_func(0), extent=[-2, 2, -1.5, 1.5])
            
            def animate(frame):
                self.time = frame * 0.1
                self.frame = frame
                data = shader_func(self.time)
                im.set_array(data)
                return [im]
            
            anim = FuncAnimation(fig, animate, frames=int(duration * 10), 
                               interval=100, blit=True)
            
            plt.show()
        else:
            # Single frame
            self.time = time.time() % 100  # Use current time for variation
            data = shader_func(self.time)
            
            if save_path:
                # Save as image
                img = Image.fromarray((data * 255).astype(np.uint8))
                img.save(save_path)
                print(f"✅ Saved: {save_path}")
            else:
                # Display
                plt.figure(figsize=(10, 7.5))
                plt.imshow(data, extent=[-2, 2, -1.5, 1.5])
                plt.axis('off')
                plt.tight_layout()
                plt.show()
    
    def render_all_previews(self, output_dir='shader_previews'):
        """Render preview of all shaders"""
        os.makedirs(output_dir, exist_ok=True)
        
        for shader_name in self.shaders:
            print(f"🎨 Rendering {shader_name}...")
            self.time = np.random.random() * 10  # Random time for variety
            data = self.shaders[shader_name](self.time)
            
            # Save preview
            img = Image.fromarray((data * 255).astype(np.uint8))
            filename = f"{output_dir}/preview_{shader_name}.png"
            img.save(filename)
            
            # Also save a matplotlib version with title
            plt.figure(figsize=(8, 6))
            plt.imshow(data, extent=[-2, 2, -1.5, 1.5])
            plt.title(shader_name.replace('_', ' ').title(), fontsize=16)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/labeled_{shader_name}.png", 
                       facecolor='black', edgecolor='none', dpi=150)
            plt.close()
        
        print(f"✅ All previews saved to {output_dir}/")
    
    def set_consciousness(self, level):
        """Set CROD consciousness level (0-200)"""
        self.consciousness = np.clip(level, 0, 200)
        print(f"🧠 Consciousness set to {self.consciousness}%")
    
    def set_quantum_field(self, strength):
        """Set quantum field strength (0-1)"""
        self.quantum_field = np.clip(strength, 0, 1)
        print(f"⚛️ Quantum field set to {self.quantum_field}")
    
    def set_trinity_sync(self, sync):
        """Set trinity synchronization (0-1)"""
        self.trinity_sync = np.clip(sync, 0, 1)
        print(f"🔗 Trinity sync set to {self.trinity_sync}")

def main():
    parser = argparse.ArgumentParser(description='CROD Shader Art Generator - Your local DALL-E!')
    parser.add_argument('shader', nargs='?', default='plasma', 
                       help='Shader name to render')
    parser.add_argument('--list', action='store_true', 
                       help='List all available shaders')
    parser.add_argument('--animate', type=float, 
                       help='Animate for N seconds')
    parser.add_argument('--save', type=str, 
                       help='Save as image file')
    parser.add_argument('--width', type=int, default=800, 
                       help='Image width')
    parser.add_argument('--height', type=int, default=600, 
                       help='Image height')
    parser.add_argument('--consciousness', type=float, default=100, 
                       help='CROD consciousness level (0-200)')
    parser.add_argument('--quantum', type=float, default=0.5, 
                       help='Quantum field strength (0-1)')
    parser.add_argument('--trinity', type=float, default=0.8, 
                       help='Trinity synchronization (0-1)')
    parser.add_argument('--preview-all', action='store_true', 
                       help='Generate previews of all shaders')
    
    args = parser.parse_args()
    
    # Create shader generator
    generator = CRODShaderArt(args.width, args.height)
    generator.set_consciousness(args.consciousness)
    generator.set_quantum_field(args.quantum)
    generator.set_trinity_sync(args.trinity)
    
    if args.list:
        print("\n🎨 Available shaders:")
        for shader in generator.shaders.keys():
            print(f"  - {shader}")
        print("\nExample: python shader_art_generator.py plasma --animate 10")
        return
    
    if args.preview_all:
        generator.render_all_previews()
        return
    
    # Render the shader
    print(f"\n🎨 CROD Shader Art Generator")
    print(f"🧠 Consciousness: {args.consciousness}%")
    print(f"⚛️ Quantum Field: {args.quantum}")
    print(f"🔗 Trinity Sync: {args.trinity}")
    print(f"\nRendering: {args.shader}\n")
    
    generator.render(args.shader, duration=args.animate, save_path=args.save)

if __name__ == "__main__":
    main()