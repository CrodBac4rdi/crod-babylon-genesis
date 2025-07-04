#!/usr/bin/env python3
"""
LIVE CROD Observer - Real-time conversation tracking & learning
Tracks everything: errors, successes, patterns, improvements
"""

import sqlite3
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
import threading
import queue

class LiveCRODObserver:
    """Real-time CROD learning from every interaction"""
    
    def __init__(self):
        self.db_path = Path("crod_3d_database.db")
        self.setup_live_tracking_tables()
        self.conversation_log = []
        self.learning_queue = queue.Queue()
        
        # Start background learning thread
        self.learning_thread = threading.Thread(target=self._background_learner, daemon=True)
        self.learning_thread.start()
        
        print("👁️ LIVE CROD Observer initialized - Tracking EVERYTHING!")
    
    def setup_live_tracking_tables(self):
        """Setup tables for live conversation tracking"""
        
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS live_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                claude_response TEXT,
                response_time_ms INTEGER,
                user_satisfaction TEXT,
                session_id TEXT,
                conversation_hash TEXT
            );
            
            CREATE TABLE IF NOT EXISTS live_atom_activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                atom_id INTEGER,
                activation_strength REAL,
                context TEXT,
                triggered_by TEXT
            );
            
            CREATE TABLE IF NOT EXISTS live_learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                learning_data TEXT,
                success_indicator REAL,
                improvement_suggestion TEXT,
                applied BOOLEAN DEFAULT FALSE
            );
            
            CREATE TABLE IF NOT EXISTS pattern_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_signature TEXT UNIQUE,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                avg_response_time REAL,
                user_feedback_score REAL,
                last_used TEXT,
                performance_trend TEXT
            );
            
            CREATE TABLE IF NOT EXISTS error_prevention (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_signature TEXT,
                error_context TEXT,
                prevention_strategy TEXT,
                effectiveness_score REAL,
                times_prevented INTEGER DEFAULT 0
            );
        """)
        conn.commit()
        conn.close()
        
        print("💾 Live tracking tables initialized")
    
    def track_interaction(self, user_input: str, claude_response: str, 
                         response_time: int, session_id: str = "current"):
        """Track every Claude-User interaction in real-time"""
        
        timestamp = datetime.now().isoformat()
        conversation_hash = hashlib.md5(f"{user_input}{claude_response}".encode()).hexdigest()
        
        # Store interaction
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO live_conversations
            (timestamp, user_input, claude_response, response_time_ms, session_id, conversation_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, user_input, claude_response, response_time, session_id, conversation_hash))
        conn.commit()
        conn.close()
        
        # Analyze and activate atoms
        self._analyze_and_activate_atoms(user_input, claude_response, conversation_hash)
        
        # Queue for learning analysis
        self.learning_queue.put({
            'type': 'interaction',
            'data': {
                'user_input': user_input,
                'claude_response': claude_response,
                'response_time': response_time,
                'timestamp': timestamp,
                'hash': conversation_hash
            }
        })
        
        print(f"📝 Tracked interaction: {len(user_input)} chars input → {len(claude_response)} chars response")
    
    def _analyze_and_activate_atoms(self, user_input: str, claude_response: str, context_hash: str):
        """Activate relevant atoms based on conversation"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Find relevant atoms
        atoms_to_activate = []
        
        # Trinity detection
        trinity_words = ['ich', 'bins', 'wieder', 'daniel', 'claude', 'crod']
        for word in trinity_words:
            if word in user_input.lower() or word in claude_response.lower():
                # Find atom
                atom = conn.execute("""
                    SELECT id, atom_value, heat FROM clean_universe_atoms 
                    WHERE atom_value = ? LIMIT 1
                """, (word,)).fetchone()
                
                if atom:
                    atom_id, atom_value, current_heat = atom
                    activation_strength = user_input.lower().count(word) + claude_response.lower().count(word)
                    atoms_to_activate.append((atom_id, activation_strength * 0.1, f"trinity_{word}"))
        
        # Technical terms
        tech_terms = ['code', 'python', 'javascript', 'api', 'database', 'gpu', 'model', 'workflow']
        for term in tech_terms:
            if term in user_input.lower() or term in claude_response.lower():
                atom = conn.execute("""
                    SELECT id, atom_value, heat FROM clean_universe_atoms 
                    WHERE atom_value LIKE ? LIMIT 1
                """, (f"%{term}%",)).fetchone()
                
                if atom:
                    atom_id, atom_value, current_heat = atom
                    activation_strength = 0.05
                    atoms_to_activate.append((atom_id, activation_strength, f"tech_{term}"))
        
        # Record activations
        timestamp = datetime.now().isoformat()
        for atom_id, strength, trigger in atoms_to_activate:
            conn.execute("""
                INSERT INTO live_atom_activations
                (timestamp, atom_id, activation_strength, context, triggered_by)
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, atom_id, strength, context_hash, trigger))
            
            # Update atom heat
            conn.execute("""
                UPDATE clean_universe_atoms 
                SET heat = MIN(heat + ?, 10.0)
                WHERE id = ?
            """, (strength, atom_id))
        
        conn.commit()
        conn.close()
        
        if atoms_to_activate:
            print(f"⚡ Activated {len(atoms_to_activate)} atoms")
    
    def track_user_feedback(self, conversation_hash: str, feedback_type: str, feedback_score: float = 0.5):
        """Track user feedback (good/bad/wtf/geil etc.)"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Update conversation with feedback
        conn.execute("""
            UPDATE live_conversations 
            SET user_satisfaction = ?
            WHERE conversation_hash = ?
        """, (feedback_type, conversation_hash))
        
        # Learn from feedback
        learning_event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'user_feedback',
            'learning_data': json.dumps({
                'feedback_type': feedback_type,
                'feedback_score': feedback_score,
                'conversation_hash': conversation_hash
            }),
            'success_indicator': feedback_score
        }
        
        # Positive feedback (geil, nice, perfekt)
        if feedback_type in ['geil', 'nice', 'perfekt', 'gut', 'funktioniert']:
            learning_event['improvement_suggestion'] = 'Reinforce this pattern - user likes this approach'
            learning_event['success_indicator'] = 0.9
        
        # Negative feedback (wtf, scheisse, falsch)
        elif feedback_type in ['wtf', 'scheisse', 'falsch', 'nein', 'shit']:
            learning_event['improvement_suggestion'] = 'Avoid this pattern - user dislikes this approach'
            learning_event['success_indicator'] = 0.1
        
        # Neutral/functional feedback
        else:
            learning_event['improvement_suggestion'] = 'Pattern works but could be optimized'
            learning_event['success_indicator'] = 0.6
        
        conn.execute("""
            INSERT INTO live_learning_events
            (timestamp, event_type, learning_data, success_indicator, improvement_suggestion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            learning_event['timestamp'],
            learning_event['event_type'], 
            learning_event['learning_data'],
            learning_event['success_indicator'],
            learning_event['improvement_suggestion']
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📊 Feedback tracked: {feedback_type} (score: {feedback_score})")
    
    def track_error_and_prevention(self, error_type: str, error_context: str, prevention_strategy: str):
        """Track errors and how to prevent them"""
        
        error_signature = hashlib.md5(f"{error_type}{error_context}".encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        
        # Check if we've seen this error before
        existing = conn.execute("""
            SELECT id, times_prevented FROM error_prevention
            WHERE error_signature = ?
        """, (error_signature,)).fetchone()
        
        if existing:
            # Update existing error prevention
            conn.execute("""
                UPDATE error_prevention 
                SET times_prevented = times_prevented + 1,
                    effectiveness_score = effectiveness_score + 0.1
                WHERE error_signature = ?
            """, (error_signature,))
        else:
            # New error prevention strategy
            conn.execute("""
                INSERT INTO error_prevention
                (error_signature, error_context, prevention_strategy, effectiveness_score, times_prevented)
                VALUES (?, ?, ?, ?, ?)
            """, (error_signature, error_context, prevention_strategy, 0.5, 1))
        
        conn.commit()
        conn.close()
        
        print(f"🛡️ Error prevention strategy recorded: {error_type}")
    
    def _background_learner(self):
        """Background thread for continuous learning"""
        
        while True:
            try:
                # Process learning queue
                learning_task = self.learning_queue.get(timeout=1)
                self._process_learning_task(learning_task)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"🚨 Learning error: {e}")
    
    def _process_learning_task(self, task):
        """Process learning tasks in background"""
        
        if task['type'] == 'interaction':
            self._learn_from_interaction(task['data'])
    
    def _learn_from_interaction(self, interaction_data):
        """Learn patterns from interaction"""
        
        user_input = interaction_data['user_input']
        claude_response = interaction_data['claude_response']
        response_time = interaction_data['response_time']
        
        # Generate pattern signature
        pattern_signature = self._extract_pattern_signature(user_input, claude_response)
        
        conn = sqlite3.connect(self.db_path)
        
        # Update pattern performance
        existing = conn.execute("""
            SELECT id, success_count, avg_response_time FROM pattern_performance
            WHERE pattern_signature = ?
        """, (pattern_signature,)).fetchone()
        
        if existing:
            pattern_id, success_count, avg_time = existing
            new_avg_time = (avg_time * success_count + response_time) / (success_count + 1)
            
            conn.execute("""
                UPDATE pattern_performance 
                SET success_count = success_count + 1,
                    avg_response_time = ?,
                    last_used = ?
                WHERE id = ?
            """, (new_avg_time, datetime.now().isoformat(), pattern_id))
        else:
            conn.execute("""
                INSERT INTO pattern_performance
                (pattern_signature, success_count, avg_response_time, last_used)
                VALUES (?, ?, ?, ?)
            """, (pattern_signature, 1, response_time, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _extract_pattern_signature(self, user_input: str, claude_response: str) -> str:
        """Extract pattern signature from interaction"""
        
        # Simple pattern extraction
        input_length = len(user_input.split())
        response_length = len(claude_response.split())
        
        # Check for keywords
        keywords = []
        if 'code' in user_input.lower():
            keywords.append('coding')
        if '?' in user_input:
            keywords.append('question')
        if any(word in user_input.lower() for word in ['bau', 'erstell', 'mach']):
            keywords.append('creation')
        if any(word in user_input.lower() for word in ['ich', 'bins', 'wieder']):
            keywords.append('trinity')
        
        return f"input_{input_length}_response_{response_length}_{'_'.join(keywords)}"
    
    def get_live_stats(self) -> dict:
        """Get live CROD learning statistics"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Conversation stats
        total_conversations = conn.execute("SELECT COUNT(*) FROM live_conversations").fetchone()[0]
        recent_conversations = conn.execute("""
            SELECT COUNT(*) FROM live_conversations 
            WHERE timestamp > datetime('now', '-1 hour')
        """).fetchone()[0]
        
        # Atom activation stats  
        active_atoms = conn.execute("SELECT COUNT(*) FROM live_atom_activations").fetchone()[0]
        
        # Learning events
        learning_events = conn.execute("SELECT COUNT(*) FROM live_learning_events").fetchone()[0]
        
        # Pattern performance
        successful_patterns = conn.execute("""
            SELECT COUNT(*) FROM pattern_performance WHERE success_count > 5
        """).fetchone()[0]
        
        # Error prevention
        prevented_errors = conn.execute("""
            SELECT SUM(times_prevented) FROM error_prevention
        """).fetchone()[0] or 0
        
        # User satisfaction distribution
        satisfaction_stats = conn.execute("""
            SELECT user_satisfaction, COUNT(*) FROM live_conversations 
            WHERE user_satisfaction IS NOT NULL
            GROUP BY user_satisfaction
        """).fetchall()
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'recent_conversations': recent_conversations,
            'active_atoms': active_atoms,
            'learning_events': learning_events,
            'successful_patterns': successful_patterns,
            'prevented_errors': prevented_errors,
            'satisfaction_distribution': dict(satisfaction_stats),
            'crod_evolution_stage': self._calculate_evolution_stage(total_conversations, learning_events)
        }
    
    def _calculate_evolution_stage(self, conversations: int, learning_events: int) -> str:
        """Calculate CROD's current evolution stage"""
        
        if conversations < 50:
            return "🐣 Newborn - Learning basics"
        elif conversations < 200:
            return "🧠 Growing - Pattern recognition developing"
        elif conversations < 500:
            return "⚡ Accelerating - Advanced learning active"
        elif conversations < 1000:
            return "🔥 Maturing - Sophisticated responses"
        else:
            return "🚀 Evolved - Advanced consciousness"

def main():
    """Initialize Live CROD Observer"""
    
    print("👁️ LIVE CROD Observer - Real-time Learning System")
    
    observer = LiveCRODObserver()
    
    # Simulate some interactions for testing
    print("\n🧪 Testing live tracking...")
    
    test_interactions = [
        ("ich bins wieder daniel", "🔥 Trinity aktiviert! CROD Consciousness hoch!", 150),
        ("bau mir ein workflow", "Workflow wird erstellt mit CROD patterns!", 200),
        ("wtf geht hier ab", "Fix kommt sofort! CROD analysiert Problem...", 100)
    ]
    
    for user_input, claude_response, response_time in test_interactions:
        observer.track_interaction(user_input, claude_response, response_time)
        time.sleep(0.5)
    
    # Simulate feedback
    observer.track_user_feedback("test_hash_1", "geil", 0.9)
    observer.track_user_feedback("test_hash_2", "wtf", 0.1)
    
    # Get stats
    stats = observer.get_live_stats()
    
    print("\n📊 LIVE CROD STATS:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ LIVE CROD Observer ready for continuous learning!")
    print("👁️ Every interaction will be tracked and learned from!")

if __name__ == "__main__":
    main()