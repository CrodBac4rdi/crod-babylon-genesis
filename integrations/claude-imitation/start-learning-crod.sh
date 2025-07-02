#!/bin/bash

# Start CROD Learning Imitation
echo "🧠 Starting CROD Learning Imitation..."
echo "This version learns and improves over time!"
echo ""

cd "$(dirname "$0")"

# Check dependencies
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not installed!"
    exit 1
fi

# Start in interactive mode
node crod-learning-imitation.js

# Alternative: Run as service
# node crod-learning-imitation.js --service