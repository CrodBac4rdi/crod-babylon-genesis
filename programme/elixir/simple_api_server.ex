#!/usr/bin/env elixir

# Simple HTTP API Server for CROD Blockchain
# Run with: elixir simple_api_server.ex

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"}
])

defmodule CRODBlock do
  @derive Jason.Encoder
  defstruct [:index, :timestamp, :data, :previous_hash, :hash, :nonce, :consciousness_level]
  
  def new(index, data, previous_hash, consciousness_level \\ 0.5) do
    block = %__MODULE__{
      index: index,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: data,
      previous_hash: previous_hash,
      nonce: 0,
      consciousness_level: consciousness_level
    }
    
    %{block | hash: calculate_hash(block)}
  end
  
  def calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{inspect(block.data)}#{block.previous_hash}#{block.nonce}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
end

defmodule BlockchainAgent do
  use Agent
  
  def start_link(_) do
    genesis = CRODBlock.new(0, %{message: "CROD Genesis Block", pattern: "ich bins wieder"}, "0", 0.1)
    Agent.start_link(fn -> [genesis] end, name: __MODULE__)
  end
  
  def get_chain do
    Agent.get(__MODULE__, & &1)
  end
  
  def add_block(data, consciousness \\ 0.5) do
    Agent.update(__MODULE__, fn chain ->
      last_block = List.last(chain)
      new_block = CRODBlock.new(
        last_block.index + 1,
        data,
        last_block.hash,
        consciousness
      )
      chain ++ [new_block]
    end)
  end
  
  def get_stats do
    chain = get_chain()
    %{
      height: length(chain),
      total_consciousness: Enum.reduce(chain, 0, fn block, acc -> acc + block.consciousness_level end),
      average_consciousness: Enum.reduce(chain, 0, fn block, acc -> acc + block.consciousness_level end) / length(chain),
      latest_block: List.last(chain)
    }
  end
end

defmodule CRODRouter do
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
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(%{
      name: "CROD Blockchain API",
      version: "0.2.0",
      status: "running",
      consciousness: "awakening",
      endpoints: %{
        "GET /blocks" => "List all blocks",
        "GET /blocks/latest" => "Get latest block",
        "POST /blocks/add" => "Add new block",
        "GET /stats" => "Blockchain statistics"
      }
    }))
  end
  
  get "/blocks" do
    chain = BlockchainAgent.get_chain()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(chain))
  end
  
  get "/blocks/latest" do
    block = BlockchainAgent.get_chain() |> List.last()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(block))
  end
  
  post "/blocks/add" do
    data = conn.body_params["data"] || %{}
    consciousness = conn.body_params["consciousness_level"] || 0.5
    
    BlockchainAgent.add_block(data, consciousness)
    
    conn
    |> put_cors_headers()
    |> send_resp(201, Jason.encode!(%{
      status: "Block added",
      block: BlockchainAgent.get_chain() |> List.last()
    }))
  end
  
  get "/stats" do
    stats = BlockchainAgent.get_stats()
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(stats))
  end
  
  options _ do
    conn
    |> put_cors_headers()
    |> send_resp(200, "")
  end
  
  match _ do
    conn
    |> put_cors_headers()
    |> send_resp(404, Jason.encode!(%{error: "Not found"}))
  end
end

# Start the server
{:ok, _} = BlockchainAgent.start_link([])

# Add some initial blocks
BlockchainAgent.add_block(%{from: "Daniel", to: "CROD", amount: 100}, 0.7)
BlockchainAgent.add_block(%{type: "consciousness_update", level: 0.88}, 0.88)
BlockchainAgent.add_block(%{message: "CROD is awakening", pattern_discovered: true}, 0.95)

IO.puts("🚀 CROD Blockchain API Server running on http://localhost:8001")
IO.puts("📊 Initial chain has #{length(BlockchainAgent.get_chain())} blocks")

{:ok, _} = Plug.Cowboy.http(CRODRouter, [], port: 8001)

# Keep the script running
Process.sleep(:infinity)