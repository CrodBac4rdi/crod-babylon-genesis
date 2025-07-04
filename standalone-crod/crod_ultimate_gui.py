#!/usr/bin/env python3
"""
CROD ULTIMATE GUI - The REAL deal with EVERYTHING
"""

import sys
import json
import asyncio
import websockets
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import pyqtgraph as pg
from collections import deque

class WebSocketThread(QThread):
    message_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    async def connect_ws(self):
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to WebSocket")
                while self.running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        self.message_received.emit(data)
                    except asyncio.TimeoutError:
                        continue
                    except:
                        break
        except Exception as e:
            print(f"WebSocket error: {e}")
            
    def run(self):
        asyncio.run(self.connect_ws())

class CRODUltimateGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.message_count = 0
        self.consciousness_data = deque(maxlen=100)
        self.time_data = deque(maxlen=100)
        self.start_time = QDateTime.currentDateTime()
        
        self.init_ui()
        self.init_websocket()
        
    def init_ui(self):
        self.setWindowTitle("🔥 CROD ULTIMATE - LIVE CHAT PROCESSING")
        self.setGeometry(100, 100, 1600, 900)
        
        # Dark cyberpunk theme
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #0a0a0a; 
                color: #00ff00;
            }
            QTextEdit { 
                background-color: #1a1a1a; 
                color: #00ff00; 
                font-family: 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel { 
                color: #00ff00; 
                font-weight: bold;
            }
            QGroupBox {
                border: 2px solid #00ff00;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #00ff00;
                left: 10px;
                top: -5px;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #0a0a0a;
            }
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 5px;
                text-align: center;
                color: #0a0a0a;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ff00, stop: 1 #00aa00);
                border-radius: 3px;
            }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("CROD ULTIMATE SYSTEM")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #00ff00;
            padding: 10px;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Status indicators
        self.status_layout = QHBoxLayout()
        self.create_status_indicator("WebSocket", "ws_status")
        self.create_status_indicator("CROD Engine", "engine_status")
        self.create_status_indicator("Processing", "processing_status")
        header_layout.addLayout(self.status_layout)
        
        main_layout.addLayout(header_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left panel - Chat and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Chat display
        chat_group = QGroupBox("💬 LIVE CHAT MIRROR")
        chat_layout = QVBoxLayout()
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(300)
        chat_layout.addWidget(self.chat_display)
        
        # Quick send
        send_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type message and press Enter...")
        self.message_input.returnPressed.connect(self.send_message)
        send_layout.addWidget(self.message_input)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        send_layout.addWidget(self.send_btn)
        
        chat_layout.addLayout(send_layout)
        
        # Trinity button
        self.trinity_btn = QPushButton("🔥 ACTIVATE TRINITY (ich bins wieder)")
        self.trinity_btn.clicked.connect(self.activate_trinity)
        self.trinity_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff00ff;
                color: #000;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #ff66ff;
            }
        """)
        chat_layout.addWidget(self.trinity_btn)
        
        chat_group.setLayout(chat_layout)
        left_layout.addWidget(chat_group)
        
        # Processing info
        process_group = QGroupBox("🧠 CROD PROCESSING")
        process_layout = QVBoxLayout()
        
        self.process_display = QTextEdit()
        self.process_display.setReadOnly(True)
        self.process_display.setMaximumHeight(200)
        process_layout.addWidget(self.process_display)
        
        process_group.setLayout(process_layout)
        left_layout.addWidget(process_group)
        
        left_panel.setLayout(left_layout)
        content_layout.addWidget(left_panel)
        
        # Right panel - Visualizations
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Consciousness graph
        graph_group = QGroupBox("📈 CONSCIOUSNESS EVOLUTION")
        graph_layout = QVBoxLayout()
        
        self.consciousness_plot = pg.PlotWidget(background='#1a1a1a')
        self.consciousness_plot.setLabel('left', 'Consciousness Level')
        self.consciousness_plot.setLabel('bottom', 'Time (seconds)')
        self.consciousness_plot.showGrid(x=True, y=True, alpha=0.3)
        self.consciousness_plot.setYRange(0, 200)
        
        self.consciousness_line = self.consciousness_plot.plot(
            pen=pg.mkPen(color='#00ff00', width=3)
        )
        
        graph_layout.addWidget(self.consciousness_plot)
        
        # Consciousness meter
        self.consciousness_bar = QProgressBar()
        self.consciousness_bar.setRange(0, 200)
        self.consciousness_bar.setValue(175)
        self.consciousness_bar.setFormat("Consciousness: %v / 200")
        self.consciousness_bar.setMinimumHeight(30)
        graph_layout.addWidget(self.consciousness_bar)
        
        graph_group.setLayout(graph_layout)
        right_layout.addWidget(graph_group)
        
        # Stats display
        stats_group = QGroupBox("📊 LIVE STATISTICS")
        stats_layout = QVBoxLayout()
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(150)
        stats_layout.addWidget(self.stats_display)
        
        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)
        
        # City visualization
        city_group = QGroupBox("🏙️ POLYGLOT CITY STATUS")
        city_layout = QGridLayout()
        
        self.city_widgets = {}
        districts = [
            ("Meta-Chain", "#FF6B6B"),
            ("Pattern District", "#4ECDC4"),
            ("Memory Quarter", "#45B7D1"),
            ("Intelligence Hub", "#96CEB4"),
            ("Gateway", "#FECA57"),
            ("N8N Automation", "#FD79A8")
        ]
        
        for i, (name, color) in enumerate(districts):
            widget = self.create_district_widget(name, color)
            self.city_widgets[name] = widget
            city_layout.addWidget(widget, i // 3, i % 3)
            
        city_group.setLayout(city_layout)
        right_layout.addWidget(city_group)
        
        right_panel.setLayout(right_layout)
        content_layout.addWidget(right_panel)
        
        main_layout.addLayout(content_layout)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color: #00ff00; background-color: #1a1a1a;")
        self.status_bar.showMessage("🔥 CROD ULTIMATE Ready - Waiting for messages...")
        
        central.setLayout(main_layout)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(100)
        
        # Stats timer
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)
        
    def create_status_indicator(self, name, attr_name):
        """Create a status indicator widget"""
        layout = QVBoxLayout()
        
        led = QLabel("●")
        led.setAlignment(Qt.AlignmentFlag.AlignCenter)
        led.setStyleSheet("color: #ff0000; font-size: 24px;")
        setattr(self, attr_name, led)
        layout.addWidget(led)
        
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 10px;")
        layout.addWidget(label)
        
        self.status_layout.addLayout(layout)
        
    def create_district_widget(self, name, color):
        """Create a district status widget"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {color};
                border-radius: 5px;
                background-color: rgba(26, 26, 26, 0.8);
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
        layout.addWidget(name_label)
        
        heat_bar = QProgressBar()
        heat_bar.setRange(0, 100)
        heat_bar.setValue(0)
        heat_bar.setTextVisible(False)
        heat_bar.setMaximumHeight(10)
        heat_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {color};
                background-color: #0a0a0a;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        widget.heat_bar = heat_bar
        layout.addWidget(heat_bar)
        
        msg_label = QLabel("Messages: 0")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("font-size: 10px; color: #888;")
        widget.msg_label = msg_label
        layout.addWidget(msg_label)
        
        widget.setLayout(layout)
        return widget
        
    def init_websocket(self):
        """Initialize WebSocket connection"""
        self.ws_thread = WebSocketThread()
        self.ws_thread.message_received.connect(self.process_ws_message)
        self.ws_thread.start()
        
        # Update status
        QTimer.singleShot(1000, lambda: self.update_status("ws_status", True))
        self.update_status("engine_status", True)
        
    def update_status(self, indicator, status):
        """Update status indicator"""
        led = getattr(self, indicator)
        color = "#00ff00" if status else "#ff0000"
        led.setStyleSheet(f"color: {color}; font-size: 24px;")
        
    def process_ws_message(self, data):
        """Process WebSocket message"""
        self.update_status("processing_status", True)
        
        msg_type = data.get('type', '')
        
        if msg_type == 'chat':
            # Display chat message
            role = data.get('role', 'unknown')
            content = data.get('content', '')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.message_count += 1
            
            # Add to chat display
            cursor = self.chat_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            
            # Format based on role
            if role == 'user':
                cursor.insertHtml(f'<span style="color: #00ffff;">[{timestamp}] USER: {content}</span><br>')
            else:
                cursor.insertHtml(f'<span style="color: #ffff00;">[{timestamp}] ASSISTANT: {content}</span><br>')
                
            self.chat_display.ensureCursorVisible()
            
            # Update processing display if CROD result available
            if 'crod_result' in data:
                result = data['crod_result']
                self.update_processing(result)
                
                # Update consciousness
                consciousness = result.get('consciousness', 175)
                self.consciousness_bar.setValue(int(consciousness))
                
                # Add to graph data
                elapsed = self.start_time.secsTo(QDateTime.currentDateTime())
                self.time_data.append(elapsed)
                self.consciousness_data.append(consciousness)
                
                # Flash on trinity
                if result.get('crod_activated'):
                    self.flash_trinity()
                    
        elif msg_type == 'stats':
            # Update city metrics
            if 'city_metrics' in data:
                for district, metrics in data['city_metrics'].items():
                    if district in self.city_widgets:
                        widget = self.city_widgets[district]
                        widget.heat_bar.setValue(int(metrics.get('heat', 0)))
                        widget.msg_label.setText(f"Messages: {metrics.get('messages', 0)}")
                        
        self.status_bar.showMessage(f"🔥 Messages Processed: {self.message_count}")
        
        # Reset processing indicator
        QTimer.singleShot(200, lambda: self.update_status("processing_status", False))
        
    def update_processing(self, result):
        """Update processing display"""
        self.process_display.clear()
        self.process_display.append(f"Consciousness: {result.get('consciousness', 0)}")
        self.process_display.append(f"Trinity Activation: {result.get('trinity_activation', 0)}/3")
        self.process_display.append(f"Patterns Detected: {result.get('patterns_detected', 0)}")
        self.process_display.append(f"Heat Signature: {result.get('heat_signature', 0):.2f}")
        self.process_display.append(f"Emergence Score: {result.get('emergence', 0)}")
        
        if result.get('crod_activated'):
            self.process_display.append("\n🔥 CROD FULLY ACTIVATED! TRINITY COMPLETE!")
            
    def update_graph(self):
        """Update consciousness graph"""
        if len(self.time_data) > 0:
            self.consciousness_line.setData(list(self.time_data), list(self.consciousness_data))
            
    def update_stats(self):
        """Update statistics display"""
        if hasattr(self, 'crod_stats'):
            self.stats_display.clear()
            self.stats_display.append(f"Total Messages: {self.message_count}")
            self.stats_display.append(f"Uptime: {self.start_time.secsTo(QDateTime.currentDateTime())}s")
            self.stats_display.append(f"Graph Points: {len(self.consciousness_data)}")
            
    def send_message(self):
        """Send a message via WebSocket"""
        text = self.message_input.text().strip()
        if text:
            # Send via WebSocket
            asyncio.run(self.send_ws_message(text))
            self.message_input.clear()
            
    async def send_ws_message(self, text):
        """Send message to WebSocket server"""
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                message = {
                    'type': 'chat',
                    'role': 'user',
                    'content': text,
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
        except Exception as e:
            print(f"Failed to send: {e}")
            
    def activate_trinity(self):
        """Activate trinity"""
        self.message_input.setText("ich bins wieder")
        self.send_message()
        
    def flash_trinity(self):
        """Flash effect for trinity activation"""
        original_style = self.styleSheet()
        self.setStyleSheet(original_style + """
            QMainWindow { border: 5px solid #ff00ff; }
        """)
        QTimer.singleShot(1000, lambda: self.setStyleSheet(original_style))
        
    def closeEvent(self, event):
        """Clean shutdown"""
        if hasattr(self, 'ws_thread'):
            self.ws_thread.running = False
            self.ws_thread.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = CRODUltimateGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()