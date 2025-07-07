#!/usr/bin/env python3
"""
CROD System Inventory Visualizer
Creates visual representations of the actual system state
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np
from datetime import datetime
import json

# Set dark theme
plt.style.use('dark_background')

def create_system_status_chart():
    """Create a comprehensive system status visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.patch.set_facecolor('#0a0a0a')
    
    # 1. Component Status Overview
    components = ['Blockchain\n(Real)', 'Blockchain\n(Mock)', 'AI/LLM', 'Frontend', 
                  'Docker', 'Database', 'Message\nBroker', 'Quantum', 'Neural Net']
    statuses = ['Not Running', 'Running', 'Not Present', 'Not Built', 
                'Not Running', 'Not Present', 'Not Running', 'Conceptual', 'Mock Only']
    colors = ['#ff4444', '#44ff44', '#666666', '#ffaa44', 
              '#ff4444', '#666666', '#ff4444', '#333333', '#ffaa44']
    
    y_pos = np.arange(len(components))
    ax1.barh(y_pos, [1]*len(components), color=colors, alpha=0.8)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(components)
    ax1.set_xlabel('Status')
    ax1.set_title('Component Status Overview', fontsize=16, pad=20)
    ax1.set_xlim(0, 1.2)
    
    # Add status labels
    for i, (comp, status) in enumerate(zip(components, statuses)):
        ax1.text(0.5, i, status, ha='center', va='center', fontweight='bold', fontsize=10)
    
    # 2. Running Services Pie Chart
    ax2.clear()
    running_data = [2, 7]  # Running vs Not Running
    labels = ['Running', 'Not Running/Not Built']
    colors_pie = ['#44ff44', '#ff4444']
    explode = (0.1, 0)
    
    pie = ax2.pie(running_data, labels=labels, colors=colors_pie, autopct='%1.0f%%',
                  startangle=90, explode=explode, shadow=True)
    ax2.set_title('Services Status Distribution', fontsize=16, pad=20)
    
    # 3. Implementation Reality Chart
    categories = ['Documented', 'Code Exists', 'Built', 'Running', 'Functional']
    elixir_blockchain = [100, 80, 0, 0, 0]
    frontend = [100, 90, 0, 0, 0]
    ai_components = [100, 20, 0, 0, 0]
    docker_setup = [100, 100, 10, 0, 0]
    
    x = np.arange(len(categories))
    width = 0.2
    
    ax3.bar(x - 1.5*width, elixir_blockchain, width, label='Blockchain', color='#ff6b6b')
    ax3.bar(x - 0.5*width, frontend, width, label='Frontend', color='#4ecdc4')
    ax3.bar(x + 0.5*width, ai_components, width, label='AI/ML', color='#45b7d1')
    ax3.bar(x + 1.5*width, docker_setup, width, label='Docker', color='#f7dc6f')
    
    ax3.set_ylabel('Completion %')
    ax3.set_xlabel('Development Stage')
    ax3.set_title('Implementation Reality Check', fontsize=16, pad=20)
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories, rotation=15)
    ax3.legend()
    ax3.set_ylim(0, 120)
    ax3.grid(True, alpha=0.3)
    
    # 4. System Architecture Reality
    ax4.clear()
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.axis('off')
    ax4.set_title('Actual System Architecture', fontsize=16, pad=20)
    
    # Draw actual running components
    # Mock Blockchain Server
    mock_blockchain = FancyBboxPatch((1, 7), 3, 1.5, 
                                     boxstyle="round,pad=0.1",
                                     facecolor='#44ff44', 
                                     edgecolor='white',
                                     alpha=0.8)
    ax4.add_patch(mock_blockchain)
    ax4.text(2.5, 7.75, 'Mock Blockchain\n(Port 3001)', ha='center', va='center', fontweight='bold')
    
    # Web Studio
    web_studio = FancyBboxPatch((5, 7), 3, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor='#44ff44',
                                edgecolor='white',
                                alpha=0.8)
    ax4.add_patch(web_studio)
    ax4.text(6.5, 7.75, 'Web Studio\n(Port 5000)', ha='center', va='center', fontweight='bold')
    
    # Draw non-functional components (grayed out)
    # Elixir Blockchain
    elixir_block = FancyBboxPatch((1, 4.5), 3, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#333333',
                                  edgecolor='#666666',
                                  alpha=0.5,
                                  linestyle='--')
    ax4.add_patch(elixir_block)
    ax4.text(2.5, 5.25, 'Elixir Blockchain\n(Not Running)', ha='center', va='center', 
             fontweight='bold', alpha=0.5)
    
    # Database
    database = FancyBboxPatch((5, 4.5), 3, 1.5,
                              boxstyle="round,pad=0.1",
                              facecolor='#333333',
                              edgecolor='#666666',
                              alpha=0.5,
                              linestyle='--')
    ax4.add_patch(database)
    ax4.text(6.5, 5.25, 'Database\n(Not Present)', ha='center', va='center', 
             fontweight='bold', alpha=0.5)
    
    # AI/LLM
    ai_component = FancyBboxPatch((1, 2), 3, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#333333',
                                  edgecolor='#666666',
                                  alpha=0.5,
                                  linestyle='--')
    ax4.add_patch(ai_component)
    ax4.text(2.5, 2.75, 'AI/LLM Integration\n(Not Implemented)', ha='center', va='center', 
             fontweight='bold', alpha=0.5)
    
    # Frontend
    frontend_comp = FancyBboxPatch((5, 2), 3, 1.5,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#333333',
                                   edgecolor='#666666',
                                   alpha=0.5,
                                   linestyle='--')
    ax4.add_patch(frontend_comp)
    ax4.text(6.5, 2.75, 'React Frontend\n(Not Built)', ha='center', va='center', 
             fontweight='bold', alpha=0.5)
    
    # Add legend
    legend_elements = [
        patches.Patch(color='#44ff44', label='Running'),
        patches.Patch(color='#333333', label='Not Running/Not Present')
    ]
    ax4.legend(handles=legend_elements, loc='lower center', ncol=2)
    
    plt.suptitle('CROD Babylon Genesis - System Inventory Analysis', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fig.text(0.5, 0.02, f'Generated: {timestamp}', ha='center', fontsize=10, alpha=0.7)
    
    plt.tight_layout()
    filename = f'system_inventory_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"System inventory visualization saved as: {filename}")
    return filename

def create_detailed_status_matrix():
    """Create a detailed status matrix of all components"""
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Component categories and their items
    components = {
        'Core Infrastructure': [
            ('Elixir Blockchain', 'code', 'not_running', 'Complex implementation exists'),
            ('Mock Blockchain Server', 'running', 'running', 'Simple mock on port 3001'),
            ('NATS Message Broker', 'docker_image', 'not_running', 'Image present, not started'),
            ('Database System', 'not_present', 'not_present', 'No DB installed'),
            ('Docker Setup', 'config', 'not_running', 'Dockerfiles exist')
        ],
        'AI/ML Components': [
            ('Neural Network', 'mock', 'not_running', 'Visualization only'),
            ('Llama Integration', 'docs', 'not_present', 'Documented, not implemented'),
            ('Pattern Recognition', 'code', 'not_running', 'Code stubs only'),
            ('Claude Integration', 'docs', 'not_present', 'Planned feature'),
            ('ML Models', 'not_present', 'not_present', 'No model files found')
        ],
        'Frontend/UI': [
            ('React GUI', 'code', 'not_built', 'Source exists, not compiled'),
            ('Web Studio', 'running', 'running', 'Image generator on port 5000'),
            ('Visualization Tools', 'code', 'functional', 'Can generate charts'),
            ('Blockchain Explorer', 'code', 'not_built', 'Component exists'),
            ('Control Panel', 'code', 'not_built', 'JSX components present')
        ],
        'Advanced Features': [
            ('Quantum Computing', 'docs', 'conceptual', 'Theory only'),
            ('Self-Modification', 'docs', 'conceptual', 'Concept documented'),
            ('Swarm Intelligence', 'docs', 'conceptual', 'Architecture planned'),
            ('Time Travel', 'docs', 'conceptual', 'Mentioned in Docker'),
            ('Consciousness Mining', 'code', 'not_running', 'Elixir module exists')
        ]
    }
    
    # Status colors
    status_colors = {
        'running': '#00ff00',
        'functional': '#88ff88',
        'code': '#ffaa00',
        'not_built': '#ff8800',
        'not_running': '#ff4444',
        'not_present': '#666666',
        'docker_image': '#4488ff',
        'config': '#ffff00',
        'docs': '#ff00ff',
        'mock': '#00ffff',
        'conceptual': '#333333'
    }
    
    # Create the matrix
    y_offset = 0
    row_height = 0.8
    col_widths = [4, 2, 2, 6]
    
    # Headers
    headers = ['Component', 'Exists As', 'Status', 'Notes']
    header_y = 11
    ax.text(0, header_y, headers[0], fontweight='bold', fontsize=12)
    ax.text(col_widths[0], header_y, headers[1], fontweight='bold', fontsize=12)
    ax.text(col_widths[0] + col_widths[1], header_y, headers[2], fontweight='bold', fontsize=12)
    ax.text(col_widths[0] + col_widths[1] + col_widths[2], header_y, headers[3], fontweight='bold', fontsize=12)
    
    y_offset = header_y - 1
    
    for category, items in components.items():
        # Category header
        category_rect = Rectangle((0, y_offset - row_height), 14, row_height,
                                 facecolor='#222222', edgecolor='white')
        ax.add_patch(category_rect)
        ax.text(7, y_offset - row_height/2, category, ha='center', va='center',
                fontweight='bold', fontsize=14)
        y_offset -= row_height * 1.2
        
        # Items
        for name, exists_as, status, notes in items:
            # Component name
            ax.text(0.1, y_offset - row_height/2, name, va='center', fontsize=10)
            
            # Exists as
            exists_rect = Rectangle((col_widths[0], y_offset - row_height*0.8), 
                                   col_widths[1]*0.8, row_height*0.6,
                                   facecolor=status_colors.get(exists_as, '#ffffff'),
                                   edgecolor='white', alpha=0.8)
            ax.add_patch(exists_rect)
            ax.text(col_widths[0] + col_widths[1]/2, y_offset - row_height/2, 
                   exists_as.replace('_', ' ').title(), ha='center', va='center', 
                   fontsize=8, fontweight='bold')
            
            # Status
            status_rect = Rectangle((col_widths[0] + col_widths[1], y_offset - row_height*0.8), 
                                   col_widths[2]*0.8, row_height*0.6,
                                   facecolor=status_colors.get(status, '#ffffff'),
                                   edgecolor='white', alpha=0.8)
            ax.add_patch(status_rect)
            ax.text(col_widths[0] + col_widths[1] + col_widths[2]/2, y_offset - row_height/2, 
                   status.replace('_', ' ').title(), ha='center', va='center', 
                   fontsize=8, fontweight='bold')
            
            # Notes
            ax.text(col_widths[0] + col_widths[1] + col_widths[2] + 0.1, 
                   y_offset - row_height/2, notes, va='center', fontsize=9, alpha=0.8)
            
            y_offset -= row_height
    
    # Add legend
    legend_y = y_offset - 1
    ax.text(0, legend_y, 'Legend:', fontweight='bold', fontsize=12)
    legend_x = 2
    for status, color in status_colors.items():
        legend_rect = Rectangle((legend_x, legend_y - 0.5), 0.4, 0.4,
                               facecolor=color, edgecolor='white')
        ax.add_patch(legend_rect)
        ax.text(legend_x + 0.5, legend_y - 0.3, status.replace('_', ' ').title(), 
               fontsize=8, va='center')
        legend_x += 2.5
        if legend_x > 12:
            legend_x = 2
            legend_y -= 0.6
    
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(legend_y - 2, header_y + 1)
    ax.axis('off')
    
    ax.set_title('CROD System Component Status Matrix', fontsize=18, fontweight='bold', pad=20)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fig.text(0.5, 0.02, f'Generated: {timestamp} | Red=Not Running, Green=Running, Gray=Not Present', 
             ha='center', fontsize=10, alpha=0.7)
    
    plt.tight_layout()
    filename = f'system_status_matrix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"System status matrix saved as: {filename}")
    return filename

def create_reality_vs_vision_chart():
    """Create a chart showing the gap between vision and reality"""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#0a0a0a')
    
    features = [
        'Blockchain Implementation',
        'AI/LLM Integration', 
        'Neural Network',
        'Quantum Computing',
        'Self-Modification',
        'Pattern Recognition',
        'Swarm Intelligence',
        'Database Persistence',
        'Container Orchestration',
        'Frontend Application',
        'Message Broker',
        'Consciousness Mining'
    ]
    
    # Vision vs Reality scores (0-100)
    vision_scores = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    reality_scores = [15, 0, 10, 0, 0, 5, 0, 0, 10, 20, 10, 5]
    
    x = np.arange(len(features))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, vision_scores, width, label='Vision/Documentation', 
                    color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, reality_scores, width, label='Actual Implementation', 
                    color='#e74c3c', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}%', ha='center', va='bottom', fontsize=8)
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}%', ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Features', fontsize=12)
    ax.set_ylabel('Implementation Level (%)', fontsize=12)
    ax.set_title('CROD: Vision vs Reality Gap Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(features, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 120)
    
    # Add gap indicator
    total_vision = sum(vision_scores)
    total_reality = sum(reality_scores)
    gap_percentage = ((total_vision - total_reality) / total_vision) * 100
    
    ax.text(0.02, 0.95, f'Implementation Gap: {gap_percentage:.1f}%', 
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.5))
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fig.text(0.5, 0.01, f'Generated: {timestamp}', ha='center', fontsize=10, alpha=0.7)
    
    plt.tight_layout()
    filename = f'vision_vs_reality_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"Vision vs Reality chart saved as: {filename}")
    return filename

if __name__ == "__main__":
    print("CROD System Inventory Visualizer")
    print("================================")
    print("Generating comprehensive system analysis...")
    
    # Generate all visualizations
    chart1 = create_system_status_chart()
    print(f"✓ Created: {chart1}")
    
    chart2 = create_detailed_status_matrix()
    print(f"✓ Created: {chart2}")
    
    chart3 = create_reality_vs_vision_chart()
    print(f"✓ Created: {chart3}")
    
    print("\nAll visualizations completed!")
    print("Check the generated PNG files for detailed system inventory analysis.")