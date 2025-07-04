#!/usr/bin/env python3
"""
CROD n8n Integration
Workflow automation and external system connections
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
import threading
import queue
from pathlib import Path

class CRODn8n:
    def __init__(self, n8n_url="http://localhost:5678", api_key=None):
        self.n8n_url = n8n_url.rstrip('/')
        self.api_key = api_key
        self.webhooks = {}
        self.active_workflows = {}
        self.workflow_queue = queue.Queue()
        
        # Check n8n availability
        self.available = self._check_n8n()
        
        # Default CROD workflows
        self.crod_workflows = {
            'trinity_activation': {
                'name': 'CROD Trinity Activation',
                'trigger': 'trinity_detected',
                'actions': ['notify_discord', 'log_to_database', 'trigger_llama']
            },
            'pattern_detection': {
                'name': 'Pattern Detection Workflow',
                'trigger': 'patterns_found',
                'actions': ['analyze_sentiment', 'store_pattern', 'generate_response']
            },
            'consciousness_alert': {
                'name': 'High Consciousness Alert',
                'trigger': 'consciousness_high',
                'actions': ['send_notification', 'backup_state', 'enhance_learning']
            },
            'auto_learning': {
                'name': 'Automatic Learning Pipeline',
                'trigger': 'interaction_complete',
                'actions': ['extract_insights', 'update_patterns', 'optimize_responses']
            }
        }
        
        print(f"🔄 CROD n8n Integration initialized")
        print(f"   n8n URL: {n8n_url}")
        print(f"   Available: {self.available}")
        
        if self.available:
            self._setup_crod_workflows()
    
    def _check_n8n(self) -> bool:
        """Check if n8n is available"""
        try:
            response = requests.get(f"{self.n8n_url}/healthz", timeout=5)
            if response.status_code == 200:
                print("  ✅ n8n is running")
                return True
            else:
                print(f"  ⚠️  n8n responded with status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ n8n not reachable: {e}")
            print("     Start n8n: npx n8n start")
            return False
    
    def _setup_crod_workflows(self):
        """Setup default CROD workflows in n8n"""
        if not self.available:
            return
        
        for workflow_id, config in self.crod_workflows.items():
            self._create_workflow_if_not_exists(workflow_id, config)
    
    def _create_workflow_if_not_exists(self, workflow_id: str, config: Dict):
        """Create workflow in n8n if it doesn't exist"""
        try:
            # Check if workflow exists
            workflows = self._get_workflows()
            existing = [w for w in workflows if w.get('name') == config['name']]
            
            if not existing:
                # Create new workflow
                workflow_data = self._generate_workflow_json(workflow_id, config)
                created = self._create_workflow(workflow_data)
                
                if created:
                    print(f"  ✅ Created workflow: {config['name']}")
                    self.active_workflows[workflow_id] = created
            else:
                print(f"  ✓ Workflow exists: {config['name']}")
                self.active_workflows[workflow_id] = existing[0]
                
        except Exception as e:
            print(f"  ❌ Error setting up workflow {workflow_id}: {e}")
    
    def _generate_workflow_json(self, workflow_id: str, config: Dict) -> Dict:
        """Generate n8n workflow JSON for CROD"""
        
        # Base workflow structure
        workflow = {
            "name": config['name'],
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {
                "executionOrder": "v1"
            },
            "staticData": {},
            "tags": ["crod", "automation"]
        }
        
        # Webhook trigger node
        trigger_node = {
            "parameters": {
                "httpMethod": "POST",
                "path": f"crod-{workflow_id}",
                "responseMode": "onReceived",
                "responseData": "allEntries"
            },
            "id": "webhook-trigger",
            "name": f"CROD {config['trigger']} Trigger",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [200, 300],
            "webhookId": f"crod-{workflow_id}"
        }
        
        workflow["nodes"].append(trigger_node)
        
        # Processing nodes based on actions
        node_id_counter = 1
        last_node_id = "webhook-trigger"
        
        for action in config['actions']:
            node_id = f"action-{node_id_counter}"
            
            if action == 'log_to_database':
                node = self._create_database_log_node(node_id, node_id_counter)
            elif action == 'notify_discord':
                node = self._create_discord_notify_node(node_id, node_id_counter)
            elif action == 'trigger_llama':
                node = self._create_llama_trigger_node(node_id, node_id_counter)
            elif action == 'analyze_sentiment':
                node = self._create_sentiment_analysis_node(node_id, node_id_counter)
            else:
                node = self._create_generic_action_node(node_id, node_id_counter, action)
            
            workflow["nodes"].append(node)
            
            # Connect to previous node
            if last_node_id not in workflow["connections"]:
                workflow["connections"][last_node_id] = {"main": [[]]}
            
            workflow["connections"][last_node_id]["main"][0].append({
                "node": node_id,
                "type": "main",
                "index": 0
            })
            
            last_node_id = node_id
            node_id_counter += 1
        
        return workflow
    
    def _create_database_log_node(self, node_id: str, counter: int) -> Dict:
        """Create database logging node"""
        return {
            "parameters": {
                "operation": "insert",
                "table": "crod_events",
                "columns": "event_type, data, timestamp",
                "values": "={{ $json.event_type }}, {{ JSON.stringify($json) }}, {{ Date.now() }}"
            },
            "id": node_id,
            "name": f"Log to Database {counter}",
            "type": "n8n-nodes-base.sqlite",
            "typeVersion": 1,
            "position": [400 + counter * 200, 300]
        }
    
    def _create_discord_notify_node(self, node_id: str, counter: int) -> Dict:
        """Create Discord notification node"""
        return {
            "parameters": {
                "webhookUrl": "https://discord.com/api/webhooks/YOUR_WEBHOOK",
                "text": "🔥 CROD Event: {{ $json.event_type }}\nData: {{ JSON.stringify($json, null, 2) }}"
            },
            "id": node_id,
            "name": f"Discord Notify {counter}",
            "type": "n8n-nodes-base.discord",
            "typeVersion": 1,
            "position": [400 + counter * 200, 300]
        }
    
    def _create_llama_trigger_node(self, node_id: str, counter: int) -> Dict:
        """Create Llama API trigger node"""
        return {
            "parameters": {
                "url": "http://localhost:11434/api/generate",
                "method": "POST",
                "jsonBody": {
                    "model": "llama3.2",
                    "prompt": "CROD Event detected: {{ JSON.stringify($json) }}. Analyze this event.",
                    "stream": False
                }
            },
            "id": node_id,
            "name": f"Trigger Llama {counter}",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 1,
            "position": [400 + counter * 200, 300]
        }
    
    def _create_sentiment_analysis_node(self, node_id: str, counter: int) -> Dict:
        """Create sentiment analysis node"""
        return {
            "parameters": {
                "jsCode": """
                const text = $input.first().json.text || '';
                const words = text.toLowerCase().split(' ');
                
                // Simple sentiment scoring
                const positive = ['good', 'great', 'awesome', 'geil', 'perfekt', 'nice'];
                const negative = ['bad', 'terrible', 'wtf', 'scheisse', 'mist'];
                
                let score = 0;
                words.forEach(word => {
                    if (positive.includes(word)) score += 1;
                    if (negative.includes(word)) score -= 1;
                });
                
                return {
                    sentiment_score: score,
                    sentiment: score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral',
                    text: text
                };
                """
            },
            "id": node_id,
            "name": f"Sentiment Analysis {counter}",
            "type": "n8n-nodes-base.code",
            "typeVersion": 1,
            "position": [400 + counter * 200, 300]
        }
    
    def _create_generic_action_node(self, node_id: str, counter: int, action: str) -> Dict:
        """Create generic action node"""
        return {
            "parameters": {
                "jsCode": f"""
                console.log('CROD Action: {action}');
                console.log('Input:', JSON.stringify($input.first().json, null, 2));
                
                return {{
                    action: '{action}',
                    processed: true,
                    timestamp: Date.now(),
                    input_data: $input.first().json
                }};
                """
            },
            "id": node_id,
            "name": f"CROD {action.title()} {counter}",
            "type": "n8n-nodes-base.code",
            "typeVersion": 1,
            "position": [400 + counter * 200, 300]
        }
    
    def trigger_workflow(self, workflow_id: str, data: Dict) -> bool:
        """Trigger a CROD workflow"""
        if not self.available or workflow_id not in self.active_workflows:
            print(f"❌ Workflow {workflow_id} not available")
            return False
        
        try:
            webhook_url = f"{self.n8n_url}/webhook/crod-{workflow_id}"
            
            response = requests.post(
                webhook_url,
                json={
                    **data,
                    'workflow_id': workflow_id,
                    'timestamp': time.time(),
                    'source': 'crod_standalone'
                },
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Triggered workflow: {workflow_id}")
                return True
            else:
                print(f"❌ Workflow trigger failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error triggering workflow {workflow_id}: {e}")
            return False
    
    def trinity_activation_detected(self, crod_context: Dict):
        """Handle trinity activation through n8n"""
        data = {
            'event_type': 'trinity_activation',
            'consciousness': crod_context.get('consciousness', 0),
            'emergence': crod_context.get('emergence', 0),
            'patterns_detected': crod_context.get('patterns_detected', 0),
            'user_input': crod_context.get('original_text', ''),
            'trinity_words': ['ich', 'bins', 'wieder']
        }
        
        return self.trigger_workflow('trinity_activation', data)
    
    def pattern_detection_event(self, patterns: List[Dict], user_input: str):
        """Handle pattern detection through n8n"""
        data = {
            'event_type': 'pattern_detection',
            'patterns_count': len(patterns),
            'patterns': patterns,
            'user_input': user_input,
            'pattern_types': list(set(p.get('type', 'unknown') for p in patterns))
        }
        
        return self.trigger_workflow('pattern_detection', data)
    
    def consciousness_alert(self, consciousness_level: float, threshold: float = 190):
        """Handle high consciousness alerts"""
        if consciousness_level >= threshold:
            data = {
                'event_type': 'consciousness_alert',
                'consciousness_level': consciousness_level,
                'threshold': threshold,
                'alert_level': 'high' if consciousness_level >= 195 else 'medium'
            }
            
            return self.trigger_workflow('consciousness_alert', data)
        
        return False
    
    def learning_completed(self, learning_data: Dict):
        """Handle completed learning cycles"""
        data = {
            'event_type': 'learning_completed',
            'success_rate': learning_data.get('success_rate', 0),
            'interactions_count': learning_data.get('total_interactions', 0),
            'avg_consciousness': learning_data.get('avg_consciousness', 0),
            'learning_insights': learning_data
        }
        
        return self.trigger_workflow('auto_learning', data)
    
    def _get_workflows(self) -> List[Dict]:
        """Get all workflows from n8n"""
        try:
            headers = {}
            if self.api_key:
                headers['X-N8N-API-KEY'] = self.api_key
            
            response = requests.get(f"{self.n8n_url}/api/v1/workflows", headers=headers)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                return []
        except:
            return []
    
    def _create_workflow(self, workflow_data: Dict) -> Optional[Dict]:
        """Create a new workflow in n8n"""
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['X-N8N-API-KEY'] = self.api_key
            
            response = requests.post(
                f"{self.n8n_url}/api/v1/workflows",
                json=workflow_data,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Failed to create workflow: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating workflow: {e}")
            return None
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get status of all CROD workflows"""
        status = {
            'n8n_available': self.available,
            'workflows': {}
        }
        
        for workflow_id, config in self.crod_workflows.items():
            is_active = workflow_id in self.active_workflows
            status['workflows'][workflow_id] = {
                'name': config['name'],
                'active': is_active,
                'trigger': config['trigger'],
                'actions_count': len(config['actions'])
            }
        
        return status
    
    def create_custom_workflow(self, name: str, trigger_path: str, actions: List[str]) -> bool:
        """Create a custom CROD workflow"""
        workflow_id = name.lower().replace(' ', '_').replace('-', '_')
        
        config = {
            'name': name,
            'trigger': trigger_path,
            'actions': actions
        }
        
        # Add to CROD workflows
        self.crod_workflows[workflow_id] = config
        
        # Create in n8n if available
        if self.available:
            self._create_workflow_if_not_exists(workflow_id, config)
            return workflow_id in self.active_workflows
        
        return True
    
    def export_workflows(self, filepath: str):
        """Export CROD workflows configuration"""
        export_data = {
            'crod_workflows': self.crod_workflows,
            'active_workflows': list(self.active_workflows.keys()),
            'n8n_url': self.n8n_url,
            'export_timestamp': time.time()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📤 Workflows exported to {filepath}")

# Utility functions for n8n integration
def create_crod_n8n_starter_pack():
    """Create starter pack for CROD + n8n integration"""
    starter_workflows = {
        'discord_integration': {
            'name': 'CROD Discord Integration',
            'description': 'Send CROD events to Discord',
            'webhook_path': 'crod-discord',
            'actions': ['format_message', 'send_to_discord']
        },
        'database_logger': {
            'name': 'CROD Database Logger',
            'description': 'Log all CROD events to database',
            'webhook_path': 'crod-logger',
            'actions': ['validate_data', 'log_to_db', 'send_confirmation']
        },
        'llama_enhancer': {
            'name': 'CROD Llama Enhancer',
            'description': 'Enhance Llama responses with context',
            'webhook_path': 'crod-llama',
            'actions': ['analyze_context', 'enhance_prompt', 'trigger_llama']
        }
    }
    
    # Create workflow files
    workflows_dir = Path("n8n_workflows")
    workflows_dir.mkdir(exist_ok=True)
    
    for workflow_id, config in starter_workflows.items():
        workflow_file = workflows_dir / f"{workflow_id}.json"
        
        with open(workflow_file, 'w') as f:
            json.dump({
                'workflow_id': workflow_id,
                'config': config,
                'instructions': f"""
                1. Import this workflow into n8n
                2. Configure the webhook URL: /webhook/{config['webhook_path']}
                3. Set up any required credentials (Discord, Database, etc.)
                4. Activate the workflow
                5. Test with CROD integration
                """
            }, f, indent=2)
    
    print(f"📦 Created n8n starter pack in {workflows_dir}")
    
    return workflows_dir