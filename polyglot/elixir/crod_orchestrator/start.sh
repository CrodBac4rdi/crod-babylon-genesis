#!/bin/bash

# CROD Orchestrator Startup Script

echo "🏗️  Starting CROD Orchestrator..."
echo "================================"

# Check if Elixir is installed
if ! command -v elixir &> /dev/null; then
    echo "❌ Elixir is not installed!"
    echo "Please install Elixir first: https://elixir-lang.org/install.html"
    exit 1
fi

# Check if Mix is available
if ! command -v mix &> /dev/null; then
    echo "❌ Mix is not available!"
    exit 1
fi

# Navigate to the project directory
cd "$(dirname "$0")"

# Install dependencies if needed
if [ ! -d "deps" ]; then
    echo "📦 Installing dependencies..."
    mix deps.get
fi

# Check if database needs setup
if [ "$1" == "setup" ]; then
    echo "🗄️  Setting up database..."
    mix ecto.create
    mix ecto.migrate
fi

# Start in different modes
case "$1" in
    "iex")
        echo "🚀 Starting in interactive Elixir mode..."
        iex -S mix
        ;;
    "cli")
        echo "🚀 Starting CLI interface..."
        mix run -e "CROD.CLI.main(['start'])"
        ;;
    "daemon")
        echo "🚀 Starting as daemon..."
        elixir --detached -S mix run --no-halt
        ;;
    *)
        echo "🚀 Starting CLI interface (default)..."
        mix run -e "CROD.CLI.main(['start'])"
        ;;
esac