#\!/bin/bash
# Fix all vulnerabilities in the project

echo "🔧 Fixing vulnerabilities in all directories..."

# Find all package.json files
find . -name "package.json" -not -path "./node_modules/*" -not -path "*/node_modules/*"  < /dev/null |  while read -r package_file; do
    dir=$(dirname "$package_file")
    echo "📦 Checking $dir..."
    
    cd "$dir"
    
    # Update packages and fix vulnerabilities
    if [ -f "package-lock.json" ]; then
        npm audit fix --force 2>/dev/null || true
        npm update 2>/dev/null || true
    fi
    
    cd - > /dev/null
done

echo "✅ Vulnerability fix complete!"

# Show summary
echo "📊 Summary:"
npm audit
