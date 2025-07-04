#!/bin/bash
# 🔥 START UNIFIED CROD - Everything connected!

echo "🧠 UNIFIED CROD SYSTEM LAUNCHER"
echo "==============================="
echo "Combining 41 files into ONE intelligent system!"
echo ""

cd "$(dirname "$0")"

# Check Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  WARNING: Ollama not running!"
    echo "   CROD LLM features will be limited"
    echo ""
fi

# Kill old processes
echo "🔧 Cleaning up old CROD processes..."
pkill -f "crod_self_reflection.py" 2>/dev/null
pkill -f "crod_identity_booster.py" 2>/dev/null
pkill -f "crod_live_monitor.py" 2>/dev/null
pkill -f "claude_teaches_crod.py" 2>/dev/null

sleep 1

# Options
echo "🎯 LAUNCH OPTIONS:"
echo "1) Full Auto Mode (learns from everything)"
echo "2) Interactive Mode (manual chat input)"
echo "3) Background Mode (runs silently)"
echo ""
read -p "Choose mode (1-3): " mode

case $mode in
    1)
        echo "🚀 Starting FULL AUTO MODE..."
        python3 unified_crod_main.py
        ;;
    2)
        echo "💬 Starting INTERACTIVE MODE..."
        python3 crod_chat_watcher.py --interactive
        ;;
    3)
        echo "🌙 Starting BACKGROUND MODE..."
        nohup python3 unified_crod_main.py > unified_crod.log 2>&1 &
        PID=$!
        echo "✅ CROD running in background (PID: $PID)"
        echo "📝 Logs: unified_crod.log"
        echo "🛑 Stop: kill $PID"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac