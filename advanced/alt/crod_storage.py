# crod_storage.py - Storage Module
# JETZT: Simple SQLite → SPÄTER: Multi-backend Monster!

import sqlite3
import json

class CRODStorage:
    def __init__(self, db_path='crod.db'):
        self.db = sqlite3.connect(db_path)
        self.init_tables()
        
    def init_tables(self):
        """Create basic tables"""
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS atoms (
                id INTEGER PRIMARY KEY,
                value TEXT UNIQUE,
                weight INTEGER DEFAULT 50
            )
        ''')
        
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                description TEXT,
                locked BOOLEAN DEFAULT 0
            )
        ''')
        
    def get_atom(self, atom_id):
        """Get atom by ID"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM atoms WHERE id = ?', (atom_id,))
        return cursor.fetchone()
        
    def add_atom(self, value, weight=50):
        """Add new atom"""
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO atoms (value, weight) VALUES (?, ?)', 
                      (value, weight))
        self.db.commit()
        return cursor.lastrowid

# Später wird das ein MONSTER mit:
# - Redis backend
# - LMDB backend  
# - MongoDB backend
# - Distributed storage
# - Caching layer
# - etc...