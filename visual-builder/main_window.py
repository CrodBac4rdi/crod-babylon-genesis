"""
MAIN WINDOW - Haupt UI für SEED Network
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from canvas import NetworkCanvas
from atom_palette import AtomPalette
from inspector import Inspector
from network import CRODNetwork
import json

class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung"""
    
    def __init__(self):
        super().__init__()
        self.network = CRODNetwork(name="New CROD Network")
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("SEED Network - CROD Builder v4.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #2d2d2d;
                color: white;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                padding: 5px;
            }
            QToolButton {
                background-color: #404040;
                color: white;
                border: none;
                padding: 5px;
                margin: 2px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            QToolButton:pressed {
                background-color: #606060;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: white;
            }
        """)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel - Atom Palette
        self.atom_palette = AtomPalette()
        self.atom_palette.setMaximumWidth(250)
        main_layout.addWidget(self.atom_palette)
        
        # Center - Canvas
        self.canvas = NetworkCanvas(self.network)
        main_layout.addWidget(self.canvas, 1)
        
        # Right panel - Inspector
        self.inspector = Inspector()
        self.inspector.setMaximumWidth(300)
        main_layout.addWidget(self.inspector)
        
        # Connect signals
        self.canvas.atom_selected.connect(self.inspector.inspect_atom)
        self.canvas.connection_selected.connect(self.inspector.inspect_connection)
        self.inspector.config_changed.connect(self.on_config_changed)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready - Drag atoms from palette to canvas")
        
        # Timer for network updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_network)
        self.timer.start(100)  # 10 Hz
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Network', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_network)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_network)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_network)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_network_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('Export CROD...', self)
        export_action.triggered.connect(self.export_crod)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        delete_action = QAction('Delete', self)
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut('Ctrl++')
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        view_menu.addAction(zoom_out_action)
        
        zoom_fit_action = QAction('Zoom to Fit', self)
        zoom_fit_action.setShortcut('Ctrl+0')
        view_menu.addAction(zoom_fit_action)
        
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = self.addToolBar('Main')
        toolbar.setMovable(False)
        
        # Play/Pause button
        self.play_pause_btn = QToolButton()
        self.play_pause_btn.setText('▶️ Play')
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        toolbar.addWidget(self.play_pause_btn)
        
        # Step button
        step_btn = QToolButton()
        step_btn.setText('⏭️ Step')
        step_btn.clicked.connect(self.step_network)
        toolbar.addWidget(step_btn)
        
        # Reset button
        reset_btn = QToolButton()
        reset_btn.setText('🔄 Reset')
        reset_btn.clicked.connect(self.reset_network)
        toolbar.addWidget(reset_btn)
        
        toolbar.addSeparator()
        
        # Speed control
        toolbar.addWidget(QLabel(' Speed: '))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(60)
        self.speed_slider.setValue(10)
        self.speed_slider.setFixedWidth(100)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        toolbar.addWidget(self.speed_slider)
        
        self.speed_label = QLabel('10 Hz')
        toolbar.addWidget(self.speed_label)
        
    def toggle_play_pause(self):
        """Toggle network execution"""
        if self.network.running:
            self.network.stop()
            self.play_pause_btn.setText('▶️ Play')
        else:
            self.network.start()
            self.play_pause_btn.setText('⏸️ Pause')
            
    def step_network(self):
        """Execute one network step"""
        self.network.tick()
        self.canvas.update()
        self.update_status()
        
    def reset_network(self):
        """Reset network state"""
        for atom in self.network.atoms.values():
            atom.state = {"active": True, "processing": False}
            atom.metrics = {"processed": 0, "errors": 0, "avg_time": 0}
        self.network.tick_count = 0
        self.canvas.update()
        self.update_status()
        
    def on_speed_changed(self, value):
        """Handle speed slider change"""
        self.speed_label.setText(f'{value} Hz')
        self.network.config['tick_rate'] = value
        self.timer.setInterval(int(1000 / value))
        
    def update_network(self):
        """Update network if running"""
        if self.network.running:
            self.network.tick()
            self.canvas.update()
            self.update_status()
            
    def update_status(self):
        """Update status bar"""
        stats = self.network.get_stats()
        status = f"Atoms: {stats['atoms']} | Connections: {stats['connections']} | "
        status += f"Ticks: {stats['tick_count']} | Processed: {stats['total_processed']}"
        if stats['total_errors'] > 0:
            status += f" | Errors: {stats['total_errors']}"
        self.status_bar.showMessage(status)
        
    def on_config_changed(self, atom_id, config):
        """Handle atom config change"""
        self.network.configure_atom(atom_id, config)
        
    def delete_selected(self):
        """Delete selected items"""
        self.canvas.delete_selected()
        
    def new_network(self):
        """Create new network"""
        reply = QMessageBox.question(self, 'New Network', 
                                   'Create new network? Unsaved changes will be lost.',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.network = CRODNetwork(name="New CROD Network")
            self.canvas.set_network(self.network)
            self.update_status()
            
    def open_network(self):
        """Open network file"""
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Network', '', 
                                                'CROD Network (*.crod);;JSON (*.json)')
        if filename:
            try:
                self.network.load_from_file(filename)
                self.canvas.set_network(self.network)
                self.update_status()
                QMessageBox.information(self, 'Success', 'Network loaded successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load network:\n{str(e)}')
                
    def save_network(self):
        """Save network"""
        if hasattr(self, 'current_file'):
            self.network.save_to_file(self.current_file)
        else:
            self.save_network_as()
            
    def save_network_as(self):
        """Save network with new name"""
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Network', '', 
                                                'CROD Network (*.crod);;JSON (*.json)')
        if filename:
            self.current_file = filename
            self.network.save_to_file(filename)
            
    def export_crod(self):
        """Export as standalone CROD"""
        filename, _ = QFileDialog.getSaveFileName(self, 'Export CROD', '', 
                                                'Python File (*.py)')
        if filename:
            # TODO: Implement CROD export
            QMessageBox.information(self, 'Export', 'CROD export coming soon!')
            
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(self, 'Exit', 
                                   'Exit SEED Network? Unsaved changes will be lost.',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()