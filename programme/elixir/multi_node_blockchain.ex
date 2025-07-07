#!/usr/bin/env elixir

# Multi-Node P2P Blockchain
# Run 3 instances with different ports

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"},
  {:httpoison, "~> 2.0"}
])

defmodule P2PBlock do
  @derive Jason.Encoder
  defstruct [:index, :timestamp, :data, :previous_hash, :hash, :nonce, :consciousness_level, :mined_by]
  
  def new(index, data, previous_hash, consciousness_level \\ 0.5, miner \\ "unknown") do
    block = %__MODULE__{
      index: index,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: data,
      previous_hash: previous_hash,
      nonce: 0,
      consciousness_level: consciousness_level,
      mined_by: miner
    }
    
    %{block | hash: calculate_hash(block)}
  end
  
  def calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{inspect(block.data)}#{block.previous_hash}#{block.nonce}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  def mine(block, difficulty) do
    target = String.duplicate("0", difficulty)
    mine_block(block, target)
  end
  
  defp mine_block(block, target) do
    hash = calculate_hash(block)
    
    if String.starts_with?(hash, target) do
      IO.puts("⛏️  Block mined by #{block.mined_by}! Nonce: #{block.nonce}")
      %{block | hash: hash}
    else
      block = %{block | nonce: block.nonce + 1}
      mine_block(block, target)
    end
  end
end

defmodule P2PNode do
  use Agent
  
  def start_link(opts) do
    node_id = opts[:node_id] || "node_#{:rand.uniform(1000)}"
    port = opts[:port] || 8001
    peers = opts[:peers] || []
    
    initial_state = %{
      node_id: node_id,
      port: port,
      peers: peers,
      chain: [create_genesis_block(node_id)],
      pending_transactions: [],
      mining: false,
      difficulty: 2
    }
    
    Agent.start_link(fn -> initial_state end, name: __MODULE__)
  end
  
  defp create_genesis_block(node_id) do
    P2PBlock.new(0, %{
      message: "CROD P2P Genesis",
      created_by: node_id,
      pattern: "ich bins wieder"
    }, "0", 0.1, node_id)
  end
  
  def get_state do
    Agent.get(__MODULE__, & &1)
  end
  
  def get_chain do
    Agent.get(__MODULE__, & &1.chain)
  end
  
  def add_transaction(transaction) do
    Agent.update(__MODULE__, fn state ->
      %{state | pending_transactions: state.pending_transactions ++ [transaction]}
    end)
    
    # Broadcast to peers
    broadcast_transaction(transaction)
  end
  
  def mine_block do
    state = get_state()
    
    if not state.mining and length(state.pending_transactions) > 0 do
      Agent.update(__MODULE__, fn s -> %{s | mining: true} end)
      
      Task.start(fn ->
        last_block = List.last(state.chain)
        new_block = P2PBlock.new(
          last_block.index + 1,
          %{transactions: state.pending_transactions},
          last_block.hash,
          calculate_consciousness(),
          state.node_id
        ) |> P2PBlock.mine(state.difficulty)
        
        # Add to own chain
        add_block(new_block)
        
        # Broadcast to peers
        broadcast_block(new_block)
        
        # Clear pending transactions
        Agent.update(__MODULE__, fn s -> 
          %{s | pending_transactions: [], mining: false}
        end)
      end)
    end
  end
  
  def add_block(block) do
    Agent.update(__MODULE__, fn state ->
      if valid_block?(block, List.last(state.chain)) do
        %{state | chain: state.chain ++ [block]}
      else
        state
      end
    end)
  end
  
  def sync_chain(remote_chain) do
    Agent.update(__MODULE__, fn state ->
      if length(remote_chain) > length(state.chain) and valid_chain?(remote_chain) do
        IO.puts("📥 Adopting longer chain from peer")
        %{state | chain: remote_chain}
      else
        state
      end
    end)
  end
  
  defp valid_block?(block, prev_block) do
    block.previous_hash == prev_block.hash and
    block.index == prev_block.index + 1 and
    String.starts_with?(block.hash, String.duplicate("0", 2))
  end
  
  defp valid_chain?([genesis | rest]) do
    Enum.reduce_while(rest, {true, genesis}, fn block, {_valid, prev} ->
      if valid_block?(block, prev) do
        {:cont, {true, block}}
      else
        {:halt, {false, nil}}
      end
    end) |> elem(0)
  end
  
  defp calculate_consciousness do
    :rand.uniform() * 0.5 + 0.5  # 0.5 to 1.0
  end
  
  defp broadcast_transaction(tx) do
    state = get_state()
    Enum.each(state.peers, fn peer_url ->
      Task.start(fn ->
        HTTPoison.post("#{peer_url}/api/transaction", Jason.encode!(tx), [{"Content-Type", "application/json"}])
      end)
    end)
  end
  
  defp broadcast_block(block) do
    state = get_state()
    Enum.each(state.peers, fn peer_url ->
      Task.start(fn ->
        HTTPoison.post("#{peer_url}/api/block", Jason.encode!(block), [{"Content-Type", "application/json"}])
      end)
    end)
  end
end

defmodule P2PRouter do
  use Plug.Router
  
  plug Plug.Logger
  plug :match
  plug Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  plug :dispatch
  
  # Enable CORS
  defp put_cors_headers(conn) do
    conn
    |> put_resp_header("access-control-allow-origin", "*")
    |> put_resp_header("access-control-allow-methods", "GET, POST, OPTIONS")
    |> put_resp_header("access-control-allow-headers", "content-type")
  end
  
  get "/" do
    state = P2PNode.get_state()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(%{
      node_id: state.node_id,
      port: state.port,
      chain_height: length(state.chain),
      peers: state.peers,
      pending_transactions: length(state.pending_transactions),
      mining: state.mining
    }))
  end
  
  get "/chain" do
    chain = P2PNode.get_chain()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(chain))
  end
  
  post "/transaction" do
    tx = conn.body_params
    P2PNode.add_transaction(tx)
    
    conn
    |> put_cors_headers()
    |> send_resp(201, Jason.encode!(%{status: "Transaction added"}))
  end
  
  post "/mine" do
    P2PNode.mine_block()
    
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(%{status: "Mining started"}))
  end
  
  # P2P endpoints
  post "/api/transaction" do
    # Receive transaction from peer
    tx = conn.body_params
    P2PNode.add_transaction(tx)
    
    conn
    |> put_cors_headers()
    |> send_resp(200, "")
  end
  
  post "/api/block" do
    # Receive block from peer
    block = conn.body_params |> to_block_struct()
    P2PNode.add_block(block)
    
    conn
    |> put_cors_headers()
    |> send_resp(200, "")
  end
  
  get "/api/chain" do
    # Share chain with peers
    chain = P2PNode.get_chain()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(chain))
  end
  
  match _ do
    conn
    |> put_cors_headers()
    |> send_resp(404, Jason.encode!(%{error: "Not found"}))
  end
  
  defp to_block_struct(map) do
    %P2PBlock{
      index: map["index"],
      timestamp: map["timestamp"],
      data: map["data"],
      previous_hash: map["previous_hash"],
      hash: map["hash"],
      nonce: map["nonce"],
      consciousness_level: map["consciousness_level"],
      mined_by: map["mined_by"]
    }
  end
end

# Parse command line args
{opts, _, _} = OptionParser.parse(System.argv(), 
  switches: [port: :integer, node: :string, peers: :string]
)

port = opts[:port] || 8001
node_id = opts[:node] || "node_#{port}"
peers = case opts[:peers] do
  nil -> []
  peer_string -> String.split(peer_string, ",")
end

# Start the node
{:ok, _} = P2PNode.start_link(node_id: node_id, port: port, peers: peers)

IO.puts("🚀 CROD P2P Node '#{node_id}' starting on port #{port}")
IO.puts("👥 Peers: #{inspect(peers)}")

# Start mining loop
Task.start(fn ->
  Process.sleep(5000)  # Wait for startup
  loop_mining()
end)

defp loop_mining do
  # Auto-mine if we have pending transactions
  state = P2PNode.get_state()
  if length(state.pending_transactions) >= 2 and not state.mining do
    IO.puts("🔄 Auto-mining block...")
    P2PNode.mine_block()
  end
  
  Process.sleep(10000)  # Check every 10 seconds
  loop_mining()
end

# Start HTTP server
{:ok, _} = Plug.Cowboy.http(P2PRouter, [], port: port)

# Keep running
Process.sleep(:infinity)