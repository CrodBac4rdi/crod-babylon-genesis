#!/usr/bin/env elixir

# Simple P2P Blockchain Node
# Uses Erlang distribution for P2P

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"}
])

defmodule SimpleP2PNode do
  use GenServer
  require Logger
  
  defstruct [
    :node_name,
    :port,
    chain: [],
    peers: [],
    pending_txs: [],
    mining: false
  ]
  
  # Client API
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def get_chain do
    GenServer.call(__MODULE__, :get_chain)
  end
  
  def add_transaction(tx) do
    GenServer.cast(__MODULE__, {:add_transaction, tx})
  end
  
  def mine_block do
    GenServer.cast(__MODULE__, :mine_block)
  end
  
  def connect_peer(peer_node) do
    GenServer.cast(__MODULE__, {:connect_peer, peer_node})
  end
  
  # Server Callbacks
  
  def init(opts) do
    node_name = opts[:node_name] || "node_#{:rand.uniform(1000)}"
    port = opts[:port] || 8001
    
    # Set node name for Erlang distribution
    Node.start(:"#{node_name}@localhost", :shortnames)
    Node.set_cookie(:crod_blockchain)
    
    genesis = %{
      index: 0,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: %{message: "CROD Genesis", node: node_name},
      previous_hash: "0",
      hash: "GENESIS_#{node_name}",
      consciousness: 0.1
    }
    
    state = %__MODULE__{
      node_name: node_name,
      port: port,
      chain: [genesis],
      peers: [],
      pending_txs: [],
      mining: false
    }
    
    Logger.info("🚀 Node #{node_name} started on port #{port}")
    Logger.info("🔗 Erlang node: #{Node.self()}")
    
    # Start auto-discovery
    schedule_peer_discovery()
    
    {:ok, state}
  end
  
  def handle_call(:get_chain, _from, state) do
    {:reply, state.chain, state}
  end
  
  def handle_call(:get_state, _from, state) do
    {:reply, %{
      node: state.node_name,
      erlang_node: Node.self(),
      chain_height: length(state.chain),
      peers: Node.list(),
      pending_txs: length(state.pending_txs),
      mining: state.mining
    }, state}
  end
  
  def handle_cast({:add_transaction, tx}, state) do
    Logger.info("📝 Adding transaction: #{inspect(tx)}")
    
    # Broadcast to peers
    broadcast_to_peers({:transaction, tx})
    
    {:noreply, %{state | pending_txs: state.pending_txs ++ [tx]}}
  end
  
  def handle_cast(:mine_block, %{mining: true} = state) do
    Logger.warn("⛏️  Already mining!")
    {:noreply, state}
  end
  
  def handle_cast(:mine_block, state) do
    if length(state.pending_txs) > 0 do
      Logger.info("⛏️  Starting to mine block...")
      
      Task.start(fn ->
        last_block = List.last(state.chain)
        
        new_block = %{
          index: last_block.index + 1,
          timestamp: DateTime.utc_now() |> DateTime.to_string(),
          data: %{
            transactions: state.pending_txs,
            miner: state.node_name
          },
          previous_hash: last_block.hash,
          consciousness: :rand.uniform()
        }
        
        # Simple mining (just add nonce)
        mined_block = mine(new_block)
        
        GenServer.cast(__MODULE__, {:block_mined, mined_block})
      end)
      
      {:noreply, %{state | mining: true}}
    else
      Logger.info("📭 No transactions to mine")
      {:noreply, state}
    end
  end
  
  def handle_cast({:block_mined, block}, state) do
    Logger.info("✅ Block mined! Hash: #{block.hash}")
    
    # Add to chain
    new_chain = state.chain ++ [block]
    
    # Broadcast to peers
    broadcast_to_peers({:new_block, block})
    
    {:noreply, %{state | 
      chain: new_chain,
      pending_txs: [],
      mining: false
    }}
  end
  
  def handle_cast({:connect_peer, peer_node}, state) do
    case Node.connect(peer_node) do
      true ->
        Logger.info("✅ Connected to peer: #{peer_node}")
        {:noreply, state}
      false ->
        Logger.warn("❌ Failed to connect to: #{peer_node}")
        {:noreply, state}
    end
  end
  
  # Handle messages from peers
  def handle_info({:transaction, tx}, state) do
    Logger.info("📥 Received transaction from peer")
    {:noreply, %{state | pending_txs: state.pending_txs ++ [tx]}}
  end
  
  def handle_info({:new_block, block}, state) do
    Logger.info("📥 Received block from peer")
    
    # Simple validation
    last_block = List.last(state.chain)
    if block.previous_hash == last_block.hash and block.index == last_block.index + 1 do
      {:noreply, %{state | chain: state.chain ++ [block]}}
    else
      Logger.warn("❌ Invalid block received")
      {:noreply, state}
    end
  end
  
  def handle_info(:discover_peers, state) do
    # Check for new peers
    current_peers = Node.list()
    if current_peers != state.peers do
      Logger.info("🔍 Peers updated: #{inspect(current_peers)}")
    end
    
    schedule_peer_discovery()
    {:noreply, %{state | peers: current_peers}}
  end
  
  defp mine(block) do
    # Simulate mining with delay
    Process.sleep(2000 + :rand.uniform(3000))
    
    nonce = :rand.uniform(100000)
    hash = :crypto.hash(:sha256, "#{inspect(block)}#{nonce}") |> Base.encode16()
    
    Map.merge(block, %{nonce: nonce, hash: hash})
  end
  
  defp broadcast_to_peers(message) do
    Node.list()
    |> Enum.each(fn peer ->
      send({__MODULE__, peer}, message)
    end)
  end
  
  defp schedule_peer_discovery do
    Process.send_after(self(), :discover_peers, 5000)
  end
