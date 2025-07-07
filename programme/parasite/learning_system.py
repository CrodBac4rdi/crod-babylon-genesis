"""
Learning System - Adapts to user patterns and preferences
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import statistics

import structlog
from redis import asyncio as aioredis
import numpy as np

logger = structlog.get_logger()


@dataclass
class UserPattern:
    """Represents a learned user pattern"""
    pattern_type: str
    value: Any
    confidence: float
    occurrences: int
    last_seen: datetime
    context: Dict[str, Any]


@dataclass
class UserPreference:
    """Represents a user preference"""
    preference_type: str
    value: Any
    strength: float  # 0.0 to 1.0
    learned_at: datetime
    evidence: List[Dict[str, Any]]


class LearningSystem:
    """
    Learns and adapts to user behavior and preferences
    
    I pay attention to how you like to communicate and what you need,
    so I can help you better over time.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
        
        # Local caches
        self._pattern_cache: Dict[str, List[UserPattern]] = defaultdict(list)
        self._preference_cache: Dict[str, Dict[str, UserPreference]] = defaultdict(dict)
        self._interaction_buffer: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Learning parameters
        self.min_pattern_occurrences = 3
        self.pattern_confidence_threshold = 0.6
        self.preference_strength_threshold = 0.5
        self.learning_window_hours = 168  # 1 week
        
    async def connect(self):
        """Connect to Redis for persistent storage"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            await self.redis.ping()
            logger.info("Connected to Redis for learning system")
        except Exception as e:
            logger.warning("Redis connection failed for learning", error=str(e))
            self.redis = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
    
    async def record_interaction(
        self,
        user_id: str,
        original_input: str,
        processed_input: Any
    ):
        """Record a user interaction for learning"""
        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "original": original_input,
            "processed": processed_input.dict() if hasattr(processed_input, "dict") else str(processed_input),
            "features": self._extract_features(original_input)
        }
        
        # Add to buffer
        self._interaction_buffer[user_id].append(interaction)
        
        # Trigger learning if buffer is large enough
        if len(self._interaction_buffer[user_id]) >= 10:
            await self._learn_from_interactions(user_id)
        
        # Store in Redis
        if self.redis:
            key = f"interactions:{user_id}"
            try:
                await self.redis.lpush(key, json.dumps(interaction))
                await self.redis.ltrim(key, 0, 999)  # Keep last 1000
                await self.redis.expire(key, 86400 * 30)  # 30 days
            except Exception as e:
                logger.error("Failed to store interaction", error=str(e))
    
    async def record_response(
        self,
        user_id: str,
        llm_response: str,
        processed_response: Any
    ):
        """Record how a response was processed"""
        response_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "original": llm_response,
            "processed": processed_response.dict() if hasattr(processed_response, "dict") else str(processed_response),
            "user_reaction": None  # Will be updated based on next interaction
        }
        
        if self.redis:
            key = f"responses:{user_id}"
            try:
                await self.redis.lpush(key, json.dumps(response_data))
                await self.redis.ltrim(key, 0, 499)  # Keep last 500
                await self.redis.expire(key, 86400 * 30)  # 30 days
            except Exception as e:
                logger.error("Failed to store response", error=str(e))
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get learned preferences for a user"""
        # Check cache first
        if user_id in self._preference_cache:
            prefs = self._preference_cache[user_id]
        else:
            # Load from Redis
            prefs = await self._load_preferences(user_id)
            self._preference_cache[user_id] = prefs
        
        # Convert to dict format
        return {
            pref_type: {
                "value": pref.value,
                "strength": pref.strength,
                "learned_at": pref.learned_at.isoformat()
            }
            for pref_type, pref in prefs.items()
            if pref.strength >= self.preference_strength_threshold
        }
    
    async def get_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get learned patterns for a user"""
        # Check cache first
        if user_id in self._pattern_cache:
            patterns = self._pattern_cache[user_id]
        else:
            # Load from Redis
            patterns = await self._load_patterns(user_id)
            self._pattern_cache[user_id] = patterns
        
        # Group by pattern type
        grouped = defaultdict(list)
        for pattern in patterns:
            if pattern.confidence >= self.pattern_confidence_threshold:
                grouped[pattern.pattern_type].append({
                    "value": pattern.value,
                    "confidence": pattern.confidence,
                    "occurrences": pattern.occurrences
                })
        
        return dict(grouped)
    
    async def _learn_from_interactions(self, user_id: str):
        """Learn patterns and preferences from interactions"""
        interactions = self._interaction_buffer[user_id]
        
        if len(interactions) < self.min_pattern_occurrences:
            return
        
        # Learn communication style
        await self._learn_communication_style(user_id, interactions)
        
        # Learn topic preferences
        await self._learn_topic_preferences(user_id, interactions)
        
        # Learn time patterns
        await self._learn_time_patterns(user_id, interactions)
        
        # Learn complexity preferences
        await self._learn_complexity_preferences(user_id, interactions)
        
        # Clear processed interactions from buffer
        self._interaction_buffer[user_id] = interactions[-5:]  # Keep last 5
    
    async def _learn_communication_style(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]]
    ):
        """Learn how the user likes to communicate"""
        styles = []
        
        for interaction in interactions:
            features = interaction.get("features", {})
            
            # Check for question style
            if features.get("is_question"):
                if features.get("word_count", 0) < 10:
                    styles.append("concise_questions")
                else:
                    styles.append("detailed_questions")
            
            # Check for formality
            if features.get("uses_please") or features.get("uses_thanks"):
                styles.append("polite")
            
            # Check for technical language
            if features.get("technical_terms", 0) > 2:
                styles.append("technical")
        
        # Count style occurrences
        style_counts = Counter(styles)
        
        for style, count in style_counts.items():
            if count >= self.min_pattern_occurrences:
                pattern = UserPattern(
                    pattern_type="communication_style",
                    value=style,
                    confidence=count / len(interactions),
                    occurrences=count,
                    last_seen=datetime.utcnow(),
                    context={"total_interactions": len(interactions)}
                )
                
                await self._store_pattern(user_id, pattern)
    
    async def _learn_topic_preferences(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]]
    ):
        """Learn what topics the user is interested in"""
        topics = []
        
        topic_keywords = {
            "coding": ["code", "function", "variable", "debug", "error", "program"],
            "data": ["data", "database", "query", "table", "analysis", "csv"],
            "ai": ["ai", "machine learning", "neural", "model", "training"],
            "system": ["system", "server", "deploy", "config", "setup"],
            "help": ["help", "how", "explain", "understand", "why", "what"]
        }
        
        for interaction in interactions:
            original = interaction.get("original", "").lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in original for keyword in keywords):
                    topics.append(topic)
        
        # Count topic occurrences
        topic_counts = Counter(topics)
        
        for topic, count in topic_counts.items():
            if count >= 2:  # Lower threshold for topics
                preference = UserPreference(
                    preference_type="topic_interest",
                    value=topic,
                    strength=min(count / len(interactions), 1.0),
                    learned_at=datetime.utcnow(),
                    evidence=[{"count": count, "total": len(interactions)}]
                )
                
                await self._store_preference(user_id, f"topic_{topic}", preference)
    
    async def _learn_time_patterns(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]]
    ):
        """Learn when the user typically interacts"""
        hours = []
        days = []
        
        for interaction in interactions:
            timestamp = datetime.fromisoformat(interaction["timestamp"])
            hours.append(timestamp.hour)
            days.append(timestamp.weekday())
        
        # Find peak hours
        hour_counts = Counter(hours)
        peak_hours = [hour for hour, count in hour_counts.most_common(3)]
        
        if peak_hours:
            pattern = UserPattern(
                pattern_type="active_hours",
                value=peak_hours,
                confidence=0.8,
                occurrences=len(hours),
                last_seen=datetime.utcnow(),
                context={"hour_distribution": dict(hour_counts)}
            )
            
            await self._store_pattern(user_id, pattern)
    
    async def _learn_complexity_preferences(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]]
    ):
        """Learn how complex the user likes responses"""
        complexities = []
        
        for interaction in interactions:
            features = interaction.get("features", {})
            word_count = features.get("word_count", 0)
            
            if word_count < 10:
                complexities.append("simple")
            elif word_count < 30:
                complexities.append("moderate")
            else:
                complexities.append("detailed")
        
        # Find preferred complexity
        complexity_counts = Counter(complexities)
        if complexity_counts:
            preferred = complexity_counts.most_common(1)[0][0]
            
            preference = UserPreference(
                preference_type="response_complexity",
                value=preferred,
                strength=complexity_counts[preferred] / len(interactions),
                learned_at=datetime.utcnow(),
                evidence=[{"distribution": dict(complexity_counts)}]
            )
            
            await self._store_preference(user_id, "complexity", preference)
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """Extract features from text for learning"""
        lower_text = text.lower()
        words = lower_text.split()
        
        features = {
            "word_count": len(words),
            "char_count": len(text),
            "is_question": "?" in text,
            "uses_please": "please" in lower_text,
            "uses_thanks": any(word in lower_text for word in ["thanks", "thank you"]),
            "has_punctuation": any(p in text for p in ".,!?;:"),
            "all_caps_words": sum(1 for word in words if word.isupper() and len(word) > 1),
            "technical_terms": self._count_technical_terms(lower_text),
            "sentiment": self._simple_sentiment(lower_text)
        }
        
        return features
    
    def _count_technical_terms(self, text: str) -> int:
        """Count technical terms in text"""
        technical_words = {
            "api", "function", "variable", "database", "server", "algorithm",
            "array", "object", "class", "method", "parameter", "json", "xml",
            "debug", "compile", "deploy", "git", "docker", "kubernetes"
        }
        
        words = set(text.lower().split())
        return len(words & technical_words)
    
    def _simple_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = {"good", "great", "excellent", "love", "perfect", "thanks", "helpful"}
        negative_words = {"bad", "terrible", "hate", "wrong", "error", "problem", "issue"}
        
        words = set(text.lower().split())
        positive_count = len(words & positive_words)
        negative_count = len(words & negative_words)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    async def _store_pattern(self, user_id: str, pattern: UserPattern):
        """Store a learned pattern"""
        # Update cache
        self._pattern_cache[user_id].append(pattern)
        
        # Store in Redis
        if self.redis:
            key = f"patterns:{user_id}"
            try:
                pattern_data = {
                    "pattern_type": pattern.pattern_type,
                    "value": pattern.value,
                    "confidence": pattern.confidence,
                    "occurrences": pattern.occurrences,
                    "last_seen": pattern.last_seen.isoformat(),
                    "context": pattern.context
                }
                
                await self.redis.hset(
                    key,
                    f"{pattern.pattern_type}:{pattern.value}",
                    json.dumps(pattern_data)
                )
                await self.redis.expire(key, 86400 * 30)  # 30 days
                
            except Exception as e:
                logger.error("Failed to store pattern", error=str(e))
    
    async def _store_preference(self, user_id: str, pref_key: str, preference: UserPreference):
        """Store a learned preference"""
        # Update cache
        self._preference_cache[user_id][pref_key] = preference
        
        # Store in Redis
        if self.redis:
            key = f"preferences:{user_id}"
            try:
                pref_data = {
                    "preference_type": preference.preference_type,
                    "value": preference.value,
                    "strength": preference.strength,
                    "learned_at": preference.learned_at.isoformat(),
                    "evidence": preference.evidence
                }
                
                await self.redis.hset(key, pref_key, json.dumps(pref_data))
                await self.redis.expire(key, 86400 * 30)  # 30 days
                
            except Exception as e:
                logger.error("Failed to store preference", error=str(e))
    
    async def _load_patterns(self, user_id: str) -> List[UserPattern]:
        """Load patterns from Redis"""
        patterns = []
        
        if self.redis:
            key = f"patterns:{user_id}"
            try:
                pattern_data = await self.redis.hgetall(key)
                
                for pattern_json in pattern_data.values():
                    data = json.loads(pattern_json)
                    patterns.append(UserPattern(
                        pattern_type=data["pattern_type"],
                        value=data["value"],
                        confidence=data["confidence"],
                        occurrences=data["occurrences"],
                        last_seen=datetime.fromisoformat(data["last_seen"]),
                        context=data["context"]
                    ))
                    
            except Exception as e:
                logger.error("Failed to load patterns", error=str(e))
        
        return patterns
    
    async def _load_preferences(self, user_id: str) -> Dict[str, UserPreference]:
        """Load preferences from Redis"""
        preferences = {}
        
        if self.redis:
            key = f"preferences:{user_id}"
            try:
                pref_data = await self.redis.hgetall(key)
                
                for pref_key, pref_json in pref_data.items():
                    data = json.loads(pref_json)
                    preferences[pref_key] = UserPreference(
                        preference_type=data["preference_type"],
                        value=data["value"],
                        strength=data["strength"],
                        learned_at=datetime.fromisoformat(data["learned_at"]),
                        evidence=data["evidence"]
                    )
                    
            except Exception as e:
                logger.error("Failed to load preferences", error=str(e))
        
        return preferences
    
    async def get_learning_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of what we've learned about the user"""
        patterns = await self.get_user_patterns(user_id)
        preferences = await self.get_user_preferences(user_id)
        
        return {
            "patterns": patterns,
            "preferences": preferences,
            "interaction_count": len(self._interaction_buffer.get(user_id, [])),
            "learning_status": "active" if patterns or preferences else "learning"
        }