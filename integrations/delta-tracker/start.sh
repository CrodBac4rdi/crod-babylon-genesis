#!/bin/bash
# CROD Delta Tracker - Start Script

echo "🚀 CROD Delta Tracker Startup"
echo "=============================="

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust not found! Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi

# Check if database exists
if [ ! -f "crod.db" ]; then
    echo "📊 Creating database..."
    sqlite3 crod.db < schema_simple.sql
    echo "✅ Database created"
fi

# Build if needed
if [ ! -f "target/release/crod-delta-tracker" ]; then
    echo "🔨 Building CROD Delta Tracker..."
    cargo build --release
fi

# Start the service
echo "🌐 Starting on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
echo "Try these commands:"
echo "  curl http://localhost:8000/health"
echo "  curl http://localhost:8000/atom/11111"
echo ""

# Run with automatic restart
while true; do
    ./target/release/crod-delta-tracker "$@"
    echo "⚠️  Service stopped. Restarting in 2 seconds..."
    sleep 2
done