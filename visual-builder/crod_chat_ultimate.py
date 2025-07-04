"""
CROD CHAT ULTIMATE - Full Featured Training Data Generator
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
import json
from datetime import datetime
import uuid
from network import CRODNetwork
from database import get_database
import time

class MessageWidget(QFrame):
    """Enhanced message widget with metadata"""
    
    def __init__(self, message_data):
        super().__init__()
        self.message_data = message_data
        self.init_ui()
        
    def init_ui(self):
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        
        # Header with metadata
        header = QHBoxLayout()
        
        # Role icon
        role_icon = "👤" if self.message_data['role'] == 'user' else "🤖"
        role_label = QLabel(role_icon)
        header.addWidget(role_label)
        
        # Role and model
        info_label = QLabel(f"{self.message_data['role']} ({self.message_data.get('model', 'N/A')})")
        info_label.setStyleSheet("color: #CBD5E0; font-size: 12px;")
        header.addWidget(info_label)
        
        header.addStretch()
        
        # Timestamp
        timestamp = QLabel(self.message_data['timestamp'].split('T')[1][:8])
        timestamp.setStyleSheet("color: #718096; font-size: 11px;")
        header.addWidget(timestamp)
        
        layout.addLayout(header)
        
        # Message content
        content = QTextEdit()
        content.setReadOnly(True)
        content.setPlainText(self.message_data['content'])
        content.setMaximumHeight(200)
        
        # Style based on role
        if self.message_data['role'] == 'user':
            self.setStyleSheet("""
                QFrame {
                    background-color: #2C5282;
                    border-radius: 10px;
                    margin: 5px 5px 5px 100px;
                }
                QTextEdit {
                    background-color: transparent;
                    color: white;
                    border: none;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2D3748;
                    border-radius: 10px;
                    margin: 5px 100px 5px 5px;
                }
                QTextEdit {
                    background-color: transparent;
                    color: white;
                    border: none;
                    font-size: 14px;
                }
            """)
            
        layout.addWidget(content)
        
        # CROD metadata if available
        if 'crod_data' in self.message_data:
            crod_info = QLabel(f"CROD: {self.message_data['crod_data']}")
            crod_info.setStyleSheet("color: #9F7AEA; font-size: 11px; padding: 5px;")
            layout.addWidget(crod_info)

class CRODChatUltimate(QMainWindow):
    """Ultimate Chat UI with full training data export"""
    
    def __init__(self):
        super().__init__()
        self.ollama_base_url = "http://localhost:11434"
        self.current_model = "llama2"
        self.available_models = []
        self.crod_network = None
        self.db = get_database()
        
        # Training data
        self.training_session = {
            "session_id": str(uuid.uuid4()),
            "started_at": datetime.now().isoformat(),
            "messages": [],
            "crod_states": [],
            "model_configs": {},
            "statistics": {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "crod_interactions": 0
            }
        }
        
        self.auto_mode = False
        self.export_formats = ['json', 'jsonl', 'csv']
        
        self.init_ui()
        self.init_crod_network()
        self.check_ollama()
        
    def init_ui(self):
        """Initialize UI with all features"""
        self.setWindowTitle("CROD Chat Ultimate - Training Data Generator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Menu bar
        self.create_menu_bar()
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # Left panel - Chat
        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        
        # Toolbar
        toolbar = self.create_toolbar()
        chat_layout.addLayout(toolbar)
        
        # Chat messages area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_widget)
        chat_layout.addWidget(self.chat_scroll)
        
        # Input area
        input_area = self.create_input_area()
        chat_layout.addLayout(input_area)
        
        main_layout.addWidget(chat_panel, 2)
        
        # Right panel - Controls & Stats
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.update_status("Ready")
        
        # Timers
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_generate_message)
        
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_statistics)
        self.stats_timer.start(1000)
        
    def apply_dark_theme(self):
        """Apply comprehensive dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F172A;
            }
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
            }
            QLabel {
                color: #E2E8F0;
            }
            QPushButton {
                background-color: #3730A3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4C1D95;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6B7280;
            }
            QLineEdit, QTextEdit {
                background-color: #1E293B;
                color: white;
                border: 2px solid #334155;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #6366F1;
            }
            QComboBox {
                background-color: #1E293B;
                color: white;
                border: 2px solid #334155;
                padding: 8px;
                border-radius: 6px;
            }
            QCheckBox {
                color: #E2E8F0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #475569;
                background-color: #1E293B;
            }
            QCheckBox::indicator:checked {
                background-color: #6366F1;
                border-color: #6366F1;
            }
            QScrollArea {
                background-color: #0F172A;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1E293B;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748B;
            }
            QGroupBox {
                border: 2px solid #334155;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
                color: #A78BFA;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #1E293B;
                color: white;
                border: 2px solid #334155;
                border-radius: 4px;
                padding: 5px;
            }
            QMenuBar {
                background-color: #1E293B;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #334155;
            }
            QMenu {
                background-color: #1E293B;
                color: white;
                border: 1px solid #334155;
            }
            QMenu::item:selected {
                background-color: #334155;
            }
        """)
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_session = QAction('New Session', self)
        new_session.triggered.connect(self.new_session)
        file_menu.addAction(new_session)
        
        export_action = QAction('Export Training Data...', self)
        export_action.triggered.connect(self.export_training_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction('Settings...', self)
        file_menu.addAction(settings_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        batch_generate = QAction('Batch Generate...', self)
        batch_generate.triggered.connect(self.batch_generate_dialog)
        tools_menu.addAction(batch_generate)
        
        analyze_action = QAction('Analyze Session...', self)
        tools_menu.addAction(analyze_action)
        
    def create_toolbar(self):
        """Create main toolbar"""
        toolbar = QHBoxLayout()
        
        # Model selector
        model_group = QHBoxLayout()
        model_group.addWidget(QLabel("Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(150)
        self.model_combo.currentTextChanged.connect(self.change_model)
        model_group.addWidget(self.model_combo)
        
        self.refresh_models_btn = QPushButton("🔄")
        self.refresh_models_btn.setMaximumWidth(40)
        self.refresh_models_btn.clicked.connect(self.refresh_models)
        model_group.addWidget(self.refresh_models_btn)
        
        toolbar.addLayout(model_group)
        
        toolbar.addSpacing(20)
        
        # Temperature
        temp_group = QHBoxLayout()
        temp_group.addWidget(QLabel("Temperature:"))
        
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(20)
        self.temp_slider.setValue(7)
        self.temp_slider.setMinimumWidth(100)
        self.temp_slider.valueChanged.connect(self.update_temp_label)
        temp_group.addWidget(self.temp_slider)
        
        self.temp_label = QLabel("0.7")
        self.temp_label.setMinimumWidth(30)
        temp_group.addWidget(self.temp_label)
        
        toolbar.addLayout(temp_group)
        
        toolbar.addStretch()
        
        # Connection status
        self.connection_status = QLabel("⚫ Offline")
        self.connection_status.setStyleSheet("font-weight: bold;")
        toolbar.addWidget(self.connection_status)
        
        return toolbar
        
    def create_input_area(self):
        """Create input area with controls"""
        layout = QVBoxLayout()
        
        # Multi-line input
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("Type your message... (Shift+Enter for new line)")
        
        # Shortcut for sending
        send_shortcut = QShortcut(QKeySequence("Return"), self.input_field)
        send_shortcut.activated.connect(self.send_message)
        
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_btn)
        
        button_layout.addStretch()
        
        # Message counter
        self.message_counter = QLabel("Messages: 0")
        button_layout.addWidget(self.message_counter)
        
        layout.addLayout(button_layout)
        
        return layout
        
    def create_right_panel(self):
        """Create right panel with controls and stats"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Auto mode controls
        auto_group = QGroupBox("Automation")
        auto_layout = QVBoxLayout()
        
        self.auto_checkbox = QCheckBox("Enable Auto Mode")
        self.auto_checkbox.stateChanged.connect(self.toggle_auto_mode)
        auto_layout.addWidget(self.auto_checkbox)
        
        # Auto interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Interval (sec):"))
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(60)
        self.interval_spin.setValue(5)
        self.interval_spin.valueChanged.connect(self.update_auto_interval)
        interval_layout.addWidget(self.interval_spin)
        
        auto_layout.addLayout(interval_layout)
        
        # Prompt templates
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "Mixed Questions",
            "Technical Deep Dive",
            "Creative Writing",
            "Code Generation",
            "Philosophy & Ethics",
            "Science & Research"
        ])
        auto_layout.addWidget(QLabel("Template:"))
        auto_layout.addWidget(self.template_combo)
        
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        # CROD Network controls
        crod_group = QGroupBox("CROD Network")
        crod_layout = QVBoxLayout()
        
        self.crod_enabled = QCheckBox("Enable CROD Processing")
        self.crod_enabled.setChecked(True)
        self.crod_enabled.stateChanged.connect(self.toggle_crod)
        crod_layout.addWidget(self.crod_enabled)
        
        # CROD stats
        self.crod_stats = QTextEdit()
        self.crod_stats.setReadOnly(True)
        self.crod_stats.setMaximumHeight(150)
        crod_layout.addWidget(self.crod_stats)
        
        crod_group.setLayout(crod_layout)
        layout.addWidget(crod_group)
        
        # Training data stats
        stats_group = QGroupBox("Training Data Statistics")
        stats_layout = QVBoxLayout()
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(200)
        stats_layout.addWidget(self.stats_display)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Export controls
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout()
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(['JSON', 'JSONL', 'CSV', 'All Formats'])
        export_layout.addWidget(QLabel("Format:"))
        export_layout.addWidget(self.format_combo)
        
        self.export_btn = QPushButton("Export Training Data")
        self.export_btn.clicked.connect(self.export_training_data)
        export_layout.addWidget(self.export_btn)
        
        self.upload_btn = QPushButton("Upload to Server")
        self.upload_btn.clicked.connect(self.upload_to_server)
        export_layout.addWidget(self.upload_btn)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        layout.addStretch()
        
        return panel
        
    def init_crod_network(self):
        """Initialize enhanced CROD network"""
        self.crod_network = CRODNetwork(name="Training-CROD")
        
        # Build comprehensive network
        # Input layer
        self.input_thinker = self.crod_network.add_atom("thinker", (0, 0))
        self.context_analyzer = self.crod_network.add_atom("evaluator", (0, 100))
        
        # Processing layer
        self.pattern_doubter = self.crod_network.add_atom("doubter", (200, 0))
        self.pattern_learner = self.crod_network.add_atom("learner", (200, 100))
        self.concept_connector = self.crod_network.add_atom("connector", (200, 200))
        
        # Memory layer
        self.short_memory = self.crod_network.add_atom("memory", (400, 0))
        self.long_memory = self.crod_network.add_atom("memory", (400, 100))
        self.short_memory.storage = []  # Initialize storage
        self.long_memory.storage = []   # Initialize storage
        
        # Synthesis layer
        self.synthesizer = self.crod_network.add_atom("synthesizer", (600, 50))
        self.quality_evaluator = self.crod_network.add_atom("evaluator", (600, 150))
        
        # Output layer
        self.output_router = self.crod_network.add_atom("router", (800, 100))
        
        # Complex connections
        self.crod_network.connect_atoms(self.input_thinker.id, "thought", self.pattern_doubter.id, "thought")
        self.crod_network.connect_atoms(self.input_thinker.id, "thought", self.pattern_learner.id, "experience")
        self.crod_network.connect_atoms(self.context_analyzer.id, "feedback", self.concept_connector.id, "thought_a")
        
        self.crod_network.connect_atoms(self.pattern_doubter.id, "confidence", self.short_memory.id, "data")
        self.crod_network.connect_atoms(self.pattern_learner.id, "pattern", self.long_memory.id, "data")
        
        self.crod_network.connect_atoms(self.short_memory.id, "retrieved", self.synthesizer.id, "concept_a")
        self.crod_network.connect_atoms(self.long_memory.id, "retrieved", self.synthesizer.id, "concept_b")
        
        self.crod_network.connect_atoms(self.synthesizer.id, "synthesis", self.quality_evaluator.id, "thought")
        self.crod_network.connect_atoms(self.quality_evaluator.id, "score", self.output_router.id, "input")
        
        # Configure for training
        self.input_thinker.configure({"creativity": 0.8, "topics": ["AI", "ML", "consciousness", "patterns", "learning"]})
        self.pattern_learner.configure({"learning_rate": 0.7, "memory_size": 1000})
        self.short_memory.configure({"capacity": 100, "decay_rate": 0.1})
        self.long_memory.configure({"capacity": 1000, "decay_rate": 0.01})
        self.synthesizer.configure({"innovation": 0.6, "coherence": 0.8})
        
    def check_ollama(self):
        """Check Ollama connection and get models"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.connection_status.setText("🟢 Connected")
                self.connection_status.setStyleSheet("color: #10B981; font-weight: bold;")
                
                # Get available models
                models_data = response.json()
                self.available_models = [m['name'] for m in models_data.get('models', [])]
                
                # Update combo box
                self.model_combo.clear()
                self.model_combo.addItems(self.available_models)
                
                if self.current_model in self.available_models:
                    self.model_combo.setCurrentText(self.current_model)
                    
                return True
        except:
            pass
            
        self.connection_status.setText("🔴 Offline")
        self.connection_status.setStyleSheet("color: #EF4444; font-weight: bold;")
        return False
        
    def add_message(self, content, role='user', model=None, crod_data=None):
        """Add message to chat and training data"""
        message_data = {
            "id": str(uuid.uuid4()),
            "content": content,
            "role": role,
            "model": model or self.current_model,
            "timestamp": datetime.now().isoformat(),
            "crod_data": crod_data
        }
        
        # Add to UI
        widget = MessageWidget(message_data)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, widget)
        
        # Add to training data
        self.training_session['messages'].append(message_data)
        
        # Update statistics
        self.training_session['statistics']['total_messages'] += 1
        if role == 'user':
            self.training_session['statistics']['user_messages'] += 1
        else:
            self.training_session['statistics']['assistant_messages'] += 1
            
        # Update counter
        self.message_counter.setText(f"Messages: {len(self.training_session['messages'])}")
        
        # Auto scroll
        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))
        
    def send_message(self):
        """Send user message"""
        content = self.input_field.toPlainText().strip()
        if not content:
            return
            
        # Add user message
        self.add_message(content, role='user')
        self.input_field.clear()
        
        # Process with CROD
        crod_output = None
        if self.crod_enabled.isChecked() and self.crod_network:
            crod_output = self.process_with_crod(content)
            
        # Get Ollama response
        QTimer.singleShot(100, lambda: self.get_ollama_response(content, crod_output))
        
    def process_with_crod(self, content):
        """Process through CROD and return insights"""
        # Feed to network
        self.input_thinker.receive_input("context", {"user_input": content})
        self.context_analyzer.receive_input("thought", {"content": content, "confidence": 0.8})
        
        # Run network cycles
        crod_cycles = []
        for i in range(10):
            self.crod_network.tick()
            
            # Capture state
            state = {
                "cycle": i,
                "processed": self.crod_network.get_stats()['total_processed'],
                "outputs": {}
            }
            
            # Capture key outputs
            for atom_name, atom in [
                ("synthesizer", self.synthesizer),
                ("quality", self.quality_evaluator),
                ("router", self.output_router)
            ]:
                if atom.outputs:
                    state["outputs"][atom_name] = str(atom.outputs)[:100]
                    
            crod_cycles.append(state)
            
        # Save CROD state
        self.training_session['crod_states'].append({
            "message_context": content[:50],
            "cycles": crod_cycles,
            "final_stats": self.crod_network.get_stats()
        })
        
        self.training_session['statistics']['crod_interactions'] += 1
        
        # Return summary
        return f"Processed {len(crod_cycles)} cycles, {self.crod_network.get_stats()['total_processed']} messages"
        
    def get_ollama_response(self, prompt, crod_data=None):
        """Get Ollama response"""
        if not self.check_ollama():
            self.add_message("Error: Ollama is offline", role='assistant')
            return
            
        try:
            # Prepare request
            request_data = {
                "model": self.current_model,
                "prompt": prompt,
                "temperature": self.temp_slider.value() / 10,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['response']
                
                # Add to chat with CROD data
                self.add_message(
                    content,
                    role='assistant',
                    model=self.current_model,
                    crod_data=crod_data
                )
                
                # Process response through CROD
                if self.crod_enabled.isChecked() and self.crod_network:
                    self.long_memory.receive_input("data", {
                        "content": content,
                        "importance": 0.8,
                        "source": "ollama_response"
                    })
                    
                    # More processing
                    for _ in range(5):
                        self.crod_network.tick()
                        
        except Exception as e:
            self.add_message(f"Error: {str(e)}", role='assistant')
            
    def toggle_auto_mode(self, state):
        """Toggle auto mode"""
        self.auto_mode = state == Qt.Checked
        if self.auto_mode:
            interval = self.interval_spin.value() * 1000
            self.auto_timer.start(interval)
            self.update_status("Auto mode enabled")
        else:
            self.auto_timer.stop()
            self.update_status("Auto mode disabled")
            
    def auto_generate_message(self):
        """Auto generate conversation"""
        template = self.template_combo.currentText()
        
        prompts = {
            "Mixed Questions": [
                "What is consciousness?",
                "How do neural networks learn?",
                "Explain quantum computing",
                "What are emergent properties?",
                "How does memory work in the brain?",
                "What is the future of AI?",
                "Explain the concept of entropy",
                "How do complex systems self-organize?"
            ],
            "Technical Deep Dive": [
                "Explain backpropagation in detail",
                "How do transformers work in NLP?",
                "What is gradient descent optimization?",
                "Explain LSTM architecture",
                "How does attention mechanism work?",
                "What is transfer learning?",
                "Explain batch normalization",
                "How do GANs generate images?"
            ],
            "Creative Writing": [
                "Write a story about an AI discovering consciousness",
                "Create a dialogue between two neural networks",
                "Describe a world where AI and humans merge",
                "Write a poem about machine learning",
                "Create a sci-fi scenario about emergent AI",
                "Describe the dreams of an artificial mind",
                "Write about AI ethics in 2050",
                "Create a narrative about digital evolution"
            ],
            "Code Generation": [
                "Write a Python function for matrix multiplication",
                "Create a neural network class from scratch",
                "Implement a genetic algorithm",
                "Write a web scraper in Python",
                "Create a REST API with Flask",
                "Implement quicksort algorithm",
                "Write a recursive fibonacci function",
                "Create a binary search tree"
            ],
            "Philosophy & Ethics": [
                "Is consciousness computable?",
                "What are the ethics of AI decision making?",
                "Can machines have free will?",
                "What is the Chinese Room argument?",
                "Should AI have rights?",
                "What is the hard problem of consciousness?",
                "Can AI be truly creative?",
                "What are the limits of machine intelligence?"
            ],
            "Science & Research": [
                "Explain protein folding",
                "How does CRISPR work?",
                "What is dark matter?",
                "Explain quantum entanglement",
                "How do black holes form?",
                "What is the theory of everything?",
                "Explain photosynthesis at molecular level",
                "How does the immune system work?"
            ]
        }
        
        # Select random prompt from template
        import random
        template_prompts = prompts.get(template, prompts["Mixed Questions"])
        prompt = random.choice(template_prompts)
        
        # Add variation
        if random.random() > 0.5:
            prompt += " Please explain in detail."
        
        # Set in input field and send
        self.input_field.setPlainText(prompt)
        self.send_message()
        
    def update_statistics(self):
        """Update statistics displays"""
        # CROD stats
        if self.crod_network:
            stats = self.crod_network.get_stats()
            crod_text = f"""Network Stats:
