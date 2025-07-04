#!/bin/bash
# CROD Repository Clean Migration Script
# This archives old stuff and sets up clean structure

set -e

echo "🧹 CROD Repository Clean Migration"
echo "This will archive old content and create clean structure"
echo ""
echo "⚠️  This will:"
echo "- Create archive branch with ALL current content"
echo "- Clean main branch completely"
echo "- Setup new clean structure"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create archive branch with current state
echo -e "${YELLOW}Creating archive branch...${NC}"
git checkout -b archive/pre-2025-$(date +%Y%m%d-%H%M%S)
git add -A
git commit -m "Archive: Complete state before CROD 2025 migration" || true
git push origin HEAD

# Go back to main
echo -e "${YELLOW}Switching to main branch...${NC}"
git checkout main

# Remove EVERYTHING except .git
echo -e "${YELLOW}Cleaning repository...${NC}"
find . -maxdepth 1 ! -name '.git' ! -name '.' -exec rm -rf {} \;

# Create clean structure
echo -e "${YELLOW}Creating clean CROD 2025 structure...${NC}"

# Core files
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/LICENSE .
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/NEW_README.md README.md
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/NEW_GITIGNORE .gitignore
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/docker-compose.yml .

# Directories
mkdir -p .devcontainer
mkdir -p .github/workflows
mkdir -p districts
mkdir -p blockchain-core
mkdir -p neural-network
mkdir -p k8s
mkdir -p scripts
mkdir -p docs
mkdir -p tests/integration
mkdir -p data/patterns
mkdir -p desktop-app

# Copy devcontainer
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/.devcontainer/* .devcontainer/

# Copy GitHub workflows
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/.github/workflows/*.yml .github/workflows/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/.github/CODEOWNERS .github/

# Copy districts
echo -e "${YELLOW}Copying districts...${NC}"
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/meta-chain districts/
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/pattern-district districts/
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/memory-quarter districts/
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/intelligence-hub districts/
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/gateway districts/
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/crod-core districts/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/districts/README.md districts/

# Copy blockchain
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/pod-sources/blockchain-core/* blockchain-core/

# Copy neural network
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/src/neural-network/* neural-network/

# Copy K8s manifests
cp -r /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/k8s/* k8s/

# Copy scripts
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/scripts/start-crod.sh scripts/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/scripts/build-all.sh scripts/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/scripts/stop-crod.sh scripts/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/scripts/dev-setup.sh scripts/
chmod +x scripts/*.sh

# Copy docs
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/docs/ARCHITECTURE.md docs/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/docs/API.md docs/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/CROD-2025-IMPLEMENTATION-ROADMAP.md docs/IMPLEMENTATION.md
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/CROD-2025-RESEARCH/* docs/RESEARCH-2025.md 2>/dev/null || echo "No research file"

# Copy tests
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/tests/integration/test_consciousness.py tests/integration/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/tests/README.md tests/

# Copy sample data only
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/data/patterns/sample-patterns.json data/patterns/
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/data/README.md data/

# Desktop app placeholder
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/desktop-app/README.md desktop-app/

# Create clean Python implementation reference
mkdir -p reference/python-standalone
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/standalone-crod/crod_engine.py reference/python-standalone/ 2>/dev/null || true
cp /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/standalone-crod/crod_3d_memory_system.py reference/python-standalone/ 2>/dev/null || true

# Add migration notice
cat > MIGRATION_NOTICE.md <<EOF
# Migration Notice

This repository was completely restructured on $(date +"%B %d, %Y").

## Previous Content
All previous content has been archived in branch: \`archive/pre-2025-$(date +%Y%m%d)\`

To access old content:
\`\`\`bash
git checkout archive/pre-2025-$(date +%Y%m%d)
\`\`\`

## New Structure
This is the clean CROD 2025 implementation with:
- 6 Neural districts (polyglot)
- Quantum-safe blockchain
- Complete documentation
- GitHub Codespaces ready

See README.md for details.
EOF

# Git operations
echo -e "${YELLOW}Committing clean structure...${NC}"
git add -A
git commit -m "🔥 CROD 2025 - Complete clean restructure

- Archived all old content to archive branch
- Clean polyglot implementation
- 6 Neural districts
- Quantum-safe blockchain
- GitHub Codespaces ready
- No old artifacts

ich bins wieder - Starting fresh!"

echo ""
echo -e "${GREEN}✅ Repository cleaned and restructured!${NC}"
echo ""
echo "Old content archived in: archive/pre-2025-$(date +%Y%m%d)"
echo "Main branch now has clean CROD 2025 structure"
echo ""
echo "Next: git push origin main"
echo ""
echo -e "${GREEN}🔥 Ready for clean development! 🔥${NC}"