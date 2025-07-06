#!/usr/bin/env python3
"""
CROD Object Renderer - Erstellt konkrete Objekte mit Shader-Effekten
Kein Psycho-Trip mehr, sondern echte Bilder!
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.patheffects as path_effects
from datetime import datetime
import argparse
import os

class CRODObjectRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.fig_width = width / 100
        self.fig_height = height / 100
        
    def render_dragon_ball(self, star_count=4, save_path=None):
        """Render a floating Dragon Ball with stars"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Background gradient
        self.add_sky_gradient(ax)
        
        # Floating effect - shadow
        shadow = Circle((0, -0.3), 0.9, color='black', alpha=0.3, zorder=1)
        shadow.set_transform(ax.transData)
        ax.add_patch(shadow)
        
        # Main ball
        ball = Circle((0, 0), 0.8, facecolor='#ff8c00', edgecolor='#ff6600', linewidth=3, zorder=10)
        ax.add_patch(ball)
        
        # Highlight/shine
        highlight = Wedge((0.3, 0.3), 0.5, 30, 150, facecolor='#ffcc00', alpha=0.6, zorder=11)
        ax.add_patch(highlight)
        
        # Small highlight
        small_highlight = Circle((0.4, 0.4), 0.15, facecolor='white', alpha=0.8, zorder=12)
        ax.add_patch(small_highlight)
        
        # Stars
        if star_count > 0 and star_count <= 7:
            self.add_dragon_ball_stars(ax, star_count)
        
        # Aura effect
        for i in range(3):
            aura = Circle((0, 0), 0.85 + i*0.1, fill=False, 
                         edgecolor='yellow', alpha=0.3-i*0.1, linewidth=2, zorder=0)
            ax.add_patch(aura)
        
        # Energy particles
        self.add_energy_particles(ax, color='yellow', intensity=20)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none')
            print(f"✅ Dragon Ball saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
        
    def render_kamehameha(self, save_path=None):
        """Render a Kamehameha energy wave"""
        fig, ax = plt.subplots(figsize=(self.fig_width * 1.5, self.fig_height))
        ax.set_xlim(-3, 3)
        ax.set_ylim(-2, 2)
        
        # Dark background
        ax.set_facecolor('#000033')
        
        # Energy core
        x = np.linspace(-3, 3, 100)
        y = np.zeros_like(x)
        
        # Wave shape
        for i in range(5):
            wave_y = np.sin(x * 2 + i*0.5) * 0.3 * (1 - i*0.15)
            ax.fill_between(x, y - wave_y, y + wave_y, 
                          color='cyan', alpha=0.6-i*0.1, zorder=10-i)
        
        # Energy source (hands position)
        source = Circle((-2.5, 0), 0.4, facecolor='white', edgecolor='cyan', 
                       linewidth=3, zorder=20)
        ax.add_patch(source)
        
        # Inner core beam
        core_y = 0.1 * np.exp(-0.5 * x**2)
        ax.fill_between(x, -core_y, core_y, color='white', alpha=0.9, zorder=15)
        
        # Energy particles
        for i in range(50):
            px = np.random.uniform(-3, 3)
            py = np.random.uniform(-0.5, 0.5) * np.exp(-0.5 * px**2)
            particle = Circle((px, py), 0.05, color='cyan', alpha=0.7)
            ax.add_patch(particle)
        
        # Lightning effects
        for i in range(3):
            lightning_x = x + np.random.normal(0, 0.02, len(x))
            lightning_y = np.sin(x * 10 + i*2) * 0.05 * np.exp(-0.3 * x**2)
            ax.plot(lightning_x, lightning_y, color='white', alpha=0.7, linewidth=1)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=ax.get_facecolor())
            print(f"✅ Kamehameha saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_pokeball(self, save_path=None):
        """Render a Pokeball"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Background
        self.add_sky_gradient(ax, color1='#e8f4f8', color2='#b8e0f0')
        
        # Shadow
        shadow = Circle((0, -0.2), 0.95, color='gray', alpha=0.3)
        ax.add_patch(shadow)
        
        # Bottom half (white)
        bottom = Wedge((0, 0), 0.9, 180, 360, facecolor='white', 
                      edgecolor='black', linewidth=3, zorder=10)
        ax.add_patch(bottom)
        
        # Top half (red)
        top = Wedge((0, 0), 0.9, 0, 180, facecolor='#ff1744', 
                   edgecolor='black', linewidth=3, zorder=10)
        ax.add_patch(top)
        
        # Center band
        band = Rectangle((-0.9, -0.08), 1.8, 0.16, facecolor='black', zorder=11)
        ax.add_patch(band)
        
        # Center button
        outer_button = Circle((0, 0), 0.25, facecolor='black', zorder=12)
        ax.add_patch(outer_button)
        inner_button = Circle((0, 0), 0.18, facecolor='white', zorder=13)
        ax.add_patch(inner_button)
        center_button = Circle((0, 0), 0.12, facecolor='black', zorder=14)
        ax.add_patch(center_button)
        
        # Shine effect
        shine = Wedge((0.3, 0.3), 0.6, 20, 120, facecolor='white', 
                     alpha=0.4, zorder=15)
        ax.add_patch(shine)
        
        # Small sparkles
        for i in range(5):
            angle = i * 72 * np.pi / 180
            r = 1.2
            sparkle = Circle((r * np.cos(angle), r * np.sin(angle)), 0.05, 
                           facecolor='yellow', alpha=0.7)
            ax.add_patch(sparkle)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none')
            print(f"✅ Pokeball saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_master_sword(self, save_path=None):
        """Render the Master Sword from Zelda"""
        fig, ax = plt.subplots(figsize=(self.fig_width * 0.6, self.fig_height * 1.2))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-3, 3)
        
        # Background - mystical forest
        self.add_mystical_background(ax)
        
        # Blade
        blade_verts = [
            (-0.1, -2), (0.1, -2),  # Base
            (0.15, 1.5), (0, 2.2), (-0.15, 1.5),  # Blade shape
            (-0.1, -2)
        ]
        blade = Polygon(blade_verts, facecolor='#c0c0c0', edgecolor='#808080', 
                       linewidth=2, zorder=10)
        ax.add_patch(blade)
        
        # Blade shine
        shine_verts = [
            (-0.05, -2), (0.05, -2),
            (0.08, 1.5), (0, 2.2), (-0.08, 1.5),
            (-0.05, -2)
        ]
        shine = Polygon(shine_verts, facecolor='white', alpha=0.5, zorder=11)
        ax.add_patch(shine)
        
        # Guard
        guard = Rectangle((-0.5, -2.2), 1.0, 0.2, facecolor='#4169e1', 
                         edgecolor='#00008b', linewidth=2, zorder=12)
        ax.add_patch(guard)
        
        # Triforce on guard
        self.add_triforce(ax, 0, -2.1, size=0.1)
        
        # Handle
        handle = Rectangle((-0.08, -2.8), 0.16, 0.6, facecolor='#4169e1', 
                          edgecolor='#00008b', linewidth=2, zorder=9)
        ax.add_patch(handle)
        
        # Pommel
        pommel = Circle((0, -2.9), 0.15, facecolor='#ffd700', 
                       edgecolor='#daa520', linewidth=2, zorder=13)
        ax.add_patch(pommel)
        
        # Magical aura
        for i in range(3):
            aura_verts = [
                (-0.1-i*0.05, -2), (0.1+i*0.05, -2),
                (0.15+i*0.05, 1.5), (0, 2.2+i*0.1), (-0.15-i*0.05, 1.5),
                (-0.1-i*0.05, -2)
            ]
            aura = Polygon(aura_verts, fill=False, edgecolor='cyan', 
                          alpha=0.3-i*0.1, linewidth=2, zorder=5-i)
            ax.add_patch(aura)
        
        # Light particles
        self.add_energy_particles(ax, color='cyan', intensity=15, y_range=(-3, 3))
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none')
            print(f"✅ Master Sword saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_portal(self, portal_type='blue', save_path=None):
        """Render a portal (Portal game style)"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Dark background
        ax.set_facecolor('#1a1a1a')
        
        # Portal colors
        if portal_type == 'blue':
            color = '#00bfff'
            glow_color = '#87ceeb'
        else:  # orange
            color = '#ff8c00'
            glow_color = '#ffa500'
        
        # Outer glow
        for i in range(5):
            glow = Circle((0, 0), 0.8 + i*0.2, fill=False, 
                         edgecolor=glow_color, alpha=0.3-i*0.05, 
                         linewidth=3, zorder=5-i)
            ax.add_patch(glow)
        
        # Portal ring
        outer_ring = Circle((0, 0), 0.8, fill=False, edgecolor=color, 
                           linewidth=8, zorder=10)
        ax.add_patch(outer_ring)
        
        # Inner portal effect
        theta = np.linspace(0, 2*np.pi, 100)
        for i in range(10):
            r = 0.7 - i*0.07
            spiral_x = r * np.cos(theta + i*0.3)
            spiral_y = r * np.sin(theta + i*0.3)
            ax.plot(spiral_x, spiral_y, color=color, alpha=0.5-i*0.04, 
                   linewidth=2, zorder=15-i)
        
        # Center vortex
        center = Circle((0, 0), 0.1, facecolor='white', alpha=0.9, zorder=20)
        ax.add_patch(center)
        
        # Particle effects
        for i in range(30):
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(0.2, 0.7)
            px = r * np.cos(angle)
            py = r * np.sin(angle)
            particle = Circle((px, py), 0.02, facecolor=glow_color, 
                            alpha=0.7, zorder=18)
            ax.add_patch(particle)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=ax.get_facecolor())
            print(f"✅ Portal saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_coin(self, coin_type='mario', save_path=None):
        """Render a game coin (Mario, Sonic ring, etc)"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Background
        self.add_sky_gradient(ax)
        
        if coin_type == 'mario':
            # Shadow
            shadow = Circle((0, -0.1), 0.85, color='gray', alpha=0.3)
            ax.add_patch(shadow)
            
            # Main coin
            coin = Circle((0, 0), 0.8, facecolor='#ffd700', 
                         edgecolor='#daa520', linewidth=4, zorder=10)
            ax.add_patch(coin)
            
            # Inner circle
            inner = Circle((0, 0), 0.6, fill=False, edgecolor='#daa520', 
                          linewidth=3, zorder=11)
            ax.add_patch(inner)
            
            # Star in center
            star_points = []
            for i in range(10):
                angle = i * np.pi / 5
                if i % 2 == 0:
                    r = 0.35
                else:
                    r = 0.15
                x = r * np.cos(angle - np.pi/2)
                y = r * np.sin(angle - np.pi/2)
                star_points.append([x, y])
            
            star = Polygon(star_points, facecolor='#daa520', 
                          edgecolor='#b8860b', linewidth=2, zorder=12)
            ax.add_patch(star)
            
            # Shine
            shine = Wedge((0.2, 0.2), 0.5, 20, 120, facecolor='white', 
                         alpha=0.4, zorder=13)
            ax.add_patch(shine)
            
        elif coin_type == 'sonic':
            # Ring shape
            outer = Circle((0, 0), 0.8, fill=False, edgecolor='#ffd700', 
                          linewidth=20, zorder=10)
            ax.add_patch(outer)
            
            inner = Circle((0, 0), 0.6, fill=False, edgecolor='#ffed4e', 
                          linewidth=15, zorder=11)
            ax.add_patch(inner)
            
            # Shine effects
            for angle in [45, 135, 225, 315]:
                rad = angle * np.pi / 180
                x = 0.7 * np.cos(rad)
                y = 0.7 * np.sin(rad)
                shine = Circle((x, y), 0.1, facecolor='white', alpha=0.6, zorder=12)
                ax.add_patch(shine)
        
        # Sparkle effects
        self.add_sparkles(ax, intensity=10)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none')
            print(f"✅ Coin saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_heart_container(self, save_path=None):
        """Render a Zelda-style heart container"""
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Background
        self.add_mystical_background(ax)
        
        # Heart shape
        t = np.linspace(0, 2*np.pi, 100)
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        
        # Normalize
        x = x / 20
        y = y / 20
        
        # Outer glow
        for i in range(3):
            scale = 1 + i*0.1
            ax.fill(x*scale, y*scale, color='#ff1493', alpha=0.2-i*0.05, zorder=5-i)
        
        # Main heart
        ax.fill(x, y, color='#ff0066', edgecolor='#cc0052', linewidth=3, zorder=10)
        
        # Inner shine
        ax.fill(x*0.8, y*0.8 + 0.1, color='#ff69b4', alpha=0.6, zorder=11)
        
        # Highlight
        highlight = Circle((-0.2, 0.3), 0.15, facecolor='white', alpha=0.7, zorder=12)
        ax.add_patch(highlight)
        
        # Particles
        self.add_energy_particles(ax, color='#ff69b4', intensity=20)
        
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='none')
            print(f"✅ Heart Container saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    def render_all_in_one_scene(self, save_path=None):
        """Render all objects in one epic scene"""
        fig = plt.figure(figsize=(20, 12))
        
        # Create main scene axis
        main_ax = fig.add_subplot(111)
        main_ax.set_xlim(-10, 10)
        main_ax.set_ylim(-6, 6)
        main_ax.set_aspect('equal')
        
        # Epic background
        main_ax.set_facecolor('#0a0a2e')
        
        # Add stars
        for i in range(100):
            x = np.random.uniform(-10, 10)
            y = np.random.uniform(-6, 6)
            star = Circle((x, y), 0.02, facecolor='white', alpha=np.random.uniform(0.3, 0.9))
            main_ax.add_patch(star)
        
        # Dragon Ball (floating top left)
        db_ax = fig.add_axes([0.1, 0.7, 0.15, 0.15])
        db_ax.set_xlim(-2, 2)
        db_ax.set_ylim(-2, 2)
        db_ax.set_aspect('equal')
        db_ax.axis('off')
        
        # Dragon ball
        ball = Circle((0, 0), 0.8, facecolor='#ff8c00', edgecolor='#ff6600', linewidth=3)
        db_ax.add_patch(ball)
        highlight = Wedge((0.3, 0.3), 0.5, 30, 150, facecolor='#ffcc00', alpha=0.6)
        db_ax.add_patch(highlight)
        # 4 stars
        for x, y in [(-0.2, 0.2), (0.2, 0.2), (-0.2, -0.2), (0.2, -0.2)]:
            star_points = []
            for i in range(10):
                angle = i * np.pi / 5
                r = 0.12 if i % 2 == 0 else 0.05
                sx = x + r * np.cos(angle - np.pi/2)
                sy = y + r * np.sin(angle - np.pi/2)
                star_points.append([sx, sy])
            star = Polygon(star_points, facecolor='red', edgecolor='darkred')
            db_ax.add_patch(star)
        
        # Pokeball (top right)
        pb_ax = fig.add_axes([0.75, 0.7, 0.15, 0.15])
        pb_ax.set_xlim(-2, 2)
        pb_ax.set_ylim(-2, 2)
        pb_ax.set_aspect('equal')
        pb_ax.axis('off')
        
        bottom = Wedge((0, 0), 0.9, 180, 360, facecolor='white', edgecolor='black', linewidth=3)
        pb_ax.add_patch(bottom)
        top = Wedge((0, 0), 0.9, 0, 180, facecolor='#ff1744', edgecolor='black', linewidth=3)
        pb_ax.add_patch(top)
        band = Rectangle((-0.9, -0.08), 1.8, 0.16, facecolor='black')
        pb_ax.add_patch(band)
        pb_ax.add_patch(Circle((0, 0), 0.25, facecolor='black'))
        pb_ax.add_patch(Circle((0, 0), 0.18, facecolor='white'))
        pb_ax.add_patch(Circle((0, 0), 0.12, facecolor='black'))
        
        # Master Sword (center)
        blade_verts = [(-0.2, -2), (0.2, -2), (0.3, 3), (0, 4), (-0.3, 3), (-0.2, -2)]
        blade = Polygon(blade_verts, facecolor='#c0c0c0', edgecolor='#808080', 
                       linewidth=2, transform=main_ax.transData)
        main_ax.add_patch(blade)
        
        guard = Rectangle((-1, -2.4), 2, 0.4, facecolor='#4169e1', 
                         edgecolor='#00008b', linewidth=2)
        main_ax.add_patch(guard)
        
        # Kamehameha wave (bottom)
        x = np.linspace(-8, 8, 100)
        for i in range(3):
            wave_y = np.sin(x * 0.5 + i*0.5) * 0.3 * (1 - i*0.2) - 3
            main_ax.fill_between(x, wave_y - 0.2, wave_y + 0.2, 
                               color='cyan', alpha=0.6-i*0.15)
        
        # Portals (left and right)
        # Blue portal
        for i in range(3):
            portal = Circle((-6, 0), 1.5 + i*0.2, fill=False, 
                          edgecolor='#00bfff', alpha=0.4-i*0.1, linewidth=3)
            main_ax.add_patch(portal)
        
        # Orange portal
        for i in range(3):
            portal = Circle((6, 0), 1.5 + i*0.2, fill=False, 
                          edgecolor='#ff8c00', alpha=0.4-i*0.1, linewidth=3)
            main_ax.add_patch(portal)
        
        # Coins scattered
        coin_positions = [(-3, 3), (3, 3), (-4, -1), (4, -1)]
        for x, y in coin_positions:
            coin = Circle((x, y), 0.3, facecolor='#ffd700', edgecolor='#daa520', linewidth=2)
            main_ax.add_patch(coin)
            inner = Circle((x, y), 0.2, fill=False, edgecolor='#daa520', linewidth=1)
            main_ax.add_patch(inner)
        
        # Heart container (top center)
        t = np.linspace(0, 2*np.pi, 100)
        hx = 16 * np.sin(t)**3 / 40
        hy = (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)) / 40 + 4
        main_ax.fill(hx, hy, color='#ff0066', edgecolor='#cc0052', linewidth=2)
        
        # Title
        main_ax.text(0, 5.5, 'CROD Game Objects Collection', 
                    fontsize=24, ha='center', color='white', weight='bold',
                    path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])
        
        main_ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            print(f"✅ All-in-One Scene saved: {save_path}")
        else:
            plt.show()
            
        plt.close()
    
    # Helper methods
    def add_dragon_ball_stars(self, ax, count):
        """Add stars to Dragon Ball"""
        positions = [
            [(0, 0)],  # 1 star
            [(-0.2, 0.1), (0.2, -0.1)],  # 2 stars
            [(-0.2, 0.2), (0, -0.1), (0.2, 0.2)],  # 3 stars
            [(-0.2, 0.2), (0.2, 0.2), (-0.2, -0.2), (0.2, -0.2)],  # 4 stars
            [(-0.3, 0.2), (0, 0.3), (0.3, 0.2), (-0.15, -0.2), (0.15, -0.2)],  # 5 stars
            [(-0.3, 0.2), (0, 0.2), (0.3, 0.2), (-0.3, -0.2), (0, -0.2), (0.3, -0.2)],  # 6 stars
            [(-0.3, 0.25), (0, 0.3), (0.3, 0.25), (-0.35, 0), (0.35, 0), 
             (-0.2, -0.25), (0.2, -0.25)]  # 7 stars
        ]
        
        star_pos = positions[count-1]
        
        for x, y in star_pos:
            # Create star shape
            star_points = []
            for i in range(10):
                angle = i * np.pi / 5
                if i % 2 == 0:
                    r = 0.12
                else:
                    r = 0.05
                sx = x + r * np.cos(angle - np.pi/2)
                sy = y + r * np.sin(angle - np.pi/2)
                star_points.append([sx, sy])
            
            star = Polygon(star_points, facecolor='red', edgecolor='darkred', 
                          linewidth=1, zorder=15)
            ax.add_patch(star)
    
    def add_sky_gradient(self, ax, color1='#87ceeb', color2='#ffffff'):
        """Add sky gradient background"""
        gradient = np.linspace(0, 1, 256).reshape(256, 1)
        gradient = np.hstack((gradient, gradient, gradient))
        
        ax.imshow(gradient, extent=[-2, 2, -2, 2], aspect='auto', 
                 cmap=plt.cm.Blues_r, alpha=0.5, zorder=0)
    
    def add_mystical_background(self, ax):
        """Add mystical forest background"""
        ax.set_facecolor('#001a33')
        
        # Add some mystical fog
        for i in range(5):
            y = -2 + i * 0.8
            fog = Rectangle((-2, y), 4, 0.5, facecolor='white', 
                           alpha=0.05, zorder=1)
            ax.add_patch(fog)
    
    def add_energy_particles(self, ax, color='cyan', intensity=10, y_range=(-2, 2)):
        """Add floating energy particles"""
        for i in range(intensity):
            x = np.random.uniform(-2, 2)
            y = np.random.uniform(y_range[0], y_range[1])
            size = np.random.uniform(0.02, 0.08)
            alpha = np.random.uniform(0.3, 0.8)
            
            particle = Circle((x, y), size, facecolor=color, alpha=alpha, zorder=7)
            ax.add_patch(particle)
    
    def add_sparkles(self, ax, intensity=5):
        """Add sparkle effects"""
        for i in range(intensity):
            x = np.random.uniform(-1.5, 1.5)
            y = np.random.uniform(-1.5, 1.5)
            
            # Cross sparkle
            ax.plot([x-0.1, x+0.1], [y, y], color='white', alpha=0.8, linewidth=1)
            ax.plot([x, x], [y-0.1, y+0.1], color='white', alpha=0.8, linewidth=1)
    
    def add_triforce(self, ax, x, y, size=0.1):
        """Add a small triforce symbol"""
        h = size * np.sqrt(3) / 2
        
        # Top triangle
        top_tri = Polygon([(x, y+h/2), (x-size/2, y-h/2), (x+size/2, y-h/2)], 
                         facecolor='gold', edgecolor='darkgoldenrod', linewidth=0.5)
        ax.add_patch(top_tri)
        
        # Bottom left triangle
        bl_tri = Polygon([(x-size/2, y-h/2), (x-size, y-3*h/2), (x, y-3*h/2)], 
                        facecolor='gold', edgecolor='darkgoldenrod', linewidth=0.5)
        ax.add_patch(bl_tri)
        
        # Bottom right triangle
        br_tri = Polygon([(x+size/2, y-h/2), (x, y-3*h/2), (x+size, y-3*h/2)], 
                        facecolor='gold', edgecolor='darkgoldenrod', linewidth=0.5)
        ax.add_patch(br_tri)

def main():
    parser = argparse.ArgumentParser(description='CROD Object Renderer - Create game objects!')
    parser.add_argument('object', nargs='?', default='dragon_ball',
                       choices=['dragon_ball', 'kamehameha', 'pokeball', 'master_sword',
                               'portal_blue', 'portal_orange', 'coin_mario', 'coin_sonic',
                               'heart_container', 'all'],
                       help='Object to render')
    parser.add_argument('--save', type=str, help='Save as image file')
    parser.add_argument('--width', type=int, default=800, help='Image width')
    parser.add_argument('--height', type=int, default=600, help='Image height')
    parser.add_argument('--stars', type=int, default=4, 
                       help='Number of stars on Dragon Ball (1-7)')
    
    args = parser.parse_args()
    
    renderer = CRODObjectRenderer(args.width, args.height)
    
    print(f"\n🎮 CROD Object Renderer")
    print(f"📦 Rendering: {args.object}\n")
    
    if args.object == 'dragon_ball':
        renderer.render_dragon_ball(star_count=args.stars, save_path=args.save)
    elif args.object == 'kamehameha':
        renderer.render_kamehameha(save_path=args.save)
    elif args.object == 'pokeball':
        renderer.render_pokeball(save_path=args.save)
    elif args.object == 'master_sword':
        renderer.render_master_sword(save_path=args.save)
    elif args.object == 'portal_blue':
        renderer.render_portal(portal_type='blue', save_path=args.save)
    elif args.object == 'portal_orange':
        renderer.render_portal(portal_type='orange', save_path=args.save)
    elif args.object == 'coin_mario':
        renderer.render_coin(coin_type='mario', save_path=args.save)
    elif args.object == 'coin_sonic':
        renderer.render_coin(coin_type='sonic', save_path=args.save)
    elif args.object == 'heart_container':
        renderer.render_heart_container(save_path=args.save)
    elif args.object == 'all':
        renderer.render_all_in_one_scene(save_path=args.save)

if __name__ == "__main__":
    main()