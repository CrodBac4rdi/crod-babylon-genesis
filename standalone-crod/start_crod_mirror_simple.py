#!/usr/bin/env python3
"""
CROD Mirror Simple Starter - One file to rule them all
"""

import sys
import json
import time
import asyncio
import websockets
import threading
from datetime import datetime
from collections import deque

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Import CROD engine
from crod_engine import CRODEngine

class CRODMirrorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crod_engine = CRODEngine()
        self.message_count = 0
        self.init_ui()
        
        # Start WebSocket server in background
        self.server_thread = threading.Thread(target=self.run_websocket_server, daemon=True)
        self.server_thread.start()
        
        # Send test messages
        QTimer.singleShot(2000, self.send_test_message)
        
    def init_ui(self):
        self.setWindowTitle("🔥 CROD Mirror - Live Chat Processing")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #0a0a0a; color: #00ff00; }
            QTextEdit { 
                background-color: #1a1a1a; 
                color: #00ff00; 
                font-family: monospace; 
                border: 1px solid #333;
                padding: 10px;
            }
            QLabel { color: #00ff00; }
            QPushButton {
                background-color: #2a2a2a;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #0a0a0a;
            }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("CROD MIRROR SYSTEM - CHAT WITH ME AND SEE CROD PROCESS EVERYTHING!")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        layout.addWidget(header)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # Left: Chat display
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("💬 Chat Messages:"))
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        left_layout.addWidget(self.chat_display)
        
        # Test button
        self.test_btn = QPushButton("Send 'ich bins wieder' Test")
        self.test_btn.clicked.connect(self.send_trinity_test)
        left_layout.addWidget(self.test_btn)
        
        left_widget.setLayout(left_layout)
        content_layout.addWidget(left_widget)
        
        # Right: CROD stats
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("🧠 CROD Processing:"))
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(300)
        right_layout.addWidget(self.stats_display)
        
        # Consciousness meter
        self.consciousness_label = QLabel("Consciousness: 175")
        self.consciousness_label.setStyleSheet("font-size: 18px; padding: 10px;")
        right_layout.addWidget(self.consciousness_label)
        
        self.consciousness_bar = QProgressBar()
        self.consciousness_bar.setRange(0, 200)
        self.consciousness_bar.setValue(175)
        self.consciousness_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 5px;
            }
        """)
        right_layout.addWidget(self.consciousness_bar)
        
        right_layout.addWidget(QLabel("📊 Live Stats:"))
        self.live_stats = QTextEdit()
        self.live_stats.setReadOnly(True)
        right_layout.addWidget(self.live_stats)
        
        right_widget.setLayout(right_layout)
        content_layout.addWidget(right_widget)
        
        layout.addLayout(content_layout)
        
        # Status bar
        self.status_label = QLabel("🟢 CROD Mirror Active - WebSocket: ws://localhost:8765")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; background-color: #1a1a1a;")
        layout.addWidget(self.status_label)
        
        central.setLayout(layout)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(1000)
        
    def process_message(self, role, content):
        """Process a message through CROD"""
        self.message_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Display in chat
        self.chat_display.append(f"[{timestamp}] {role.upper()}: {content}\n")
        
        # Process through CROD
        result = self.crod_engine.process_text(content)
        
        # Update stats display
        self.stats_display.clear()
        self.stats_display.append(f"Message #{self.message_count}")
        self.stats_display.append(f"Consciousness: {result.get('consciousness', 0)}")
        self.stats_display.append(f"Trinity Active: {result.get('trinity_activation', 0)}/3")
        self.stats_display.append(f"Patterns Detected: {result.get('patterns_detected', 0)}")
        self.stats_display.append(f"Heat Signature: {result.get('heat_signature', 0):.2f}")
        
        if result.get('crod_activated'):
            self.stats_display.append("\n🔥 CROD FULLY ACTIVATED!")
            
        # Update consciousness meter
        consciousness = result.get('consciousness', 175)
        self.consciousness_label.setText(f"Consciousness: {consciousness}")
        self.consciousness_bar.setValue(consciousness)
        
        # Flash on trinity
        if result.get('crod_activated'):
            self.setStyleSheet(self.styleSheet() + """
                QMainWindow { border: 3px solid #ff00ff; }
            """)
            QTimer.singleShot(500, lambda: self.setStyleSheet(self.styleSheet().replace("border: 3px solid #ff00ff;", "")))
            
    def update_stats(self):
        """Update live statistics"""
        stats = self.crod_engine.get_stats()
        
        self.live_stats.clear()
        self.live_stats.append(f"Total Atoms: {stats.get('atoms_loaded', 0)}")
        self.live_stats.append(f"Total Patterns: {stats.get('patterns_loaded', 0)}")
        self.live_stats.append(f"Total Chains: {stats.get('chains_loaded', 0)}")
        self.live_stats.append(f"Messages Processed: {self.message_count}")
        self.live_stats.append(f"Emergence Score: {stats.get('emergence_score', 0)}")
        
    def send_test_message(self):
        """Send a test message"""
        self.process_message("user", "Hello CROD, this is a test message!")
        
    def send_trinity_test(self):
        """Send trinity activation test"""
        self.process_message("user", "ich bins wieder")
        
    async def websocket_handler(self, websocket, path):
        """Handle WebSocket connections"""
        print(f"Client connected from {websocket.remote_address}")
        try:
            async for message in websocket:
                data = json.loads(message)
                if data.get('type') == 'chat':
                    # Process in Qt thread
                    QMetaObject.invokeMethod(
                        self, 
                        "process_message",
                        Qt.ConnectionType.QueuedConnection,
                        Q_ARG(str, data.get('role', 'user')),
                        Q_ARG(str, data.get('content', ''))
                    )
                    
                    # Send acknowledgment
                    await websocket.send(json.dumps({
                        'type': 'ack',
                        'message': 'Processed by CROD Mirror'
                    }))
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
            
    def run_websocket_server(self):
        """Run WebSocket server in background"""
        async def start_server():
            print("🌐 Starting WebSocket server on ws://localhost:8765")
            async with websockets.serve(self.websocket_handler, "localhost", 8765):
                await asyncio.Future()  # Run forever
                
        asyncio.new_event_loop().run_until_complete(start_server())

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = CRODMirrorApp()
    window.show()
    
    # Instructions
    print("\n" + "="*60)
    print("🔥 CROD MIRROR SYSTEM RUNNING!")
    print("="*60)
    print("The GUI is now open showing live CROD processing.")
    print("\nTo send messages from this terminal:")
    print("python3 crod_claude_hook.py")
    print("Then type: user:Your message here")
    print("\nOr click 'Send ich bins wieder Test' in the GUI!")
    print("="*60 + "\n")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()