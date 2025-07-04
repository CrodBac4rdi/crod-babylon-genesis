#!/usr/bin/env python3
"""
Read ABSOLUTELY EVERYTHING - Every single file in CROD Programming
Including: Docker volumes, K8s configs, binaries, EVERYTHING!
"""

import os
import json
import mimetypes
from pathlib import Path
from collections import defaultdict

class AbsoluteEverythingReader:
    def __init__(self, max_tokens=95000):  # Leave some buffer
        self.max_tokens = max_tokens
        self.chars_per_token = 4
        self.max_chars = max_tokens * self.chars_per_token
        self.stats = defaultdict(int)
        
    def get_all_files(self, directory, exclude_patterns=None):
        """Get EVERY SINGLE FILE - no filters!"""
        if exclude_patterns is None:
            exclude_patterns = [
                'node_modules',  # Maybe include these too?
                '.git/objects',  # Git objects are binary
                '__pycache__',
                '.pyc',
                '.pyo'
            ]
            
        all_files = []
        total_size = 0
        
        print("🔍 Scanning EVERYTHING...")
        
        for root, dirs, files in os.walk(directory):
            # Skip some directories to avoid infinite recursion
            dirs[:] = [d for d in dirs if not any(pattern in os.path.join(root, d) for pattern in exclude_patterns)]
            
            for file in files:
                filepath = Path(root) / file
                try:
                    size = os.path.getsize(filepath)
                    total_size += size
                    
                    # Categorize files
                    ext = filepath.suffix.lower()
                    if ext:
                        self.stats[ext] += 1
                    else:
                        self.stats['no_extension'] += 1
                        
                    all_files.append({
                        'path': filepath,
                        'size': size,
                        'type': self.get_file_type(filepath),
                        'readable': self.is_readable(filepath)
                    })
                    
                except Exception as e:
                    self.stats['errors'] += 1
                    
        print(f"📊 Found {len(all_files)} files, Total size: {total_size / 1024 / 1024:.2f} MB")
        return all_files
        
    def get_file_type(self, filepath):
        """Determine file type"""
        mime_type, _ = mimetypes.guess_type(str(filepath))
        
        if mime_type:
            return mime_type.split('/')[0]
            
        # Check by extension
        ext = filepath.suffix.lower()
        
        # Code files
        if ext in ['.py', '.js', '.ts', '.go', '.rs', '.ex', '.exs', '.java', '.c', '.cpp', '.h']:
            return 'code'
            
        # Config files
        if ext in ['.yaml', '.yml', '.json', '.toml', '.conf', '.cfg', '.ini', '.env']:
            return 'config'
            
        # Docker/K8s
        if 'dockerfile' in str(filepath).lower() or ext in ['.dockerfile']:
            return 'docker'
        if ext in ['.yaml', '.yml'] and any(x in str(filepath).lower() for x in ['k8s', 'kubernetes', 'deployment', 'service']):
            return 'kubernetes'
            
        # Documentation
        if ext in ['.md', '.rst', '.txt', '.adoc']:
            return 'docs'
            
        # Data files
        if ext in ['.sql', '.db', '.sqlite', '.jsonl', '.csv', '.tsv']:
            return 'data'
            
        # Archives
        if ext in ['.zip', '.tar', '.gz', '.7z', '.rar']:
            return 'archive'
            
        # Binary
        if ext in ['.exe', '.bin', '.so', '.dll', '.dylib', '.wasm']:
            return 'binary'
            
        return 'unknown'
        
    def is_readable(self, filepath):
        """Check if file is text-readable"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read(1024)  # Try reading first 1KB
            return True
        except:
            return False
            
    def create_smart_batches(self, files):
        """Create batches optimized by file type and readability"""
        # Separate by type and readability
        categorized = defaultdict(list)
        
        for file_info in files:
            key = f"{file_info['type']}_{file_info['readable']}"
            categorized[key].append(file_info)
            
        batches = []
        batch_num = 0
        
        # Process readable files first
        for category, file_list in sorted(categorized.items(), key=lambda x: x[0].endswith('False')):
            print(f"\n📦 Processing category: {category} ({len(file_list)} files)")
            
            current_batch = []
            current_size = 0
            
            for file_info in sorted(file_list, key=lambda x: x['size']):
                estimated_tokens = file_info['size'] // self.chars_per_token
                
                if current_size + estimated_tokens > self.max_tokens and current_batch:
                    batch_num += 1
                    batches.append({
                        'number': batch_num,
                        'category': category,
                        'files': current_batch,
                        'estimated_tokens': current_size,
                        'file_count': len(current_batch)
                    })
                    current_batch = []
                    current_size = 0
                    
                current_batch.append(file_info)
                current_size += estimated_tokens
                
            if current_batch:
                batch_num += 1
                batches.append({
                    'number': batch_num,
                    'category': category,
                    'files': current_batch,
                    'estimated_tokens': current_size,
                    'file_count': len(current_batch)
                })
                
        return batches
        
    def analyze_everything(self, directory):
        """Analyze EVERYTHING and create reading plan"""
        files = self.get_all_files(directory)
        batches = self.create_smart_batches(files)
        
        analysis = {
            'directory': str(directory),
            'total_files': len(files),
            'total_batches': len(batches),
            'file_stats': dict(self.stats),
            'readable_files': sum(1 for f in files if f['readable']),
            'binary_files': sum(1 for f in files if not f['readable']),
            'batches': []
        }
        
        # Summarize batches
        for batch in batches:
            batch_summary = {
                'number': batch['number'],
                'category': batch['category'],
                'file_count': batch['file_count'],
                'estimated_tokens': batch['estimated_tokens'],
                'sample_files': [str(f['path']) for f in batch['files'][:5]]  # First 5 files
            }
            analysis['batches'].append(batch_summary)
            
        return analysis, batches

if __name__ == '__main__':
    reader = AbsoluteEverythingReader()
    
    # Analyze ENTIRE CROD Programming directory
    crod_dir = "/home/daniel/Schreibtisch/Crod Programming"
    
    print(f"🚀 READING ABSOLUTELY EVERYTHING IN: {crod_dir}")
    print("This includes: Code, Configs, Docker files, K8s YAMLs, Binaries, EVERYTHING!\n")
    
    analysis, full_batches = reader.analyze_everything(crod_dir)
    
    print("\n📊 COMPLETE ANALYSIS:")
    print(f"Total files: {analysis['total_files']:,}")
    print(f"Readable files: {analysis['readable_files']:,}")
    print(f"Binary files: {analysis['binary_files']:,}")
    print(f"Total batches: {analysis['total_batches']}")
    
    print("\n📈 FILE TYPE DISTRIBUTION:")
    for ext, count in sorted(analysis['file_stats'].items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {ext}: {count:,} files")
        
    print("\n📦 BATCH EXAMPLES:")
    for batch in analysis['batches'][:10]:  # First 10 batches
        print(f"\nBatch {batch['number']} ({batch['category']}): {batch['file_count']} files, ~{batch['estimated_tokens']:,} tokens")
        for f in batch['sample_files'][:3]:
            print(f"  - {f}")
            
    # Save complete plan
    with open('crod_complete_reading_plan.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    # Save full batch details
    with open('crod_full_batches.json', 'w') as f:
        # Convert Path objects to strings
        serializable_batches = []
        for batch in full_batches:
            batch_copy = batch.copy()
            batch_copy['files'] = [
                {**f, 'path': str(f['path'])} 
                for f in batch['files']
            ]
            serializable_batches.append(batch_copy)
        json.dump(serializable_batches, f, indent=2)
    
    print("\n✅ Complete reading plan saved!")
    print("📖 Now I can REALLY read EVERYTHING in your CROD universe!")
    print(f"🔥 Ready to process {analysis['total_batches']} batches systematically!")