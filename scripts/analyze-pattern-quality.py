#!/usr/bin/env python3
"""
Analyze pattern quality between COMPLETE and CLEAN universes
Check for duplicates, nulls, and actual unique patterns
"""

import json
from collections import defaultdict

def analyze_patterns():
    complete_patterns = {}
    clean_patterns = {}
    
    # Load COMPLETE patterns
    print("Loading COMPLETE patterns...")
    with open('training/knowledge/universe/universe_patterns.jsonl', 'r') as f:
        for line in f:
            if line.strip():
                try:
                    p = json.loads(line)
                    if p.get('pattern_id') is not None:
                        complete_patterns[p['pattern_id']] = p
                except:
                    pass
    
    # Load CLEAN patterns
    print("Loading CLEAN patterns...")
    null_count = 0
    with open('training/knowledge/clean-universe/clean_patterns.jsonl', 'r') as f:
        for line in f:
            if line.strip():
                try:
                    p = json.loads(line)
                    if p.get('pattern_id') is not None:
                        clean_patterns[p['pattern_id']] = p
                    else:
                        null_count += 1
                except:
                    pass
    
    # Analysis
    complete_ids = set(complete_patterns.keys())
    clean_ids = set(clean_patterns.keys())
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"COMPLETE patterns: {len(complete_patterns):,}")
    print(f"CLEAN patterns (non-null): {len(clean_patterns):,}")
    print(f"CLEAN null patterns: {null_count:,}")
    
    print(f"\nShared patterns: {len(complete_ids & clean_ids):,}")
    print(f"Unique to COMPLETE: {len(complete_ids - clean_ids):,}")
    print(f"Unique to CLEAN: {len(clean_ids - complete_ids):,}")
    
    # Check if they're identical
    if complete_ids == clean_ids:
        print("\n⚠️ WARNING: Pattern IDs are identical!")
        print("CLEAN's extra 50k patterns are all NULL/invalid!")
    
    # Sample quality check
    print(f"\n🔍 Quality Check (first different pattern):")
    for pid in sorted(complete_ids | clean_ids)[:1000]:
        if pid in complete_patterns and pid in clean_patterns:
            cp = complete_patterns[pid]
            clp = clean_patterns[pid]
            if cp != clp:
                print(f"Pattern {pid} differs:")
                print(f"  COMPLETE: {cp.get('atoms')} strength={cp.get('strength')}")
                print(f"  CLEAN: {clp.get('atoms')} strength={clp.get('strength')}")
                break

if __name__ == "__main__":
    analyze_patterns()