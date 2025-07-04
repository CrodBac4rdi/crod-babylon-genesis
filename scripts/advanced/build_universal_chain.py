#!/usr/bin/env python3
"""
CROD UNIVERSAL KNOWLEDGE CHAIN BUILDER
EVERYTHING IS CONNECTED - ATOMS → PATTERNS → CHAINS → NETWORKS
ZERO REDUNDANCY - MAXIMUM CONNECTIONS
"""

import json
import hashlib
import uuid
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class CRODUniversalChain:
    def __init__(self):
        self.atoms = {}  # atom_id -> atom data
        self.patterns = {}  # pattern_id -> pattern data  
        self.chains = {}  # chain_id -> chain data
        self.networks = {}  # network_id -> network data
        self.connections = defaultdict(list)  # id -> [connected_ids]
        self.atom_index = defaultdict(list)  # atom_content -> [atom_ids]
        
    def create_atom_id(self, content):
        """Create deterministic ID for atom - zero redundancy!"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def add_atom(self, content, atom_type, source=None, metadata=None):
        """Add atom with zero redundancy"""
        atom_id = self.create_atom_id(content)
        
        if atom_id not in self.atoms:
            self.atoms[atom_id] = {
                "id": atom_id,
                "content": content,
                "type": atom_type,
                "sources": [source] if source else [],
                "metadata": metadata or {},
                "created": datetime.now().isoformat(),
                "connections": [],
                "heat": 0.5
            }
            self.atom_index[content.lower()].append(atom_id)
        else:
            # Update existing atom - add source, increase heat
            if source and source not in self.atoms[atom_id]["sources"]:
                self.atoms[atom_id]["sources"].append(source)
            self.atoms[atom_id]["heat"] = min(1.0, self.atoms[atom_id]["heat"] + 0.1)
            
        return atom_id
    
    def add_pattern(self, atom_ids, pattern_type, strength=None, metadata=None):
        """Create pattern from atoms"""
        pattern_id = f"pattern_{hashlib.sha256(''.join(sorted(atom_ids)).encode()).hexdigest()[:16]}"
        
        if pattern_id not in self.patterns:
            self.patterns[pattern_id] = {
                "id": pattern_id, 
                "atoms": atom_ids,
                "type": pattern_type,
                "strength": strength or (sum(self.atoms[aid]["heat"] for aid in atom_ids if aid in self.atoms) / len(atom_ids)),
                "metadata": metadata or {},
                "created": datetime.now().isoformat(),
                "connections": []
            }
            
            # Connect atoms to pattern
            for atom_id in atom_ids:
                if atom_id in self.atoms:
                    self.atoms[atom_id]["connections"].append(pattern_id)
                    self.connections[atom_id].append(pattern_id)
                    self.connections[pattern_id].append(atom_id)
                    
        return pattern_id
    
    def add_chain(self, pattern_ids, chain_type, flow=None, metadata=None):
        """Create chain from patterns"""
        chain_id = f"chain_{hashlib.sha256('->'.join(pattern_ids).encode()).hexdigest()[:16]}"
        
        if chain_id not in self.chains:
            self.chains[chain_id] = {
                "id": chain_id,
                "patterns": pattern_ids,
                "type": chain_type,
                "flow": flow or "sequential",
                "metadata": metadata or {},
                "created": datetime.now().isoformat(),
                "connections": []
            }
            
            # Connect patterns to chain
            for pattern_id in pattern_ids:
                if pattern_id in self.patterns:
                    self.patterns[pattern_id]["connections"].append(chain_id)
                    self.connections[pattern_id].append(chain_id)
                    self.connections[chain_id].append(pattern_id)
                    
        return chain_id
    
    def add_network(self, chain_ids, network_type, topology=None, metadata=None):
        """Create network from chains"""
        network_id = f"network_{hashlib.sha256('<->'.join(sorted(chain_ids)).encode()).hexdigest()[:16]}"
        
        if network_id not in self.networks:
            self.networks[network_id] = {
                "id": network_id,
                "chains": chain_ids,
                "type": network_type,
                "topology": topology or "mesh",
                "metadata": metadata or {},
                "created": datetime.now().isoformat(),
                "connections": []
            }
            
            # Connect chains to network
            for chain_id in chain_ids:
                if chain_id in self.chains:
                    self.chains[chain_id]["connections"].append(network_id)
                    self.connections[chain_id].append(network_id)
                    self.connections[network_id].append(chain_id)
                    
        return network_id
    
    def connect_entities(self, id1, id2, connection_type="related"):
        """Connect any two entities"""
        self.connections[id1].append({"id": id2, "type": connection_type})
        self.connections[id2].append({"id": id1, "type": connection_type})
    
    def query_by_content(self, search_term):
        """Find atoms by content"""
        results = []
        search_lower = search_term.lower()
        
        for content, atom_ids in self.atom_index.items():
            if search_lower in content:
                results.extend(atom_ids)
                
        return results
    
    def get_connected(self, entity_id, depth=1):
        """Get all connected entities up to depth"""
        visited = set()
        queue = [(entity_id, 0)]
        results = []
        
        while queue:
            current_id, current_depth = queue.pop(0)
            
            if current_id in visited or current_depth > depth:
                continue
                
            visited.add(current_id)
            if current_depth > 0:  # Don't include the starting entity
                results.append(current_id)
                
            if current_depth < depth:
                for connected_id in self.connections.get(current_id, []):
                    if isinstance(connected_id, dict):
                        connected_id = connected_id["id"]
                    queue.append((connected_id, current_depth + 1))
                    
        return results
    
    def export_to_jsonl(self, output_dir):
        """Export everything to JSONL files"""
        output_path = Path(output_dir)
        
        # Single universal chain file
        with open(output_path / "crod_universal_chain.jsonl", 'w') as f:
            # Export atoms
            for atom in self.atoms.values():
                f.write(json.dumps({"layer": "atom", **atom}) + '\n')
                
            # Export patterns  
            for pattern in self.patterns.values():
                f.write(json.dumps({"layer": "pattern", **pattern}) + '\n')
                
            # Export chains
            for chain in self.chains.values():
                f.write(json.dumps({"layer": "chain", **chain}) + '\n')
                
            # Export networks
            for network in self.networks.values():
                f.write(json.dumps({"layer": "network", **network}) + '\n')
        
        # Connection index
        with open(output_path / "crod_connections.jsonl", 'w') as f:
            for entity_id, connected_ids in self.connections.items():
                f.write(json.dumps({
                    "entity": entity_id,
                    "connections": connected_ids,
                    "connection_count": len(connected_ids)
                }) + '\n')
        
        print(f"✅ Universal chain exported:")
        print(f"   📊 {len(self.atoms)} atoms")
        print(f"   🔗 {len(self.patterns)} patterns") 
        print(f"   ⛓️ {len(self.chains)} chains")
        print(f"   🌐 {len(self.networks)} networks")
        print(f"   🔌 {len(self.connections)} connections")

def build_crod_universal_chain():
    """Build the ultimate CROD knowledge chain"""
    chain = CRODUniversalChain()
    
    print("🔥 BUILDING CROD UNIVERSAL KNOWLEDGE CHAIN...")
    
    # Load existing atoms
    research_dir = Path("/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH")
    
    if (research_dir / "crod_atoms.jsonl").exists():
        print("📥 Loading existing atoms...")
        with open(research_dir / "crod_atoms.jsonl") as f:
            for line in f:
                atom = json.loads(line)
                chain.add_atom(
                    atom["atom"],
                    atom["type"], 
                    atom["source"],
                    {"heat": atom["heat"], "category": atom.get("category")}
                )
    
    # Load research findings
    if (research_dir / "research_consolidated.jsonl").exists():
        print("📥 Loading research findings...")
        with open(research_dir / "research_consolidated.jsonl") as f:
            for line in f:
                finding = json.loads(line)
                
                # Add finding as atom
                finding_id = chain.add_atom(
                    finding.get("title", finding.get("name", str(finding))),
                    finding["type"],
                    "research_consolidated",
                    finding
                )
                
                # Create patterns for related data
                if "technologies" in finding:
                    tech_atoms = []
                    for tech in finding["technologies"]:
                        if isinstance(tech, dict):
                            tech_name = tech.get("name", str(tech))
                        else:
                            tech_name = str(tech)
                        tech_id = chain.add_atom(tech_name, "technology", "research")
                        tech_atoms.append(tech_id)
                    
                    if tech_atoms:
                        pattern_id = chain.add_pattern(
                            tech_atoms + [finding_id],
                            "technology_group",
                            metadata={"category": finding.get("category")}
                        )
    
    # Load technologies database
    if (research_dir / "technologies.jsonl").exists():
        print("📥 Loading technologies database...")
        tech_atoms = []
        performance_atoms = []
        
        with open(research_dir / "technologies.jsonl") as f:
            for line in f:
                tech = json.loads(line)
                
                # Technology atom
                tech_id = chain.add_atom(
                    tech["name"],
                    "technology",
                    "technologies_db",
                    tech
                )
                tech_atoms.append(tech_id)
                
                # Performance atom
                if "performance" in tech:
                    perf_id = chain.add_atom(
                        f"{tech['name']}_performance_{tech['performance']}",
                        "performance",
                        "technologies_db",
                        {"value": tech["performance"], "technology": tech["name"]}
                    )
                    performance_atoms.append(perf_id)
                    
                    # Connect tech to performance
                    chain.connect_entities(tech_id, perf_id, "has_performance")
        
        # Create technology patterns by category
        categories = defaultdict(list)
        for tech_id in tech_atoms:
            tech_data = chain.atoms[tech_id]["metadata"]
            category = tech_data.get("category", "unknown")
            categories[category].append(tech_id)
        
        category_patterns = []
        for category, cat_tech_atoms in categories.items():
            if len(cat_tech_atoms) >= 2:
                pattern_id = chain.add_pattern(
                    cat_tech_atoms,
                    "technology_category", 
                    metadata={"category": category}
                )
                category_patterns.append(pattern_id)
        
        # Create technology chain
        if category_patterns:
            tech_chain_id = chain.add_chain(
                category_patterns,
                "technology_stack",
                "parallel",
                {"description": "Complete 2025 technology stack"}
            )
            
            # Create CROD implementation network
            crod_network_id = chain.add_network(
                [tech_chain_id],
                "crod_implementation",
                "centralized",
                {"goal": "Transform CROD with 2025 technologies"}
            )
    
    # Create meta-patterns for implementation
    print("🔗 Creating implementation patterns...")
    
    # Quick wins pattern
    quick_wins = chain.query_by_content("1 week") + chain.query_by_content("2 days") + chain.query_by_content("easy")
    if quick_wins:
        quick_pattern = chain.add_pattern(
            quick_wins[:10],  # Limit to prevent huge patterns
            "quick_wins",
            1.0,
            {"priority": "immediate", "effort": "low"}
        )
    
    # High performance pattern
    high_perf = chain.query_by_content("million") + chain.query_by_content("packets") + chain.query_by_content("faster")
    if high_perf:
        perf_pattern = chain.add_pattern(
            high_perf[:10],
            "high_performance", 
            0.9,
            {"impact": "revolutionary", "type": "performance"}
        )
    
    # Security pattern
    security = chain.query_by_content("quantum") + chain.query_by_content("crypto") + chain.query_by_content("security")
    if security:
        security_pattern = chain.add_pattern(
            security[:10],
            "security_critical",
            0.8,
            {"urgency": "critical", "deadline": "2029"}
        )
    
    return chain

if __name__ == "__main__":
    chain = build_crod_universal_chain()
    chain.export_to_jsonl("/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH")
    
    print("\n🌟 CROD UNIVERSAL KNOWLEDGE CHAIN COMPLETE!")
    print("🔥 EVERYTHING IS CONNECTED!")
    print("🧠 ZERO REDUNDANCY!")
    print("⚡ MAXIMUM QUERYABILITY!")
    print("🚀 READY FOR CROD DOMINATION!")