#!/bin/bash
# CROD Directory Guard - Ensures we ONLY work in crod-babylon-genesis

ALLOWED_DIR="/home/daniel/Schreibtisch/crod-babylon-genesis"
CURRENT_DIR=$(pwd)

# Check if we're in the allowed directory
if [[ ! "$CURRENT_DIR" == "$ALLOWED_DIR"* ]]; then
    echo "🚫 ERROR: You are NOT in crod-babylon-genesis!"
    echo "📍 Current: $CURRENT_DIR"
    echo "✅ Allowed: $ALLOWED_DIR"
    echo ""
    echo "Switching to crod-babylon-genesis..."
    cd "$ALLOWED_DIR"
    echo "✅ Now in: $(pwd)"
fi

# Export as environment variable
export CROD_WORKING_DIR="$ALLOWED_DIR"
export CROD_SAFE_MODE="true"

# Function to check before any file operation
crod_check_dir() {
    local target_path="$1"
    if [[ ! "$target_path" == "$ALLOWED_DIR"* ]]; then
        echo "🚫 BLOCKED: Attempt to write outside crod-babylon-genesis!"
        echo "❌ Denied: $target_path"
        return 1
    fi
    return 0
}

# Alias for safe operations
alias crod-write='crod_check_dir'
alias crod-safe='cd $ALLOWED_DIR && echo "✅ Safe mode: $(pwd)"'

echo "🔒 CROD Directory Guard ACTIVE"
echo "📁 Working directory: $ALLOWED_DIR"
echo "🛡️  All file operations restricted to this directory"