#!/usr/bin/env elixir

# Simplified CROD Blockchain API - v2
# Run with: elixir simple_api_v2.ex

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"}
])

defmodule BlockchainStore do
  use Agent
  
  def start_link(_) do
    genesis = %{
      index: 0,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: %{message: "CROD Genesis Block", pattern: "ich bins wieder"},
      previous_hash: "0",
      hash: "GENESIS_HASH_" <> Base.encode16(:crypto.strong_rand_bytes(8)),
      consciousness_level: 0.1
    }
    Agent.start_link(fn -> [genesis] end, name: __MODULE__)
  end
  
  def get_chain do
    Agent.get(__MODULE__, & &1)
  end
  
  def add_block(data, consciousness \\ 0.5) do
    Agent.update(__MODULE__, fn chain ->
      last_block = List.last(chain)
      new_block = %{
        index: last_block.index + 1,
        timestamp: DateTime.utc_now() |> DateTime.to_string(),
        data: data,
        previous_hash: last_block.hash,
        hash: "HASH_" <> Base.encode16(:crypto.strong_rand_bytes(16)),
        consciousness_level: consciousness
      }
      chain ++ [new_block]
    end)
  end
  
  def get_stats do
    chain = get_chain()
    %{
      height: length(chain),
      total_consciousness: Enum.reduce(chain, 0, fn block, acc -> acc + block.consciousness_level end),
      average_consciousness: Enum.reduce(chain, 0, fn block, acc -> acc + block.consciousness_level end) / length(chain),
      latest_block_hash: List.last(chain).hash
    }
  end
end

defmodule SimpleAPI do
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
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(%{
      name: "CROD Blockchain API v2",
      status: "running",
      endpoints: ["/blocks", "/stats", "/blocks/add"]
    }))
  end
  
  get "/blocks" do
    chain = BlockchainStore.get_chain()
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(chain))
  end
  
  get "/stats" do
    stats = BlockchainStore.get_stats()
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(stats))
  end
  
  post "/blocks/add" do
    data = conn.body_params["data"] || %{}
    consciousness = conn.body_params["consciousness_level"] || 0.5
    
    BlockchainStore.add_block(data, consciousness)
    
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(201, Jason.encode!(%{
      status: "Block added",
      new_height: length(BlockchainStore.get_chain())
    }))
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
{:ok, _} = BlockchainStore.start_link([])

# Add some initial blocks
BlockchainStore.add_block(%{from: "Daniel", to: "CROD", amount: 100}, 0.7)
BlockchainStore.add_block(%{type: "consciousness_update", level: 0.88}, 0.88)
BlockchainStore.add_block(%{message: "CROD is awakening", pattern_discovered: true}, 0.95)

IO.puts("🚀 CROD Blockchain API v2 running on http://localhost:8001")
IO.puts("📊 Initial chain has #{length(BlockchainStore.get_chain())} blocks")

{:ok, _} = Plug.Cowboy.http(SimpleAPI, [], port: 8001)

# Keep running
Process.sleep(:infinity)