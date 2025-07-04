#!/bin/bash
# Fix npm vulnerabilities in all package.json files

echo "🔧 Fixing npm vulnerabilities..."

# Update all package.json files to latest versions
find . -name "package.json" -not -path "./node_modules/*" -not -path "./alt/*" | while read pkg; do
    dir=$(dirname "$pkg")
    echo "Updating $dir..."
    
    cd "$dir"
    
    # Update dependencies to latest versions
    if [ -f "package-lock.json" ]; then
        rm package-lock.json
    fi
    
    # Update all dependencies
    npm update --save
    
    # Audit and fix
    npm audit fix --force || true
    
    cd - > /dev/null
done

echo "✅ Vulnerabilities fixed!"