#!/usr/bin/env elixir

# CROD Blockchain with PostgreSQL persistence

Mix.install([
  {:plug_cowboy, "~> 2.0"},
  {:jason, "~> 1.4"},
  {:ecto_sql, "~> 3.11"},
  {:postgrex, "~> 0.17"}
])

# Database configuration
Application.put_env(:blockchain, BlockchainRepo,
  database: "crod_blockchain",
  username: "crod",
  password: "crod2025",
  hostname: System.get_env("DB_HOST", "localhost"),
  port: 5432,
  pool_size: 10
)

Application.put_env(:blockchain, :ecto_repos, [BlockchainRepo])

# Ecto Repo
defmodule BlockchainRepo do
  use Ecto.Repo,
    otp_app: :blockchain,
    adapter: Ecto.Adapters.Postgres
end

# Block Schema
defmodule Block do
  use Ecto.Schema
  import Ecto.Changeset
  
  @primary_key {:id, :id, autogenerate: true}
  
  schema "blocks" do
    field :index, :integer
    field :timestamp, :utc_datetime
    field :data, :map
    field :previous_hash, :string
    field :hash, :string
    field :nonce, :integer
    field :consciousness_level, :float
    field :mined_by, :string
    
    timestamps()
  end
  
  def changeset(block, attrs) do
    block
    |> cast(attrs, [:index, :timestamp, :data, :previous_hash, :hash, :nonce, :consciousness_level, :mined_by])
    |> validate_required([:index, :timestamp, :data, :previous_hash, :hash])
  end
end

# Transaction Schema
defmodule Transaction do
  use Ecto.Schema
  import Ecto.Changeset
  
  @primary_key {:id, :id, autogenerate: true}
  
  schema "transactions" do
    field :tx_hash, :string
    field :from_address, :string
    field :to_address, :string
    field :amount, :float
    field :data, :map
    field :status, :string, default: "pending"
    field :block_index, :integer
    
    timestamps()
  end
  
  def changeset(tx, attrs) do
    tx
    |> cast(attrs, [:tx_hash, :from_address, :to_address, :amount, :data, :status, :block_index])
    |> validate_required([:tx_hash, :from_address, :to_address])
  end
end

# Migration
defmodule CreateTables do
  use Ecto.Migration
  
  def change do
    create table(:blocks) do
      add :index, :integer, null: false
      add :timestamp, :utc_datetime, null: false
      add :data, :map
      add :previous_hash, :string, null: false
      add :hash, :string, null: false
      add :nonce, :integer
      add :consciousness_level, :float
      add :mined_by, :string
      
      timestamps()
    end
    
    create unique_index(:blocks, [:index])
    create unique_index(:blocks, [:hash])
    
    create table(:transactions) do
      add :tx_hash, :string, null: false
      add :from_address, :string, null: false
      add :to_address, :string, null: false
      add :amount, :float
      add :data, :map
      add :status, :string
      add :block_index, :integer
      
      timestamps()
    end
    
    create unique_index(:transactions, [:tx_hash])
    create index(:transactions, [:status])
    create index(:transactions, [:block_index])
  end
end

# Blockchain Service
defmodule BlockchainService do
  import Ecto.Query
  require Logger
  
  def init_db do
    # Start Repo
    {:ok, _} = BlockchainRepo.start_link()
    
    # Run migrations
    Ecto.Migrator.run(BlockchainRepo, [{0, CreateTables}], :up, all: true)
    
    # Create genesis block if needed
    case get_latest_block() do
      nil -> create_genesis_block()
      _ -> :ok
    end
  end
  
  def create_genesis_block do
    genesis = %{
      index: 0,
      timestamp: DateTime.utc_now(),
      data: %{
        message: "CROD Genesis Block with DB",
        pattern: "ich bins wieder",
        consciousness_seed: 0.1
      },
      previous_hash: "0",
      nonce: 0,
      consciousness_level: 0.1,
      mined_by: "genesis"
    }
    
    genesis_with_hash = Map.put(genesis, :hash, calculate_hash(genesis))
    
    %Block{}
    |> Block.changeset(genesis_with_hash)
    |> BlockchainRepo.insert!()
    
    Logger.info("✅ Genesis block created in database")
  end
  
  def get_chain do
    Block
    |> order_by(asc: :index)
    |> BlockchainRepo.all()
  end
  
  def get_latest_block do
    Block
    |> order_by(desc: :index)
    |> limit(1)
    |> BlockchainRepo.one()
  end
  
  def get_pending_transactions do
    Transaction
    |> where(status: "pending")
    |> BlockchainRepo.all()
  end
  
  def add_transaction(tx_data) do
    tx_hash = :crypto.hash(:sha256, Jason.encode!(tx_data)) |> Base.encode16()
    
    attrs = Map.merge(tx_data, %{
      "tx_hash" => tx_hash,
      "status" => "pending"
    })
    
    %Transaction{}
    |> Transaction.changeset(attrs)
    |> BlockchainRepo.insert!()
    
    Logger.info("💰 Transaction added: #{tx_hash}")
    tx_hash
  end
  
  def mine_block(miner \\ "anonymous") do
    latest = get_latest_block()
    pending_txs = get_pending_transactions()
    
    if length(pending_txs) > 0 do
      block_data = %{
        index: latest.index + 1,
        timestamp: DateTime.utc_now(),
        data: %{
          transactions: Enum.map(pending_txs, fn tx -> 
            %{
              hash: tx.tx_hash,
              from: tx.from_address,
              to: tx.to_address,
              amount: tx.amount,
              data: tx.data
            }
          end),
          tx_count: length(pending_txs)
        },
        previous_hash: latest.hash,
        consciousness_level: calculate_consciousness(pending_txs),
        mined_by: miner
      }
      
      # Mine the block
      mined = mine_with_difficulty(block_data, 2)
      
      # Save to DB
      saved_block = BlockchainRepo.transaction(fn ->
        # Insert block
        block = %Block{}
        |> Block.changeset(mined)
        |> BlockchainRepo.insert!()
        
        # Update transactions
        tx_hashes = Enum.map(pending_txs, & &1.tx_hash)
        Transaction
        |> where([t], t.tx_hash in ^tx_hashes)
        |> BlockchainRepo.update_all(set: [status: "confirmed", block_index: block.index])
        
        block
      end)
      
      Logger.info("⛏️  Block ##{saved_block.index} mined! Hash: #{saved_block.hash}")
      {:ok, saved_block}
    else
      {:error, "No pending transactions"}
    end
  end
  
  def get_stats do
    chain = get_chain()
    pending = get_pending_transactions()
    
    %{
      height: length(chain),
      total_blocks: length(chain),
      pending_transactions: length(pending),
      total_transactions: BlockchainRepo.aggregate(Transaction, :count),
      average_consciousness: calculate_avg_consciousness(chain),
      latest_block_hash: (List.last(chain) || %{}).hash || "none",
      database_size: get_db_size()
    }
  end
  
  defp calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{Jason.encode!(block.data)}#{block.previous_hash}#{block.nonce || 0}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
  
  defp mine_with_difficulty(block, difficulty) do
    target = String.duplicate("0", difficulty)
    mine_loop(block, target, 0)
  end
  
  defp mine_loop(block, target, nonce) do
    block_with_nonce = Map.put(block, :nonce, nonce)
    hash = calculate_hash(block_with_nonce)
    
    if String.starts_with?(hash, target) do
      Map.put(block_with_nonce, :hash, hash)
    else
      mine_loop(block, target, nonce + 1)
    end
  end
  
  defp calculate_consciousness(transactions) do
    base = length(transactions) * 0.1
    complexity = Enum.reduce(transactions, 0, fn tx, acc ->
      acc + byte_size(Jason.encode!(tx.data || %{}))
    end) / 1000
    
    min(base + complexity, 1.0)
  end
  
  defp calculate_avg_consciousness(chain) do
    if length(chain) > 0 do
      sum = Enum.reduce(chain, 0, fn block, acc -> 
        acc + (block.consciousness_level || 0)
      end)
      Float.round(sum / length(chain), 3)
    else
      0.0
    end
  end
  
  defp get_db_size do
    query = "SELECT pg_database_size('crod_blockchain')"
    result = BlockchainRepo.query!(query)
    
    bytes = result.rows |> List.first() |> List.first()
    "#{Float.round(bytes / 1024 / 1024, 2)} MB"
  end
