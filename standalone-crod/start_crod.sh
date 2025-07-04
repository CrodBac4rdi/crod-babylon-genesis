#!/bin/bash

echo "🚀 Starting CROD Standalone..."
echo "=============================="

cd "$(dirname "$0")"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama not running! Starting it..."
    echo "   Run: ollama serve"
    echo "   Then: ollama pull llama3.2"
    echo ""
fi

# Check Python dependencies
echo "📦 Checking dependencies..."
python3 -c "import PyQt6; print('✅ PyQt6 installed')" 2>/dev/null || echo "❌ PyQt6 missing - run: pip install -r requirements.txt"
python3 -c "import numpy; print('✅ NumPy installed')" 2>/dev/null || echo "❌ NumPy missing"
python3 -c "import requests; print('✅ Requests installed')" 2>/dev/null || echo "❌ Requests missing"

echo ""
echo "🧠 Starting CROD..."
python3 main.py