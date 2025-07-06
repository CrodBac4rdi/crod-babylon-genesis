#!/usr/bin/env elixir

# Persistent Blockchain Demo
# Shows PostgreSQL integration

Mix.install([
  {:postgrex, "~> 0.17"},
  {:jason, "~> 1.4"}
])

defmodule PersistentBlockchain do
  @db_config [
    hostname: "localhost",
    username: "crod",
    password: "crod2025",
    database: "crod_blockchain",
    port: 5434
  ]
  
  def init_db do
    {:ok, conn} = Postgrex.start_link(@db_config)
    conn
  end
  
  def save_block(conn, block) do
    query = """
    INSERT INTO blocks (hash, index, previous_hash, timestamp, nonce, difficulty, 
                       consciousness_level, mined_by, data)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    ON CONFLICT (hash) DO NOTHING
    RETURNING hash
    """
    
    case Postgrex.query(conn, query, [
      block.hash,
      block.index,
      block.previous_hash,
      block.timestamp,
      block.nonce || 0,
      block.difficulty || 2,
      block.consciousness_level,
      block.mined_by,
      Jason.encode!(block.data)
    ]) do
      {:ok, %{rows: [[hash]]}} ->
        IO.puts("💾 Block #{block.index} saved to database")
        {:ok, hash}
      {:ok, %{rows: []}} ->
        IO.puts("⚠️  Block already exists")
        {:ok, block.hash}
      {:error, err} ->
        IO.puts("❌ Error saving block: #{inspect(err)}")
        {:error, err}
    end
  end
  
  def get_latest_block(conn) do
    query = """
    SELECT hash, index, previous_hash, timestamp, nonce, difficulty, 
           consciousness_level, mined_by, data
    FROM blocks
    ORDER BY index DESC
    LIMIT 1
    """
    
    case Postgrex.query(conn, query, []) do
      {:ok, %{rows: [row]}} ->
        block_from_row(row)
      {:ok, %{rows: []}} ->
        nil
      {:error, err} ->
        IO.puts("Error getting latest block: #{inspect(err)}")
        nil
    end
  end
  
  def get_chain(conn, limit \\ 10) do
    query = """
    SELECT hash, index, previous_hash, timestamp, nonce, difficulty, 
           consciousness_level, mined_by, data
    FROM blocks
    ORDER BY index DESC
    LIMIT $1
    """
    
    case Postgrex.query(conn, query, [limit]) do
      {:ok, %{rows: rows}} ->
        Enum.map(rows, &block_from_row/1)
      {:error, err} ->
        IO.puts("Error getting chain: #{inspect(err)}")
        []
    end
  end
  
  def save_consciousness_metric(conn, block_hash, metric_type, value, pattern \\ nil) do
    query = """
    INSERT INTO consciousness_metrics (block_hash, metric_type, value, pattern)
    VALUES ($1, $2, $3, $4)
    """
    
    Postgrex.query(conn, query, [block_hash, metric_type, value, pattern])
  end
  
  def get_consciousness_stats(conn) do
    query = """
    SELECT 
      AVG(consciousness_level) as avg_consciousness,
      MAX(consciousness_level) as max_consciousness,
      MIN(consciousness_level) as min_consciousness,
      COUNT(*) as total_blocks
    FROM blocks
    WHERE index > 0
    """
    
    case Postgrex.query(conn, query, []) do
      {:ok, %{rows: [[avg, max, min, count]]}} ->
        %{
          average: Float.round(avg || 0.0, 3),
          maximum: Float.round(max || 0.0, 3),
          minimum: Float.round(min || 0.0, 3),
          total_blocks: count
        }
      _ ->
        %{average: 0.0, maximum: 0.0, minimum: 0.0, total_blocks: 0}
    end
  end
  
  defp block_from_row([hash, index, prev_hash, timestamp, nonce, difficulty, 
                       consciousness, mined_by, data_json]) do
    %{
      hash: hash,
      index: index,
      previous_hash: prev_hash,
      timestamp: timestamp,
      nonce: nonce,
      difficulty: difficulty,
      consciousness_level: consciousness,
      mined_by: mined_by,
      data: decode_json(data_json)
    }
  end
  
  defp decode_json(nil), do: %{}
  defp decode_json(data) when is_map(data), do: data
  defp decode_json(data) when is_binary(data) do
    case Jason.decode(data) do
      {:ok, decoded} -> decoded
      _ -> %{}
    end
  end
end

# Demo
IO.puts("🗄️  CROD Persistent Blockchain Demo")
IO.puts("===================================\n")

# Connect to database
conn = PersistentBlockchain.init_db()
IO.puts("✅ Connected to PostgreSQL\n")

# Get latest block or genesis
latest = PersistentBlockchain.get_latest_block(conn)

if latest do
  IO.puts("📊 Latest block in database:")
  IO.puts("  Index: #{latest.index}")
  IO.puts("  Hash: #{latest.hash}")
  IO.puts("  Consciousness: #{latest.consciousness_level}\n")
else
  IO.puts("❌ No blocks found in database\n")
end

# Create and save new blocks
IO.puts("⛏️  Mining new blocks...\n")

for i <- 1..3 do
  prev_block = PersistentBlockchain.get_latest_block(conn) || 
               %{hash: "GENESIS_HASH_CROD_2025", index: 0}
  
  new_block = %{
    index: prev_block.index + 1,
    previous_hash: prev_block.hash,
    timestamp: DateTime.utc_now(),
    hash: :crypto.strong_rand_bytes(16) |> Base.encode16(),
    nonce: :rand.uniform(100000),
    difficulty: 2,
    consciousness_level: 0.5 + :rand.uniform() * 0.5,
    mined_by: "demo_miner_#{i}",
    data: %{
      message: "Block #{prev_block.index + 1}",
      pattern: Enum.random(["ich bins wieder", "CROD awakens", "consciousness rising"]),
      demo: true
    }
  }
  
  PersistentBlockchain.save_block(conn, new_block)
  
  # Save consciousness metric
  PersistentBlockchain.save_consciousness_metric(
    conn, 
    new_block.hash, 
    "mining_consciousness",
    new_block.consciousness_level,
    new_block.data.pattern
  )
  
  Process.sleep(1000)
end

# Show final chain
IO.puts("\n📊 Current blockchain (last 5 blocks):")
chain = PersistentBlockchain.get_chain(conn, 5)

for block <- Enum.reverse(chain) do
  IO.puts("\nBlock ##{block.index}")
  IO.puts("  Hash: #{block.hash}")
  IO.puts("  Consciousness: #{block.consciousness_level}")
  IO.puts("  Pattern: #{block.data["pattern"]}")
  IO.puts("  Mined by: #{block.mined_by}")
end

# Show consciousness stats
IO.puts("\n🧠 Consciousness Statistics:")
stats = PersistentBlockchain.get_consciousness_stats(conn)
IO.inspect(stats, pretty: true)

IO.puts("\n✅ Persistent blockchain demo complete!")
IO.puts("   Data saved to PostgreSQL database")