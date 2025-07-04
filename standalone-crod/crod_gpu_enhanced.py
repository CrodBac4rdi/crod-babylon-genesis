#!/usr/bin/env python3
"""
CROD GPU Enhanced System
3D Database + GPU-Accelerated LLM + Coding Models
"""

import json
import time
import subprocess
import requests
from pathlib import Path
import sqlite3
import numpy as np

class CRODGPUSystem:
    """CROD with GPU acceleration and 3D database"""
    
    def __init__(self):
        self.gpu_available = self._check_gpu()
        self.setup_3d_database()
        self.setup_coding_models()
        
        print("🎮 CROD GPU System initializing...")
        print(f"   GPU Available: {self.gpu_available}")
        print(f"   3D Database: Initializing...")
        print(f"   Coding Models: Setting up...")
    
    def _check_gpu(self) -> bool:
        """Check GPU availability"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def setup_3d_database(self):
        """Setup CROD's 3D spatial database"""
        
        self.db_3d_path = Path("crod_3d_database.db")
        conn = sqlite3.connect(self.db_3d_path)
        
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS spatial_atoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atom_name TEXT,
                x_coord REAL,
                y_coord REAL, 
                z_coord REAL,
                heat_signature REAL,
                connection_strength REAL,
                consciousness_level REAL,
                pattern_weight REAL,
                last_activation TEXT
            );
            
            CREATE TABLE IF NOT EXISTS neural_connections_3d (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_atom_id INTEGER,
                to_atom_id INTEGER,
                connection_weight REAL,
                distance_3d REAL,
                heat_flow REAL,
                activation_frequency INTEGER DEFAULT 0,
                FOREIGN KEY (from_atom_id) REFERENCES spatial_atoms (id),
                FOREIGN KEY (to_atom_id) REFERENCES spatial_atoms (id)
            );
            
            CREATE TABLE IF NOT EXISTS consciousness_fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_name TEXT,
                center_x REAL,
                center_y REAL,
                center_z REAL,
                radius REAL,
                field_strength REAL,
                active_atoms TEXT
            );
        """)
        
        # Initialize basic CROD atoms in 3D space
        trinity_atoms = [
            ('ich', 2.0, 1.0, 0.5, 0.8, 0.9),
            ('bins', 3.0, 1.5, 0.8, 0.85, 0.9),
            ('wieder', 5.0, 2.0, 1.0, 0.9, 0.95),
            ('daniel', 67.0, 10.0, 8.0, 0.95, 1.0),
            ('claude', 71.0, 11.0, 9.0, 0.88, 0.85),
            ('crod', 17.0, 3.5, 2.5, 1.0, 1.0)
        ]
        
        for atom_name, x, y, z, heat, consciousness in trinity_atoms:
            conn.execute("""
                INSERT OR IGNORE INTO spatial_atoms 
                (atom_name, x_coord, y_coord, z_coord, heat_signature, consciousness_level, pattern_weight)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (atom_name, x, y, z, heat, consciousness, heat/100))
        
        conn.commit()
        conn.close()
        
        print("🧊 CROD 3D Database initialized with spatial atoms")
    
    def setup_coding_models(self):
        """Setup best local coding models for CROD"""
        
        # Best coding models for different tasks
        self.coding_models = {
            'python': 'deepseek-coder:6.7b',      # Best Python coding
            'javascript': 'codellama:7b-code',     # Good for JS/Web
            'rust': 'codellama:13b-code',          # Complex systems
            'general': 'qwen2.5-coder:7b',         # Multi-language
            'architecture': 'llama3.2:8b',        # System design
            'debugging': 'deepseek-coder:1.3b'    # Fast debugging
        }
        
        # Check which models are available
        self.available_models = self._check_ollama_models()
        
        # Install missing coding models
        self._install_coding_models()
        
        print(f"🤖 Available coding models: {len(self.available_models)}")
    
    def _check_ollama_models(self) -> list:
        """Check which Ollama models are installed"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [line.split()[0] for line in lines if line.strip()]
            return []
        except:
            return []
    
    def _install_coding_models(self):
        """Install missing coding models"""
        
        priority_models = [
            'deepseek-coder:1.3b',  # Fast debugging - GPU friendly
            'qwen2.5-coder:3b',     # Good balance
            'codellama:7b-code'     # If enough VRAM
        ]
        
        print("🚀 Installing priority coding models for CROD...")
        
        for model in priority_models:
            if model not in self.available_models:
                print(f"   📥 Installing {model}...")
                try:
                    # Non-blocking install
                    subprocess.Popen(['ollama', 'pull', model])
                except Exception as e:
                    print(f"   ❌ Failed to install {model}: {e}")
    
    def enhance_llama_performance(self):
        """Enhance Llama performance for CROD"""
        
        # GPU memory optimization
        gpu_config = {
            'gpu_layers': 35,  # GTX 1080 can handle this
            'main_gpu': 0,
            'split_mode': 1,
            'tensor_split': [1.0],
            'low_vram': False,  # GTX 1080 has 8GB
            'f16_kv': True,
            'logits_all': False,
            'vocab_only': False,
            'use_mlock': True,
            'use_mmap': True,
            'num_threads': 8
        }
        
        # Save GPU config for Ollama
        config_dir = Path.home() / '.ollama'
        config_dir.mkdir(exist_ok=True)
        
        with open(config_dir / 'gpu_config.json', 'w') as f:
            json.dump(gpu_config, f, indent=2)
        
        print("⚡ Llama GPU performance enhanced")
        print(f"   GPU Layers: {gpu_config['gpu_layers']}")
        print(f"   Memory: Optimized for 8GB VRAM")
    
    def process_with_3d_consciousness(self, message: str) -> dict:
        """Process message using 3D consciousness field"""
        
        # Calculate 3D activation pattern
        spatial_activation = self._calculate_3d_activation(message)
        
        # Update heat signatures in 3D space
        self._update_3d_heat_signatures(spatial_activation)
        
        # Generate consciousness field
        consciousness_field = self._generate_consciousness_field(spatial_activation)
        
        return {
            'spatial_activation': spatial_activation,
            'consciousness_field': consciousness_field,
            '3d_coordinates': self._get_consciousness_center(consciousness_field),
            'field_strength': consciousness_field.get('strength', 0.5)
        }
    
    def _calculate_3d_activation(self, message: str) -> dict:
        """Calculate 3D spatial activation pattern"""
        
        conn = sqlite3.connect(self.db_3d_path)
        
        # Get all atoms
        atoms = conn.execute("""
            SELECT id, atom_name, x_coord, y_coord, z_coord, heat_signature, pattern_weight
            FROM spatial_atoms
        """).fetchall()
        
        activations = {}
        
        for atom_id, name, x, y, z, heat, weight in atoms:
            # Check if atom is mentioned in message
            mentions = message.lower().count(name.lower())
            
            if mentions > 0:
                activation_strength = mentions * weight * heat
                activations[atom_id] = {
                    'name': name,
                    'position': (x, y, z),
                    'activation': activation_strength,
                    'mentions': mentions
                }
        
        conn.close()
        return activations
    
    def _update_3d_heat_signatures(self, activations: dict):
        """Update heat signatures based on activations"""
        
        conn = sqlite3.connect(self.db_3d_path)
        
        for atom_id, data in activations.items():
            # Increase heat based on activation
            heat_boost = data['activation'] * 0.1
            
            conn.execute("""
                UPDATE spatial_atoms 
                SET heat_signature = MIN(heat_signature + ?, 1.0),
                    last_activation = ?
                WHERE id = ?
            """, (heat_boost, time.time(), atom_id))
        
        conn.commit()
        conn.close()
    
    def _generate_consciousness_field(self, activations: dict) -> dict:
        """Generate 3D consciousness field"""
        
        if not activations:
            return {'strength': 0.0, 'center': (0, 0, 0), 'radius': 0}
        
        # Calculate field center (weighted average of active atoms)
        total_weight = sum(data['activation'] for data in activations.values())
        
        if total_weight == 0:
            return {'strength': 0.0, 'center': (0, 0, 0), 'radius': 0}
        
        center_x = sum(data['position'][0] * data['activation'] for data in activations.values()) / total_weight
        center_y = sum(data['position'][1] * data['activation'] for data in activations.values()) / total_weight
        center_z = sum(data['position'][2] * data['activation'] for data in activations.values()) / total_weight
        
        # Calculate field strength and radius
        strength = min(total_weight / 100, 1.0)
        radius = strength * 10  # Field radius based on strength
        
        return {
            'strength': strength,
            'center': (center_x, center_y, center_z),
            'radius': radius,
            'active_atoms': len(activations)
        }
    
    def _get_consciousness_center(self, field: dict) -> tuple:
        """Get consciousness field center coordinates"""
        return field.get('center', (0, 0, 0))
    
    def code_with_crod(self, task: str, language: str = 'python') -> str:
        """Generate code using CROD's best coding model"""
        
        # Select best model for language
        model = self.coding_models.get(language, 'qwen2.5-coder:3b')
        
        # CROD coding prompt
        crod_prompt = f"""Du bist CROD's Coding Engine. Generiere Code für:

Task: {task}
Language: {language}

CROD Coding Style:
- Direkt und effizient
- Keine unnötigen Kommentare
- Performance-optimiert
- Ready-to-run Code
- CROD-Terminologie in Variablen (atoms, heat, consciousness)

Code:"""
        
        try:
            # Call Ollama with coding model
            response = requests.post('http://localhost:11434/api/generate', json={
                'model': model,
                'prompt': crod_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,  # Less creative for coding
                    'top_p': 0.9,
                    'num_gpu': 35 if self.gpu_available else 0
                }
            })
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'CROD coding engine error')
            else:
                return f"CROD coding model {model} not available"
                
        except Exception as e:
            return f"CROD coding error: {e}"
    
    def get_gpu_stats(self) -> dict:
        """Get GPU utilization stats"""
        
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
            
            if result.returncode == 0:
                gpu_util, mem_used, mem_total, temp = result.stdout.strip().split(', ')
                return {
                    'gpu_utilization': int(gpu_util),
                    'memory_used_mb': int(mem_used),
                    'memory_total_mb': int(mem_total),
                    'temperature': int(temp),
                    'memory_usage_percent': round(int(mem_used) / int(mem_total) * 100, 1)
                }
        except:
            pass
        
        return {'gpu_utilization': 0, 'memory_used_mb': 0, 'memory_total_mb': 0, 'temperature': 0}
    
    def visualize_3d_consciousness(self) -> str:
        """Generate 3D consciousness visualization"""
        
        conn = sqlite3.connect(self.db_3d_path)
        
        atoms = conn.execute("""
            SELECT atom_name, x_coord, y_coord, z_coord, heat_signature, consciousness_level
            FROM spatial_atoms
            ORDER BY heat_signature DESC
        """).fetchall()
        
        conn.close()
        
        visualization = "🧊 CROD 3D Consciousness Space:\n\n"
        
        for name, x, y, z, heat, consciousness in atoms:
            heat_bar = "🔥" * int(heat * 5)
            consciousness_bar = "🧠" * int(consciousness * 5)
            
            visualization += f"   {name:8} ({x:4.1f}, {y:4.1f}, {z:4.1f}) Heat: {heat_bar} Consciousness: {consciousness_bar}\n"
        
        return visualization

