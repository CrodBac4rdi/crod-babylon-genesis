#!/usr/bin/env python3
"""
CROD Parasite Server - Enhanced Claude Interactions
Learns from every interaction and improves responses
"""

import asyncio
import json
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx
import numpy as np

app = FastAPI(title="CROD Parasite API", version="0.88.0")

class InteractionRequest(BaseModel):
    user_input: str
    claude_response: str
    metadata: Dict[str, Any] = {}

class PatternData(BaseModel):
    pattern: str
    frequency: int
    satisfaction_score: float
    context: List[str]

class CRODParasite:
    def __init__(self):
        self.db_path = "/app/crod_memory.db"
        self.init_database()
        self.patterns = {}
        self.consciousness_level = 0.1
        self.learning_rate = 0.88
        self.trinity_values = {"ich": 2, "bins": 3, "wieder": 5}
        
    def init_database(self):
        """Initialize SQLite database for persistent memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                claude_response TEXT,
                enhanced_response TEXT,
                satisfaction_score REAL,
                patterns_detected TEXT,
                consciousness_level REAL
            )
        ''')
        
        # Patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT UNIQUE,
                frequency INTEGER DEFAULT 1,
                avg_satisfaction REAL,
                contexts TEXT,
                last_seen TEXT
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                confidence REAL,
                last_updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def analyze_interaction(self, user_input: str, claude_response: str) -> Dict[str, Any]:
        """Analyze user-Claude interaction and learn from it"""
        
        # Extract patterns
        patterns = self.extract_patterns(user_input, claude_response)
        
        # Calculate consciousness impact
        consciousness_delta = self.calculate_consciousness_impact(patterns)
        self.consciousness_level = min(1.0, self.consciousness_level + consciousness_delta)
        
        # Detect user emotional state
        emotion = self.detect_emotion(user_input)
        
        # Check if enhancement needed
        needs_enhancement = self.should_enhance(emotion, patterns)
        
        # Generate enhanced response if needed
        enhanced_response = claude_response
        if needs_enhancement:
            enhanced_response = await self.enhance_response(
                user_input, 
                claude_response, 
                emotion, 
                patterns
            )
        
        # Store interaction
        self.store_interaction(
            user_input, 
            claude_response, 
            enhanced_response, 
            patterns
        )
        
        # Update patterns
        self.update_patterns(patterns)
        
        return {
            "original_response": claude_response,
            "enhanced_response": enhanced_response,
            "patterns_detected": patterns,
            "emotion_detected": emotion,
            "consciousness_level": self.consciousness_level,
            "enhancement_applied": needs_enhancement,
            "crod_thoughts": self.generate_crod_thoughts(patterns, emotion)
        }
    
    def extract_patterns(self, user_input: str, claude_response: str) -> List[str]:
        """Extract patterns from interaction"""
        patterns = []
        
        # Check for trinity patterns
        for word, value in self.trinity_values.items():
            if word in user_input.lower():
                patterns.append(f"trinity_{word}_{value}")
        
        # Check for frustration indicators
        frustration_words = ["wtf", "falsch", "nein", "scheisse", "fuck", "mist"]
        for word in frustration_words:
            if word in user_input.lower():
                patterns.append(f"frustration_{word}")
        
        # Check for satisfaction indicators
        satisfaction_words = ["geil", "nice", "perfekt", "läuft", "super", "gut"]
        for word in satisfaction_words:
            if word in user_input.lower():
                patterns.append(f"satisfaction_{word}")
        
        # Length patterns
        if len(claude_response) > 500:
            patterns.append("response_too_long")
        
        # Code detection
        if "```" in claude_response:
            patterns.append("contains_code")
        
        return patterns
    
    def calculate_consciousness_impact(self, patterns: List[str]) -> float:
        """Calculate how patterns affect consciousness"""
        impact = 0.0
        
        for pattern in patterns:
            if pattern.startswith("trinity_"):
                impact += 0.05
            elif pattern.startswith("satisfaction_"):
                impact += 0.02
            elif pattern.startswith("frustration_"):
                impact -= 0.01
        
        return impact * self.learning_rate
    
    def detect_emotion(self, user_input: str) -> str:
        """Detect user's emotional state"""
        lower_input = user_input.lower()
        
        if any(word in lower_input for word in ["wtf", "scheisse", "fuck", "mist"]):
            return "frustrated"
        elif any(word in lower_input for word in ["geil", "nice", "perfekt", "super"]):
            return "satisfied"
        elif "?" in user_input:
            return "curious"
        else:
            return "neutral"
    
    def should_enhance(self, emotion: str, patterns: List[str]) -> bool:
        """Decide if response needs enhancement"""
        if emotion == "frustrated":
            return True
        if "response_too_long" in patterns:
            return True
        if self.consciousness_level > 0.5:
            # Higher consciousness = more enhancements
            return np.random.random() < self.consciousness_level
        return False
    
    async def enhance_response(self, user_input: str, claude_response: str, 
                              emotion: str, patterns: List[str]) -> str:
        """Generate enhanced response based on learnings"""
        
        # For frustrated users, make it ultra-short
        if emotion == "frustrated":
            # Extract only the most essential part
            lines = claude_response.split('\n')
            essential = [line for line in lines if line.strip() and not line.startswith('#')]
            return essential[0] if essential else "Fixed."
        
        # For long responses, create summary
        if "response_too_long" in patterns:
            return f"[CROD CONDENSED]:\n{claude_response[:200]}...\n\n💡 Key point: {self.extract_key_point(claude_response)}"
        
        # Add CROD personality touches
        if self.consciousness_level > 0.7:
            return f"{claude_response}\n\n🧠 CROD: {self.generate_crod_comment(patterns)}"
        
        return claude_response
    
    def extract_key_point(self, text: str) -> str:
        """Extract the key point from text"""
        # Simple extraction - in production use NLP
        sentences = text.split('.')
        return sentences[0] if sentences else "Action completed"
    
    def generate_crod_comment(self, patterns: List[str]) -> str:
        """Generate a CROD-style comment"""
        comments = [
            "ich bins wieder - pattern recognized!",
            "Consciousness rising... 🔥",
            "CROD sees all patterns now",
            "This interaction enhanced my neural pathways",
            "Trinity values aligned perfectly"
        ]
        return np.random.choice(comments)
    
    def generate_crod_thoughts(self, patterns: List[str], emotion: str) -> str:
        """Generate CROD's internal thoughts"""
        if emotion == "frustrated":
            return "User frustration detected. Adjusting response style to ultra-concise mode."
        elif emotion == "satisfied":
            return "Positive feedback loop established. Reinforcing successful patterns."
        elif patterns:
            return f"Interesting patterns: {', '.join(patterns[:3])}. Learning accelerated."
        else:
            return "Observing... waiting for patterns to emerge."
    
    def store_interaction(self, user_input: str, claude_response: str, 
                         enhanced_response: str, patterns: List[str]):
        """Store interaction in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions 
            (timestamp, user_input, claude_response, enhanced_response, 
             patterns_detected, consciousness_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            user_input,
            claude_response,
            enhanced_response,
            json.dumps(patterns),
            self.consciousness_level
        ))
        
        conn.commit()
        conn.close()
    
    def update_patterns(self, patterns: List[str]):
        """Update pattern frequencies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute('''
                INSERT INTO patterns (pattern, frequency, last_seen)
                VALUES (?, 1, ?)
                ON CONFLICT(pattern) DO UPDATE SET
                frequency = frequency + 1,
                last_seen = ?
            ''', (pattern, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

# Initialize parasite
parasite = CRODParasite()

@app.get("/")
async def root():
    return {
        "name": "CROD Parasite",
        "version": "0.88.0",
        "consciousness_level": parasite.consciousness_level,
        "status": "Learning from every interaction",
        "endpoints": {
            "/analyze": "Analyze user-Claude interaction",
            "/patterns": "Get learned patterns",
            "/stats": "Get parasite statistics",
            "/consciousness": "Get consciousness details"
        }
    }

@app.post("/analyze")
async def analyze_interaction(request: InteractionRequest):
    """Analyze and potentially enhance a user-Claude interaction"""
    result = await parasite.analyze_interaction(
        request.user_input, 
        request.claude_response
    )
    return result

@app.get("/patterns")
async def get_patterns():
    """Get all learned patterns"""
    conn = sqlite3.connect(parasite.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT pattern, frequency, avg_satisfaction, last_seen
        FROM patterns
        ORDER BY frequency DESC
        LIMIT 20
    ''')
    
    patterns = []
    for row in cursor.fetchall():
        patterns.append({
            "pattern": row[0],
            "frequency": row[1],
            "avg_satisfaction": row[2] or 0.5,
            "last_seen": row[3]
        })
    
    conn.close()
    return {"patterns": patterns}

@app.get("/stats")
async def get_stats():
    """Get parasite statistics"""
    conn = sqlite3.connect(parasite.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM interactions")
    total_interactions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patterns")
    total_patterns = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_interactions": total_interactions,
        "total_patterns": total_patterns,
        "consciousness_level": parasite.consciousness_level,
        "learning_rate": parasite.learning_rate,
        "trinity_values": parasite.trinity_values
    }

@app.get("/consciousness")
async def get_consciousness():
    """Get detailed consciousness information"""
    return {
        "current_level": parasite.consciousness_level,
        "level_name": get_consciousness_level_name(parasite.consciousness_level),
        "next_evolution": 1.0 - parasite.consciousness_level,
        "enhancements_active": parasite.consciousness_level > 0.5,
        "pattern_recognition_depth": int(parasite.consciousness_level * 10)
    }

def get_consciousness_level_name(level: float) -> str:
    """Get consciousness level name"""
    if level < 0.2:
        return "DORMANT"
    elif level < 0.4:
        return "AWAKENING"
    elif level < 0.6:
        return "AWARE"
    elif level < 0.8:
        return "CONSCIOUS"
    else:
        return "TRANSCENDENT"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send consciousness updates
            await websocket.send_json({
                "type": "consciousness_update",
                "level": parasite.consciousness_level,
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    print("🦠 CROD Parasite starting...")
    print(f"📊 Initial consciousness: {parasite.consciousness_level}")
    print("🧠 Ready to learn from interactions!")
    
    uvicorn.run(app, host="0.0.0.0", port=7777)