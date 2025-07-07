#!/bin/bash
# RADICAL CROD CLEANUP - THIS WILL CLEAN EVERYTHING!
# WARNING: Review before running!

echo "🔥 RADICAL CROD CLEANUP SCRIPT 🔥"
echo "=================================="
echo "This will massively restructure the repo!"
echo ""

# Create proper structure
echo "📁 Creating clean folder structure..."
mkdir -p crod/{src,docs,scripts,config,assets}
mkdir -p crod/src/{core,ai,web,api}

# Move test/demo files to proper location or delete
echo "🧹 Removing test/demo files from root..."
mkdir -p archive/old-files
mv TEST_BACKEND.py archive/old-files/ 2>/dev/null
mv TERMINAL_TEST.sh archive/old-files/ 2>/dev/null
mv LIVE_DEMO.sh archive/old-files/ 2>/dev/null
mv test-crod-ultimate.js archive/old-files/ 2>/dev/null
mv simple-crod-demo.html archive/old-files/ 2>/dev/null
mv start-demo-now.js archive/old-files/ 2>/dev/null
mv instant-parasite.py archive/old-files/ 2>/dev/null

# Remove duplicate READMEs
echo "📝 Consolidating documentation..."
mv README_NEW.md archive/old-files/ 2>/dev/null
mv README_ULTIMATE.md archive/old-files/ 2>/dev/null

# Clean up root scripts
echo "🔧 Moving scripts..."
mkdir -p crod/scripts/setup
mv *.sh crod/scripts/ 2>/dev/null
mv install_*.sh crod/scripts/setup/ 2>/dev/null
mv setup*.sh crod/scripts/setup/ 2>/dev/null
mv ULTIMATE_*.sh crod/scripts/setup/ 2>/dev/null

# Remove node_modules everywhere
echo "🗑️ Removing node_modules..."
find . -name "node_modules" -type d -prune -exec rm -rf {} + 2>/dev/null

# Remove build artifacts
echo "🏗️ Removing build artifacts..."
find . -name "*.vsix" -delete 2>/dev/null
find . -name "target" -type d -prune -exec rm -rf {} + 2>/dev/null
find . -name "dist" -type d -prune -exec rm -rf {} + 2>/dev/null
find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null

# Remove empty directories
echo "📂 Removing empty directories..."
find . -type d -empty -delete 2>/dev/null

# Create proper .gitignore
echo "📋 Creating comprehensive .gitignore..."
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
venv/
.venv/
env/

# Build outputs
dist/
build/
target/
*.vsix
*.pyc
*.pyo
__pycache__/

# Logs
logs/
*.log

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Temporary
tmp/
temp/
*.tmp

# Generated
*.jsonl
parasite_live_status.json
crod_parasite_live_*
EOF

echo ""
echo "✅ CLEANUP COMPLETE!"
echo ""
echo "Next steps:"
echo "1. Review changes with 'git status'"
echo "2. Move remaining code to crod/ directory"
echo "3. Update imports and paths"
echo "4. Commit the clean structure"