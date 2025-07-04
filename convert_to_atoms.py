#!/usr/bin/env python3
"""
Convert all CROD knowledge to atomic JSONL format
ATOMS → PATTERNS → CHAINS → NETWORKS
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def extract_atoms_from_md(file_path, content):
    """Extract atomic knowledge from markdown"""
    atoms = []
    
    # Extract headers as structural atoms
    headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    for header in headers:
        atoms.append({
            "atom": header.strip(),
            "type": "concept",
            "source": str(file_path),
            "heat": 0.5,
            "category": "structure"
        })
    
    # Extract technologies mentioned
    tech_patterns = [
        r'\b(eBPF|XDP|DPDK|SPDK|NATS|Redis|Docker|CRI-O|HTTP/3|QUIC)\b',
        r'\b(WebGPU|WebNN|WebAssembly|WASM|WebTransport|WebCodecs)\b',
        r'\b(Kubernetes|K8s|PostgreSQL|Elixir|Rust|Go|Python)\b',
        r'\b(Intel AMX|ARM|RISC-V|CXL|RDMA|InfiniBand)\b'
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            atoms.append({
                "atom": match.lower(),
                "type": "technology", 
                "source": str(file_path),
                "heat": 0.8,
                "category": "tech"
            })
    
    # Extract performance numbers
    perf_pattern = r'(\d+(?:\.\d+)?)\s*(?:x|%|M|k|GB|ms|μs)\s+(faster|improvement|packets|ops|latency|bandwidth)'
    perf_matches = re.findall(perf_pattern, content, re.IGNORECASE)
    for value, metric in perf_matches:
        atoms.append({
            "atom": f"{value}_{metric}",
            "type": "performance",
            "source": str(file_path),
            "heat": 0.9,
            "category": "metrics",
            "value": float(value) if '.' in value else int(value)
        })
    
    return atoms

def convert_directory_to_atoms(directory):
    """Convert all markdown files to atoms"""
    all_atoms = []
    
    for md_file in Path(directory).rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                atoms = extract_atoms_from_md(md_file, content)
                all_atoms.extend(atoms)
                print(f"✅ Processed {md_file}: {len(atoms)} atoms")
        except Exception as e:
            print(f"❌ Error processing {md_file}: {e}")
    
    return all_atoms

def create_patterns_from_atoms(atoms):
    """Create patterns by grouping related atoms"""
    patterns = []
    
    # Group by source file
    by_source = {}
    for atom in atoms:
        source = atom['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(atom)
    
    # Create patterns for each source
    for source, source_atoms in by_source.items():
        if len(source_atoms) >= 3:  # Minimum atoms for pattern
            pattern = {
                "pattern": f"knowledge_{Path(source).stem}",
                "atoms": [atom['atom'] for atom in source_atoms],
                "strength": sum(atom['heat'] for atom in source_atoms) / len(source_atoms),
                "source": source,
                "type": "knowledge_pattern",
                "created": datetime.now().isoformat()
            }
            patterns.append(pattern)
    
    return patterns

def main():
    crod_dir = "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7"
    output_dir = "/home/daniel/Schreibtisch/Crod Programming/CROD-2025-RESEARCH"
    
    print("🔄 Converting CROD knowledge to atoms...")
    atoms = convert_directory_to_atoms(crod_dir)
    
    print(f"🧠 Extracted {len(atoms)} atoms")
    
    # Save atoms
    atoms_file = Path(output_dir) / "crod_atoms.jsonl"
    with open(atoms_file, 'w') as f:
        for atom in atoms:
            f.write(json.dumps(atom) + '\n')
    
    print("🔗 Creating patterns from atoms...")
    patterns = create_patterns_from_atoms(atoms)
    
    print(f"🎯 Created {len(patterns)} patterns")
    
    # Save patterns
    patterns_file = Path(output_dir) / "crod_patterns.jsonl"  
    with open(patterns_file, 'w') as f:
        for pattern in patterns:
            f.write(json.dumps(pattern) + '\n')
    
    print("✅ CROD knowledge atomized!")
    print(f"📁 Files: {atoms_file}, {patterns_file}")

if __name__ == "__main__":
    main()