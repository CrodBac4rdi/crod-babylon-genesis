#!/usr/bin/env python3
"""
Smart Batch Reader - Reads EVERYTHING in 100k token batches
"""

import os
import json
from pathlib import Path

class SmartBatchReader:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.chars_per_token = 4  # Rough estimate
        self.max_chars = max_tokens * self.chars_per_token
        
    def get_all_files(self, directory, extensions=['.py', '.js', '.md', '.json']):
        """Get all relevant files"""
        files = []
        for ext in extensions:
            files.extend(Path(directory).rglob(f'*{ext}'))
        return files
        
    def estimate_size(self, filepath):
        """Estimate file size in tokens"""
        try:
            size = os.path.getsize(filepath)
            return size // self.chars_per_token
        except:
            return 0
            
    def create_batches(self, files):
        """Create optimal batches under 100k tokens"""
        batches = []
        current_batch = []
        current_size = 0
        
        # Sort by size for better packing
        files_with_size = [(f, self.estimate_size(f)) for f in files]
        files_with_size.sort(key=lambda x: x[1])
        
        for filepath, size in files_with_size:
            if current_size + size > self.max_tokens and current_batch:
                batches.append(current_batch)
                current_batch = []
                current_size = 0
                
            current_batch.append(filepath)
            current_size += size
            
        if current_batch:
            batches.append(current_batch)
            
        return batches
        
    def read_batch(self, batch):
        """Read a batch of files"""
        contents = {}
        total_chars = 0
        
        for filepath in batch:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if total_chars + len(content) < self.max_chars:
                        contents[str(filepath)] = content
                        total_chars += len(content)
                    else:
                        # Partial read
                        remaining = self.max_chars - total_chars
                        contents[str(filepath)] = content[:remaining] + "\n[TRUNCATED]"
                        break
            except:
                contents[str(filepath)] = "[ERROR READING FILE]"
                
        return contents
        
    def analyze_codebase(self, directory):
        """Analyze entire codebase in batches"""
        print(f"🔍 Analyzing {directory}")
        
        files = self.get_all_files(directory)
        print(f"📁 Found {len(files)} files")
        
        batches = self.create_batches(files)
        print(f"📦 Created {len(batches)} batches")
        
        analysis = {
            'total_files': len(files),
            'total_batches': len(batches),
            'batches': []
        }
        
        for i, batch in enumerate(batches):
            batch_info = {
                'batch_number': i + 1,
                'files_count': len(batch),
                'files': [str(f) for f in batch],
                'estimated_tokens': sum(self.estimate_size(f) for f in batch)
            }
            analysis['batches'].append(batch_info)
            
        return analysis

if __name__ == '__main__':
    reader = SmartBatchReader()
    
    # Analyze CROD codebase
    crod_dir = "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7"
    analysis = reader.analyze_codebase(crod_dir)
    
    print("\n📊 BATCH PLAN:")
    print(f"Total files: {analysis['total_files']}")
    print(f"Total batches needed: {analysis['total_batches']}")
    
    for batch in analysis['batches'][:5]:  # Show first 5 batches
        print(f"\nBatch {batch['batch_number']}: {batch['files_count']} files, ~{batch['estimated_tokens']} tokens")
        for f in batch['files'][:3]:  # Show first 3 files
            print(f"  - {f}")
            
    # Save plan
    with open('crod_reading_plan.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    print("\n✅ Reading plan saved to crod_reading_plan.json")
    print("📖 Now I can read everything systematically!")