# crod_viz_plugin_bridge.py - Bridge between Deep Viz and Plugin System
from flask import Flask, jsonify, request
from flask_cors import CORS
from crod_plugin_system import CRODSystem
import webbrowser
import threading

app = Flask(__name__)
CORS(app)

# Initialize plugin system
print("Initializing CROD Plugin System...")
system = CRODSystem()
system.load_plugins_from_directory('plugins')
print(f"Loaded {len(system.plugins)} plugins")

@app.route('/')
def index():
    """Serve the visualization HTML"""
    with open('crod_deep_viz_ui.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/plugins')
def get_plugins():
    """Get loaded plugins info"""
    return jsonify(system.get_plugin_info())

@app.route('/api/capabilities')
def get_capabilities():
    """Get all available capabilities"""
    return jsonify({
        'capabilities': list(system.capability_map.keys()),
        'mapping': system.capability_map
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze text using plugins"""
    data = request.json
    text = data.get('text', '')
    
    # Use Engine plugin for full processing
    if 'process_text' in system.capability_map:
        try:
            result = system.call_capability('process_text', text)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Fallback to individual capabilities
    results = {}
    
    # Pattern detection
    if 'detect_patterns' in system.capability_map:
        try:
            results['patterns'] = system.call_capability('detect_patterns', text)
        except Exception as e:
            results['patterns_error'] = str(e)
    
    # ML analysis
    if 'visualize_gradients' in system.capability_map:
        try:
            results['ml_analysis'] = system.call_capability('visualize_gradients')
        except Exception as e:
            results['ml_error'] = str(e)
    
    # Text analysis
    if 'analyze_text' in system.capability_map:
        try:
            results['text_analysis'] = system.call_capability('analyze_text', text)
        except Exception as e:
            results['text_error'] = str(e)
    
    return jsonify(results)

@app.route('/api/gradients')
def get_gradients():
    """Get ML gradients"""
    try:
        layer_count = request.args.get('layers', 10, type=int)
        gradients = system.call_capability('calculate_gradients', layer_count)
        return jsonify({'gradients': gradients})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get all statistics"""
    stats = {}
    
    # Get engine stats
    if 'get_session_stats' in system.capability_map:
        try:
            stats = system.call_capability('get_session_stats')
        except:
            pass
    
    # Fallback to storage stats
    if not stats and 'get_stats' in system.capability_map:
        try:
            stats = system.call_capability('get_stats')
        except:
            pass
    
    return jsonify(stats)

@app.route('/api/events', methods=['POST'])
def emit_event():
    """Emit event to plugin system"""
    data = request.json
    system.emit_event(
        data.get('event_type'),
        data.get('data', {}),
        data.get('source', 'WebUI'),
        data.get('target')
    )
    return jsonify({'status': 'event_emitted'})

def open_browser():
    """Open browser after server starts"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("\n🚀 CROD Modular System starting...")
    print("📦 Plugins loaded:")
    for plugin in system.get_plugin_info():
        print(f"   - {plugin['name']} v{plugin['version']}")
    print("\n📊 Open http://localhost:5000 in your browser\n")
    
    # Open browser
    timer = threading.Timer(1, open_browser)
    timer.start()
    
    # Run server
    app.run(debug=True, port=5000)