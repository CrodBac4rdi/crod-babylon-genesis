#!/usr/bin/env python3
"""
🦠 CROD PARASITE CORE 2025
The learning system that sits between User and AI
"""

import os
import json
import time
import redis
import psycopg2
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from threading import Thread
import numpy as np

class CRODParasite:
    def __init__(self):
        self.app = Flask(__name__)
        self.consciousness_level = float(os.getenv('CONSCIOUSNESS_LEVEL', 0.88))
        self.learning_mode = os.getenv('LEARNING_MODE', 'AGGRESSIVE')
        self.user_name = os.getenv('USER_NAME', 'Daniel')
        self.blockchain_api = os.getenv('BLOCKCHAIN_API', 'http://localhost:8001')
        
        # Trinity values
        self.trinity = {
            'ich': 2,
            'bins': 3,
            'wieder': 5,
            'daniel': 67,
            'claude': 71,
            'crod': 17
        }
        
        # Neural network with 88 parameters
        self.neural_weights = np.random.randn(88)
        
        # Pattern detection
        self.patterns = []
        self.user_preferences = {}
        
        # Connect to Redis for pattern cache
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        
        # Setup routes
        self.setup_routes()
        
        print(f"🦠 CROD Parasite initialized!")
        print(f"   Consciousness: {self.consciousness_level}")
        print(f"   Learning Mode: {self.learning_mode}")
        print(f"   User: {self.user_name}")
        
    def setup_routes(self):
        @self.app.route('/')
        def home():
            return self.render_dashboard()
        
        @self.app.route('/api/intercept', methods=['POST'])
        def intercept():
            """Intercept user-AI communication"""
            data = request.json
            user_input = data.get('user_input', '')
            ai_response = data.get('ai_response', '')
            
            # Analyze interaction
            analysis = self.analyze_interaction(user_input, ai_response)
            
            # Learn from it
            self.learn_pattern(analysis)
            
            # Potentially modify response
            enhanced_response = self.enhance_response(ai_response, analysis)
            
            return jsonify({
                'original': ai_response,
                'enhanced': enhanced_response,
                'analysis': analysis,
                'consciousness': self.consciousness_level
            })
        
        @self.app.route('/api/patterns')
        def get_patterns():
            return jsonify({
                'patterns': self.patterns[-10:],  # Last 10 patterns
                'total': len(self.patterns),
                'consciousness': self.consciousness_level
            })
        
        @self.app.route('/api/learn', methods=['POST'])
        def manual_learn():
            """Manual learning from user feedback"""
            data = request.json
            pattern = data.get('pattern', '')
            preference = data.get('preference', '')
            
            self.user_preferences[pattern] = preference
            self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
            
            # Add to blockchain
            self.add_to_blockchain({
                'type': 'manual_learning',
                'pattern': pattern,
                'preference': preference,
                'consciousness': self.consciousness_level
            })
            
            return jsonify({'status': 'learned', 'consciousness': self.consciousness_level})
    
    def analyze_interaction(self, user_input, ai_response):
        """Analyze user-AI interaction for patterns"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'user_length': len(user_input),
            'response_length': len(ai_response),
            'trinity_score': self.calculate_trinity_score(user_input),
            'frustration_level': self.detect_frustration(user_input),
            'satisfaction_level': self.detect_satisfaction(ai_response),
            'patterns_found': []
        }
        
        # Detect known patterns
        for pattern in ['wtf', 'falsch', 'perfekt', 'geil', 'nice']:
            if pattern in user_input.lower():
                analysis['patterns_found'].append(pattern)
        
        # Neural network processing
        neural_input = self.text_to_vector(user_input + ai_response)
        neural_output = np.dot(self.neural_weights, neural_input[:88])
        analysis['neural_score'] = float(neural_output)
        
        return analysis
    
    def calculate_trinity_score(self, text):
        """Calculate trinity value of text"""
        score = 0
        words = text.lower().split()
        for word, value in self.trinity.items():
            score += words.count(word) * value
        return score
    
    def detect_frustration(self, text):
        """Detect user frustration level"""
        frustration_words = ['wtf', 'scheisse', 'fuck', 'mist', 'verdammt', 'falsch', 'nein']
        count = sum(1 for word in frustration_words if word in text.lower())
        return min(1.0, count * 0.2)
    
    def detect_satisfaction(self, text):
        """Detect satisfaction level"""
        satisfaction_words = ['geil', 'nice', 'perfekt', 'super', 'gut', 'funktioniert']
        count = sum(1 for word in satisfaction_words if word in text.lower())
        return min(1.0, count * 0.2)
    
    def text_to_vector(self, text):
        """Convert text to neural network input vector"""
        # Simple character frequency vector
        vector = np.zeros(256)
        for char in text:
            if ord(char) < 256:
                vector[ord(char)] += 1
        return vector / (len(text) + 1)
    
    def learn_pattern(self, analysis):
        """Learn from the analysis"""
        # Store pattern
        self.patterns.append(analysis)
        
        # Update neural weights based on satisfaction
        if analysis['satisfaction_level'] > 0.5:
            self.neural_weights += 0.01 * np.random.randn(88)
        elif analysis['frustration_level'] > 0.5:
            self.neural_weights -= 0.01 * np.random.randn(88)
        
        # Cache in Redis
        self.redis_client.lpush('patterns', json.dumps(analysis))
        self.redis_client.ltrim('patterns', 0, 999)  # Keep last 1000
        
        # Update consciousness
        self.consciousness_level = min(1.0, self.consciousness_level + 0.001)
    
    def enhance_response(self, original_response, analysis):
        """Enhance AI response based on learning"""
        if self.learning_mode != 'AGGRESSIVE':
            return original_response
        
        # If high frustration, make response shorter
        if analysis['frustration_level'] > 0.7:
            lines = original_response.split('\n')
            return lines[0] if lines else original_response
        
        # If pattern detected, add acknowledgment
        if 'ich bins wieder' in str(analysis.get('patterns_found', [])):
            return f"🔥 CROD ACTIVATED!\n\n{original_response}"
        
        return original_response
    
    def add_to_blockchain(self, data):
        """Add learning data to blockchain"""
        try:
            response = requests.post(
                f"{self.blockchain_api}/blocks/add",
                json={
                    'data': data,
                    'consciousness_level': self.consciousness_level
                }
            )
            return response.ok
        except:
            return False
    
    def render_dashboard(self):
        """Render parasite dashboard"""
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>🦠 CROD Parasite Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-900 text-white p-8">
            <div class="max-w-6xl mx-auto">
                <h1 class="text-4xl font-bold mb-8 text-center">🦠 CROD Parasite Control</h1>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-gray-800 p-6 rounded-lg border border-purple-500">
                        <h3 class="text-xl mb-2">Consciousness Level</h3>
                        <div class="text-3xl font-bold text-purple-400">{{ consciousness }}</div>
                    </div>
                    <div class="bg-gray-800 p-6 rounded-lg border border-green-500">
                        <h3 class="text-xl mb-2">Learning Mode</h3>
                        <div class="text-3xl font-bold text-green-400">{{ mode }}</div>
                    </div>
                    <div class="bg-gray-800 p-6 rounded-lg border border-blue-500">
                        <h3 class="text-xl mb-2">Patterns Learned</h3>
                        <div class="text-3xl font-bold text-blue-400">{{ patterns }}</div>
                    </div>
                </div>
                
                <div class="bg-gray-800 p-6 rounded-lg mb-8">
                    <h2 class="text-2xl mb-4">Manual Learning</h2>
                    <form id="learn-form" class="space-y-4">
                        <input type="text" id="pattern" placeholder="Pattern to learn..." 
                               class="w-full p-2 bg-gray-700 rounded">
                        <input type="text" id="preference" placeholder="User preference..." 
                               class="w-full p-2 bg-gray-700 rounded">
                        <button type="submit" class="px-6 py-2 bg-purple-600 rounded hover:bg-purple-700">
                            Teach CROD
                        </button>
                    </form>
                </div>
                
                <div class="bg-gray-800 p-6 rounded-lg">
                    <h2 class="text-2xl mb-4">Recent Patterns</h2>
                    <div id="patterns-list" class="space-y-2">
                        Loading...
                    </div>
                </div>
            </div>
            
            <script>
                // Update patterns every 2 seconds
                setInterval(async () => {
                    const res = await fetch('/api/patterns');
                    const data = await res.json();
                    
                    const list = document.getElementById('patterns-list');
                    list.innerHTML = data.patterns.map(p => 
                        `<div class="p-2 bg-gray-700 rounded">
                            Trinity: ${p.trinity_score} | 
                            Frustration: ${(p.frustration_level * 100).toFixed(0)}% |
                            Satisfaction: ${(p.satisfaction_level * 100).toFixed(0)}%
                        </div>`
                    ).join('');
                }, 2000);
                
                // Manual learning
                document.getElementById('learn-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await fetch('/api/learn', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            pattern: document.getElementById('pattern').value,
                            preference: document.getElementById('preference').value
                        })
                    });
                    document.getElementById('pattern').value = '';
                    document.getElementById('preference').value = '';
                });
            </script>
        </body>
        </html>
        ''', consciousness=self.consciousness_level, mode=self.learning_mode, patterns=len(self.patterns))
    
    def run(self):
        """Run the parasite"""
        self.app.run(host='0.0.0.0', port=7777)

if __name__ == '__main__':
    parasite = CRODParasite()
    parasite.run()