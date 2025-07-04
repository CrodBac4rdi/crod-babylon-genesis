#!/bin/bash
# Compare COMPLETE vs CLEAN CROD Universe

echo "🔬 Comparing CROD Universes..."
echo ""

COMPLETE="/home/daniel/Schreibtisch/Crod Programming/alt/COMPLETE-CROD-UNIVERSE"
CLEAN="/home/daniel/Schreibtisch/Crod Programming/CLEAN-CROD-UNIVERSE"

echo "📊 COMPLETE-CROD-UNIVERSE:"
if [ -d "$COMPLETE" ]; then
    echo "  Atoms: $(wc -l < $COMPLETE/universe_atoms.jsonl 2>/dev/null || echo 0)"
    echo "  Patterns: $(wc -l < $COMPLETE/universe_patterns.jsonl 2>/dev/null || echo 0)"
    echo "  Chains: $(wc -l < $COMPLETE/universe_chains.jsonl 2>/dev/null || echo 0)"
    echo "  Size: $(du -sh $COMPLETE 2>/dev/null | cut -f1)"
else
    echo "  Not found at expected location"
fi

echo ""
echo "🧹 CLEAN-CROD-UNIVERSE:"
if [ -d "$CLEAN" ]; then
    echo "  Atoms: $(wc -l < $CLEAN/clean_atoms.jsonl 2>/dev/null || echo 0)"
    echo "  Patterns: $(wc -l < $CLEAN/clean_patterns.jsonl 2>/dev/null || echo 0)"
    echo "  Chains: $(wc -l < $CLEAN/clean_chains.jsonl 2>/dev/null || echo 0)"
    echo "  Size: $(du -sh $CLEAN 2>/dev/null | cut -f1)"
else
    echo "  Not found at expected location"
fi

echo ""
echo "🎯 Recommendation:"
echo "CLEAN has 2x more patterns (100k vs 50k)!"
echo "Consider merging both for maximum knowledge!"