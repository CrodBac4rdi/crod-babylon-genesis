"""
CROD ATOM TYPES - Konkrete Atom Implementierungen
"""

import random
import json
from typing import Dict, Any, List
from atom_base import CRODAtom

class ThinkerAtom(CRODAtom):
    """Generiert neue Gedanken"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "thinker")
        self.thought_patterns = [
            "Was wäre wenn {}?",
            "Könnte {} mit {} verbunden werden?",
            "Die Emergenz von {} führt zu {}",
            "Selbstorganisation entsteht durch {}",
            "Pattern {} wiederholt sich in {}"
        ]
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "creativity": 0.5,
            "speed": 1.0,
            "topics": ["consciousness", "patterns", "emergence", "networks", "atoms"]
        }
        
    def get_input_ports(self) -> List[str]:
        return ["trigger", "context"]
        
    def get_output_ports(self) -> List[str]:
        return ["thought"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Generate thought based on config
        creativity = self.config["creativity"]
        topics = self.config["topics"]
        
        if random.random() < creativity:
            # Creative thought
            pattern = random.choice(self.thought_patterns)
            topic1 = random.choice(topics)
            topic2 = random.choice(topics)
            thought = pattern.format(topic1, topic2)
        else:
            # Standard thought
            topic = random.choice(topics)
            thought = f"Analysiere {topic}"
            
        confidence = random.uniform(0.3, 0.9) * creativity
        
        return {
            "thought": {
                "content": thought,
                "confidence": confidence,
                "generator": self.id
            }
        }

class DoubterAtom(CRODAtom):
    """Zweifelt an Gedanken"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "doubter")
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skepticism": 0.7,
            "depth": 3
        }
        
    def get_input_ports(self) -> List[str]:
        return ["thought"]
        
    def get_output_ports(self) -> List[str]:
        return ["doubt", "confidence"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        thought_data = inputs.get("thought", {})
        content = thought_data.get("content", "")
        confidence = thought_data.get("confidence", 0.5)
        
        # Calculate doubt
        skepticism = self.config["skepticism"]
        doubt_level = skepticism * (1 - confidence)
        
        questions = []
        if doubt_level > 0.3:
            questions.append(f"Ist '{content}' wirklich wahr?")
        if doubt_level > 0.5:
            questions.append("Welche Annahmen stecken dahinter?")
        if doubt_level > 0.7:
            questions.append("Gibt es Gegenbeispiele?")
            
        adjusted_confidence = confidence * (1 - doubt_level * 0.3)
        
        return {
            "doubt": {
                "original": content,
                "doubt_level": doubt_level,
                "questions": questions
            },
            "confidence": adjusted_confidence
        }

class LearnerAtom(CRODAtom):
    """Extrahiert Patterns aus Erfahrungen"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "learner")
        self.pattern_memory = []
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "learning_rate": 0.3,
            "memory_size": 100
        }
        
    def get_input_ports(self) -> List[str]:
        return ["experience"]
        
    def get_output_ports(self) -> List[str]:
        return ["pattern", "knowledge"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        experience = inputs.get("experience", {})
        
        # Store in memory
        self.pattern_memory.append(experience)
        if len(self.pattern_memory) > self.config["memory_size"]:
            self.pattern_memory.pop(0)
            
        # Extract pattern
        if len(self.pattern_memory) >= 3:
            # Simple pattern detection
            pattern_type = "repetition" if len(set(str(m) for m in self.pattern_memory[-3:])) == 1 else "variation"
            
            return {
                "pattern": {
                    "type": pattern_type,
                    "confidence": self.config["learning_rate"],
                    "examples": self.pattern_memory[-3:]
                },
                "knowledge": {
                    "total_experiences": len(self.pattern_memory),
                    "pattern_found": True
                }
            }
            
        return {
            "pattern": None,
            "knowledge": {
                "total_experiences": len(self.pattern_memory),
                "pattern_found": False
            }
        }

class ConnectorAtom(CRODAtom):
    """Verbindet zwei Gedanken"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "connector")
        self.pending_thoughts = []
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "threshold": 0.5,
            "max_connections": 10
        }
        
    def get_input_ports(self) -> List[str]:
        return ["thought_a", "thought_b"]
        
    def get_output_ports(self) -> List[str]:
        return ["connection", "strength"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        thought_a = inputs.get("thought_a", {})
        thought_b = inputs.get("thought_b", {})
        
        if thought_a and thought_b:
            # Calculate connection strength
            conf_a = thought_a.get("confidence", 0.5)
            conf_b = thought_b.get("confidence", 0.5)
            
            strength = 1 - abs(conf_a - conf_b)
            
            if strength >= self.config["threshold"]:
                return {
                    "connection": {
                        "thought_a": thought_a.get("content", ""),
                        "thought_b": thought_b.get("content", ""),
                        "type": "similarity" if strength > 0.7 else "contrast"
                    },
                    "strength": strength
                }
                
        return {
            "connection": None,
            "strength": 0
        }

class EvaluatorAtom(CRODAtom):
    """Bewertet Qualität von Gedanken"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "evaluator")
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "strictness": 0.5,
            "criteria_weights": {
                "clarity": 0.3,
                "relevance": 0.4,
                "novelty": 0.3
            }
        }
        
    def get_input_ports(self) -> List[str]:
        return ["thought", "criteria"]
        
    def get_output_ports(self) -> List[str]:
        return ["score", "feedback"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        thought = inputs.get("thought", {})
        criteria = inputs.get("criteria", self.config["criteria_weights"])
        
        # Simple scoring
        content = thought.get("content", "")
        confidence = thought.get("confidence", 0.5)
        
        scores = {
            "clarity": confidence,
            "relevance": random.uniform(0.3, 0.8),
            "novelty": random.uniform(0.2, 0.9)
        }
        
        # Weighted average
        total_score = sum(
            scores.get(crit, 0.5) * weight 
            for crit, weight in criteria.items()
        )
        
        # Apply strictness
        final_score = total_score * (2 - self.config["strictness"])
        
        feedback = []
        if final_score < 0.3:
            feedback.append("Needs improvement")
        elif final_score < 0.7:
            feedback.append("Good potential")
        else:
            feedback.append("Excellent thought")
            
        return {
            "score": final_score,
            "feedback": {
                "scores": scores,
                "comments": feedback,
                "overall": final_score
            }
        }

class MemoryAtom(CRODAtom):
    """Speichert und retrieved Informationen"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "memory")
        self.storage = []
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "capacity": 100,
            "decay_rate": 0.01
        }
        
    def get_input_ports(self) -> List[str]:
        return ["data", "query"]
        
    def get_output_ports(self) -> List[str]:
        return ["stored", "retrieved"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs.get("data")
        query = inputs.get("query")
        
        outputs = {}
        
        if data:
            # Store data
            if isinstance(data, dict):
                importance = data.get("importance", 0.5)
                memory_item = {
                    "content": data,
                    "importance": importance,
                    "age": 0
                }
            else:
                # Handle non-dict data
                memory_item = {
                    "content": data,
                    "importance": 0.5,
                    "age": 0
                }
            
            self.storage.append(memory_item)
            
            # Manage capacity
            if len(self.storage) > self.config["capacity"]:
                # Remove least important
                self.storage.sort(key=lambda x: x["importance"])
                self.storage = self.storage[-self.config["capacity"]:]
                
            outputs["stored"] = {
                "success": True,
                "memory_size": len(self.storage)
            }
            
        if query:
            # Retrieve data
            if self.storage:
                # Simple retrieval - random for now
                memory = random.choice(self.storage)
                outputs["retrieved"] = memory["content"]
            else:
                outputs["retrieved"] = None
                
        # Apply decay
        for item in self.storage:
            item["age"] += 1
            if isinstance(item["importance"], (int, float)):
                item["importance"] *= (1 - self.config["decay_rate"])
            
        return outputs

class SynthesizerAtom(CRODAtom):
    """Kombiniert Konzepte zu neuen Ideen"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "synthesizer")
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "innovation": 0.5,
            "coherence": 0.7
        }
        
    def get_input_ports(self) -> List[str]:
        return ["concept_a", "concept_b"]
        
    def get_output_ports(self) -> List[str]:
        return ["synthesis"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        concept_a = inputs.get("concept_a", {})
        concept_b = inputs.get("concept_b", {})
        
        if concept_a and concept_b:
            # Extract content
            content_a = concept_a.get("content", "")
            content_b = concept_b.get("content", "")
            
            # Generate synthesis
            if random.random() < self.config["innovation"]:
                # Innovative combination
                synthesis = f"Neue Erkenntnis: {content_a} transformiert {content_b}"
            else:
                # Standard combination
                synthesis = f"{content_a} und {content_b} ergänzen sich"
                
            confidence = (
                concept_a.get("confidence", 0.5) * 
                concept_b.get("confidence", 0.5) * 
                self.config["coherence"]
            )
            
            return {
                "synthesis": {
                    "content": synthesis,
                    "sources": [content_a, content_b],
                    "confidence": confidence,
                    "innovation_level": self.config["innovation"]
                }
            }
            
        return {"synthesis": None}

class RouterAtom(CRODAtom):
    """Leitet Nachrichten basierend auf Regeln weiter"""
    
    def __init__(self, atom_id: str = None):
        super().__init__(atom_id, "router")
        
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "routing_table": {
                "high_confidence": "output_a",
                "low_confidence": "output_b",
                "default": "output_c"
            },
            "default_route": "output_c"
        }
        
    def get_input_ports(self) -> List[str]:
        return ["input"]
        
    def get_output_ports(self) -> List[str]:
        return ["output_a", "output_b", "output_c"]
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs.get("input", {})
        
        # Determine route
        confidence = data.get("confidence", 0.5)
        
        if confidence > 0.7:
            route = "output_a"
        elif confidence < 0.3:
            route = "output_b"
        else:
            route = self.config["default_route"]
            
        return {route: data}

# Registry of all atom types
ATOM_TYPES = {
    "thinker": ThinkerAtom,
    "doubter": DoubterAtom,
    "learner": LearnerAtom,
    "connector": ConnectorAtom,
    "evaluator": EvaluatorAtom,
    "memory": MemoryAtom,
    "synthesizer": SynthesizerAtom,
    "router": RouterAtom
}

def create_atom(atom_type: str, atom_id: str = None) -> CRODAtom:
    """Factory function to create atoms"""
    if atom_type in ATOM_TYPES:
        return ATOM_TYPES[atom_type](atom_id)
    else:
        raise ValueError(f"Unknown atom type: {atom_type}")