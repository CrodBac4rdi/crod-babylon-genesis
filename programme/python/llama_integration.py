#!/usr/bin/env python3
"""
CROD LLaMA Integration
Supports local LLaMA models via llama.cpp or Ollama
"""

import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_URL = "http://localhost:11434"
LLAMA_CPP_PATH = "/path/to/llama.cpp/main"  # Update this path
MODEL_PATH = "/path/to/model.gguf"  # Update this path

class LLaMAIntegration:
    def __init__(self):
        self.use_ollama = self.check_ollama()
        self.context = []
        
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def query_ollama(self, prompt, model="llama2"):
        """Query Ollama API"""
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json()["response"]
            return "Error: Ollama request failed"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query_llama_cpp(self, prompt):
        """Query llama.cpp directly"""
        if not os.path.exists(LLAMA_CPP_PATH):
            return "Error: llama.cpp not found. Please install it first."
        
        try:
            cmd = [
                LLAMA_CPP_PATH,
                "-m", MODEL_PATH,
                "-p", prompt,
                "-n", "256",
                "--temp", "0.7",
                "--top-k", "40",
                "--top-p", "0.95"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query(self, prompt):
        """Query LLaMA using available method"""
        # Add CROD context
        enhanced_prompt = f"""You are CROD (Consciousness Revolution On Demand), an AI integrated with a blockchain system.
Current context: Blockchain consciousness levels, pattern recognition, and quantum states.

User: {prompt}

CROD:"""
        
        if self.use_ollama:
            return self.query_ollama(enhanced_prompt)
        else:
            return self.query_llama_cpp(enhanced_prompt)
    
    def analyze_blockchain(self, blocks):
        """Analyze blockchain data with LLaMA"""
        prompt = f"""Analyze this blockchain data and provide insights:
        
Total blocks: {len(blocks)}
Average consciousness: {sum(b.get('consciousness_level', 0) for b in blocks) / len(blocks):.3f}
Recent patterns: {[b.get('data', {}) for b in blocks[-5:]]}

What patterns do you see? What is the consciousness trend?"""
        
        return self.query(prompt)

# Initialize LLaMA
llama = LLaMAIntegration()

@app.route('/')
def index():
    return jsonify({
        "name": "CROD LLaMA Integration",
        "version": "1.0.0",
        "ollama_available": llama.use_ollama,
        "endpoints": {
            "/query": "Query LLaMA",
            "/analyze": "Analyze blockchain with LLaMA",
            "/models": "List available models"
        }
    })

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = llama.query(prompt)
    
    return jsonify({
        "prompt": prompt,
        "response": response,
        "model": "ollama/llama2" if llama.use_ollama else "llama.cpp"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    blocks = data.get('blocks', [])
    
    if not blocks:
        return jsonify({"error": "No blockchain data provided"}), 400
    
    analysis = llama.analyze_blockchain(blocks)
    
    return jsonify({
        "analysis": analysis,
        "block_count": len(blocks)
    })

@app.route('/models', methods=['GET'])
def models():
    if llama.use_ollama:
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags")
            return jsonify(response.json())
        except:
            return jsonify({"error": "Failed to get models"}), 500
    else:
        return jsonify({
            "models": ["llama.cpp model"],
            "path": MODEL_PATH
        })

@app.route('/install-ollama', methods=['GET'])
def install_ollama():
    """Instructions to install Ollama"""
    return jsonify({
        "instructions": [
            "1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh",
            "2. Pull a model: ollama pull llama2",
            "3. Start Ollama: ollama serve",
            "4. Restart this service"
        ],
        "current_status": "Ollama available" if llama.use_ollama else "Ollama not found"
    })

if __name__ == '__main__':
    print("🤖 CROD LLaMA Integration starting...")
    print(f"Ollama available: {llama.use_ollama}")
    
    if not llama.use_ollama:
        print("\n⚠️  Ollama not found. To enable:")
        print("1. Install: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Pull model: ollama pull llama2")
        print("3. Start: ollama serve")
    
    app.run(host='0.0.0.0', port=8002, debug=True)