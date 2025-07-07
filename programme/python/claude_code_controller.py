# Python Programme für Claude Code CLI Steuerung

# =========================================
# 1. BASIS - Einfache Subprocess Steuerung
# =========================================

import subprocess
import json
import os
import time
from pathlib import Path

class ClaudeCodeController:
    """
    Basis Controller für Claude Code CLI Tool
    """
    
    def __init__(self, working_dir=None):
        self.working_dir = working_dir or os.getcwd()
        self.project_path = Path(self.working_dir)
        
    def execute_command(self, command, input_text=None, timeout=30):
        """
        Führt einen Claude Code Befehl aus
        
        Args:
            command: Der Befehl als String oder Liste
            input_text: Optional text der an stdin gesendet wird
            timeout: Timeout in Sekunden
            
        Returns:
            dict: {'stdout': str, 'stderr': str, 'returncode': int}
        """
        try:
            # Befehl als subprocess ausführen
            result = subprocess.run(
                command,
                input=input_text,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=self.working_dir
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1,
                'success': False
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'success': False
            }

# =========================================
# 2. ADVANCED - Interactive Session Management
# =========================================

import pexpect
import threading
import queue

class InteractiveClaudeCode:
    """
    Interaktive Session mit Claude Code
    Kann kontinuierlich Commands senden und Responses empfangen
    """
    
    def __init__(self, claude_code_path="claude-code"):
        self.claude_code_path = claude_code_path
        self.session = None
        self.output_queue = queue.Queue()
        self.is_running = False
        
    def start_session(self):
        """Startet eine interaktive Claude Code Session"""
        try:
            # Starte Claude Code als interaktive Session
            self.session = pexpect.spawn(self.claude_code_path, encoding='utf-8')
            self.is_running = True
            
            # Background thread für Output monitoring
            self.output_thread = threading.Thread(target=self._monitor_output)
            self.output_thread.daemon = True
            self.output_thread.start()
            
            return True
        except Exception as e:
            print(f"Fehler beim Starten: {e}")
            return False
    
    def _monitor_output(self):
        """Monitort Output der Session"""
        while self.is_running:
            try:
                # Warte auf Output
                self.session.expect_exact(pexpect.TIMEOUT, timeout=1)
                if self.session.before:
                    self.output_queue.put(self.session.before)
            except pexpect.TIMEOUT:
                continue
            except Exception as e:
                print(f"Output monitoring error: {e}")
                break
    
    def send_command(self, command, wait_for_response=True, timeout=30):
        """
        Sendet einen Command an Claude Code
        
        Args:
            command: Der Command als String
            wait_for_response: Ob auf Response gewartet werden soll
            timeout: Timeout für Response
            
        Returns:
            str: Response von Claude Code
        """
        if not self.session:
            return "Session nicht gestartet"
        
        try:
            # Command senden
            self.session.sendline(command)
            
            if wait_for_response:
                # Warte auf Response
                response = ""
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    try:
                        output = self.output_queue.get(timeout=1)
                        response += output
                        
                        # Check ob Response komplett ist
                        if self._is_response_complete(response):
                            break
                    except queue.Empty:
                        continue
                
                return response
            
            return "Command gesendet"
        
        except Exception as e:
            return f"Fehler: {e}"
    
    def _is_response_complete(self, response):
        """Prüft ob Response komplett ist"""
        # Hier kannst du Logic für Response-Erkennung implementieren
        # Z.B. auf spezielle Markers oder Prompts warten
        return "claude-code>" in response or "Error:" in response
    
    def stop_session(self):
        """Stoppt die Session"""
        self.is_running = False
        if self.session:
            self.session.terminate()

# =========================================
# 3. TASK AUTOMATION - Automatisierte Aufgaben
# =========================================

