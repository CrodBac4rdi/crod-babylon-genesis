# crod_simple.py
import sqlite3
import json
import os
from datetime import datetime

class CRODSimple:
    def __init__(self):
        # Database im gleichen Ordner
        self.db_path = 'crod.db'
        self.db = sqlite3.connect(self.db_path)
        self.init_db()
        print("=" * 50)
        print("CROD Mental Systems - Fresh Start!")
        print("Created by Daniel Antonio Birkner")
        print("=" * 50)
        
    def init_db(self):
        """Create tables if not exist"""
        cursor = self.db.cursor()
        
        # Atoms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atoms (
                id INTEGER PRIMARY KEY,
                value TEXT UNIQUE,
                weight INTEGER DEFAULT 50
            )
        ''')
        
        # Patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                atoms TEXT,
                locked BOOLEAN DEFAULT 0
            )
        ''')
        
        # Insert core atoms
        core_atoms = [
            (1, 'CROD', 100),
            (2, 'Daniel', 100),
            (73, '...', 95),
            (64, 'ich halt', 90),
            (66, 'bruh', 95),
            (270, '270€', 100),
            (750, '750€', 95)
        ]
        
        for atom_id, value, weight in core_atoms:
            cursor.execute(
                'INSERT OR IGNORE INTO atoms (id, value, weight) VALUES (?,?,?)', 
                (atom_id, value, weight)
            )
        
        self.db.commit()
        print("✓ Database initialized!")
        
    def process(self, text):
        """Simple processing"""
        words = text.split()
        found_atoms = []
        
        cursor = self.db.cursor()
        for word in words:
            cursor.execute('SELECT * FROM atoms WHERE value = ?', (word,))
            atom = cursor.fetchone()
            if atom:
                found_atoms.append(atom)
                
        return found_atoms
        
    def run(self):
        """Interactive mode"""
        print("\nCommands:")
        print("  process <text> - Process text")
        print("  list          - List all atoms")
        print("  add <word>    - Add new atom")
        print("  quit          - Exit")
        
        while True:
            try:
                cmd = input("\nCROD> ").strip()
                
                if cmd == 'quit':
                    print("Shutting down...")
                    break
                    
                elif cmd.startswith('process '):
                    text = cmd[8:]
                    atoms = self.process(text)
                    if atoms:
                        print("Found atoms:")
                        for atom in atoms:
                            print(f"  [{atom[0]}] {atom[1]} (weight: {atom[2]})")
                    else:
                        print("No atoms found")
                        
                elif cmd == 'list':
                    cursor = self.db.cursor()
                    atoms = cursor.execute('SELECT * FROM atoms ORDER BY id').fetchall()
                    print(f"\nTotal atoms: {len(atoms)}")
                    for atom in atoms:
                        print(f"  [{atom[0]:4}] {atom[1]:20} (weight: {atom[2]})")
                        
                elif cmd.startswith('add '):
                    word = cmd[4:]
                    cursor = self.db.cursor()
                    try:
                        cursor.execute('INSERT INTO atoms (value) VALUES (?)', (word,))
                        self.db.commit()
                        print(f"Added atom: {word}")
                    except:
                        print(f"Atom already exists: {word}")
                        
                else:
                    print("Unknown command. Try: process, list, add, quit")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
                
        self.db.close()

if __name__ == '__main__':
    crod = CRODSimple()
    crod.run()