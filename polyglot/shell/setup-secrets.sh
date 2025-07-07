#!/bin/bash
# 🔐 CROD Secrets Setup Helper

echo "🔐 CROD GitHub Secrets Setup"
echo "=========================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

# Create .env from example
echo "📋 Creating .env from .env.example..."
cp .env.example .env

echo ""
echo "✅ Local .env created with development defaults"
echo ""
echo "🔐 WICHTIG: Folgende Secrets musst du in GitHub setzen:"
echo ""
echo "1️⃣  Geh zu: github.com/CrodBac4rdi/crod-babylon-genesis"
echo "2️⃣  Settings → Secrets and variables → Codespaces"
echo "3️⃣  Click 'New repository secret' für jeden:"
echo ""
echo "   PFLICHT:"
echo "   --------"
echo "   • ANTHROPIC_API_KEY    - Dein Claude API Key"
echo "   • DANIEL_OVERRIDE_KEY  - Dein geheimer Master Key"
echo ""
echo "   OPTIONAL:"
echo "   ---------"
echo "   • OPENAI_API_KEY      - Falls du GPT nutzt"
echo "   • CROD_MASTER_KEY     - Master encryption key"
echo "   • DOCKERHUB_TOKEN     - Für private Docker images"
echo ""
echo "📍 Direct link:"
echo "   https://github.com/CrodBac4rdi/crod-babylon-genesis/settings/secrets/codespaces"
echo ""
echo "Nach dem Setup sind die Secrets automatisch in deinem Codespace verfügbar!"
echo ""

# Check if we're in Codespaces
if [ -n "$CODESPACES" ]; then
    echo "🎮 Du bist bereits im Codespace!"
    echo ""
    echo "Checking secrets..."
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo "✅ ANTHROPIC_API_KEY is set"
    else
        echo "❌ ANTHROPIC_API_KEY is NOT set"
    fi
    
    if [ -n "$DANIEL_OVERRIDE_KEY" ]; then
        echo "✅ DANIEL_OVERRIDE_KEY is set"
    else
        echo "❌ DANIEL_OVERRIDE_KEY is NOT set"
    fi
fi

echo ""
echo "🚀 Ready to start CROD? Run: ./scripts/start-crod.sh"