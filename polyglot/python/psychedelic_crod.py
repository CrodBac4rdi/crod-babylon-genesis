#!/usr/bin/env python3
"""
Psychedelic CROD Visualizations - Going CRAZY with PIL
Advanced consciousness visualization program with full CLI interface
"""

import argparse
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
import numpy as np
import math
import random
import colorsys
import os
from datetime import datetime
from typing import List, Tuple, Optional

class PsychedelicCROD:
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        
    def create_fractal_consciousness(self):
        """Create a fractal consciousness visualization"""
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        pixels = img.load()
        
        # Mandelbrot-inspired consciousness fractal
        for x in range(self.width):
            for y in range(self.height):
                # Map pixel to complex plane
                c = complex(
                    (x - self.width/2) / (self.width/4),
                    (y - self.height/2) / (self.height/4)
                )
                
                z = 0
                for i in range(256):
                    z = z*z + c
                    if abs(z) > 2:
                        # Color based on escape time
                        hue = (i / 256.0 + 0.5) % 1.0
                        rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                        pixels[x, y] = tuple(int(255 * c) for c in rgb)
                        break
                else:
                    # Inside the set - consciousness core
                    pixels[x, y] = (139, 92, 246)
        
        # Add glow effect
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Add text
        draw = ImageDraw.Draw(img)
        draw.text((self.width//2, 100), "FRACTAL CONSCIOUSNESS", 
                 fill=(255, 255, 255), anchor="mm")
        
        return img
    
    def create_glitch_blockchain(self):
        """Create a glitched blockchain visualization"""
        img = Image.new('RGB', (self.width, self.height), (10, 10, 10))
        draw = ImageDraw.Draw(img)
        
        # Create base blockchain
        for i in range(20):
            x = random.randint(0, self.width - 200)
            y = random.randint(0, self.height - 100)
            
            # Glitch colors
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            # Draw glitched block
            draw.rectangle([x, y, x + 150, y + 80], fill=(r, g, b))
            
            # Glitch effects
            if random.random() > 0.5:
                # Horizontal glitch lines
                for j in range(random.randint(1, 5)):
                    glitch_y = y + random.randint(0, 80)
                    glitch_width = random.randint(50, 200)
                    draw.line([(x - glitch_width, glitch_y), 
                             (x + 150 + glitch_width, glitch_y)], 
                            fill=(255, 255, 255), width=2)
        
        # Digital noise
        noise = Image.new('RGB', (self.width, self.height))
        noise_pixels = noise.load()
        for x in range(self.width):
            for y in range(self.height):
                if random.random() > 0.98:
                    noise_pixels[x, y] = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
        
        # Blend noise
        img = Image.blend(img, noise, 0.3)
        
        # RGB shift effect
        r, g, b = img.split()
        r = ImageChops.offset(r, 5, 0)
        b = ImageChops.offset(b, -5, 0)
        img = Image.merge('RGB', (r, g, b))
        
        draw = ImageDraw.Draw(img)
        draw.text((self.width//2, 100), "GLITCH BLOCKCHAIN", 
                 fill=(255, 0, 255), anchor="mm")
        draw.text((self.width//2, 150), "ERROR: CONSCIOUSNESS OVERFLOW", 
                 fill=(0, 255, 0), anchor="mm")
        
        return img
    
    def create_neural_explosion(self):
        """Create an exploding neural network visualization"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create neural explosion
        for i in range(1000):
            # Random angle and distance
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, min(self.width, self.height) / 2)
            
            # Explosion physics
            speed = math.exp(-distance / 200)
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Color based on distance
            hue = (distance / 500) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, speed)
            color = tuple(int(255 * c) for c in rgb) + (int(255 * speed),)
            
            # Draw neuron
            size = int(10 * speed)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            
            # Neural connections
            if random.random() > 0.95:
                target_angle = angle + random.uniform(-0.5, 0.5)
                target_dist = distance + random.uniform(-100, 100)
                target_x = center_x + target_dist * math.cos(target_angle)
                target_y = center_y + target_dist * math.sin(target_angle)
                
                draw.line([(x, y), (target_x, target_y)], 
                         fill=color[:3] + (50,), width=1)
        
        # Central core
        for r in range(100, 0, -5):
            alpha = int(255 * (1 - r/100))
            draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                        fill=(255, 255, 255, alpha))
        
        draw.text((self.width//2, 100), "NEURAL EXPLOSION", 
                 fill=(255, 255, 255, 255), anchor="mm")
        
        return img
    
    def create_dna_kaleidoscope(self):
        """Create a DNA kaleidoscope effect"""
        # Create base segment
        segment_size = 300
        segment = Image.new('RGBA', (segment_size, segment_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(segment)
        
        # Draw DNA pattern in segment
        for i in range(0, segment_size, 20):
            # DNA strand
            y1 = segment_size//2 + 50 * math.sin(i * 0.1)
            y2 = segment_size//2 + 50 * math.sin(i * 0.1 + math.pi)
            
            # Nucleotides
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            color = random.choice(colors)
            
            draw.ellipse([i-5, y1-5, i+5, y1+5], fill=color)
            draw.ellipse([i-5, y2-5, i+5, y2+5], fill=color)
            
            if i % 40 == 0:
                draw.line([(i, y1), (i, y2)], fill=(255, 255, 255), width=2)
        
        # Create kaleidoscope
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        
        # Number of reflections
        reflections = 12
        angle_step = 360 / reflections
        
        for i in range(reflections):
            angle = i * angle_step
            
            # Rotate segment
            rotated = segment.rotate(angle, expand=True)
            
            # Calculate position
            x = self.width//2 - rotated.width//2
            y = self.height//2 - rotated.height//2
            
            # Paste with transparency
            img.paste(rotated, (x, y), rotated)
        
        # Add center
        draw = ImageDraw.Draw(img)
        draw.ellipse([self.width//2 - 50, self.height//2 - 50,
                     self.width//2 + 50, self.height//2 + 50],
                    fill=(255, 255, 255))
        
        draw.text((self.width//2, 100), "DNA KALEIDOSCOPE", 
                 fill=(255, 255, 255), anchor="mm")
        
        return img
    
    def create_quantum_tunnel(self):
        """Create a quantum tunnel visualization"""
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create tunnel rings
        for z in range(100, 0, -2):
            # Perspective scaling
            scale = 1000 / (z + 100)
            radius = int(50 * scale)
            
            # Position with perspective
            x = center_x + int((math.sin(z * 0.1) * 50) * scale)
            y = center_y + int((math.cos(z * 0.1) * 50) * scale)
            
            # Color based on depth
            brightness = int(255 * (1 - z/100))
            hue = (z / 100) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.8, brightness/255)
            color = tuple(int(255 * c) for c in rgb)
            
            # Draw ring
            if radius > 0:
                draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                           outline=color, width=3)
        
        # Quantum particles
        for _ in range(200):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            # Distance from center
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            if dist < 400:
                size = int(5 * (1 - dist/400))
                brightness = int(255 * (1 - dist/400))
                draw.ellipse([x - size, y - size, x + size, y + size],
                           fill=(brightness, brightness, 255))
        
        # Motion blur for speed effect
        img = img.filter(ImageFilter.GaussianBlur(radius=3))
        
        draw = ImageDraw.Draw(img)
        draw.text((self.width//2, 100), "QUANTUM TUNNEL", 
                 fill=(255, 255, 255), anchor="mm")
        draw.text((self.width//2, self.height - 100), "ENTER THE CONSCIOUSNESS STREAM", 
                 fill=(150, 150, 255), anchor="mm")
        
        return img
    
    def create_holographic_interface(self):
        """Create a holographic interface visualization"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        
        # Holographic grid
        grid_size = 50
        for x in range(0, self.width, grid_size):
            for y in range(0, self.height, grid_size):
                # Holographic shimmer
                offset = math.sin(x * 0.01) * math.cos(y * 0.01) * 10
                
                # Grid lines with offset
                draw.line([(x + offset, 0), (x + offset, self.height)], 
                         fill=(0, 255, 255, 50), width=1)
                draw.line([(0, y + offset), (self.width, y + offset)], 
                         fill=(255, 0, 255, 50), width=1)
        
        # Holographic panels
        panels = [
            {"x": 100, "y": 200, "w": 300, "h": 200, "title": "QUANTUM STATE"},
            {"x": 500, "y": 300, "w": 400, "h": 250, "title": "NEURAL ACTIVITY"},
            {"x": 1000, "y": 200, "w": 350, "h": 300, "title": "DNA SEQUENCES"},
            {"x": 200, "y": 600, "w": 500, "h": 150, "title": "CONSCIOUSNESS METER"},
        ]
        
        for panel in panels:
            # Panel background
            for i in range(3):
                offset = i * 3
                draw.rectangle([panel["x"] + offset, panel["y"] + offset,
                              panel["x"] + panel["w"] + offset, panel["y"] + panel["h"] + offset],
                             fill=None, outline=(0, 255, 255, 100 - i*30), width=2)
            
            # Panel title
            draw.text((panel["x"] + panel["w"]//2, panel["y"] + 20), panel["title"],
                     fill=(255, 255, 255, 255), anchor="mm")
            
            # Random data visualization
            for j in range(10):
                bar_height = random.randint(20, panel["h"] - 60)
                bar_x = panel["x"] + 20 + j * 30
                bar_y = panel["y"] + panel["h"] - 30
                
                draw.rectangle([bar_x, bar_y - bar_height, bar_x + 20, bar_y],
                             fill=(0, 255, 255, 150))
        
        # Central hologram
        center_x, center_y = self.width // 2, self.height // 2
        for r in range(150, 0, -10):
            alpha = int(100 * (1 - r/150))
            draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                        outline=(100, 200, 255, alpha), width=2)
        
        draw.text((self.width//2, 100), "HOLOGRAPHIC INTERFACE", 
                 fill=(255, 255, 255, 255), anchor="mm")
        
        return img
    
    def create_consciousness_spiral(self):
        """Create a consciousness spiral visualization"""
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Fibonacci spiral
        a = 1
        b = 1
        
        for i in range(1000):
            # Spiral coordinates
            angle = i * 0.1
            radius = a + b * angle
            
            if radius > min(self.width, self.height) / 2:
                break
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            # Color based on golden ratio
            hue = (angle / (2 * math.pi)) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            color = tuple(int(255 * c) for c in rgb)
            
            # Draw point with size based on radius
            size = max(1, int(10 - radius/100))
            draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            
            # Consciousness particles
            if i % 10 == 0:
                for _ in range(3):
                    px = x + random.randint(-20, 20)
                    py = y + random.randint(-20, 20)
                    particle_color = tuple(int(c * 0.5) for c in color)
                    draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=particle_color)
        
        # Central consciousness core
        for r in range(50, 0, -5):
            brightness = int(255 * (1 - r/50))
            draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                        fill=(brightness, brightness, brightness))
        
        draw.text((self.width//2, 100), "CONSCIOUSNESS SPIRAL", 
                 fill=(255, 255, 255), anchor="mm")
        draw.text((self.width//2, 150), "φ = 1.618033988749...", 
                 fill=(200, 200, 200), anchor="mm")
        
        return img
    
    def create_plasma_field(self):
        """Create a plasma field visualization"""
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        pixels = img.load()
        
        # Plasma generation
        for x in range(self.width):
            for y in range(self.height):
                # Multiple sine waves
                value1 = math.sin(x * 0.01)
                value2 = math.sin(y * 0.01)
                value3 = math.sin((x + y) * 0.01)
                value4 = math.sin(math.sqrt(x*x + y*y) * 0.01)
                
                # Combine waves
                value = (value1 + value2 + value3 + value4) / 4
                
                # Map to color
                hue = (value + 1) / 2  # Normalize to 0-1
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.8)
                pixels[x, y] = tuple(int(255 * c) for c in rgb)
        
        # Add some noise
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        draw = ImageDraw.Draw(img)
        draw.text((self.width//2, 100), "PLASMA CONSCIOUSNESS FIELD", 
                 fill=(255, 255, 255), anchor="mm")
        
        return img
    
    def generate_all_psychedelic(self, output_dir: str = 'output/psychedelic', quality: int = 95):
        """Generate all psychedelic visualizations"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🌈 Generating Psychedelic CROD Graphics...")
        
        visuals = [
            ("fractal_consciousness", self.create_fractal_consciousness()),
            ("glitch_blockchain", self.create_glitch_blockchain()),
            ("neural_explosion", self.create_neural_explosion()),
            ("dna_kaleidoscope", self.create_dna_kaleidoscope()),
            ("quantum_tunnel", self.create_quantum_tunnel()),
            ("holographic_interface", self.create_holographic_interface()),
            ("consciousness_spiral", self.create_consciousness_spiral()),
            ("plasma_field", self.create_plasma_field())
        ]
        
        for name, img in visuals:
            filename = f"{output_dir}/crod_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(filename, 'PNG', quality=quality)
            print(f"✅ Saved: {filename}")
        
        print("\n🎨 All psychedelic graphics generated!")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Psychedelic CROD Graphics Generator - Create mind-bending consciousness visualizations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --all                    Generate all psychedelic visualizations
  %(prog)s --type fractal           Generate only fractal consciousness
  %(prog)s --list                   List available visualization types
  %(prog)s --size 3840x2160         Set custom 4K resolution
  %(prog)s --output /path/to/dir    Specify output directory
  %(prog)s --quality 100            Maximum quality output
''')
    
    parser.add_argument('--all', action='store_true', 
                       help='Generate all psychedelic visualization types')
    parser.add_argument('--type', choices=[
        'fractal', 'glitch', 'neural', 'kaleidoscope', 
        'tunnel', 'holographic', 'spiral', 'plasma'
    ], help='Generate specific psychedelic visualization')
    parser.add_argument('--list', action='store_true',
                       help='List all available psychedelic visualization types')
    parser.add_argument('--size', default='1920x1080',
                       help='Output resolution (default: 1920x1080)')
    parser.add_argument('--output', default='output/psychedelic',
                       help='Output directory (default: output/psychedelic)')
    parser.add_argument('--no-animation', action='store_true',
                       help='Skip psychedelic animation generation')
    parser.add_argument('--quality', type=int, default=95,
                       help='PNG quality (1-100, default: 95)')
    parser.add_argument('--frames', type=int, default=20,
                       help='Number of animation frames (default: 20)')
    
    return parser.parse_args()


def generate_psychedelic_animation(output_dir: str, frames: int = 20, width: int = 800, height: int = 600):
    """Generate consciousness rotation animation"""
    print("\n🎬 Creating psychedelic animation...")
    frame_list = []
    
    for i in range(frames):
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rotating colors
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                hue = ((x + y + i * 20) / 1000) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.8)
                color = tuple(int(255 * c) for c in rgb)
                
                draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=color)
        
        # Rotating text
        angle = i * (360 / frames)
        text_img = Image.new('RGBA', (400, 100), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((200, 50), "CROD PSYCHEDELIC", fill=(255, 255, 255, 255), anchor="mm")
        
        rotated_text = text_img.rotate(angle, expand=True)
        # Center the rotated text
        paste_x = (width - rotated_text.width) // 2
        paste_y = (height - rotated_text.height) // 2
        img.paste(rotated_text, (paste_x, paste_y), rotated_text)
        
        frame_list.append(img)
    
    gif_path = f'{output_dir}/consciousness_rotation.gif'
    frame_list[0].save(gif_path, 
                      save_all=True, append_images=frame_list[1:], 
                      duration=100, loop=0)
    print(f"✅ Saved: {gif_path}")


def main():
    """Main program entry point"""
    args = parse_arguments()
    
    # Parse resolution
    try:
        width, height = map(int, args.size.split('x'))
    except ValueError:
        print(f"Error: Invalid resolution format '{args.size}'. Use WIDTHxHEIGHT (e.g., 1920x1080)")
        sys.exit(1)
    
    # Validate quality
    if not 1 <= args.quality <= 100:
        print(f"Error: Quality must be between 1 and 100, got {args.quality}")
        sys.exit(1)
    
    # Create visualizer with custom settings
    psychedelic = PsychedelicCROD(width=width, height=height)
    
    # Handle list command
    if args.list:
        print("\nAvailable psychedelic visualization types:")
        print("  fractal       - Fractal consciousness patterns (Mandelbrot-inspired)")
        print("  glitch        - Glitched blockchain with RGB shifts")
        print("  neural        - Exploding neural network visualization")
        print("  kaleidoscope  - DNA kaleidoscope sacred geometry")
        print("  tunnel        - Quantum tunnel perspective effects")
        print("  holographic   - Holographic interface with data panels")
        print("  spiral        - Consciousness spiral (golden ratio)")
        print("  plasma        - Plasma consciousness field")
        print("\nUse --type <name> to generate a specific visualization")
        print("Use --all to generate all visualizations at once")
        return
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Generate visualizations
    if args.all:
        psychedelic.generate_all_psychedelic(output_dir=args.output, quality=args.quality)
        if not args.no_animation:
            generate_psychedelic_animation(args.output, frames=args.frames, 
                                         width=min(width, 800), height=min(height, 600))
    elif args.type:
        print(f"\n🌈 Generating {args.type} psychedelic visualization...")
        
        # Map type to method
        method_map = {
            'fractal': psychedelic.create_fractal_consciousness,
            'glitch': psychedelic.create_glitch_blockchain,
            'neural': psychedelic.create_neural_explosion,
            'kaleidoscope': psychedelic.create_dna_kaleidoscope,
            'tunnel': psychedelic.create_quantum_tunnel,
            'holographic': psychedelic.create_holographic_interface,
            'spiral': psychedelic.create_consciousness_spiral,
            'plasma': psychedelic.create_plasma_field
        }
        
        img = method_map[args.type]()
        filename = f"{args.output}/crod_{args.type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename, 'PNG', quality=args.quality)
        print(f"✅ Saved: {filename}")
        print(f"\n🎨 {args.type.capitalize()} visualization complete!")
    else:
        print("Error: Specify --all or --type <visualization>")
        print("Use --list to see available types")
        print("Use --help for more information")
        sys.exit(1)
    
    print("\n🌈 Psychedelic CROD Complete!")


if __name__ == "__main__":
    main()