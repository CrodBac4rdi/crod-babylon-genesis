#!/usr/bin/env python3
"""
CROD AI Research Integration
Integrates cutting-edge AI models and research tools
Based on patterns from OpenAI, Meta, Anthropic research
"""

import asyncio
import json
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import subprocess
import os

# Import research libraries (wenn verfügbar)
try:
    import torch
    import transformers
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class ModelType(Enum):
    """Current state-of-the-art models"""
    # Meta Models
    LLAMA_3 = "meta-llama/Llama-3-8b"
    CODE_LLAMA = "codellama/CodeLlama-7b-Python-hf"
    
    # Microsoft Models
    PHI_3 = "microsoft/phi-3-mini-4k-instruct"
    
    # Mistral Models
    MISTRAL_7B = "mistralai/Mistral-7B-Instruct-v0.3"
    MIXTRAL = "mistralai/Mixtral-8x7B-v0.1"
    
    # Google Models
    GEMMA_2B = "google/gemma-2b-it"
    
    # Stability AI
    STABLE_CODE = "stabilityai/stable-code-3b"
    
    # OpenAI (via API)
    GPT_4 = "gpt-4-turbo-preview"
    GPT_4O = "gpt-4o"
    
    # Anthropic (via API)
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-5-sonnet"


@dataclass
class ResearchTask:
    """Research task structure"""
    task_type: str
    input_data: Any
    model_preferences: List[ModelType]
    context: Optional[Dict] = None
    stream: bool = True


