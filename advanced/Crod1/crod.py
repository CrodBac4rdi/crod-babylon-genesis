#!/usr/bin/env python3
"""
CROD v3.0 - Main Entry Point
With Gradient Engine Integration
"""

import os
from crod_plugin_system import CRODSystem
import json

def main():
    """Main CROD entry point"""
    print("=" * 60)
    print("CROD v3.0 - Mental System by Daniel D. Birkner")
    print("=" * 60)
    
    # Create system
    system = CRODSystem(db_path='crod.db')
    
    # Load all plugins from plugins directory
    print("\nLoading plugins...")
    system.load_plugins_from_directory('plugins')
    
    # Debug: Show capability map
    print(f"\nAvailable capabilities: {list(system.capability_map.keys())}")
    
    # Show loaded plugins
    print("\nLoaded plugins:")
    plugin_count = 0
    for plugin_info in system.get_plugin_info():
        plugin_count += 1
        print(f"✓ {plugin_info['name']} v{plugin_info['version']}")
        print(f"  {plugin_info['description']}")
        print(f"  Capabilities: {', '.join(plugin_info['capabilities'])}")
        print()
    
    if plugin_count == 0:
        print("⚠️  NO PLUGINS LOADED! Check your plugins directory!")
        print(f"   Looking in: {os.path.abspath('plugins')}")
    
    # Interactive mode
    print("\nCROD Ready! Type 'help' for commands, 'exit' to quit")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nDaniel: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("Saving state...")
                # Save gradient state if available
                if 'get_gradient_state' in system.capability_map:
                    state = system.call_capability('get_gradient_state')
                    with open('gradient_state.json', 'w') as f:
                        json.dump(state, f, indent=2)
                print("Goodbye!")
                break
                
            elif user_input.lower() == 'help':
                print_help()
                
            elif user_input.lower() == 'stats':
                show_stats(system)
                
            elif user_input.lower() == 'gradients':
                show_gradients(system)
                
            elif user_input.lower() == 'patterns':
                show_patterns(system)
                
            else:
                # Process through full pipeline
                process_input(system, user_input)
                
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")

def process_input(system: CRODSystem, text: str):
    """Process user input through all plugins"""
    
    print(f"\n🔍 Processing: '{text}'")
    print(f"   Available capabilities: {len(system.capability_map)}")
    
    # 1. Process through gradient engine
    if 'process_message_gradients' in system.capability_map:
        try:
            gradient_result = system.call_capability('process_message_gradients', text)
            print(f"\n📊 Gradient Analysis:")
            print(f"   Total Gradient: {gradient_result['total_gradient']:.3f}")
            print(f"   Words: {len(gradient_result['words'])}")
            
            # Show permission level
            state = system.call_capability('get_gradient_state')
            print(f"   Permission Level: {state['current_permission']}")
            print(f"   Context: {state['context']}")
        except Exception as e:
            print(f"   Gradient error: {e}")
    
    # 2. Detect patterns
    patterns = []  # Initialize patterns variable
    if 'detect_patterns' in system.capability_map:
        try:
            patterns = system.call_capability('detect_patterns', text)
            if patterns:
                print(f"\n🎯 Patterns Detected:")
                for p in patterns:
                    print(f"   - {p.get('pattern_name', p.get('pattern_id'))} "
                          f"(confidence: {p.get('confidence', 'N/A')})")
        except Exception as e:
            print(f"   Pattern error: {e}")
    
    # 3. Chat response
    if 'process_message' in system.capability_map:
        try:
            chat_analysis = system.call_capability('process_message', text)
            print(f"\n💬 Chat Analysis:")
            print(f"   Mood: {chat_analysis['mood']['mood']} "
                  f"({chat_analysis['mood']['confidence']:.1%} confidence)")
            print(f"   Language: {chat_analysis['language']['primary']}")
            if chat_analysis['keywords']:
                print(f"   Keywords: {', '.join(chat_analysis['keywords'])}")
        except Exception as e:
            print(f"   Chat error: {e}")
    
    # 4. ML Analysis (if patterns found)
    if patterns and 'visualize_gradients' in system.capability_map:
        try:
            ml_viz = system.call_capability('visualize_gradients')
            if ml_viz.get('recommendations'):
                print(f"\n🤖 ML Recommendations:")
                for rec in ml_viz['recommendations']:
                    print(f"   - {rec['issue']}: {rec['solution']}")
        except:
            pass

