# crod_web_ui.py - Local Web Interface
import webbrowser
import threading
import json
import os
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from crod_engine import CRODEngine

app = Flask(__name__)
CORS(app)

# Global engine instance
engine = CRODEngine()

# Player stats
player_stats = {
    'level': 1,
    'exp': 0,
    'exp_to_next': 100,
    'title': 'Novice Pattern Seeker',
    'str': 10,
    'agi': 10,
    'int': 10,
    'patterns_found': 0,
    'messages': 0
}

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'crod_ui.html')

@app.route('/api/process', methods=['POST'])
def process_text():
    """Process text through CROD engine"""
    global player_stats
    
    data = request.json
    text = data.get('text', '')
    
    # Process with engine
    result = engine.process(text)
    
    # Update player stats
    player_stats['messages'] += 1
    player_stats['exp'] += 10
    
    if result.get('patterns'):
        player_stats['patterns_found'] += len(result['patterns'])
    
    # Check level up
    if player_stats['exp'] >= player_stats['exp_to_next']:
        player_stats['level'] += 1
        player_stats['exp'] = 0
        player_stats['exp_to_next'] = 100 * player_stats['level']
        player_stats['str'] += 2
        player_stats['agi'] += 2
        player_stats['int'] += 2
        
        # Update title
        if player_stats['level'] >= 10:
            player_stats['title'] = "CROD Master"
        elif player_stats['level'] >= 5:
            player_stats['title'] = "Pattern Hunter"
        else:
            player_stats['title'] = "Apprentice Debugger"
    
    return jsonify({
        'result': result,
        'player_stats': player_stats
    })

@app.route('/api/stats')
def get_stats():
    """Get current stats"""
    engine_stats = engine.get_stats()
    return jsonify({
        'engine': engine_stats,
        'player': player_stats
    })

@app.route('/api/graph')
def get_graph_data():
    """Get graph data for visualization"""
    # Get atoms
    atoms = []
    if hasattr(engine.storage, 'get_all_atoms'):
        atoms = engine.storage.get_all_atoms()
    
    # Convert to graph format
    nodes = []
    links = []
    
    for atom in atoms:
        nodes.append({
            'id': atom['id'],
            'name': atom['value'],
            'val': atom['weight'],
            'group': atom.get('category', 'default')
        })
    
    # Add some connections based on patterns
    if len(nodes) > 1:
        for i in range(min(10, len(nodes)-1)):
            links.append({
                'source': nodes[i]['id'],
                'target': nodes[i+1]['id']
            })
    
    return jsonify({
        'nodes': nodes,
        'links': links
    })

def open_browser():
    """Open browser after server starts"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Create HTML file if it doesn't exist
    if not os.path.exists('crod_ui.html'):
        print("Creating HTML UI file...")
        with open('crod_ui.html', 'w') as f:
            f.write('''<!-- PLACEHOLDER - See next artifact for full HTML -->''')
    
    # Open browser after 1 second
    threading.Timer(1, open_browser).start()
    
    # Start server
    print("Starting CROD Web UI on http://localhost:5000")
    app.run(debug=False, port=5000)