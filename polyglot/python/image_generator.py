#!/usr/bin/env python3
"""
CROD Image Generator - Basierend auf der vorhandenen 3D-Visualisierungslogik
Erzeugt 3D-Visualisierungen, Shader-Art und andere Bilder
"""

import sys
import json
import os
import time
import random
import base64
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

# Verzeichnis für generierte Bilder
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bilder", "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ImageGenerator:
    """CROD Image Generator für verschiedene Visualisierungen"""
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.styles = [
            "neural", "plasma", "fractal", "neon", "cyberpunk", 
            "quantum", "consciousness", "abstract", "matrix", "digital"
        ]
        self.objects = [
            "sphere", "cube", "pyramid", "torus", "dna", 
            "brain", "neural-network", "galaxy", "wave", "crystal"
        ]
    
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet eine Bildgenerierungsanfrage und gibt das Ergebnis zurück
        
        Args:
            data: Dictionary mit 'prompt' und optionalen Parametern
            
        Returns:
            Dictionary mit dem Pfad zum generierten Bild
        """
        prompt = data.get("prompt", "")
        style = data.get("style", "")
        width = data.get("width", self.width)
        height = data.get("height", self.height)
        
        if not prompt:
            return {
                "success": False,
                "message": "Kein Prompt angegeben."
            }
            
        try:
            # Stil aus dem Prompt extrahieren, falls nicht explizit angegeben
            if not style:
                for s in self.styles:
                    if s.lower() in prompt.lower():
                        style = s
                        break
                if not style:
                    style = random.choice(self.styles)
            
            # Art des zu generierenden Bildes bestimmen
            if "3d" in prompt.lower() or any(obj in prompt.lower() for obj in self.objects):
                image, metadata = self._generate_3d_visualization(prompt, style, width, height)
            elif "shader" in prompt.lower() or "plasma" in prompt.lower() or "fractal" in prompt.lower():
                image, metadata = self._generate_shader_art(prompt, style, width, height)
            elif "system" in prompt.lower() or "architecture" in prompt.lower():
                image, metadata = self._generate_system_visualization(prompt, style, width, height)
            else:
                image, metadata = self._generate_abstract_art(prompt, style, width, height)
            
            # Bild speichern
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{style}_{timestamp}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            image.save(filepath)
            
            # Base64-kodiertes Bild für direktes Anzeigen
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            return {
                "success": True,
                "file_path": filepath,
                "style": style,
                "metadata": metadata,
                "base64_image": img_str,
                "width": width,
                "height": height
            }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Fehler bei der Bildgenerierung: {str(e)}"
            }
    
    def _generate_3d_visualization(self, prompt: str, style: str, width: int, height: int) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Generiert eine 3D-Visualisierung basierend auf dem Prompt
        """
        # Grundlage erstellen
        image = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Hintergrund mit Farbverlauf
        self._draw_gradient_background(image, style)
        
        # 3D-Objekt bestimmen
        object_type = "sphere"  # Standard
        for obj in self.objects:
            if obj in prompt.lower():
                object_type = obj
                break
        
        # 3D-Objekt zeichnen
        if object_type == "sphere":
            self._draw_sphere(draw, width, height, style)
        elif object_type == "cube":
            self._draw_cube(draw, width, height, style)
        elif object_type == "pyramid":
            self._draw_pyramid(draw, width, height, style)
        elif object_type == "torus":
            self._draw_torus(draw, width, height, style)
        elif object_type == "dna":
            self._draw_dna_helix(draw, width, height, style)
        elif object_type == "brain":
            self._draw_brain(draw, width, height, style)
        elif object_type == "neural-network":
            self._draw_neural_network(draw, width, height, style)
        elif object_type == "galaxy":
            self._draw_galaxy(draw, width, height, style)
        elif object_type == "wave":
            self._draw_wave(draw, width, height, style)
        elif object_type == "crystal":
            self._draw_crystal(draw, width, height, style)
        
        # Effekte hinzufügen
        image = self._apply_effects(image, style)
        
        metadata = {
            "object_type": object_type,
            "style": style,
            "generation_time": time.time(),
            "prompt": prompt
        }
        
        return image, metadata
    
    def _generate_shader_art(self, prompt: str, style: str, width: int, height: int) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Generiert Shader-Art basierend auf dem Prompt
        """
        # Grundlage erstellen
        image = Image.new("RGB", (width, height), (0, 0, 0))
        
        # Parameter aus dem Prompt extrahieren
        complexity = 5  # Standardwert
        for i in range(1, 11):
            if f"complexity {i}" in prompt.lower():
                complexity = i
                break
        
        # Verschiedene Shader-Typen
        if "plasma" in prompt.lower():
            image = self._generate_plasma_shader(width, height, complexity, style)
        elif "fractal" in prompt.lower():
            image = self._generate_fractal_shader(width, height, complexity, style)
        elif "wave" in prompt.lower():
            image = self._generate_wave_shader(width, height, complexity, style)
        elif "noise" in prompt.lower():
            image = self._generate_noise_shader(width, height, complexity, style)
        else:
            # Standard: Mischung aus verschiedenen Effekten
            image = self._generate_mixed_shader(width, height, complexity, style)
        
        # Effekte hinzufügen
        image = self._apply_effects(image, style)
        
        metadata = {
            "shader_type": style,
            "complexity": complexity,
            "generation_time": time.time(),
            "prompt": prompt
        }
        
        return image, metadata
    
    def _generate_system_visualization(self, prompt: str, style: str, width: int, height: int) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Generiert eine Systemvisualisierung basierend auf dem Prompt
        """
        # Grundlage erstellen
        image = Image.new("RGB", (width, height), (10, 10, 30))
        draw = ImageDraw.Draw(image)
        
        # Hintergrund mit Raster
        self._draw_grid_background(image, style)
        
        # Verbindungen und Knoten zeichnen (Systemarchitektur)
        num_nodes = random.randint(5, 15)
        nodes = []
        for _ in range(num_nodes):
            x = random.randint(50, width-50)
            y = random.randint(50, height-50)
            size = random.randint(20, 40)
            nodes.append((x, y, size))
        
        # Verbindungen zeichnen
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if random.random() < 0.3:  # 30% Chance für eine Verbindung
                    x1, y1, _ = nodes[i]
                    x2, y2, _ = nodes[j]
                    
                    # Farbe basierend auf Stil
                    if style == "neon" or style == "cyberpunk":
                        color = (random.randint(0, 100), random.randint(150, 255), random.randint(150, 255))
                    elif style == "quantum":
                        color = (random.randint(100, 200), random.randint(0, 100), random.randint(150, 255))
                    else:
                        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
                    
                    draw.line((x1, y1, x2, y2), fill=color, width=2)
        
        # Knoten zeichnen
        for x, y, size in nodes:
            if style == "neon":
                color = (0, random.randint(150, 255), random.randint(150, 255))
            elif style == "cyberpunk":
                color = (random.randint(200, 255), random.randint(0, 100), random.randint(100, 200))
            elif style == "quantum":
                color = (random.randint(100, 200), 0, random.randint(150, 255))
            else:
                color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
                
            draw.ellipse((x-size//2, y-size//2, x+size//2, y+size//2), fill=color)
        
        # Effekte hinzufügen
        image = self._apply_effects(image, style)
        
        metadata = {
            "nodes": num_nodes,
            "style": style,
            "generation_time": time.time(),
            "prompt": prompt
        }
        
        return image, metadata
    
    def _generate_abstract_art(self, prompt: str, style: str, width: int, height: int) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Generiert abstrakte Kunst basierend auf dem Prompt
        """
        # Grundlage erstellen
        image = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Hintergrund
        self._draw_gradient_background(image, style)
        
        # Abstrakte Formen hinzufügen
        num_shapes = random.randint(20, 50)
        for _ in range(num_shapes):
            shape_type = random.choice(["circle", "rectangle", "line", "polygon"])
            x = random.randint(0, width)
            y = random.randint(0, height)
            
            # Farbe basierend auf Stil
            if style == "neon":
                color = (random.randint(0, 50), random.randint(150, 255), random.randint(150, 255))
            elif style == "cyberpunk":
                color = (random.randint(200, 255), random.randint(0, 100), random.randint(0, 100))
            elif style == "quantum":
                color = (random.randint(100, 150), 0, random.randint(150, 255))
            elif style == "neural":
                color = (random.randint(150, 255), random.randint(0, 100), random.randint(100, 200))
            else:
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            
            # Form zeichnen
            if shape_type == "circle":
                size = random.randint(10, 100)
                draw.ellipse((x-size, y-size, x+size, y+size), fill=color)
            elif shape_type == "rectangle":
                width_rect = random.randint(10, 200)
                height_rect = random.randint(10, 200)
                draw.rectangle((x, y, x+width_rect, y+height_rect), fill=color)
            elif shape_type == "line":
                end_x = x + random.randint(-200, 200)
                end_y = y + random.randint(-200, 200)
                draw.line((x, y, end_x, end_y), fill=color, width=random.randint(1, 10))
            elif shape_type == "polygon":
                num_points = random.randint(3, 8)
                points = []
                for _ in range(num_points):
                    px = x + random.randint(-100, 100)
                    py = y + random.randint(-100, 100)
                    points.extend([px, py])
                draw.polygon(points, fill=color)
        
        # Effekte hinzufügen
        image = self._apply_effects(image, style)
        
        metadata = {
            "shapes": num_shapes,
            "style": style,
            "generation_time": time.time(),
            "prompt": prompt
        }
        
        return image, metadata
    
    # Hilfsfunktionen für die Bildgenerierung
    
    def _draw_gradient_background(self, image: Image.Image, style: str) -> None:
        """Zeichnet einen Farbverlauf als Hintergrund"""
        width, height = image.size
        pixels = image.load()
        
        if style == "neural":
            color1 = (0, 0, 50)
            color2 = (50, 0, 100)
        elif style == "plasma":
            color1 = (50, 0, 50)
            color2 = (0, 0, 100)
        elif style == "fractal":
            color1 = (0, 20, 40)
            color2 = (40, 0, 60)
        elif style == "neon":
            color1 = (0, 20, 30)
            color2 = (0, 40, 50)
        elif style == "cyberpunk":
            color1 = (50, 0, 20)
            color2 = (20, 0, 40)
        elif style == "quantum":
            color1 = (20, 0, 40)
            color2 = (0, 0, 60)
        else:
            color1 = (0, 0, 30)
            color2 = (30, 0, 60)
        
        for y in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / height)
            
            for x in range(width):
                # Etwas Rauschen hinzufügen
                noise = random.randint(-10, 10)
                pixels[x, y] = (max(0, min(255, r + noise)), 
                               max(0, min(255, g + noise)), 
                               max(0, min(255, b + noise)))
    
    def _draw_grid_background(self, image: Image.Image, style: str) -> None:
        """Zeichnet ein Rasterhintergrund"""
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        if style == "neon":
            grid_color = (0, 100, 100)
        elif style == "cyberpunk":
            grid_color = (100, 0, 50)
        elif style == "quantum":
            grid_color = (50, 0, 100)
        else:
            grid_color = (50, 50, 80)
        
        # Horizontale Linien
        step = 30
        for y in range(0, height, step):
            draw.line((0, y, width, y), fill=grid_color, width=1)
        
        # Vertikale Linien
        for x in range(0, width, step):
            draw.line((x, 0, x, height), fill=grid_color, width=1)
    
    def _draw_sphere(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine 3D-Kugel"""
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 4
        
        if style == "neon":
            color = (0, 200, 200)
        elif style == "cyberpunk":
            color = (200, 50, 100)
        elif style == "quantum":
            color = (100, 0, 200)
        else:
            color = (100, 100, 200)
        
        # Grundform
        draw.ellipse((center_x - radius, center_y - radius, 
                       center_x + radius, center_y + radius), 
                      fill=color)
        
        # Highlight für 3D-Effekt
        highlight_radius = radius * 0.7
        highlight_offset = radius * 0.3
        highlight_color = (min(255, color[0] + 50), 
                           min(255, color[1] + 50), 
                           min(255, color[2] + 50))
        
        draw.ellipse((center_x - highlight_radius - highlight_offset, 
                       center_y - highlight_radius - highlight_offset,
                       center_x + highlight_radius - highlight_offset, 
                       center_y + highlight_radius - highlight_offset), 
                      fill=highlight_color)
    
    def _draw_cube(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet einen 3D-Würfel"""
        center_x = width // 2
        center_y = height // 2
        size = min(width, height) // 5
        
        if style == "neon":
            color1 = (0, 200, 200)
            color2 = (0, 150, 150)
            color3 = (0, 100, 100)
        elif style == "cyberpunk":
            color1 = (200, 50, 100)
            color2 = (150, 30, 80)
            color3 = (100, 20, 50)
        else:
            color1 = (100, 100, 200)
            color2 = (80, 80, 180)
            color3 = (60, 60, 160)
        
        # Vorderseite
        points = [
            (center_x - size, center_y - size),
            (center_x + size, center_y - size),
            (center_x + size, center_y + size),
            (center_x - size, center_y + size)
        ]
        draw.polygon(points, fill=color1)
        
        # Oben
        offset = size // 2
        points = [
            (center_x - size, center_y - size),
            (center_x + size, center_y - size),
            (center_x + size - offset, center_y - size - offset),
            (center_x - size - offset, center_y - size - offset)
        ]
        draw.polygon(points, fill=color2)
        
        # Rechts
        points = [
            (center_x + size, center_y - size),
            (center_x + size, center_y + size),
            (center_x + size - offset, center_y + size - offset),
            (center_x + size - offset, center_y - size - offset)
        ]
        draw.polygon(points, fill=color3)
    
    def _draw_pyramid(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine 3D-Pyramide"""
        center_x = width // 2
        center_y = height // 2
        size = min(width, height) // 4
        
        if style == "neon":
            color1 = (0, 200, 200)
            color2 = (0, 150, 150)
            color3 = (0, 100, 100)
        elif style == "cyberpunk":
            color1 = (200, 50, 100)
            color2 = (150, 30, 80)
            color3 = (100, 20, 50)
        else:
            color1 = (100, 100, 200)
            color2 = (80, 80, 180)
            color3 = (60, 60, 160)
        
        # Basis
        points = [
            (center_x - size, center_y + size),
            (center_x + size, center_y + size),
            (center_x + size, center_y - size),
            (center_x - size, center_y - size)
        ]
        draw.polygon(points, fill=color1)
        
        # Spitze
        top_point = (center_x, center_y - size * 2)
        
        # Vorderseite
        points = [
            (center_x - size, center_y + size),
            (center_x + size, center_y + size),
            top_point
        ]
        draw.polygon(points, fill=color2)
        
        # Rechte Seite
        points = [
            (center_x + size, center_y + size),
            (center_x + size, center_y - size),
            top_point
        ]
        draw.polygon(points, fill=color3)
    
    def _draw_torus(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet einen 3D-Torus (vereinfacht)"""
        center_x = width // 2
        center_y = height // 2
        outer_radius = min(width, height) // 4
        inner_radius = outer_radius // 2
        
        if style == "neon":
            color = (0, 200, 200)
        elif style == "cyberpunk":
            color = (200, 50, 100)
        else:
            color = (100, 100, 200)
        
        # Äußerer Kreis
        draw.ellipse((center_x - outer_radius, center_y - outer_radius, 
                       center_x + outer_radius, center_y + outer_radius), 
                      fill=color)
        
        # Innerer Kreis (Loch)
        draw.ellipse((center_x - inner_radius, center_y - inner_radius, 
                       center_x + inner_radius, center_y + inner_radius), 
                      fill=(0, 0, 0))  # Schwarz für das Loch
    
    def _draw_dna_helix(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine DNA-Helix"""
        center_x = width // 2
        height_offset = height // 8
        amplitude = width // 6
        period = height // 4
        strand_width = 10
        
        if style == "neon":
            color1 = (0, 200, 200)
            color2 = (0, 150, 255)
        elif style == "cyberpunk":
            color1 = (200, 50, 100)
            color2 = (255, 100, 50)
        elif style == "quantum":
            color1 = (100, 0, 200)
            color2 = (50, 0, 255)
        else:
            color1 = (100, 100, 200)
            color2 = (200, 100, 100)
        
        # Erste Helix
        for y in range(height_offset, height - height_offset, 2):
            x = center_x + amplitude * np.sin(2 * np.pi * y / period)
            
            # Variiere die Größe für besseren 3D-Effekt
            size = int(strand_width * (0.5 + 0.5 * np.sin(2 * np.pi * y / period)))
            
            draw.ellipse((x - size, y - size//2, x + size, y + size//2), fill=color1)
        
        # Zweite Helix
        for y in range(height_offset, height - height_offset, 2):
            x = center_x + amplitude * np.sin(2 * np.pi * y / period + np.pi)
            
            # Variiere die Größe für besseren 3D-Effekt
            size = int(strand_width * (0.5 + 0.5 * np.sin(2 * np.pi * y / period + np.pi)))
            
            draw.ellipse((x - size, y - size//2, x + size, y + size//2), fill=color2)
        
        # Verbindungen zwischen den Helices
        for y in range(height_offset, height - height_offset, period // 2):
            x1 = center_x + amplitude * np.sin(2 * np.pi * y / period)
            x2 = center_x + amplitude * np.sin(2 * np.pi * y / period + np.pi)
            
            connection_color = (min(255, (color1[0] + color2[0]) // 2), 
                                min(255, (color1[1] + color2[1]) // 2),
                                min(255, (color1[2] + color2[2]) // 2))
            
            draw.line((x1, y, x2, y), fill=connection_color, width=3)
    
    def _draw_brain(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet ein stilisiertes Gehirn"""
        center_x = width // 2
        center_y = height // 2
        brain_width = width // 2
        brain_height = height // 3
        
        if style == "neural":
            color = (150, 50, 200)
            highlight = (200, 100, 255)
        elif style == "quantum":
            color = (100, 0, 200)
            highlight = (150, 50, 255)
        else:
            color = (200, 150, 150)
            highlight = (255, 200, 200)
        
        # Grundform (zwei Hälften)
        draw.ellipse((center_x - brain_width, center_y - brain_height, 
                       center_x - brain_width//8, center_y + brain_height), 
                      fill=color)
        
        draw.ellipse((center_x + brain_width//8, center_y - brain_height, 
                       center_x + brain_width, center_y + brain_height), 
                      fill=color)
        
        # Verbindung in der Mitte
        draw.rectangle((center_x - brain_width//8, center_y - brain_height//2, 
                        center_x + brain_width//8, center_y + brain_height//2), 
                       fill=color)
        
        # Neuronale Verbindungen (zufällig)
        num_connections = 50
        for _ in range(num_connections):
            x1 = random.randint(center_x - brain_width, center_x + brain_width)
            y1 = random.randint(center_y - brain_height, center_y + brain_height)
            
            # Stelle sicher, dass der Punkt im Gehirn ist
            dx1 = (x1 - (center_x - brain_width//2)) / (brain_width//2)
            dy1 = (y1 - center_y) / brain_height
            
            if dx1**2 + dy1**2 <= 1 or (x1 > center_x and (dx1-1)**2 + dy1**2 <= 1):
                x2 = random.randint(center_x - brain_width, center_x + brain_width)
                y2 = random.randint(center_y - brain_height, center_y + brain_height)
                
                dx2 = (x2 - (center_x - brain_width//2)) / (brain_width//2)
                dy2 = (y2 - center_y) / brain_height
                
                if dx2**2 + dy2**2 <= 1 or (x2 > center_x and (dx2-1)**2 + dy2**2 <= 1):
                    connection_color = (random.randint(highlight[0]-50, highlight[0]), 
                                       random.randint(highlight[1]-50, highlight[1]),
                                       random.randint(highlight[2]-50, highlight[2]))
                    
                    draw.line((x1, y1, x2, y2), fill=connection_color, width=1)
    
    def _draw_neural_network(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet ein neuronales Netzwerk"""
        # Knoten und Schichten definieren
        layers = [4, 7, 7, 4]  # Anzahl Neuronen pro Schicht
        neurons = []
        
        if style == "neural":
            base_color = (150, 50, 200)
            active_color = (200, 100, 255)
        elif style == "quantum":
            base_color = (100, 0, 200)
            active_color = (150, 50, 255)
        elif style == "neon":
            base_color = (0, 150, 150)
            active_color = (0, 255, 255)
        else:
            base_color = (100, 100, 150)
            active_color = (150, 150, 200)
        
        # Neuronen platzieren
        layer_spacing = width // (len(layers) + 1)
        for l, layer_size in enumerate(layers):
            layer_x = (l + 1) * layer_spacing
            neuron_spacing = height // (layer_size + 1)
            
            layer_neurons = []
            for n in range(layer_size):
                neuron_y = (n + 1) * neuron_spacing
                neuron_size = random.randint(10, 20)
                
                # Zufällig einige Neuronen aktivieren
                if random.random() < 0.3:
                    color = active_color
                else:
                    color = base_color
                
                draw.ellipse((layer_x - neuron_size, neuron_y - neuron_size, 
                               layer_x + neuron_size, neuron_y + neuron_size), 
                              fill=color)
                
                layer_neurons.append((layer_x, neuron_y))
            
            neurons.append(layer_neurons)
        
        # Verbindungen zwischen den Schichten
        for l in range(len(layers) - 1):
            for start_neuron in neurons[l]:
                for end_neuron in neurons[l + 1]:
                    # Nicht alle Verbindungen zeichnen
                    if random.random() < 0.6:
                        # Gewicht der Verbindung durch Farbintensität darstellen
                        weight = random.random()
                        connection_color = (
                            int(base_color[0] * weight),
                            int(base_color[1] * weight),
                            int(base_color[2] * weight)
                        )
                        
                        draw.line((start_neuron[0], start_neuron[1], 
                                   end_neuron[0], end_neuron[1]), 
                                  fill=connection_color, width=1)
    
    def _draw_galaxy(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine Galaxie"""
        center_x = width // 2
        center_y = height // 2
        galaxy_radius = min(width, height) // 3
        
        if style == "neural":
            color = (100, 50, 200)
        elif style == "quantum":
            color = (50, 0, 150)
        elif style == "neon":
            color = (0, 100, 150)
        else:
            color = (100, 100, 150)
        
        # Zentrum der Galaxie
        center_size = galaxy_radius // 4
        center_color = (min(255, color[0] * 2), 
                        min(255, color[1] * 2), 
                        min(255, color[2] * 2))
        
        draw.ellipse((center_x - center_size, center_y - center_size, 
                       center_x + center_size, center_y + center_size), 
                      fill=center_color)
        
        # Sterne in Spiralarmen
        num_arms = 4
        stars_per_arm = 200
        
        for arm in range(num_arms):
            angle_offset = arm * (2 * np.pi / num_arms)
            
            for i in range(stars_per_arm):
                # Spiralarm-Parametrisierung
                distance = random.random() * galaxy_radius
                angle = angle_offset + distance / galaxy_radius * 2 * np.pi
                
                x = center_x + distance * np.cos(angle)
                y = center_y + distance * np.sin(angle)
                
                # Sternfarbe und -größe variieren
                star_brightness = random.random()
                star_color = (min(255, int(color[0] + star_brightness * 155)), 
                             min(255, int(color[1] + star_brightness * 155)), 
                             min(255, int(color[2] + star_brightness * 155)))
                
                star_size = int(1 + star_brightness * 3)
                
                draw.ellipse((x - star_size, y - star_size, 
                               x + star_size, y + star_size), 
                              fill=star_color)
    
    def _draw_wave(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine Wellenform"""
        center_y = height // 2
        amplitude = height // 4
        wave_width = 3
        
        if style == "neural":
            color = (150, 50, 200)
        elif style == "quantum":
            color = (100, 0, 200)
        elif style == "neon":
            color = (0, 200, 200)
        else:
            color = (100, 100, 200)
        
        # Sinuswelle
        for x in range(0, width, 2):
            # Kombiniere mehrere Frequenzen für komplexere Welle
            y = center_y + amplitude * np.sin(x * 0.02) * 0.7
            y += amplitude * np.sin(x * 0.05) * 0.3
            
            draw.ellipse((x - wave_width, y - wave_width, 
                           x + wave_width, y + wave_width), 
                          fill=color)
        
        # Zweite Welle (versetzt)
        second_color = (min(255, color[0] + 50), 
                        min(255, color[1] + 50),
                        min(255, color[2] + 50))
        
        for x in range(0, width, 3):
            # Andere Frequenzkombination
            y = center_y + amplitude * 0.7 * np.sin(x * 0.03 + np.pi/2)
            y += amplitude * 0.3 * np.sin(x * 0.07 + np.pi/4)
            
            draw.ellipse((x - wave_width//2, y - wave_width//2, 
                           x + wave_width//2, y + wave_width//2), 
                          fill=second_color)
    
    def _draw_crystal(self, draw: ImageDraw.Draw, width: int, height: int, style: str) -> None:
        """Zeichnet eine Kristallstruktur"""
        center_x = width // 2
        center_y = height // 2
        crystal_size = min(width, height) // 4
        
        if style == "neural":
            color = (150, 50, 200)
        elif style == "quantum":
            color = (100, 0, 200)
        elif style == "neon":
            color = (0, 200, 200)
        else:
            color = (100, 100, 200)
        
        # Zentraler Kristall (regelmäßiges Sechseck)
        points = []
        for i in range(6):
            angle = i * 2 * np.pi / 6
            x = center_x + crystal_size * np.cos(angle)
            y = center_y + crystal_size * np.sin(angle)
            points.extend([x, y])
        
        draw.polygon(points, fill=color)
        
        # Kleinere Kristalle um den Hauptkristall
        num_crystals = 6
        for i in range(num_crystals):
            angle = i * 2 * np.pi / num_crystals
            offset_x = crystal_size * 1.5 * np.cos(angle)
            offset_y = crystal_size * 1.5 * np.sin(angle)
            
            # Größe und Farbe variieren
            secondary_size = crystal_size * 0.5
            secondary_color = (max(0, color[0] - 30),
                              max(0, color[1] - 30),
                              max(0, color[2] - 30))
            
            secondary_points = []
            for j in range(6):
                point_angle = j * 2 * np.pi / 6
                x = center_x + offset_x + secondary_size * np.cos(point_angle)
                y = center_y + offset_y + secondary_size * np.sin(point_angle)
                secondary_points.extend([x, y])
            
            draw.polygon(secondary_points, fill=secondary_color)
    
    # Shader-Generatoren
    
    def _generate_plasma_shader(self, width: int, height: int, complexity: int, style: str) -> Image.Image:
        """Generiert einen Plasma-Shader"""
        image = Image.new("RGB", (width, height), (0, 0, 0))
        pixels = image.load()
        
        if style == "neon":
            base_colors = [(0, 100, 255), (0, 255, 255), (0, 100, 150)]
        elif style == "cyberpunk":
            base_colors = [(255, 0, 100), (150, 0, 150), (100, 0, 100)]
        elif style == "quantum":
            base_colors = [(100, 0, 255), (50, 0, 200), (0, 0, 150)]
        else:
            base_colors = [(0, 0, 200), (100, 0, 150), (150, 0, 100)]
        
        # Komplexität bestimmt die Anzahl der Sinuswellen
        frequencies = [random.uniform(0.01, 0.1) for _ in range(complexity)]
        phases = [random.uniform(0, 2 * np.pi) for _ in range(complexity)]
        
        for y in range(height):
            for x in range(width):
                # Kombiniere mehrere Sinuswellen für komplexeres Plasma
                value = 0
                for freq, phase in zip(frequencies, phases):
                    value += np.sin(x * freq + phase)
                    value += np.sin(y * freq + phase)
                    value += np.sin((x + y) * freq + phase)
                    value += np.sin(np.sqrt(x*x + y*y) * freq + phase)
                
                # Normalisieren auf [0, 1]
                value = (value + 4 * complexity) / (8 * complexity)
                
                # Farbe interpolieren
                r = int(base_colors[0][0] * (1 - value) + base_colors[1][0] * value)
                g = int(base_colors[0][1] * (1 - value) + base_colors[1][1] * value)
                b = int(base_colors[0][2] * (1 - value) + base_colors[1][2] * value)
                
                pixels[x, y] = (r, g, b)
        
        return image
    
    def _generate_fractal_shader(self, width: int, height: int, complexity: int, style: str) -> Image.Image:
        """Generiert einen einfachen Fraktal-Shader (Julia-Set)"""
        image = Image.new("RGB", (width, height), (0, 0, 0))
        pixels = image.load()
        
        if style == "neon":
            palette = [(0, i, 255-i) for i in range(0, 256, 16)]
        elif style == "cyberpunk":
            palette = [(255-i, 0, i) for i in range(0, 256, 16)]
        elif style == "quantum":
            palette = [(i, 0, 255-i//2) for i in range(0, 256, 16)]
        else:
            palette = [(0, 0, i) for i in range(0, 256, 16)]
        
        # Julia-Set Parameter
        c_real = random.uniform(-1.0, 0.5)
        c_imag = random.uniform(-1.0, 1.0)
        
        max_iter = 20 + complexity * 10
        escape_radius = 4.0
        
        # Skalierungsfaktoren
        scale_x = 3.0 / width
        scale_y = 3.0 / height
        
        for y in range(height):
            for x in range(width):
                # Punkt im komplexen Raum
                z_real = (x - width / 2) * scale_x
                z_imag = (y - height / 2) * scale_y
                
                # Julia-Set Iteration
                iteration = 0
                while iteration < max_iter and (z_real*z_real + z_imag*z_imag) < escape_radius:
                    # z = z^2 + c
                    temp = z_real*z_real - z_imag*z_imag + c_real
                    z_imag = 2*z_real*z_imag + c_imag
                    z_real = temp
                    
                    iteration += 1
                
                # Farbauswahl basierend auf Iterationszahl
                if iteration == max_iter:
                    pixels[x, y] = (0, 0, 0)  # Schwarz für Punkte im Set
                else:
                    color_index = iteration % len(palette)
                    pixels[x, y] = palette[color_index]
        
        return image
    
    def _generate_wave_shader(self, width: int, height: int, complexity: int, style: str) -> Image.Image:
        """Generiert einen Wellenmuster-Shader"""
        image = Image.new("RGB", (width, height), (0, 0, 0))
        pixels = image.load()
        
        if style == "neon":
            color1 = (0, 150, 255)
            color2 = (0, 255, 150)
        elif style == "cyberpunk":
            color1 = (255, 0, 100)
            color2 = (100, 0, 255)
        elif style == "quantum":
            color1 = (100, 0, 255)
            color2 = (50, 0, 200)
        else:
            color1 = (0, 100, 200)
            color2 = (0, 200, 100)
        
        # Komplexität bestimmt die Anzahl der Wellen
        wave_count = complexity
        frequencies = [random.uniform(0.01, 0.1) for _ in range(wave_count)]
        phases = [random.uniform(0, 2 * np.pi) for _ in range(wave_count)]
        
        for y in range(height):
            for x in range(width):
                # Kombiniere mehrere Wellen
                value = 0
                for freq, phase in zip(frequencies, phases):
                    value += np.sin(x * freq + phase)
                    value += np.cos(y * freq * 1.5 + phase)
                
                # Normalisieren auf [0, 1]
                value = (value + 2 * wave_count) / (4 * wave_count)
                
                # Farbe interpolieren
                r = int(color1[0] * (1 - value) + color2[0] * value)
                g = int(color1[1] * (1 - value) + color2[1] * value)
                b = int(color1[2] * (1 - value) + color2[2] * value)
                
                pixels[x, y] = (r, g, b)
        
        return image
    
    def _generate_noise_shader(self, width: int, height: int, complexity: int, style: str) -> Image.Image:
        """Generiert einen Rauschen-Shader"""
        image = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        if style == "neon":
            base_color = (0, 150, 150)
        elif style == "cyberpunk":
            base_color = (150, 0, 100)
        elif style == "quantum":
            base_color = (100, 0, 150)
        else:
            base_color = (50, 50, 100)
        
        # Grundfarbe
        draw.rectangle((0, 0, width, height), fill=base_color)
        
        # Rauschen hinzufügen
        pixels = image.load()
        noise_strength = 30 + complexity * 10
        
        for y in range(height):
            for x in range(width):
                # Rauschen generieren
                noise = random.randint(-noise_strength, noise_strength)
                
                # Farbe anpassen
                r = max(0, min(255, base_color[0] + noise))
                g = max(0, min(255, base_color[1] + noise))
                b = max(0, min(255, base_color[2] + noise))
                
                pixels[x, y] = (r, g, b)
        
        return image
    
    def _generate_mixed_shader(self, width: int, height: int, complexity: int, style: str) -> Image.Image:
        """Generiert einen gemischten Shader mit mehreren Effekten"""
        # Basiseffekt auswählen
        base_shader = random.choice([
            self._generate_plasma_shader,
            self._generate_fractal_shader,
            self._generate_wave_shader
        ])
        
        # Basiseffekt generieren
        image = base_shader(width, height, complexity, style)
        
        # Zusätzliche Effekte
        if random.random() < 0.5:
            # Überlagerungseffekt
            overlay = self._generate_noise_shader(width, height, complexity // 2, style)
            image = Image.blend(image, overlay, 0.2)
        
        if random.random() < 0.3:
            # Kreisförmige Muster hinzufügen
            draw = ImageDraw.Draw(image)
            
            if style == "neon":
                circle_color = (0, 255, 255, 100)  # Semi-transparent
            elif style == "cyberpunk":
                circle_color = (255, 0, 100, 100)
            elif style == "quantum":
                circle_color = (150, 0, 255, 100)
            else:
                circle_color = (100, 100, 200, 100)
            
            for _ in range(complexity * 2):
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(20, 100)
                
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), 
                             fill=circle_color)
        
        return image
    
    def _apply_effects(self, image: Image.Image, style: str) -> Image.Image:
        """Wendet Bildeffekte basierend auf dem Stil an"""
        if style == "neon":
            # Neon-Glühen
            image = image.filter(ImageFilter.GaussianBlur(radius=3))
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)
            
        elif style == "cyberpunk":
            # Höherer Kontrast, leichte Verzerrung
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            
            # Chromatische Aberration simulieren
            r, g, b = image.split()
            r = ImageOps.deform(r, lambda x, y: (x + 3, y))
            b = ImageOps.deform(b, lambda x, y: (x - 3, y))
            image = Image.merge('RGB', (r, g, b))
            
        elif style == "quantum":
            # Leichte Unschärfe und Farbverstärkung
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.5)
            
        elif style == "neural":
            # Strukturierte Muster
            image = image.filter(ImageFilter.EDGE_ENHANCE)
            
        elif style == "fractal":
            # Schärfen für mehr Details
            image = image.filter(ImageFilter.SHARPEN)
        
        return image


def main():
    """Hauptfunktion zum Verarbeiten der Anfrage"""
    try:
        # Eingabe vom Node.js-Server lesen
        input_data = sys.stdin.read()
        request_data = json.loads(input_data)
        
        # Bildgenerator initialisieren und Anfrage verarbeiten
        generator = ImageGenerator()
        response = generator.process_request(request_data)
        
        # Antwort zurückgeben
        print(json.dumps(response))
        
    except Exception as e:
        error_response = {
            "success": False,
            "message": f"Fehler im Image Generator: {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(1)


if __name__ == "__main__":
    main()
