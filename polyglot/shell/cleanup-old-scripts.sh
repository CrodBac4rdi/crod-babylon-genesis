#!/bin/bash

echo "🧹 Cleaning up old startup scripts..."

# Create archive directory
mkdir -p archived-scripts

# Move old/duplicate startup scripts
OLD_SCRIPTS=(
    "START-CROD-NOW.sh"
    "START-CROD-POLYGLOT.sh"
    "start-blockchain.sh"
    "test-blockchain.sh"
    "run.sh"
    "crod-integration/claude/crod-launch.sh"
)

for script in "${OLD_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "Archiving: $script"
        mv "$script" archived-scripts/ 2>/dev/null || true
    fi
done

# Move overly ambitious documentation
mkdir -p archived-docs

DOCS_TO_ARCHIVE=(
    "docs/COMPLETE-SYSTEM-OVERVIEW.md"
    "docs/QUICK-START.md"
    "docs/100K-TPS-BREAKTHROUGH.md"
    "docs/QUANTUM-CONSCIOUSNESS.md"
    "docs/TIME-TRAVEL-BLOCKCHAIN.md"
)

for doc in "${DOCS_TO_ARCHIVE[@]}"; do
    if [ -f "$doc" ]; then
        echo "Archiving doc: $doc"
        mv "$doc" archived-docs/ 2>/dev/null || true
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Old scripts moved to: archived-scripts/"
echo "📄 Old docs moved to: archived-docs/"
echo ""
echo "🎯 NOW YOU HAVE ONE ENTRY POINT:"
echo "   ./start-simple.sh"
echo ""
echo "📖 Check out the new visual guide:"
echo "   docs/VISUAL-GUIDE.md"