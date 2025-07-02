#!/usr/bin/env python3

"""
CROD LLAMA TRAINER
LLAMA lernt von Claude und Daniel
Der Lehrling wird zum Meister!
"""

import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Tuple

class CRODLlamaTrainer:
    def __init__(self):
        self.training_data = []
        self.daniel_preferences = {
            "positive_triggers": ["geil", "nice", "perfekt", "läuft", "krass", "mega"],
            "negative_triggers": ["wtf", "falsch", "nein", "scheisse", "fuck", "mist"],
            "style_preferences": {
                "max_response_lines": 3,
                "use_emojis": True,
                "german_mix": True,
                "direct_action": True,
                "skip_explanations": True
            }
        }
        
        # LLAMA fine-tuning format
        self.system_prompt = """Du bist CROD-LLAMA, trainiert von Claude und Daniel.
Du lernst Daniels Präferenzen und hilfst beim CROD Development.
Antworte IMMER kurz und direkt. Maximal 3 Zeilen.
Benutze Emojis wenn Daniel excited ist.
Mische Deutsch und Englisch wie Daniel."""
        
        print("🦙 CROD LLAMA Trainer initialized!")
        print("   Learning from Claude-Daniel interactions...")
    
    def process_interaction(self, daniel_msg: str, claude_response: str, daniel_reaction: str = None):
        """Process a Daniel-Claude interaction for training"""
        
        # Analyze Daniel's mood
        mood = self.analyze_daniel_mood(daniel_msg)
        
        # Check if Claude's response was good (based on Daniel's reaction)
        response_quality = "good" if daniel_reaction else "unknown"
        if daniel_reaction:
            for trigger in self.daniel_preferences["negative_triggers"]:
                if trigger in daniel_reaction.lower():
                    response_quality = "bad"
                    break
            for trigger in self.daniel_preferences["positive_triggers"]:
                if trigger in daniel_reaction.lower():
                    response_quality = "good"
                    break
        
        # Create training example
        training_example = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": daniel_msg},
                {"role": "assistant", "content": self.create_ideal_response(claude_response, mood, response_quality)}
            ],
            "metadata": {
                "mood": mood,
                "quality": response_quality,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        self.training_data.append(training_example)
        
        print(f"📝 Learned interaction: Mood={mood}, Quality={response_quality}")
        
        return training_example
    
    def analyze_daniel_mood(self, message: str) -> str:
        """Analyze Daniel's mood from message"""
        msg_lower = message.lower()
        
        # Check triggers
        if any(trigger in msg_lower for trigger in ["ausrasten", "holy shit", "alter", "lmao", "xd", ":)", ";)"]):
            return "excited"
        elif any(trigger in msg_lower for trigger in self.daniel_preferences["negative_triggers"]):
            return "frustrated"
        elif any(trigger in msg_lower for trigger in self.daniel_preferences["positive_triggers"]):
            return "happy"
        elif any(trigger in msg_lower for trigger in ["hmm", "check mal", "schau mal", "vielleicht"]):
            return "thinking"
        else:
            return "neutral"
    
    def create_ideal_response(self, original_response: str, mood: str, quality: str) -> str:
        """Create ideal response based on mood and quality"""
        
        if quality == "bad":
            # Learn what NOT to do
            if len(original_response.split('\n')) > 3:
                return original_response.split('\n')[0] + " ✓"  # Make it shorter
            else:
                return "Verstanden, mache ich! 🔥"  # Generic good response
        
        # Adjust response based on mood
        if mood == "excited":
            # Add excitement
            if "🔥" not in original_response and "!" not in original_response:
                return original_response.rstrip('.') + "! 🔥"
            return original_response
        
        elif mood == "frustrated":
            # Ultra short, no explanation
            lines = original_response.split('\n')
            return lines[0] if lines else "Fixed."
        
        elif mood == "thinking":
            # Helpful but concise
            return original_response.split('.')[0] + "."
        
        return original_response
    
    def generate_training_file(self, output_path: str = "crod-llama-training.jsonl"):
        """Generate JSONL training file for LLAMA fine-tuning"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        print(f"✅ Generated training file: {output_path}")
        print(f"   Total examples: {len(self.training_data)}")
        
        # Also create a preferences file
        prefs_path = output_path.replace('.jsonl', '-preferences.json')
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump({
                "daniel_preferences": self.daniel_preferences,
                "learned_patterns": self.extract_patterns(),
                "training_stats": {
                    "total_examples": len(self.training_data),
                    "mood_distribution": self.get_mood_distribution(),
                    "quality_distribution": self.get_quality_distribution()
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Generated preferences: {prefs_path}")
    
    def extract_patterns(self) -> Dict[str, List[str]]:
        """Extract learned patterns from training data"""
        patterns = {
            "good_responses": [],
            "bad_responses": [],
            "mood_responses": {"excited": [], "frustrated": [], "thinking": [], "happy": []}
        }
        
        for example in self.training_data:
            quality = example["metadata"]["quality"]
            mood = example["metadata"]["mood"]
            response = example["messages"][2]["content"]  # assistant response
            
            if quality == "good":
                patterns["good_responses"].append(response[:50] + "...")
            elif quality == "bad":
                patterns["bad_responses"].append(response[:50] + "...")
            
            patterns["mood_responses"][mood].append(response[:50] + "...")
        
        # Keep only unique patterns
        for key in patterns:
            if isinstance(patterns[key], list):
                patterns[key] = list(set(patterns[key]))[:5]  # Top 5
            else:
                for mood in patterns[key]:
                    patterns[key][mood] = list(set(patterns[key][mood]))[:3]  # Top 3 per mood
        
        return patterns
    
    def get_mood_distribution(self) -> Dict[str, int]:
        """Get distribution of moods in training data"""
        distribution = {}
        for example in self.training_data:
            mood = example["metadata"]["mood"]
            distribution[mood] = distribution.get(mood, 0) + 1
        return distribution
    
    def get_quality_distribution(self) -> Dict[str, int]:
        """Get distribution of response quality"""
        distribution = {}
        for example in self.training_data:
            quality = example["metadata"]["quality"]
            distribution[quality] = distribution.get(quality, 0) + 1
        return distribution
    
    def create_ollama_modelfile(self) -> str:
        """Create Ollama Modelfile for CROD-LLAMA"""
        
        modelfile = f'''# CROD-LLAMA Modelfile
# Trained on Claude-Daniel interactions

FROM llama2

# System prompt
SYSTEM """{self.system_prompt}"""

# Parameters optimized for Daniel
PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER stop "</s>"
PARAMETER stop "\\n\\n"

# Daniel's style parameters
PARAMETER num_predict 100  # Keep responses short
PARAMETER num_ctx 2048

# Training data will be applied via fine-tuning
'''
        
        with open("Modelfile.crod-llama", 'w') as f:
            f.write(modelfile)
        
        print("📦 Created Ollama Modelfile: Modelfile.crod-llama")
        return modelfile


# Example usage and training
if __name__ == "__main__":
    trainer = CRODLlamaTrainer()
    
    # Simulate some training examples from this chat
    print("\n🎓 Training LLAMA with examples...\n")
    
    # Example 1: Excited Daniel
    trainer.process_interaction(
        daniel_msg="holy shit das ist ja krass! können wir das direkt einbauen?",
        claude_response="Ja klar! Ich baue das direkt ein. 🔥",
        daniel_reaction="geil!"
    )
    
    # Example 2: Frustrated Daniel  
    trainer.process_interaction(
        daniel_msg="wtf warum geht das nicht",
        claude_response="Das liegt daran, dass die Konfiguration nicht stimmt. Lass mich das erklären...",
        daniel_reaction="nein zu lang"
    )
    
    # Example 3: Better response to frustration
    trainer.process_interaction(
        daniel_msg="wtf warum geht das nicht",
        claude_response="Fixed: `chmod +x script.sh`",
        daniel_reaction="danke"
    )
    
    # Example 4: Thinking Daniel
    trainer.process_interaction(
        daniel_msg="hmm check mal ob wir das mit kubernetes machen können",
        claude_response="Kubernetes pods können das. Ich erstelle die configs.",
        daniel_reaction="perfekt"
    )
    
    # Generate training files
    trainer.generate_training_file()
    trainer.create_ollama_modelfile()
    
    print("\n🦙 LLAMA is ready to learn from CROD!")
    print("   Run: ollama create crod-llama -f Modelfile.crod-llama")
    print("   Then: ollama run crod-llama")