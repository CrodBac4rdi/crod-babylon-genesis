# debug_plugins.py - Debug why plugins don't load
import os
import importlib.util
from plugin_base import CRODPlugin

def debug_plugin_loading():
    plugin_dir = 'plugins'
    print(f"Checking plugins directory: {plugin_dir}\n")
    
    # List all files
    files = os.listdir(plugin_dir)
    print(f"Files found: {files}\n")
    
    for filename in files:
        if filename.endswith('.py') and not filename.startswith('_'):
            print(f"\n{'='*50}")
            print(f"Checking: {filename}")
            print('='*50)
            
            filepath = os.path.join(plugin_dir, filename)
            module_name = filename[:-3]
            
            try:
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✓ Module loaded successfully")
                
                # Find CRODPlugin subclasses
                found_plugins = []
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, CRODPlugin) and 
                        attr != CRODPlugin):
                        found_plugins.append(attr_name)
                        
                        # Try to instantiate
                        try:
                            plugin = attr()
                            print(f"✓ Plugin instantiated: {plugin.name}")
                            print(f"  Version: {plugin.version}")
                            print(f"  Description: {plugin.description}")
                            
                            # Check methods
                            methods = ['initialize', 'get_capabilities']
                            for method in methods:
                                if hasattr(plugin, method):
                                    print(f"  ✓ Has {method} method")
                                else:
                                    print(f"  ✗ Missing {method} method")
                                    
                        except Exception as e:
                            print(f"✗ Failed to instantiate {attr_name}: {e}")
                
                if not found_plugins:
                    print("✗ No CRODPlugin subclasses found in module")
                    print(f"  Found classes: {[attr for attr in dir(module) if isinstance(getattr(module, attr), type)]}")
                    
            except Exception as e:
                print(f"✗ Failed to load module: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    debug_plugin_loading()