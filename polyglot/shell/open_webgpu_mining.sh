#!/bin/bash

echo "🚀 Opening CROD WebGPU Mining Interface"
echo "======================================"
echo ""

# Check for Chrome/Chromium
BROWSER=""

if command -v google-chrome &> /dev/null; then
    BROWSER="google-chrome"
elif command -v google-chrome-stable &> /dev/null; then
    BROWSER="google-chrome-stable"
elif command -v chromium &> /dev/null; then
    BROWSER="chromium"
elif command -v chromium-browser &> /dev/null; then
    BROWSER="chromium-browser"
fi

if [ -z "$BROWSER" ]; then
    echo "❌ Chrome/Chromium not found!"
    echo ""
    echo "WebGPU requires Chrome or Chromium. Please install with:"
    echo "  sudo apt install google-chrome-stable"
    echo "or"
    echo "  sudo apt install chromium-browser"
    echo ""
    echo "Firefox does NOT support WebGPU yet!"
    exit 1
fi

echo "✅ Found browser: $BROWSER"
echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Open WebGPU mining interface
echo "🌐 Opening WebGPU Mining Interface..."
$BROWSER "$DIR/webgpu_mining.html" &

echo ""
echo "📝 WebGPU Tips:"
echo "  - Make sure hardware acceleration is enabled"
echo "  - Check chrome://gpu for WebGPU status"
echo "  - Enable experimental features in chrome://flags if needed"
echo ""
echo "⚡ Happy GPU Mining!"