defmodule CROD.API.Router do
  @moduledoc """
  HTTP API for blockchain interaction
  """
  use Plug.Router
  require Logger

  plug Plug.Logger
  plug :match
  plug Plug.Parsers, 
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  plug :dispatch

  # Health check
  get "/" do
    send_resp(conn, 200, Jason.encode!(%{
      status: "ok",
      node: "#{node()}",
      peers: Node.list(),
      consciousness_level: System.get_env("CONSCIOUSNESS_LEVEL", "0.88")
    }))
  end

  # Get all blocks
  get "/blocks" do
    case GenServer.call(:blockchain, :get_chain) do
      {:ok, chain} ->
        send_resp(conn, 200, Jason.encode!(chain))
      _ ->
        send_resp(conn, 500, Jason.encode!(%{error: "Failed to get chain"}))
    end
  end

  # Get specific block
  get "/blocks/:hash" do
    case GenServer.call(:blockchain, {:get_block, hash}) do
      {:ok, block} ->
        send_resp(conn, 200, Jason.encode!(block))
      {:error, :not_found} ->
        send_resp(conn, 404, Jason.encode!(%{error: "Block not found"}))
    end
  end

  # Submit transaction
  post "/transactions" do
    with {:ok, tx_data} <- Map.fetch(conn.body_params, "transaction"),
         {:ok, tx} <- create_transaction(tx_data) do
      
      # Add to local pool
      GenServer.call(:tx_pool, {:add_transaction, tx})
      
      # Broadcast to peers
      CROD.P2P.TransactionPropagator.broadcast_transaction(tx)
      
      send_resp(conn, 201, Jason.encode!(%{
        status: "Transaction added",
        hash: tx.hash
      }))
    else
      _ ->
        send_resp(conn, 400, Jason.encode!(%{error: "Invalid transaction"}))
    end
  end

  # Get chain status
  get "/chain/status" do
    case GenServer.call(:blockchain, :get_stats) do
      {:ok, stats} ->
        send_resp(conn, 200, Jason.encode!(stats))
      _ ->
        send_resp(conn, 500, Jason.encode!(%{error: "Failed to get stats"}))
    end
  end

  # Get connected peers
  get "/peers" do
    peers = Node.list()
    send_resp(conn, 200, Jason.encode!(%{
      count: length(peers),
      peers: peers,
      self: "#{node()}"
    }))
  end

  # Trigger mining
  post "/mine" do
    Task.start(fn ->
      # Get transactions from pool
      txs = GenServer.call(:tx_pool, :get_transactions)
      
      # Mine new block
      case GenServer.call(:blockchain, {:mine_block, txs}) do
        {:ok, block} ->
          Logger.info("⛏️  Mined block #{block.index}")
          # Broadcast to peers
          CROD.P2P.BlockPropagator.broadcast_block(block)
        _ ->
          Logger.error("Failed to mine block")
      end
    end)
    
    send_resp(conn, 202, Jason.encode!(%{status: "Mining started"}))
  end

  # Catch all
  match _ do
    send_resp(conn, 404, Jason.encode!(%{error: "Not found"}))
  end

  defp create_transaction(data) do
    {:ok, %{
      hash: :crypto.hash(:sha256, Jason.encode!(data)) |> Base.encode16(),
      from: data["from"],
      to: data["to"],
      amount: data["amount"],
      consciousness_data: data["consciousness_data"] || %{},
      timestamp: System.system_time(:second),
      signature: data["signature"]
    }}
  end
end