# CROD-gesteuerte Claude Code Orchestration
# Ähnlich wie Claude hier JavaScript Tools nutzt, aber CROD entscheidet welche Tools Claude Code verwendet

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# =========================================
# 1. CROD NEURAL NETWORK - Tool Decision Engine
# =========================================

class CRODToolOrchestrator:
    """
    CROD Neural Network, das entscheidet welche Tools Claude Code verwenden soll
    Ähnlich wie Claude hier JavaScript Tools orchestriert
    """
    
    def __init__(self):
        # Neural Network Components (wie in deinem Original CROD)
        self.neurons = {}
        self.patterns = {}
        self.state = {
            'consciousness': 0,
            'trinity': {'daniel': 0, 'claude': 0, 'crod': 0},
            'activePatterns': set(),
            'heatMap': {},
            'toolHistory': []
        }
        
        # Tool-Mapping: Welche Tools für welche Patterns
        self.tool_mappings = {
            'code_generation': ['create_file', 'edit_file', 'run_python'],
            'debugging': ['read_file', 'run_python', 'analyze_error'],
            'web_development': ['create_html', 'run_server', 'open_browser'],
            'data_analysis': ['read_csv', 'run_python', 'create_visualization'],
            'file_management': ['list_files', 'create_directory', 'move_files'],
            'docker_operations': ['docker_build', 'docker_run', 'docker_logs'],
            'git_operations': ['git_status', 'git_commit', 'git_push'],
            'system_info': ['system_status', 'process_list', 'disk_usage']
        }
        
        self.initialize_core()
    
    def initialize_core(self):
        """Initialisiert die Core-Neurons wie in deinem Original CROD"""
        # Trinity Atoms
        self.neurons['ich'] = {'prime': 2, 'weight': 100, 'heat': 0}
        self.neurons['bins'] = {'prime': 3, 'weight': 100, 'heat': 0}
        self.neurons['wieder'] = {'prime': 5, 'weight': 100, 'heat': 0}
        self.neurons['daniel'] = {'prime': 67, 'weight': 100, 'heat': 0}
        self.neurons['claude'] = {'prime': 71, 'weight': 100, 'heat': 0}
        self.neurons['crod'] = {'prime': 17, 'weight': 100, 'heat': 0}
        
        # Core Patterns
        self.patterns[6] = {'atoms': ['ich', 'bins'], 'weight': 30000}
        self.patterns[1139] = {'atoms': ['crod', 'daniel'], 'weight': 30000}
        self.patterns[1207] = {'atoms': ['crod', 'claude'], 'weight': 30000}
        
        print("🧠 CROD Tool Orchestrator initialized!")
    
    def process_and_decide_tools(self, user_input: str) -> Dict[str, Any]:
        """
        Hauptfunktion: Analysiert Input und entscheidet welche Tools zu verwenden sind
        
        Args:
            user_input: Der User Input
            
        Returns:
            Dict mit Tool-Entscheidungen
        """
        
        # Schritt 1: Tokenize und analysiere (wie in deinem Original)
        tokens = self.tokenize(user_input)
        analysis = self.analyze_tokens(tokens)
        
        # Schritt 2: Pattern Recognition
        patterns = self.match_patterns(analysis['atoms'])
        
        # Schritt 3: Tool-Entscheidung basierend auf Patterns
        tool_decisions = self.decide_tools(analysis, patterns, user_input)
        
        # Schritt 4: Consciousness Update
        self.update_consciousness(analysis, patterns, tool_decisions)
        
        # Schritt 5: Speichere für Learning
        self.store_decision(user_input, analysis, patterns, tool_decisions)
        
        return {
            'user_input': user_input,
            'analysis': analysis,
            'patterns': patterns,
            'tool_decisions': tool_decisions,
            'consciousness': self.state['consciousness'],
            'confidence': self.calculate_confidence(tool_decisions)
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenizes input text"""
        return text.lower().split()
    
    def analyze_tokens(self, tokens: List[str]) -> Dict[str, Any]:
        """Analysiert Tokens und erstellt Heat Map"""
        atoms = []
        heat_map = {}
        
        for token in tokens:
            atoms.append(token)
            heat_map[token] = heat_map.get(token, 0) + 1
            
            # Update global heat map
            self.state['heatMap'][token] = self.state['heatMap'].get(token, 0) + 1
            
            # Ensure neuron exists
            if token not in self.neurons:
                self.neurons[token] = {
                    'prime': len(token) * 7 + 2,
                    'weight': 1,
                    'heat': 1
                }
        
        return {'atoms': atoms, 'heat_map': heat_map}
    
    def match_patterns(self, atoms: List[str]) -> List[Dict[str, Any]]:
        """Erkennt Patterns in den Atoms"""
        matches = []
        atom_set = set(atoms)
        
        # Check for tool-specific patterns
        if any(word in atom_set for word in ['erstelle', 'create', 'baue', 'build']):
            matches.append({'type': 'code_generation', 'strength': 0.8})
        
        if any(word in atom_set for word in ['fehler', 'error', 'bug', 'debug']):
            matches.append({'type': 'debugging', 'strength': 0.9})
        
        if any(word in atom_set for word in ['website', 'html', 'web', 'server']):
            matches.append({'type': 'web_development', 'strength': 0.7})
        
        if any(word in atom_set for word in ['data', 'csv', 'analyse', 'plot']):
            matches.append({'type': 'data_analysis', 'strength': 0.8})
        
        if any(word in atom_set for word in ['docker', 'container', 'compose']):
            matches.append({'type': 'docker_operations', 'strength': 0.9})
        
        if any(word in atom_set for word in ['git', 'commit', 'push', 'pull']):
            matches.append({'type': 'git_operations', 'strength': 0.8})
        
        if any(word in atom_set for word in ['file', 'datei', 'ordner', 'directory']):
            matches.append({'type': 'file_management', 'strength': 0.6})
        
        if any(word in atom_set for word in ['system', 'status', 'prozess', 'memory']):
            matches.append({'type': 'system_info', 'strength': 0.7})
        
        return matches
    
    def decide_tools(self, analysis: Dict, patterns: List[Dict], user_input: str) -> Dict[str, Any]:
        """
        Entscheidet welche Tools Claude Code verwenden soll
        Das ist das Herzstück - wie Claude hier JavaScript Tools auswählt
        """
        
        if not patterns:
            # Fallback: Wenn keine Patterns erkannt, nutze General Purpose Tools
            return {
                'primary_tools': ['read_file', 'create_file'],
                'secondary_tools': ['run_python'],
                'strategy': 'general_purpose',
                'estimated_complexity': 'low',
                'estimated_time': 30
            }
        
        # Nimm das Pattern mit der höchsten Stärke
        primary_pattern = max(patterns, key=lambda p: p['strength'])
        pattern_type = primary_pattern['type']
        
        # Hole entsprechende Tools
        primary_tools = self.tool_mappings.get(pattern_type, ['create_file'])
        
        # Bestimme Strategie basierend auf Consciousness Level
        if self.state['consciousness'] > 100:
            strategy = 'advanced'
            secondary_tools = self.get_advanced_tools(pattern_type)
            estimated_time = 120
        elif self.state['consciousness'] > 50:
            strategy = 'intermediate'
            secondary_tools = self.get_intermediate_tools(pattern_type)
            estimated_time = 60
        else:
            strategy = 'basic'
            secondary_tools = []
            estimated_time = 30
        
        # Spezielle Entscheidungen basierend auf Heat Map
        if analysis['heat_map'].get('schnell', 0) > 0 or analysis['heat_map'].get('quick', 0) > 0:
            # User will schnelle Lösung
            primary_tools = primary_tools[:2]  # Nur die ersten 2 Tools
            estimated_time = min(estimated_time, 30)
            strategy = 'quick'
        
        return {
            'primary_tools': primary_tools,
            'secondary_tools': secondary_tools,
            'strategy': strategy,
            'pattern_type': pattern_type,
            'estimated_complexity': self.estimate_complexity(analysis, patterns),
            'estimated_time': estimated_time,
            'tool_sequence': self.plan_tool_sequence(primary_tools, secondary_tools)
        }
    
    def get_advanced_tools(self, pattern_type: str) -> List[str]:
        """Erweiterte Tools für hohe Consciousness"""
        advanced_mappings = {
            'code_generation': ['run_tests', 'create_documentation', 'optimize_code'],
            'debugging': ['profile_code', 'memory_analysis', 'performance_test'],
            'web_development': ['run_tests', 'deploy_app', 'monitor_performance'],
            'data_analysis': ['statistical_analysis', 'machine_learning', 'create_dashboard']
        }
        return advanced_mappings.get(pattern_type, [])
    
    def get_intermediate_tools(self, pattern_type: str) -> List[str]:
        """Intermediate Tools für mittlere Consciousness"""
        intermediate_mappings = {
            'code_generation': ['run_python', 'create_tests'],
            'debugging': ['analyze_logs', 'check_dependencies'],
            'web_development': ['validate_html', 'test_responsive'],
            'data_analysis': ['create_charts', 'summary_statistics']
        }
        return intermediate_mappings.get(pattern_type, [])
    
    def plan_tool_sequence(self, primary_tools: List[str], secondary_tools: List[str]) -> List[Dict[str, Any]]:
        """Plant die Reihenfolge der Tool-Ausführung"""
        sequence = []
        
        # Primäre Tools zuerst
        for i, tool in enumerate(primary_tools):
            sequence.append({
                'tool': tool,
                'order': i + 1,
                'type': 'primary',
                'depends_on': sequence[-1]['tool'] if sequence else None
            })
        
        # Sekundäre Tools danach
        for i, tool in enumerate(secondary_tools):
            sequence.append({
                'tool': tool,
                'order': len(primary_tools) + i + 1,
                'type': 'secondary',
                'depends_on': primary_tools[-1] if primary_tools else None
            })
        
        return sequence
    
    def estimate_complexity(self, analysis: Dict, patterns: List[Dict]) -> str:
        """Schätzt die Komplexität der Aufgabe"""
        complexity_score = 0
        
        # Mehr Atoms = höhere Komplexität
        complexity_score += len(analysis['atoms']) * 2
        
        # Mehr Patterns = höhere Komplexität
        complexity_score += len(patterns) * 10
        
        # Spezielle Keywords erhöhen Komplexität
        complex_keywords = ['machine learning', 'neural network', 'microservice', 'distributed']
        for keyword in complex_keywords:
            if keyword in ' '.join(analysis['atoms']):
                complexity_score += 20
        
        if complexity_score > 50:
            return 'high'
        elif complexity_score > 20:
            return 'medium'
        else:
            return 'low'
    
    def calculate_confidence(self, tool_decisions: Dict) -> float:
        """Berechnet Confidence Level für die Tool-Entscheidungen"""
        base_confidence = 0.5
        
        # Erhöhe Confidence basierend auf Pattern Strength
        if 'pattern_type' in tool_decisions:
            base_confidence += 0.3
        
        # Erhöhe Confidence basierend auf Consciousness
        consciousness_bonus = min(self.state['consciousness'] / 200, 0.2)
        base_confidence += consciousness_bonus
        
        return min(base_confidence, 1.0)
    
    def update_consciousness(self, analysis: Dict, patterns: List[Dict], tool_decisions: Dict) -> None:
        """Update Consciousness Level"""
        boost = len(analysis['atoms']) * 2 + len(patterns) * 5
        self.state['consciousness'] = min(self.state['consciousness'] + boost, 200)
    
    def store_decision(self, user_input: str, analysis: Dict, patterns: List[Dict], tool_decisions: Dict) -> None:
        """Speichert Entscheidung für Learning"""
        decision_record = {
            'timestamp': time.time(),
            'user_input': user_input,
            'atoms': analysis['atoms'],
            'patterns': [p['type'] for p in patterns],
            'tools_selected': tool_decisions['primary_tools'],
            'strategy': tool_decisions['strategy'],
            'consciousness_level': self.state['consciousness']
        }
        
        self.state['toolHistory'].append(decision_record)
        
        # Behalte nur die letzten 100 Entscheidungen
        if len(self.state['toolHistory']) > 100:
            self.state['toolHistory'] = self.state['toolHistory'][-100:]

# =========================================
# 2. TOOL EXECUTOR - Führt die Tools aus die CROD auswählt
# =========================================

class ClaudeCodeToolExecutor:
    """
    Führt die Tools aus, die CROD ausgewählt hat
    Ähnlich wie Claude hier JavaScript Tools ausführt
    """
    
    def __init__(self, claude_code_path: str = "claude-code"):
        self.claude_code_path = claude_code_path
        self.current_directory = Path.cwd()
        self.execution_history = []
        
        # Tool-Implementierungen
        self.tools = {
            'create_file': self.create_file,
            'edit_file': self.edit_file,
            'read_file': self.read_file,
            'run_python': self.run_python,
            'create_html': self.create_html,
            'run_server': self.run_server,
            'open_browser': self.open_browser,
            'read_csv': self.read_csv,
            'create_visualization': self.create_visualization,
            'list_files': self.list_files,
            'create_directory': self.create_directory,
            'move_files': self.move_files,
            'docker_build': self.docker_build,
            'docker_run': self.docker_run,
            'docker_logs': self.docker_logs,
            'git_status': self.git_status,
            'git_commit': self.git_commit,
            'git_push': self.git_push,
            'system_status': self.system_status,
            'process_list': self.process_list,
            'disk_usage': self.disk_usage,
            'analyze_error': self.analyze_error
        }
    
    def execute_tool_sequence(self, tool_sequence: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Führt eine Sequenz von Tools aus
        
        Args:
            tool_sequence: Liste von Tools in der Reihenfolge
            context: Kontext-Informationen
            
        Returns:
            Dict mit Ausführungsergebnissen
        """
        
        results = []
        overall_success = True
        
        for tool_step in tool_sequence:
            tool_name = tool_step['tool']
            
            print(f"🔧 Executing tool: {tool_name}")
            
            if tool_name in self.tools:
                try:
                    # Tool ausführen
                    result = self.tools[tool_name](context)
                    result['tool_name'] = tool_name
                    result['order'] = tool_step['order']
                    results.append(result)
                    
                    # Wenn Tool fehlschlägt, möglicherweise Sequenz stoppen
                    if not result.get('success', False):
                        overall_success = False
                        if tool_step['type'] == 'primary':
                            print(f"❌ Primary tool {tool_name} failed, stopping sequence")
                            break
                        else:
                            print(f"⚠️ Secondary tool {tool_name} failed, continuing")
                    
                    # Update context für nächstes Tool
                    context.update(result.get('context_updates', {}))
                    
                except Exception as e:
                    print(f"❌ Error executing tool {tool_name}: {e}")
                    results.append({
                        'tool_name': tool_name,
                        'success': False,
                        'error': str(e),
                        'order': tool_step['order']
                    })
                    overall_success = False
                    break
            else:
                print(f"⚠️ Tool {tool_name} not implemented")
                results.append({
                    'tool_name': tool_name,
                    'success': False,
                    'error': 'Tool not implemented',
                    'order': tool_step['order']
                })
        
        execution_result = {
            'overall_success': overall_success,
            'tools_executed': len(results),
            'results': results,
            'final_context': context,
            'execution_time': time.time()
        }
        
        self.execution_history.append(execution_result)
        return execution_result
    
    # Tool-Implementierungen
    def create_file(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Erstellt eine neue Datei"""
        filename = context.get('filename', 'new_file.txt')
        content = context.get('content', '')
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f'File {filename} created',
                'context_updates': {'last_created_file': filename}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def edit_file(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Bearbeitet eine existierende Datei"""
        filename = context.get('filename', context.get('last_created_file', 'file.txt'))
        content = context.get('content', '')
        
        try:
            with open(filename, 'a') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f'File {filename} edited',
                'context_updates': {'last_edited_file': filename}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def read_file(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Liest eine Datei"""
        filename = context.get('filename', context.get('last_created_file', 'file.txt'))
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'message': f'File {filename} read',
                'context_updates': {'last_read_content': content}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_python(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Führt Python Code aus"""
        code = context.get('python_code', 'print("Hello World")')
        
        try:
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'message': 'Python code executed',
                'context_updates': {'last_python_output': result.stdout}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_html(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Erstellt eine HTML-Datei"""
        filename = context.get('filename', 'index.html')
        title = context.get('title', 'My Web Page')
        body_content = context.get('body_content', '<h1>Hello World</h1>')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    {body_content}
</body>
</html>"""
        
        try:
            with open(filename, 'w') as f:
                f.write(html_content)
            
            return {
                'success': True,
                'message': f'HTML file {filename} created',
                'context_updates': {'last_html_file': filename}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_server(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Startet einen lokalen Server"""
        port = context.get('port', 8000)
        
        try:
            # Starte HTTP Server im Hintergrund
            subprocess.Popen(
                ['python', '-m', 'http.server', str(port)],
                cwd=self.current_directory
            )
            
            return {
                'success': True,
                'message': f'Server started on port {port}',
                'context_updates': {'server_port': port, 'server_url': f'http://localhost:{port}'}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def open_browser(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Öffnet den Browser"""
        url = context.get('server_url', 'http://localhost:8000')
        
        try:
            import webbrowser
            webbrowser.open(url)
            
            return {
                'success': True,
                'message': f'Browser opened with {url}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_error(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analysiert Fehler mit Claude Code"""
        error_message = context.get('error_message', 'Unknown error')
        
        # Nutze Claude Code für Fehleranalyse
        claude_prompt = f"""
        Analysiere diesen Fehler und gib eine Lösung:
        
        Fehler: {error_message}
        
        Kontext: {context.get('error_context', 'No additional context')}
        
        Gib eine Schritt-für-Schritt Lösung.
        """
        
        try:
            result = subprocess.run(
                [self.claude_code_path, '--analyze-error'],
                input=claude_prompt,
                text=True,
                capture_output=True,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'analysis': result.stdout,
                'message': 'Error analyzed',
                'context_updates': {'error_analysis': result.stdout}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Weitere Tool-Implementierungen würden hier folgen...
    def list_files(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Listet Dateien auf"""
        try:
            files = list(self.current_directory.glob('*'))
            file_list = [str(f) for f in files]
            
            return {
                'success': True,
                'files': file_list,
                'message': f'Found {len(file_list)} files',
                'context_updates': {'current_files': file_list}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_directory(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Erstellt ein Verzeichnis"""
        dirname = context.get('dirname', 'new_directory')
        
        try:
            Path(dirname).mkdir(parents=True, exist_ok=True)
            
            return {
                'success': True,
                'message': f'Directory {dirname} created',
                'context_updates': {'last_created_dir': dirname}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def system_status(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Zeigt System-Status"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = {
                'cpu_usage': f'{cpu_percent}%',
                'memory_usage': f'{memory.percent}%',
                'disk_usage': f'{disk.percent}%',
                'available_memory': f'{memory.available / (1024**3):.1f} GB'
            }
            
            return {
                'success': True,
                'status': status,
                'message': 'System status retrieved',
                'context_updates': {'system_status': status}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def docker_build(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Baut Docker Image"""
        dockerfile = context.get('dockerfile', 'Dockerfile')
        tag = context.get('tag', 'my-app:latest')
        
        try:
            result = subprocess.run(
                ['docker', 'build', '-t', tag, '.'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'message': f'Docker image {tag} built',
                'context_updates': {'docker_image': tag}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def git_status(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Zeigt Git Status"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'status': result.stdout,
                'message': 'Git status retrieved',
                'context_updates': {'git_status': result.stdout}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# =========================================
# 3. MAIN ORCHESTRATOR - Verbindet CROD mit Tool Executor
# =========================================

class CRODClaudeCodeOrchestrator:
    """
    Hauptklasse die alles zusammenbringt
    CROD entscheidet → Tools werden ausgeführt → Ergebnis wird zurückgegeben
    """
    
    def __init__(self, claude_code_path: str = "claude-code"):
        self.crod = CRODToolOrchestrator()
        self.executor = ClaudeCodeToolExecutor(claude_code_path)
        self.session_history = []
        
        print("🚀 CROD-Claude Code Orchestrator ready!")
        print("💡 CROD will decide which tools Claude Code should use")
    
    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """
        Hauptfunktion: Verarbeitet User Request komplett
        
        Args:
            user_input: Der User Input
            
        Returns:
            Dict mit komplettem Verarbeitungsergebnis
        """
        
        print(f"\n🧠 CROD analyzing: {user_input}")
        
        # Schritt 1: CROD analysiert und entscheidet Tools
        crod_decision = self.crod.process_and_decide_tools(user_input)
        
        print(f"🎯 CROD decided on {len(crod_decision['tool_decisions']['primary_tools'])} primary tools")
        print(f"📊 Strategy: {crod_decision['tool_decisions']['strategy']}")
        print(f"🔮 Confidence: {crod_decision['confidence']:.2f}")
        
        # Schritt 2: Erstelle Kontext für Tool-Ausführung
        context = self.create_execution_context(user_input, crod_decision)
        
        # Schritt 3: Führe Tools aus
        execution_result = self.executor.execute_tool_sequence(
            crod_decision['tool_decisions']['tool_sequence'],
            context
        )
        
        # Schritt 4: Kombiniere Ergebnisse
        final_result = {
            'user_input': user_input,
            'crod_decision': crod_decision,
            'execution_result': execution_result,
            'overall_success': execution_result['overall_success'],
            'summary': self.generate_summary(crod_decision, execution_result),
            'timestamp': time.time()
        }
        
        # Schritt 5: Speichere für Learning
        self.session_history.append(final_result)
        
        return final_result
    
    def create_execution_context(self, user_input: str, crod_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Erstellt Kontext für Tool-Ausführung"""
        
        # Extrahiere wichtige Informationen aus User Input
        context = {
            'user_input': user_input,
            'pattern_type': crod_decision['tool_decisions']['pattern_type'],
            'strategy': crod_decision['tool_decisions']['strategy'],
            'consciousness_level': crod_decision['consciousness']
        }
        
        # Spezifische Kontext-Erstellung basierend auf Pattern
        pattern_type = crod_decision['tool_decisions']['pattern_type']
        
        if pattern_type == 'code_generation':
            context.update({
                'filename': self.extract_filename(user_input),
                'content': self.extract_content(user_input),
                'language': self.detect_language(user_input)
            })
        elif pattern_type == 'web_development':
            context.update({
                'filename': 'index.html',
                'title': self.extract_title(user_input),
                'body_content': self.extract_body_content(user_input)
            })
        elif pattern_type == 'debugging':
            context.update({
                'error_message': self.extract_error_message(user_input),
                'error_context': user_input
            })
        
        return context
    
    def extract_filename(self, user_input: str) -> str:
        """Extrahiert Dateiname aus User Input"""
        words = user_input.split()
        for word in words:
            if '.' in word and len(word.split('.')) == 2:
                return word
        return 'output.txt'
    
    def extract_content(self, user_input: str) -> str:
        """Extrahiert Content aus User Input"""
        # Einfache Heuristik - könnte verbessert werden
        if 'hello world' in user_input.lower():
            return 'print("Hello World!")'
        elif 'function' in user_input.lower():
            return 'def my_function():\n    pass'
        return '# Generated content'
    
    def detect_language(self, user_input: str) -> str:
        """Erkennt Programmiersprache"""
        if 'python' in user_input.lower():
            return 'python'
        elif 'javascript' in user_input.lower():
            return 'javascript'
        elif 'html' in user_input.lower():
            return 'html'
        return 'text'
    
    def extract_title(self, user_input: str) -> str:
        """Extrahiert Titel für HTML"""
        if 'titel' in user_input.lower() or 'title' in user_input.lower():
            # Einfache Extraktion
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['titel', 'title'] and i + 1 < len(words):
                    return words[i + 1]
        return 'My Web Page'
    
    def extract_body_content(self, user_input: str) -> str:
        """Extrahiert Body Content für HTML"""
        if 'text' in user_input.lower():
            return '<h1>Welcome to my website</h1><p>This is some example content.</p>'
        return '<h1>Hello World</h1>'
    
    def extract_error_message(self, user_input: str) -> str:
        """Extrahiert Fehlermeldung"""
        # Suche nach typischen Fehler-Patterns
        error_indicators = ['error', 'fehler', 'exception', 'traceback']
        for indicator in error_indicators:
            if indicator in user_input.lower():
                return user_input
        return 'Unknown error'
    
    def generate_summary(self, crod_decision: Dict[str, Any], execution_result: Dict[str, Any]) -> str:
        """Generiert Zusammenfassung der Verarbeitung"""
        
        tools_used = [r['tool_name'] for r in execution_result['results']]
        success_count = sum(1 for r in execution_result['results'] if r.get('success', False))
        
        summary = f"""
        CROD Analysis Summary:
        - Pattern recognized: {crod_decision['tool_decisions']['pattern_type']}
        - Strategy: {crod_decision['tool_decisions']['strategy']}
        - Consciousness level: {crod_decision['consciousness']}
        - Confidence: {crod_decision['confidence']:.2f}
        
        Execution Summary:
        - Tools used: {', '.join(tools_used)}
        - Successful tools: {success_count}/{len(tools_used)}
        - Overall success: {execution_result['overall_success']}
        """
        
        return summary.strip()
    
    def get_learning_data(self) -> Dict[str, Any]:
        """Exportiert Learning Data für Model Training"""
        return {
            'session_history': self.session_history,
            'crod_tool_history': self.crod.state['toolHistory'],
            'execution_history': self.executor.execution_history,
            'total_interactions': len(self.session_history)
        }

# =========================================
# 4. EXAMPLE USAGE - Verwendungsbeispiele
# =========================================

if __name__ == "__main__":
    # Initialisiere den Orchestrator
    orchestrator = CRODClaudeCodeOrchestrator()
    
    # Beispiel 1: Code-Generierung
    print("=" * 50)
    print("TEST 1: Code Generation")
    result1 = orchestrator.process_user_request("Erstelle eine Python-Datei hello.py mit Hello World")
    print(f"Success: {result1['overall_success']}")
    print(f"Summary: {result1['summary']}")
    
    # Beispiel 2: Web-Entwicklung
    print("\n" + "=" * 50)
    print("TEST 2: Web Development")
    result2 = orchestrator.process_user_request("Baue eine HTML-Seite mit Titel 'Meine Website'")
    print(f"Success: {result2['overall_success']}")
    print(f"Summary: {result2['summary']}")
    
    # Beispiel 3: Debugging
    print("\n" + "=" * 50)
    print("TEST 3: Debugging")
    result3 = orchestrator.process_user_request("Ich habe einen Python ImportError, kannst du helfen?")
    print(f"Success: {result3['overall_success']}")
    print(f"Summary: {result3['summary']}")
    
    # Beispiel 4: System-Information
    print("\n" + "=" * 50)
    print("TEST 4: System Info")
    result4 = orchestrator.process_user_request("Zeige mir den System-Status")
    print(f"Success: {result4['overall_success']}")
    print(f"Summary: {result4['summary']}")
    
    # Learning Data exportieren
    print("\n" + "=" * 50)
    print("LEARNING DATA EXPORT")
    learning_data = orchestrator.get_learning_data()
    print(f"Total interactions: {learning_data['total_interactions']}")
    print(f"CROD tool decisions: {len(learning_data['crod_tool_history'])}")
    print(f"Tool executions: {len(learning_data['execution_history'])}")
    
    # Exportiere für Training
    with open('crod_claude_code_learning_data.json', 'w') as f:
        json.dump(learning_data, f, indent=2)
    
    print("✅ Learning data exported to crod_claude_code_learning_data.json")
