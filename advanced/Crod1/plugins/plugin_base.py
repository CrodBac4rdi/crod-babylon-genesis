# plugins/plugin_base.py - Import helper for plugins
import sys
import os

# Add parent directory to path so plugins can import from main directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now import and re-export CRODPlugin
from crod_plugin_system import CRODPlugin

# Re-export for easy import
__all__ = ['CRODPlugin']