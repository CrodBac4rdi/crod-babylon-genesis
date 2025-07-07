#!/bin/bash

# CROD POLYGLOT CITY 2025 - Startup Script

echo "🔥 Starting CROD POLYGLOT CITY 2025 🔥"
echo "================================="
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running! Please start Docker first."
    exit 1
fi

# Start NATS first
echo "📡 Starting NATS Message Bus..."
docker run -d --rm --name crod-nats -p 4222:4222 -p 8222:8222 nats:latest -m 8222
sleep 2

# Function to start a district
start_district() {
    local name=$1
    local port=$2
    local dir=$3
    local cmd=$4
    
    echo ""
    echo "🏙️  Starting $name on port $port..."
    cd "$dir" || exit 1
    
    # Kill any existing process on the port
    lsof -ti:$port | xargs -r kill -9 2>/dev/null
    
    # Start the service
    eval "$cmd" &
    
    cd - > /dev/null
}

# Start all districts
start_district "Phoenix Rathaus" 4000 "crod-rathaus-phoenix" "mix phx.server"
start_district "Python Parasit" 6666 "crod-parasit-python" "python3 parasit.py"
start_district "Rust Pattern" 7007 "crod-pattern-rust" "cargo run --release"
start_district "Go Memory" 7031 "crod-memory-go" "go run main.go"
start_district "JS Gateway" 7888 "crod-gateway-js" "npm start"

echo ""
echo "🌆 CROD POLYGLOT CITY 2025 is starting up!"
echo ""
echo "Access points:"
echo "  🏛️  Phoenix Rathaus: http://localhost:4000/dashboard"
echo "  🦖 Python Parasit: http://localhost:6666/status"
echo "  🦀 Rust Pattern: http://localhost:7007/"
echo "  🧠 Go Memory: http://localhost:7031/health"
echo "  🎪 JS Gateway: http://localhost:7888/"
echo "  📡 NATS Monitor: http://localhost:8222/"
echo ""
echo "Press Ctrl+C to shutdown the city"
echo ""

# Wait for interrupt
trap 'echo "\n🚪 Shutting down CROD City..."; docker stop crod-nats; kill $(jobs -p); exit' INT

# Keep script running
while true; do
    sleep 1
done