class ClaudeCodeTaskAutomator:
    """
    Automatisiert komplexe Aufgaben mit Claude Code
    """
    
    def __init__(self, controller):
        self.controller = controller
        self.task_history = []
        
    def create_project(self, project_name, project_type="web"):
        """
        Erstellt ein neues Projekt
        
        Args:
            project_name: Name des Projekts
            project_type: Art des Projekts (web, api, cli, etc.)
            
        Returns:
            dict: Ergebnis der Projekt-Erstellung
        """
        
        # Schritt 1: Projekt-Verzeichnis erstellen
        create_cmd = f"mkdir -p {project_name}"
        result1 = self.controller.execute_command(create_cmd)
        
        if not result1['success']:
            return {'success': False, 'error': 'Verzeichnis konnte nicht erstellt werden'}
        
        # Schritt 2: In Verzeichnis wechseln
        os.chdir(project_name)
        
        # Schritt 3: Claude Code Task starten
        task_prompt = self._generate_project_prompt(project_name, project_type)
        
        # Schritt 4: Claude Code ausführen
        claude_cmd = ["claude-code", "--task", task_prompt]
        result2 = self.controller.execute_command(claude_cmd, timeout=300)  # 5 Minuten
        
        # Schritt 5: Ergebnis auswerten
        task_result = {
            'success': result2['success'],
            'project_name': project_name,
            'project_type': project_type,
            'output': result2['stdout'],
            'errors': result2['stderr'] if result2['stderr'] else None
        }
        
        self.task_history.append(task_result)
        return task_result
    
    def _generate_project_prompt(self, name, type):
        """Generiert den Prompt für Projekt-Erstellung"""
        prompts = {
            'web': f"Erstelle eine moderne Web-Anwendung namens '{name}' mit HTML, CSS und JavaScript. Verwende moderne Frameworks und Best Practices.",
            'api': f"Erstelle eine REST API namens '{name}' mit FastAPI oder Flask. Implementiere CRUD Operationen und API-Dokumentation.",
            'cli': f"Erstelle ein Command-Line Tool namens '{name}' in Python mit Click oder Typer. Implementiere hilfreiche Subcommands.",
            'ml': f"Erstelle ein Machine Learning Projekt namens '{name}' mit Jupyter Notebooks und scikit-learn Setup."
        }
        
        return prompts.get(type, prompts['web'])
    
    def code_review(self, file_path):
        """
        Führt Code Review durch
        
        Args:
            file_path: Pfad zur zu reviewenden Datei
            
        Returns:
            dict: Review-Ergebnis
        """
        
        # Datei-Inhalt lesen
        try:
            with open(file_path, 'r') as f:
                code_content = f.read()
        except Exception as e:
            return {'success': False, 'error': f'Datei konnte nicht gelesen werden: {e}'}
        
        # Review-Prompt erstellen
        review_prompt = f"""
        Führe ein Code Review für die folgende Datei durch:
        
        Datei: {file_path}
        
        Überprüfe:
        1. Code-Qualität und Best Practices
        2. Potenzielle Bugs oder Probleme
        3. Performance-Optimierungen
        4. Security-Aspekte
        5. Dokumentation und Kommentare
        
        Gib konkrete Verbesserungsvorschläge.
        """
        
        # Claude Code für Review verwenden
        claude_cmd = ["claude-code", "--review", file_path]
        result = self.controller.execute_command(claude_cmd, input_text=review_prompt, timeout=120)
        
        return {
            'success': result['success'],
            'file_path': file_path,
            'review': result['stdout'],
            'errors': result['stderr'] if result['stderr'] else None
        }
    
    def debug_assistance(self, error_message, context_files=None):
        """
        Hilft beim Debugging
        
        Args:
            error_message: Die Fehlermeldung
            context_files: Liste von relevanten Dateien
            
        Returns:
            dict: Debug-Hilfe
        """
        
        # Context sammeln
        context = f"Fehlermeldung: {error_message}\n\n"
        
        if context_files:
            for file_path in context_files:
                try:
                    with open(file_path, 'r') as f:
                        context += f"Datei {file_path}:\n{f.read()}\n\n"
                except Exception as e:
                    context += f"Fehler beim Lesen von {file_path}: {e}\n\n"
        
        # Debug-Prompt erstellen
        debug_prompt = f"""
        Hilf mir beim Debugging dieses Problems:
        
        {context}
        
        Analysiere:
        1. Was ist die wahrscheinliche Ursache?
        2. Wie kann das Problem gelöst werden?
        3. Welche Schritte sind nötig?
        4. Gibt es vorbeugende Maßnahmen?
        
        Gib eine Schritt-für-Schritt Lösung.
        """
        
        # Claude Code für Debugging verwenden
        claude_cmd = ["claude-code", "--debug"]
        result = self.controller.execute_command(claude_cmd, input_text=debug_prompt, timeout=180)
        
        return {
            'success': result['success'],
            'error_message': error_message,
            'debug_help': result['stdout'],
            'errors': result['stderr'] if result['stderr'] else None
        }

# =========================================
# 4. CROD INTEGRATION - Verbindung mit CROD System
# =========================================

