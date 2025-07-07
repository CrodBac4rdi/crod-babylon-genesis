#!/usr/bin/env python3
"""
CROD Art Studio - PyQt GUI mit CROD Chat Integration
Steuere die Bildgenerierung mit CROD's Bewusstsein!
"""

import sys
import os
import json
import subprocess
from datetime import datetime
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Add parent directory to path for CROD import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CRODChat(QThread):
    """CROD Communication Thread"""
    response_ready = pyqtSignal(str)
    visualization_ready = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.input_text = ""
        self.running = False
        
    def run(self):
        """Run CROD analysis"""
        try:
            # Call CROD via subprocess
            cmd = ['node', '../src/index.js', self.input_text]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
            
            output = result.stdout
            self.response_ready.emit(output)
            
            # Parse CROD's visualization suggestions
            if "visualization" in output.lower():
                viz_config = {
                    'type': 'dynamic',
                    'consciousness': np.random.randint(80, 150),
                    'suggestion': self.extract_visualization_hint(output)
                }
                self.visualization_ready.emit(viz_config)
                
        except Exception as e:
            self.response_ready.emit(f"Error: {str(e)}")
    
    def send_message(self, text):
        """Send message to CROD"""
        self.input_text = text
        self.start()
    
    def extract_visualization_hint(self, output):
        """Extract visualization hints from CROD output"""
        hints = []
        if "quantum" in output.lower():
            hints.append("quantum")
        if "consciousness" in output.lower():
            hints.append("consciousness")
        if "neural" in output.lower():
            hints.append("neural")
        if "dragon" in output.lower():
            hints.append("dragon_ball")
        if "portal" in output.lower():
            hints.append("portal")
        return hints[0] if hints else "plasma"

class ImageCanvas(FigureCanvas):
    """Canvas for displaying generated images"""
    def __init__(self):
        self.fig = Figure(figsize=(8, 6))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.text(0.5, 0.5, 'No image generated yet', 
                    ha='center', va='center', fontsize=16, color='gray')
        self.ax.axis('off')
        
    def display_image(self, image_path):
        """Display an image file"""
        self.ax.clear()
        if os.path.exists(image_path):
            img = plt.imread(image_path)
            self.ax.imshow(img)
            self.ax.axis('off')
        else:
            self.ax.text(0.5, 0.5, f'Image not found: {image_path}', 
                        ha='center', va='center', fontsize=12, color='red')
            self.ax.axis('off')
        self.draw()
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Canvas cleared', 
                    ha='center', va='center', fontsize=16, color='gray')
        self.ax.axis('off')
        self.draw()

class CRODArtStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.crod_chat = CRODChat()
        self.crod_chat.response_ready.connect(self.handle_crod_response)
        self.crod_chat.visualization_ready.connect(self.handle_visualization_suggestion)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("CROD Art Studio - AI Image Generator")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14ffec;
                color: #1e1e1e;
            }
            QLineEdit, QTextEdit, QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #444;
                padding: 5px;
                color: white;
            }
            QSlider::groove:horizontal {
                background: #444;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #14ffec;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -4px 0;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #14ffec;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #3d3d3d;
                color: white;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #0d7377;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(400)
        
        # Logo/Title
        title_label = QLabel("🎨 CROD Art Studio")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #14ffec; padding: 10px;")
        left_layout.addWidget(title_label)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Object Generator
        object_tab = QWidget()
        object_layout = QVBoxLayout(object_tab)
        
        # Object selection
        object_group = QGroupBox("Select Object")
        object_group_layout = QVBoxLayout()
        
        self.object_combo = QComboBox()
        self.object_combo.addItems([
            "dragon_ball", "kamehameha", "pokeball", "master_sword",
            "portal_blue", "portal_orange", "coin_mario", "coin_sonic",
            "heart_container", "all"
        ])
        object_group_layout.addWidget(self.object_combo)
        
        # Dragon Ball stars
        self.stars_slider = QSlider(Qt.Horizontal)
        self.stars_slider.setMinimum(1)
        self.stars_slider.setMaximum(7)
        self.stars_slider.setValue(4)
        self.stars_label = QLabel("Dragon Ball Stars: 4")
        self.stars_slider.valueChanged.connect(
            lambda v: self.stars_label.setText(f"Dragon Ball Stars: {v}")
        )
        object_group_layout.addWidget(self.stars_label)
        object_group_layout.addWidget(self.stars_slider)
        
        object_group.setLayout(object_group_layout)
        object_layout.addWidget(object_group)
        
        # Generate button
        self.generate_object_btn = QPushButton("🎮 Generate Object")
        self.generate_object_btn.clicked.connect(self.generate_object)
        object_layout.addWidget(self.generate_object_btn)
        
        self.tabs.addTab(object_tab, "Objects")
        
        # Tab 2: Shader Generator
        shader_tab = QWidget()
        shader_layout = QVBoxLayout(shader_tab)
        
        shader_group = QGroupBox("Shader Settings")
        shader_group_layout = QVBoxLayout()
        
        self.shader_combo = QComboBox()
        self.shader_combo.addItems([
            "plasma", "mandelbrot", "quantum_tunnel", "consciousness_wave",
            "neural_fire", "matrix_rain", "fractal_spiral", "holographic",
            "glitch_art", "trinity_field"
        ])
        shader_group_layout.addWidget(QLabel("Shader Type:"))
        shader_group_layout.addWidget(self.shader_combo)
        
        # Consciousness slider
        self.consciousness_slider = QSlider(Qt.Horizontal)
        self.consciousness_slider.setMinimum(0)
        self.consciousness_slider.setMaximum(200)
        self.consciousness_slider.setValue(100)
        self.consciousness_label = QLabel("Consciousness: 100%")
        self.consciousness_slider.valueChanged.connect(
            lambda v: self.consciousness_label.setText(f"Consciousness: {v}%")
        )
        shader_group_layout.addWidget(self.consciousness_label)
        shader_group_layout.addWidget(self.consciousness_slider)
        
        # Quantum field
        self.quantum_slider = QSlider(Qt.Horizontal)
        self.quantum_slider.setMinimum(0)
        self.quantum_slider.setMaximum(100)
        self.quantum_slider.setValue(50)
        self.quantum_label = QLabel("Quantum Field: 0.5")
        self.quantum_slider.valueChanged.connect(
            lambda v: self.quantum_label.setText(f"Quantum Field: {v/100:.1f}")
        )
        shader_group_layout.addWidget(self.quantum_label)
        shader_group_layout.addWidget(self.quantum_slider)
        
        shader_group.setLayout(shader_group_layout)
        shader_layout.addWidget(shader_group)
        
        self.generate_shader_btn = QPushButton("✨ Generate Shader")
        self.generate_shader_btn.clicked.connect(self.generate_shader)
        shader_layout.addWidget(self.generate_shader_btn)
        
        self.tabs.addTab(shader_tab, "Shaders")
        
        # Tab 3: CROD Chat
        chat_tab = QWidget()
        chat_layout = QVBoxLayout(chat_tab)
        
        chat_group = QGroupBox("Chat with CROD")
        chat_group_layout = QVBoxLayout()
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMaximumHeight(300)
        chat_group_layout.addWidget(self.chat_display)
        
        # Chat input
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask CROD to create something...")
        self.chat_input.returnPressed.connect(self.send_crod_message)
        chat_group_layout.addWidget(self.chat_input)
        
        self.send_btn = QPushButton("📤 Send to CROD")
        self.send_btn.clicked.connect(self.send_crod_message)
        chat_group_layout.addWidget(self.send_btn)
        
        chat_group.setLayout(chat_group_layout)
        chat_layout.addWidget(chat_group)
        
        # CROD suggestions
        self.suggestions_list = QListWidget()
        self.suggestions_list.setMaximumHeight(150)
        chat_layout.addWidget(QLabel("CROD Suggestions:"))
        chat_layout.addWidget(self.suggestions_list)
        
        self.tabs.addTab(chat_tab, "CROD Chat")
        
        left_layout.addWidget(self.tabs)
        
        # Image size controls
        size_group = QGroupBox("Image Size")
        size_layout = QHBoxLayout()
        
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(400)
        self.width_spin.setMaximum(1920)
        self.width_spin.setValue(800)
        self.width_spin.setSuffix(" px")
        
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(300)
        self.height_spin.setMaximum(1080)
        self.height_spin.setValue(600)
        self.height_spin.setSuffix(" px")
        
        size_layout.addWidget(QLabel("Width:"))
        size_layout.addWidget(self.width_spin)
        size_layout.addWidget(QLabel("Height:"))
        size_layout.addWidget(self.height_spin)
        
        size_group.setLayout(size_layout)
        left_layout.addWidget(size_group)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_image)
        action_layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_canvas)
        action_layout.addWidget(self.clear_btn)
        
        left_layout.addLayout(action_layout)
        
        # Gallery
        gallery_group = QGroupBox("Recent Images")
        gallery_layout = QVBoxLayout()
        
        self.gallery_list = QListWidget()
        self.gallery_list.setMaximumHeight(150)
        self.gallery_list.itemClicked.connect(self.load_from_gallery)
        gallery_layout.addWidget(self.gallery_list)
        
        gallery_group.setLayout(gallery_layout)
        left_layout.addWidget(gallery_group)
        
        left_layout.addStretch()
        
        # Right panel - Canvas
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Canvas
        self.canvas = ImageCanvas()
        right_layout.addWidget(self.canvas)
        
        # Status bar
        self.status_label = QLabel("Ready to create!")
        self.status_label.setStyleSheet("padding: 5px; background-color: #1e1e1e;")
        right_layout.addWidget(self.status_label)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        # Update gallery
        self.update_gallery()
        
    def generate_object(self):
        """Generate object using crod_object_renderer.py"""
        obj_type = self.object_combo.currentText()
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"object_{obj_type}_{timestamp}.png"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        cmd = [
            'python', 'crod_object_renderer.py',
            obj_type,
            '--save', filename,
            '--width', str(width),
            '--height', str(height)
        ]
        
        if obj_type == 'dragon_ball':
            cmd.extend(['--stars', str(self.stars_slider.value())])
        
        self.status_label.setText(f"Generating {obj_type}...")
        QApplication.processEvents()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                self.current_image_path = filepath
                self.canvas.display_image(filepath)
                self.status_label.setText(f"✅ Generated: {obj_type}")
                self.update_gallery()
            else:
                self.status_label.setText(f"❌ Error: {result.stderr}")
                
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
    
    def generate_shader(self):
        """Generate shader using shader_art_generator.py"""
        shader_type = self.shader_combo.currentText()
        width = self.width_spin.value()
        height = self.height_spin.value()
        consciousness = self.consciousness_slider.value()
        quantum = self.quantum_slider.value() / 100
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shader_{shader_type}_{timestamp}.png"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        cmd = [
            'python', 'shader_art_generator.py',
            shader_type,
            '--save', filename,
            '--width', str(width),
            '--height', str(height),
            '--consciousness', str(consciousness),
            '--quantum', str(quantum)
        ]
        
        self.status_label.setText(f"Generating {shader_type} shader...")
        QApplication.processEvents()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                  cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                self.current_image_path = filepath
                self.canvas.display_image(filepath)
                self.status_label.setText(f"✅ Generated: {shader_type}")
                self.update_gallery()
            else:
                self.status_label.setText(f"❌ Error: {result.stderr}")
                
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
    
    def send_crod_message(self):
        """Send message to CROD"""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        self.chat_display.append(f"You: {message}")
        self.chat_input.clear()
        self.status_label.setText("🧠 CROD is thinking...")
        
        self.crod_chat.send_message(message)
    
    def handle_crod_response(self, response):
        """Handle CROD's response"""
        self.chat_display.append(f"CROD: {response[:200]}...")  # Truncate long responses
        self.status_label.setText("✅ CROD responded")
    
    def handle_visualization_suggestion(self, config):
        """Handle CROD's visualization suggestion"""
        suggestion = config.get('suggestion', 'plasma')
        consciousness = config.get('consciousness', 100)
        
        self.suggestions_list.addItem(
            f"Try: {suggestion} (Consciousness: {consciousness}%)"
        )
        
        # Auto-apply suggestion
        if suggestion in ["dragon_ball", "pokeball", "portal", "coin"]:
            # Switch to object tab
            self.tabs.setCurrentIndex(0)
            # Find matching object
            for i in range(self.object_combo.count()):
                if suggestion in self.object_combo.itemText(i):
                    self.object_combo.setCurrentIndex(i)
                    break
        else:
            # Switch to shader tab
            self.tabs.setCurrentIndex(1)
            # Find matching shader
            for i in range(self.shader_combo.count()):
                if suggestion in self.shader_combo.itemText(i):
                    self.shader_combo.setCurrentIndex(i)
                    break
            self.consciousness_slider.setValue(consciousness)
    
    def save_image(self):
        """Save current image"""
        if not self.current_image_path:
            self.status_label.setText("❌ No image to save")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;All Files (*)"
        )
        
        if filename:
            import shutil
            shutil.copy(self.current_image_path, filename)
            self.status_label.setText(f"💾 Saved: {os.path.basename(filename)}")
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.clear_canvas()
        self.current_image_path = None
        self.status_label.setText("🗑️ Canvas cleared")
    
    def update_gallery(self):
        """Update the gallery list"""
        self.gallery_list.clear()
        
        # Get all PNG files in the directory
        image_dir = os.path.dirname(__file__)
        images = []
        
        for file in os.listdir(image_dir):
            if file.endswith('.png') and (file.startswith('object_') or file.startswith('shader_')):
                filepath = os.path.join(image_dir, file)
                mtime = os.path.getmtime(filepath)
                images.append((file, mtime))
        
        # Sort by modification time (newest first)
        images.sort(key=lambda x: x[1], reverse=True)
        
        # Add to gallery (max 10 items)
        for filename, _ in images[:10]:
            self.gallery_list.addItem(filename)
    
    def load_from_gallery(self, item):
        """Load image from gallery"""
        filename = item.text()
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if os.path.exists(filepath):
            self.current_image_path = filepath
            self.canvas.display_image(filepath)
            self.status_label.setText(f"📂 Loaded: {filename}")
        else:
            self.status_label.setText(f"❌ File not found: {filename}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    studio = CRODArtStudio()
    studio.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()