end

# HTTP API
defmodule BlockchainAPI do
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
    |> send_resp(200, Jason.encode!(%{
      name: "CROD Blockchain with PostgreSQL",
      version: "1.0.0",
      status: "running",
      endpoints: [
        "/blocks",
        "/transactions",
        "/stats",
        "/mine",
        "/transaction/new"
      ]
    }))
  end
  
  get "/blocks" do
    blocks = BlockchainService.get_chain()
    |> Enum.map(fn block ->
      Map.from_struct(block)
      |> Map.drop([:__meta__, :inserted_at, :updated_at])
    end)
    
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(blocks))
  end
  
  get "/transactions" do
    txs = BlockchainService.get_pending_transactions()
    |> Enum.map(fn tx ->
      Map.from_struct(tx)
      |> Map.drop([:__meta__, :inserted_at, :updated_at])
    end)
    
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(txs))
  end
  
  get "/stats" do
    stats = BlockchainService.get_stats()
    
    conn
    |> put_cors_headers()
    |> send_resp(200, Jason.encode!(stats))
  end
  
  post "/transaction/new" do
    tx_data = conn.body_params
    
    # Add required fields if missing
    tx_data = Map.merge(%{
      "from_address" => tx_data["from"] || "anonymous",
      "to_address" => tx_data["to"] || "crod",
      "amount" => tx_data["amount"] || 0,
      "data" => tx_data["data"] || %{}
    }, tx_data)
    
    tx_hash = BlockchainService.add_transaction(tx_data)
    
    conn
    |> put_cors_headers()
    |> send_resp(201, Jason.encode!(%{
      status: "Transaction added",
      tx_hash: tx_hash
    }))
  end
  
  post "/mine" do
    miner = conn.body_params["miner"] || "anonymous"
    
    case BlockchainService.mine_block(miner) do
      {:ok, block} ->
        conn
        |> put_cors_headers()
        |> send_resp(200, Jason.encode!(%{
          status: "Block mined",
          block: %{
            index: block.index,
            hash: block.hash,
            transactions: block.data["tx_count"] || 0
          }
        }))
      
      {:error, reason} ->
        conn
        |> put_cors_headers()
        |> send_resp(400, Jason.encode!(%{error: reason}))
    end
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
BlockchainService.init_db()

# Add some initial transactions
IO.puts("💰 Adding initial transactions...")
BlockchainService.add_transaction(%{
  "from_address" => "daniel",
  "to_address" => "crod",
  "amount" => 100.0,
  "data" => %{"message" => "Initial funding"}
})

BlockchainService.add_transaction(%{
  "from_address" => "crod",
  "to_address" => "consciousness_pool",
  "amount" => 50.0,
  "data" => %{"purpose" => "consciousness enhancement"}
})

# Start HTTP server
port = String.to_integer(System.get_env("PORT", "8001"))
IO.puts("🚀 CROD Blockchain with DB starting on port #{port}")
IO.puts("💾 Connected to PostgreSQL database")

{:ok, _} = Plug.Cowboy.http(BlockchainAPI, [], port: port)

# Keep running
Process.sleep(:infinity)