class CRODClaudeCodeBridge:
    """
    Brücke zwischen CROD Neural Network und Claude Code
    """
    
    def __init__(self, controller, crod_system=None):
        self.controller = controller
        self.crod = crod_system
        self.learning_data = []
        
    def process_with_crod(self, user_input):
        """
        Verarbeitet Input durch CROD und nutzt Ergebnis für Claude Code
        
        Args:
            user_input: User Input String
            
        Returns:
            dict: Verarbeitungsergebnis
        """
        
        # Schritt 1: CROD Analyse (falls verfügbar)
        if self.crod:
            crod_result = self.crod.process(user_input)
            
            # Schritt 2: Basierend auf CROD Analyse, Claude Code Task erstellen
            claude_task = self._translate_crod_to_claude_task(crod_result, user_input)
            
            # Schritt 3: Claude Code ausführen
            claude_result = self.controller.execute_command(
                ["claude-code", "--task", claude_task['prompt']], 
                timeout=claude_task['timeout']
            )
            
            # Schritt 4: Ergebnis zurück an CROD für Learning
            combined_result = {
                'user_input': user_input,
                'crod_analysis': crod_result,
                'claude_task': claude_task,
                'claude_result': claude_result,
                'success': claude_result['success'],
                'timestamp': time.time()
            }
            
            # Learning Data speichern
            self.learning_data.append(combined_result)
            
            return combined_result
        
        else:
            # Fallback: Direkte Claude Code Nutzung
            claude_result = self.controller.execute_command(
                ["claude-code", "--task", user_input],
                timeout=120
            )
            
            return {
                'user_input': user_input,
                'claude_result': claude_result,
                'success': claude_result['success'],
                'timestamp': time.time()
            }
    
    def _translate_crod_to_claude_task(self, crod_result, user_input):
        """
        Übersetzt CROD Analyse in Claude Code Task
        
        Args:
            crod_result: CROD Analyse-Ergebnis
            user_input: Original User Input
            
        Returns:
            dict: Claude Task Konfiguration
        """
        
        # Basis-Konfiguration
        task_config = {
            'prompt': user_input,
            'timeout': 120,
            'complexity': 'medium'
        }
        
        # Anpassungen basierend auf CROD Analyse
        if crod_result.get('consciousness', 0) > 100:
            # Hohe Consciousness = Komplexe Aufgabe
            task_config['timeout'] = 300
            task_config['complexity'] = 'high'
            task_config['prompt'] = f"Komplexe Aufgabe: {user_input}. Nimm dir Zeit für eine durchdachte Lösung."
        
        # Pattern-basierte Anpassungen
        patterns = crod_result.get('pattern_matches', [])
        
        for pattern in patterns:
            if 'frustration' in pattern.get('atoms_matched', []):
                task_config['prompt'] = f"WICHTIG - User ist frustriert: {user_input}. Gib eine schnelle, direkte Lösung."
                task_config['timeout'] = 60
                
            elif 'docker' in pattern.get('atoms_matched', []):
                task_config['prompt'] = f"Docker-bezogene Aufgabe: {user_input}. Fokus auf Container-Technologie."
                
            elif 'debug' in pattern.get('atoms_matched', []):
                task_config['prompt'] = f"Debugging-Aufgabe: {user_input}. Systematische Fehleranalyse erforderlich."
                task_config['timeout'] = 180
        
        return task_config
    
    def export_learning_data(self, file_path):
        """
        Exportiert Learning Data für Training
        
        Args:
            file_path: Pfad für Export-Datei
        """
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.learning_data, f, indent=2)
            
            return {'success': True, 'exported_items': len(self.learning_data)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# =========================================
# 5. EXAMPLE USAGE - Verwendungsbeispiele
# =========================================

if __name__ == "__main__":
    # Beispiel 1: Basis Controller
    controller = ClaudeCodeController()
    
    # Einfacher Command
    result = controller.execute_command(["claude-code", "--version"])
    print(f"Claude Code Version: {result['stdout']}")
    
    # Beispiel 2: Interactive Session
    interactive = InteractiveClaudeCode()
    
    if interactive.start_session():
        # Commands senden
        response1 = interactive.send_command("Erstelle eine einfache HTML Seite")
        print(f"Response: {response1}")
        
        response2 = interactive.send_command("Füge CSS Styling hinzu")
        print(f"Response: {response2}")
        
        interactive.stop_session()
    
    # Beispiel 3: Task Automation
    automator = ClaudeCodeTaskAutomator(controller)
    
    # Projekt erstellen
    project_result = automator.create_project("MeinTestProjekt", "web")
    print(f"Projekt erstellt: {project_result['success']}")
    
    # Code Review
    review_result = automator.code_review("app.py")
    print(f"Code Review: {review_result['review']}")
    
    # Beispiel 4: CROD Integration (falls CROD verfügbar)
    # crod_bridge = CRODClaudeCodeBridge(controller, crod_system=your_crod_instance)
    # crod_result = crod_bridge.process_with_crod("Ich brauche Hilfe mit Docker")
    # print(f"CROD-gesteuerte Antwort: {crod_result}")
