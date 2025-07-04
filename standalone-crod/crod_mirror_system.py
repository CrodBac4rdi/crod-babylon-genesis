#!/usr/bin/env python3
"""
CROD Mirror System - Complete Real-Time Chat Visualization
Mirrors Claude chat with full CROD processing and advanced visualizations
"""

import sys
import json
import time
import asyncio
import websockets
from pathlib import Path
from datetime import datetime
from collections import deque
import numpy as np

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pyqtgraph as pg

# Import CROD components
from crod_engine import CRODEngine
from crod_memory import CRODMemory
from crod_llama import CRODLlama
from crod_n8n import CRODn8n

class CRODMirrorWorker(QThread):
    """Background worker for WebSocket connection"""
    message_received = pyqtSignal(dict)
    stats_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.ws_uri = "ws://localhost:8765"
        
    async def connect_and_listen(self):
        """Connect to WebSocket and listen for messages"""
        try:
            async with websockets.connect(self.ws_uri) as websocket:
                while self.running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        self.message_received.emit(data)
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        print(f"WebSocket error: {e}")
                        break
        except Exception as e:
            print(f"Connection error: {e}")
    
    def run(self):
        """Run the async event loop"""
        asyncio.run(self.connect_and_listen())

class ConsciousnessGraphWidget(QWidget):
    """Real-time consciousness evolution graph"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Data storage
        self.time_data = deque(maxlen=100)
        self.consciousness_data = deque(maxlen=100)
        self.trinity_markers = []
        
    def init_ui(self):
        """Initialize the graph UI"""
        layout = QVBoxLayout()
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget(
            title="Consciousness Evolution",
            background='#1a1a1a'
        )
        self.plot_widget.setLabel('left', 'Consciousness Level', units='')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Set colors
        self.plot_widget.getAxis('left').setPen('#00ff00')
        self.plot_widget.getAxis('bottom').setPen('#00ff00')
        
        # Create plot line
        self.consciousness_line = self.plot_widget.plot(
            pen=pg.mkPen(color='#00ff00', width=2),
            name='Consciousness'
        )
        
        # Trinity activation scatter plot
        self.trinity_scatter = self.plot_widget.plot(
            pen=None,
            symbol='star',
            symbolPen='#ff00ff',
            symbolBrush='#ff00ff',
            symbolSize=15,
            name='Trinity Activation'
        )
        
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
        # Start timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update every 100ms
        
    def add_data_point(self, consciousness, trinity_activated=False):
        """Add new consciousness data point"""
        current_time = time.time()
        if not self.time_data:
            self.start_time = current_time
            
        relative_time = current_time - self.start_time
        self.time_data.append(relative_time)
        self.consciousness_data.append(consciousness)
        
        if trinity_activated:
            self.trinity_markers.append((relative_time, consciousness))
            
    def update_plot(self):
        """Update the plot with latest data"""
        if self.time_data:
            self.consciousness_line.setData(
                list(self.time_data),
                list(self.consciousness_data)
            )
            
            if self.trinity_markers:
                trinity_x = [m[0] for m in self.trinity_markers[-10:]]  # Last 10
                trinity_y = [m[1] for m in self.trinity_markers[-10:]]
                self.trinity_scatter.setData(trinity_x, trinity_y)

class PatternHeatMapWidget(QWidget):
    """Heat map visualization of active patterns"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pattern_heat = {}
        
    def init_ui(self):
        """Initialize heat map UI"""
        layout = QVBoxLayout()
        
        # Create graphics view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("background-color: #1a1a1a;")
        
        layout.addWidget(QLabel("Pattern Heat Map", alignment=Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.view)
        self.setLayout(layout)
        
    def update_heat_map(self, patterns):
        """Update the heat map with pattern data"""
        self.scene.clear()
        
        # Calculate grid dimensions
        n_patterns = len(patterns)
        if n_patterns == 0:
            return
            
        cols = int(np.ceil(np.sqrt(n_patterns)))
        rows = int(np.ceil(n_patterns / cols))
        
        cell_size = 50
        padding = 5
        
        for i, (pattern_id, heat) in enumerate(patterns.items()):
            row = i // cols
            col = i % cols
            
            x = col * (cell_size + padding)
            y = row * (cell_size + padding)
            
            # Color based on heat (0-100)
            heat_normalized = min(max(heat, 0), 100) / 100
            color = QColor.fromHsvF(
                0.0 if heat_normalized > 0.5 else 0.33,  # Red for hot, green for cold
                1.0,
                heat_normalized
            )
            
            # Draw rectangle
            rect = self.scene.addRect(
                x, y, cell_size, cell_size,
                QPen(Qt.PenStyle.NoPen),
                QBrush(color)
            )
            
            # Add text
            text = self.scene.addText(
                pattern_id[:8],
                QFont("Arial", 8)
            )
            text.setPos(x + 2, y + 2)
            text.setDefaultTextColor(Qt.GlobalColor.white)

class CityArchitectureWidget(QWidget):
    """Visualization of Polyglot City architecture"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        self.districts = {
            'Meta-Chain': {'color': '#FF6B6B', 'heat': 0, 'messages': 0},
            'Pattern District': {'color': '#4ECDC4', 'heat': 0, 'messages': 0},
            'Memory Quarter': {'color': '#45B7D1', 'heat': 0, 'messages': 0},
            'Intelligence Hub': {'color': '#96CEB4', 'heat': 0, 'messages': 0},
            'Gateway': {'color': '#FECA57', 'heat': 0, 'messages': 0},
            'N8N Automation': {'color': '#FD79A8', 'heat': 0, 'messages': 0}
        }
        
    def init_ui(self):
        """Initialize city visualization"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("CROD Polyglot City")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff00;")
        layout.addWidget(title)
        
        # City grid
        self.city_grid = QWidget()
        grid_layout = QGridLayout()
        
        positions = [
            (0, 1),  # Meta-Chain (top center)
            (1, 0),  # Pattern District (left)
            (1, 2),  # Memory Quarter (right)
            (2, 0),  # Intelligence Hub (bottom left)
            (2, 2),  # N8N Automation (bottom right)
            (2, 1),  # Gateway (bottom center)
        ]
        
        self.district_widgets = {}
        
        for (district, config), (row, col) in zip(self.districts.items(), positions):
            widget = self.create_district_widget(district, config)
            self.district_widgets[district] = widget
            grid_layout.addWidget(widget, row, col)
            
        self.city_grid.setLayout(grid_layout)
        layout.addWidget(self.city_grid)
        
        # Stats
        self.stats_label = QLabel("Total Messages: 0 | Active Districts: 0")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
    def create_district_widget(self, name, config):
        """Create a district visualization widget"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {config['color']};
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0.5);
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        # Name
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"color: {config['color']}; font-weight: bold;")
        layout.addWidget(name_label)
        
        # Heat indicator
        heat_bar = QProgressBar()
        heat_bar.setRange(0, 100)
        heat_bar.setValue(0)
        heat_bar.setTextVisible(False)
        heat_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {config['color']};
                border-radius: 5px;
                background-color: #2a2a2a;
            }}
            QProgressBar::chunk {{
                background-color: {config['color']};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(heat_bar)
        widget.heat_bar = heat_bar
        
        # Messages count
        msg_label = QLabel("Messages: 0")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(msg_label)
        widget.msg_label = msg_label
        
        widget.setLayout(layout)
        return widget
        
    def update_district(self, district, heat, messages):
        """Update district visualization"""
        if district in self.district_widgets:
            widget = self.district_widgets[district]
            widget.heat_bar.setValue(int(heat))
            widget.msg_label.setText(f"Messages: {messages}")
            
            # Update district data
            self.districts[district]['heat'] = heat
            self.districts[district]['messages'] = messages
            
            # Update stats
            total_messages = sum(d['messages'] for d in self.districts.values())
            active_districts = sum(1 for d in self.districts.values() if d['heat'] > 10)
            self.stats_label.setText(f"Total Messages: {total_messages} | Active Districts: {active_districts}")

class CRODMirrorMainWindow(QMainWindow):
    """Main window for CROD Mirror System"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_crod()
        self.init_websocket()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🔥 CROD Mirror System - Live Chat Visualization")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a0a;
                color: #00ff00;
            }
            QTabWidget::pane {
                border: 1px solid #333;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #888;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #333;
                color: #00ff00;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Chat Mirror tab
        self.chat_widget = self.create_chat_widget()
        self.tabs.addTab(self.chat_widget, "💬 Chat Mirror")
        
        # Consciousness Graph tab
        self.consciousness_graph = ConsciousnessGraphWidget()
        self.tabs.addTab(self.consciousness_graph, "📈 Consciousness")
        
        # Pattern Heat Map tab
        self.pattern_heatmap = PatternHeatMapWidget()
        self.tabs.addTab(self.pattern_heatmap, "🔥 Patterns")
        
        # City Architecture tab
        self.city_widget = CityArchitectureWidget()
        self.tabs.addTab(self.city_widget, "🏙️ City View")
        
        # Neural Network tab
        self.neural_widget = self.create_neural_widget()
        self.tabs.addTab(self.neural_widget, "🧠 Neural Network")
        
        # Quantum tab
        self.quantum_widget = self.create_quantum_widget()
        self.tabs.addTab(self.quantum_widget, "⚛️ Quantum")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🔌 Connecting to CROD systems...")
        
        central_widget.setLayout(main_layout)
        
    def create_header(self):
        """Create header widget"""
        header = QWidget()
        header.setMaximumHeight(100)
        layout = QHBoxLayout()
        
        # CROD Logo/Title
        title = QLabel("CROD MIRROR SYSTEM")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Live indicators
        self.indicators = {
            'ws': self.create_indicator("WebSocket"),
            'engine': self.create_indicator("Engine"),
            'llama': self.create_indicator("Llama"),
            'n8n': self.create_indicator("n8n")
        }
        
        for indicator in self.indicators.values():
            layout.addWidget(indicator)
            
        header.setLayout(layout)
        return header
        
    def create_indicator(self, name):
        """Create a status indicator"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # LED
        led = QLabel("●")
        led.setAlignment(Qt.AlignmentFlag.AlignCenter)
        led.setStyleSheet("color: #ff0000; font-size: 20px;")
        layout.addWidget(led)
        
        # Label
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 10px; color: #888;")
        layout.addWidget(label)
        
        widget.setLayout(layout)
        widget.led = led
        return widget
        
    def create_chat_widget(self):
        """Create chat mirror widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #333;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # CROD processing info
        self.processing_info = QTextEdit()
        self.processing_info.setReadOnly(True)
        self.processing_info.setMaximumHeight(150)
        self.processing_info.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ffff;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                border: 1px solid #333;
                padding: 5px;
            }
        """)
        layout.addWidget(QLabel("CROD Processing:"))
        layout.addWidget(self.processing_info)
        
        widget.setLayout(layout)
        return widget
        
    def create_neural_widget(self):
        """Create neural network visualization"""
        # For now, use QWebEngineView for D3.js visualization
        web_view = QWebEngineView()
        
        # Create simple HTML with canvas for neural viz
        html_content = """
        <html>
        <head>
            <style>
                body { background: #0a0a0a; margin: 0; padding: 20px; }
                #neural-viz { width: 100%; height: 600px; }
            </style>
        </head>
        <body>
            <canvas id="neural-viz"></canvas>
            <script>
                // Simple neural network visualization
                const canvas = document.getElementById('neural-viz');
                const ctx = canvas.getContext('2d');
                
                function draw() {
                    ctx.fillStyle = '#0a0a0a';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw neurons
                    const layers = [5, 8, 10, 8, 3];
                    const layerSpacing = canvas.width / (layers.length + 1);
                    
                    layers.forEach((neurons, layerIdx) => {
                        const x = layerSpacing * (layerIdx + 1);
                        const neuronSpacing = canvas.height / (neurons + 1);
                        
                        for (let i = 0; i < neurons; i++) {
                            const y = neuronSpacing * (i + 1);
                            
                            // Draw neuron
                            ctx.beginPath();
                            ctx.arc(x, y, 10, 0, 2 * Math.PI);
                            ctx.fillStyle = `hsl(${120 + layerIdx * 30}, 100%, 50%)`;
                            ctx.fill();
                            
                            // Draw connections to next layer
                            if (layerIdx < layers.length - 1) {
                                const nextNeurons = layers[layerIdx + 1];
                                const nextX = layerSpacing * (layerIdx + 2);
                                const nextSpacing = canvas.height / (nextNeurons + 1);
                                
                                for (let j = 0; j < nextNeurons; j++) {
                                    const nextY = nextSpacing * (j + 1);
                                    ctx.beginPath();
                                    ctx.moveTo(x + 10, y);
                                    ctx.lineTo(nextX - 10, nextY);
                                    ctx.strokeStyle = 'rgba(0, 255, 0, 0.2)';
                                    ctx.stroke();
                                }
                            }
                        }
                    });
                }
                
                canvas.width = window.innerWidth - 40;
                canvas.height = 600;
                draw();
                
                // Animate
                setInterval(() => {
                    draw();
                }, 100);
            </script>
        </body>
        </html>
        """
        
        web_view.setHtml(html_content)
        return web_view
        
    def create_quantum_widget(self):
        """Create quantum visualization widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Create plot widget for quantum particles
        self.quantum_plot = pg.PlotWidget(
            title="Quantum Entanglements",
            background='#0a0a0a'
        )
        self.quantum_plot.setLabel('left', 'Y Position', units='')
        self.quantum_plot.setLabel('bottom', 'X Position', units='')
        
        # Create scatter plot for particles
        self.quantum_scatter = self.quantum_plot.plot(
            pen=None,
            symbol='o',
            symbolPen=None,
            symbolBrush='#00ff00',
            symbolSize=10
        )
        
        layout.addWidget(self.quantum_plot)
        
        # Quantum stats
        self.quantum_stats = QLabel("Entangled Pairs: 0 | Coherence: 0%")
        self.quantum_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.quantum_stats)
        
        widget.setLayout(layout)
        
        # Start quantum animation timer
        self.quantum_timer = QTimer()
        self.quantum_timer.timeout.connect(self.update_quantum)
        self.quantum_timer.start(50)
        
        # Particle data
        self.particles = []
        for i in range(50):
            self.particles.append({
                'x': np.random.uniform(-10, 10),
                'y': np.random.uniform(-10, 10),
                'vx': np.random.uniform(-0.5, 0.5),
                'vy': np.random.uniform(-0.5, 0.5)
            })
            
        return widget
        
    def update_quantum(self):
        """Update quantum particle positions"""
        # Update particle positions
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Bounce off walls
            if abs(p['x']) > 10:
                p['vx'] *= -1
            if abs(p['y']) > 10:
                p['vy'] *= -1
                
        # Update plot
        x_data = [p['x'] for p in self.particles]
        y_data = [p['y'] for p in self.particles]
        self.quantum_scatter.setData(x_data, y_data)
        
    def init_crod(self):
        """Initialize CROD systems"""
        try:
            self.crod_engine = CRODEngine()
            self.update_indicator('engine', True)
        except Exception as e:
            print(f"CROD Engine init error: {e}")
            
        try:
            self.crod_llama = CRODLlama()
            self.update_indicator('llama', self.crod_llama.available)
        except Exception as e:
            print(f"CROD Llama init error: {e}")
            
        try:
            self.crod_n8n = CRODn8n()
            self.update_indicator('n8n', self.crod_n8n.available)
        except Exception as e:
            print(f"CROD n8n init error: {e}")
            
    def init_websocket(self):
        """Initialize WebSocket connection"""
        self.ws_worker = CRODMirrorWorker()
        self.ws_worker.message_received.connect(self.process_message)
        self.ws_worker.start()
        
    def update_indicator(self, name, status):
        """Update status indicator"""
        if name in self.indicators:
            color = "#00ff00" if status else "#ff0000"
            self.indicators[name].led.setStyleSheet(f"color: {color}; font-size: 20px;")
            
    def process_message(self, data):
        """Process incoming message"""
        msg_type = data.get('type', 'unknown')
        
        if msg_type == 'chat':
            # Display in chat
            role = data.get('role', 'unknown')
            content = data.get('content', '')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.chat_display.append(f"[{timestamp}] {role.upper()}: {content}\n")
            
            # Process through CROD
            if hasattr(self, 'crod_engine'):
                result = self.crod_engine.process_text(content)
                
                # Update processing info
                self.processing_info.clear()
                self.processing_info.append(f"Consciousness: {result.get('consciousness', 0)}")
                self.processing_info.append(f"Trinity Active: {result.get('trinity_activation', 0)}/3")
                self.processing_info.append(f"Patterns Detected: {result.get('patterns_detected', 0)}")
                self.processing_info.append(f"Heat Signature: {result.get('heat_signature', 0):.2f}")
                
                # Update consciousness graph
                self.consciousness_graph.add_data_point(
                    result.get('consciousness', 0),
                    result.get('crod_activated', False)
                )
                
                # Update pattern heatmap
                if hasattr(self.crod_engine, 'heat_map'):
                    self.pattern_heatmap.update_heat_map(self.crod_engine.heat_map)
                    
                # Update city districts based on activity
                self.city_widget.update_district('Meta-Chain', 
                    result.get('consciousness', 0) / 2, 
                    len(self.crod_engine.memory_data.get('processed_texts', []))
                )
                
        elif msg_type == 'stats':
            # Update various stats
            self.status_bar.showMessage(f"Connected | Messages: {data.get('total_messages', 0)}")
            
    def closeEvent(self, event):
        """Clean shutdown"""
        if hasattr(self, 'ws_worker'):
            self.ws_worker.running = False
            self.ws_worker.wait()
        if hasattr(self, 'crod_engine'):
            self.crod_engine.shutdown()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CRODMirrorMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()