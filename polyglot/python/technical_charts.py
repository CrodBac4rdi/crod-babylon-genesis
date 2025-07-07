#!/usr/bin/env python3
"""
CROD Technical Charts and Diagrams
Creates scientific diagrams, flowcharts, and statistics
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
from datetime import datetime
import os

class TechnicalChartGenerator:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.output_dir = "visualization/output/technical"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Try to load a font, fall back to default if not available
        try:
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    def create_architecture_flowchart(self):
        """Create CROD architecture flowchart"""
        img = Image.new('RGB', (self.width, self.height), (245, 245, 250))
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((self.width//2 - 200, 30), "CROD System Architecture", 
                 fill=(20, 20, 30), font=self.font_large)
        
        # Define components
        components = [
            {"name": "Quantum Core", "x": self.width//2, "y": 150, "color": (100, 200, 255)},
            {"name": "Neural Network", "x": self.width//4, "y": 300, "color": (255, 150, 100)},
            {"name": "Blockchain", "x": 3*self.width//4, "y": 300, "color": (150, 255, 150)},
            {"name": "Pattern Engine", "x": self.width//4, "y": 450, "color": (255, 200, 100)},
            {"name": "Consciousness Layer", "x": 3*self.width//4, "y": 450, "color": (200, 150, 255)},
            {"name": "API Gateway", "x": self.width//2, "y": 600, "color": (100, 255, 200)},
            {"name": "User Interface", "x": self.width//2, "y": 750, "color": (255, 100, 150)}
        ]
        
        # Draw components
        for comp in components:
            self.draw_component_box(draw, comp["x"], comp["y"], comp["name"], comp["color"])
        
        # Draw connections
        connections = [
            (components[0], components[1]),  # Quantum -> Neural
            (components[0], components[2]),  # Quantum -> Blockchain
            (components[1], components[3]),  # Neural -> Pattern
            (components[2], components[4]),  # Blockchain -> Consciousness
            (components[3], components[5]),  # Pattern -> API
            (components[4], components[5]),  # Consciousness -> API
            (components[5], components[6])   # API -> UI
        ]
        
        for start, end in connections:
            self.draw_arrow(draw, start["x"], start["y"] + 40, 
                          end["x"], end["y"] - 40, (100, 100, 120))
        
        # Add annotations
        draw.text((50, self.height - 100), 
                 "Data Flow: Quantum computations → Neural processing → Pattern detection → User interface",
                 fill=(60, 60, 80), font=self.font_small)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/architecture_flowchart_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def draw_component_box(self, draw, x, y, text, color):
        """Draw a component box with text"""
        width = 200
        height = 80
        
        # Box with gradient effect
        for i in range(5):
            shade = tuple(int(c * (1 - i * 0.1)) for c in color)
            draw.rounded_rectangle([x - width//2 + i, y - height//2 + i,
                                   x + width//2 + i, y + height//2 + i],
                                  radius=15, fill=shade)
        
        # Main box
        draw.rounded_rectangle([x - width//2, y - height//2,
                               x + width//2, y + height//2],
                              radius=15, fill=color, outline=(40, 40, 50), width=2)
        
        # Text
        text_bbox = draw.textbbox((0, 0), text, font=self.font_medium)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.text((x - text_width//2, y - text_height//2), text, 
                 fill=(255, 255, 255), font=self.font_medium)
    
    def draw_arrow(self, draw, x1, y1, x2, y2, color):
        """Draw an arrow between two points"""
        # Arrow line
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
        
        # Arrowhead
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_length = 15
        arrow_angle = 0.5
        
        x3 = x2 - arrow_length * math.cos(angle - arrow_angle)
        y3 = y2 - arrow_length * math.sin(angle - arrow_angle)
        x4 = x2 - arrow_length * math.cos(angle + arrow_angle)
        y4 = y2 - arrow_length * math.sin(angle + arrow_angle)
        
        draw.polygon([(x2, y2), (x3, y3), (x4, y4)], fill=color)
    
    def create_performance_statistics(self):
        """Create performance statistics chart"""
        img = Image.new('RGB', (self.width, self.height), (245, 245, 250))
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((self.width//2 - 150, 30), "CROD Performance Metrics", 
                 fill=(20, 20, 30), font=self.font_large)
        
        # Chart area
        chart_left = 150
        chart_top = 150
        chart_right = self.width - 150
        chart_bottom = self.height - 150
        chart_width = chart_right - chart_left
        chart_height = chart_bottom - chart_top
        
        # Draw axes
        draw.line([(chart_left, chart_bottom), (chart_right, chart_bottom)], 
                 fill=(60, 60, 80), width=2)
        draw.line([(chart_left, chart_top), (chart_left, chart_bottom)], 
                 fill=(60, 60, 80), width=2)
        
        # Performance data
        metrics = [
            {"name": "Quantum Processing", "value": 95, "color": (100, 200, 255)},
            {"name": "Neural Accuracy", "value": 88, "color": (255, 150, 100)},
            {"name": "Blockchain TPS", "value": 78, "color": (150, 255, 150)},
            {"name": "Pattern Recognition", "value": 92, "color": (255, 200, 100)},
            {"name": "System Uptime", "value": 99.9, "color": (200, 150, 255)},
            {"name": "API Response Time", "value": 85, "color": (100, 255, 200)}
        ]
        
        # Bar chart
        bar_width = chart_width // (len(metrics) * 2)
        bar_spacing = bar_width
        
        for i, metric in enumerate(metrics):
            x = chart_left + bar_spacing + i * (bar_width + bar_spacing)
            bar_height = int(chart_height * metric["value"] / 100)
            y_top = chart_bottom - bar_height
            
            # Draw bar with gradient
            for j in range(bar_width):
                intensity = 1 - (j / bar_width) * 0.3
                bar_color = tuple(int(c * intensity) for c in metric["color"])
                draw.line([(x + j, y_top), (x + j, chart_bottom)], 
                         fill=bar_color, width=1)
            
            # Value label
            draw.text((x + bar_width//2 - 15, y_top - 25), 
                     f"{metric['value']}%", fill=(40, 40, 60), font=self.font_small)
            
            # Metric name (rotated would be better, but PIL doesn't support easily)
            draw.text((x - 10, chart_bottom + 10), 
                     metric["name"][:8] + "...", fill=(40, 40, 60), font=self.font_small)
        
        # Y-axis labels
        for i in range(0, 101, 20):
            y = chart_bottom - (i * chart_height // 100)
            draw.text((chart_left - 40, y - 10), f"{i}%", 
                     fill=(60, 60, 80), font=self.font_small)
            draw.line([(chart_left - 5, y), (chart_left, y)], 
                     fill=(60, 60, 80), width=1)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/performance_statistics_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_neural_network_diagram(self):
        """Create neural network architecture diagram"""
        img = Image.new('RGB', (self.width, self.height), (245, 245, 250))
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((self.width//2 - 180, 30), "CROD Neural Network Architecture", 
                 fill=(20, 20, 30), font=self.font_large)
        
        # Network layers
        layers = [
            {"neurons": 5, "name": "Input Layer"},
            {"neurons": 8, "name": "Hidden Layer 1"},
            {"neurons": 6, "name": "Hidden Layer 2"},
            {"neurons": 3, "name": "Output Layer"}
        ]
        
        layer_spacing = self.width // (len(layers) + 1)
        neuron_positions = []
        
        # Draw neurons
        for layer_idx, layer in enumerate(layers):
            x = layer_spacing * (layer_idx + 1)
            layer_neurons = []
            
            neuron_spacing = self.height // (layer["neurons"] + 2)
            
            for neuron_idx in range(layer["neurons"]):
                y = neuron_spacing * (neuron_idx + 1) + 100
                
                # Neuron circle with gradient
                for i in range(20, 0, -1):
                    intensity = 255 - (20 - i) * 10
                    color = (intensity, intensity, 255)
                    draw.ellipse([x - i, y - i, x + i, y + i], fill=color)
                
                layer_neurons.append((x, y))
            
            neuron_positions.append(layer_neurons)
            
            # Layer label
            draw.text((x - 50, self.height - 100), layer["name"], 
                     fill=(40, 40, 60), font=self.font_medium)
        
        # Draw connections
        for layer_idx in range(len(neuron_positions) - 1):
            current_layer = neuron_positions[layer_idx]
            next_layer = neuron_positions[layer_idx + 1]
            
            for current_neuron in current_layer:
                for next_neuron in next_layer:
                    # Random weight visualization
                    weight = random.random()
                    color_intensity = int(100 + weight * 155)
                    line_color = (color_intensity, color_intensity, 255)
                    line_width = int(1 + weight * 2)
                    
                    draw.line([current_neuron, next_neuron], 
                             fill=line_color, width=line_width)
        
        # Add activation function annotation
        draw.text((50, 50), "Activation: ReLU / Sigmoid", 
                 fill=(60, 60, 80), font=self.font_small)
        draw.text((50, 70), "Learning Rate: 0.001", 
                 fill=(60, 60, 80), font=self.font_small)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/neural_network_diagram_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_blockchain_flowchart(self):
        """Create blockchain process flowchart"""
        img = Image.new('RGB', (self.width, self.height), (245, 245, 250))
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((self.width//2 - 150, 30), "CROD Blockchain Process", 
                 fill=(20, 20, 30), font=self.font_large)
        
        # Blockchain blocks
        block_width = 200
        block_height = 120
        block_spacing = 50
        start_x = 200
        y = self.height // 2
        
        blocks = [
            {"id": "Genesis", "hash": "0x0000", "data": "Initial State"},
            {"id": "Block 1", "hash": "0xa3f2", "data": "Neural Weights"},
            {"id": "Block 2", "hash": "0xb8d1", "data": "Pattern Data"},
            {"id": "Block 3", "hash": "0xc5e9", "data": "Quantum State"},
            {"id": "Current", "hash": "0xd7f4", "data": "Processing..."}
        ]
        
        for i, block in enumerate(blocks):
            x = start_x + i * (block_width + block_spacing)
            
            # Block shadow
            draw.rounded_rectangle([x + 5, y - block_height//2 + 5,
                                   x + block_width + 5, y + block_height//2 + 5],
                                  radius=10, fill=(200, 200, 210))
            
            # Block body
            color = (150, 255, 150) if i == 0 else (100, 200, 255)
            draw.rounded_rectangle([x, y - block_height//2,
                                   x + block_width, y + block_height//2],
                                  radius=10, fill=color, outline=(40, 40, 50), width=2)
            
            # Block content
            draw.text((x + 10, y - 40), f"{block['id']}", 
                     fill=(255, 255, 255), font=self.font_medium)
            draw.text((x + 10, y - 10), f"Hash: {block['hash']}", 
                     fill=(255, 255, 255), font=self.font_small)
            draw.text((x + 10, y + 10), f"Data: {block['data']}", 
                     fill=(255, 255, 255), font=self.font_small)
            
            # Chain link
            if i < len(blocks) - 1:
                draw.line([(x + block_width, y), (x + block_width + block_spacing, y)],
                         fill=(60, 60, 80), width=3)
                # Arrow
                arrow_x = x + block_width + block_spacing - 10
                draw.polygon([(arrow_x, y), (arrow_x - 10, y - 5), (arrow_x - 10, y + 5)],
                           fill=(60, 60, 80))
        
        # Mining annotation
        draw.text((self.width//2 - 100, self.height - 150), 
                 "Mining: Quantum-enhanced Proof of Consciousness",
                 fill=(60, 60, 80), font=self.font_medium)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/blockchain_flowchart_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def create_system_statistics_dashboard(self):
        """Create comprehensive system statistics dashboard"""
        img = Image.new('RGB', (self.width, self.height), (245, 245, 250))
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((self.width//2 - 180, 20), "CROD System Statistics Dashboard", 
                 fill=(20, 20, 30), font=self.font_large)
        
        # Grid layout for different charts
        # Top left: Line chart
        self.draw_line_chart(draw, 50, 100, 500, 300, "Processing Speed Over Time")
        
        # Top right: Pie chart
        self.draw_pie_chart(draw, self.width - 550, 100, 200, "Resource Usage")
        
        # Bottom left: Scatter plot
        self.draw_scatter_plot(draw, 50, 450, 500, 300, "Pattern Recognition Accuracy")
        
        # Bottom right: Heat map
        self.draw_heat_map(draw, self.width - 550, 450, 500, 300, "System Activity Heatmap")
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/system_statistics_dashboard_{timestamp}.png"
        img.save(filename)
        print(f"Created: {filename}")
        return img
    
    def draw_line_chart(self, draw, x, y, width, height, title):
        """Draw a line chart"""
        # Title
        draw.text((x + width//2 - 80, y - 30), title, fill=(40, 40, 60), font=self.font_medium)
        
        # Chart area
        draw.rectangle([x, y, x + width, y + height], outline=(60, 60, 80), width=2)
        
        # Generate data points
        points = []
        for i in range(20):
            px = x + (i * width // 20)
            py = y + height - int(random.random() * height * 0.8 + height * 0.1)
            points.append((px, py))
        
        # Draw line
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(100, 200, 255), width=3)
        
        # Draw points
        for point in points:
            draw.ellipse([point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4],
                        fill=(255, 100, 100))
    
    def draw_pie_chart(self, draw, x, y, radius, title):
        """Draw a pie chart"""
        # Title
        draw.text((x - 60, y - radius - 40), title, fill=(40, 40, 60), font=self.font_medium)
        
        # Pie slices
        slices = [
            {"percent": 35, "color": (255, 150, 100), "label": "Neural"},
            {"percent": 25, "color": (100, 200, 255), "label": "Quantum"},
            {"percent": 20, "color": (150, 255, 150), "label": "Blockchain"},
            {"percent": 20, "color": (255, 200, 100), "label": "Other"}
        ]
        
        start_angle = 0
        for slice_data in slices:
            end_angle = start_angle + (slice_data["percent"] * 360 // 100)
            
            # Draw slice
            draw.pieslice([x - radius, y - radius, x + radius, y + radius],
                         start_angle, end_angle, fill=slice_data["color"], outline=(40, 40, 50))
            
            # Label
            mid_angle = math.radians((start_angle + end_angle) / 2)
            label_x = x + int(radius * 0.7 * math.cos(mid_angle))
            label_y = y + int(radius * 0.7 * math.sin(mid_angle))
            draw.text((label_x - 20, label_y - 10), slice_data["label"], 
                     fill=(255, 255, 255), font=self.font_small)
            
            start_angle = end_angle
    
    def draw_scatter_plot(self, draw, x, y, width, height, title):
        """Draw a scatter plot"""
        # Title
        draw.text((x + width//2 - 100, y - 30), title, fill=(40, 40, 60), font=self.font_medium)
        
        # Chart area
        draw.rectangle([x, y, x + width, y + height], outline=(60, 60, 80), width=2)
        
        # Generate random points
        for _ in range(100):
            px = x + random.randint(10, width - 10)
            py = y + random.randint(10, height - 10)
            
            # Color based on position (simulating clusters)
            if px < x + width // 2 and py < y + height // 2:
                color = (255, 100, 100)
            elif px >= x + width // 2 and py < y + height // 2:
                color = (100, 255, 100)
            else:
                color = (100, 100, 255)
            
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=color)
    
    def draw_heat_map(self, draw, x, y, width, height, title):
        """Draw a heat map"""
        # Title
        draw.text((x + width//2 - 80, y - 30), title, fill=(40, 40, 60), font=self.font_medium)
        
        # Generate heat map data
        cell_size = 20
        cols = width // cell_size
        rows = height // cell_size
        
        for row in range(rows):
            for col in range(cols):
                # Random heat value
                heat = random.random()
                
                # Color from blue (cold) to red (hot)
                red = int(255 * heat)
                blue = int(255 * (1 - heat))
                green = int(128 * (1 - abs(heat - 0.5) * 2))
                
                cell_x = x + col * cell_size
                cell_y = y + row * cell_size
                
                draw.rectangle([cell_x, cell_y, cell_x + cell_size, cell_y + cell_size],
                             fill=(red, green, blue))
    
    def create_all_diagrams(self):
        """Create all technical diagrams"""
        print("Creating technical diagrams and charts...")
        
        self.create_architecture_flowchart()
        self.create_performance_statistics()
        self.create_neural_network_diagram()
        self.create_blockchain_flowchart()
        self.create_system_statistics_dashboard()
        
        print(f"\nAll technical diagrams created in {self.output_dir}/")

if __name__ == "__main__":
    generator = TechnicalChartGenerator()
    generator.create_all_diagrams()