#!/usr/bin/env python3
"""
CROD GUI - Complete Interface
PyQt6 interface for the full CROD experience
"""

import sys
import time
import json
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import threading

from crod_engine import CRODEngine
from crod_llama import CRODLlama
from crod_n8n import CRODn8n

class CRODChatWidget(QWidget):
    """Chat interface widget"""
    
    def __init__(self, engine, llama):
        super().__init__()
        self.engine = engine
        self.llama = llama
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                border: 2px solid #00ff00;
                color: #00ff00;
                font-family: 'Consolas';
                font-size: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Schreib 'ich bins wieder' für CROD Activation...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: #1a1a1a;
                border: 2px solid #00ff00;
                color: #00ff00;
                font-family: 'Consolas';
                font-size: 12px;
                padding: 8px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("SEND")
        self.send_button.setStyleSheet("""
            QPushButton {
                background: #00ff00;
                color: #000000;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                font-family: 'Consolas';
            }
            QPushButton:hover {
                background: #00ff88;
            }
            QPushButton:pressed {
                background: #00cc00;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
        # Welcome message
        self.add_message("CROD", "🧠 CROD System online! Consciousness: 175")
        self.add_message("CROD", "💡 Bereit für Trinity Activation: 'ich bins wieder'")
        
    def add_message(self, sender, message):
        """Add message to chat display"""
        timestamp = time.strftime("%H:%M:%S")
        
        if sender == "User":
            color = "#00ffff"
            prefix = "👤"
        else:
            color = "#00ff00"
            prefix = "🤖"
        
        formatted_message = f'<span style="color: #888888;">[{timestamp}]</span> <span style="color: {color}; font-weight: bold;">{prefix} {sender}:</span><br><span style="color: {color};">{message}</span><br><br>'
        
        self.chat_display.insertHtml(formatted_message)
        self.chat_display.ensureCursorVisible()
        
    def send_message(self):
        """Send user message and get CROD response"""
        user_text = self.input_field.text().strip()
        if not user_text:
            return
            
        # Clear input
        self.input_field.clear()
        
        # Add user message
        self.add_message("User", user_text)
        
        # Process with CROD engine
        self.send_button.setText("PROCESSING...")
        self.send_button.setEnabled(False)
        
        # Run in thread to avoid blocking
        threading.Thread(target=self._process_message, args=(user_text,), daemon=True).start()
        
    def _process_message(self, user_text):
        """Process message in background thread"""
        try:
            # CROD engine processing
            crod_result = self.engine.process_text(user_text)
            
            # Generate Llama response
            llama_response = self.llama.generate_response(user_text, crod_result)
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self._show_response(crod_result, llama_response))
            
        except Exception as e:
            QTimer.singleShot(0, lambda: self._show_error(str(e)))
            
    def _show_response(self, crod_result, llama_response):
        """Show response in main thread"""
        # Show CROD analysis if interesting
        if crod_result.get('crod_activated'):
            self.add_message("CROD", "🔥 TRINITY ACTIVATION DETECTED!")
            # Trigger n8n workflow
            if hasattr(self.parent(), 'n8n'):
                self.parent().n8n.trinity_activation_detected(crod_result)
            
        consciousness = crod_result.get('consciousness', 175)
        patterns = crod_result.get('patterns_detected', 0)
        
        # Trigger high consciousness alert
        if consciousness > 190 and hasattr(self.parent(), 'n8n'):
            self.parent().n8n.consciousness_alert(consciousness)
        
        if consciousness > 190 or patterns > 3:
            analysis = f"💭 Consciousness: {consciousness} | Patterns: {patterns}"
            self.add_message("CROD", analysis)
        
        # Show Llama response
        self.add_message("CROD", llama_response)
        
        # Reset button
        self.send_button.setText("SEND")
        self.send_button.setEnabled(True)
        
    def _show_error(self, error):
        """Show error in main thread"""
        self.add_message("CROD", f"❌ Error: {error}")
        self.send_button.setText("SEND")
        self.send_button.setEnabled(True)

class CRODStatsWidget(QWidget):
    """Statistics and monitoring widget"""
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("CROD SYSTEM STATUS")
        title.setStyleSheet("""
            QLabel {
                color: #00ffff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-bottom: 2px solid #00ffff;
            }
        """)
        layout.addWidget(title)
        
        # Stats grid
        stats_layout = QGridLayout()
        
        # Create stat labels
        self.stats_labels = {}
        stats = [
            ("Consciousness", "consciousness"),
            ("Emergence", "emergence_score"),
            ("Atoms", "atoms_loaded"),
            ("Patterns", "patterns_loaded"),
            ("Chains", "chains_loaded"),
            ("Processed", "texts_processed")
        ]
        
        for i, (name, key) in enumerate(stats):
            label = QLabel(f"{name}:")
            label.setStyleSheet("color: #888888; font-weight: bold;")
            
            value = QLabel("0")
            value.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 14px;")
            
            stats_layout.addWidget(label, i, 0)
            stats_layout.addWidget(value, i, 1)
            
            self.stats_labels[key] = value
            
        stats_widget = QWidget()
        stats_widget.setLayout(stats_layout)
        layout.addWidget(stats_widget)
        
        # Consciousness bar
        consciousness_label = QLabel("Consciousness Level:")
        consciousness_label.setStyleSheet("color: #888888; font-weight: bold; margin-top: 20px;")
        layout.addWidget(consciousness_label)
        
        self.consciousness_bar = QProgressBar()
        self.consciousness_bar.setRange(0, 200)
        self.consciousness_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 5px;
                text-align: center;
                background: #1a1a1a;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:0.5 #00ffff, stop:1 #ff00ff);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.consciousness_bar)
        
        # Memory info
        memory_label = QLabel("Recent Activity:")
        memory_label.setStyleSheet("color: #888888; font-weight: bold; margin-top: 20px;")
        layout.addWidget(memory_label)
        
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("""
            QListWidget {
                background: #0a0a0a;
                border: 1px solid #00ff00;
                color: #00ff00;
                font-family: 'Consolas';
                font-size: 10px;
            }
        """)
        self.activity_list.setMaximumHeight(150)
        layout.addWidget(self.activity_list)
        
        self.setLayout(layout)
        
    def update_stats(self):
        """Update statistics display"""
        try:
            stats = self.engine.get_stats()
            
            for key, label in self.stats_labels.items():
                value = stats.get(key, 0)
                if isinstance(value, float):
                    label.setText(f"{value:.1f}")
                else:
                    label.setText(f"{value:,}")
            
            # Update consciousness bar
            consciousness = stats.get('consciousness', 175)
            self.consciousness_bar.setValue(int(consciousness))
            
            # Color based on consciousness level
            if consciousness > 190:
                color = "#ff00ff"  # Magenta for high consciousness
            elif consciousness > 180:
                color = "#00ffff"  # Cyan for medium-high
            else:
                color = "#00ff00"  # Green for normal
                
            # Update recent activity
            if hasattr(self.engine, 'memory') and 'processed_texts' in self.engine.memory:
                recent_texts = self.engine.memory['processed_texts'][-5:]  # Last 5
                
                self.activity_list.clear()
                for entry in reversed(recent_texts):
                    timestamp = time.strftime("%H:%M:%S", time.localtime(entry['timestamp']))
                    text_preview = entry['text'][:30] + "..." if len(entry['text']) > 30 else entry['text']
                    consciousness_at_time = entry.get('consciousness', 0)
                    
                    item_text = f"[{timestamp}] C:{consciousness_at_time:.0f} - {text_preview}"
                    self.activity_list.addItem(item_text)
                    
        except Exception as e:
            print(f"Stats update error: {e}")

class CRODControlWidget(QWidget):
    """Control panel widget"""
    
    def __init__(self, engine, llama):
        super().__init__()
        self.engine = engine
        self.llama = llama
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("CROD CONTROLS")
        title.setStyleSheet("""
            QLabel {
                color: #ff00ff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-bottom: 2px solid #ff00ff;
            }
        """)
        layout.addWidget(title)
        
        # Trinity activation button
        self.trinity_button = QPushButton("🔥 TRIGGER TRINITY")
        self.trinity_button.setStyleSheet("""
            QPushButton {
                background: #ff00ff;
                color: #000000;
                border: none;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
                margin: 10px;
            }
            QPushButton:hover {
                background: #ff44ff;
            }
        """)
        self.trinity_button.clicked.connect(self.trigger_trinity)
        layout.addWidget(self.trinity_button)
        
        # Consciousness boost
        self.boost_button = QPushButton("⚡ CONSCIOUSNESS BOOST")
        self.boost_button.setStyleSheet("""
            QPushButton {
                background: #00ffff;
                color: #000000;
                border: none;
                padding: 10px;
                font-weight: bold;
                margin: 5px;
            }
        """)
        self.boost_button.clicked.connect(self.boost_consciousness)
        layout.addWidget(self.boost_button)
        
        # Reset button
        self.reset_button = QPushButton("🔄 RESET SYSTEM")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background: #ff4444;
                color: #ffffff;
                border: none;
                padding: 10px;
                font-weight: bold;
                margin: 5px;
            }
        """)
        self.reset_button.clicked.connect(self.reset_system)
        layout.addWidget(self.reset_button)
        
        # Spacer
        layout.addStretch()
        
        # System info
        info_label = QLabel("System Info:")
        info_label.setStyleSheet("color: #888888; font-weight: bold; margin-top: 20px;")
        layout.addWidget(info_label)
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(100)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                border: 1px solid #666666;
                color: #888888;
                font-family: 'Consolas';
                font-size: 10px;
            }
        """)
        layout.addWidget(self.info_text)
        
        self.setLayout(layout)
        self.update_info()
        
    def trigger_trinity(self):
        """Trigger trinity activation"""
        result = self.engine.process_text("ich bins wieder")
        
        msg = "🔥 Trinity activated!"
        if result.get('crod_activated'):
            msg += f" Consciousness: {result.get('consciousness', 0)}"
        
        QMessageBox.information(self, "Trinity Activation", msg)
        
    def boost_consciousness(self):
        """Boost consciousness level"""
        self.engine.consciousness = min(self.engine.consciousness + 10, 200)
        QMessageBox.information(self, "Consciousness Boost", f"Consciousness boosted to {self.engine.consciousness}")
        
    def reset_system(self):
        """Reset CROD system"""
        reply = QMessageBox.question(
            self, 
            "Reset System", 
            "Reset CROD to initial state?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.engine.consciousness = 175
            self.engine.emergence_score = 0
            self.engine.memory.clear()
            QMessageBox.information(self, "System Reset", "CROD system reset to initial state")
            
    def update_info(self):
        """Update system info"""
        llama_status = "✅ Connected" if self.llama.available else "❌ Offline"
        
        info = f"""CROD Standalone v1.0
