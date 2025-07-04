# plugins/storage_plugin.py - CROD Storage Plugin
from plugin_base import CRODPlugin
import sqlite3
import json
from typing import List, Dict, Any, Optional

class StoragePlugin(CRODPlugin):
    """Database storage plugin using existing crod_storage.py logic"""
    
    @property
    def name(self):
        return "Storage"
    
    @property
    def version(self):
        return "2.0.0"
    
    @property
    def description(self):
        return "Database storage and retrieval for CROD system"
    
    def initialize(self, system):
        self.system = system
        self.db_path = system.db_path
        self._init_database()
    
    def get_capabilities(self):
        return [
            'get_atom',
            'get_all_atoms',
            'add_atom',
            'update_atom',
            'get_pattern',
            'get_all_patterns',
            'add_pattern',
            'add_route',
            'get_routes',
            'get_stats',
            'search'
        ]
    
    def _init_database(self):
        """Initialize database tables if not exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Atoms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atoms (
                atom_id INTEGER PRIMARY KEY,
                value TEXT NOT NULL,
                weight INTEGER DEFAULT 50,
                category TEXT DEFAULT 'default',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_name TEXT NOT NULL,
                atom_sequence TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Semantic routes table
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
        
        # ML formulas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ml_formulas (
                formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
                formula_name TEXT NOT NULL,
                formula_type TEXT,
                formula_value TEXT NOT NULL,
                numeric_value REAL,
                related_atoms TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Insert core atoms if empty
        cursor.execute('SELECT COUNT(*) FROM atoms')
        if cursor.fetchone()[0] == 0:
            self._insert_core_atoms(conn)
        
        conn.close()
    
    def _insert_core_atoms(self, conn):
        """Insert core CROD atoms"""
        core_atoms = [
            (1, 'CROD', 100, 'core'),
            (2, 'Daniel', 100, 'core'),
            (3, 'Helper', 95, 'core'),
            (4, 'Mental', 95, 'core'),
            (5, 'Systems', 95, 'core'),
            (11, 'null', 90, 'check'),
            (12, 'check', 90, 'check'),
            (46, '?.', 90, 'operator'),
            (64, 'ich', 90, 'daniel'),
            (65, 'halt', 90, 'daniel'),
            (66, 'bruh', 95, 'daniel'),
            (73, '...', 95, 'daniel'),
            (79, 'SELECT', 90, 'sql'),
            (80, 'FROM', 90, 'sql'),
            (171, 'gradient', 85, 'ml'),
            (172, 'vanishing', 80, 'ml'),
            (173, 'exploding', 80, 'ml')
        ]
        
        cursor = conn.cursor()
        cursor.executemany(
    'INSERT OR IGNORE INTO patterns (pattern_id, pattern_name, atom_sequence, confidence, usage_count, success_rate) VALUES (?, ?, ?, ?, ?, ?)',
    patterns
)
        
        # Insert core patterns
        patterns = [
    ('P001', 'NULL_CHECK', '[11, 12]', 0.98, 1847, 0.987),
    ('P076', 'CROD_COMPLETE', '[1, 2, 3, 4, 5]', 1.0, 10000, 1.0),
    ('P075', 'DANIEL_DNA', '[2, 64, 65, 66, 73]', 1.0, 9999, 1.0),
    ('P055', 'ML_GRADIENT', '[171, 172, 173]', 0.96, 456, 0.962)
]

        cursor.executemany(
    'INSERT OR IGNORE INTO patterns (pattern_id, pattern_name, atom_sequence, confidence, usage_count, success_rate) VALUES (?, ?, ?, ?, ?, ?)',
    patterns
)
        
        conn.commit()
    
    def get_atom(self, atom_id: int) -> Optional[Dict]:
        """Get single atom by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM atoms WHERE atom_id = ?', (atom_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'category': row[3]
            }
        return None
    
    def get_all_atoms(self) -> List[Dict]:
        """Get all atoms"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM atoms ORDER BY atom_id')
        atoms = []
        for row in cursor.fetchall():
            atoms.append({
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'category': row[3]
            })
        
        conn.close()
        return atoms
    
    def add_atom(self, value: str, weight: int = 50, category: str = 'default') -> int:
        """Add new atom"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO atoms (value, weight, category) VALUES (?, ?, ?)',
            (value, weight, category)
        )
        atom_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Emit event
        self.system.emit_event(
            'atom_added',
            {'atom_id': atom_id, 'value': value, 'category': category},
            self.name
        )
        
        return atom_id
    
    def get_pattern(self, pattern_id: str) -> Optional[Dict]:
        """Get single pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patterns WHERE pattern_id = ?', (pattern_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'atoms': json.loads(row[2]),
                'confidence': row[3],
                'usage_count': row[4],
                'success_rate': row[5]
            }
        return None
    
    def get_all_patterns(self) -> List[Dict]:
        """Get all patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patterns ORDER BY usage_count DESC')
        patterns = []
        for row in cursor.fetchall():
            patterns.append({
                'id': row[0],
                'name': row[1],
                'atoms': json.loads(row[2]),
                'confidence': row[3],
                'usage_count': row[4],
                'success_rate': row[5]
            })
        
        conn.close()
        return patterns
    
    def add_pattern(self, pattern_name: str, atom_sequence: List[int], confidence: float = 0.5) -> str:
        """Add new pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate pattern ID
        cursor.execute('SELECT COUNT(*) FROM patterns')
        count = cursor.fetchone()[0]
        pattern_id = f'P{2000 + count}'
        
        cursor.execute(
            'INSERT INTO patterns (pattern_id, pattern_name, atom_sequence, confidence) VALUES (?, ?, ?, ?)',
            (pattern_id, pattern_name, json.dumps(atom_sequence), confidence)
        )
        
        conn.commit()
        conn.close()
        
        return pattern_id
    
    def add_route(self, input_atoms: List[int], matched_pattern: str, execution_key: int, success: bool, execution_time: float):
        """Add semantic route execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO semantic_routes (input_atoms, matched_pattern, execution_key, success, execution_time) VALUES (?, ?, ?, ?, ?)',
            (json.dumps(input_atoms), matched_pattern, execution_key, success, execution_time)
        )
        
        # Update pattern success rate
        if matched_pattern:
            cursor.execute(
                'UPDATE patterns SET usage_count = usage_count + 1 WHERE pattern_id = ?',
                (matched_pattern,)
            )
            
            # Calculate new success rate
            cursor.execute(
                'SELECT COUNT(*) as total, SUM(success) as successes FROM semantic_routes WHERE matched_pattern = ?',
                (matched_pattern,)
            )
            total, successes = cursor.fetchone()
            if total > 0:
                success_rate = successes / total
                cursor.execute(
                    'UPDATE patterns SET success_rate = ? WHERE pattern_id = ?',
                    (success_rate, matched_pattern)
                )
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
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
        
        # Success rate
        cursor.execute('SELECT AVG(CAST(success AS REAL)) FROM semantic_routes')
        stats['average_success_rate'] = cursor.fetchone()[0] or 0
        
        # Category distribution
        cursor.execute('SELECT category, COUNT(*) FROM atoms GROUP BY category')
        stats['categories'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def search(self, query: str) -> Dict:
        """Search atoms and patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        results = {'atoms': [], 'patterns': []}
        
        # Search atoms
        cursor.execute(
            'SELECT * FROM atoms WHERE value LIKE ? OR category LIKE ?',
            (f'%{query}%', f'%{query}%')
        )
        for row in cursor.fetchall():
            results['atoms'].append({
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'category': row[3]
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
                'confidence': row[3]
            })
        
        conn.close()
        return results
    
    def handle_event(self, event_type: str, data: Dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'request_stats':
            stats = self.get_stats()
            self.system.emit_event(
                'stats_updated',
                stats,
                self.name,
                source
            )