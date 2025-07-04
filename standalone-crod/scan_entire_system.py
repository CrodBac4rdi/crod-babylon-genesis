#!/usr/bin/env python3
"""
COMPLETE SYSTEM SCANNER - Find EVERYTHING Daniel has installed/created
Not just CROD Programming - THE ENTIRE SYSTEM!
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

class CompleteSystemScanner:
    def __init__(self):
        self.results = {
            'python_packages': [],
            'npm_packages': [],
            'system_packages': [],
            'docker_images': [],
            'docker_containers': [],
            'k8s_resources': [],
            'databases': [],
            'services': [],
            'user_directories': [],
            'development_tools': [],
            'ai_models': [],
            'custom_scripts': [],
            'config_files': [],
            'cron_jobs': [],
            'systemd_services': [],
            'network_ports': [],
            'environment_vars': {},
            'redis_info': {},
            'ollama_models': [],
            'vscode_extensions': [],
            'shell_history': [],
            'git_repos': []
        }
        
    def scan_everything(self):
        """Scan the ENTIRE system for Daniel's setup"""
        print("🔍 COMPLETE SYSTEM SCAN STARTING...")
        print("This will find EVERYTHING you have access to!\n")
        
        # Python packages
        self.scan_python_packages()
        
        # NPM packages
        self.scan_npm_packages()
        
        # System packages (apt)
        self.scan_system_packages()
        
        # Docker
        self.scan_docker()
        
        # Kubernetes
        self.scan_kubernetes()
        
        # Databases
        self.scan_databases()
        
        # Services and processes
        self.scan_services()
        
        # User directories
        self.scan_user_directories()
        
        # Development tools
        self.scan_dev_tools()
        
        # AI Models (Ollama)
        self.scan_ai_models()
        
        # Custom scripts and configs
        self.scan_custom_files()
        
        # Network and ports
        self.scan_network()
        
        # Environment
        self.scan_environment()
        
        # Git repositories
        self.scan_git_repos()
        
        return self.results
        
    def scan_python_packages(self):
        """Get all Python packages"""
        try:
            # pip list
            result = subprocess.run(['pip3', 'list', '--format=json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.results['python_packages'] = json.loads(result.stdout)
                print(f"✅ Found {len(self.results['python_packages'])} Python packages")
                
            # Also check user packages
            user_result = subprocess.run(['pip3', 'list', '--user', '--format=json'], 
                                       capture_output=True, text=True)
            if user_result.returncode == 0:
                user_packages = json.loads(user_result.stdout)
                print(f"  📦 {len(user_packages)} in user space")
        except Exception as e:
            print(f"❌ Python scan error: {e}")
            
    def scan_npm_packages(self):
        """Get all NPM packages"""
        try:
            # Global packages
            result = subprocess.run(['npm', 'list', '-g', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                npm_data = json.loads(result.stdout)
                self.results['npm_packages'] = list(npm_data.get('dependencies', {}).keys())
                print(f"✅ Found {len(self.results['npm_packages'])} global NPM packages")
        except Exception as e:
            print(f"❌ NPM scan error: {e}")
            
    def scan_system_packages(self):
        """Get installed system packages"""
        try:
            # Get all installed packages
            result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                packages = []
                for line in lines:
                    if line.startswith('ii'):
                        parts = line.split()
                        if len(parts) >= 3:
                            packages.append({
                                'name': parts[1],
                                'version': parts[2]
                            })
                            
                # Filter for development/Daniel-installed packages
                keywords = ['python', 'node', 'docker', 'kubectl', 'k3s', 'redis', 
                           'postgres', 'mysql', 'mongodb', 'nginx', 'git', 'build-essential',
                           'ollama', 'cuda', 'nvidia', 'tensorflow', 'torch']
                           
                relevant_packages = [p for p in packages 
                                   if any(k in p['name'].lower() for k in keywords)]
                
                self.results['system_packages'] = relevant_packages
                print(f"✅ Found {len(relevant_packages)} relevant system packages")
        except Exception as e:
            print(f"❌ System package scan error: {e}")
            
    def scan_docker(self):
        """Get Docker images and containers"""
        try:
            # Docker images
            result = subprocess.run(['docker', 'images', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        self.results['docker_images'].append(json.loads(line))
                print(f"✅ Found {len(self.results['docker_images'])} Docker images")
                
            # Docker containers
            result = subprocess.run(['docker', 'ps', '-a', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        self.results['docker_containers'].append(json.loads(line))
                print(f"✅ Found {len(self.results['docker_containers'])} Docker containers")
        except Exception as e:
            print(f"❌ Docker scan error: {e}")
            
    def scan_kubernetes(self):
        """Get Kubernetes resources"""
        try:
            # Export kubeconfig
            os.environ['KUBECONFIG'] = os.path.expanduser('~/.kube/config')
            
            # Get all namespaces
            result = subprocess.run(['kubectl', 'get', 'all', '--all-namespaces', '-o', 'json'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                k8s_data = json.loads(result.stdout)
                self.results['k8s_resources'] = {
                    'total_items': len(k8s_data.get('items', [])),
                    'namespaces': [],
                    'pods': [],
                    'services': []
                }
                
                for item in k8s_data.get('items', []):
                    kind = item.get('kind', '')
                    if kind == 'Pod':
                        self.results['k8s_resources']['pods'].append(item['metadata']['name'])
                    elif kind == 'Service':
                        self.results['k8s_resources']['services'].append(item['metadata']['name'])
                        
                print(f"✅ Found {len(self.results['k8s_resources']['pods'])} K8s pods")
        except Exception as e:
            print(f"❌ Kubernetes scan error: {e}")
            
    def scan_databases(self):
        """Find all databases"""
        databases = []
        
        # SQLite databases
        for root, dirs, files in os.walk('/home/daniel'):
            for file in files:
                if file.endswith('.db') or file.endswith('.sqlite'):
                    databases.append({
                        'type': 'sqlite',
                        'path': os.path.join(root, file)
                    })
                    
        # Redis
        try:
            result = subprocess.run(['redis-cli', 'INFO'], capture_output=True, text=True)
            if result.returncode == 0:
                self.results['redis_info'] = {'status': 'running', 'info': result.stdout[:500]}
                databases.append({'type': 'redis', 'status': 'running'})
        except:
            pass
            
        self.results['databases'] = databases
        print(f"✅ Found {len(databases)} databases")
        
    def scan_services(self):
        """Get running services"""
        try:
            # Systemd services
            result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '.service' in line and any(k in line.lower() for k in 
                        ['crod', 'docker', 'k3s', 'redis', 'ollama', 'postgres', 'nginx']):
                        self.results['services'].append(line.strip())
                        
            print(f"✅ Found {len(self.results['services'])} relevant services")
        except Exception as e:
            print(f"❌ Service scan error: {e}")
            
    def scan_user_directories(self):
        """Scan user directories for projects"""
        home = Path.home()
        
        important_dirs = []
        for path in [home / 'Schreibtisch', home / 'Documents', home / 'Projects', 
                     home / 'workspace', home / '.config', home / '.local']:
            if path.exists():
                # Find directories with code/projects
                for item in path.rglob('*'):
                    if item.is_dir() and any(marker in item.parts for marker in 
                        ['crod', 'CROD', 'programming', 'code', 'dev', 'src']):
                        important_dirs.append(str(item))
                        
        self.results['user_directories'] = important_dirs[:50]  # Top 50
        print(f"✅ Found {len(important_dirs)} project directories")
        
    def scan_dev_tools(self):
        """Check installed development tools"""
        tools = []
        
        # Check for common tools
        tool_commands = {
            'git': '--version',
            'node': '--version',
            'npm': '--version',
            'python3': '--version',
            'pip3': '--version',
            'docker': '--version',
            'kubectl': 'version --client',
            'k3s': '--version',
            'cargo': '--version',
            'rustc': '--version',
            'go': 'version',
            'elixir': '--version',
            'mix': '--version',
            'redis-cli': '--version',
            'psql': '--version',
            'mysql': '--version',
            'ollama': '--version',
            'code': '--version',  # VS Code
            'nvim': '--version',
            'vim': '--version'
        }
        
        for tool, version_arg in tool_commands.items():
            try:
                result = subprocess.run([tool] + version_arg.split(), 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    tools.append({
                        'tool': tool,
                        'version': result.stdout.strip().split('\n')[0]
                    })
            except:
                pass
                
        self.results['development_tools'] = tools
        print(f"✅ Found {len(tools)} development tools")
        
    def scan_ai_models(self):
        """Check Ollama models"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line:
                        parts = line.split()
                        if parts:
                            self.results['ollama_models'].append({
                                'name': parts[0],
                                'size': parts[1] if len(parts) > 1 else 'unknown'
                            })
                            
                print(f"✅ Found {len(self.results['ollama_models'])} Ollama models")
        except Exception as e:
            print(f"❌ Ollama scan error: {e}")
            
    def scan_custom_files(self):
        """Find custom scripts and configs"""
        # Shell scripts in home
        scripts = []
        configs = []
        
        home = Path.home()
        
        # Find shell scripts
        for script in home.rglob('*.sh'):
            if 'crod' in str(script).lower():
                scripts.append(str(script))
                
        # Important config files
        config_paths = [
            home / '.bashrc',
            home / '.zshrc',
            home / '.config' / 'Code' / 'User' / 'settings.json',
            home / '.claude' / 'CLAUDE.md',
            '/etc/docker/daemon.json',
            '/etc/systemd/system/'
        ]
        
        for config in config_paths:
            if Path(config).exists():
                configs.append(str(config))
                
        self.results['custom_scripts'] = scripts[:50]
        self.results['config_files'] = configs
        print(f"✅ Found {len(scripts)} custom scripts, {len(configs)} config files")
        
    def scan_network(self):
        """Check network ports and services"""
        try:
            # Get listening ports
            result = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line and any(port in line for port in 
                        ['3000', '5000', '8000', '8080', '8888', '6379', '5432', '27017',
                         '30000', '30001', '30002', '30888', '30889']):  # K8s NodePorts
                        self.results['network_ports'].append(line.strip())
                        
                print(f"✅ Found {len(self.results['network_ports'])} relevant ports")
        except:
            pass
            
    def scan_environment(self):
        """Get environment variables"""
        # Only get relevant ones
        relevant_vars = ['PATH', 'PYTHONPATH', 'NODE_PATH', 'KUBECONFIG', 
                        'DOCKER_HOST', 'GOPATH', 'CARGO_HOME', 'RUSTUP_HOME']
                        
        for var in relevant_vars:
            if var in os.environ:
                self.results['environment_vars'][var] = os.environ[var]
                
        print(f"✅ Captured {len(self.results['environment_vars'])} environment variables")
        
    def scan_git_repos(self):
        """Find all git repositories"""
        repos = []
        
        # Search common locations
        search_paths = [
            Path.home() / 'Schreibtisch',
            Path.home() / 'Documents',
            Path.home() / 'Projects',
            Path.home() / 'workspace'
        ]
        
        for base_path in search_paths:
            if base_path.exists():
                for git_dir in base_path.rglob('.git'):
                    if git_dir.is_dir():
                        repo_path = git_dir.parent
                        repos.append({
                            'path': str(repo_path),
                            'name': repo_path.name
                        })
                        
        self.results['git_repos'] = repos
        print(f"✅ Found {len(repos)} git repositories")
        
    def save_results(self):
        """Save scan results"""
        output_file = '/home/daniel/.claude/SYSTEM_SCAN_COMPLETE.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"\n💾 Complete system scan saved to: {output_file}")
        
        # Also create a summary
        summary = {
            'scan_date': datetime.now().isoformat(),
            'totals': {
                'python_packages': len(self.results['python_packages']),
                'npm_packages': len(self.results['npm_packages']),
                'system_packages': len(self.results['system_packages']),
                'docker_images': len(self.results['docker_images']),
                'docker_containers': len(self.results['docker_containers']),
                'k8s_pods': len(self.results['k8s_resources'].get('pods', [])),
                'databases': len(self.results['databases']),
                'services': len(self.results['services']),
                'dev_tools': len(self.results['development_tools']),
                'ollama_models': len(self.results['ollama_models']),
                'git_repos': len(self.results['git_repos'])
            },
            'highlights': {
                'has_docker': any('docker' in t['tool'] for t in self.results['development_tools']),
                'has_k8s': any('kubectl' in t['tool'] for t in self.results['development_tools']),
                'has_ollama': len(self.results['ollama_models']) > 0,
                'crod_services_running': sum(1 for s in self.results['services'] if 'crod' in s.lower())
            }
        }
        
        summary_file = '/home/daniel/.claude/SYSTEM_SCAN_SUMMARY.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
        return summary

if __name__ == '__main__':
    print("🚀 COMPLETE SYSTEM SCANNER")
    print("=" * 60)
    print("This will scan EVERYTHING on your system that you have access to!")
    print("Finding all packages, tools, services, and configurations...\n")
    
    scanner = CompleteSystemScanner()
    results = scanner.scan_everything()
    
    summary = scanner.save_results()
    
    print("\n" + "=" * 60)
    print("📊 SCAN COMPLETE!")
    print("=" * 60)
    
    print("\n🔥 WHAT I FOUND:")
    for key, value in summary['totals'].items():
        print(f"  {key}: {value}")
        
    print("\n💡 KEY INSIGHTS:")
    print(f"  Docker available: {summary['highlights']['has_docker']}")
    print(f"  Kubernetes available: {summary['highlights']['has_k8s']}")
    print(f"  Ollama AI models: {summary['highlights']['has_ollama']}")
    print(f"  CROD services running: {summary['highlights']['crod_services_running']}")
    
    print("\n📚 Claude's memory updated with COMPLETE system knowledge!")
    print("🧠 Now I know EVERYTHING available on your system!")