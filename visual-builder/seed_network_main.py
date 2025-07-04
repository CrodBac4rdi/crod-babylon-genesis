#!/usr/bin/env python3
"""
SEED NETWORK - MAIN ENTRY POINT
Startet das komplette CROD Builder System
"""

import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Hauptfunktion"""
    print("🚀 SEED NETWORK CROD BUILDER v4.0")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return 1
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("SEED Network")
    app.setOrganizationName("CROD Systems")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    print("✅ System gestartet!")
    print("🎯 Baue deine CRODs mit Drag & Drop!")
    
    # Run application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())