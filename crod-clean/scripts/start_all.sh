#!/bin/bash

echo "
╔═══════════════════════════════════════════════╗
║        🚀 CROD Clean - Starting All Services   ║
╚═══════════════════════════════════════════════╝
"

# Start Python Visualization Studio
echo "🎨 Starting Visualization Studio..."
cd backend/python && python crod_web_studio.py &
PYTHON_PID=$!

# Start Node.js Core System
echo "🧠 Starting Core System..."
cd ../../src/core && node crod-live-system.js &
NODE_PID=$!

# Start Elixir Backend (if available)
if command -v mix &> /dev/null; then
    echo "🔮 Starting Elixir Backend..."
    cd ../../backend/elixir && mix phx.server &
    ELIXIR_PID=$!
fi

# Start Rust Performance Engine (if available)
if command -v cargo &> /dev/null; then
    echo "🦀 Starting Rust Engine..."
    cd ../../backend/rust && cargo run --release &
    RUST_PID=$!
fi

echo "
✅ All services started!

Services running:
- Visualization Studio: http://localhost:5000
- Core API: http://localhost:3456
- WebSocket: ws://localhost:8765
- Elixir Phoenix: http://localhost:4000 (if available)

Press Ctrl+C to stop all services
"

# Wait for interrupt
trap "kill $PYTHON_PID $NODE_PID $ELIXIR_PID $RUST_PID 2>/dev/null; exit" INT
wait