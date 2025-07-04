#!/usr/bin/env python3
"""
CROD Standalone - Complete System
Main entry point for the full CROD experience
"""

import sys
import os
from pathlib import Path

# Add our modules to path
sys.path.insert(0, str(Path(__file__).parent))

from crod_gui import CRODMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont

def setup_dark_theme(app):
    """Setup cyberpunk dark theme"""
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(15, 15, 15))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 255, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 255, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 255, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 150, 255))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    
    app.setPalette(palette)
    
    # Set font
    font = QFont("Consolas", 10)
    app.setFont(font)

def main():
    print("🚀 CROD Standalone - Initializing...")
    print("===================================")
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("CROD Standalone")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CROD Labs")
    
    # Setup theme
    setup_dark_theme(app)
    
    # Create main window
    window = CRODMainWindow()
    window.show()
    
    print("✅ CROD GUI launched!")
    print("💡 Ready for 'ich bins wieder' activation!")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()