Atoms: {stats['atoms']}
Connections: {stats['connections']}
Messages: {stats['total_processed']}
Ticks: {stats['tick_count']}
Errors: {stats['total_errors']}

Memory Usage:
Short: {len(getattr(self.short_memory, 'storage', []))}/{self.short_memory.config.get('capacity', 100)}
Long: {len(getattr(self.long_memory, 'storage', []))}/{self.long_memory.config.get('capacity', 1000)}
"""
            self.crod_stats.setPlainText(crod_text)
            
        # Training stats
        session_stats = self.training_session['statistics']
        stats_text = f"""Session Statistics:
Total Messages: {session_stats['total_messages']}
User Messages: {session_stats['user_messages']}
Assistant Messages: {session_stats['assistant_messages']}
CROD Interactions: {session_stats['crod_interactions']}

Session ID: {self.training_session['session_id'][:8]}...
Started: {self.training_session['started_at'].split('T')[0]}
Duration: {self.get_session_duration()}
"""
        self.stats_display.setPlainText(stats_text)
        
    def get_session_duration(self):
        """Calculate session duration"""
        start = datetime.fromisoformat(self.training_session['started_at'])
        duration = datetime.now() - start
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
    def export_training_data(self):
        """Export training data in multiple formats"""
        # Create export directory
        export_dir = f"training_exports/{self.training_session['session_id']}"
        os.makedirs(export_dir, exist_ok=True)
        
        format_choice = self.format_combo.currentText()
        
        # Prepare data
        export_data = {
            "session": self.training_session,
            "model_config": {
                "model": self.current_model,
                "temperature": self.temp_slider.value() / 10,
                "ollama_url": self.ollama_base_url
            },
            "crod_config": self.crod_network.to_dict() if self.crod_network else None,
            "exported_at": datetime.now().isoformat()
        }
        
        # Export formats
        if format_choice in ["JSON", "All Formats"]:
            # Full JSON export
            json_file = os.path.join(export_dir, "training_data.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"Exported JSON: {json_file}")
            
        if format_choice in ["JSONL", "All Formats"]:
            # JSONL format (one message per line)
            jsonl_file = os.path.join(export_dir, "messages.jsonl")
            with open(jsonl_file, 'w', encoding='utf-8') as f:
                for msg in self.training_session['messages']:
                    f.write(json.dumps(msg, ensure_ascii=False) + '\n')
            print(f"Exported JSONL: {jsonl_file}")
            
        if format_choice in ["CSV", "All Formats"]:
            # CSV format
            import csv
            csv_file = os.path.join(export_dir, "conversation.csv")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'role', 'content', 'model', 'crod_data'])
                for msg in self.training_session['messages']:
                    writer.writerow([
                        msg['timestamp'],
                        msg['role'],
                        msg['content'],
                        msg.get('model', ''),
                        msg.get('crod_data', '')
                    ])
            print(f"Exported CSV: {csv_file}")
            
        # Show success message
        QMessageBox.information(self, "Export Complete",
            f"Training data exported to:\n{export_dir}")
            
        self.update_status(f"Exported to {export_dir}")
        
    def upload_to_server(self):
        """Upload training data to server"""
        # First export to ensure latest data
        self.export_training_data()
        
        # Get server URL from user
        server_url, ok = QInputDialog.getText(
            self, "Upload to Server",
            "Enter server URL:",
            text="http://localhost:8000/upload"
        )
        
        if ok and server_url:
            try:
                # Prepare upload data
                upload_data = {
                    "session_id": self.training_session['session_id'],
                    "messages": self.training_session['messages'],
                    "statistics": self.training_session['statistics'],
                    "model": self.current_model,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Send to server
                response = requests.post(
                    server_url,
                    json=upload_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    QMessageBox.information(self, "Success",
                        "Training data uploaded successfully!")
                    self.update_status("Upload successful")
                else:
                    QMessageBox.warning(self, "Upload Failed",
                        f"Server returned: {response.status_code}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error",
                    f"Upload failed: {str(e)}")
                    
    def batch_generate_dialog(self):
        """Show batch generation dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Batch Generate Training Data")
        dialog.setModal(True)
        layout = QVBoxLayout(dialog)
        
        # Number of exchanges
        layout.addWidget(QLabel("Number of exchanges:"))
        num_spin = QSpinBox()
        num_spin.setMinimum(1)
        num_spin.setMaximum(100)
        num_spin.setValue(10)
        layout.addWidget(num_spin)
        
        # Delay between
        layout.addWidget(QLabel("Delay between (seconds):"))
        delay_spin = QSpinBox()
        delay_spin.setMinimum(1)
        delay_spin.setMaximum(30)
        delay_spin.setValue(3)
        layout.addWidget(delay_spin)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Start batch generation
            self.batch_generate(num_spin.value(), delay_spin.value())
            
    def batch_generate(self, num_exchanges, delay):
        """Batch generate training data"""
        self.update_status(f"Batch generating {num_exchanges} exchanges...")
        
        # Temporarily set auto mode
        self.auto_checkbox.setChecked(True)
        self.interval_spin.setValue(delay)
        
        # Stop after specified exchanges
        def stop_batch():
            if len(self.training_session['messages']) >= num_exchanges * 2:
                self.auto_checkbox.setChecked(False)
                self.update_status("Batch generation complete")
                
        # Connect to statistics update
        self.stats_timer.timeout.connect(stop_batch)
        
    def clear_chat(self):
        """Clear chat history"""
        reply = QMessageBox.question(
            self, "Clear Chat",
            "This will start a new session. Export current data first?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            self.export_training_data()
            
        self.new_session()
        
    def new_session(self):
        """Start new training session"""
        # Clear UI
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Reset training data
        self.training_session = {
            "session_id": str(uuid.uuid4()),
            "started_at": datetime.now().isoformat(),
            "messages": [],
            "crod_states": [],
            "model_configs": {},
            "statistics": {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "crod_interactions": 0
            }
        }
        
        # Reset CROD
        if self.crod_network:
            self.init_crod_network()
            
        self.update_status("New session started")
        
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.showMessage(message)
        
    def update_temp_label(self, value):
        """Update temperature label"""
        self.temp_label.setText(f"{value/10:.1f}")
        
    def update_auto_interval(self, value):
        """Update auto timer interval"""
        if self.auto_mode:
            self.auto_timer.setInterval(value * 1000)
            
    def change_model(self, model):
        """Change current model"""
        self.current_model = model
        self.training_session['model_configs'][model] = {
            "selected_at": datetime.now().isoformat(),
            "temperature": self.temp_slider.value() / 10
        }
        
    def refresh_models(self):
        """Refresh available models"""
        self.check_ollama()
        
    def toggle_crod(self, state):
        """Toggle CROD network"""
        if state == Qt.Checked and not self.crod_network:
            self.init_crod_network()
            
    def closeEvent(self, event):
        """Handle close event"""
        reply = QMessageBox.question(
            self, "Exit",
            "Export training data before closing?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            event.ignore()
        else:
            if reply == QMessageBox.Yes:
                self.export_training_data()
                
            # Save final state
            if self.crod_network:
                self.db.save_network(self.crod_network.id, self.crod_network.to_dict())
                
            event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    window = CRODChatUltimate()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()