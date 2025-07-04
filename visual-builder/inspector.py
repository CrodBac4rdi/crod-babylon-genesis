"""
INSPECTOR - Inspector Panel für Atoms und Connections
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json

class ConfigEditor(QWidget):
    """Widget for editing configuration values"""
    
    config_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.config = {}
        self.editors = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.layout = QFormLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
    def set_config(self, config: dict):
        """Set configuration to edit"""
        self.config = config.copy()
        self.clear_editors()
        
        for key, value in self.config.items():
            self.add_editor(key, value)
            
    def clear_editors(self):
        """Clear all editors"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.editors.clear()
        
    def add_editor(self, key: str, value):
        """Add editor for a config value"""
        label = QLabel(key.replace('_', ' ').title() + ":")
        label.setStyleSheet("color: white;")
        
        if isinstance(value, bool):
            editor = QCheckBox()
            editor.setChecked(value)
            editor.stateChanged.connect(lambda: self.on_value_changed(key))
            
        elif isinstance(value, (int, float)):
            editor = QDoubleSpinBox() if isinstance(value, float) else QSpinBox()
            editor.setMinimum(-9999)
            editor.setMaximum(9999)
            editor.setValue(value)
            editor.setStyleSheet("""
                QSpinBox, QDoubleSpinBox {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #505050;
                    border-radius: 3px;
                    padding: 2px;
                }
            """)
            editor.valueChanged.connect(lambda: self.on_value_changed(key))
            
        elif isinstance(value, str):
            editor = QLineEdit()
            editor.setText(value)
            editor.setStyleSheet("""
                QLineEdit {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #505050;
                    border-radius: 3px;
                    padding: 2px;
                }
            """)
            editor.textChanged.connect(lambda: self.on_value_changed(key))
            
        elif isinstance(value, list):
            editor = QTextEdit()
            editor.setPlainText(json.dumps(value, indent=2))
            editor.setMaximumHeight(60)
            editor.setStyleSheet("""
                QTextEdit {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #505050;
                    border-radius: 3px;
                    padding: 2px;
                }
            """)
            editor.textChanged.connect(lambda: self.on_value_changed(key))
            
        elif isinstance(value, dict):
            editor = QTextEdit()
            editor.setPlainText(json.dumps(value, indent=2))
            editor.setMaximumHeight(80)
            editor.setStyleSheet("""
                QTextEdit {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #505050;
                    border-radius: 3px;
                    padding: 2px;
                }
            """)
            editor.textChanged.connect(lambda: self.on_value_changed(key))
            
        else:
            editor = QLabel(str(value))
            editor.setStyleSheet("color: #888;")
            
        self.editors[key] = editor
        self.layout.addRow(label, editor)
        
    def on_value_changed(self, key):
        """Handle value change"""
        editor = self.editors[key]
        
        if isinstance(editor, QCheckBox):
            self.config[key] = editor.isChecked()
        elif isinstance(editor, (QSpinBox, QDoubleSpinBox)):
            self.config[key] = editor.value()
        elif isinstance(editor, QLineEdit):
            self.config[key] = editor.text()
        elif isinstance(editor, QTextEdit):
            try:
                self.config[key] = json.loads(editor.toPlainText())
            except:
                pass  # Invalid JSON
                
        self.config_changed.emit(self.config)

