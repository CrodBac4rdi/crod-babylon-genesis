defmodule CROD.P2PSync do
  @moduledoc """
  P2P synchronization for CROD Blockchain nodes.
  Handles block propagation and chain synchronization across connected nodes.
  """
  use GenServer
  require Logger

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    # Subscribe to blockchain events
    :ok = Phoenix.PubSub.subscribe(CROD.PubSub, "blockchain:events")
    
    # Start periodic sync
    schedule_sync()
    
    {:ok, %{syncing: false}}
  end

  # Broadcast new block to all connected nodes
  def broadcast_block(block) do
    for node <- Node.list() do
      Task.start(fn ->
        GenServer.cast({__MODULE__, node}, {:new_block, block, Node.self()})
      end)
    end
  end

  # Request chain from a specific node
  def request_chain(from_node) do
    GenServer.call({__MODULE__, from_node}, :get_chain)
  end

  # Handle incoming new block
  def handle_cast({:new_block, block, from_node}, state) do
    Logger.info("Received new block from #{from_node}: #{block.index}")
    
    # Add to local blockchain if valid
    case CROD.Blockchain.add_block(:blockchain1, block.data) do
      {:ok, _} -> Logger.info("Block added successfully")
      {:error, reason} -> Logger.warn("Failed to add block: #{reason}")
    end
    
    {:noreply, state}
  end

  # Handle chain request
  def handle_call(:get_chain, _from, state) do
    chain = CROD.Blockchain.get_chain(:blockchain1)
    {:reply, chain, state}
  end

  # Handle blockchain events
  def handle_info({:blockchain_event, :new_block, block}, state) do
    broadcast_block(block)
    {:noreply, state}
  end

  # Periodic chain sync
  def handle_info(:sync_chain, state) do
    if not state.syncing and length(Node.list()) > 0 do
      Task.start(fn -> sync_with_peers() end)
    end
    
    schedule_sync()
    {:noreply, state}
  end

  defp sync_with_peers do
    Logger.info("Syncing with peers...")
    
    # Get chains from all peers
    chains = for node <- Node.list() do
      try do
        request_chain(node)
      catch
        _, _ -> nil
      end
    end |> Enum.filter(&(&1 != nil))
    
    # Find longest valid chain
    local_chain = CROD.Blockchain.get_chain(:blockchain1)
    longest_chain = [local_chain | chains]
      |> Enum.max_by(&length/1)
    
    # Replace chain if found longer valid one
    if length(longest_chain) > length(local_chain) do
      Logger.info("Found longer chain, replacing...")
      # In real implementation, would validate and replace entire chain
    end
  end

  defp schedule_sync do
    Process.send_after(self(), :sync_chain, 30_000) # Every 30 seconds
  end
end