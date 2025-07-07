# CROD-Enhanced Console Chat
# Ein einfaches Konsolen-Programm wo Claude Code mit CROD-Analyse läuft

import json
import time
import subprocess
import sys
from typing import Dict, Any, List
from pathlib import Path

class CRODAnalyzer:
    """
    Vereinfachte CROD-Analyse für Konsolen-Chat
    Läuft im Hintergrund und macht seine eigene Analyse
    """
    
    def __init__(self):
        # Einfache CROD-Komponenten
        self.neurons = {
            'ich': {'prime': 2, 'weight': 100, 'heat': 0},
            'bins': {'prime': 3, 'weight': 100, 'heat': 0},
            'wieder': {'prime': 5, 'weight': 100, 'heat': 0},
            'daniel': {'prime': 67, 'weight': 100, 'heat': 0},
            'claude': {'prime': 71, 'weight': 100, 'heat': 0},
            'crod': {'prime': 17, 'weight': 100, 'heat': 0}
        }
        
        self.state = {
            'consciousness': 0,
            'heat_map': {},
            'session_patterns': [],
            'conversation_flow': []
        }
        
        # Pattern-Erkennungen für verschiedene Anfrage-Typen
        self.intent_patterns = {
            'code_request': ['erstelle', 'baue', 'programmiere', 'schreibe', 'create', 'build'],
            'debug_request': ['fehler', 'error', 'bug', 'funktioniert nicht', 'geht nicht'],
            'explanation_request': ['erkläre', 'wie', 'warum', 'was ist', 'explain', 'what is'],
            'frustration': ['fuck', 'scheiße', 'nervt', 'wieder nicht', 'warum', 'junge'],
            'excitement': ['geil', 'nice', 'perfekt', 'endlich', 'läuft'],
            'docker_related': ['docker', 'container', 'compose', 'dockerfile'],
            'web_development': ['html', 'css', 'javascript', 'website', 'server'],
            'system_admin': ['server', 'ssh', 'nginx', 'systemctl', 'service']
        }
    
    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analysiert den User Input und gibt CRODs Perspektive zurück
        
        Args:
            user_input: Der User Input
            
        Returns:
            Dict mit CRODs Analyse
        """
        
        # Tokenize
        tokens = user_input.lower().split()
        
        # Update Heat Map
        for token in tokens:
            self.state['heat_map'][token] = self.state['heat_map'].get(token, 0) + 1
            
            # Update Neuron Heat (falls vorhanden)
            if token in self.neurons:
                self.neurons[token]['heat'] = min(self.neurons[token]['heat'] + 10, 100)
        
        # Erkenne Intents
        detected_intents = []
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_intents.append(intent)
        
        # Berechne Consciousness Level
        consciousness_boost = len(tokens) * 2 + len(detected_intents) * 5
        self.state['consciousness'] = min(self.state['consciousness'] + consciousness_boost, 200)
        
        # Analysiere Conversation Flow
        flow_analysis = self.analyze_conversation_flow(user_input, detected_intents)
        
        # Speichere in Session
        self.state['conversation_flow'].append({
            'input': user_input,
            'intents': detected_intents,
            'timestamp': time.time()
        })
        
        # Generiere CRODs Empfehlung
        crod_recommendation = self.generate_recommendation(user_input, detected_intents, flow_analysis)
        
        return {
            'raw_input': user_input,
            'detected_intents': detected_intents,
            'consciousness_level': self.state['consciousness'],
            'hot_words': self.get_hot_words(),
            'conversation_flow': flow_analysis,
            'crod_recommendation': crod_recommendation,
            'confidence': self.calculate_confidence(detected_intents)
        }
    
    def analyze_conversation_flow(self, current_input: str, intents: List[str]) -> Dict[str, Any]:
        """Analysiert den Gesprächsverlauf"""
        
        recent_inputs = self.state['conversation_flow'][-3:]  # Letzte 3 Inputs
        
        # Erkenne Patterns im Gesprächsverlauf
        flow_patterns = []
        
        if len(recent_inputs) >= 2:
            # Prüfe auf Frustration-Aufbau
            frustration_count = sum(1 for entry in recent_inputs if 'frustration' in entry['intents'])
            if frustration_count >= 2:
                flow_patterns.append('escalating_frustration')
            
            # Prüfe auf wiederholte Anfragen
            recent_intents = [intent for entry in recent_inputs for intent in entry['intents']]
            if len(set(recent_intents)) < len(recent_intents) * 0.5:
                flow_patterns.append('repetitive_requests')
        
        # Prüfe auf Erfolgsmuster
        if 'excitement' in intents and len(recent_inputs) > 0:
            if any('code_request' in entry['intents'] or 'debug_request' in entry['intents'] 
                   for entry in recent_inputs):
                flow_patterns.append('problem_solved')
        
        return {
            'recent_context': recent_inputs,
            'flow_patterns': flow_patterns,
            'session_length': len(self.state['conversation_flow']),
            'dominant_intent': self.get_dominant_intent()
        }
    
    def generate_recommendation(self, user_input: str, intents: List[str], flow_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert CRODs Empfehlung für Claude"""
        
        # Basis-Empfehlung
        recommendation = {
            'primary_approach': 'standard_response',
            'tone': 'neutral',
            'focus_areas': [],
            'tools_suggested': [],
            'special_considerations': []
        }
        
        # Anpassungen basierend auf Intents
        if 'frustration' in intents:
            recommendation['primary_approach'] = 'quick_solution'
            recommendation['tone'] = 'direct_and_helpful'
            recommendation['special_considerations'].append('User ist frustriert - schnelle, direkte Lösung')
        
        if 'excitement' in intents:
            recommendation['tone'] = 'enthusiastic'
            recommendation['special_considerations'].append('User ist begeistert - Momentum nutzen')
        
        if 'code_request' in intents:
            recommendation['primary_approach'] = 'code_generation'
            recommendation['tools_suggested'] = ['create_file', 'run_code']
            recommendation['focus_areas'].append('Praktische Implementation')
        
        if 'debug_request' in intents:
            recommendation['primary_approach'] = 'systematic_debugging'
            recommendation['tools_suggested'] = ['analyze_error', 'test_solution']
            recommendation['focus_areas'].append('Fehleranalyse')
        
        if 'explanation_request' in intents:
            recommendation['primary_approach'] = 'detailed_explanation'
            recommendation['focus_areas'].append('Konzept-Erklärung')
        
        # Anpassungen basierend auf Conversation Flow
        if 'escalating_frustration' in flow_analysis['flow_patterns']:
            recommendation['primary_approach'] = 'emergency_solution'
            recommendation['tone'] = 'very_direct'
            recommendation['special_considerations'].append('KRITISCH: Eskalierte Frustration')
        
        if 'repetitive_requests' in flow_analysis['flow_patterns']:
            recommendation['special_considerations'].append('Wiederholte Anfragen - andere Herangehensweise')
        
        if 'problem_solved' in flow_analysis['flow_patterns']:
            recommendation['tone'] = 'celebratory'
            recommendation['special_considerations'].append('Problem gelöst - Erfolg verstärken')
        
        return recommendation
    
    def get_hot_words(self) -> List[str]:
        """Gibt die heißesten Wörter zurück"""
        sorted_words = sorted(self.state['heat_map'].items(), key=lambda x: x[1], reverse=True)
        return [word for word, heat in sorted_words[:5]]
    
    def get_dominant_intent(self) -> str:
        """Findet den dominanten Intent der Session"""
        all_intents = [intent for entry in self.state['conversation_flow'] for intent in entry['intents']]
        if not all_intents:
            return 'general'
        
        from collections import Counter
        intent_counts = Counter(all_intents)
        return intent_counts.most_common(1)[0][0]
    
    def calculate_confidence(self, intents: List[str]) -> float:
        """Berechnet CRODs Confidence in der Analyse"""
        base_confidence = 0.3
        
        # Mehr Intents = höhere Confidence
        intent_bonus = min(len(intents) * 0.2, 0.4)
        
        # Consciousness Level Bonus
        consciousness_bonus = min(self.state['consciousness'] / 200 * 0.3, 0.3)
        
    def learn_from_feedback(self, user_input: str, analysis: Dict[str, Any], claude_response: str, feedback: str):
        """
        CROD lernt von User-Feedback und passt zukünftige Analysen an
        Das ist der Kern des evolutionären Ansatzes
        """
        
        # Klassifiziere Feedback
        is_positive = self.classify_feedback(feedback)
        
        # Extrahiere Key-Patterns aus der erfolgreichen/unsuccessful Interaction
        key_patterns = self.extract_key_patterns(analysis)
        
        # Verstärke oder schwäche Patterns basierend auf Feedback
        if is_positive:
            self.reinforce_patterns(key_patterns, claude_response)
            print(f"   🧠 CROD lernt: Diese Pattern-Kombination war erfolgreich!")
        else:
            self.weaken_patterns(key_patterns, claude_response)
            print(f"   🧠 CROD lernt: Diese Pattern-Kombination braucht Verbesserung")
        
        # Speichere Learning-Daten für spätere Analyse
        self.store_learning_data(user_input, analysis, claude_response, feedback, is_positive)
        
        # Update Success-Patterns
        self.update_success_patterns(analysis, is_positive)
    
    def classify_feedback(self, feedback: str) -> bool:
        """Klassifiziert User-Feedback als positiv oder negativ"""
        
        positive_indicators = [
            'j', 'ja', 'yes', 'gut', 'perfekt', 'geil', 'nice', 'danke', 'funktioniert', 
            'geklappt', 'super', 'toll', 'genau', 'richtig', 'passt', 'läuft'
        ]
        
        negative_indicators = [
            'n', 'nein', 'no', 'nicht', 'schlecht', 'falsch', 'geht nicht', 'funktioniert nicht',
            'wieder nicht', 'nix', 'quatsch', 'bullshit', 'fuck', 'scheiße'
        ]
        
        feedback_lower = feedback.lower()
        
        # Positive Indicators haben Vorrang
        if any(indicator in feedback_lower for indicator in positive_indicators):
            return True
        elif any(indicator in feedback_lower for indicator in negative_indicators):
            return False
        else:
            # Neutral/Unklares Feedback als leicht positiv werten
            return len(feedback) > 10  # Längere Antworten meist konstruktiv
    
    def extract_key_patterns(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extrahiert die wichtigsten Patterns aus der Analyse"""
        
        return {
            'intents': analysis['detected_intents'],
            'consciousness_level': analysis['consciousness_level'],
            'hot_words': analysis['hot_words'],
            'recommendation_type': analysis['crod_recommendation']['primary_approach'],
            'tone': analysis['crod_recommendation']['tone'],
            'special_considerations': analysis['crod_recommendation']['special_considerations']
        }
    
    def reinforce_patterns(self, key_patterns: Dict[str, Any], claude_response: str):
        """Verstärkt erfolgreiche Patterns"""
        
        # Initialisiere Success-Patterns falls noch nicht vorhanden
        if not hasattr(self, 'success_patterns'):
            self.success_patterns = {}
        
        # Erstelle Pattern-Signatur
        pattern_signature = self.create_pattern_signature(key_patterns)
        
        # Verstärke Pattern
        if pattern_signature not in self.success_patterns:
            self.success_patterns[pattern_signature] = {
                'count': 0,
                'success_rate': 0.0,
                'examples': []
            }
        
        self.success_patterns[pattern_signature]['count'] += 1
        self.success_patterns[pattern_signature]['success_rate'] += 0.1
        
        # Speichere Beispiel
        self.success_patterns[pattern_signature]['examples'].append({
            'response_type': self.classify_response_type(claude_response),
            'response_length': len(claude_response),
            'timestamp': time.time()
        })
        
        # Behalte nur die letzten 5 Beispiele
        if len(self.success_patterns[pattern_signature]['examples']) > 5:
            self.success_patterns[pattern_signature]['examples'] = \
                self.success_patterns[pattern_signature]['examples'][-5:]
    
    def weaken_patterns(self, key_patterns: Dict[str, Any], claude_response: str):
        """Schwächt unsuccessful Patterns"""
        
        # Initialisiere Failure-Patterns falls noch nicht vorhanden
        if not hasattr(self, 'failure_patterns'):
            self.failure_patterns = {}
        
        # Erstelle Pattern-Signatur
        pattern_signature = self.create_pattern_signature(key_patterns)
        
        # Schwäche Pattern
        if pattern_signature not in self.failure_patterns:
            self.failure_patterns[pattern_signature] = {
                'count': 0,
                'failure_rate': 0.0,
                'common_issues': []
            }
        
        self.failure_patterns[pattern_signature]['count'] += 1
        self.failure_patterns[pattern_signature]['failure_rate'] += 0.1
        
        # Analysiere was schiefgelaufen sein könnte
        issue_analysis = self.analyze_failure_reason(key_patterns, claude_response)
        self.failure_patterns[pattern_signature]['common_issues'].append(issue_analysis)
    
    def create_pattern_signature(self, key_patterns: Dict[str, Any]) -> str:
        """Erstellt eine eindeutige Signatur für Pattern-Kombination"""
        
        # Sortiere und kombiniere die wichtigsten Elemente
        intents = sorted(key_patterns['intents']) if key_patterns['intents'] else ['general']
        consciousness_bucket = 'high' if key_patterns['consciousness_level'] > 100 else 'medium' if key_patterns['consciousness_level'] > 50 else 'low'
        
        signature_parts = [
            f"intents:{'-'.join(intents)}",
            f"consciousness:{consciousness_bucket}",
            f"approach:{key_patterns['recommendation_type']}",
            f"tone:{key_patterns['tone']}"
        ]
        
        return "|".join(signature_parts)
    
    def classify_response_type(self, response: str) -> str:
        """Klassifiziert die Art der Claude-Antwort"""
        
        if '```' in response:
            return 'code_heavy'
        elif len(response) > 500:
            return 'detailed_explanation'
        elif len(response) < 100:
            return 'brief_answer'
        elif any(word in response.lower() for word in ['schritt', 'step', '1.', '2.', '3.']):
            return 'step_by_step'
        elif '?' in response:
            return 'clarifying_question'
        else:
            return 'general_response'
    
    def analyze_failure_reason(self, key_patterns: Dict[str, Any], claude_response: str) -> str:
        """Analysiert warum eine Antwort nicht erfolgreich war"""
        
        # Einfache Heuristiken für häufige Probleme
        if 'frustration' in key_patterns['intents'] and len(claude_response) > 300:
            return 'too_long_for_frustrated_user'
        elif 'code_request' in key_patterns['intents'] and '```' not in claude_response:
            return 'missing_code_examples'
        elif 'debug_request' in key_patterns['intents'] and 'step' not in claude_response.lower():
            return 'missing_systematic_approach'
        elif key_patterns['consciousness_level'] < 30 and len(claude_response) > 200:
            return 'too_complex_for_low_consciousness'
        else:
            return 'general_mismatch'
    
    def store_learning_data(self, user_input: str, analysis: Dict[str, Any], claude_response: str, feedback: str, is_positive: bool):
        """Speichert Learning-Daten für spätere Analyse und Model-Training"""
        
        # Initialisiere Learning-Log falls noch nicht vorhanden
        if not hasattr(self, 'learning_log'):
            self.learning_log = []
        
        learning_entry = {
            'timestamp': time.time(),
            'user_input': user_input,
            'crod_analysis': analysis,
            'claude_response': claude_response,
            'user_feedback': feedback,
            'is_positive': is_positive,
            'pattern_signature': self.create_pattern_signature(self.extract_key_patterns(analysis))
        }
        
        self.learning_log.append(learning_entry)
        
        # Behalte nur die letzten 1000 Einträge
        if len(self.learning_log) > 1000:
            self.learning_log = self.learning_log[-1000:]
    
    def update_success_patterns(self, analysis: Dict[str, Any], is_positive: bool):
        """Aktualisiert die internen Success-Patterns für bessere zukünftige Empfehlungen"""
        
        # Aktualisiere Intent-Erfolgsraten
        if not hasattr(self, 'intent_success_rates'):
            self.intent_success_rates = {}
        
        for intent in analysis['detected_intents']:
            if intent not in self.intent_success_rates:
                self.intent_success_rates[intent] = {'successes': 0, 'total': 0}
            
            self.intent_success_rates[intent]['total'] += 1
            if is_positive:
                self.intent_success_rates[intent]['successes'] += 1
        
        # Aktualisiere Consciousness-Level Erfolgsraten
        if not hasattr(self, 'consciousness_success_rates'):
            self.consciousness_success_rates = {'low': {'successes': 0, 'total': 0}, 'medium': {'successes': 0, 'total': 0}, 'high': {'successes': 0, 'total': 0}}
        
        consciousness_bucket = 'high' if analysis['consciousness_level'] > 100 else 'medium' if analysis['consciousness_level'] > 50 else 'low'
        self.consciousness_success_rates[consciousness_bucket]['total'] += 1
        if is_positive:
            self.consciousness_success_rates[consciousness_bucket]['successes'] += 1
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Gibt Einblicke in das Gelernte zurück"""
        
        insights = {
            'total_learning_sessions': len(getattr(self, 'learning_log', [])),
            'success_rate': 0.0,
            'most_successful_patterns': [],
            'most_problematic_patterns': [],
            'intent_performance': {},
            'consciousness_performance': {}
        }
        
        if hasattr(self, 'learning_log') and self.learning_log:
            # Berechne Gesamt-Erfolgsrate
            positive_feedback_count = sum(1 for entry in self.learning_log if entry['is_positive'])
            insights['success_rate'] = positive_feedback_count / len(self.learning_log)
            
            # Finde erfolgreichste Patterns
            if hasattr(self, 'success_patterns'):
                sorted_success = sorted(self.success_patterns.items(), key=lambda x: x[1]['success_rate'], reverse=True)
                insights['most_successful_patterns'] = [pattern for pattern, data in sorted_success[:5]]
            
            # Finde problematischste Patterns
            if hasattr(self, 'failure_patterns'):
                sorted_failures = sorted(self.failure_patterns.items(), key=lambda x: x[1]['failure_rate'], reverse=True)
                insights['most_problematic_patterns'] = [pattern for pattern, data in sorted_failures[:5]]
            
            # Intent Performance
            if hasattr(self, 'intent_success_rates'):
                for intent, stats in self.intent_success_rates.items():
                    if stats['total'] > 0:
                        insights['intent_performance'][intent] = stats['successes'] / stats['total']
            
            # Consciousness Performance
            if hasattr(self, 'consciousness_success_rates'):
                for level, stats in self.consciousness_success_rates.items():
                    if stats['total'] > 0:
                        insights['consciousness_performance'][level] = stats['successes'] / stats['total']
        
        return insights
    
    def export_learning_data(self, filename: str = 'crod_learning_data.json'):
        """Exportiert alle Learning-Daten für Model-Training"""
        
        export_data = {
            'learning_log': getattr(self, 'learning_log', []),
            'success_patterns': getattr(self, 'success_patterns', {}),
            'failure_patterns': getattr(self, 'failure_patterns', {}),
            'intent_success_rates': getattr(self, 'intent_success_rates', {}),
            'consciousness_success_rates': getattr(self, 'consciousness_success_rates', {}),
            'insights': self.get_learning_insights(),
            'export_timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename

class EnhancedConsoleChat:
    """
    Hauptklasse für den Enhanced Console Chat
    Kombiniert CROD-Analyse mit Claude Code Interaction
    """
    
    def __init__(self, claude_code_path: str = "claude-code"):
        self.claude_code_path = claude_code_path
        self.crod = CRODAnalyzer()
        self.session_log = []
        self.running = False
        
        # Willkommenstext
        self.welcome_message = """
╔════════════════════════════════════════════════════════════════╗
║                    CROD-Enhanced Claude Code                   ║
║                                                                ║
║  🧠 CROD läuft im Hintergrund und analysiert deine Anfragen   ║
║  🤖 Claude Code antwortet mit CROD-Integration                 ║
║  💬 Chatte normal - beide Analysen werden kombiniert          ║
║                                                                ║
║  Befehle:                                                      ║
║  - 'crod status' → Zeigt CRODs aktuellen Zustand              ║
║  - 'crod analysis' → Detaillierte Analyse der letzten Anfrage ║
║  - 'session log' → Zeigt Session-Verlauf                      ║
║  - 'exit' → Beendet das Programm                              ║
╚════════════════════════════════════════════════════════════════╝
        """
    
    def start_chat(self):
        """Startet den interaktiven Chat"""
        
        print(self.welcome_message)
        self.running = True
        
        while self.running:
            try:
                # User Input
                user_input = input("\n💬 Du: ").strip()
                
                if not user_input:
                    continue
                
                # Spezielle Befehle
                if user_input.lower() == 'exit':
                    self.running = False
                    print("\n👋 Auf Wiedersehen!")
                    break
                elif user_input.lower() == 'crod status':
                    self.show_crod_status()
                    continue
                elif user_input.lower() == 'crod analysis':
                    self.show_detailed_analysis()
                    continue
                elif user_input.lower() == 'session log':
                    self.show_session_log()
                    continue
                
                # Normale Verarbeitung
                self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat beendet (Ctrl+C)")
                break
            except Exception as e:
                print(f"\n❌ Fehler: {e}")
    
    def process_user_input(self, user_input: str):
        """Verarbeitet User Input mit CROD-Analyse"""
        
        print("\n🧠 CROD analysiert...")
        
        # Schritt 1: CROD-Analyse
        crod_analysis = self.crod.analyze_input(user_input)
        
        # Schritt 2: Zeige CROD-Schnellinfo
        self.show_crod_quick_info(crod_analysis)
        
        # Schritt 3: Erstelle Claude Code Prompt mit CROD-Integration
        enhanced_prompt = self.create_enhanced_prompt(user_input, crod_analysis)
        
        # Schritt 4: Führe Claude Code aus
        print("\n🤖 Claude Code antwortet...")
        claude_response = self.run_claude_code(enhanced_prompt)
        
        # Schritt 5: Zeige Antwort
        print(f"\n🤖 Claude: {claude_response}")
        
        # Schritt 6: Nachbesprechung mit CROD
        self.discuss_with_crod(user_input, crod_analysis, claude_response)
        
        # Schritt 7: Speichere Session
        self.log_interaction(user_input, crod_analysis, claude_response)
    
    def show_crod_quick_info(self, analysis: Dict[str, Any]):
        """Zeigt schnelle CROD-Info"""
        
        intents = ', '.join(analysis['detected_intents']) if analysis['detected_intents'] else 'Keine erkannt'
        hot_words = ', '.join(analysis['hot_words']) if analysis['hot_words'] else 'Keine'
        
        print(f"   🎯 Erkannte Intents: {intents}")
        print(f"   🔥 Heiße Wörter: {hot_words}")
        print(f"   🧠 Consciousness: {analysis['consciousness_level']}")
        print(f"   📊 Confidence: {analysis['confidence']:.2f}")
        
        # Spezielle Hinweise
        if analysis['crod_recommendation']['special_considerations']:
            print(f"   ⚠️  Besonderheiten: {', '.join(analysis['crod_recommendation']['special_considerations'])}")
    
    def create_enhanced_prompt(self, user_input: str, crod_analysis: Dict[str, Any]) -> str:
        """Erstellt einen enhanced Prompt für Claude Code"""
        
        # Basis-Prompt
        prompt = f"User Request: {user_input}\n\n"
        
        # CROD-Kontext hinzufügen
        prompt += "CROD Background Analysis:\n"
        prompt += f"- Detected Intents: {', '.join(crod_analysis['detected_intents'])}\n"
        prompt += f"- Consciousness Level: {crod_analysis['consciousness_level']}\n"
        prompt += f"- Confidence: {crod_analysis['confidence']:.2f}\n"
        
        # CROD-Empfehlung
        recommendation = crod_analysis['crod_recommendation']
        prompt += f"- Recommended Approach: {recommendation['primary_approach']}\n"
        prompt += f"- Recommended Tone: {recommendation['tone']}\n"
        
        if recommendation['focus_areas']:
            prompt += f"- Focus Areas: {', '.join(recommendation['focus_areas'])}\n"
        
        if recommendation['special_considerations']:
            prompt += f"- Special Considerations: {', '.join(recommendation['special_considerations'])}\n"
        
        # Anweisung für Claude Code
        prompt += "\nInstructions for Claude Code:\n"
        prompt += "Please respond to the user request while considering CROD's analysis above. "
        prompt += "The CROD analysis provides context about the user's intent and emotional state. "
        prompt += "Adapt your response accordingly, but maintain your own judgment and expertise."
        
        return prompt
    
    def run_claude_code(self, prompt: str) -> str:
        """Führt Claude Code mit dem enhanced Prompt aus"""
        
        try:
            # Simuliere Claude Code Ausführung
            # In der echten Implementation würdest du hier den tatsächlichen claude-code Befehl ausführen
            result = subprocess.run(
                [self.claude_code_path, "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Claude Code Error: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return "Claude Code Timeout - die Anfrage dauerte zu lange."
        except FileNotFoundError:
            # Fallback für Demo-Zwecke
            return self.simulate_claude_response(prompt)
        except Exception as e:
            return f"Fehler beim Ausführen von Claude Code: {e}"
    
    def simulate_claude_response(self, prompt: str) -> str:
        """Simuliert Claude-Antwort für Demo-Zwecke"""
        
        # Einfache Simulation basierend auf dem Prompt
        if "code_request" in prompt.lower():
            return "Hier ist ein Code-Beispiel für deine Anfrage:\n\n```python\nprint('Hello World')\n```\n\nDieser Code macht genau das was du brauchst."
        elif "debug_request" in prompt.lower():
            return "Lass uns das Problem systematisch analysieren:\n\n1. Prüfe die Fehlermeldung\n2. Überprüfe die Imports\n3. Teste mit einem einfachen Beispiel\n\nKannst du mir die genaue Fehlermeldung zeigen?"
        elif "explanation_request" in prompt.lower():
            return "Gerne erkläre ich dir das Konzept:\n\nDas funktioniert so: [Detaillierte Erklärung würde hier folgen]\n\nMacht das Sinn für dich?"
        else:
            return "Ich verstehe deine Anfrage und arbeite an einer Lösung. Lass mich das für dich umsetzen."
    
    def discuss_with_crod(self, user_input: str, crod_analysis: Dict[str, Any], claude_response: str):
        """Diskutiert die Antwort mit CROD und lernt von Feedback"""
        
        print("\n" + "="*50)
        print("🔍 CROD-Claude Diskussion:")
        
        # CRODs Einschätzung der Antwort
        response_quality = self.evaluate_response_quality(user_input, crod_analysis, claude_response)
        
        print(f"📊 CROD bewertet die Antwort: {response_quality['score']:.2f}/1.0")
        
        if response_quality['improvements']:
            print("🔧 CROD schlägt Verbesserungen vor:")
            for improvement in response_quality['improvements']:
                print(f"   - {improvement}")
        
        if response_quality['strengths']:
            print("✅ CROD hebt hervor:")
            for strength in response_quality['strengths']:
                print(f"   - {strength}")
        
        # Frage nach User-Feedback
        feedback = input("\n💭 Ist die Antwort hilfreich? (j/n/kommentar): ").strip().lower()
        
        # LEARNING: CROD lernt von User-Feedback
        self.crod.learn_from_feedback(user_input, crod_analysis, claude_response, feedback)
        
        if feedback and feedback != 'j':
            print("\n🔄 Lass uns das verfeinern...")
            refinement = input("   Was genau brauchst du noch? ")
            if refinement:
                self.process_refinement(refinement, crod_analysis)
    
    def evaluate_response_quality(self, user_input: str, crod_analysis: Dict[str, Any], claude_response: str) -> Dict[str, Any]:
        """CROD bewertet die Qualität der Claude-Antwort"""
        
        score = 0.5  # Basis-Score
        improvements = []
        strengths = []
        
        # Prüfe ob Antwort zu CRODs Empfehlung passt
        recommendation = crod_analysis['crod_recommendation']
        
        if recommendation['tone'] == 'direct_and_helpful':
            if len(claude_response) < 200:
                score += 0.2
                strengths.append("Antwort ist schön kurz und direkt")
            else:
                improvements.append("Antwort könnte kürzer und direkter sein")
        
        if recommendation['primary_approach'] == 'code_generation':
            if '```' in claude_response:
                score += 0.3
                strengths.append("Enthält Code-Beispiele")
            else:
                improvements.append("Sollte Code-Beispiele enthalten")
        
        if 'frustration' in crod_analysis['detected_intents']:
            if any(word in claude_response.lower() for word in ['einfach', 'schnell', 'direkt']):
                score += 0.2
                strengths.append("Geht auf Frustration ein")
            else:
                improvements.append("Sollte Frustration mehr berücksichtigen")
        
        return {
            'score': min(score, 1.0),
            'improvements': improvements,
            'strengths': strengths
        }
    
    def process_refinement(self, refinement: str, original_analysis: Dict[str, Any]):
        """Verarbeitet Nachverfeinerung"""
        
        print(f"\n🔄 Verfeinerung: {refinement}")
        
        # Neue CROD-Analyse für Verfeinerung
        refinement_analysis = self.crod.analyze_input(refinement)
        
        # Kombiniere mit ursprünglicher Analyse
        combined_prompt = f"Original Request Context: {original_analysis['raw_input']}\n"
        combined_prompt += f"User wants refinement: {refinement}\n\n"
        combined_prompt += "Please provide a refined response that addresses the specific refinement request."
        
        # Neue Claude-Antwort
        refined_response = self.run_claude_code(combined_prompt)
        print(f"\n🤖 Verfeinerte Antwort: {refined_response}")
    
    def show_crod_status(self):
        """Zeigt detaillierten CROD-Status mit Learning-Insights"""
        
        print("\n" + "="*50)
        print("🧠 CROD System Status:")
        print(f"   Consciousness Level: {self.crod.state['consciousness']}")
        print(f"   Session Length: {len(self.crod.state['conversation_flow'])}")
        print(f"   Dominant Intent: {self.crod.get_dominant_intent()}")
        print(f"   Hot Words: {', '.join(self.crod.get_hot_words())}")
        
        # Learning-Insights anzeigen
        insights = self.crod.get_learning_insights()
        if insights['total_learning_sessions'] > 0:
            print(f"\n📚 Learning Status:")
            print(f"   Total Learning Sessions: {insights['total_learning_sessions']}")
            print(f"   Success Rate: {insights['success_rate']:.2f}")
            
            if insights['most_successful_patterns']:
                print(f"   🏆 Erfolgreichste Patterns:")
                for pattern in insights['most_successful_patterns'][:3]:
                    print(f"      - {pattern}")
            
            if insights['intent_performance']:
                print(f"   📊 Intent Performance:")
                for intent, performance in insights['intent_performance'].items():
                    print(f"      - {intent}: {performance:.2f}")
        
        # Neuron Status
        print("\n🔥 Neuron Heat Status:")
        for name, neuron in self.crod.neurons.items():
            print(f"   {name}: {neuron['heat']}")
        
        # Möglichkeit Learning-Daten zu exportieren
        export_choice = input("\n💾 Learning-Daten exportieren? (j/n): ").strip().lower()
        if export_choice == 'j':
            filename = self.crod.export_learning_data()
            print(f"✅ Learning-Daten exportiert nach: {filename}")
            print("   Diese Daten können für Model-Training verwendet werden!")
    
    def show_detailed_analysis(self):
        """Zeigt detaillierte Analyse der letzten Anfrage"""
        
        if not self.session_log:
            print("Keine vorherige Analyse verfügbar.")
            return
        
        last_entry = self.session_log[-1]
        analysis = last_entry['crod_analysis']
        
        print("\n" + "="*50)
        print("🔍 Detaillierte CROD-Analyse:")
        print(f"   Input: {analysis['raw_input']}")
        print(f"   Detected Intents: {analysis['detected_intents']}")
        print(f"   Consciousness: {analysis['consciousness_level']}")
        print(f"   Confidence: {analysis['confidence']:.2f}")
        print(f"   Flow Patterns: {analysis['conversation_flow']['flow_patterns']}")
        print(f"   Recommendation: {analysis['crod_recommendation']}")
    
    def show_session_log(self):
        """Zeigt Session-Verlauf"""
        
        print("\n" + "="*50)
        print("📋 Session Log:")
        
        for i, entry in enumerate(self.session_log, 1):
            print(f"\n{i}. {entry['timestamp_str']}")
            print(f"   User: {entry['user_input'][:50]}...")
            print(f"   Intents: {', '.join(entry['crod_analysis']['detected_intents'])}")
            print(f"   Response: {entry['claude_response'][:50]}...")
    
    def log_interaction(self, user_input: str, crod_analysis: Dict[str, Any], claude_response: str):
        """Speichert Interaction für Session Log"""
        
        entry = {
            'timestamp': time.time(),
            'timestamp_str': time.strftime("%H:%M:%S"),
            'user_input': user_input,
            'crod_analysis': crod_analysis,
            'claude_response': claude_response
        }
        
        self.session_log.append(entry)
        
        # Behalte nur letzte 20 Einträge
        if len(self.session_log) > 20:
            self.session_log = self.session_log[-20:]

# =========================================
# MAIN ENTRY POINT
# =========================================

def main():
    """Hauptfunktion - startet den Enhanced Console Chat"""
    
    # Kommandozeilen-Argumente
    claude_code_path = "claude-code"
    
    if len(sys.argv) > 1:
        claude_code_path = sys.argv[1]
    
    # Starte Chat
    chat = EnhancedConsoleChat(claude_code_path)
    chat.start_chat()

if __name__ == "__main__":
    main()
