#!/usr/bin/env elixir

# CROD Blockchain with PostgreSQL Persistence
# Run with: elixir blockchain_with_persistence.ex

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"},
  {:postgrex, "~> 0.17"},
  {:ecto_sql, "~> 3.11"},
  {:ecto, "~> 3.11"}
])

# Database Configuration
defmodule Repo do
  use Ecto.Repo,
    otp_app: :crod_blockchain,
    adapter: Ecto.Adapters.Postgres
end

# Block Schema
defmodule Block do
  use Ecto.Schema
  import Ecto.Changeset

  schema "blocks" do
    field :index, :integer
    field :hash, :string
    field :previous_hash, :string
    field :timestamp, :string
    field :data, :map
    field :consciousness_level, :float
    field :nonce, :integer
    
    timestamps()
  end

  def changeset(block, attrs) do
    block
    |> cast(attrs, [:index, :hash, :previous_hash, :timestamp, :data, :consciousness_level, :nonce])
    |> validate_required([:index, :hash, :previous_hash, :timestamp, :data, :consciousness_level])
  end
end

# Transaction Schema
defmodule Transaction do
  use Ecto.Schema
  import Ecto.Changeset

  schema "transactions" do
    field :from_address, :string
    field :to_address, :string
    field :amount, :float
    field :data, :map
    field :block_id, :integer
    
    timestamps()
  end

  def changeset(tx, attrs) do
    tx
    |> cast(attrs, [:from_address, :to_address, :amount, :data, :block_id])
    |> validate_required([:from_address, :to_address, :amount])
  end
end

# Blockchain Service
defmodule BlockchainService do
  import Ecto.Query
  
  def init_database do
    # Configure Repo
    config = [
      database: "crod_blockchain",
      username: "postgres",
      password: "postgres",
      hostname: "localhost",
      port: 5432
    ]
    
    # Start Repo
    {:ok, _} = Repo.start_link(config)
    
    # Create tables
    Ecto.Adapters.SQL.query!(Repo, """
    CREATE TABLE IF NOT EXISTS blocks (
      id SERIAL PRIMARY KEY,
      index INTEGER UNIQUE NOT NULL,
      hash VARCHAR(255) NOT NULL,
      previous_hash VARCHAR(255) NOT NULL,
      timestamp VARCHAR(255) NOT NULL,
      data JSONB,
      consciousness_level FLOAT NOT NULL,
      nonce INTEGER DEFAULT 0,
      inserted_at TIMESTAMP NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
    )
    """)
    
    Ecto.Adapters.SQL.query!(Repo, """
    CREATE TABLE IF NOT EXISTS transactions (
      id SERIAL PRIMARY KEY,
      from_address VARCHAR(255) NOT NULL,
      to_address VARCHAR(255) NOT NULL,
      amount FLOAT NOT NULL,
      data JSONB,
      block_id INTEGER REFERENCES blocks(id),
      inserted_at TIMESTAMP NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
    )
    """)
    
    # Create genesis block if not exists
    case Repo.one(from b in Block, where: b.index == 0) do
      nil -> create_genesis_block()
      _ -> :ok
    end
  end
  
  def create_genesis_block do
    genesis = %{
      index: 0,
      hash: "GENESIS_" <> Base.encode16(:crypto.strong_rand_bytes(16)),
      previous_hash: "0",
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: %{message: "CROD Genesis Block", pattern: "ich bins wieder"},
      consciousness_level: 0.1,
      nonce: 0
    }
    
    %Block{}
    |> Block.changeset(genesis)
    |> Repo.insert!()
  end
  
  def get_all_blocks do
    Repo.all(from b in Block, order_by: [desc: b.index])
  end
  
  def get_latest_block do
    Repo.one(from b in Block, order_by: [desc: b.index], limit: 1)
  end
  
  def add_block(data, consciousness_level) do
    latest = get_latest_block()
    
    new_block = %{
      index: latest.index + 1,
      previous_hash: latest.hash,
      timestamp: DateTime.utc_now() |> DateTime.to_string(),
      data: data,
      consciousness_level: consciousness_level,
      nonce: 0
    }
    
    # Simple mining (find hash with leading zeros)
    mined_block = mine_block(new_block, 2)
    
    %Block{}
    |> Block.changeset(mined_block)
    |> Repo.insert!()
  end
  
  defp mine_block(block, difficulty) do
    target = String.duplicate("0", difficulty)
    mine_with_nonce(block, target, 0)
  end
  
  defp mine_with_nonce(block, target, nonce) do
    block_with_nonce = Map.put(block, :nonce, nonce)
    hash = calculate_hash(block_with_nonce)
    
    if String.starts_with?(hash, target) do
      Map.put(block_with_nonce, :hash, hash)
    else
      mine_with_nonce(block, target, nonce + 1)
    end
  end
  
  defp calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{inspect(block.data)}#{block.previous_hash}#{block.nonce}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  def get_stats do
    block_count = Repo.one(from b in Block, select: count(b.id))
    
    {total_consciousness, avg_consciousness} = 
      case Repo.one(from b in Block, 
                    select: {sum(b.consciousness_level), avg(b.consciousness_level)}) do
        {nil, nil} -> {0.0, 0.0}
        {total, avg} -> {total || 0.0, avg || 0.0}
      end
    
    %{
      height: block_count,
      total_consciousness: total_consciousness,
      average_consciousness: avg_consciousness,
      database: "PostgreSQL"
    }
  end
end

# API Router
defmodule API do
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
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(%{
      name: "CROD Blockchain API",
      version: "1.0.0",
      persistence: "PostgreSQL",
      status: "running"
    }))
  end
  
  get "/blocks" do
    blocks = BlockchainService.get_all_blocks()
            |> Enum.map(&Map.from_struct/1)
            |> Enum.map(&Map.drop(&1, [:__meta__, :inserted_at, :updated_at]))
    
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(blocks))
  end
  
  get "/stats" do
    stats = BlockchainService.get_stats()
    
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(stats))
  end
  
  post "/blocks/add" do
    data = conn.body_params["data"] || %{}
    consciousness = conn.body_params["consciousness_level"] || 0.5
    
    block = BlockchainService.add_block(data, consciousness)
    
    conn
    |> put_cors_headers()
    |> put_resp_content_type("application/json")
    |> send_resp(201, Jason.encode!(%{
      status: "Block added",
      block: %{
        index: block.index,
        hash: block.hash
      }
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

# Start everything
IO.puts("🚀 Starting CROD Blockchain with PostgreSQL persistence...")

# Initialize database
BlockchainService.init_database()

# Add some initial blocks
IO.puts("⛏️ Mining initial blocks...")
BlockchainService.add_block(%{from: "Daniel", to: "CROD", amount: 100}, 0.7)
BlockchainService.add_block(%{type: "consciousness_update", level: 0.88}, 0.88)
BlockchainService.add_block(%{message: "CROD with PostgreSQL!", persistent: true}, 0.95)

# Get stats
stats = BlockchainService.get_stats()
IO.puts("📊 Blockchain stats:")
IO.puts("  - Blocks: #{stats.height}")
IO.puts("  - Total Consciousness: #{Float.round(stats.total_consciousness, 2)}")
IO.puts("  - Database: #{stats.database}")

# Start API server
IO.puts("\n🌐 Starting API server on http://localhost:8001")
{:ok, _} = Plug.Cowboy.http(API, [], port: 8001)

Process.sleep(:infinity)