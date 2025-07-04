# crod_storage.py - Storage Module Version 2
# Implementiert IStorage Interface - kann nie brechen!

import sqlite3
import json
from typing import Dict, List, Any, Optional
from crod_interfaces import IStorage, Atom

class CRODStorage(IStorage):
    def __init__(self, db_path='crod.db'):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.init_tables()
        
    def init_tables(self):
        """Create tables with ALL columns from start"""
        # Create atoms table with ALL possible columns
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS atoms (
                id INTEGER PRIMARY KEY,
                value TEXT UNIQUE,
                weight INTEGER DEFAULT 50,
                category TEXT DEFAULT 'default',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT DEFAULT '{}'
            )
        ''')
        
        # Create patterns table
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                description TEXT,
                locked BOOLEAN DEFAULT 0,
                atoms TEXT DEFAULT '[]',
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create executions table for logging
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                patterns_found TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.commit()
        print("✓ Database initialized!")
        
    def get_atom(self, atom_id: int) -> Optional[Dict[str, Any]]:
        """Get atom by ID - returns dict or None"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM atoms WHERE id = ?', (atom_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'category': row[3] if len(row) > 3 else 'default',
                'created_at': row[4] if len(row) > 4 else None,
                'metadata': json.loads(row[5]) if len(row) > 5 else {}
            }
        return None
        
    def add_atom(self, value: str, weight: int = 50, category: str = 'default') -> int:
        """Add new atom - returns ID"""
        cursor = self.db.cursor()
        try:
            cursor.execute(
                'INSERT INTO atoms (value, weight, category) VALUES (?, ?, ?)', 
                (value, weight, category)
            )
            self.db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Atom already exists
            cursor.execute('SELECT id FROM atoms WHERE value = ?', (value,))
            return cursor.fetchone()[0]
    
    def get_all_atoms(self) -> List[Dict[str, Any]]:
        """Get all atoms as list of dicts"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM atoms')
        atoms = []
        
        for row in cursor.fetchall():
            atoms.append({
                'id': row[0],
                'value': row[1],
                'weight': row[2],
                'category': row[3] if len(row) > 3 else 'default',
                'created_at': row[4] if len(row) > 4 else None,
                'metadata': json.loads(row[5]) if len(row) > 5 else {}
            })
        
        return atoms
    
    def log_execution(self, text: str, patterns: List[str]):
        """Log execution for learning"""
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO executions (input_text, patterns_found) VALUES (?, ?)',
            (text, json.dumps(patterns))
        )
        self.db.commit()
    
    def get_pattern_stats(self) -> List[Dict[str, Any]]:
        """Get pattern usage statistics"""
        cursor = self.db.cursor()
        cursor.execute('SELECT id, description, usage_count FROM patterns ORDER BY usage_count DESC')
        return [
            {'id': row[0], 'description': row[1], 'usage_count': row[2]}
            for row in cursor.fetchall()
        ]
    
    def update_pattern_usage(self, pattern_id: str):
        """Update pattern usage count"""
        cursor = self.db.cursor()
        cursor.execute(
            'UPDATE patterns SET usage_count = usage_count + 1 WHERE id = ?',
            (pattern_id,)
        )
        self.db.commit()
    
    def get_recent_executions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent executions"""
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT * FROM executions ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        return [
            {
                'id': row[0],
                'input_text': row[1],
                'patterns_found': row[2],
                'timestamp': row[3]
            }
            for row in cursor.fetchall()
        ]
    
    def close(self):
        """Close database connection"""
        self.db.close()

# Backwards compatibility
if __name__ == "__main__":
    # Test storage
    storage = CRODStorage()
    
    # Add test atom
    atom_id = storage.add_atom("test", 75, "test_category")
    print(f"Added atom with ID: {atom_id}")
    
    # Get atom
    atom = storage.get_atom(atom_id)
    print(f"Retrieved atom: {atom}")
    
    # Get all atoms
    all_atoms = storage.get_all_atoms()
    print(f"Total atoms: {len(all_atoms)}")
    
    storage.close()