"""
BUILD EXE - Script zum Erstellen der .exe Datei
"""

import os
import sys
import subprocess

def build_exe():
    """Build executable using PyInstaller"""
    
    print("🔨 SEED Network EXE Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller gefunden")
    except ImportError:
        print("❌ PyInstaller nicht installiert!")
        print("Installiere mit: pip install pyinstaller")
        return 1
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=SEED_Network",
        "--windowed",  # No console window
        "--onefile",   # Single EXE
        "--icon=NONE", # No icon for now
        "--add-data=atom_types.py;.",
        "--add-data=atom_base.py;.",
        "--add-data=network.py;.",
        "--add-data=main_window.py;.",
        "--add-data=canvas.py;.",
        "--add-data=atom_palette.py;.",
        "--add-data=inspector.py;.",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "seed_network.py"
    ]
    
    print("\n🚀 Starte Build Process...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ Build erfolgreich!")
        print("EXE liegt in: dist/SEED_Network.exe")
        return 0
    else:
        print("\n❌ Build fehlgeschlagen!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(build_exe())