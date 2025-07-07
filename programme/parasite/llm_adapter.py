"""
LLM Adapter - Unified interface for multiple AI providers
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod
from enum import Enum

import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx

# LLM provider imports
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

logger = structlog.get_logger()


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"  # For local models
    MOCK = "mock"    # For testing


class LLMResponse:
    """Standardized LLM response"""
    def __init__(
        self,
        content: str,
        provider: LLMProvider,
        model: str,
        usage: Optional[Dict[str, int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.content = content
        self.provider = provider
        self.model = model
        self.usage = usage or {}
        self.metadata = metadata or {}


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the provider is available"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        if not openai:
            raise ImportError("openai package not installed")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate response using OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                provider=LLMProvider.OPENAI,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except Exception as e:
            logger.error("OpenAI generation failed", error=str(e))
            raise
    
    async def is_available(self) -> bool:
        """Check if OpenAI is available"""
        try:
            # Simple test request
            await self.client.models.list()
            return True
        except Exception:
            return False


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        if not anthropic:
            raise ImportError("anthropic package not installed")
        
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate response using Anthropic Claude"""
        try:
            # Convert messages to Anthropic format
            system_message = None
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = await self.client.messages.create(
                model=self.model,
                messages=user_messages,
                system=system_message,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return LLMResponse(
                content=response.content[0].text,
                provider=LLMProvider.ANTHROPIC,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            )
        except Exception as e:
            logger.error("Anthropic generation failed", error=str(e))
            raise
    
    async def is_available(self) -> bool:
        """Check if Anthropic is available"""
        try:
            # Simple test - we can't list models, so just return True if client exists
            return self.client is not None
        except Exception:
            return False


class LocalProvider(BaseLLMProvider):
    """Local model provider (e.g., Ollama, llama.cpp)"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient()
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate response using local model"""
        try:
            # Format for Ollama API
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=30.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            return LLMResponse(
                content=data["response"],
                provider=LLMProvider.LOCAL,
                model=self.model,
                metadata={"eval_count": data.get("eval_count", 0)}
            )
        except Exception as e:
            logger.error("Local model generation failed", error=str(e))
            raise
    
    async def is_available(self) -> bool:
        """Check if local model is available"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.client.aclose()


class MockProvider(BaseLLMProvider):
    """Mock provider for testing"""
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate mock response"""
        user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        # Simple mock responses
        if "hello" in user_message.lower():
            content = "Hello! I'm the CROD Parasite's mock LLM. How can I help you today?"
        elif "explain" in user_message.lower():
            content = "I'd be happy to explain that! [Mock explanation would go here]"
        else:
            content = f"I received your message: '{user_message}'. This is a mock response."
        
        return LLMResponse(
            content=content,
            provider=LLMProvider.MOCK,
            model="mock-model",
            usage={"total_tokens": len(content.split())}
        )
    
    async def is_available(self) -> bool:
        """Mock provider is always available"""
        return True


class LLMAdapter:
    """
    Unified adapter for multiple LLM providers
    
    I handle the complexity of talking to different AI systems,
    so you don't have to worry about the details.
    """
    
    def __init__(self):
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self.primary_provider: Optional[LLMProvider] = None
        self.fallback_order: List[LLMProvider] = []
        
        # Usage tracking
        self.usage_stats: Dict[LLMProvider, Dict[str, int]] = {}
        
        logger.info("LLM Adapter initialized")
    
    def add_provider(
        self,
        provider_type: LLMProvider,
        provider_instance: BaseLLMProvider,
        is_primary: bool = False
    ):
        """Add a provider to the adapter"""
        self.providers[provider_type] = provider_instance
        
        if is_primary:
            self.primary_provider = provider_type
        
        # Update fallback order
        if provider_type not in self.fallback_order:
            self.fallback_order.append(provider_type)
        
        # Initialize usage stats
        self.usage_stats[provider_type] = {
            "requests": 0,
            "tokens": 0,
            "errors": 0
        }
        
        logger.info("Added LLM provider", provider=provider_type.value, is_primary=is_primary)
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using available providers
        
        Will try primary provider first, then fallbacks if needed.
        """
        # Determine which provider to use
        if provider and provider in self.providers:
            providers_to_try = [provider]
        elif self.primary_provider:
            providers_to_try = [self.primary_provider] + [
                p for p in self.fallback_order if p != self.primary_provider
            ]
        else:
            providers_to_try = self.fallback_order
        
        last_error = None
        
        # Try each provider
        for provider_type in providers_to_try:
            provider_instance = self.providers.get(provider_type)
            if not provider_instance:
                continue
            
            try:
                # Check availability
                if not await provider_instance.is_available():
                    logger.warning("Provider not available", provider=provider_type.value)
                    continue
                
                # Generate response
                response = await provider_instance.generate(
                    messages, temperature, max_tokens, **kwargs
                )
                
                # Update stats
                self.usage_stats[provider_type]["requests"] += 1
                self.usage_stats[provider_type]["tokens"] += response.usage.get("total_tokens", 0)
                
                logger.info(
                    "Generated response",
                    provider=provider_type.value,
                    tokens=response.usage.get("total_tokens", 0)
                )
                
                return response
                
            except Exception as e:
                last_error = e
                self.usage_stats[provider_type]["errors"] += 1
                logger.error(
                    "Provider failed",
                    provider=provider_type.value,
                    error=str(e)
                )
        
        # All providers failed
        raise Exception(f"All LLM providers failed. Last error: {last_error}")
    
    async def get_available_providers(self) -> List[LLMProvider]:
        """Get list of available providers"""
        available = []
        
        for provider_type, provider_instance in self.providers.items():
            if await provider_instance.is_available():
                available.append(provider_type)
        
        return available
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for all providers"""
        return {
            "providers": {
                provider.value: stats
                for provider, stats in self.usage_stats.items()
            },
            "total_requests": sum(s["requests"] for s in self.usage_stats.values()),
            "total_tokens": sum(s["tokens"] for s in self.usage_stats.values()),
            "total_errors": sum(s["errors"] for s in self.usage_stats.values())
        }
    
    @classmethod
    def create_with_defaults(cls, config: Dict[str, Any]) -> "LLMAdapter":
        """Create adapter with default configuration"""
        adapter = cls()
        
        # Add OpenAI if configured
        if config.get("openai_api_key"):
            adapter.add_provider(
                LLMProvider.OPENAI,
                OpenAIProvider(
                    api_key=config["openai_api_key"],
                    model=config.get("openai_model", "gpt-4")
                ),
                is_primary=config.get("primary_provider") == "openai"
            )
        
        # Add Anthropic if configured
        if config.get("anthropic_api_key"):
            adapter.add_provider(
                LLMProvider.ANTHROPIC,
                AnthropicProvider(
                    api_key=config["anthropic_api_key"],
                    model=config.get("anthropic_model", "claude-3-opus-20240229")
                ),
                is_primary=config.get("primary_provider") == "anthropic"
            )
        
        # Add local provider if configured
        if config.get("local_model_url"):
            adapter.add_provider(
                LLMProvider.LOCAL,
                LocalProvider(
                    base_url=config["local_model_url"],
                    model=config.get("local_model", "llama2")
                ),
                is_primary=config.get("primary_provider") == "local"
            )
        
        # Always add mock provider as fallback
        adapter.add_provider(
            LLMProvider.MOCK,
            MockProvider()
        )
        
        return adapter