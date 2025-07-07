#!/bin/bash
# CROD Duplicate Cleanup Script
# WARNING: Review before running!

echo "🧹 CROD Duplicate Cleanup Script"
echo "================================"
echo "This will remove duplicate files. Review carefully!"
echo ""

# Function to safely remove duplicates
remove_duplicate() {
    local file=$1
    if [ -f "$file" ]; then
        echo "Removing: $file"
        rm -f "$file"
    fi
}

# JavaScript duplicates - keep versions in /src, remove from /crod-clean
remove_duplicate "crod-clean/src/core/crod-enhanced.js"
remove_duplicate "crod-clean/src/core/crod-ultimate-engine.js"
remove_duplicate "crod-clean/src/core/crod-claude-pingpong.js"
remove_duplicate "crod-clean/src/core/crod-intercept-system.js"
remove_duplicate "crod-clean/src/core/crod-polyglot-trainer.js"

# Python duplicates - keep main versions
remove_duplicate "crod-clean/src/ai/crod-swarm-intelligence.py"
remove_duplicate "crod-clean/src/core/distributed-systems/crod-p2p-discovery.py"
remove_duplicate "crod-main/scripts/visualization/crod_visualizer.py"
remove_duplicate "crod-clean/scripts/visualization/crod_visualizer.py"

# Keep parasite in projects, remove from crod-clean
remove_duplicate "crod-clean/src/ai/crod_parasite.py"
remove_duplicate "crod-clean/backend/python/crod_parasite.py"

# Keep web studio in bilder (original), remove duplicates
remove_duplicate "crod-clean/src/visualization/crod_web_studio.py"
remove_duplicate "crod-clean/backend/python/crod_web_studio.py"

# Elixir duplicates - keep in src/integrations
remove_duplicate "src/core/neural/crod-neural-bridge-elixir.ex"
remove_duplicate "crod-clean/src/core/neural/crod-neural-bridge-elixir.ex"

echo ""
echo "✅ Cleanup complete!"
echo "Removed duplicate files to consolidate CROD into one unified system."