class Inspector(QWidget):
    """Inspector panel for atoms and connections"""
    
    config_changed = pyqtSignal(str, dict)  # atom_id, new_config
    
    def __init__(self):
        super().__init__()
        self.current_atom = None
        self.current_connection = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        self.title = QLabel("Inspector")
        self.title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(self.title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget {
                background-color: #2d2d2d;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #404040;
                color: white;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #505050;
            }
        """)
        
        # Properties tab
        self.properties_widget = QWidget()
        self.properties_layout = QVBoxLayout(self.properties_widget)
        
        self.info_label = QLabel("Select an atom or connection")
        self.info_label.setStyleSheet("color: #888; padding: 10px;")
        self.properties_layout.addWidget(self.info_label)
        
        self.properties_layout.addStretch()
        
        self.tabs.addTab(self.properties_widget, "Properties")
        
        # Config tab
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        
        self.config_editor = ConfigEditor()
        self.config_editor.config_changed.connect(self.on_config_changed)
        self.config_layout.addWidget(self.config_editor)
        
        self.tabs.addTab(self.config_widget, "Configuration")
        
        # Metrics tab
        self.metrics_widget = QWidget()
        self.metrics_layout = QVBoxLayout(self.metrics_widget)
        
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        self.metrics_text.setStyleSheet("""
            QTextEdit {
                background-color: #404040;
                color: white;
                border: none;
                font-family: monospace;
            }
        """)
        self.metrics_layout.addWidget(self.metrics_text)
        
        self.tabs.addTab(self.metrics_widget, "Metrics")
        
        layout.addWidget(self.tabs)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
            }
        """)
        
    def inspect_atom(self, atom):
        """Inspect an atom"""
        self.current_atom = atom
        self.current_connection = None
        
        # Update title
        self.title.setText(f"Atom: {atom.type}")
        
        # Clear properties
        while self.properties_layout.count() > 0:
            child = self.properties_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Add atom info
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMaximumHeight(200)
        info.setStyleSheet("""
            QTextEdit {
                background-color: #404040;
                color: white;
                border: none;
                font-family: monospace;
            }
        """)
        
        info_text = f"ID: {atom.id}\n"
        info_text += f"Type: {atom.type}\n"
        info_text += f"Position: ({atom.position['x']}, {atom.position['y']})\n"
        info_text += f"\nInput Ports:\n"
        for port in atom.get_input_ports():
            info_text += f"  • {port}\n"
        info_text += f"\nOutput Ports:\n"
        for port in atom.get_output_ports():
            info_text += f"  • {port}\n"
            
        info.setPlainText(info_text)
        self.properties_layout.addWidget(info)
        self.properties_layout.addStretch()
        
        # Update config
        self.config_editor.set_config(atom.config)
        
        # Update metrics
        self.update_metrics()
        
    def inspect_connection(self, connection):
        """Inspect a connection"""
        self.current_atom = None
        self.current_connection = connection
        
        # Update title
        self.title.setText(f"Connection")
        
        # Clear properties
        while self.properties_layout.count() > 0:
            child = self.properties_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Add connection info
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMaximumHeight(150)
        info.setStyleSheet("""
            QTextEdit {
                background-color: #404040;
                color: white;
                border: none;
                font-family: monospace;
            }
        """)
        
        info_text = f"ID: {connection.id}\n"
        info_text += f"From: {connection.from_atom}.{connection.from_port}\n"
        info_text += f"To: {connection.to_atom}.{connection.to_port}\n"
        info_text += f"Type: {connection.type}\n"
        info_text += f"Strength: {connection.strength}"
        
        info.setPlainText(info_text)
        self.properties_layout.addWidget(info)
        self.properties_layout.addStretch()
        
        # Clear config
        self.config_editor.clear_editors()
        
        # Clear metrics
        self.metrics_text.clear()
        
    def update_metrics(self):
        """Update metrics display"""
        if self.current_atom:
            metrics = self.current_atom.metrics
            
            text = "Performance Metrics:\n"
            text += "=" * 30 + "\n\n"
            text += f"Messages Processed: {metrics['processed']}\n"
            text += f"Errors: {metrics['errors']}\n"
            text += f"Avg Processing Time: {metrics['avg_time']:.3f}s\n"
            
            if metrics['processed'] > 0:
                error_rate = metrics['errors'] / metrics['processed'] * 100
                text += f"Error Rate: {error_rate:.1f}%\n"
                
            self.metrics_text.setPlainText(text)
            
    def on_config_changed(self, new_config):
        """Handle config change"""
        if self.current_atom:
            self.config_changed.emit(self.current_atom.id, new_config)