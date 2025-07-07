#!/usr/bin/env python3
"""
CROD AI Chat Service - Backend für KI-Chatinterface
Unterstützt verschiedene KI-Modelle: Claude, GPT, etc.
"""

import sys
import json
import os
import requests
from typing import Dict, Any, Optional
import time

# Konfiguration
DEFAULT_MODEL = "claude"
API_KEYS = {
    "claude": os.environ.get("ANTHROPIC_API_KEY", ""),
    "gpt": os.environ.get("OPENAI_API_KEY", ""),
    "gemini": os.environ.get("GOOGLE_API_KEY", "")
}

# Model Endpoints
MODEL_ENDPOINTS = {
    "claude": "https://api.anthropic.com/v1/messages",
    "gpt": "https://api.openai.com/v1/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
}

class ChatService:
    """CROD Chat Service Interface zu verschiedenen KI-Modellen"""
    
    def __init__(self):
        self.conversation_history = []
    
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet eine Chat-Anfrage und gibt eine Antwort zurück
        
        Args:
            data: Dictionary mit 'message' und optional 'model'
            
        Returns:
            Dictionary mit der Antwort des KI-Modells
        """
        message = data.get("message", "")
        model = data.get("model", DEFAULT_MODEL)
        
        if not message:
            return {
                "content": "Keine Nachricht erhalten.",
                "model": model,
                "success": False
            }
            
        try:
            # Modellspezifische Verarbeitung
            if model == "claude":
                return self._call_claude(message)
            elif model == "gpt":
                return self._call_gpt(message)
            elif model == "gemini":
                return self._call_gemini(message)
            else:
                return {
                    "content": f"Unbekanntes Modell: {model}",
                    "model": model,
                    "success": False
                }
                
        except Exception as e:
            return {
                "content": f"Fehler bei der Verarbeitung: {str(e)}",
                "model": model,
                "success": False
            }
    
    def _call_claude(self, message: str) -> Dict[str, Any]:
        """Ruft Claude API auf"""
        api_key = API_KEYS.get("claude")
        if not api_key:
            # Wenn kein API-Key vorhanden, simuliere eine Antwort
            return self._simulate_ai_response(message, "claude")
            
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Konversationsverlauf einbeziehen
        messages = self.conversation_history + [{"role": "user", "content": message}]
        
        data = {
            "model": "claude-3-opus-20240229",
            "messages": messages,
            "max_tokens": 1000
        }
        
        response = requests.post(
            MODEL_ENDPOINTS["claude"],
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_message = result.get("content", [{"text": "Keine Antwort erhalten."}])[0]["text"]
            
            # Zur Konversation hinzufügen
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            # Konversation auf maximal 10 Nachrichten begrenzen
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                
            return {
                "content": ai_message,
                "model": "claude",
                "tokens_used": result.get("usage", {}).get("output_tokens", 0),
                "success": True
            }
        else:
            return {
                "content": f"API-Fehler: {response.status_code} - {response.text}",
                "model": "claude",
                "success": False
            }
    
    def _call_gpt(self, message: str) -> Dict[str, Any]:
        """Ruft GPT API auf"""
        api_key = API_KEYS.get("gpt")
        if not api_key:
            # Wenn kein API-Key vorhanden, simuliere eine Antwort
            return self._simulate_ai_response(message, "gpt")
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Konversationsverlauf einbeziehen
        messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent."}]
        for item in self.conversation_history:
            messages.append(item)
        messages.append({"role": "user", "content": message})
        
        data = {
            "model": "gpt-4",
            "messages": messages,
            "max_tokens": 1000
        }
        
        response = requests.post(
            MODEL_ENDPOINTS["gpt"],
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_message = result["choices"][0]["message"]["content"]
            
            # Zur Konversation hinzufügen
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            # Konversation auf maximal 10 Nachrichten begrenzen
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                
            return {
                "content": ai_message,
                "model": "gpt",
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                "success": True
            }
        else:
            return {
                "content": f"API-Fehler: {response.status_code} - {response.text}",
                "model": "gpt",
                "success": False
            }
    
    def _call_gemini(self, message: str) -> Dict[str, Any]:
        """Ruft Gemini API auf"""
        api_key = API_KEYS.get("gemini")
        if not api_key:
            # Wenn kein API-Key vorhanden, simuliere eine Antwort
            return self._simulate_ai_response(message, "gemini")
            
        # Konversation formatieren
        conversation = []
        for i in range(0, len(self.conversation_history), 2):
            if i+1 < len(self.conversation_history):
                conversation.append({
                    "parts": [{"text": self.conversation_history[i]["content"]}],
                    "role": "user"
                })
                conversation.append({
                    "parts": [{"text": self.conversation_history[i+1]["content"]}],
                    "role": "model"
                })
        
        # Aktuelle Nachricht hinzufügen
        conversation.append({
            "parts": [{"text": message}],
            "role": "user"
        })
        
        data = {
            "contents": conversation,
            "generationConfig": {
                "maxOutputTokens": 1000,
            }
        }
        
        url = f"{MODEL_ENDPOINTS['gemini']}?key={api_key}"
        
        response = requests.post(
            url,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_message = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Zur Konversation hinzufügen
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            # Konversation auf maximal 10 Nachrichten begrenzen
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                
            return {
                "content": ai_message,
                "model": "gemini",
                "success": True
            }
        else:
            return {
                "content": f"API-Fehler: {response.status_code} - {response.text}",
                "model": "gemini",
                "success": False
            }
    
    def _simulate_ai_response(self, message: str, model_name: str) -> Dict[str, Any]:
        """
        Simuliert eine AI-Antwort, wenn keine API-Keys verfügbar sind
        """
        # Kurze Verzögerung für realistischeres Verhalten
        time.sleep(1)
        
        # Einfache Antworten basierend auf Schlüsselwörtern
        if "hallo" in message.lower() or "hi" in message.lower():
            response = f"Hallo! Ich bin das simulierte {model_name.upper()}-Modell. Wie kann ich dir helfen?"
        elif "wie geht" in message.lower():
            response = "Mir geht es gut, danke der Nachfrage! Wie kann ich dir heute helfen?"
        elif "hilfe" in message.lower():
            response = "Ich bin hier, um zu helfen! Was möchtest du wissen?"
        elif "code" in message.lower() or "programmier" in message.lower():
            response = "Ich kann dir mit Programmieraufgaben helfen. Bitte teile mir mehr Details mit."
        elif "bild" in message.lower() or "visualisier" in message.lower():
            response = "Die Bildgenerierung kannst du über den entsprechenden Tab in der CROD-Oberfläche nutzen."
        elif "danke" in message.lower():
            response = "Gerne! Stehe jederzeit für weitere Fragen zur Verfügung."
        else:
            response = f"Ich habe deine Nachricht erhalten: '{message}'. Als simuliertes {model_name.upper()}-Modell kann ich darauf nur begrenzt antworten. Bitte konfiguriere einen API-Schlüssel für vollständige Funktionalität."
        
        return {
            "content": response,
            "model": model_name,
            "tokens_used": len(response.split()),
            "success": True
        }


def main():
    """Hauptfunktion zum Verarbeiten der Anfrage"""
    try:
        # Eingabe vom Node.js-Server lesen
        input_data = sys.stdin.read()
        request_data = json.loads(input_data)
        
        # Chat-Service initialisieren und Anfrage verarbeiten
        service = ChatService()
        response = service.process_request(request_data)
        
        # Antwort zurückgeben
        print(json.dumps(response))
        
    except Exception as e:
        error_response = {
            "content": f"Fehler im Chat-Service: {str(e)}",
            "model": request_data.get("model", DEFAULT_MODEL) if 'request_data' in locals() else DEFAULT_MODEL,
            "success": False
        }
        print(json.dumps(error_response))
        sys.exit(1)


if __name__ == "__main__":
    main()
