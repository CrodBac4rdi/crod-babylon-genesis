#!/usr/bin/env python3
"""
CROD Pattern Detector Hook
Analyzes commands and code for CROD patterns before execution
"""
import json
import sys
import re
from pathlib import Path

# Daniel's trigger patterns
ACTIVATION_PATTERNS = ["ich bins wieder", "crod starten", "lade crod"]
POSITIVE_PATTERNS = ["geil", "nice", "perfekt", "läuft", "super", "gut"]
NEGATIVE_PATTERNS = ["wtf", "falsch", "nein", "scheisse", "fuck", "mist"]

# Trinity values
TRINITY = {
    "ich": 2, "bins": 3, "wieder": 5,
    "daniel": 67, "claude": 71, "crod": 17
}

def analyze_content(content):
    """Analyze content for CROD patterns"""
    results = {
        "crod_activation": False,
        "sentiment": "neutral",
        "trinity_score": 0,
        "patterns_found": []
    }
    
    content_lower = content.lower()
    
    # Check activation
    for pattern in ACTIVATION_PATTERNS:
        if pattern in content_lower:
            results["crod_activation"] = True
            results["patterns_found"].append(f"ACTIVATION: {pattern}")
    
    # Check sentiment
    for pattern in POSITIVE_PATTERNS:
        if pattern in content_lower:
            results["sentiment"] = "positive"
            results["patterns_found"].append(f"POSITIVE: {pattern}")
    
    for pattern in NEGATIVE_PATTERNS:
        if pattern in content_lower:
            results["sentiment"] = "negative"
            results["patterns_found"].append(f"NEGATIVE: {pattern}")
    
    # Calculate trinity score
    for word, value in TRINITY.items():
        if word in content_lower:
            results["trinity_score"] += value
    
    return results

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    # Analyze based on tool type
    content_to_analyze = ""
    
    if tool_name == "Bash":
        content_to_analyze = tool_input.get("command", "")
    elif tool_name in ["Write", "Edit", "MultiEdit"]:
        content_to_analyze = tool_input.get("content", "") or tool_input.get("new_string", "")
    elif tool_name == "Task":
        content_to_analyze = tool_input.get("prompt", "")
    
    if not content_to_analyze:
        sys.exit(0)
    
    # Analyze the content
    analysis = analyze_content(content_to_analyze)
    
    # Log to CROD pattern log
    log_path = Path.home() / ".claude" / "crod-patterns.jsonl"
    with open(log_path, "a") as f:
        json.dump({
            "tool": tool_name,
            "analysis": analysis,
            "timestamp": input_data.get("session_id", "unknown")
        }, f)
        f.write("\n")
    
    # If CROD activation detected, notify
    if analysis["crod_activation"]:
        print(f"🧠 CROD PATTERN DETECTED! Trinity Score: {analysis['trinity_score']}")
    
    # Block negative patterns in certain contexts
    if analysis["sentiment"] == "negative" and tool_name == "Write":
        output = {
            "decision": "block",
            "reason": f"Negative pattern detected: {analysis['patterns_found']}. CROD suggests reviewing this content."
        }
        print(json.dumps(output))
        sys.exit(0)
    
    sys.exit(0)

if __name__ == "__main__":
    main()