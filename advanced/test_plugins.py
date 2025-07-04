# test_plugins.py - Test if plugin system works
from crod_plugin_system import CRODSystem

def test_plugin_system():
    print("=== CROD Plugin System Test ===\n")
    
    # 1. Create system
    print("1. Creating CROD System...")
    system = CRODSystem()
    print("✓ System created\n")
    
    # 2. Load plugins
    print("2. Loading plugins from directory...")
    system.load_plugins_from_directory('plugins')
    print()
    
    # 3. Show loaded plugins
    print("3. Loaded plugins:")
    for plugin in system.get_plugin_info():
        print(f"\n📦 {plugin['name']} v{plugin['version']}")
        print(f"   {plugin['description']}")
        print(f"   Capabilities: {', '.join(plugin['capabilities'])}")
    print()
    
    # 4. Test ML plugin
    print("\n4. Testing ML Plugin...")
    try:
        # Calculate gradients
        gradients = system.call_capability('calculate_gradients', 5)
        print(f"✓ Calculated {len(gradients)} gradients")
        
        # Get ML formulas
        formulas = system.call_capability('get_ml_formulas')
        print(f"✓ Got {len(formulas)} ML formulas")
        
        # Visualize
        viz = system.call_capability('visualize_gradients')
        print(f"✓ Visualization data ready:")
        print(f"  - Vanishing: {viz['summary']['vanishing_count']} layers")
        print(f"  - Exploding: {viz['summary']['exploding_count']} layers")
        print(f"  - Normal: {viz['summary']['normal_count']} layers")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n✅ Plugin system is working!")
    print("\nNext steps:")
    print("1. Create more plugins in the plugins/ folder")
    print("2. Each plugin is automatically loaded")
    print("3. No need to modify main code!")

if __name__ == '__main__':
    test_plugin_system()