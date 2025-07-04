# plugins/ml_plugin.py - Example ML Plugin for CROD
from plugin_base import CRODPlugin
import numpy as np
import json

class MLAnalyzerPlugin(CRODPlugin):
    """Machine Learning analysis plugin"""
    
    @property
    def name(self):
        return "MLAnalyzer"
    
    @property
    def version(self):
        return "1.0.0"
    
    @property
    def description(self):
        return "Provides ML analysis and gradient visualization"
    
    def initialize(self, system):
        self.system = system
        self.gradients = []
        self.formulas = {
            'forward_pass': 'z1 = w1*x + b1, h = σ(z1)',
            'loss_gradient_z': 0.6187,
            'loss_gradient_h': 3.1449,
            'loss_gradient_h_final': -2.0666
        }
    
    def get_capabilities(self):
        return [
            'calculate_gradients',
            'detect_vanishing_gradients',
            'detect_exploding_gradients',
            'get_ml_formulas',
            'visualize_gradients'
        ]
    
    def calculate_gradients(self, layer_count: int = 10) -> list:
        """Calculate gradient flow through layers"""
        gradients = []
        for i in range(layer_count):
            # Simulate gradient flow
            if i < layer_count // 2:
                # Vanishing gradients in early layers
                gradient = np.random.exponential(0.1) * (0.9 ** i)
            else:
                # Exploding gradients in later layers
                gradient = np.random.exponential(1.0) * (1.1 ** (i - layer_count//2))
            
            gradients.append({
                'layer': i,
                'gradient': float(gradient),
                'type': 'vanishing' if gradient < 0.5 else 'exploding' if gradient > 2.0 else 'normal'
            })
        
        self.gradients = gradients
        
        # Emit event for visualization
        self.system.emit_event(
            'gradients_calculated',
            {'gradients': gradients},
            self.name
        )
        
        return gradients
    
    def detect_vanishing_gradients(self, threshold: float = 0.01) -> list:
        """Detect layers with vanishing gradients"""
        if not self.gradients:
            self.calculate_gradients()
        
        vanishing = [g for g in self.gradients if g['gradient'] < threshold]
        
        if vanishing:
            self.system.emit_event(
                'ml_issue_detected',
                {
                    'issue': 'vanishing_gradients',
                    'layers': [g['layer'] for g in vanishing],
                    'severity': 'high' if len(vanishing) > 3 else 'medium'
                },
                self.name
            )
        
        return vanishing
    
    def detect_exploding_gradients(self, threshold: float = 10.0) -> list:
        """Detect layers with exploding gradients"""
        if not self.gradients:
            self.calculate_gradients()
        
        exploding = [g for g in self.gradients if g['gradient'] > threshold]
        
        if exploding:
            self.system.emit_event(
                'ml_issue_detected',
                {
                    'issue': 'exploding_gradients',
                    'layers': [g['layer'] for g in exploding],
                    'severity': 'critical' if len(exploding) > 2 else 'high'
                },
                self.name
            )
        
        return exploding
    
    def get_ml_formulas(self) -> dict:
        """Get ML formulas and values"""
        return self.formulas
    
    def visualize_gradients(self) -> dict:
        """Get gradient visualization data"""
        if not self.gradients:
            self.calculate_gradients()
        
        return {
            'gradients': self.gradients,
            'summary': {
                'total_layers': len(self.gradients),
                'vanishing_count': len([g for g in self.gradients if g['type'] == 'vanishing']),
                'exploding_count': len([g for g in self.gradients if g['type'] == 'exploding']),
                'normal_count': len([g for g in self.gradients if g['type'] == 'normal'])
            },
            'recommendations': self._get_recommendations()
        }
    
    def _get_recommendations(self) -> list:
        """Get recommendations based on gradient analysis"""
        recommendations = []
        
        vanishing = self.detect_vanishing_gradients()
        if vanishing:
            recommendations.append({
                'issue': 'Vanishing Gradients',
                'solution': 'Use ReLU activation, Batch Normalization, or Skip Connections',
                'severity': 'high'
            })
        
        exploding = self.detect_exploding_gradients()
        if exploding:
            recommendations.append({
                'issue': 'Exploding Gradients',
                'solution': 'Use Gradient Clipping, Lower Learning Rate, or L2 Regularization',
                'severity': 'critical'
            })
        
        return recommendations
    
    def handle_event(self, event_type: str, data: dict, source: str):
        """Handle events from other plugins"""
        if event_type == 'model_trained':
            # Auto-analyze gradients after training
            self.calculate_gradients(data.get('layer_count', 10))
            self.detect_vanishing_gradients()
            self.detect_exploding_gradients()
        elif event_type == 'request_ml_analysis':
            # Respond to analysis requests
            viz_data = self.visualize_gradients()
            self.system.emit_event(
                'ml_analysis_complete',
                viz_data,
                self.name,
                source
            )