defmodule CROD.P2P.Supervisor do
  @moduledoc """
  Supervises P2P communication between blockchain nodes
  """
  use Supervisor
  require Logger

  def start_link(opts) do
    Supervisor.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(opts) do
    Logger.info("🔗 Starting P2P Supervisor")
    
    children = [
      # P2P Message Handler
      {CROD.P2P.MessageHandler, name: :p2p_handler},
      
      # Block Propagator - broadcasts new blocks to peers
      {CROD.P2P.BlockPropagator, name: :block_propagator},
      
      # Transaction Propagator - broadcasts new transactions
      {CROD.P2P.TransactionPropagator, name: :tx_propagator}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end

defmodule CROD.P2P.MessageHandler do
  @moduledoc """
  Handles incoming P2P messages from other nodes
  """
  use GenServer
  require Logger

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: opts[:name])
  end

  def init(_opts) do
    # Subscribe to distributed Erlang messages
    :net_kernel.monitor_nodes(true)
    {:ok, %{}}
  end

  def handle_info({:nodeup, node}, state) do
    Logger.info("📡 Node joined: #{node}")
    # Sync blockchain with new node
    sync_with_node(node)
    {:noreply, state}
  end

  def handle_info({:nodedown, node}, state) do
    Logger.warn("📴 Node left: #{node}")
    {:noreply, state}
  end

  defp sync_with_node(node) do
    Task.start(fn ->
      # Get remote chain
      case GenServer.call({:blockchain, node}, :get_chain, 10_000) do
        {:ok, remote_chain} ->
          # Compare and sync if needed
          GenServer.cast(:blockchain, {:sync_chain, remote_chain})
          Logger.info("🔄 Synced with #{node}")
        _ ->
          Logger.warn("Failed to sync with #{node}")
      end
    end)
  end
end

defmodule CROD.P2P.BlockPropagator do
  @moduledoc """
  Propagates new blocks to all connected peers
  """
  use GenServer
  require Logger

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: opts[:name])
  end

  def init(_opts) do
    {:ok, %{}}
  end

  def broadcast_block(block) do
    GenServer.cast(__MODULE__, {:broadcast_block, block})
  end

  def handle_cast({:broadcast_block, block}, state) do
    peers = Node.list()
    Logger.info("📢 Broadcasting block #{block.index} to #{length(peers)} peers")
    
    Enum.each(peers, fn peer ->
      GenServer.cast({:blockchain, peer}, {:add_block_from_peer, block})
    end)
    
    {:noreply, state}
  end
end

defmodule CROD.P2P.TransactionPropagator do
  @moduledoc """
  Propagates new transactions to all connected peers
  """
  use GenServer
  require Logger

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: opts[:name])
  end

  def init(_opts) do
    {:ok, %{}}
  end

  def broadcast_transaction(tx) do
    GenServer.cast(__MODULE__, {:broadcast_tx, tx})
  end

  def handle_cast({:broadcast_tx, tx}, state) do
    peers = Node.list()
    Logger.info("📤 Broadcasting transaction to #{length(peers)} peers")
    
    Enum.each(peers, fn peer ->
      GenServer.cast({:tx_pool, peer}, {:add_transaction_from_peer, tx})
    end)
    
    {:noreply, state}
  end
end