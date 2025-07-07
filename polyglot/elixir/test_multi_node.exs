#!/usr/bin/env elixir

# Test Multi-Node Blockchain
# Run this after starting nodes with ./start_multi_node.sh

IO.puts("🔗 CROD Multi-Node Blockchain Test")
IO.puts("==================================")

# Connect to all nodes
nodes = [:"node1@127.0.0.1", :"node2@127.0.0.1", :"node3@127.0.0.1"]

IO.puts("\nConnecting to nodes...")
for node <- nodes do
  case Node.connect(node) do
    true -> IO.puts("✅ Connected to #{node}")
    false -> IO.puts("❌ Failed to connect to #{node}")
  end
end

IO.puts("\nConnected nodes: #{inspect(Node.list())}")

# Test: Add block on node1, should propagate to others
IO.puts("\n📤 Adding block on node1...")
result = :rpc.call(:"node1@127.0.0.1", CROD.Blockchain, :add_block, 
  [:blockchain1, %{
    data: "Multi-node test block",
    consciousness_level: 0.88,
    from_node: "test_client"
  }])

IO.puts("Result: #{inspect(result)}")

# Wait for propagation
Process.sleep(1000)

# Check chains on all nodes
IO.puts("\n📊 Checking chains on all nodes:")
for node <- nodes do
  chain = :rpc.call(node, CROD.Blockchain, :get_chain, [:blockchain1])
  IO.puts("\n#{node}:")
  IO.puts("  Chain length: #{length(chain)}")
  if length(chain) > 0 do
    latest = List.last(chain)
    IO.puts("  Latest block: #{latest.index} - #{inspect(latest.data)}")
  end
end

# Test mining on different nodes
IO.puts("\n⛏️  Mining blocks on different nodes...")

tasks = for {node, index} <- Enum.with_index(nodes) do
  Task.async(fn ->
    :rpc.call(node, CROD.Blockchain, :mine_block, [
      :blockchain1, 
      %{
        data: "Block mined by #{node}",
        consciousness_level: 0.5 + index * 0.1
      }
    ])
  end)
end

results = Task.await_many(tasks, 30_000)
IO.puts("Mining results: #{inspect(results)}")

# Final chain state
Process.sleep(2000)
IO.puts("\n📊 Final chain state:")
for node <- nodes do
  chain = :rpc.call(node, CROD.Blockchain, :get_chain, [:blockchain1])
  IO.puts("#{node}: #{length(chain)} blocks")
end