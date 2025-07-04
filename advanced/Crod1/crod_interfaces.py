# crod_interfaces.py - Stabile Schnittstellen für alle Module
# Diese Datei NIEMALS ändern - nur erweitern!

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class IStorage(ABC):
    """Storage Interface - Egal ob SQLite, Redis, MongoDB"""
    
    @abstractmethod
    def get_atom(self, atom_id: int) -> Optional[Dict[str, Any]]:
        """Get atom by ID - returns dict or None"""
        pass
    
    @abstractmethod
    def add_atom(self, value: str, weight: int = 50, category: str = 'default') -> int:
        """Add new atom - returns ID"""
        pass
    
    @abstractmethod
    def get_all_atoms(self) -> List[Dict[str, Any]]:
        """Get all atoms as list of dicts"""
        pass
    
    @abstractmethod
    def close(self):
        """Close storage connection"""
        pass

class IPatterns(ABC):
    """Pattern Detection Interface"""
    
    @abstractmethod
    def detect(self, text: str) -> List[str]:
        """Detect patterns in text - returns list of pattern IDs"""
        pass
    
    @abstractmethod
    def add_pattern(self, pattern_id: str, description: str):
        """Add new pattern"""
        pass

class IChat(ABC):
    """Chat Interface"""
    
    @abstractmethod
    def process_message(self, message: str) -> str:
        """Process chat message - returns response"""
        pass

class IEngine(ABC):
    """Engine Interface"""
    
    @abstractmethod
    def process(self, text: str) -> Dict[str, Any]:
        """Process text - returns result dict"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        pass

# Data Classes für konsistente Datenstrukturen
class Atom:
    """Atom data structure"""
    def __init__(self, atom_id: int, value: str, weight: int = 50, category: str = 'default'):
        self.id = atom_id
        self.value = value
        self.weight = weight
        self.category = category
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'value': self.value,
            'weight': self.weight,
            'category': self.category
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Atom':
        return Atom(
            atom_id=data.get('id', 0),
            value=data.get('value', ''),
            weight=data.get('weight', 50),
            category=data.get('category', 'default')
        )

class Pattern:
    """Pattern data structure"""
    def __init__(self, pattern_id: str, description: str, atoms: List[int] = None):
        self.id = pattern_id
        self.description = description
        self.atoms = atoms or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'description': self.description,
            'atoms': self.atoms
        }