class CRODResearchIntegration:
    """
    Integrates latest AI research and models
    Patterns from:
    - OpenAI's GPT best practices
    - Meta's LLaMA fine-tuning
    - Google's chain-of-thought prompting
    - Anthropic's constitutional AI
    """
    
    def __init__(self):
        self.available_models = self._detect_available_models()
        self.model_cache = {}
        self.research_patterns = self._load_research_patterns()
        
    def _detect_available_models(self) -> Dict[str, bool]:
        """Detect which models/APIs are available"""
        available = {
            "local_models": HAS_TRANSFORMERS and torch.cuda.is_available(),
            "openai_api": HAS_OPENAI and os.getenv("OPENAI_API_KEY"),
            "anthropic_api": os.getenv("ANTHROPIC_API_KEY") is not None,
            "ollama": self._check_ollama(),
            "llama_cpp": self._check_llama_cpp()
        }
        return available
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _check_llama_cpp(self) -> bool:
        """Check if llama.cpp is available"""
        try:
            result = subprocess.run(["which", "llama"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _load_research_patterns(self) -> Dict[str, Any]:
        """Load cutting-edge prompting patterns"""
        return {
            # Chain-of-Thought (Google Research)
            "chain_of_thought": {
                "pattern": "Let's think step by step:\n1. {step1}\n2. {step2}\n...",
                "use_cases": ["complex_reasoning", "math", "logic"]
            },
            
            # Tree-of-Thought (Princeton/Google)
            "tree_of_thought": {
                "pattern": "Consider multiple approaches:\nApproach A: {a}\nApproach B: {b}\nEvaluating...",
                "use_cases": ["creative_problem_solving", "planning"]
            },
            
            # ReAct (Princeton)
            "react": {
                "pattern": "Thought: {thought}\nAction: {action}\nObservation: {observation}\n",
                "use_cases": ["tool_use", "web_search", "code_generation"]
            },
            
            # Constitutional AI (Anthropic)
            "constitutional": {
                "pattern": "Helpful, Harmless, Honest evaluation:\n{evaluation}",
                "use_cases": ["safety", "alignment", "critique"]
            },
            
            # Self-Consistency (Google)
            "self_consistency": {
                "pattern": "Generate multiple solutions and vote:\nSolution 1: {s1}\nSolution 2: {s2}\n",
                "use_cases": ["accuracy", "reliability"]
            },
            
            # Reflexion (MIT)
            "reflexion": {
                "pattern": "Initial attempt: {attempt}\nReflection: {reflection}\nImproved: {improved}",
                "use_cases": ["code_generation", "writing", "planning"]
            }
        }
    
    async def process_research_task(self, task: ResearchTask) -> Dict[str, Any]:
        """Process a research task using best available model and patterns"""
        
        # Select best available model
        model = self._select_best_model(task)
        
        # Apply appropriate research pattern
        pattern = self._select_pattern(task)
        
        # Process based on model type
        if model in [ModelType.GPT_4, ModelType.GPT_4O]:
            return await self._process_openai(task, model, pattern)
        elif model in [ModelType.CLAUDE_3_OPUS, ModelType.CLAUDE_3_SONNET]:
            return await self._process_anthropic(task, model, pattern)
        elif self.available_models["ollama"]:
            return await self._process_ollama(task, model, pattern)
        else:
            return await self._process_local(task, model, pattern)
    
    def _select_best_model(self, task: ResearchTask) -> ModelType:
        """Select best available model for task"""
        # Prioritize based on task type
        if task.task_type == "code_generation":
            preferences = [
                ModelType.CLAUDE_3_SONNET,
                ModelType.GPT_4,
                ModelType.CODE_LLAMA,
                ModelType.STABLE_CODE
            ]
        elif task.task_type == "research":
            preferences = [
                ModelType.GPT_4O,
                ModelType.CLAUDE_3_OPUS,
                ModelType.MIXTRAL
            ]
        else:
            preferences = task.model_preferences
        
        # Return first available
        for model in preferences:
            if self._is_model_available(model):
                return model
        
        # Fallback
        return ModelType.MISTRAL_7B
    
    def _select_pattern(self, task: ResearchTask) -> str:
        """Select appropriate research pattern"""
        task_to_pattern = {
            "code_generation": "reflexion",
            "complex_reasoning": "chain_of_thought",
            "research": "react",
            "creative": "tree_of_thought",
            "verification": "self_consistency"
        }
        return task_to_pattern.get(task.task_type, "chain_of_thought")
    
    async def _process_ollama(self, task: ResearchTask, model: ModelType, pattern: str) -> Dict:
        """Process using Ollama (local models)"""
        model_name = model.value.split("/")[-1].lower()
        
        # Build prompt with research pattern
        prompt = self._build_prompt_with_pattern(task, pattern)
        
        # Run Ollama
        cmd = ["ollama", "run", model_name, prompt]
        if task.stream:
            # Stream response
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            results = []
            async for line in process.stdout:
                decoded = line.decode().strip()
                if decoded:
                    print(json.dumps({
                        "type": "stream",
                        "content": decoded
                    }))
                    results.append(decoded)
            
            return {
                "model": model_name,
                "pattern": pattern,
                "response": "\n".join(results)
            }
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "model": model_name,
                "pattern": pattern,
                "response": result.stdout
            }
    
    def _build_prompt_with_pattern(self, task: ResearchTask, pattern_name: str) -> str:
        """Build prompt using research pattern"""
        pattern = self.research_patterns[pattern_name]
        
        base_prompt = f"{task.input_data}\n\n"
        
        if pattern_name == "chain_of_thought":
            return base_prompt + "Let's solve this step by step:\n"
        elif pattern_name == "tree_of_thought":
            return base_prompt + "Let's explore multiple approaches:\n"
        elif pattern_name == "reflexion":
            return base_prompt + "I'll solve this and then reflect on my solution:\n"
        elif pattern_name == "react":
            return base_prompt + "Thought: I need to analyze this request\nAction: "
        else:
            return base_prompt
    
    def _is_model_available(self, model: ModelType) -> bool:
        """Check if specific model is available"""
        if model in [ModelType.GPT_4, ModelType.GPT_4O]:
            return self.available_models["openai_api"]
        elif model in [ModelType.CLAUDE_3_OPUS, ModelType.CLAUDE_3_SONNET]:
            return self.available_models["anthropic_api"]
        elif self.available_models["ollama"]:
            # Check if model is pulled in Ollama
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            model_name = model.value.split("/")[-1].lower()
            return model_name in result.stdout
        else:
            return self.available_models["local_models"]
    
    async def run_multimodal_analysis(self, image_path: str, text: str) -> Dict:
        """Run multimodal analysis using best available model"""
        # Modern multimodal models: GPT-4V, Claude 3, Gemini Pro Vision
        if self.available_models["openai_api"]:
            # Use GPT-4 Vision
            return await self._analyze_with_gpt4v(image_path, text)
        elif self.available_models["anthropic_api"]:
            # Use Claude 3 Vision
            return await self._analyze_with_claude3(image_path, text)
        else:
            # Fallback to CLIP or other local models
            return await self._analyze_with_local_multimodal(image_path, text)
    
    async def generate_embeddings(self, texts: List[str], model: str = "text-embedding-3-large") -> List[List[float]]:
        """Generate embeddings using best available model"""
        if self.available_models["openai_api"]:
            # Use OpenAI embeddings
            import openai
            response = await openai.Embedding.acreate(
                input=texts,
                model=model
            )
            return [item["embedding"] for item in response["data"]]
        else:
            # Use local sentence transformers
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            return model.encode(texts).tolist()


# CLI Interface
async def main():
    integration = CRODResearchIntegration()
    
    print(json.dumps({
        "type": "system",
        "message": "CROD Research Integration initialized",
        "available_models": integration.available_models
    }))
    
    # Example task
    task = ResearchTask(
        task_type="code_generation",
        input_data="Create a Python function that implements binary search",
        model_preferences=[ModelType.CLAUDE_3_SONNET, ModelType.CODE_LLAMA],
        stream=True
    )
    
    result = await integration.process_research_task(task)
    print(json.dumps({
        "type": "result",
        "data": result
    }))


if __name__ == "__main__":
    asyncio.run(main())