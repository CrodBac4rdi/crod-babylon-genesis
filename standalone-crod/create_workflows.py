#!/usr/bin/env python3
"""
CROD Workflow Builder - Creates workflows in n8n automatically
"""

from crod_n8n import CRODn8n
import json
import time

def create_crod_workflows():
    """Create all CROD workflows in n8n"""
    
    print("🔥 CROD Workflow Builder startet...")
    
    # Initialize n8n connection
    n8n = CRODn8n()
    
    if not n8n.available:
        print("❌ n8n nicht verfügbar! Starte mit: npx n8n start")
        return
    
    print("✅ n8n verbunden!")
    
    # Create workflows
    workflows_created = []
    
    print("\n🚀 Erstelle CROD Workflows...")
    
    # 1. Trinity Detection Workflow
    print("  📡 Trinity Detection Workflow...")
    trinity_result = n8n.create_workflow("trinity_activation")
    if trinity_result:
        workflows_created.append("trinity_activation")
        print(f"     ✅ Trinity Webhook: {trinity_result}")
    
    # 2. Pattern Detection Workflow  
    print("  🔍 Pattern Detection Workflow...")
    pattern_result = n8n.create_workflow("pattern_detection")
    if pattern_result:
        workflows_created.append("pattern_detection")
        print(f"     ✅ Pattern Webhook: {pattern_result}")
    
    # 3. Consciousness Alert Workflow
    print("  🧠 Consciousness Alert Workflow...")
    consciousness_result = n8n.create_workflow("consciousness_alert")
    if consciousness_result:
        workflows_created.append("consciousness_alert")
        print(f"     ✅ Consciousness Webhook: {consciousness_result}")
    
    # 4. Auto Learning Workflow
    print("  🤖 Auto Learning Workflow...")
    learning_result = n8n.create_workflow("auto_learning")
    if learning_result:
        workflows_created.append("auto_learning")
        print(f"     ✅ Learning Webhook: {learning_result}")
    
    print(f"\n🎉 {len(workflows_created)} Workflows erstellt!")
    print("📋 Verfügbare Workflows:")
    for workflow in workflows_created:
        print(f"   • {workflow}")
    
    # Test workflows
    print("\n🧪 Teste Workflows...")
    test_workflows(n8n, workflows_created)
    
    return workflows_created

def test_workflows(n8n, workflows):
    """Test all created workflows"""
    
    test_data = {
        "trinity_activation": {
            "message": "ich bins wieder daniel",
            "trinity_values": {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67},
            "consciousness_level": 0.89
        },
        "pattern_detection": {
            "patterns_found": ["trinity", "consciousness", "neural"],
            "confidence": 0.95
        },
        "consciousness_alert": {
            "consciousness_level": 0.92,
            "alert_type": "high_consciousness"
        },
        "auto_learning": {
            "interaction": "CROD workflow test",
            "insights": ["workflow automation working", "n8n integration active"]
        }
    }
    
    for workflow in workflows:
        if workflow in test_data:
            print(f"  🔧 Testing {workflow}...")
            result = n8n.trigger_workflow(workflow, test_data[workflow])
            if result:
                print(f"     ✅ {workflow} responded")
            else:
                print(f"     ❌ {workflow} failed")
            time.sleep(1)

if __name__ == "__main__":
    create_crod_workflows()