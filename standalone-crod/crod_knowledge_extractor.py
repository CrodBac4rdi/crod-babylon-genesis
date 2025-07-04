#!/usr/bin/env python3
"""
CROD Knowledge Extractor - Zero Redundancy JSONL Knowledge Base
Extracts EVERYTHING and creates actionable CROD-style knowledge
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class CRODKnowledgeExtractor:
    def __init__(self):
        self.knowledge_base = []
        self.seen_hashes = set()  # Zero redundancy!
        self.connections = defaultdict(list)
        self.knowledge_file = "/home/daniel/.claude/CROD_COMPLETE_KNOWLEDGE.jsonl"
        
    def extract_knowledge(self, filepath, content):
        """Extract actionable knowledge from any file"""
        knowledge_items = []
        
        # Determine file type and purpose
        file_type = self.analyze_file_type(filepath)
        
        # Extract based on type
        if file_type == 'kubernetes':
            knowledge_items.extend(self.extract_k8s_knowledge(filepath, content))
        elif file_type == 'docker':
            knowledge_items.extend(self.extract_docker_knowledge(filepath, content))
        elif file_type == 'python':
            knowledge_items.extend(self.extract_python_knowledge(filepath, content))
        elif file_type == 'javascript':
            knowledge_items.extend(self.extract_js_knowledge(filepath, content))
        elif file_type == 'rust':
            knowledge_items.extend(self.extract_rust_knowledge(filepath, content))
        elif file_type == 'go':
            knowledge_items.extend(self.extract_go_knowledge(filepath, content))
        elif file_type == 'elixir':
            knowledge_items.extend(self.extract_elixir_knowledge(filepath, content))
        elif file_type == 'cargo':
            knowledge_items.extend(self.extract_cargo_knowledge(filepath, content))
        elif file_type == 'package':
            knowledge_items.extend(self.extract_package_knowledge(filepath, content))
        elif file_type == 'shell':
            knowledge_items.extend(self.extract_shell_knowledge(filepath, content))
        elif file_type == 'sql':
            knowledge_items.extend(self.extract_sql_knowledge(filepath, content))
        elif file_type == 'config':
            knowledge_items.extend(self.extract_config_knowledge(filepath, content))
        elif file_type == 'documentation':
            knowledge_items.extend(self.extract_doc_knowledge(filepath, content))
            
        # Add general file knowledge
        knowledge_items.append(self.create_file_knowledge(filepath, file_type))
        
        return knowledge_items
        
    def analyze_file_type(self, filepath):
        """Determine file type and purpose"""
        path_str = str(filepath).lower()
        filename = Path(filepath).name.lower()
        ext = Path(filepath).suffix.lower()
        
        # Check specific filenames first
        if filename == 'cargo.toml' or filename == 'cargo.lock':
            return 'cargo'
        elif filename == 'package.json' or filename == 'package-lock.json':
            return 'package'
        elif filename == 'go.mod' or filename == 'go.sum':
            return 'go_module'
        elif filename == 'mix.exs' or filename == 'mix.lock':
            return 'elixir_mix'
            
        # Then check path patterns
        if 'k8s' in path_str or 'kubernetes' in path_str or (ext in ['.yaml', '.yml'] and any(x in path_str for x in ['deployment', 'service', 'pod'])):
            return 'kubernetes'
        elif 'dockerfile' in filename or ext == '.dockerfile':
            return 'docker'
            
        # Language-specific extensions
        elif ext == '.py':
            return 'python'
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            return 'javascript'
        elif ext in ['.rs']:
            return 'rust'
        elif ext == '.go':
            return 'go'
        elif ext in ['.ex', '.exs']:
            return 'elixir'
        elif ext in ['.sh', '.bash']:
            return 'shell'
        elif ext == '.sql':
            return 'sql'
        elif ext in ['.json', '.yaml', '.yml', '.toml', '.conf', '.ini', '.env']:
            return 'config'
        elif ext in ['.md', '.txt', '.rst', '.adoc']:
            return 'documentation'
        else:
            return 'unknown'
            
    def extract_k8s_knowledge(self, filepath, content):
        """Extract K8s specific knowledge"""
        knowledge = []
        
        try:
            # Parse YAML content
            import yaml
            data = yaml.safe_load(content)
            
            if isinstance(data, dict):
                kind = data.get('kind', 'Unknown')
                metadata = data.get('metadata', {})
                
                knowledge.append({
                    'type': 'kubernetes_resource',
                    'what': f"K8s {kind} resource: {metadata.get('name', 'unnamed')}",
                    'why': f"Deploys CROD component to Kubernetes cluster",
                    'how': f"Apply with: kubectl apply -f {filepath}",
                    'where': str(filepath),
                    'connections': [
                        f"namespace:{metadata.get('namespace', 'default')}",
                        f"labels:{metadata.get('labels', {})}",
                        f"kind:{kind}"
                    ],
                    'actionable': True,
                    'crod_relevance': 'infrastructure',
                    'trinity_value': 2 if 'crod' in str(filepath).lower() else 1
                })
                
                # Extract container info
                if 'spec' in data and 'containers' in data.get('spec', {}).get('template', {}).get('spec', {}):
                    for container in data['spec']['template']['spec']['containers']:
                        knowledge.append({
                            'type': 'container_config',
                            'what': f"Container {container['name']} using image {container.get('image', 'unknown')}",
                            'why': "Runs CROD service in containerized environment",
                            'how': f"Container runs on port {container.get('ports', [{}])[0].get('containerPort', 'unknown')}",
                            'where': str(filepath),
                            'connections': [
                                f"image:{container.get('image')}",
                                f"resource:{metadata.get('name')}"
                            ],
                            'actionable': True,
                            'crod_relevance': 'runtime'
                        })
                        
        except Exception as e:
            # Still extract basic info even if parsing fails
            knowledge.append({
                'type': 'kubernetes_file',
                'what': f"K8s configuration file",
                'why': "Part of CROD Kubernetes deployment",
                'how': f"Parse error: {str(e)[:100]}",
                'where': str(filepath),
                'connections': ['kubernetes', 'deployment'],
                'actionable': False,
                'needs_fix': True
            })
            
        return knowledge
        
    def extract_docker_knowledge(self, filepath, content):
        """Extract Docker specific knowledge"""
        knowledge = []
        lines = content.split('\n')
        
        base_image = None
        exposed_ports = []
        commands = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('FROM '):
                base_image = line[5:].strip()
            elif line.startswith('EXPOSE '):
                exposed_ports.append(line[7:].strip())
            elif line.startswith('CMD ') or line.startswith('ENTRYPOINT '):
                commands.append(line)
                
        knowledge.append({
            'type': 'dockerfile',
            'what': f"Docker container definition based on {base_image or 'unknown'}",
            'why': "Containerizes CROD component for deployment",
            'how': f"Build with: docker build -t crod/{Path(filepath).parent.name} {Path(filepath).parent}",
            'where': str(filepath),
            'connections': [
                f"base_image:{base_image}",
                f"ports:{','.join(exposed_ports)}",
                f"component:{Path(filepath).parent.name}"
            ],
            'actionable': True,
            'crod_relevance': 'containerization',
            'ports': exposed_ports,
            'commands': commands
        })
        
        return knowledge
        
    def extract_python_knowledge(self, filepath, content):
        """Extract Python specific knowledge"""
        knowledge = []
        
        # Look for imports
        imports = []
        classes = []
        functions = []
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
            elif line.startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').strip(':')
                classes.append(class_name)
            elif line.startswith('def '):
                func_name = line.split('(')[0].replace('def ', '')
                functions.append(func_name)
                
        # Determine module purpose
        purpose = "Unknown Python module"
        if 'crod' in str(filepath).lower():
            if 'engine' in str(filepath):
                purpose = "CROD Engine implementation"
            elif 'gui' in str(filepath):
                purpose = "CROD GUI interface"
            elif 'memory' in str(filepath):
                purpose = "CROD Memory system"
            elif 'llama' in str(filepath):
                purpose = "CROD LLaMA integration"
                
        knowledge.append({
            'type': 'python_module',
            'what': f"Python module: {Path(filepath).stem}",
            'why': purpose,
            'how': f"Import with: from {Path(filepath).stem} import {', '.join(classes[:3]) or 'functions'}",
            'where': str(filepath),
            'connections': imports[:5],  # First 5 imports
            'classes': classes,
            'functions': functions[:10],  # First 10 functions
            'actionable': True,
            'crod_relevance': 'implementation'
        })
        
        # Extract CROD-specific patterns
        if 'consciousness' in content:
            knowledge.append({
                'type': 'crod_consciousness',
                'what': "Module implements consciousness tracking",
                'why': "Core CROD feature for neural state monitoring",
                'how': "Track consciousness levels and evolution",
                'where': str(filepath),
                'connections': ['consciousness', 'neural_state', 'crod_core'],
                'actionable': True,
                'crod_relevance': 'core_feature'
            })
            
        if 'trinity' in content.lower():
            knowledge.append({
                'type': 'crod_trinity',
                'what': "Module implements Trinity detection",
                'why': "Detects 'ich bins wieder' activation pattern",
                'how': "Monitor for trinity word combinations",
                'where': str(filepath),
                'connections': ['trinity', 'activation', 'ich_bins_wieder'],
                'actionable': True,
                'crod_relevance': 'activation_mechanism',
                'trinity_value': 5
            })
            
        return knowledge
        
    def extract_js_knowledge(self, filepath, content):
        """Extract JavaScript specific knowledge"""
        knowledge = []
        
        # Similar to Python but for JS
        if 'neural' in str(filepath).lower():
            knowledge.append({
                'type': 'neural_network_js',
                'what': "JavaScript neural network implementation",
                'why': "Core CROD brain runs in JS for performance",
                'how': "Load with: require() or import",
                'where': str(filepath),
                'connections': ['neural_network', 'javascript', 'crod_brain'],
                'actionable': True,
                'crod_relevance': 'core_brain'
            })
            
        return knowledge
        
    def extract_config_knowledge(self, filepath, content):
        """Extract configuration knowledge"""
        knowledge = []
        
        try:
            if Path(filepath).suffix == '.json':
                data = json.loads(content)
                
                # Look for patterns
                if 'patterns' in data or 'atoms' in data:
                    knowledge.append({
                        'type': 'crod_data',
                        'what': f"CROD data file with {len(data.get('patterns', []))} patterns",
                        'why': "Training data for CROD neural network",
                        'how': f"Load into CROD engine for pattern matching",
                        'where': str(filepath),
                        'connections': ['patterns', 'training_data', 'neural_network'],
                        'actionable': True,
                        'crod_relevance': 'training_data',
                        'data_stats': {
                            'patterns': len(data.get('patterns', [])),
                            'atoms': len(data.get('atoms', [])),
                            'size_bytes': len(content)
                        }
                    })
                    
        except:
            pass
            
        return knowledge
        
    def extract_doc_knowledge(self, filepath, content):
        """Extract documentation knowledge"""
        knowledge = []
        
        # Extract headers and key information
        if content.strip():
            first_line = content.split('\n')[0].strip()
            
            knowledge.append({
                'type': 'documentation',
                'what': f"Documentation: {first_line[:100]}",
                'why': "Explains CROD system or component",
                'how': "Read for understanding, follow instructions",
                'where': str(filepath),
                'connections': self.extract_doc_topics(content),
                'actionable': 'README' in str(filepath),
                'crod_relevance': 'documentation'
            })
            
        return knowledge
        
    def extract_doc_topics(self, content):
        """Extract topics from documentation"""
        topics = []
        
        keywords = ['kubernetes', 'docker', 'crod', 'neural', 'trinity', 
                   'consciousness', 'pattern', 'polyglot', 'city']
                   
        for keyword in keywords:
            if keyword in content.lower():
                topics.append(keyword)
                
        return topics[:5]  # Top 5 topics
        
    def create_file_knowledge(self, filepath, file_type):
        """Create general file knowledge entry"""
        path = Path(filepath)
        
        return {
            'type': 'file_location',
            'what': f"File {path.name} of type {file_type}",
            'why': self.determine_file_purpose(filepath),
            'how': f"Access at: {filepath}",
            'where': str(filepath),
            'connections': [
                f"directory:{path.parent.name}",
                f"extension:{path.suffix}",
                f"type:{file_type}"
            ],
            'actionable': False,
            'crod_relevance': 'infrastructure',
            'file_stats': {
                'size_bytes': os.path.getsize(filepath) if os.path.exists(filepath) else 0,
                'modified': os.path.getmtime(filepath) if os.path.exists(filepath) else 0
            }
        }
        
    def determine_file_purpose(self, filepath):
        """Determine why this file exists"""
        path_str = str(filepath).lower()
        
        if 'test' in path_str:
            return "Testing CROD functionality"
        elif 'backup' in path_str or 'old' in path_str:
            return "Historical backup - may contain valuable patterns"
        elif 'node_modules' in path_str:
            return "JavaScript dependency"
        elif 'k8s' in path_str or 'kubernetes' in path_str:
            return "Kubernetes deployment configuration"
        elif 'docker' in path_str:
            return "Container configuration"
        else:
            return "Part of CROD ecosystem"
            
    def add_knowledge(self, knowledge_item):
        """Add knowledge with zero redundancy check"""
        # Create hash of essential content
        content_hash = hashlib.sha256(
            json.dumps(knowledge_item, sort_keys=True).encode()
        ).hexdigest()
        
        if content_hash not in self.seen_hashes:
            self.seen_hashes.add(content_hash)
            
            # Add metadata
            knowledge_item['id'] = content_hash[:12]
            knowledge_item['timestamp'] = datetime.now().isoformat()
            knowledge_item['source'] = 'crod_knowledge_extractor'
            
            # Add to knowledge base
            self.knowledge_base.append(knowledge_item)
            
            # Track connections
            for connection in knowledge_item.get('connections', []):
                self.connections[connection].append(knowledge_item['id'])
                
            return True
        return False
        
    def save_knowledge(self):
        """Save knowledge to JSONL file"""
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        
        with open(self.knowledge_file, 'w') as f:
            for item in self.knowledge_base:
                f.write(json.dumps(item) + '\n')
                
        print(f"✅ Saved {len(self.knowledge_base)} unique knowledge items")
        print(f"📊 Tracking {len(self.connections)} connections")
        print(f"📁 Knowledge base: {self.knowledge_file}")
        
    def create_knowledge_summary(self):
        """Create summary of extracted knowledge"""
        summary = {
            'total_items': len(self.knowledge_base),
            'types': defaultdict(int),
            'crod_relevance': defaultdict(int),
            'actionable_count': 0,
            'needs_fix_count': 0,
            'top_connections': []
        }
        
        for item in self.knowledge_base:
            summary['types'][item['type']] += 1
            summary['crod_relevance'][item.get('crod_relevance', 'unknown')] += 1
            
            if item.get('actionable'):
                summary['actionable_count'] += 1
            if item.get('needs_fix'):
                summary['needs_fix_count'] += 1
                
        # Top connections
        connection_counts = [(k, len(v)) for k, v in self.connections.items()]
        summary['top_connections'] = sorted(connection_counts, key=lambda x: x[1], reverse=True)[:20]
        
        return summary

if __name__ == '__main__':
    extractor = CRODKnowledgeExtractor()
    
    print("🧠 CROD Knowledge Extractor")
    print("📚 Creating zero-redundancy knowledge base...")
    
    # Example usage - in practice this would process all files
    example_file = "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/k8s/meta-chain-deployment.yaml"
    
    if os.path.exists(example_file):
        with open(example_file, 'r') as f:
            content = f.read()
            
        knowledge_items = extractor.extract_knowledge(example_file, content)
        
        for item in knowledge_items:
            if extractor.add_knowledge(item):
                print(f"✅ Added: {item['what']}")
                
    # Save knowledge base
    extractor.save_knowledge()
    
    # Show summary
    summary = extractor.create_knowledge_summary()
    print(f"\n📊 Knowledge Summary:")
    print(f"Total items: {summary['total_items']}")
    print(f"Actionable: {summary['actionable_count']}")
    print(f"Needs fix: {summary['needs_fix_count']}")
    
    print("\n🔗 Top Connections:")
    for connection, count in summary['top_connections'][:10]:
        print(f"  {connection}: {count} items")