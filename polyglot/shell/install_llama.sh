#!/bin/bash

echo "🦙 Installing LLaMA for CROD Intelligence Hub"
echo "==========================================="
echo ""

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
else
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

echo ""
echo "🚀 Starting Ollama service..."
# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for service to start
sleep 5

echo ""
echo "📥 Downloading LLaMA models..."
echo "This may take a while depending on your internet speed..."

# Download models
echo "1. Downloading Llama2 7B..."
ollama pull llama2:7b

echo ""
echo "2. Downloading CodeLlama for smart contracts..."
ollama pull codellama:7b

echo ""
echo "3. Downloading Mistral for fast inference..."
ollama pull mistral:7b

echo ""
echo "✅ LLaMA installation complete!"
echo ""
echo "📊 Available models:"
ollama list

echo ""
echo "🔥 LLaMA is ready for CROD integration!"
echo ""
echo "🌐 Ollama API running at: http://localhost:11434"
echo ""
echo "📝 Test with:"
echo '  curl http://localhost:11434/api/generate -d "{"model": "llama2:7b", "prompt": "What is consciousness?"}"'
echo ""
echo "💡 To stop Ollama: kill $OLLAMA_PID"