end

# HTTP API
defmodule SimpleP2PAPI do
  use Plug.Router
  
  plug Plug.Logger
  plug :match
  plug Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  plug :dispatch
  
  defp put_cors_headers(conn) do
    conn
    |> put_resp_header("access-control-allow-origin", "*")
    |> put_resp_header("access-control-allow-methods", "GET, POST, OPTIONS")
    |> put_resp_header("access-control-allow-headers", "content-type")
  end
  
  get "/" do
    state = GenServer.call(SimpleP2PNode, :get_state)
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(state))
  end
  
  get "/chain" do
    chain = SimpleP2PNode.get_chain()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(chain))
  end
  
  post "/transaction" do
    tx = Map.merge(conn.body_params, %{
      "timestamp" => DateTime.utc_now() |> DateTime.to_string(),
      "id" => :crypto.strong_rand_bytes(8) |> Base.encode16()
    })
    
    SimpleP2PNode.add_transaction(tx)
    
    conn
    |> put_cors_headers()
    |> send_resp(201, Jason.encode!(%{status: "Transaction added", tx: tx}))
  end
  
  post "/mine" do
    SimpleP2PNode.mine_block()
    
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(%{status: "Mining started"}))
  end
  
  post "/connect" do
    peer = conn.body_params["peer"]
    if peer do
      SimpleP2PNode.connect_peer(String.to_atom(peer))
      conn
      |> put_cors_headers()
      |> send_resp(200, Jason.encode!(%{status: "Connecting to #{peer}"}))
    else
      conn
      |> put_cors_headers()
      |> send_resp(400, Jason.encode!(%{error: "Missing peer parameter"}))
    end
  end
  
  match _ do
    conn
    |> put_cors_headers()
    |> send_resp(404, Jason.encode!(%{error: "Not found"}))
  end
end

# Parse arguments
{opts, _, _} = OptionParser.parse(System.argv(), 
  switches: [port: :integer, node: :string]
)

port = opts[:port] || 8001
node_name = opts[:node] || "node#{port}"

# Start the node
{:ok, _} = SimpleP2PNode.start_link(node_name: node_name, port: port)

# Start auto-mining
Task.start(fn ->
  loop_auto_mine()
end)

defp loop_auto_mine do
  Process.sleep(15000)  # Every 15 seconds
  
  state = GenServer.call(SimpleP2PNode, :get_state)
  if state.pending_txs > 0 and not state.mining do
    IO.puts("🤖 Auto-mining triggered...")
    SimpleP2PNode.mine_block()
  end
  
  loop_auto_mine()
end

# Start HTTP server
IO.puts("🌐 Starting HTTP API on port #{port}")
{:ok, _} = Plug.Cowboy.http(SimpleP2PAPI, [], port: port)

# Keep running
Process.sleep(:infinity)