"""
DATABASE - JSON basierte Datenbank für CROD
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class CRODDatabase:
    """JSON Database für CROD Networks"""
    
    def __init__(self, data_dir: str = "crod_data"):
        self.data_dir = data_dir
        self.networks_dir = os.path.join(data_dir, "networks")
        self.history_file = os.path.join(data_dir, "crod_history.json")
        self.main_db_file = os.path.join(data_dir, "crod_data.json")
        
        # Create directories
        os.makedirs(self.networks_dir, exist_ok=True)
        
        # Initialize database
        self.data = self._load_database()
        
    def _load_database(self) -> Dict[str, Any]:
        """Load main database"""
        if os.path.exists(self.main_db_file):
            with open(self.main_db_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize new database
            return {
                "networks": {},
                "training_sessions": [],
                "atom_statistics": {},
                "total_messages": 0,
                "created_at": datetime.now().isoformat()
            }
            
    def save_database(self):
        """Save main database"""
        with open(self.main_db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
            
    def save_network(self, network_id: str, network_data: Dict[str, Any]):
        """Save network to database"""
        # Update main database
        self.data["networks"][network_id] = {
            "name": network_data.get("name", "Unknown"),
            "atoms": len(network_data.get("atoms", {})),
            "connections": len(network_data.get("connections", {})),
            "last_modified": datetime.now().isoformat(),
            "stats": network_data.get("stats", {})
        }
        
        # Save full network to file
        network_file = os.path.join(self.networks_dir, f"{network_id}.crod")
        with open(network_file, 'w') as f:
            json.dump(network_data, f, indent=2)
            
        self.save_database()
        print(f"💾 Network saved: {network_id}")
        
    def load_network(self, network_id: str) -> Dict[str, Any]:
        """Load network from database"""
        network_file = os.path.join(self.networks_dir, f"{network_id}.crod")
        if os.path.exists(network_file):
            with open(network_file, 'r') as f:
                return json.load(f)
        return None
        
    def save_training_session(self, session_data: Dict[str, Any]):
        """Save training session"""
        session = {
            "id": len(self.data["training_sessions"]),
            "timestamp": datetime.now().isoformat(),
            "network_name": session_data.get("network_name", "Unknown"),
            "epochs": session_data.get("epochs", 0),
            "final_accuracy": session_data.get("final_accuracy", 0),
            "final_loss": session_data.get("final_loss", 0),
            "performance_history": session_data.get("performance_history", [])
        }
        
        self.data["training_sessions"].append(session)
        
        # Also save to history file
        self._save_history(session)
        
        self.save_database()
        print(f"📊 Training session saved")
        
    def _save_history(self, session: Dict[str, Any]):
        """Save to history file"""
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                
        history.append(session)
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    def update_atom_statistics(self, atom_type: str, metrics: Dict[str, Any]):
        """Update atom statistics"""
        if atom_type not in self.data["atom_statistics"]:
            self.data["atom_statistics"][atom_type] = {
                "total_created": 0,
                "total_processed": 0,
                "total_errors": 0,
                "avg_processing_time": 0
            }
            
        stats = self.data["atom_statistics"][atom_type]
        stats["total_created"] += 1
        stats["total_processed"] += metrics.get("processed", 0)
        stats["total_errors"] += metrics.get("errors", 0)
        
        # Update average time
        if metrics.get("avg_time", 0) > 0:
            current_avg = stats["avg_processing_time"]
            new_count = stats["total_processed"]
            stats["avg_processing_time"] = (
                (current_avg * (new_count - 1) + metrics["avg_time"]) / new_count
                if new_count > 0 else metrics["avg_time"]
            )
            
        self.data["total_messages"] += metrics.get("processed", 0)
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        return {
            "total_networks": len(self.data["networks"]),
            "total_training_sessions": len(self.data["training_sessions"]),
            "total_messages_processed": self.data["total_messages"],
            "atom_statistics": self.data["atom_statistics"],
            "database_created": self.data["created_at"]
        }
        
    def list_networks(self) -> List[Dict[str, Any]]:
        """List all saved networks"""
        networks = []
        for network_id, info in self.data["networks"].items():
            networks.append({
                "id": network_id,
                "name": info["name"],
                "atoms": info["atoms"],
                "connections": info["connections"],
                "last_modified": info["last_modified"]
            })
        return networks
        
    def get_best_training_session(self) -> Dict[str, Any]:
        """Get best training session by accuracy"""
        if not self.data["training_sessions"]:
            return None
            
        return max(self.data["training_sessions"], 
                  key=lambda x: x.get("final_accuracy", 0))

# Global database instance
_db_instance = None

def get_database() -> CRODDatabase:
    """Get database singleton"""
    global _db_instance
    if _db_instance is None:
        _db_instance = CRODDatabase()
    return _db_instance