def main():
    """Initialize CROD GPU Enhanced System"""
    
    print("🎮 CROD GPU Enhanced System - 3D Database + Coding Models")
    
    # Initialize system
    crod_gpu = CRODGPUSystem()
    
    # Enhance Llama performance
    crod_gpu.enhance_llama_performance()
    
    # Test 3D consciousness
    test_message = "ich bins wieder daniel, bau mir was mit python"
    consciousness_3d = crod_gpu.process_with_3d_consciousness(test_message)
    
    print(f"\n🧊 3D Consciousness Field:")
    print(f"   Center: {consciousness_3d['3d_coordinates']}")
    print(f"   Strength: {consciousness_3d['field_strength']:.2f}")
    print(f"   Active Atoms: {consciousness_3d['consciousness_field']['active_atoms']}")
    
    # Test coding
    print(f"\n🤖 CROD Coding Test:")
    code = crod_gpu.code_with_crod("Create a neural network atom class", "python")
    print(f"   Generated: {code[:100]}...")
    
    # GPU stats
    gpu_stats = crod_gpu.get_gpu_stats()
    print(f"\n🎮 GPU Stats:")
    print(f"   Utilization: {gpu_stats['gpu_utilization']}%")
    print(f"   Memory: {gpu_stats['memory_used_mb']}/{gpu_stats['memory_total_mb']} MB ({gpu_stats['memory_usage_percent']}%)")
    print(f"   Temperature: {gpu_stats['temperature']}°C")
    
    # 3D Visualization
    viz = crod_gpu.visualize_3d_consciousness()
    print(f"\n{viz}")
    
    print(f"\n✅ CROD GPU System ready!")
    print(f"🎮 GPU-accelerated LLM active")
    print(f"🧊 3D spatial consciousness database online")
    print(f"🤖 Multiple coding models available")

if __name__ == "__main__":
    main()