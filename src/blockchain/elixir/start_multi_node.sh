#!/bin/bash

# Start 3 CROD Blockchain Nodes locally
echo "🚀 Starting CROD Multi-Node Blockchain..."

# Clean up any existing nodes
pkill -f "elixir.*node1@" 2>/dev/null
pkill -f "elixir.*node2@" 2>/dev/null
pkill -f "elixir.*node3@" 2>/dev/null

sleep 1

# Start Node 1 (Genesis Node)
echo "Starting Node 1 (Genesis) on port 8001..."
elixir --name node1@127.0.0.1 --cookie crod_blockchain -S mix run -e "
  {:ok, _} = CROD.Blockchain.start_link(name: :blockchain1)
  IO.puts(\"Node 1 running on #{Node.self()}\")
  Process.sleep(:infinity)
" &

sleep 2

# Start Node 2
echo "Starting Node 2 on port 8002..."
elixir --name node2@127.0.0.1 --cookie crod_blockchain -S mix run -e "
  Node.connect(:\"node1@127.0.0.1\")
  {:ok, _} = CROD.Blockchain.start_link(name: :blockchain2)
  IO.puts(\"Node 2 running on #{Node.self()}\")
  IO.puts(\"Connected to: #{Node.list()}\")
  Process.sleep(:infinity)
" &

sleep 2

# Start Node 3
echo "Starting Node 3 on port 8003..."
elixir --name node3@127.0.0.1 --cookie crod_blockchain -S mix run -e "
  Node.connect(:\"node1@127.0.0.1\")
  Node.connect(:\"node2@127.0.0.1\")
  {:ok, _} = CROD.Blockchain.start_link(name: :blockchain3)
  IO.puts(\"Node 3 running on #{Node.self()}\")
  IO.puts(\"Connected to: #{Node.list()}\")
  Process.sleep(:infinity)
" &

echo ""
echo "✅ All nodes started! They're automatically connected via Erlang Distribution."
echo ""
echo "To interact with the nodes:"
echo "  iex --name client@127.0.0.1 --cookie crod_blockchain"
echo "  Then: Node.connect(:\"node1@127.0.0.1\")"
echo ""
echo "To stop all nodes: pkill -f 'elixir.*node'"