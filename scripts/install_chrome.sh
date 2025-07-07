#!/bin/bash

echo "🌐 Installing Google Chrome with WebGPU support"
echo "=============================================="
echo ""
echo "Please run the following commands with sudo:"
echo ""

# Download and install Chrome
echo "# 1. Add Google Chrome repository key:"
echo "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -"
echo ""

echo "# 2. Add Chrome repository:"
echo "sudo sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google-chrome.list'"
echo ""

echo "# 3. Update package list:"
echo "sudo apt update"
echo ""

echo "# 4. Install Google Chrome:"
echo "sudo apt install google-chrome-stable"
echo ""

echo "# 5. Set Chrome as default browser:"
echo "sudo update-alternatives --config x-www-browser"
echo "# Choose google-chrome from the list"
echo ""

echo "# 6. Set for xdg-open:"
echo "xdg-settings set default-web-browser google-chrome.desktop"
echo ""

echo "🚀 After installation, Chrome will have WebGPU enabled by default!"
echo ""
echo "To verify WebGPU is working:"
echo "1. Open Chrome and go to: chrome://gpu"
echo "2. Look for 'WebGPU: Hardware accelerated'"
echo ""
echo "For maximum performance, enable these flags in chrome://flags:"
echo "- #enable-webgpu-developer-features"
echo "- #enable-unsafe-webgpu"