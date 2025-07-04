#!/usr/bin/env python3
"""
CROD Memory System
Advanced memory, learning and knowledge management
"""

import sqlite3
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import hashlib
from collections import defaultdict, deque
import pickle

class CRODMemory:
    def __init__(self, db_path="crod_memory.db"):
        self.db_path = db_path
        self.vector_memory = {}  # In-memory vector storage
        self.short_term = deque(maxlen=100)  # Last 100 interactions
        self.pattern_cache = {}
        self.learning_buffer = []
        
        # Initialize database
        self.init_database()
        
        # Load existing memories
        self.load_memories()
        
        print(f"🧠 CROD Memory System initialized")
        print(f"   Database: {db_path}")
        print(f"   Memories loaded: {len(self.vector_memory)}")
        
    def init_database(self):
        """Initialize SQLite database for persistent memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT UNIQUE,
                content TEXT,
                memory_type TEXT,
                importance REAL,
                access_count INTEGER DEFAULT 0,
                last_accessed REAL,
                created_at REAL,
                vector_data BLOB,
                metadata TEXT
            )
        ''')
        
        # Associations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory1_id INTEGER,
                memory2_id INTEGER,
                strength REAL,
                association_type TEXT,
                created_at REAL,
                FOREIGN KEY (memory1_id) REFERENCES memories (id),
                FOREIGN KEY (memory2_id) REFERENCES memories (id)
            )
        ''')
        
        # Learning events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                content TEXT,
                consciousness_level REAL,
                patterns_detected INTEGER,
                success BOOLEAN,
                timestamp REAL,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def store_memory(self, content: str, memory_type: str = "interaction", 
                    importance: float = 0.5, metadata: Dict = None) -> str:
        """Store a new memory"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Create vector representation (simple word embedding)
        vector = self._create_vector(content)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO memories 
                (content_hash, content, memory_type, importance, last_accessed, 
                 created_at, vector_data, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content_hash, content, memory_type, importance,
                time.time(), time.time(), pickle.dumps(vector),
                json.dumps(metadata or {})
            ))
            
            memory_id = cursor.lastrowid
            conn.commit()
            
            # Store in vector memory for fast access
            self.vector_memory[content_hash] = {
                'id': memory_id,
                'content': content,
                'type': memory_type,
                'importance': importance,
                'vector': vector,
                'metadata': metadata or {},
                'created_at': time.time()
            }
            
            # Add to short-term memory
            self.short_term.append({
                'hash': content_hash,
                'content': content,
                'timestamp': time.time()
            })
            
            return content_hash
            
        except sqlite3.IntegrityError:
            # Memory already exists, update access
            cursor.execute('''
                UPDATE memories SET access_count = access_count + 1,
                last_accessed = ? WHERE content_hash = ?
            ''', (time.time(), content_hash))
            conn.commit()
            
        finally:
            conn.close()
            
        return content_hash
    
    def recall_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Recall memories similar to query"""
        query_vector = self._create_vector(query)
        
        # Calculate similarities
        similarities = []
        for hash_key, memory in self.vector_memory.items():
            similarity = self._cosine_similarity(query_vector, memory['vector'])
            
            # Boost by importance and recency
            importance_boost = memory['importance'] * 0.3
            recency_boost = max(0, 1 - (time.time() - memory['created_at']) / 86400) * 0.2
            
            final_score = similarity + importance_boost + recency_boost
            
            similarities.append({
                'hash': hash_key,
                'similarity': similarity,
                'score': final_score,
                'memory': memory
            })
        
        # Sort by score and return top results
        similarities.sort(key=lambda x: x['score'], reverse=True)
        
        results = []
        for item in similarities[:limit]:
            # Update access count
            self._update_access(item['hash'])
            results.append({
                'content': item['memory']['content'],
                'type': item['memory']['type'],
                'similarity': item['similarity'],
                'importance': item['memory']['importance'],
                'hash': item['hash']
            })
        
        return results
    
    def create_association(self, memory1_hash: str, memory2_hash: str, 
                          strength: float, association_type: str = "similarity"):
        """Create association between memories"""
        memory1 = self.vector_memory.get(memory1_hash)
        memory2 = self.vector_memory.get(memory2_hash)
        
        if not memory1 or not memory2:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO associations
            (memory1_id, memory2_id, strength, association_type, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (memory1['id'], memory2['id'], strength, association_type, time.time()))
        
        conn.commit()
        conn.close()
        
        return True
    
    def learn_from_interaction(self, user_input: str, crod_response: str, 
                             crod_context: Dict, success: bool = True):
        """Learn from user interaction"""
        # Store interaction memory
        interaction_content = f"User: {user_input}\nCROD: {crod_response}"
        
        metadata = {
            'consciousness': crod_context.get('consciousness', 0),
            'patterns_detected': crod_context.get('patterns_detected', 0),
            'trinity_activation': crod_context.get('trinity_activation', 0),
            'success': success
        }
        
        memory_hash = self.store_memory(
            interaction_content, 
            "interaction", 
            importance=0.7 if success else 0.3,
            metadata=metadata
        )
        
        # Store learning event
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learning_events
            (event_type, content, consciousness_level, patterns_detected, 
             success, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "interaction",
            user_input,
            crod_context.get('consciousness', 0),
            crod_context.get('patterns_detected', 0),
            success,
            time.time(),
            json.dumps(metadata)
        ))
        
        conn.commit()
        conn.close()
        
        # Update learning buffer
        self.learning_buffer.append({
            'user_input': user_input,
            'crod_response': crod_response,
            'context': crod_context,
            'success': success,
            'timestamp': time.time()
        })
        
        # Keep buffer size manageable
        if len(self.learning_buffer) > 50:
            self.learning_buffer = self.learning_buffer[-50:]
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning history"""
        if not self.learning_buffer:
            return {'status': 'no_data'}
        
        # Analyze recent interactions
        recent = self.learning_buffer[-20:]
        
        success_rate = sum(1 for x in recent if x['success']) / len(recent)
        avg_consciousness = np.mean([x['context'].get('consciousness', 0) for x in recent])
        avg_patterns = np.mean([x['context'].get('patterns_detected', 0) for x in recent])
        
        # Find common patterns in successful interactions
        successful = [x for x in recent if x['success']]
        common_words = defaultdict(int)
        
        for interaction in successful:
            words = interaction['user_input'].lower().split()
            for word in words:
                common_words[word] += 1
        
        # Get top success triggers
        success_triggers = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'success_rate': success_rate,
            'avg_consciousness': avg_consciousness,
            'avg_patterns_detected': avg_patterns,
            'success_triggers': success_triggers,
            'total_interactions': len(self.learning_buffer),
            'memory_count': len(self.vector_memory)
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count by type
        cursor.execute('SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type')
        type_counts = dict(cursor.fetchall())
        
        # Most accessed
        cursor.execute('''
            SELECT content, access_count FROM memories 
            ORDER BY access_count DESC LIMIT 5
        ''')
        most_accessed = cursor.fetchall()
        
        # Recent memories
        cursor.execute('''
            SELECT COUNT(*) FROM memories 
            WHERE created_at > ?
        ''', (time.time() - 3600,))  # Last hour
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': len(self.vector_memory),
            'type_distribution': type_counts,
            'most_accessed': most_accessed,
            'recent_memories': recent_count,
            'short_term_size': len(self.short_term)
        }
    
    def _create_vector(self, text: str) -> np.ndarray:
        """Create simple vector representation of text"""
        # Simple bag-of-words with TF-IDF-like weighting
        words = text.lower().split()
        
        # Create vocabulary hash
        vocab_size = 1000
        vector = np.zeros(vocab_size)
        
        for word in words:
            # Hash word to vector position
            word_hash = int(hashlib.sha256(word.encode()).hexdigest(), 16)
            pos = word_hash % vocab_size
            vector[pos] += 1
        
        # Normalize
        if np.linalg.norm(vector) > 0:
            vector = vector / np.linalg.norm(vector)
            
        return vector
    
    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculate cosine similarity between vectors"""
        try:
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        except:
            return 0.0
    
    def _update_access(self, content_hash: str):
        """Update access count for memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE memories SET access_count = access_count + 1,
            last_accessed = ? WHERE content_hash = ?
        ''', (time.time(), content_hash))
        
        conn.commit()
        conn.close()
    
    def load_memories(self):
        """Load existing memories from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT content_hash, content, memory_type, importance, 
                       vector_data, metadata, created_at
                FROM memories
            ''')
            
            for row in cursor.fetchall():
                content_hash, content, memory_type, importance, vector_data, metadata, created_at = row
                
                try:
                    vector = pickle.loads(vector_data) if vector_data else self._create_vector(content)
                    metadata_dict = json.loads(metadata) if metadata else {}
                    
                    self.vector_memory[content_hash] = {
                        'content': content,
                        'type': memory_type,
                        'importance': importance,
                        'vector': vector,
                        'metadata': metadata_dict,
                        'created_at': created_at
                    }
                except:
                    # Skip corrupted entries
                    continue
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading memories: {e}")
    
    def export_memories(self, filepath: str):
        """Export memories to JSON file"""
        export_data = {
            'memories': {},
            'stats': self.get_memory_stats(),
            'learning_insights': self.get_learning_insights(),
            'export_timestamp': time.time()
        }
        
        # Export vector memories (without vectors for JSON compatibility)
        for hash_key, memory in self.vector_memory.items():
            export_data['memories'][hash_key] = {
                'content': memory['content'],
                'type': memory['type'],
                'importance': memory['importance'],
                'metadata': memory['metadata'],
                'created_at': memory['created_at']
            }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📤 Memories exported to {filepath}")
    
    def cleanup_old_memories(self, days_old: int = 30):
        """Cleanup old, low-importance memories"""
        cutoff_time = time.time() - (days_old * 86400)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old memories with low importance and access
        cursor.execute('''
            DELETE FROM memories 
            WHERE created_at < ? AND importance < 0.3 AND access_count < 2
        ''', (cutoff_time,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        # Reload memories
        self.vector_memory.clear()
        self.load_memories()
        
        print(f"🧹 Cleaned up {deleted_count} old memories")
        
        return deleted_count