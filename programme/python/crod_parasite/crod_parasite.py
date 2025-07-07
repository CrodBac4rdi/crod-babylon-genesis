"""
CROD Parasite - The Bridge Between Humans and LLMs
A friendly intermediary that understands, translates, and enhances communication
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from enum import Enum
import re

import structlog
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from .context_manager import ContextManager
from .llm_adapter import LLMAdapter
from .permission_client import PermissionClient
from .learning_system import LearningSystem
from .personality import ParasitePersonality

logger = structlog.get_logger()


class IntentType(Enum):
    """Types of user intents the parasite can recognize"""
    QUERY = "query"
    COMMAND = "command"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    CONVERSATION = "conversation"
    SYSTEM_CONTROL = "system_control"
    EXPLANATION_REQUEST = "explanation_request"


class CommunicationMode(Enum):
    """How the parasite should communicate"""
    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    EDUCATIONAL = "educational"
    CONCISE = "concise"
    VERBOSE = "verbose"


class Message(BaseModel):
    """Structured message format"""
    content: str
    intent: Optional[IntentType] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CRODParasite:
    """
    The CROD Parasite - Your friendly AI communication bridge
    
    I'm here to help you communicate with complex AI systems in a way that
    makes sense to both of you. Think of me as your helpful translator and
    guardian who ensures nothing gets lost in translation.
    """
    
    def __init__(
        self,
        context_manager: ContextManager,
        llm_adapter: LLMAdapter,
        permission_client: PermissionClient,
        learning_system: LearningSystem,
        personality: Optional[ParasitePersonality] = None
    ):
        self.context = context_manager
        self.llm = llm_adapter
        self.permissions = permission_client
        self.learner = learning_system
        self.personality = personality or ParasitePersonality()
        
        # Internal state
        self._communication_mode = CommunicationMode.FRIENDLY
        self._active_conversations: Dict[str, List[Message]] = {}
        self._user_preferences: Dict[str, Any] = {}
        
        logger.info("CROD Parasite initialized", 
                   personality=self.personality.name,
                   mode=self._communication_mode.value)
    
    async def process_human_input(
        self, 
        user_id: str, 
        input_text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process input from a human user
        
        This is where the magic happens - I take what you said and figure out
        what you really meant, then prepare it for the AI systems.
        """
        logger.info("Processing human input", user_id=user_id)
        
        # Analyze the input
        intent = await self._analyze_intent(input_text)
        enhanced_input = await self._enhance_human_input(input_text, intent, context)
        
        # Check permissions
        if intent.intent == IntentType.SYSTEM_CONTROL:
            allowed = await self.permissions.check_permission(
                user_id, "system_control", enhanced_input.metadata
            )
            if not allowed:
                return self._create_friendly_denial(user_id, intent)
        
        # Update context
        await self.context.add_message(user_id, "human", enhanced_input)
        
        # Learn from the interaction
        await self.learner.record_interaction(user_id, input_text, enhanced_input)
        
        # Prepare for LLM
        llm_ready = await self._prepare_for_llm(enhanced_input, user_id)
        
        return {
            "original": input_text,
            "interpreted": enhanced_input.content,
            "intent": intent.intent.value,
            "confidence": intent.confidence,
            "llm_ready": llm_ready,
            "parasite_notes": self._get_helpful_notes(intent)
        }
    
    async def process_llm_response(
        self,
        user_id: str,
        llm_response: str,
        original_intent: IntentType,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process response from an LLM and make it human-friendly
        
        I take the AI's response and translate it into something that makes
        sense for you, adding helpful context and explanations where needed.
        """
        logger.info("Processing LLM response", user_id=user_id)
        
        # Parse and understand the response
        parsed = await self._parse_llm_response(llm_response)
        
        # Translate to human-friendly format
        human_friendly = await self._humanize_response(
            parsed, original_intent, self._communication_mode
        )
        
        # Add helpful context
        enriched = await self._enrich_response(human_friendly, user_id, context)
        
        # Update context
        await self.context.add_message(user_id, "assistant", enriched)
        
        # Learn from the response
        await self.learner.record_response(user_id, llm_response, enriched)
        
        return {
            "original": llm_response,
            "humanized": enriched.content,
            "explanation": self._generate_explanation(parsed, original_intent),
            "suggestions": await self._generate_suggestions(user_id, enriched),
            "confidence": enriched.confidence,
            "parasite_commentary": self.personality.add_commentary(enriched)
        }
    
    async def _analyze_intent(self, text: str) -> Message:
        """Analyze user intent from their input"""
        # Simple pattern matching for now, can be enhanced with NLP
        patterns = {
            IntentType.COMMAND: [
                r"^(do|make|create|build|run|execute|start|stop)",
                r"(please|could you|can you).*(do|make|create|build)"
            ],
            IntentType.QUERY: [
                r"^(what|how|why|when|where|who|which)",
                r"(tell me|explain|show me)"
            ],
            IntentType.CONFIRMATION: [
                r"^(yes|no|confirm|cancel|proceed|abort)",
                r"(that's right|correct|wrong)"
            ],
            IntentType.EXPLANATION_REQUEST: [
                r"(explain|clarify|what does.*mean|I don't understand)",
                r"(break.*down|elaborate|more detail)"
            ]
        }
        
        intent_type = IntentType.CONVERSATION  # default
        confidence = 0.7
        
        lower_text = text.lower().strip()
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, lower_text, re.IGNORECASE):
                    intent_type = intent
                    confidence = 0.9
                    break
        
        return Message(
            content=text,
            intent=intent_type,
            confidence=confidence,
            metadata={"analyzed_at": datetime.utcnow().isoformat()}
        )
    
    async def _enhance_human_input(
        self, 
        text: str, 
        intent: Message,
        context: Optional[Dict[str, Any]]
    ) -> Message:
        """Enhance human input with context and clarifications"""
        enhanced = text
        
        # Add context from conversation history
        if context:
            relevant_context = await self.context.get_relevant_context(
                context.get("user_id"), text
            )
            if relevant_context:
                enhanced = f"{text}\n[Context: {relevant_context}]"
        
        # Fix common ambiguities
        ambiguity_fixes = {
            "it": await self._resolve_pronoun("it", context),
            "that": await self._resolve_pronoun("that", context),
            "this": await self._resolve_pronoun("this", context)
        }
        
        for pronoun, resolution in ambiguity_fixes.items():
            if pronoun in text.lower() and resolution:
                enhanced = enhanced.replace(pronoun, f"{pronoun} ({resolution})")
        
        return Message(
            content=enhanced,
            intent=intent.intent,
            confidence=intent.confidence,
            metadata={
                **intent.metadata,
                "enhanced": True,
                "original": text
            }
        )
    
    async def _prepare_for_llm(self, message: Message, user_id: str) -> Dict[str, Any]:
        """Prepare the message for LLM consumption"""
        # Get user preferences
        preferences = await self.learner.get_user_preferences(user_id)
        
        # Structure for LLM
        return {
            "messages": [
                {
                    "role": "system",
                    "content": self._generate_system_prompt(message.intent, preferences)
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            "temperature": self._get_temperature_for_intent(message.intent),
            "max_tokens": self._get_max_tokens_for_intent(message.intent),
            "metadata": {
                "user_id": user_id,
                "intent": message.intent.value,
                "preferences": preferences
            }
        }
    
    async def _humanize_response(
        self,
        parsed_response: Dict[str, Any],
        original_intent: IntentType,
        mode: CommunicationMode
    ) -> Message:
        """Convert LLM response to human-friendly format"""
        content = parsed_response.get("content", "")
        
        if mode == CommunicationMode.FRIENDLY:
            # Add friendly touches
            content = self.personality.make_friendly(content)
            
        elif mode == CommunicationMode.EDUCATIONAL:
            # Add explanations
            content = await self._add_educational_context(content, original_intent)
            
        elif mode == CommunicationMode.CONCISE:
            # Simplify and shorten
            content = self._make_concise(content)
        
        return Message(
            content=content,
            intent=original_intent,
            confidence=parsed_response.get("confidence", 1.0),
            metadata=parsed_response.get("metadata", {})
        )
    
    def _create_friendly_denial(self, user_id: str, intent: Message) -> Dict[str, Any]:
        """Create a friendly permission denial message"""
        return {
            "success": False,
            "message": self.personality.create_denial_message(),
            "suggestion": "Perhaps we could try a different approach?",
            "intent": intent.intent.value,
            "help": "I can help you with queries, explanations, and many other tasks!"
        }
    
    def _get_helpful_notes(self, intent: Message) -> str:
        """Generate helpful notes based on the intent"""
        notes = {
            IntentType.COMMAND: "I'll help execute this safely and explain what happens.",
            IntentType.QUERY: "Let me find the best answer for you.",
            IntentType.EXPLANATION_REQUEST: "I'll break this down in a way that makes sense.",
            IntentType.CONFIRMATION: "Got it! Let me confirm that for you.",
            IntentType.CONVERSATION: "I'm here to chat and help however I can!",
            IntentType.SYSTEM_CONTROL: "This requires special permissions. Let me check...",
            IntentType.CLARIFICATION: "Let me help clarify this for you."
        }
        return notes.get(intent.intent, "I'm processing your request...")
    
    async def _generate_suggestions(self, user_id: str, response: Message) -> List[str]:
        """Generate helpful follow-up suggestions"""
        # Learn from user patterns
        patterns = await self.learner.get_user_patterns(user_id)
        
        suggestions = []
        
        # Base suggestions on intent and response
        if response.intent == IntentType.QUERY:
            suggestions.extend([
                "Would you like more details?",
                "Should I explain any technical terms?",
                "Want to see some examples?"
            ])
        elif response.intent == IntentType.COMMAND:
            suggestions.extend([
                "Shall I proceed with this action?",
                "Would you like to see what will happen first?",
                "Need me to explain the process?"
            ])
        
        # Personalize based on patterns
        if patterns.get("prefers_examples", False):
            suggestions.append("I can show you some examples if that helps!")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _generate_system_prompt(self, intent: IntentType, preferences: Dict[str, Any]) -> str:
        """Generate appropriate system prompt for the LLM"""
        base_prompt = "You are a helpful AI assistant working with the CROD system."
        
        intent_prompts = {
            IntentType.COMMAND: "Execute commands safely and explain each step.",
            IntentType.QUERY: "Provide clear, accurate answers with examples when helpful.",
            IntentType.EXPLANATION_REQUEST: "Break down complex topics into understandable parts.",
            IntentType.SYSTEM_CONTROL: "Handle system operations with care and confirm before proceeding."
        }
        
        prompt = f"{base_prompt} {intent_prompts.get(intent, '')}"
        
        # Add user preferences
        if preferences.get("technical_level") == "beginner":
            prompt += " Avoid jargon and explain technical terms."
        elif preferences.get("technical_level") == "expert":
            prompt += " You can use technical terminology freely."
        
        return prompt
    
    def _get_temperature_for_intent(self, intent: IntentType) -> float:
        """Get appropriate temperature setting for the intent"""
        temperatures = {
            IntentType.COMMAND: 0.3,  # More deterministic for commands
            IntentType.QUERY: 0.7,    # Balanced for queries
            IntentType.CONVERSATION: 0.8,  # More creative for conversation
            IntentType.EXPLANATION_REQUEST: 0.6,  # Clear but not too rigid
            IntentType.SYSTEM_CONTROL: 0.2,  # Very deterministic for system ops
        }
        return temperatures.get(intent, 0.7)
    
    def _get_max_tokens_for_intent(self, intent: IntentType) -> int:
        """Get appropriate max tokens for the intent"""
        max_tokens = {
            IntentType.COMMAND: 500,
            IntentType.QUERY: 1000,
            IntentType.CONVERSATION: 800,
            IntentType.EXPLANATION_REQUEST: 1500,
            IntentType.SYSTEM_CONTROL: 300,
        }
        return max_tokens.get(intent, 800)
    
    async def _resolve_pronoun(self, pronoun: str, context: Optional[Dict[str, Any]]) -> Optional[str]:
        """Resolve pronouns to their referents"""
        if not context:
            return None
            
        # Simple resolution based on recent context
        recent_entities = context.get("recent_entities", [])
        if recent_entities:
            return recent_entities[0]  # Most recent entity
        
        return None
    
    async def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse and structure LLM response"""
        # Try to extract JSON if present
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                return {
                    "content": response,
                    "structured": parsed,
                    "confidence": 0.9
                }
            except json.JSONDecodeError:
                pass
        
        # Otherwise return as plain content
        return {
            "content": response,
            "structured": None,
            "confidence": 0.8
        }
    
    async def _add_educational_context(self, content: str, intent: IntentType) -> str:
        """Add educational context to responses"""
        educational_additions = []
        
        # Find technical terms and add explanations
        technical_terms = self._find_technical_terms(content)
        if technical_terms:
            educational_additions.append(
                "\n\n📚 Quick explanations:\n" + 
                "\n".join([f"• {term}: {self._get_simple_explanation(term)}" 
                          for term in technical_terms[:3]])
            )
        
        return content + "".join(educational_additions)
    
    def _make_concise(self, content: str) -> str:
        """Make response more concise"""
        # Remove redundant phrases
        concise = re.sub(r'(In other words|To put it simply|Basically)', '', content)
        
        # Shorten sentences
        sentences = concise.split('. ')
        if len(sentences) > 5:
            # Keep most important sentences
            concise = '. '.join(sentences[:5]) + '.'
        
        return concise.strip()
    
    def _find_technical_terms(self, text: str) -> List[str]:
        """Find technical terms in text"""
        # Simple pattern matching for now
        technical_patterns = [
            r'\b(API|SDK|LLM|ML|AI|GPU|CPU|RAM|JSON|XML|SQL)\b',
            r'\b(algorithm|neural network|machine learning|deep learning)\b',
            r'\b(server|client|database|cache|queue)\b'
        ]
        
        terms = set()
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.update(matches)
        
        return list(terms)
    
    def _get_simple_explanation(self, term: str) -> str:
        """Get simple explanation for technical terms"""
        explanations = {
            "API": "A way for different programs to talk to each other",
            "LLM": "Large Language Model - the AI brain that understands and generates text",
            "JSON": "A simple format for organizing data that computers can read",
            "algorithm": "A step-by-step recipe for solving a problem",
            "neural network": "Computer system inspired by how brains work",
            # Add more as needed
        }
        return explanations.get(term.upper(), f"A technical concept in computing")
    
    def _generate_explanation(self, parsed: Dict[str, Any], intent: IntentType) -> str:
        """Generate explanation of what happened"""
        if intent == IntentType.COMMAND:
            return "I've translated your command and the system has processed it."
        elif intent == IntentType.QUERY:
            return "I've found the information you were looking for."
        elif intent == IntentType.EXPLANATION_REQUEST:
            return "I've broken this down to make it clearer."
        else:
            return "I've processed your request and here's the result."
    
    async def set_communication_mode(self, mode: CommunicationMode):
        """Change how the parasite communicates"""
        self._communication_mode = mode
        logger.info("Communication mode changed", mode=mode.value)
    
    async def get_conversation_summary(self, user_id: str) -> str:
        """Get a summary of the conversation"""
        messages = await self.context.get_recent_messages(user_id, limit=10)
        
        if not messages:
            return "We haven't talked yet! Feel free to ask me anything."
        
        # Create a friendly summary
        summary = f"Here's what we've discussed:\n"
        topics = self._extract_topics(messages)
        
        for i, topic in enumerate(topics, 1):
            summary += f"{i}. {topic}\n"
        
        summary += f"\n{self.personality.add_summary_flavor()}"
        
        return summary
    
    def _extract_topics(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract main topics from messages"""
        topics = []
        
        for msg in messages:
            if msg.get("intent") == IntentType.QUERY.value:
                topics.append(f"You asked about: {msg.get('summary', 'something')}")
            elif msg.get("intent") == IntentType.COMMAND.value:
                topics.append(f"We executed: {msg.get('summary', 'a command')}")
            elif msg.get("intent") == IntentType.EXPLANATION_REQUEST.value:
                topics.append(f"I explained: {msg.get('summary', 'a concept')}")
        
        return topics[:5]  # Limit to 5 most recent topics