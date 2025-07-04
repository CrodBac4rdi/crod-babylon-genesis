"""
CROD NETWORK - Verwaltet das gesamte Netzwerk
"""

import json
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from atom_base import CRODAtom
from atom_types import create_atom

class Connection:
    """Represents a connection between atoms"""
    
    def __init__(self, from_atom: str, from_port: str, to_atom: str, to_port: str):
        self.id = str(uuid.uuid4())
        self.from_atom = from_atom
        self.from_port = from_port
        self.to_atom = to_atom
        self.to_port = to_port
        self.strength = 1.0
        self.type = "data"
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_atom": self.from_atom,
            "from_port": self.from_port,
            "to_atom": self.to_atom,
            "to_port": self.to_port,
            "strength": self.strength,
            "type": self.type
        }

class CRODNetwork:
    """Main network manager"""
    
    def __init__(self, network_id: str = None, name: str = "New Network"):
        self.id = network_id or str(uuid.uuid4())
        self.name = name
        self.atoms: Dict[str, CRODAtom] = {}
        self.connections: Dict[str, Connection] = {}
        self.config = {
            "tick_rate": 10,  # Hz
            "max_queue_size": 100,
            "error_handling": "continue",
            "logging_level": "info"
        }
        self.running = False
        self.tick_count = 0
        self.changelog = []
        
    def add_atom(self, atom_type: str, position: Tuple[float, float] = (0, 0)) -> CRODAtom:
        """Add new atom to network"""
        atom = create_atom(atom_type)
        atom.set_position(position[0], position[1])
        
        self.atoms[atom.id] = atom
        
        self._log_change("atom_added", {
            "atom_id": atom.id,
            "type": atom_type,
            "position": position
        })
        
        return atom
        
    def remove_atom(self, atom_id: str):
        """Remove atom from network"""
        if atom_id in self.atoms:
            # Remove all connections
            conns_to_remove = []
            for conn_id, conn in self.connections.items():
                if conn.from_atom == atom_id or conn.to_atom == atom_id:
                    conns_to_remove.append(conn_id)
                    
            for conn_id in conns_to_remove:
                self.remove_connection(conn_id)
                
            # Remove atom
            del self.atoms[atom_id]
            
            self._log_change("atom_removed", {"atom_id": atom_id})
            
    def connect_atoms(self, from_atom_id: str, from_port: str, 
                     to_atom_id: str, to_port: str) -> Optional[Connection]:
        """Connect two atoms"""
        if from_atom_id not in self.atoms or to_atom_id not in self.atoms:
            return None
            
        from_atom = self.atoms[from_atom_id]
        to_atom = self.atoms[to_atom_id]
        
        # Validate ports
        if from_port not in from_atom.get_output_ports():
            print(f"❌ Invalid output port: {from_port}")
            return None
            
        if to_port not in to_atom.get_input_ports():
            print(f"❌ Invalid input port: {to_port}")
            return None
            
        # Create connection
        conn = Connection(from_atom_id, from_port, to_atom_id, to_port)
        self.connections[conn.id] = conn
        
        # Setup atom connections
        from_atom.connect_output(from_port, to_atom, to_port)
        
        self._log_change("connection_added", {
            "connection_id": conn.id,
            "from": f"{from_atom_id}.{from_port}",
            "to": f"{to_atom_id}.{to_port}"
        })
        
        return conn
        
    def remove_connection(self, connection_id: str):
        """Remove connection"""
        if connection_id in self.connections:
            conn = self.connections[connection_id]
            
            # Disconnect atoms
            if conn.from_atom in self.atoms and conn.to_atom in self.atoms:
                from_atom = self.atoms[conn.from_atom]
                to_atom = self.atoms[conn.to_atom]
                from_atom.disconnect_output(conn.from_port, to_atom, conn.to_port)
                
            del self.connections[connection_id]
            
            self._log_change("connection_removed", {
                "connection_id": connection_id
            })
            
    def configure_atom(self, atom_id: str, config: Dict[str, Any]):
        """Configure atom"""
        if atom_id in self.atoms:
            old_config = self.atoms[atom_id].config.copy()
            self.atoms[atom_id].configure(config)
            
            self._log_change("atom_configured", {
                "atom_id": atom_id,
                "old_config": old_config,
                "new_config": config
            })
            
    def tick(self):
        """Execute one network cycle"""
        self.tick_count += 1
        
        # Trigger all atoms without inputs (sources)
        for atom in self.atoms.values():
            if not atom.get_input_ports():
                # Source atom - trigger it
                atom.execute()
                
    def start(self):
        """Start network execution"""
        self.running = True
        print(f"▶️ Network {self.name} started")
        
    def stop(self):
        """Stop network execution"""
        self.running = False
        print(f"⏹️ Network {self.name} stopped")
        
    def get_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        total_processed = sum(atom.metrics["processed"] for atom in self.atoms.values())
        total_errors = sum(atom.metrics["errors"] for atom in self.atoms.values())
        
        return {
            "atoms": len(self.atoms),
            "connections": len(self.connections),
            "tick_count": self.tick_count,
            "total_processed": total_processed,
            "total_errors": total_errors,
            "running": self.running
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize network to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "atoms": {
                atom_id: atom.to_dict() 
                for atom_id, atom in self.atoms.items()
            },
            "connections": {
                conn_id: conn.to_dict()
                for conn_id, conn in self.connections.items()
            },
            "config": self.config,
            "stats": self.get_stats()
        }
        
    def from_dict(self, data: Dict[str, Any]):
        """Load network from dictionary"""
        self.id = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.config = data.get("config", self.config)
        
        # Clear current network
        self.atoms.clear()
        self.connections.clear()
        
        # Load atoms
        for atom_id, atom_data in data.get("atoms", {}).items():
            atom_type = atom_data["type"]
            atom = create_atom(atom_type, atom_id)
            atom.from_dict(atom_data)
            self.atoms[atom_id] = atom
            
        # Load connections
        for conn_data in data.get("connections", {}).values():
            self.connect_atoms(
                conn_data["from_atom"],
                conn_data["from_port"],
                conn_data["to_atom"],
                conn_data["to_port"]
            )
            
    def save_to_file(self, filename: str):
        """Save network to file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"💾 Network saved to {filename}")
        
    def load_from_file(self, filename: str):
        """Load network from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        self.from_dict(data)
        print(f"📂 Network loaded from {filename}")
        
    def _log_change(self, action: str, details: Dict[str, Any]):
        """Log change to changelog"""
        self.changelog.append({
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "tick": self.tick_count
        })
        
    def get_changelog(self) -> List[Dict[str, Any]]:
        """Get changelog"""
        return self.changelog