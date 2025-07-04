"""
CROD CHAT UI - Claude-style Chat Interface mit Ollama
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
import json
from datetime import datetime
from network import CRODNetwork
from database import get_database

class ChatMessage(QWidget):
    """Single chat message widget"""
    
    def __init__(self, text, is_user=True, timestamp=None):
        super().__init__()
        self.init_ui(text, is_user, timestamp)
        
    def init_ui(self, text, is_user, timestamp):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Message bubble
        bubble = QTextEdit()
        bubble.setReadOnly(True)
        bubble.setPlainText(text)
        bubble.setMaximumHeight(150)
        bubble.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Style based on sender
        if is_user:
            bubble.setStyleSheet("""
                QTextEdit {
                    background-color: #4A5568;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
            """)
            layout.addStretch()
            layout.addWidget(bubble, 1)
        else:
            bubble.setStyleSheet("""
                QTextEdit {
                    background-color: #2D3748;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
            """)
            layout.addWidget(bubble, 1)
            layout.addStretch()
            
        # Adjust height to content
        bubble.document().setDocumentMargin(10)
        height = bubble.document().size().height() + 20
        bubble.setFixedHeight(min(int(height), 150))

class CRODChatUI(QMainWindow):
    """Main Chat UI Window"""
    
    def __init__(self):
        super().__init__()
        self.ollama_base_url = "http://localhost:11434"
        self.current_model = "llama2"
        self.crod_network = None
        self.db = get_database()
        self.auto_mode = False
        self.conversation_history = []
        self.init_ui()
        self.check_ollama()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("CROD Chat - Ollama Integration")
        self.setGeometry(100, 100, 900, 700)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A202C;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4A5568;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #718096;
            }
            QPushButton:pressed {
                background-color: #2D3748;
            }
            QLineEdit, QTextEdit {
                background-color: #2D3748;
                color: white;
                border: 1px solid #4A5568;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox {
                background-color: #4A5568;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QCheckBox {
                color: white;
            }
            QScrollBar:vertical {
                background-color: #2D3748;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #4A5568;
                border-radius: 5px;
            }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Top toolbar
        toolbar = QHBoxLayout()
        
        # Model selector
        toolbar.addWidget(QLabel("Model:"))
        self.model_selector = QComboBox()
        self.model_selector.addItems(["llama2", "mistral", "neural-chat", "codellama"])
        self.model_selector.currentTextChanged.connect(self.change_model)
        toolbar.addWidget(self.model_selector)
        
        toolbar.addSpacing(20)
        
        # Auto mode checkbox
        self.auto_checkbox = QCheckBox("Auto Mode")
        self.auto_checkbox.stateChanged.connect(self.toggle_auto_mode)
        toolbar.addWidget(self.auto_checkbox)
        
        # CROD Network checkbox
        self.crod_checkbox = QCheckBox("Enable CROD Network")
        self.crod_checkbox.setChecked(True)
        self.crod_checkbox.stateChanged.connect(self.toggle_crod)
        toolbar.addWidget(self.crod_checkbox)
        
        toolbar.addStretch()
        
        # Status indicator
        self.status_label = QLabel("⚫ Disconnected")
        toolbar.addWidget(self.status_label)
        
        layout.addLayout(toolbar)
        
        # Chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #1A202C;
                border: none;
            }
        """)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch()
        
        self.chat_scroll.setWidget(self.chat_widget)
        layout.addWidget(self.chat_scroll)
        
        # CROD stats panel
        self.stats_panel = QWidget()
        self.stats_panel.setMaximumHeight(100)
        self.stats_panel.setStyleSheet("""
            QWidget {
                background-color: #2D3748;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        stats_layout = QHBoxLayout(self.stats_panel)
        
        self.stats_label = QLabel("CROD Network: Idle")
        self.stats_label.setStyleSheet("color: #90CDF4;")
        stats_layout.addWidget(self.stats_label)
        
        layout.addWidget(self.stats_panel)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Auto mode timer
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_generate)
        
        # CROD update timer
        self.crod_timer = QTimer()
        self.crod_timer.timeout.connect(self.update_crod_stats)
        self.crod_timer.start(500)
        
    def check_ollama(self):
        """Check Ollama connection"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.status_label.setText("🟢 Connected")
                self.status_label.setStyleSheet("color: #68D391;")
                return True
        except:
            pass
            
        self.status_label.setText("🔴 Ollama Offline")
        self.status_label.setStyleSheet("color: #FC8181;")
        return False
        
    def change_model(self, model):
        """Change Ollama model"""
        self.current_model = model
        self.add_system_message(f"Switched to model: {model}")
        
    def toggle_auto_mode(self, state):
        """Toggle auto mode"""
        self.auto_mode = state == Qt.Checked
        if self.auto_mode:
            self.auto_timer.start(3000)  # Generate every 3 seconds
            self.add_system_message("Auto mode enabled - generating messages automatically")
        else:
            self.auto_timer.stop()
            self.add_system_message("Auto mode disabled")
            
    def toggle_crod(self, state):
        """Toggle CROD network"""
        if state == Qt.Checked:
            self.init_crod_network()
            self.add_system_message("CROD Network enabled")
        else:
            self.crod_network = None
            self.add_system_message("CROD Network disabled")
            
    def init_crod_network(self):
        """Initialize CROD network"""
        self.crod_network = CRODNetwork(name="Chat-CROD")
        
        # Build chat-optimized network
        self.thinker = self.crod_network.add_atom("thinker", (0, 0))
        self.doubter = self.crod_network.add_atom("doubter", (200, 0))
        self.learner = self.crod_network.add_atom("learner", (400, 0))
        self.memory = self.crod_network.add_atom("memory", (600, 0))
        self.synthesizer = self.crod_network.add_atom("synthesizer", (800, 0))
        
        # Connect atoms
        self.crod_network.connect_atoms(self.thinker.id, "thought", self.doubter.id, "thought")
        self.crod_network.connect_atoms(self.doubter.id, "confidence", self.learner.id, "experience")
        self.crod_network.connect_atoms(self.learner.id, "pattern", self.memory.id, "data")
        self.crod_network.connect_atoms(self.memory.id, "retrieved", self.synthesizer.id, "concept_a")
        
        # Configure for chat
        self.thinker.configure({"creativity": 0.8})
        self.learner.configure({"learning_rate": 0.6})
        self.memory.configure({"capacity": 500})
        
    def add_message(self, text, is_user=True):
        """Add message to chat"""
        msg = ChatMessage(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, msg)
        
        # Auto scroll
        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))
        
        # Save to history
        self.conversation_history.append({
            "text": text,
            "is_user": is_user,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_system_message(self, text):
        """Add system message"""
        label = QLabel(f"⚡ {text}")
        label.setStyleSheet("color: #9CA3AF; padding: 5px;")
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, label)
        
    def send_message(self):
        """Send user message"""
        text = self.input_field.text().strip()
        if not text:
            return
            
        # Add user message
        self.add_message(text, is_user=True)
        self.input_field.clear()
        
        # Process with CROD if enabled
        if self.crod_network:
            self.process_with_crod(text)
            
        # Get Ollama response
        QTimer.singleShot(100, lambda: self.get_ollama_response(text))
        
    def process_with_crod(self, text):
        """Process message through CROD network"""
        # Feed to thinker
        self.thinker.receive_input("context", {"user_input": text})
        
        # Run network cycles
        for _ in range(5):
            self.crod_network.tick()
            
    def get_ollama_response(self, prompt):
        """Get response from Ollama"""
        if not self.check_ollama():
            self.add_message("Error: Ollama is not running", is_user=False)
            return
            
        try:
            # Show typing indicator
            self.add_system_message("CROD is thinking...")
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                text = response.json()['response']
                self.add_message(text, is_user=False)
                
                # Feed response back to CROD
                if self.crod_network:
                    self.memory.receive_input("data", {
                        "content": text,
                        "importance": 0.7
                    })
                    
                    # More processing
                    for _ in range(3):
                        self.crod_network.tick()
                        
        except Exception as e:
            self.add_message(f"Error: {str(e)}", is_user=False)
            
    def auto_generate(self):
        """Auto generate conversation"""
        prompts = [
            "What is consciousness?",
            "How do neural networks learn?",
            "Explain quantum computing",
            "What are emergent properties?",
            "How does memory work?",
            "What is the nature of time?",
            "Explain chaos theory",
            "What is artificial general intelligence?"
        ]
        
        import random
        prompt = random.choice(prompts)
        self.input_field.setText(prompt)
        self.send_message()
        
    def update_crod_stats(self):
        """Update CROD statistics display"""
        if self.crod_network:
            stats = self.crod_network.get_stats()
            self.stats_label.setText(
                f"CROD Network: {stats['atoms']} atoms | "
                f"{stats['connections']} connections | "
                f"{stats['total_processed']} messages | "
                f"{stats['tick_count']} ticks"
            )
            
    def closeEvent(self, event):
        """Save on close"""
        if self.crod_network:
            self.db.save_network(self.crod_network.id, self.crod_network.to_dict())
            
        # Save conversation
        with open("crod_data/chat_history.json", "w") as f:
            json.dump(self.conversation_history, f, indent=2)
            
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = CRODChatUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()