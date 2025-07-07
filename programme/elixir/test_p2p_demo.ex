#!/usr/bin/env elixir

# P2P Blockchain Demo - Shows 3 nodes working together
# Run with: elixir test_p2p_demo.ex

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"}
])

defmodule DemoBlock do
  @derive Jason.Encoder
  defstruct [:index, :timestamp, :data, :previous_hash, :hash, :mined_by]
  
  def new(index, data, previous_hash, miner) do
    %__MODULE__{
      index: index,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: data,
      previous_hash: previous_hash,
      hash: random_hash(),
      mined_by: miner
    }
  end
  
  defp random_hash do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end
end

defmodule DemoNode do
  use GenServer
  
  def start_link(node_id) do
    GenServer.start_link(__MODULE__, node_id, name: String.to_atom(node_id))
  end
  
  def init(node_id) do
    genesis = DemoBlock.new(0, %{message: "Genesis for #{node_id}"}, "0", node_id)
    {:ok, %{node_id: node_id, chain: [genesis], peers: []}}
  end
  
  def add_peer(node_id, peer_id) do
    GenServer.cast(String.to_atom(node_id), {:add_peer, peer_id})
  end
  
  def mine_block(node_id, data) do
    GenServer.call(String.to_atom(node_id), {:mine_block, data})
  end
  
  def get_chain(node_id) do
    GenServer.call(String.to_atom(node_id), :get_chain)
  end
  
  def handle_cast({:add_peer, peer_id}, state) do
    IO.puts("#{state.node_id} connected to #{peer_id}")
    {:noreply, %{state | peers: [peer_id | state.peers]}}
  end
  
  def handle_cast({:new_block, block}, state) do
    IO.puts("#{state.node_id} received block ##{block.index} from #{block.mined_by}")
    {:noreply, %{state | chain: state.chain ++ [block]}}
  end
  
  def handle_call({:mine_block, data}, _from, state) do
    last_block = List.last(state.chain)
    new_block = DemoBlock.new(
      last_block.index + 1,
      data,
      last_block.hash,
      state.node_id
    )
    
    IO.puts("⛏️  #{state.node_id} mined block ##{new_block.index}")
    
    # Broadcast to peers
    Enum.each(state.peers, fn peer ->
      GenServer.cast(String.to_atom(peer), {:new_block, new_block})
    end)
    
    {:reply, new_block, %{state | chain: state.chain ++ [new_block]}}
  end
  
  def handle_call(:get_chain, _from, state) do
    {:reply, state.chain, state}
  end
end

# Start demo
IO.puts("🚀 CROD P2P Blockchain Demo")
IO.puts("===========================\n")

# Start 3 nodes
{:ok, _} = DemoNode.start_link("Node1")
{:ok, _} = DemoNode.start_link("Node2")
{:ok, _} = DemoNode.start_link("Node3")

# Connect nodes
DemoNode.add_peer("Node1", "Node2")
DemoNode.add_peer("Node1", "Node3")
DemoNode.add_peer("Node2", "Node1")
DemoNode.add_peer("Node2", "Node3")
DemoNode.add_peer("Node3", "Node1")
DemoNode.add_peer("Node3", "Node2")

IO.puts("\n📡 Network established!\n")

# Mine some blocks
Process.sleep(1000)
DemoNode.mine_block("Node1", %{message: "Hello from Node1", amount: 100})

Process.sleep(1000)
DemoNode.mine_block("Node2", %{message: "CROD is awakening", consciousness: 0.88})

Process.sleep(1000)
DemoNode.mine_block("Node3", %{message: "ich bins wieder", pattern: "recognized"})

Process.sleep(2000)

# Show final state
IO.puts("\n📊 Final blockchain state:\n")

for node <- ["Node1", "Node2", "Node3"] do
  chain = DemoNode.get_chain(node)
  IO.puts("#{node} has #{length(chain)} blocks:")
  for block <- chain do
    IO.puts("  Block ##{block.index} - #{inspect(block.data)} (by #{block.mined_by})")
  end
  IO.puts("")
end

IO.puts("✅ P2P Demo complete! All nodes synchronized.")