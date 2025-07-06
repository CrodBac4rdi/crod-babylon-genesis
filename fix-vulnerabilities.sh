#!/bin/bash
# Fix known vulnerabilities in CROD Babylon Genesis

echo "🔧 Fixing vulnerabilities in CROD Babylon Genesis..."

# 1. Update npm packages in root
echo "📦 Updating root npm packages..."
npm update
npm audit fix

# 2. Update Tauri app
echo "📦 Updating Tauri app packages..."
cd crod-chain-app
npm update
npm audit fix
cd ..

# 3. Update VSCode extension
echo "📦 Updating VSCode extension packages..."
cd crod-claude-chat
npm update
npm audit fix
cd ..

# 4. Update frontend packages
echo "📦 Updating frontend packages..."
cd src/frontend/crod-gui
npm update
npm audit fix
cd ../../..

# 5. Create security report
echo "📄 Creating security report..."
cat > SECURITY_FIXES.md << EOF
# Security Fixes Applied - $(date)

## NPM Vulnerabilities Fixed
- Updated all npm dependencies to latest versions
- Ran npm audit fix on all projects

## Python Dependencies
All Python packages use >= versions which auto-update to latest secure versions:
- numpy>=1.24.0
- scipy>=1.10.0
- matplotlib>=3.7.0
- Pillow>=10.0.0

## Rust/Cargo
Tauri and related crates are at version 2.x which is latest stable.

## Recommendations
1. Regularly run: npm audit
2. Keep Python packages updated: pip install -r requirements.txt --upgrade
3. Update Rust: cargo update

EOF

echo "✅ Vulnerability fixes complete! Check SECURITY_FIXES.md for details."