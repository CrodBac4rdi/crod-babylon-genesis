"""
Context Manager - Maintains conversation state and history
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque

import structlog
from redis import asyncio as aioredis

logger = structlog.get_logger()


class ContextManager:
    """
    Manages conversation context and state across sessions
    
    I keep track of what we've talked about, so our conversations
    feel natural and continuous.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
        self.local_cache: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.context_window = 10  # Number of recent messages to consider
        
    async def connect(self):
        """Connect to Redis for persistent storage"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            await self.redis.ping()
            logger.info("Connected to Redis for context management")
        except Exception as e:
            logger.warning("Redis connection failed, using local cache only", error=str(e))
            self.redis = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
    
    async def add_message(
        self, 
        user_id: str, 
        role: str, 
        message: Any,
        ttl: int = 86400  # 24 hours default
    ):
        """Add a message to the conversation history"""
        entry = {
            "role": role,
            "content": message.content if hasattr(message, "content") else str(message),
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": getattr(message, "metadata", {})
        }
        
        # Add to local cache
        self.local_cache[user_id].append(entry)
        
        # Add to Redis if available
        if self.redis:
            key = f"context:{user_id}"
            try:
                # Get existing messages
                existing = await self.redis.get(key)
                messages = json.loads(existing) if existing else []
                
                # Add new message and limit size
                messages.append(entry)
                messages = messages[-50:]  # Keep last 50 messages
                
                # Save back to Redis
                await self.redis.setex(key, ttl, json.dumps(messages))
                
            except Exception as e:
                logger.error("Failed to save context to Redis", error=str(e))
    
    async def get_recent_messages(
        self, 
        user_id: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent messages for a user"""
        # Try Redis first
        if self.redis:
            try:
                key = f"context:{user_id}"
                data = await self.redis.get(key)
                if data:
                    messages = json.loads(data)
                    return messages[-limit:]
            except Exception as e:
                logger.error("Failed to get context from Redis", error=str(e))
        
        # Fall back to local cache
        messages = list(self.local_cache[user_id])
        return messages[-limit:]
    
    async def get_relevant_context(
        self, 
        user_id: str, 
        current_input: str
    ) -> Optional[str]:
        """Get relevant context for the current input"""
        messages = await self.get_recent_messages(user_id, self.context_window)
        
        if not messages:
            return None
        
        # Extract relevant information
        relevant_parts = []
        
        # Look for recent entities, topics, and commands
        for msg in messages[-5:]:  # Last 5 messages
            content = msg.get("content", "")
            
            # Extract potential entities (simple approach)
            if any(word in content.lower() for word in ["file", "function", "variable", "system"]):
                relevant_parts.append(f"Previously discussed: {content[:100]}...")
        
        # Look for unresolved questions
        for msg in messages:
            if msg.get("role") == "human" and "?" in msg.get("content", ""):
                # Check if this question was answered
                relevant_parts.append(f"Earlier question: {msg['content'][:100]}...")
        
        return " | ".join(relevant_parts[:3]) if relevant_parts else None
    
    async def get_user_state(self, user_id: str) -> Dict[str, Any]:
        """Get current state for a user"""
        state_key = f"state:{user_id}"
        
        if self.redis:
            try:
                data = await self.redis.get(state_key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error("Failed to get user state", error=str(e))
        
        # Default state
        return {
            "active": True,
            "last_seen": datetime.utcnow().isoformat(),
            "preferences": {},
            "current_task": None
        }
    
    async def set_user_state(self, user_id: str, state: Dict[str, Any]):
        """Update user state"""
        state_key = f"state:{user_id}"
        state["last_updated"] = datetime.utcnow().isoformat()
        
        if self.redis:
            try:
                await self.redis.setex(state_key, 86400, json.dumps(state))
            except Exception as e:
                logger.error("Failed to save user state", error=str(e))
    
    async def get_conversation_topics(self, user_id: str) -> List[str]:
        """Extract main topics from conversation"""
        messages = await self.get_recent_messages(user_id, 20)
        
        topics = []
        topic_keywords = {
            "technical": ["code", "function", "api", "system", "error", "debug"],
            "data": ["database", "query", "data", "table", "record"],
            "help": ["how", "what", "why", "explain", "help"],
            "action": ["create", "update", "delete", "run", "execute"]
        }
        
        for msg in messages:
            content = msg.get("content", "").lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in content for keyword in keywords):
                    if topic not in topics:
                        topics.append(topic)
        
        return topics
    
    async def clear_context(self, user_id: str):
        """Clear conversation context for a user"""
        # Clear local cache
        if user_id in self.local_cache:
            self.local_cache[user_id].clear()
        
        # Clear from Redis
        if self.redis:
            try:
                await self.redis.delete(f"context:{user_id}")
                await self.redis.delete(f"state:{user_id}")
            except Exception as e:
                logger.error("Failed to clear context from Redis", error=str(e))
    
    async def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation context"""
        messages = await self.get_recent_messages(user_id, 20)
        topics = await self.get_conversation_topics(user_id)
        state = await self.get_user_state(user_id)
        
        # Count message types
        message_counts = defaultdict(int)
        for msg in messages:
            message_counts[msg.get("role", "unknown")] += 1
        
        # Find time span
        if messages:
            first_time = datetime.fromisoformat(messages[0]["timestamp"])
            last_time = datetime.fromisoformat(messages[-1]["timestamp"])
            duration = last_time - first_time
        else:
            duration = timedelta(0)
        
        return {
            "message_count": len(messages),
            "message_types": dict(message_counts),
            "topics": topics,
            "duration_minutes": int(duration.total_seconds() / 60),
            "current_state": state,
            "last_activity": messages[-1]["timestamp"] if messages else None
        }
    
    async def find_similar_conversations(
        self, 
        user_id: str, 
        current_topic: str
    ) -> List[Dict[str, Any]]:
        """Find similar past conversations (simplified version)"""
        # In a real implementation, this would use vector similarity
        # For now, just return recent conversations with similar keywords
        
        messages = await self.get_recent_messages(user_id, 50)
        similar = []
        
        topic_words = set(current_topic.lower().split())
        
        for i, msg in enumerate(messages):
            content_words = set(msg.get("content", "").lower().split())
            overlap = len(topic_words & content_words)
            
            if overlap > 2:  # At least 2 words in common
                similar.append({
                    "message": msg,
                    "similarity": overlap / len(topic_words),
                    "index": i
                })
        
        # Sort by similarity
        similar.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similar[:5]  # Top 5 similar messages