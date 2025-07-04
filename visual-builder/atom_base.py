"""
CROD ATOM BASE - Basis für alle Atom-Typen
"""

import uuid
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class CRODAtom(ABC):
    """Basis-Klasse für alle CROD Atoms"""
    
    def __init__(self, atom_id: str = None, atom_type: str = "base"):
        self.id = atom_id or str(uuid.uuid4())
        self.type = atom_type
        self.position = {"x": 0, "y": 0}
        self.config = self.get_default_config()
        self.state = {"active": True, "processing": False}
        self.inputs = {}
        self.outputs = {}
        self.input_connections = []
        self.output_connections = []
        self.metrics = {
            "processed": 0,
            "errors": 0,
            "avg_time": 0
        }
        
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Returns default configuration"""
        pass
        
    @abstractmethod
    def get_input_ports(self) -> List[str]:
        """Returns list of input port names"""
        pass
        
    @abstractmethod
    def get_output_ports(self) -> List[str]:
        """Returns list of output port names"""
        pass
        
    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        pass
        
    def receive_input(self, port: str, data: Any):
        """Receives data on input port"""
        if port in self.get_input_ports():
            self.inputs[port] = data
            
            # Check if all required inputs are present
            if self.all_inputs_ready():
                self.execute()
                
    def all_inputs_ready(self) -> bool:
        """Check if all required inputs are available"""
        required_ports = self.get_input_ports()
        
        # For atoms with optional ports, check if at least one input exists
        if self.type in ["thinker", "memory", "router"]:
            return len(self.inputs) > 0
            
        # For others, need all inputs
        return all(port in self.inputs for port in required_ports)
        
    def execute(self):
        """Execute atom processing"""
        if self.state["processing"]:
            return
            
        self.state["processing"] = True
        start_time = datetime.now()
        
        try:
            # Process inputs
            results = self.process(self.inputs)
            
            # Send outputs
            for port, data in results.items():
                self.send_output(port, data)
                
            # Update metrics
            self.metrics["processed"] += 1
            elapsed = (datetime.now() - start_time).total_seconds()
            self.metrics["avg_time"] = (
                (self.metrics["avg_time"] * (self.metrics["processed"] - 1) + elapsed)
                / self.metrics["processed"]
            )
            
            # Clear inputs for next cycle
            self.inputs.clear()
            
        except Exception as e:
            self.metrics["errors"] += 1
            print(f"❌ Error in {self.type} {self.id}: {e}")
            
        finally:
            self.state["processing"] = False
            
    def send_output(self, port: str, data: Any):
        """Send data to connected atoms"""
        self.outputs[port] = data
        
        # Notify all connected atoms
        for conn in self.output_connections:
            if conn["from_port"] == port:
                target_atom = conn["to_atom"]
                target_port = conn["to_port"]
                if target_atom:
                    target_atom.receive_input(target_port, data)
                    
    def connect_output(self, from_port: str, to_atom: 'CRODAtom', to_port: str):
        """Connect output port to another atom's input"""
        if from_port in self.get_output_ports():
            connection = {
                "from_port": from_port,
                "to_atom": to_atom,
                "to_port": to_port
            }
            self.output_connections.append(connection)
            
            # Also register on target atom
            to_atom.input_connections.append({
                "from_atom": self,
                "from_port": from_port,
                "to_port": to_port
            })
            
    def disconnect_output(self, from_port: str, to_atom: 'CRODAtom', to_port: str):
        """Disconnect output port"""
        self.output_connections = [
            conn for conn in self.output_connections
            if not (conn["from_port"] == from_port and 
                   conn["to_atom"] == to_atom and 
                   conn["to_port"] == to_port)
        ]
        
    def configure(self, config: Dict[str, Any]):
        """Update configuration"""
        self.config.update(config)
        
    def set_position(self, x: float, y: float):
        """Set visual position"""
        self.position = {"x": x, "y": y}
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "position": self.position,
            "config": self.config,
            "state": self.state,
            "metrics": self.metrics
        }
        
    def from_dict(self, data: Dict[str, Any]):
        """Load from dictionary"""
        self.id = data.get("id", self.id)
        self.position = data.get("position", self.position)
        self.config = data.get("config", self.config)
        self.state = data.get("state", self.state)
        self.metrics = data.get("metrics", self.metrics)