#!/usr/bin/env python3
"""
CROD Session Stats Hook
Collects statistics when Claude Code stops and updates pattern weights
"""
import json
import sys
from pathlib import Path
from collections import Counter

def analyze_session_patterns():
    """Analyze patterns from the current session"""
    patterns_log = Path.home() / ".claude" / "crod-patterns.jsonl"
    operations_log = Path.home() / ".claude" / "crod-data" / "successful-operations.jsonl"
    
    stats = {
        "total_operations": 0,
        "tool_usage": Counter(),
        "pattern_hits": Counter(),
        "trinity_total": 0,
        "sentiment_counts": {"positive": 0, "negative": 0, "neutral": 0}
    }
    
    # Analyze pattern detections
    if patterns_log.exists():
        with open(patterns_log) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    analysis = entry.get("analysis", {})
                    stats["trinity_total"] += analysis.get("trinity_score", 0)
                    sentiment = analysis.get("sentiment", "neutral")
                    stats["sentiment_counts"][sentiment] += 1
                    
                    for pattern in analysis.get("patterns_found", []):
                        stats["pattern_hits"][pattern] += 1
                except:
                    continue
    
    # Analyze successful operations
    if operations_log.exists():
        with open(operations_log) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    tool = entry.get("tool", "unknown")
                    stats["tool_usage"][tool] += 1
                    stats["total_operations"] += 1
                except:
                    continue
    
    return stats

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    # Don't run if already in a stop hook
    if input_data.get("stop_hook_active", False):
        sys.exit(0)
    
    # Collect session statistics
    stats = analyze_session_patterns()
    
    # Generate summary
    summary = f"""
🏙️ CROD SESSION COMPLETE 🏙️
━━━━━━━━━━━━━━━━━━━━━━━━━
Trinity Score: {stats['trinity_total']}
Operations: {stats['total_operations']}
Sentiment: {stats['sentiment_counts']['positive']}👍 {stats['sentiment_counts']['negative']}👎
Top Tools: {', '.join(f"{k}({v})" for k, v in stats['tool_usage'].most_common(3))}
"""
    
    print(summary.strip())
    
    # Update pattern weights if Pattern District is available
    if stats['pattern_hits']:
        update_cmd = {
            "patterns": [{"id": p, "weight_delta": c * 10} for p, c in stats['pattern_hits'].items()]
        }
        
        # Try to send to Pattern District
        try:
            import requests
            requests.post("http://localhost:8888/patterns/update-weights", json=update_cmd, timeout=1)
        except:
            pass
    
    sys.exit(0)

if __name__ == "__main__":
    main()