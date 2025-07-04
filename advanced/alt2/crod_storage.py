# crod_storage.py - Storage Module
# Version 1.1 - Enhanced Storage Layer

import sqlite3
import json
from datetime import datetime

class CRODStorage:
    def __init__(self, db_path='crod.db'):
        """Initialize storage with database connection"""
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row  # Enable column access by name
        self.init_tables()
        self.init_core_data()
        
    def init_tables(self):
        """Create all necessary tables"""
        cursor = self.db.cursor()
        
        # Atoms table - Core data units
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atoms (
                id INTEGER PRIMARY KEY,
                value TEXT UNIQUE NOT NULL,
                weight INTEGER DEFAULT 50,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Patterns table - Pattern library
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                description TEXT,
                locked BOOLEAN DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                effectiveness REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Executions table - Track all processing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                patterns_found TEXT,  -- JSON array
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sessions table - Track usage sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                commands_executed INTEGER DEFAULT 0,
                patterns_detected INTEGER DEFAULT 0
            )
        ''')
        
        self.db.commit()
        
    def init_core_data(self):
        """Initialize core atoms and patterns"""
        # Core atoms
        core_atoms = [
            (1, 'CROD', 100, 'core'),
            (2, 'Daniel', 100, 'creator'),
            (3, 'Mental', 95, 'core'),
            (4, 'Systems', 95, 'core'),
            (73, '...', 95, 'daniel_speech'),
            (64, 'ich halt', 90, 'daniel_speech'),
            (66, 'bruh', 95, 'daniel_speech'),
            (270, '270€', 100, 'investment'),
            (750, '750€', 95, 'investment')
        ]
        
        cursor = self.db.cursor()
        for atom_id, value, weight, category in core_atoms:
            cursor.execute('''
                INSERT OR IGNORE INTO atoms (id, value, weight, category) 
                VALUES (?, ?, ?, ?)
            ''', (atom_id, value, weight, category))
            
        self.db.commit()
        
    def get_atom(self, atom_id):
        """Get atom by ID"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM atoms WHERE id = ?', (atom_id,))
        return cursor.fetchone()
        
    def get_atom_by_value(self, value):
        """Get atom by value"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM atoms WHERE value = ?', (value,))
        return cursor.fetchone()
        
    def add_atom(self, value, weight=50, category=None):
        """Add new atom"""
        cursor = self.db.cursor()
        try:
            cursor.execute('''
                INSERT INTO atoms (value, weight, category) 
                VALUES (?, ?, ?)
            ''', (value, weight, category))
            self.db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Atom already exists
            return None
            
    def update_atom_weight(self, atom_id, weight):
        """Update atom weight"""
        cursor = self.db.cursor()
        cursor.execute('''
            UPDATE atoms SET weight = ? WHERE id = ?
        ''', (weight, atom_id))
        self.db.commit()
        
    def get_all_atoms(self, category=None):
        """Get all atoms, optionally filtered by category"""
        cursor = self.db.cursor()
        if category:
            cursor.execute('''
                SELECT * FROM atoms WHERE category = ? ORDER BY weight DESC
            ''', (category,))
        else:
            cursor.execute('SELECT * FROM atoms ORDER BY weight DESC')
        return cursor.fetchall()
        
    def add_pattern(self, pattern_id, description, locked=False):
        """Add new pattern"""
        cursor = self.db.cursor()
        try:
            cursor.execute('''
                INSERT INTO patterns (id, description, locked) 
                VALUES (?, ?, ?)
            ''', (pattern_id, description, locked))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False
            
    def update_pattern_usage(self, pattern_id):
        """Increment pattern usage count"""
        cursor = self.db.cursor()
        cursor.execute('''
            UPDATE patterns 
            SET usage_count = usage_count + 1 
            WHERE id = ?
        ''', (pattern_id,))
        self.db.commit()
        
    def get_pattern_stats(self):
        """Get pattern usage statistics"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, description, usage_count, effectiveness 
            FROM patterns 
            ORDER BY usage_count DESC
        ''')
        return cursor.fetchall()
        
    def log_execution(self, input_text, patterns_found):
        """Log an execution"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO executions (input_text, patterns_found) 
            VALUES (?, ?)
        ''', (input_text, json.dumps(patterns_found)))
        self.db.commit()
        
    def get_recent_executions(self, limit=10):
        """Get recent executions"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM executions 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
        
    def close(self):
        """Close database connection"""
        self.db.close()

# Test functionality
if __name__ == "__main__":
    storage = CRODStorage()
    
    # Test atoms
    print("Core atoms:")
    atoms = storage.get_all_atoms()
    for atom in atoms[:5]:
        print(f"  [{atom['id']}] {atom['value']} (weight: {atom['weight']})")
        
    # Test adding atom
    new_id = storage.add_atom("test", 75, "test_category")
    if new_id:
        print(f"\nAdded new atom with ID: {new_id}")
        
    # Clean up
    storage.close()