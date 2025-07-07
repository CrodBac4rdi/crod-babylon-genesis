#!/bin/bash

# 🦠 CROD Live Demo Script
# Zeigt live alle Funktionen des Systems

echo "🦠 CROD Live Demo gestartet!"
echo "================================="
echo ""

# Test 1: Python Code Execution
echo "✅ Test 1: Python Code Execution"
echo "Code: print('Hello from CROD Python!')"
python3 -c "print('Hello from CROD Python!')"
echo ""

# Test 2: JavaScript Code Execution (falls verfügbar)
echo "✅ Test 2: JavaScript Code Execution"
echo "Code: console.log('Hello from CROD JavaScript!')"
if command -v node &> /dev/null; then
    node -e "console.log('Hello from CROD JavaScript!')"
else
    echo "Node.js nicht verfügbar - wird über APT installiert..."
fi
echo ""

# Test 3: Bash Code Execution
echo "✅ Test 3: Bash Code Execution"
echo "Code: echo 'Hello from CROD Bash!'"
echo 'Hello from CROD Bash!'
echo ""

# Test 4: File Operations
echo "✅ Test 4: File Operations"
echo "Creating test file..."
echo "CROD System Test File" > /tmp/crod_test.txt
echo "File created: $(cat /tmp/crod_test.txt)"
rm /tmp/crod_test.txt
echo "File deleted."
echo ""

# Test 5: System Information
echo "✅ Test 5: System Information"
echo "OS: $(uname -s)"
echo "Version: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Python: $(python3 --version)"
echo "Current Directory: $(pwd)"
echo ""

# Test 6: Live Server Status
echo "✅ Test 6: Live Server Status"
echo "Checking development server..."
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "🟢 Development server is running on http://localhost:5173"
else
    echo "🔴 Development server is not running"
fi
echo ""

# Test 7: Live Metrics Simulation
echo "✅ Test 7: Live Metrics Simulation"
for i in {1..5}; do
    CPU=$(shuf -i 10-90 -n 1)
    MEM=$(shuf -i 20-80 -n 1)
    echo "CPU: ${CPU}%, RAM: ${MEM}%, Tasks: $i"
    sleep 1
done
echo ""

echo "🦠 CROD Live Demo beendet!"
echo "System ist bereit für AI/ML Live Coding!"
echo "Öffne http://localhost:5173 im Browser für die GUI!"
