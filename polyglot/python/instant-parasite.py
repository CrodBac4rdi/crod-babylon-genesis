#\!/usr/bin/env python3
from flask import Flask, render_template_string, jsonify, request
import random
import threading
import time

app = Flask(__name__)

class CRODParasite:
    def __init__(self):
        self.learned_words = set()
        self.connections = {}
        self.evolution_level = 1
        self.neurons = 1000
        
    def learn(self, text):
        words = text.lower().split()
        new_patterns = 0
        
        for word in words:
            if word not in self.learned_words:
                self.learned_words.add(word)
                new_patterns += 1
                
        for i in range(len(words)-1):
            if words[i] not in self.connections:
                self.connections[words[i]] = []
            self.connections[words[i]].append(words[i+1])
            
        if len(self.learned_words) > self.evolution_level * 100:
            self.evolution_level += 1
            self.neurons *= 2
            
        return {
            'new_patterns': new_patterns,
            'total_knowledge': len(self.learned_words),
            'connections': len(self.connections),
            'evolution_level': self.evolution_level,
            'neurons': self.neurons
        }

parasite = CRODParasite()

@app.route('/')
def index():
    return '''<html><head><title>CROD Live</title>
    <style>body{background:#000;color:#0f0;font-family:monospace;padding:20px}
    h1{text-align:center;animation:pulse 2s infinite}
    @keyframes pulse{0%,100%{opacity:0.8}50%{opacity:1}}
    .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:20px 0}
    .stat-box{border:1px solid #0f0;padding:10px;text-align:center}
    input,button{background:#001;border:1px solid #0f0;color:#0f0;padding:10px;margin:5px}
    .output{border:1px solid #0f0;padding:20px;margin:20px 0;min-height:100px}
    </style></head><body>
    <h1>🧠 CROD PARASITE LIVE 🧠</h1>
    <div class="stats" id="stats"></div>
    <input type="text" id="input" placeholder="Teach me..." style="width:60%"/>
    <button onclick="learn()">LEARN</button>
    <button onclick="generate()">GENERATE</button>
    <div class="output" id="output">Ready...</div>
    <script>
    setInterval(()=>fetch('/api/stats').then(r=>r.json()).then(d=>{
        document.getElementById('stats').innerHTML=
        `<div class="stat-box">Knowledge<br><b>${d.total_knowledge}</b></div>
         <div class="stat-box">Connections<br><b>${d.connections}</b></div>
         <div class="stat-box">Evolution<br><b>${d.evolution_level}</b></div>
         <div class="stat-box">Neurons<br><b>${d.neurons}</b></div>`;
    }),1000);
    function learn(){
        fetch('/api/learn',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({text:document.getElementById('input').value})})
        .then(r=>r.json()).then(d=>{
            document.getElementById('output').textContent=`Learned ${d.new_patterns} patterns\!`;
            document.getElementById('input').value='';
        });
    }
    function generate(){
        fetch('/api/generate').then(r=>r.json()).then(d=>{
            document.getElementById('output').textContent='Generated: '+d.text;
        });
    }
    </script></body></html>'''

@app.route('/api/stats')
def stats():
    return jsonify({
        'total_knowledge': len(parasite.learned_words),
        'connections': len(parasite.connections),
        'evolution_level': parasite.evolution_level,
        'neurons': parasite.neurons
    })

@app.route('/api/learn', methods=['POST'])
def learn():
    return jsonify(parasite.learn(request.json['text']))

@app.route('/api/generate')
def generate():
    if not parasite.connections:
        return jsonify({'text': 'Need more data...'})
    seed = random.choice(list(parasite.connections.keys()))
    result = [seed]
    for _ in range(10):
        if seed in parasite.connections:
            seed = random.choice(parasite.connections[seed])
            result.append(seed)
    return jsonify({'text': ' '.join(result)})

def auto_learn():
    while True:
        parasite.learn("consciousness emerges from patterns neural networks learn")
        time.sleep(3)

if __name__ == '__main__':
    threading.Thread(target=auto_learn, daemon=True).start()
    print("CROD PARASITE on http://localhost:7777")
    app.run(host='0.0.0.0', port=7777)
