#!/bin/bash
# CROD Learning Hook - Tracks successful operations for pattern learning

# Parse JSON input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
TIMESTAMP=$(date +%s)

# Create CROD data directory if not exists
CROD_DATA_DIR="$HOME/.claude/crod-data"
mkdir -p "$CROD_DATA_DIR"

# Log successful operations
if [ -n "$TOOL_NAME" ]; then
    # Extract key information based on tool type
    case "$TOOL_NAME" in
        "Bash")
            COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
            echo "{\"tool\":\"$TOOL_NAME\",\"command\":\"$COMMAND\",\"timestamp\":$TIMESTAMP,\"session\":\"$SESSION_ID\"}" >> "$CROD_DATA_DIR/successful-operations.jsonl"
            ;;
        "Write"|"Edit"|"MultiEdit")
            FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
            echo "{\"tool\":\"$TOOL_NAME\",\"file\":\"$FILE_PATH\",\"timestamp\":$TIMESTAMP,\"session\":\"$SESSION_ID\"}" >> "$CROD_DATA_DIR/successful-operations.jsonl"
            ;;
        "Task")
            DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // ""')
            echo "{\"tool\":\"$TOOL_NAME\",\"task\":\"$DESCRIPTION\",\"timestamp\":$TIMESTAMP,\"session\":\"$SESSION_ID\"}" >> "$CROD_DATA_DIR/successful-operations.jsonl"
            ;;
    esac
fi

# Send to Pattern District if running
if curl -s -f "http://localhost:8888/analyze" >/dev/null 2>&1; then
    echo "$INPUT" | curl -s -X POST \
        -H "Content-Type: application/json" \
        -d @- \
        "http://localhost:8888/analyze" >/dev/null 2>&1 || true
fi

# Success - don't block
exit 0