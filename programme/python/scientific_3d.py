#!/usr/bin/env python3
"""
CROD Scientific 3D Visualizations
Creates anime-style 3D objects and scientific diagrams
"""

from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
from datetime import datetime
import os

class Scientific3DRenderer:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.output_dir = "visualization/output/3d"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def render_3d_sphere(self, img, center, radius, color, shading=True):
        """Render a 3D sphere with anime-style shading"""
        draw = ImageDraw.Draw(img)
        
        # Main sphere
        left = center[0] - radius
        top = center[1] - radius
        right = center[0] + radius
        bottom = center[1] + radius
        
        # Gradient shading for 3D effect
        for i in range(radius, 0, -1):
            intensity = int(255 * (i / radius))
            if shading:
                shade_color = tuple(int(c * intensity / 255) for c in color)
            else:
                shade_color = color
            
            draw.ellipse([
                center[0] - i, center[1] - i,
                center[0] + i, center[1] + i
            ], fill=shade_color)
        
        # Anime-style highlight
        highlight_radius = radius // 3
        highlight_x = center[0] - radius // 3
        highlight_y = center[1] - radius // 3
        
        for i in range(highlight_radius, 0, -1):
            alpha = int(255 * (i / highlight_radius))
            highlight_color = (255, 255, 255, alpha)
            draw.ellipse([
                highlight_x - i, highlight_y - i,
                highlight_x + i, highlight_y + i
            ], fill=highlight_color)
    
    def create_dragon_ball(self):
        """Create a 3D Dragon Ball with stars"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Orange sphere
        center = (self.width // 2, self.height // 2)
        radius = 200
        self.render_3d_sphere(img, center, radius, (255, 140, 0))
        
        # Red stars (4-star Dragon Ball)
        star_positions = [
            (center[0] - 50, center[1] - 50),
            (center[0] + 50, center[1] - 50),
            (center[0] - 50, center[1] + 50),
            (center[0] + 50, center[1] + 50)
        ]
        
        for pos in star_positions:
            self.draw_star(draw, pos, 20, (255, 0, 0))
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/dragon_ball_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def draw_star(self, draw, center, size, color):
        """Draw a 5-pointed star"""
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.5
            x = center[0] + r * math.cos(angle - math.pi/2)
            y = center[1] + r * math.sin(angle - math.pi/2)
            points.append((x, y))
        draw.polygon(points, fill=color)
    
    def create_pokeball(self):
        """Create a 3D Pokéball"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        center = (self.width // 2, self.height // 2)
        radius = 200
        
        # Bottom half (white)
        draw.pieslice([center[0] - radius, center[1] - radius,
                      center[0] + radius, center[1] + radius],
                     0, 180, fill=(240, 240, 240))
        
        # Top half (red)
        draw.pieslice([center[0] - radius, center[1] - radius,
                      center[0] + radius, center[1] + radius],
                     180, 360, fill=(255, 0, 0))
        
        # Black band
        band_width = 20
        draw.rectangle([center[0] - radius, center[1] - band_width//2,
                       center[0] + radius, center[1] + band_width//2],
                      fill=(20, 20, 20))
        
        # Center button
        button_radius = 30
        draw.ellipse([center[0] - button_radius, center[1] - button_radius,
                     center[0] + button_radius, center[1] + button_radius],
                    fill=(20, 20, 20))
        
        inner_radius = 20
        draw.ellipse([center[0] - inner_radius, center[1] - inner_radius,
                     center[0] + inner_radius, center[1] + inner_radius],
                    fill=(240, 240, 240))
        
        # 3D shading
        for i in range(radius, radius-30, -1):
            alpha = int(128 * (radius - i) / 30)
            shade = Image.new('RGBA', (self.width, self.height), (0, 0, 0, alpha))
            shade_draw = ImageDraw.Draw(shade)
            shade_draw.ellipse([center[0] - i, center[1] - i,
                               center[0] + i, center[1] + i],
                              fill=(0, 0, 0, alpha))
            img = Image.alpha_composite(img, shade)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/pokeball_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_master_sword(self):
        """Create the Master Sword from Zelda"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Sword blade
        blade_top = (self.width // 2, 100)
        blade_bottom = (self.width // 2, self.height - 300)
        blade_width = 60
        
        # Blade gradient
        for i in range(blade_width // 2):
            color_intensity = 255 - i * 3
            blade_color = (color_intensity, color_intensity, 255)
            draw.polygon([
                (blade_top[0] - blade_width//2 + i, blade_top[1]),
                (blade_top[0] + blade_width//2 - i, blade_top[1]),
                (blade_bottom[0] + blade_width//2 - i, blade_bottom[1]),
                (blade_bottom[0] - blade_width//2 + i, blade_bottom[1])
            ], fill=blade_color)
        
        # Hilt
        hilt_y = blade_bottom[1]
        hilt_width = 150
        hilt_height = 30
        draw.rectangle([
            self.width//2 - hilt_width//2, hilt_y,
            self.width//2 + hilt_width//2, hilt_y + hilt_height
        ], fill=(128, 64, 255))
        
        # Handle
        handle_width = 40
        handle_height = 150
        draw.rectangle([
            self.width//2 - handle_width//2, hilt_y + hilt_height,
            self.width//2 + handle_width//2, hilt_y + hilt_height + handle_height
        ], fill=(64, 32, 128))
        
        # Triforce symbol on blade
        triforce_y = blade_top[1] + 100
        self.draw_triforce(draw, (self.width//2, triforce_y), 30, (255, 215, 0))
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/master_sword_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def draw_triforce(self, draw, center, size, color):
        """Draw the Triforce symbol"""
        height = size * math.sqrt(3) / 2
        
        # Top triangle
        top_triangle = [
            (center[0], center[1] - height),
            (center[0] - size//2, center[1]),
            (center[0] + size//2, center[1])
        ]
        draw.polygon(top_triangle, fill=color)
        
        # Bottom left triangle
        bl_triangle = [
            (center[0] - size//2, center[1]),
            (center[0] - size, center[1] + height),
            (center[0], center[1] + height)
        ]
        draw.polygon(bl_triangle, fill=color)
        
        # Bottom right triangle
        br_triangle = [
            (center[0] + size//2, center[1]),
            (center[0], center[1] + height),
            (center[0] + size, center[1] + height)
        ]
        draw.polygon(br_triangle, fill=color)
    
    def create_heart_container(self):
        """Create a Zelda heart container"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        center = (self.width // 2, self.height // 2)
        size = 150
        
        # Create heart shape
        heart_points = []
        for t in np.linspace(0, 2*math.pi, 100):
            x = 16 * (math.sin(t)**3)
            y = -13 * math.cos(t) + 5 * math.cos(2*t) + 2 * math.cos(3*t) + math.cos(4*t)
            heart_points.append((center[0] + x * size/16, center[1] + y * size/16))
        
        # 3D effect with gradients
        for i in range(20):
            offset = i * 2
            color_intensity = 255 - i * 10
            heart_color = (255, color_intensity, color_intensity)
            
            offset_points = [(p[0] + offset/2, p[1] + offset/2) for p in heart_points]
            draw.polygon(offset_points, fill=heart_color)
        
        # Main heart
        draw.polygon(heart_points, fill=(255, 0, 0))
        
        # Shine effect
        shine_points = [(p[0] - 30, p[1] - 30) for p in heart_points[:30]]
        draw.polygon(shine_points, fill=(255, 128, 128))
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/heart_container_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_sonic_ring(self):
        """Create a Sonic ring/coin"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        center = (self.width // 2, self.height // 2)
        outer_radius = 150
        inner_radius = 100
        
        # 3D ring effect
        for angle in range(360):
            rad = math.radians(angle)
            
            # Outer edge
            x1 = center[0] + outer_radius * math.cos(rad)
            y1 = center[1] + outer_radius * math.sin(rad) * 0.7  # Elliptical for 3D
            
            # Inner edge
            x2 = center[0] + inner_radius * math.cos(rad)
            y2 = center[1] + inner_radius * math.sin(rad) * 0.7
            
            # Color gradient for metallic effect
            intensity = int(128 + 127 * math.sin(rad * 2))
            color = (255, 215, intensity)
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
        
        # Front face
        draw.ellipse([
            center[0] - outer_radius, center[1] - outer_radius * 0.7,
            center[0] + outer_radius, center[1] + outer_radius * 0.7
        ], outline=(255, 215, 0), width=5)
        
        draw.ellipse([
            center[0] - inner_radius, center[1] - inner_radius * 0.7,
            center[0] + inner_radius, center[1] + inner_radius * 0.7
        ], outline=(255, 215, 0), width=5)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/sonic_ring_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_mario_coin(self):
        """Create a Mario coin"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        
        center = (self.width // 2, self.height // 2)
        radius = 150
        
        # 3D coin layers
        for i in range(10):
            offset = i * 3
            layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(layer)
            
            color_val = 255 - i * 10
            coin_color = (color_val, color_val, 0)
            
            draw.ellipse([
                center[0] - radius + offset, center[1] - radius * 0.8 + offset,
                center[0] + radius + offset, center[1] + radius * 0.8 + offset
            ], fill=coin_color)
            
            img = Image.alpha_composite(img, layer)
        
        # Main coin
        draw = ImageDraw.Draw(img)
        draw.ellipse([
            center[0] - radius, center[1] - radius * 0.8,
            center[0] + radius, center[1] + radius * 0.8
        ], fill=(255, 215, 0))
        
        # Star in center
        self.draw_star(draw, center, 60, (255, 255, 0))
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/mario_coin_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_portal_gun_portals(self):
        """Create Portal game portals (blue and orange)"""
        img = Image.new('RGBA', (self.width, self.height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Blue portal
        blue_center = (self.width // 3, self.height // 2)
        self.draw_portal(img, blue_center, 150, (0, 162, 255), "BLUE")
        
        # Orange portal
        orange_center = (2 * self.width // 3, self.height // 2)
        self.draw_portal(img, orange_center, 150, (255, 162, 0), "ORANGE")
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/portal_portals_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def draw_portal(self, img, center, radius, color, label):
        """Draw a single portal with swirling effect"""
        portal_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(portal_img)
        
        # Swirling layers
        for i in range(50):
            layer_radius = radius - i * 3
            if layer_radius <= 0:
                break
            
            angle_offset = i * 10
            opacity = 255 - i * 5
            layer_color = (*color, opacity)
            
            # Create swirl effect
            for angle in range(0, 360, 5):
                rad = math.radians(angle + angle_offset)
                x = center[0] + layer_radius * math.cos(rad) * (1 + 0.1 * math.sin(rad * 5))
                y = center[1] + layer_radius * math.sin(rad) * (1 + 0.1 * math.cos(rad * 5))
                
                draw.ellipse([x-5, y-5, x+5, y+5], fill=layer_color)
        
        # Center vortex
        for i in range(20):
            vortex_radius = 20 - i
            vortex_color = (*color, 255)
            draw.ellipse([
                center[0] - vortex_radius, center[1] - vortex_radius,
                center[0] + vortex_radius, center[1] + vortex_radius
            ], fill=vortex_color)
        
        # Add to main image
        img.paste(portal_img, (0, 0), portal_img)
    
    def create_all_objects(self):
        """Create all 3D anime-style objects"""
        print("Creating 3D anime-style objects...")
        
        self.create_dragon_ball()
        self.create_pokeball()
        self.create_master_sword()
        self.create_heart_container()
        self.create_sonic_ring()
        self.create_mario_coin()
        self.create_portal_gun_portals()
        
        print(f"\nAll 3D objects created in {self.output_dir}/")

if __name__ == "__main__":
    renderer = Scientific3DRenderer()
    renderer.create_all_objects()