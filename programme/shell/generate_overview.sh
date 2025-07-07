#!/bin/bash
# Repository Overview Generator

echo "# CROD Clean Repository Overview"
echo "Generated: $(date)"
echo
echo "## Repository Structure"
echo '```'
find . -type f -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/venv/*" | sort
echo '```'
echo
echo "## Documentation Overview"
echo '```'
find ./docs -type f -name "*.md" | sort
echo '```'
echo
echo "## Assets Overview"
echo '```'
find ./assets -type f | sort
echo '```'
echo
echo "## Scripts Overview"
echo '```'
find ./scripts -type f | sort
echo '```'