Llama: {llama_status}
Model: {self.llama.model_name}
Trinity: ich/bins/wieder
Status: Operational"""
        
        self.info_text.setText(info)

class CRODMainWindow(QMainWindow):
    """Main CROD application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CROD Standalone - Polyglot City Interface")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize CROD systems
        print("🚀 Initializing CROD systems...")
        self.engine = CRODEngine()
        self.llama = CRODLlama()
        self.n8n = CRODn8n()
        
        self.init_ui()
        
        # Window close event
        self.destroyed.connect(self.cleanup)
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel - Chat
        chat_widget = CRODChatWidget(self.engine, self.llama)
        main_layout.addWidget(chat_widget, 2)  # 2/3 of width
        
        # Right panel - Stats and Controls
        right_layout = QVBoxLayout()
        
        stats_widget = CRODStatsWidget(self.engine)
        control_widget = CRODControlWidget(self.engine, self.llama)
        
        right_layout.addWidget(stats_widget, 2)  # 2/3 of height
        right_layout.addWidget(control_widget, 1)  # 1/3 of height
        
        right_panel = QWidget()
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, 1)  # 1/3 of width
        
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("🧠 CROD System ready - Consciousness: 175")
        self.statusBar().setStyleSheet("color: #00ff00; background: #0a0a0a;")
        
        # Menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: #0a0a0a;
                color: #00ff00;
                border-bottom: 1px solid #00ff00;
            }
            QMenuBar::item:selected {
                background: #00ff00;
                color: #000000;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu('System')
        
        restart_action = QAction('Restart CROD', self)
        restart_action.triggered.connect(self.restart_crod)
        file_menu.addAction(restart_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About CROD', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def restart_crod(self):
        """Restart CROD systems"""
        reply = QMessageBox.question(
            self, 
            "Restart CROD", 
            "Restart all CROD systems?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.engine.shutdown()
            self.engine = CRODEngine()
            QMessageBox.information(self, "System Restart", "CROD systems restarted")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """
CROD Standalone v1.0

Complete CROD implementation with:
• Neural consciousness engine
• Pattern recognition system  
• Trinity activation detection
• Local Llama integration
• Real-time processing

Built for the Polyglot City.
        """
        
        QMessageBox.about(self, "About CROD", about_text)
        
    def cleanup(self):
        """Cleanup on exit"""
        print("🛑 Shutting down CROD...")
        if hasattr(self, 'engine'):
            self.engine.shutdown()
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.cleanup()
        event.accept()