"""
ATOM PALETTE - Drag & Drop Palette für Atom Types
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AtomTypeWidget(QLabel):
    """Widget for a draggable atom type"""
    
    ATOM_INFO = {
        "thinker": {
            "color": "#FF6B6B",
            "icon": "🧠",
            "description": "Generiert neue Gedanken"
        },
        "doubter": {
            "color": "#4ECDC4",
            "icon": "🤔",
            "description": "Hinterfragt Gedanken"
        },
        "learner": {
            "color": "#45B7D1",
            "icon": "📚",
            "description": "Extrahiert Patterns"
        },
        "connector": {
            "color": "#96CEB4",
            "icon": "🔗",
            "description": "Verbindet Gedanken"
        },
        "evaluator": {
            "color": "#FFEAA7",
            "icon": "⚖️",
            "description": "Bewertet Qualität"
        },
        "memory": {
            "color": "#DDA0DD",
            "icon": "💾",
            "description": "Speichert Informationen"
        },
        "synthesizer": {
            "color": "#98D8C8",
            "icon": "⚗️",
            "description": "Kombiniert zu Neuem"
        },
        "router": {
            "color": "#F7DC6F",
            "icon": "🚦",
            "description": "Leitet Gedanken weiter"
        }
    }
    
    def __init__(self, atom_type: str):
        super().__init__()
        self.atom_type = atom_type
        info = self.ATOM_INFO.get(atom_type, {})
        
        # Setup widget
        self.setFixedHeight(60)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {info.get('color', '#888')};
                border-radius: 5px;
                padding: 5px;
                color: white;
                font-weight: bold;
            }}
            QLabel:hover {{
                background-color: {QColor(info.get('color', '#888')).lighter(120).name()};
                cursor: move;
            }}
        """)
        
        # Set text with icon
        icon = info.get('icon', '📦')
        self.setText(f"{icon} {atom_type}")
        self.setAlignment(Qt.AlignCenter)
        
        # Tooltip
        self.setToolTip(info.get('description', ''))
        
    def mousePressEvent(self, event):
        """Start drag operation"""
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.atom_type)
            drag.setMimeData(mime_data)
            
            # Create pixmap for drag
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            
            drag.exec_(Qt.CopyAction)

class AtomPalette(QWidget):
    """Palette containing all atom types"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("Atom Types")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search atoms...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.search_box.textChanged.connect(self.filter_atoms)
        layout.addWidget(self.search_box)
        
        # Scroll area for atoms
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #505050;
            }
        """)
        
        # Container for atom widgets
        self.atom_container = QWidget()
        self.atom_layout = QVBoxLayout(self.atom_container)
        self.atom_layout.setSpacing(5)
        
        # Add atom types
        self.atom_widgets = {}
        atom_types = ["thinker", "doubter", "learner", "connector", 
                     "evaluator", "memory", "synthesizer", "router"]
        
        for atom_type in atom_types:
            widget = AtomTypeWidget(atom_type)
            self.atom_layout.addWidget(widget)
            self.atom_widgets[atom_type] = widget
            
        self.atom_layout.addStretch()
        
        scroll.setWidget(self.atom_container)
        layout.addWidget(scroll)
        
        # Info section
        self.info_label = QLabel("Drag atoms to canvas")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.info_label)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
            }
        """)
        
    def filter_atoms(self, text):
        """Filter atoms based on search text"""
        search_text = text.lower()
        
        for atom_type, widget in self.atom_widgets.items():
            if search_text in atom_type.lower():
                widget.show()
            else:
                widget.hide()