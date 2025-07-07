#!/bin/bash
# Security Fix Script for CROD

echo "🔐 Fixing Security Vulnerabilities"
echo "=================================="

# Update all npm packages
echo "📦 Updating npm packages..."
for dir in $(find . -name "package.json" -not -path "*/node_modules/*" -exec dirname {} \;); do
    echo "Checking $dir..."
    cd "$dir"
    if [ -f "package-lock.json" ]; then
        npm audit fix --force
    fi
    cd - > /dev/null
done

# Update Python packages
echo "🐍 Updating Python packages..."
pip install --upgrade pip

# Use minimal requirements for security
if [ -f "requirements-minimal.txt" ]; then
    pip install -r requirements-minimal.txt --upgrade
fi

# Clean up old packages
echo "🧹 Cleaning up..."
pip cache purge
npm cache clean --force

echo "✅ Security fixes applied!"
echo ""
echo "Recommendations:"
echo "1. Use requirements-minimal.txt instead of the bloated requirements.txt"
echo "2. Only install packages you actually need"
echo "3. Keep dependencies updated regularly"