def show_stats(system: CRODSystem):
    """Show system statistics"""
    print("\n📈 System Statistics:")
    
    # Database stats
    if 'get_stats' in system.capability_map:
        try:
            db_stats = system.call_capability('get_stats')
            print(f"\n   Database:")
            print(f"   - Atoms: {db_stats['total_atoms']}")
            print(f"   - Patterns: {db_stats['total_patterns']}")
            print(f"   - Routes: {db_stats['total_routes']}")
            print(f"   - Success Rate: {db_stats['average_success_rate']:.1%}")
        except:
            pass
    
    # Gradient stats
    if 'analyze_gradient_flow' in system.capability_map:
        try:
            gradient_flow = system.call_capability('analyze_gradient_flow')
            print(f"\n   Gradients:")
            print(f"   - Messages: {gradient_flow['total_messages']}")
            print(f"   - Average: {gradient_flow['average_gradient']:.3f}")
            print(f"   - Trend: {gradient_flow['trend']}")
        except:
            pass
    
    # Chat stats
    if 'analyze_session' in system.capability_map:
        try:
            chat_stats = system.call_capability('analyze_session')
            print(f"\n   Chat Session:")
            print(f"   - Messages: {chat_stats['total_messages']}")
            print(f"   - Duration: {chat_stats['session_duration']}")
        except:
            pass

def show_gradients(system: CRODSystem):
    """Show gradient information"""
    if 'get_gradient_state' not in system.capability_map:
        print("Gradient plugin not loaded!")
        return
    
    state = system.call_capability('get_gradient_state')
    print("\n🔥 Gradient State:")
    print(f"   Permission: {state['current_permission']}")
    print(f"   Context: {state['context']}")
    print(f"   Discovered Words: {state['discovered_patterns']}")
    
    print("\n   Top Word Gradients:")
    sorted_words = sorted(state['word_gradients'].items(), 
                         key=lambda x: x[1], reverse=True)[:10]
    for word, gradient in sorted_words:
        print(f"   - {word}: {gradient:.3f}")

def show_patterns(system: CRODSystem):
    """Show pattern information"""
    if 'get_all_patterns' not in system.capability_map:
        print("Storage plugin not loaded!")
        return
    
    patterns = system.call_capability('get_all_patterns')
    print(f"\n🎯 Patterns ({len(patterns)} total):")
    
    # Show top patterns by usage
    top_patterns = sorted(patterns, key=lambda x: x['usage_count'], reverse=True)[:10]
    for p in top_patterns:
        print(f"   - {p['id']}: {p['name']}")
        print(f"     Usage: {p['usage_count']} | Success: {p['success_rate']:.1%}")

def print_help():
    """Print help information"""
    print("\n📚 CROD Commands:")
    print("   help      - Show this help")
    print("   stats     - Show system statistics")
    print("   gradients - Show gradient information")
    print("   patterns  - Show pattern information")
    print("   exit      - Save and exit")
    print("\n   Or just type any text to process it!")
    print("\n   Special phrases:")
    print("   'ich bins wieder' - Restore previous session")
    print("   'speicher das'    - Save current state")
    print("   '???'             - Increase urgency")

if __name__ == '__main__':
    # Startup message
    print("\nInitializing CROD Mental System...")
    
    # Check for gradient state file
    try:
        with open('gradient_state.json', 'r') as f:
            print("Found previous gradient state!")
            # Could restore here if needed
    except:
        print("Starting fresh session...")
    
    # Run main
    main()