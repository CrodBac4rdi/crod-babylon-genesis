# crod_deep_viz_api.py - Backend API for Deep Visualization UI
import os
import json
import sqlite3
import asyncio
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
from collections import defaultdict, Counter
import webbrowser
import threading

app = Flask(__name__)
CORS(app)

class CRODVisualizationAPI:
    def __init__(self, db_path='crod.db'):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize database with sample data if empty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS atoms (
                    atom_id INTEGER PRIMARY KEY,
                    value TEXT NOT NULL,
                    weight INTEGER DEFAULT 50,
                    categories TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_name TEXT NOT NULL,
                    atom_sequence TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS semantic_routes (
                    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_atoms TEXT NOT NULL,
                    matched_pattern TEXT,
                    execution_key INTEGER,
                    success BOOLEAN,
                    execution_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ml_formulas (
                    formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    formula_name TEXT NOT NULL,
                    formula_type TEXT,
                    formula_value TEXT NOT NULL,
                    numeric_value REAL,
                    related_atoms TEXT
                )
            ''')
            
            conn.commit()
            self.insert_sample_data(conn)
        
        conn.close()
    
    def insert_sample_data(self, conn):
        """Insert CROD sample data"""
        cursor = conn.cursor()
        
        # Core atoms
        core_atoms = [
            (1, 'CROD', 100, '["core", "identity", "system"]'),
            (2, 'Daniel', 100, '["core", "creator", "identity"]'),
            (3, 'Helper', 95, '["core", "assistant", "identity"]'),
            (4, 'Mental', 95, '["core", "system", "name"]'),
            (5, 'Systems', 95, '["core", "system", "name"]'),
            (46, '?.', 90, '["operator", "safety", "null-check"]'),
            (64, 'ich', 90, '["daniel", "german", "speech"]'),
            (65, 'halt', 90, '["daniel", "german", "connector"]'),
            (66, 'bruh', 95, '["daniel", "reaction", "frustration"]'),
            (73, '...', 95, '["daniel", "thinking", "pause"]'),
            (79, 'SELECT', 90, '["sql", "command", "query"]'),
            (171, 'gradient', 85, '["ml", "concept", "optimization"]'),
            (172, 'vanishing', 80, '["ml", "problem", "gradient"]'),
            (173, 'exploding', 80, '["ml", "problem", "gradient"]')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO atoms (atom_id, value, weight, categories) VALUES (?, ?, ?, ?)',
            core_atoms
        )
        
        # Core patterns
        patterns = [
            ('P001', 'NULL_CHECK', '[11, 12]', 0.98, 1847, 0.987),
            ('P076', 'CROD_COMPLETE', '[1, 2, 3, 4, 5]', 1.0, 10000, 1.0),
            ('P075', 'DANIEL_DNA', '[2, 64, 65, 66, 73]', 1.0, 9999, 1.0),
            ('P055', 'ML_GRADIENT', '[171, 172, 173]', 0.96, 456, 0.962)
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO patterns VALUES (?, ?, ?, ?, ?, ?)',
            patterns
        )
        
        # ML formulas
        formulas = [
            ('forward_pass', 'gradient', 'z1 = w1*x + b1, h = σ(z1)', None, '[171]'),
            ('loss_gradient_z', 'gradient', '∂L/∂z', 0.6187, '[171]'),
            ('loss_gradient_h', 'gradient', '∂L/∂h', 3.1449, '[171]'),
            ('special_y', 'special', 'y', -1.066, '[171]')
        ]
        
        for formula in formulas:
            cursor.execute(
                'INSERT OR IGNORE INTO ml_formulas (formula_name, formula_type, formula_value, numeric_value, related_atoms) VALUES (?, ?, ?, ?, ?)',
                formula
            )
        
        conn.commit()
    
    def get_graph_data(self):
        """Get node and edge data for visualization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get atoms as nodes
        cursor.execute('SELECT atom_id, value, weight, categories FROM atoms')
        atoms = cursor.fetchall()
        
        nodes = []
        for atom in atoms:
            atom_id, value, weight, categories = atom
            try:
                cats = json.loads(categories) if categories else []
            except:
                cats = []
            
            nodes.append({
                'id': atom_id,
                'label': value,
                'size': weight / 10,  # Scale weight for visualization
                'group': cats[0] if cats else 'default',
                'categories': cats,
                'weight': weight
            })
        
        # Get patterns to create edges
        cursor.execute('SELECT pattern_id, pattern_name, atom_sequence, confidence FROM patterns')
        patterns = cursor.fetchall()
        
        edges = []
        edge_id = 0
        for pattern in patterns:
            pattern_id, pattern_name, atom_sequence, confidence = pattern
            try:
                atoms_in_pattern = json.loads(atom_sequence)
                # Create edges between consecutive atoms in pattern
                for i in range(len(atoms_in_pattern) - 1):
                    edges.append({
                        'id': edge_id,
                        'source': atoms_in_pattern[i],
                        'target': atoms_in_pattern[i + 1],
                        'strength': confidence,
                        'pattern': pattern_id
                    })
                    edge_id += 1
            except:
                pass
        
        conn.close()
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def get_pattern_flow(self):
        """Get pattern execution flow data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sr.input_atoms, sr.matched_pattern, sr.success, sr.execution_time, p.pattern_name
            FROM semantic_routes sr
            LEFT JOIN patterns p ON sr.matched_pattern = p.pattern_id
            ORDER BY sr.created_at DESC
            LIMIT 100
        ''')
        
        flows = []
        for row in cursor.fetchall():
            input_atoms, matched_pattern, success, exec_time, pattern_name = row
            flows.append({
                'input': input_atoms,
                'pattern': matched_pattern,
                'pattern_name': pattern_name or 'Unknown',
                'success': bool(success),
                'time': exec_time
            })
        
        conn.close()
        return flows
    
    def get_ml_data(self):
        """Get ML visualization data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ml_formulas')
        formulas = []
        for row in cursor.fetchall():
            formulas.append({
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'formula': row[3],
                'value': row[4],
                'atoms': json.loads(row[5]) if row[5] else []
            })
        
        conn.close()
        
        # Generate gradient visualization data
        gradients = []
        for i in range(10):
            gradients.append({
                'layer': i,
                'gradient': np.random.exponential(0.5) if i < 5 else np.random.exponential(2.0),
                'type': 'vanishing' if i < 5 else 'exploding'
            })
        
        return {
            'formulas': formulas,
            'gradients': gradients
        }
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count atoms
        cursor.execute('SELECT COUNT(*) FROM atoms')
        stats['total_atoms'] = cursor.fetchone()[0]
        
        # Count patterns
        cursor.execute('SELECT COUNT(*) FROM patterns')
        stats['total_patterns'] = cursor.fetchone()[0]
        
        # Count routes
        cursor.execute('SELECT COUNT(*) FROM semantic_routes')
        stats['total_routes'] = cursor.fetchone()[0]
        
        # Get category distribution
        cursor.execute('SELECT categories FROM atoms WHERE categories IS NOT NULL')
        all_categories = []
        for row in cursor.fetchall():
            try:
                cats = json.loads(row[0])
                all_categories.extend(cats)
            except:
                pass
        
        stats['category_distribution'] = dict(Counter(all_categories))
        
        # Get success rate
        cursor.execute('SELECT AVG(CAST(success AS REAL)) FROM semantic_routes')
        stats['route_success_rate'] = cursor.fetchone()[0] or 0
        
        conn.close()
        return stats
    
    def search(self, query):
        """Search atoms, patterns, and formulas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        results = {
            'atoms': [],
            'patterns': [],
            'formulas': []
        }
        
        # Search atoms
        cursor.execute(
            'SELECT * FROM atoms WHERE value LIKE ? OR categories LIKE ?',
            (f'%{query}%', f'%{query}%')
        )
        for row in cursor.fetchall():
            results['atoms'].append({
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'categories': json.loads(row[3]) if row[3] else []
            })
        
        # Search patterns
        cursor.execute(
            'SELECT * FROM patterns WHERE pattern_name LIKE ? OR pattern_id LIKE ?',
            (f'%{query}%', f'%{query}%')
        )
        for row in cursor.fetchall():
            results['patterns'].append({
                'id': row[0],
                'name': row[1],
                'atoms': json.loads(row[2]),
                'confidence': row[3]
            })
        
        conn.close()
        return results

# Initialize API
viz_api = CRODVisualizationAPI()

# Routes
@app.route('/')
def index():
    """Serve the HTML file"""
    return send_from_directory('.', 'crod_deep_viz_ui.html')

@app.route('/api/graph')
def get_graph():
    """Get graph visualization data"""
    return jsonify(viz_api.get_graph_data())

@app.route('/api/patterns/flow')
def get_pattern_flow():
    """Get pattern execution flow"""
    return jsonify(viz_api.get_pattern_flow())

@app.route('/api/ml')
def get_ml_data():
    """Get ML visualization data"""
    return jsonify(viz_api.get_ml_data())

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    return jsonify(viz_api.get_database_stats())

@app.route('/api/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    return jsonify(viz_api.search(query))

@app.route('/api/atom/<int:atom_id>')
def get_atom(atom_id):
    """Get specific atom details"""
    conn = sqlite3.connect(viz_api.db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM atoms WHERE atom_id = ?', (atom_id,))
    atom = cursor.fetchone()
    
    if not atom:
        return jsonify({'error': 'Atom not found'}), 404
    
    # Get patterns using this atom
    cursor.execute('SELECT * FROM patterns WHERE atom_sequence LIKE ?', (f'%{atom_id}%',))
    patterns = []
    for row in cursor.fetchall():
        patterns.append({
            'id': row[0],
            'name': row[1],
            'confidence': row[3],
            'usage': row[4]
        })
    
    conn.close()
    
    return jsonify({
        'atom': {
            'id': atom[0],
            'value': atom[1],
            'weight': atom[2],
            'categories': json.loads(atom[3]) if atom[3] else []
        },
        'patterns': patterns
    })

def open_browser():
    """Open browser after server starts"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Open browser after 1 second
    timer = threading.Timer(1, open_browser)
    timer.start()
    
    print("🚀 CROD Deep Visualization starting...")
    print("📊 Open http://localhost:5000 in your browser")
    
    # Run server
    app.run(debug=True, port=5000)