#!/usr/bin/env python3
"""
COMPLETE CROD ATOMIZER
Transform ALL knowledge to atomic JSONL format
- Include ALL directories
- Skip node_modules duplicates  
- Create master knowledge database
"""

import os
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class CRODCompleteAtomizer:
    def __init__(self):
        self.atoms = {}
        self.processed_files = set()
        self.skipped_paths = set()
        
    def should_skip_path(self, path):
        """Skip node_modules and other noise"""
        skip_patterns = [
            'node_modules',
            '.git',
            '__pycache__',
            '.pytest_cache',
            'target/debug',
            'target/release'
        ]
        
        path_str = str(path)
        for pattern in skip_patterns:
            if pattern in path_str:
                return True
        return False
    
    def create_atom_id(self, content):
        """Create deterministic ID"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def extract_atoms_from_md(self, file_path, content):
        """Enhanced atom extraction"""
        atoms = []
        
        # Headers as concepts
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        for header in headers:
            clean_header = re.sub(r'[🔥⚡💀🚀🧠⚠️📊🎯💡🌟🔍📁🏗️💻📚]', '', header).strip()
            if len(clean_header) > 3:
                atoms.append({
                    "content": clean_header,
                    "type": "concept",
                    "category": "structure",
                    "heat": 0.6
                })
        
        # Technologies with better pattern matching
        tech_patterns = [
            # Networking
            r'\b(eBPF|XDP|DPDK|SPDK|NATS|Redis|Kafka|RabbitMQ)\b',
            r'\b(HTTP/3|QUIC|WebSocket|WebTransport|gRPC|REST)\b',
            r'\b(RDMA|InfiniBand|RoCE|TCP|UDP|DNS)\b',
            
            # Container/Orchestration  
            r'\b(Docker|Kubernetes|K8s|CRI-O|containerd|Podman)\b',
            r'\b(Helm|ArgoCD|Istio|Linkerd|Prometheus|Grafana)\b',
            
            # Programming/Frameworks
            r'\b(Elixir|Rust|Go|Python|JavaScript|TypeScript)\b',
            r'\b(Phoenix|GenServer|BEAM|Actix|FastAPI|Express)\b',
            
            # Browsers/Web
            r'\b(WebGPU|WebNN|WebAssembly|WASM|WebCodecs)\b',
            r'\b(Chrome|Firefox|Safari|Edge|V8|SpiderMonkey)\b',
            
            # Hardware/Infrastructure
            r'\b(Intel|AMD|NVIDIA|ARM|RISC-V|x86|GPU|CPU|NPU)\b',
            r'\b(AMX|AVX-512|TDX|SEV-SNP|CXL|PCIe|NVMe)\b',
            
            # Cryptography/Security
            r'\b(AES|RSA|ECC|ML-KEM|ML-DSA|NIST|quantum|TLS)\b',
            r'\b(SGX|HSM|TPM|SEV|confidential|enclave)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in set(matches):  # Remove duplicates
                atoms.append({
                    "content": match.lower(),
                    "type": "technology",
                    "category": "tech", 
                    "heat": 0.8
                })
        
        # Performance metrics
        perf_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:x|times|×)\s+(?:faster|improvement|better)',
            r'(\d+(?:\.\d+)?)\s*(?:M|million|k|thousand)\s+(?:packets|ops|operations|requests)/(?:sec|second)',
            r'(\d+(?:\.\d+)?)\s*(?:ms|μs|microsecond|millisecond|ns)\s+(?:latency|delay)',
            r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s+(?:faster|improvement|reduction|less)',
            r'(\d+(?:\.\d+)?)\s*(?:GB|MB|TB)\s+(?:bandwidth|throughput|storage)'
        ]
        
        for pattern in perf_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                atoms.append({
                    "content": f"performance_{match}",
                    "type": "performance",
                    "category": "metrics",
                    "heat": 0.9,
                    "value": float(match) if '.' in match else int(match)
                })
        
        # Code blocks as implementations
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        for lang, code in code_blocks:
            if lang and len(code.strip()) > 20:
                atoms.append({
                    "content": f"code_example_{lang}",
                    "type": "implementation",
                    "category": "code",
                    "heat": 0.7,
                    "language": lang or "unknown",
                    "code": code.strip()[:200]  # First 200 chars
                })
        
        # URLs as resources
        urls = re.findall(r'https?://[^\s\)]+', content)
        for url in set(urls):  # Remove duplicates
            atoms.append({
                "content": url,
                "type": "resource",
                "category": "link",
                "heat": 0.4
            })
        
        # Add source metadata to all atoms
        for atom in atoms:
            atom["source"] = str(file_path)
            atom["extracted_at"] = datetime.now().isoformat()
            
        return atoms
    
    def add_atom(self, atom_data):
        """Add atom with deduplication"""
        atom_id = self.create_atom_id(atom_data["content"])
        
        if atom_id not in self.atoms:
            self.atoms[atom_id] = {
                "id": atom_id,
                **atom_data,
                "sources": [atom_data["source"]],
                "mention_count": 1
            }
        else:
            # Update existing atom
            existing = self.atoms[atom_id]
            if atom_data["source"] not in existing["sources"]:
                existing["sources"].append(atom_data["source"])
            existing["mention_count"] += 1
            existing["heat"] = min(1.0, existing["heat"] + 0.05)  # Increase heat
            
        return atom_id
    
    def process_directory(self, directory):
        """Process all markdown files in directory"""
        print(f"🔄 Processing directory: {directory}")
        
        for md_file in Path(directory).rglob("*.md"):
            if self.should_skip_path(md_file):
                self.skipped_paths.add(str(md_file))
                continue
                
            if str(md_file) in self.processed_files:
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if len(content.strip()) < 50:  # Skip tiny files
                    continue
                    
                atoms = self.extract_atoms_from_md(md_file, content)
                for atom_data in atoms:
                    self.add_atom(atom_data)
                    
                self.processed_files.add(str(md_file))
                print(f"✅ {md_file}: {len(atoms)} atoms")
                
            except Exception as e:
                print(f"❌ Error processing {md_file}: {e}")
    
    def add_research_files(self):
        """Add our new research files"""
        research_dir = Path("/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH")
        
        # Add all our research docs
        research_files = [
            "research_consolidated.jsonl",
            "technologies.jsonl", 
            "crod_universal_chain.jsonl"
        ]
        
        for filename in research_files:
            filepath = research_dir / filename
            if filepath.exists():
                print(f"📥 Loading {filename}...")
                with open(filepath) as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            
                            # Convert to atom format
                            content = data.get("title", data.get("name", data.get("content", str(data))))
                            atom_data = {
                                "content": content,
                                "type": data.get("type", "research"),
                                "category": data.get("category", "research"),
                                "heat": 0.8,
                                "source": str(filepath),
                                "metadata": data
                            }
                            self.add_atom(atom_data)
                            
                        except json.JSONDecodeError:
                            continue
    
    def export_to_jsonl(self, output_path):
        """Export master knowledge database"""
        with open(output_path, 'w') as f:
            for atom in self.atoms.values():
                f.write(json.dumps(atom) + '\n')
                
        print(f"✅ Exported {len(self.atoms)} atoms to {output_path}")
        
    def create_statistics(self):
        """Generate statistics"""
        stats = {
            "total_atoms": len(self.atoms),
            "processed_files": len(self.processed_files),
            "skipped_paths": len(self.skipped_paths),
            "by_type": defaultdict(int),
            "by_category": defaultdict(int),
            "high_heat_atoms": 0,
            "most_mentioned": []
        }
        
        for atom in self.atoms.values():
            stats["by_type"][atom["type"]] += 1
            stats["by_category"][atom["category"]] += 1
            if atom["heat"] >= 0.8:
                stats["high_heat_atoms"] += 1
                
        # Most mentioned atoms
        sorted_atoms = sorted(self.atoms.values(), key=lambda x: x["mention_count"], reverse=True)
        stats["most_mentioned"] = [(a["content"], a["mention_count"]) for a in sorted_atoms[:10]]
        
        return stats

def main():
    atomizer = CRODCompleteAtomizer()
    
    print("🚀 CROD COMPLETE ATOMIZER STARTING...")
    
    # Process all directories
    base_dir = "/home/daniel/Schreibtisch/Crod Programming"
    atomizer.process_directory(base_dir)
    
    # Add research files
    atomizer.add_research_files()
    
    # Export master database
    output_path = "/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH/crod_master_knowledge.jsonl"
    atomizer.export_to_jsonl(output_path)
    
    # Create statistics
    stats = atomizer.create_statistics()
    
    print("\n📊 ATOMIZATION COMPLETE!")
    print(f"   🧠 Total atoms: {stats['total_atoms']}")
    print(f"   📁 Files processed: {stats['processed_files']}")
    print(f"   🚫 Files skipped: {stats['skipped_paths']}")
    print(f"   🔥 High heat atoms: {stats['high_heat_atoms']}")
    
    print("\n🎯 By Type:")
    for atom_type, count in sorted(stats["by_type"].items(), key=lambda x: x[1], reverse=True):
        print(f"   {atom_type}: {count}")
        
    print("\n🏆 Most Mentioned:")
    for content, count in stats["most_mentioned"][:5]:
        print(f"   {content}: {count} mentions")
    
    # Save statistics  
    stats_path = "/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH/atomization_stats.json"
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📈 Statistics saved to: {stats_path}")
    print("🌟 CROD KNOWLEDGE IS NOW FULLY ATOMIC! 🌟")

if __name__ == "__main__":
    main()