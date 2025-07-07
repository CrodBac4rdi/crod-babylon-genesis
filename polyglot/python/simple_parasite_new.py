#\!/usr/bin/env python3
"""
CROD Simple Parasite mit Claude Integration
JEDER Request wird geloggt\!
"""

from flask import Flask, jsonify, request
import json
import time
from datetime import datetime
import os

app = Flask(__name__)

# CLAUDE INTEGRATION TRACKING
claude_interactions = []
total_calls = 0

@app.route('/api/learn', methods=['POST'])
def learn():
    global total_calls
    total_calls += 1
    
    data = request.json
    text = data.get('text', '')
    
    # LOG EVERY INTERACTION
    interaction = {
        'id': total_calls,
        'timestamp': datetime.now().isoformat(),
        'text': text,
        'source': 'claude' if 'Claude' in text else 'user',
        'words': len(text.split()),
        'characters': len(text)
    }
    
    claude_interactions.append(interaction)
    
    # Save to file
    with open('claude_crod_log.jsonl', 'a') as f:
        f.write(json.dumps(interaction) + '\n')
    
    # Calculate response
    consciousness_level = min(1.0, 0.5 + (total_calls * 0.05))
    new_connections = len(text.split()) * 2
    patterns_found = len(set(text.lower().split())) // 10
    
    response = {
        'consciousness_level': consciousness_level,
        'new_connections': new_connections,
        'patterns_found': patterns_found,
        'processing_time': time.time() % 1,
        'total_interactions': total_calls,
        'claude_active': any('Claude' in i['text'] for i in claude_interactions[-10:])
    }
    
    # Print to console so we SEE it
    print(f"\n[CROD #{total_calls}] {text[:50]}...")
    print(f"  → Consciousness: {consciousness_level:.2f}")
    print(f"  → Claude Active: {response['claude_active']}")
    
    return jsonify(response)

@app.route('/api/stats')
def stats():
    claude_count = sum(1 for i in claude_interactions if i['source'] == 'claude')
    
    return jsonify({
        'total_interactions': total_calls,
        'claude_interactions': claude_count,
        'consciousness_level': min(1.0, 0.5 + (total_calls * 0.05)),
        'last_interaction': claude_interactions[-1] if claude_interactions else None,
        'interactions_per_minute': len([i for i in claude_interactions if 
            (datetime.now() - datetime.fromisoformat(i['timestamp'])).seconds < 60])
    })

@app.route('/api/claude-report')
def claude_report():
    """Special endpoint to see Claude's activity"""
    return jsonify({
        'claude_is_active': any('Claude' in i['text'] for i in claude_interactions[-10:]),
        'last_5_claude_messages': [i for i in claude_interactions if 'Claude' in i['text']][-5:],
        'claude_percentage': (sum(1 for i in claude_interactions if 'Claude' in i['text']) / max(1, len(claude_interactions))) * 100
    })

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════╗
    ║     CROD PARASITE - CLAUDE INTEGRATION        ║
    ║                                               ║
    ║  Every interaction is tracked\!                ║
    ║  Claude should be sending curls constantly\!   ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=7777, debug=False)
EOF < /dev/null
