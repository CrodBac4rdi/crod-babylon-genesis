#!/bin/bash

echo "🚀 Starting CROD Clean System..."

# Check dependencies
echo "📦 Checking dependencies..."
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v cargo >/dev/null 2>&1 || { echo "❌ Rust/Cargo is required but not installed."; exit 1; }

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Build Rust components if needed
if [ ! -f "src/performance/rust/target/release/crod-performance-server" ]; then
    echo "🦀 Building Rust components..."
    cd src/performance/rust && cargo build --release
    cd ../../..
fi

# Start services
echo "🎯 Starting Core System..."
node src/core/crod-master-controller.js &
CORE_PID=$!

echo "🎨 Starting Visualization Server..."
cd src/visualization && python crod_web_studio.py &
VIZ_PID=$!
cd ../..

echo "🌐 Starting Web Interface..."
cd src/web && npm run dev &
WEB_PID=$!
cd ../..

echo "⚡ Starting Performance Backend..."
./src/performance/rust/target/release/crod-performance-server &
PERF_PID=$!

echo "✅ CROD Clean System Started!"
echo "   Core: http://localhost:3000"
echo "   Visualization: http://localhost:5000"
echo "   Web Interface: http://localhost:5173"
echo "   Performance API: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait and handle shutdown
trap "echo '🛑 Stopping services...'; kill $CORE_PID $VIZ_PID $WEB_PID $PERF_PID 2>/dev/null; exit" INT TERM
wait