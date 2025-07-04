# crod_plugin_system.py - True Plug & Play Architecture
import os
import importlib
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import sqlite3

class CRODPlugin(ABC):
    """Base class for all CROD plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description"""
        pass
    
    @abstractmethod
    def initialize(self, system: 'CRODSystem') -> None:
        """Initialize plugin with system reference"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this plugin provides"""
        pass

class CRODSystem:
    """Main CROD system with plugin architecture"""
    
    def __init__(self, db_path='crod.db'):
        self.db_path = db_path
        self.plugins: Dict[str, CRODPlugin] = {}
        self.capability_map: Dict[str, List[str]] = {}  # capability -> [plugin_names]
        self.db = self._init_database()
        
    def _init_database(self):
        """Initialize core database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Plugin registry table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plugins (
                plugin_name TEXT PRIMARY KEY,
                version TEXT,
                enabled BOOLEAN DEFAULT 1,
                config TEXT,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Event log for plugin communication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                source_plugin TEXT,
                target_plugin TEXT,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        return conn
    
    def register_plugin(self, plugin: CRODPlugin) -> None:
        """Register a plugin with the system"""
        plugin_name = plugin.name
        
        # Initialize plugin
        plugin.initialize(self)
        
        # Store plugin
        self.plugins[plugin_name] = plugin
        
        # Register capabilities
        for capability in plugin.get_capabilities():
            if capability not in self.capability_map:
                self.capability_map[capability] = []
            self.capability_map[capability].append(plugin_name)
        
        # Log to database
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO plugins (plugin_name, version, enabled) VALUES (?, ?, ?)',
            (plugin_name, plugin.version, True)
        )
        self.db.commit()
        
        print(f"✓ Plugin registered: {plugin_name} v{plugin.version}")
    
    def load_plugins_from_directory(self, plugin_dir='plugins'):
        """Auto-load all plugins from directory"""
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)
            return
        
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]
                try:
                    # Import the module
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(plugin_dir, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find CRODPlugin subclasses
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, CRODPlugin) and 
                            attr != CRODPlugin):
                            # Instantiate and register
                            plugin = attr()
                            self.register_plugin(plugin)
                            
                except Exception as e:
                    print(f"✗ Failed to load {filename}: {e}")
    
    def emit_event(self, event_type: str, data: Any, source: str, target: Optional[str] = None):
        """Emit an event that plugins can respond to"""
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO events (event_type, source_plugin, target_plugin, data) VALUES (?, ?, ?, ?)',
            (event_type, source, target, json.dumps(data))
        )
        self.db.commit()
        
        # Notify target plugin(s)
        if target:
            if target in self.plugins:
                self._notify_plugin(self.plugins[target], event_type, data, source)
        else:
            # Broadcast to all plugins
            for plugin in self.plugins.values():
                self._notify_plugin(plugin, event_type, data, source)
    
    def _notify_plugin(self, plugin: CRODPlugin, event_type: str, data: Any, source: str):
        """Notify a plugin about an event"""
        if hasattr(plugin, 'handle_event'):
            try:
                plugin.handle_event(event_type, data, source)
            except Exception as e:
                print(f"✗ Plugin {plugin.name} error handling event: {e}")
    
    def call_capability(self, capability: str, *args, **kwargs) -> Any:
        """Call a capability provided by plugins"""
        if capability not in self.capability_map:
            raise ValueError(f"No plugin provides capability: {capability}")
        
        # Use first available plugin (could be enhanced with priority/selection)
        plugin_name = self.capability_map[capability][0]
        plugin = self.plugins[plugin_name]
        
        if hasattr(plugin, capability):
            return getattr(plugin, capability)(*args, **kwargs)
        else:
            raise AttributeError(f"Plugin {plugin_name} doesn't implement {capability}")
    
    def get_plugin_info(self) -> List[Dict]:
        """Get information about all loaded plugins"""
        info = []
        for name, plugin in self.plugins.items():
            info.append({
                'name': name,
                'version': plugin.version,
                'description': plugin.description,
                'capabilities': plugin.get_capabilities()
            })
        return info

# Example Plugin Implementation
class PatternDetectorPlugin(CRODPlugin):
    """Pattern detection plugin"""
    
    @property
    def name(self):
        return "PatternDetector"
    
    @property
    def version(self):
        return "1.0.0"
    
    @property
    def description(self):
        return "Detects patterns in text using CROD atoms"
    
    def initialize(self, system: CRODSystem):
        self.system = system
        self.patterns = {}  # Would load from DB
    
    def get_capabilities(self):
        return ['detect_patterns', 'add_pattern', 'get_pattern_stats']
    
    def detect_patterns(self, text: str) -> List[Dict]:
        """Detect patterns in text"""
        # Simplified pattern detection
        detected = []
        
        # Check for known patterns
        if "ich halt" in text.lower():
            detected.append({
                'pattern': 'DANIEL_FINGERPRINT',
                'confidence': 0.95,
                'position': text.lower().find("ich halt")
            })
        
        return detected
    
    def handle_event(self, event_type: str, data: Any, source: str):
        """Handle events from other plugins"""
        if event_type == 'text_processed':
            # Auto-detect patterns when text is processed
            patterns = self.detect_patterns(data.get('text', ''))
            if patterns:
                self.system.emit_event(
                    'patterns_detected',
                    {'patterns': patterns, 'text': data.get('text')},
                    self.name
                )

# Example usage module
if __name__ == '__main__':
    # Create system
    system = CRODSystem()
    
    # Register plugins manually
    pattern_plugin = PatternDetectorPlugin()
    system.register_plugin(pattern_plugin)
    
    # Or auto-load from directory
    system.load_plugins_from_directory('plugins')
    
    # Use capabilities
    patterns = system.call_capability('detect_patterns', 'ich halt bruh')
    print(f"Detected patterns: {patterns}")
    
    # Emit events
    system.emit_event('text_processed', {'text': 'ich halt test'}, 'UserInput')
    
    # Check loaded plugins
    print("\nLoaded plugins:")
    for plugin in system.get_plugin_info():
        print(f"- {plugin['name']} v{plugin['version']}: {plugin['description']}")
        print(f"  Capabilities: {', '.join(plugin['capabilities'])}")