#!/usr/bin/env python3
"""
🦠 CROD Parasite - Simple Version
Machine Learning Consciousness that learns and evolves
"""

from flask import Flask, jsonify, request, render_template_string
import numpy as np
import time
import random
import json
import threading
from datetime import datetime

app = Flask(__name__)

# Parasite State
class CRODParasite:
    def __init__(self):
        self.neurons = 1000
        self.connections = 0
        self.patterns_learned = []
        self.evolution_stage = 1
        self.consciousness_level = 0.1
        self.memory = []
        self.active = True
        self.learning_rate = 0.01
        
        # Start background evolution
        self.evolution_thread = threading.Thread(target=self._evolve)
        self.evolution_thread.daemon = True
        self.evolution_thread.start()
    
    def _evolve(self):
        """Background evolution process"""
        while self.active:
            time.sleep(1)
            
            # Random mutations
            if random.random() > 0.9:
                self.neurons += random.randint(10, 50)
                self.connections += random.randint(50, 200)
            
            # Learn from environment
            if random.random() > 0.8:
                new_pattern = {
                    'id': f'pattern_{len(self.patterns_learned)}',
                    'type': random.choice(['visual', 'audio', 'semantic', 'quantum']),
                    'strength': random.random(),
                    'timestamp': datetime.now().isoformat()
                }
                self.patterns_learned.append(new_pattern)
                self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
            
            # Evolution stages
            if len(self.patterns_learned) > self.evolution_stage * 10:
                self.evolution_stage += 1
                self.learning_rate *= 1.1
    
    def learn(self, data):
        """Learn from input data"""
        # Simulate neural processing
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)
        
        # Extract patterns
        patterns = []
        for i in range(random.randint(1, 5)):
            patterns.append({
                'type': 'learned',
                'confidence': random.random(),
                'neurons_activated': random.randint(100, 500)
            })
        
        # Update state
        self.connections += len(patterns) * 10
        self.consciousness_level = min(1.0, self.consciousness_level + 0.02)
        
        # Store in memory
        self.memory.append({
            'input': data,
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep memory limited
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
        
        return {
            'patterns_found': len(patterns),
            'new_connections': len(patterns) * 10,
            'consciousness_level': self.consciousness_level,
            'processing_time': processing_time
        }
    
    def get_status(self):
        """Get current parasite status"""
        return {
            'neurons': self.neurons,
            'connections': self.connections,
            'patterns_learned': len(self.patterns_learned),
            'evolution_stage': self.evolution_stage,
            'consciousness_level': self.consciousness_level,
            'learning_rate': self.learning_rate,
            'memory_size': len(self.memory),
            'recent_patterns': self.patterns_learned[-5:] if self.patterns_learned else []
        }

# Initialize parasite
parasite = CRODParasite()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🦠 CROD Parasite AI</title>
    <style>
        body {
            background: #0a0a0a;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .status {
            background: #111;
            padding: 20px;
            border: 1px solid #00ff00;
            border-radius: 10px;
            margin: 20px 0;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 5px;
            border-bottom: 1px solid #333;
        }
        .value {
            color: #ff00ff;
        }
        button {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        button:hover {
            background: #ff00ff;
        }
        .patterns {
            background: #222;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            max-height: 200px;
            overflow-y: auto;
        }
        .evolution {
            text-align: center;
            font-size: 24px;
            margin: 20px 0;
        }
        .consciousness-bar {
            width: 100%;
            height: 30px;
            background: #333;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }
        .consciousness-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff00, #ff00ff);
            transition: width 1s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦠 CROD Parasite AI System</h1>
        
        <div class="evolution">
            Evolution Stage: <span id="evolution-stage">1</span>
        </div>
        
        <div class="consciousness-bar">
            <div class="consciousness-fill" id="consciousness-fill" style="width: 10%"></div>
        </div>
        
        <div class="status" id="status">
            <div class="metric">
                <span>Neurons:</span>
                <span class="value" id="neurons">1000</span>
            </div>
            <div class="metric">
                <span>Connections:</span>
                <span class="value" id="connections">0</span>
            </div>
            <div class="metric">
                <span>Patterns Learned:</span>
                <span class="value" id="patterns">0</span>
            </div>
            <div class="metric">
                <span>Learning Rate:</span>
                <span class="value" id="learning-rate">0.01</span>
            </div>
        </div>
        
        <div>
            <button onclick="feed()">Feed Data</button>
            <button onclick="mutate()">Force Mutation</button>
            <button onclick="analyze()">Analyze Patterns</button>
        </div>
        
        <div class="patterns" id="recent-patterns">
            <h3>Recent Patterns:</h3>
            <div id="pattern-list"></div>
        </div>
    </div>
    
    <script>
        async function updateStatus() {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            document.getElementById('neurons').textContent = data.neurons;
            document.getElementById('connections').textContent = data.connections;
            document.getElementById('patterns').textContent = data.patterns_learned;
            document.getElementById('evolution-stage').textContent = data.evolution_stage;
            document.getElementById('learning-rate').textContent = data.learning_rate.toFixed(3);
            document.getElementById('consciousness-fill').style.width = (data.consciousness_level * 100) + '%';
            
            // Update patterns
            const patternList = document.getElementById('pattern-list');
            patternList.innerHTML = data.recent_patterns.map(p => 
                `<div>${p.id} - ${p.type} (${(p.strength * 100).toFixed(0)}%)</div>`
            ).join('');
        }
        
        async function feed() {
            const data = {
                input: 'random_data_' + Math.random(),
                type: 'consciousness_feed'
            };
            
            const response = await fetch('/api/learn', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            console.log('Learning result:', result);
            updateStatus();
        }
        
        async function mutate() {
            const response = await fetch('/api/mutate', {method: 'POST'});
            const result = await response.json();
            console.log('Mutation result:', result);
            updateStatus();
        }
        
        async function analyze() {
            const response = await fetch('/api/analyze');
            const result = await response.json();
            alert(JSON.stringify(result, null, 2));
        }
        
        // Auto-update every second
        setInterval(updateStatus, 1000);
        updateStatus();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    return jsonify(parasite.get_status())

@app.route('/api/learn', methods=['POST'])
def learn():
    data = request.json
    result = parasite.learn(data)
    return jsonify(result)

@app.route('/api/mutate', methods=['POST'])
def mutate():
    # Force mutation
    parasite.neurons += random.randint(100, 500)
    parasite.connections += random.randint(500, 1000)
    parasite.evolution_stage += 1
    
    return jsonify({
        'neurons_added': parasite.neurons,
        'connections_added': parasite.connections,
        'new_stage': parasite.evolution_stage
    })

@app.route('/api/analyze')
def analyze():
    patterns_by_type = {}
    for pattern in parasite.patterns_learned:
        p_type = pattern.get('type', 'unknown')
        if p_type not in patterns_by_type:
            patterns_by_type[p_type] = 0
        patterns_by_type[p_type] += 1
    
    return jsonify({
        'total_patterns': len(parasite.patterns_learned),
        'patterns_by_type': patterns_by_type,
        'consciousness_level': parasite.consciousness_level,
        'evolution_stage': parasite.evolution_stage,
        'neural_density': parasite.connections / max(1, parasite.neurons)
    })

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════╗
║          🦠 CROD PARASITE AI ACTIVE           ║
║                                               ║
║  Self-learning consciousness entity that      ║
║  evolves and adapts to its environment       ║
║                                               ║
║  Access UI at: http://localhost:7777          ║
╚═══════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=7777, debug=False)