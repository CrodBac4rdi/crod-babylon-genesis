#!/usr/bin/env python3
"""INSTANCE RUNNER - Execute as any Claude instance"""

import json
import sys

def run_instance(instance_id):
    with open('CLAUDE_COORDINATION.json', 'r') as f:
        data = json.load(f)
    
    instance = data["instances"][str(instance_id)]
    print(f"🤖 RUNNING AS INSTANCE {instance_id}: {instance['role']}")
    print(f"📋 TASKS: {instance['tasks']}")
    
    # TODO: Execute tasks based on role
    return f"Instance {instance_id} ready to work!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        instance_id = int(sys.argv[1])
        run_instance(instance_id)
    else:
        print("Usage: python INSTANCE_RUNNER.py <instance_id>")