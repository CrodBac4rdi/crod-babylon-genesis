# plugins/engine_plugin.py - CROD Engine Plugin
from plugin_base import CRODPlugin
import time
from typing import Dict, Any

class EnginePlugin(CRODPlugin):
    """Main CROD Engine orchestrator plugin"""
    
    @property
    def name(self):
        return "Engine"
    
    @property
    def version(self):
        return "2.0.0"
    
    @property
    def description(self):
        return "Main CROD engine orchestrating all operations"
    
    def initialize(self, system):
        self.system = system
        self.session_start = time.time()
        self.processed_count = 0
    
    def get_capabilities(self):
        return [
            'process_text',
            'get_session_stats',
            'run_full_analysis',
            'export_session'
        ]
    
    def process_text(self, text: str) -> Dict:
        """Main text processing pipeline"""
        start_time = time.time()
        results = {
            'input': text,
            'timestamp': time.time(),
            'processing': {}
        }
        
        # 1. Chat processing
        if 'process_message' in self.system.capability_map:
            try:
                chat_result = self.system.call_capability('process_message', text)
                results['processing']['chat'] = chat_result
            except Exception as e:
                results['processing']['chat_error'] = str(e)
        
        # 2. Pattern detection
        if 'detect_patterns' in self.system.capability_map:
            try:
                patterns = self.system.call_capability('detect_patterns', text)
                results['processing']['patterns'] = patterns
            except Exception as e:
                results['processing']['pattern_error'] = str(e)
        
        # 3. Store in database
        if 'add_route' in self.system.capability_map:
            try:
                # Convert text to atoms (simplified)
                atoms = []
                if 'find_atom_sequence' in self.system.capability_map:
                    atoms = self.system.call_capability('find_atom_sequence', text)
                
                # Find matched pattern
                matched_pattern = None
                if results['processing'].get('patterns'):
                    matched_pattern = results['processing']['patterns'][0]['pattern_id']
                
                # Store route
                self.system.call_capability(
                    'add_route',
                    atoms,
                    matched_pattern,
                    800,  # Default execution key
                    True,  # Success
                    time.time() - start_time
                )
            except Exception as e:
                results['processing']['storage_error'] = str(e)
        
        # 4. ML Analysis (if significant patterns found)
        if results['processing'].get('patterns') and 'calculate_gradients' in self.system.capability_map:
            try:
                ml_analysis = self.system.call_capability('visualize_gradients')
                results['processing']['ml'] = ml_analysis
            except Exception as e:
                results['processing']['ml_error'] = str(e)
        
        # Update stats
        self.processed_count += 1
        results['processing_time'] = time.time() - start_time
        
        # Emit completion event
        self.system.emit_event(
            'text_processing_complete',
            results,
            self.name
        )
        
        return results
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        stats = {
            'session_duration': time.time() - self.session_start,
            'messages_processed': self.processed_count,
            'uptime': self._format_duration(time.time() - self.session_start),
            'capabilities_available': list(self.system.capability_map.keys()),
            'plugins_loaded': len(self.system.plugins)
        }
        
        # Get stats from other plugins
        if 'get_stats' in self.system.capability_map:
            try:
                db_stats = self.system.call_capability('get_stats')
                stats['database'] = db_stats
            except:
                pass
        
        if 'analyze_session' in self.system.capability_map:
            try:
                chat_stats = self.system.call_capability('analyze_session')
                stats['chat'] = chat_stats
            except:
                pass
        
        return stats
    
    def run_full_analysis(self, text: str) -> Dict:
        """Run comprehensive analysis on text"""
        analysis = {
            'text': text,
            'timestamp': time.time(),
            'analyses': {}
        }
        
        # Process through main pipeline
        process_result = self.process_text(text)
        analysis['analyses']['processing'] = process_result
        
        # Additional deep analysis
        if 'analyze_text' in self.system.capability_map:
            try:
                deep_analysis = self.system.call_capability('analyze_text', text)
                analysis['analyses']['deep'] = deep_analysis
            except Exception as e:
                analysis['analyses']['deep_error'] = str(e)
        
        # Get recommendations
        if 'ml' in process_result['processing']:
            analysis['recommendations'] = process_result['processing']['ml'].get('recommendations', [])
        
        return analysis
    
    def export_session(self) -> Dict:
        """Export current session data"""
        export = {
            'session_id': f"crod_session_{int(self.session_start)}",
            'timestamp': time.time(),
            'duration': time.time() - self.session_start,
            'stats': self.get_session_stats()
        }
        
        # Get message history
        if 'get_message_history' in self.system.capability_map:
            try:
                messages = self.system.call_capability('get_message_history', 9999)
                export['messages'] = messages
            except:
                pass
        
        # Get all patterns
        if 'get_all_patterns' in self.system.capability_map:
            try:
                patterns = self.system.call_capability('get_all_patterns')
                export['patterns'] = patterns
            except:
                pass
        
        return export
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration as H:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{secs:02d}"
    
    def handle_event(self, event_type: str, data: Dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'request_full_pipeline':
            # Run full processing pipeline
            if 'text' in data:
                result = self.process_text(data['text'])
                self.system.emit_event(
                    'pipeline_complete',
                    result,
                    self.name,
                    source
                )