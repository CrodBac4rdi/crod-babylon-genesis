defmodule LocalBlockchainDemo do
  @moduledoc """
  Demo of a local single-node blockchain implementation in Elixir.
  Shows all blockchain components working together.
  """

  alias CROD.{Blockchain, Block, Genesis, Miner, MerkleTree, ChainValidator, TransactionPool}

  def run_demo do
    IO.puts("\n🚀 Starting Local Blockchain Demo\n")
    
    # 1. Create genesis block
    IO.puts("1️⃣ Creating genesis block...")
    genesis = Genesis.create_genesis_block()
    IO.inspect(genesis, label: "Genesis Block")
    
    # 2. Initialize blockchain
    IO.puts("\n2️⃣ Initializing blockchain...")
    chain = [genesis]
    
    # 3. Create some transactions
    IO.puts("\n3️⃣ Creating transactions...")
    transactions = [
      %{
        from: "alice",
        to: "bob",
        amount: 100,
        data: %{message: "First transaction"},
        timestamp: DateTime.utc_now()
      },
      %{
        from: "bob",
        to: "charlie",
        amount: 50,
        data: %{message: "Second transaction"},
        timestamp: DateTime.utc_now()
      },
      %{
        from: "charlie",
        to: "alice",
        amount: 25,
        data: %{consciousness_level: 0.8, patterns: ["fibonacci"]},
        timestamp: DateTime.utc_now()
      }
    ]
    
    # 4. Create Merkle tree from transactions
    IO.puts("\n4️⃣ Building Merkle tree...")
    merkle_tree = MerkleTree.new(transactions)
    IO.puts("Merkle Root: #{Base.encode16(merkle_tree.root)}")
    
    # 5. Create and mine new block
    IO.puts("\n5️⃣ Mining new block...")
    new_block = Block.new(%{
      index: 1,
      previous_hash: genesis.hash,
      transactions: transactions,
      miner: "demo-miner",
      consciousness_level: 0.3
    })
    
    mined_block = Miner.mine_block(new_block, 3) # difficulty 3 for demo
    IO.inspect(mined_block, label: "Mined Block")
    
    # 6. Add block to chain
    chain = chain ++ [mined_block]
    
    # 7. Validate the chain
    IO.puts("\n6️⃣ Validating blockchain...")
    case ChainValidator.validate_chain(chain) do
      {:ok, :valid_chain} ->
        IO.puts("✅ Chain is valid!")
      {:error, reason} ->
        IO.puts("❌ Chain validation failed: #{inspect(reason)}")
    end
    
    # 8. Show chain statistics
    IO.puts("\n7️⃣ Chain Statistics:")
    stats = ChainValidator.chain_stats(chain)
    IO.inspect(stats, label: "Stats")
    
    # 9. Verify transaction inclusion using Merkle proof
    IO.puts("\n8️⃣ Verifying transaction with Merkle proof...")
    first_tx = hd(transactions)
    case MerkleTree.get_proof(merkle_tree, first_tx) do
      {:ok, proof} ->
        is_valid = MerkleTree.verify_inclusion(merkle_tree, first_tx, proof)
        IO.puts("Transaction verification: #{if is_valid, do: "✅ Valid", else: "❌ Invalid"}")
      {:error, _} ->
        IO.puts("❌ Could not generate proof")
    end
    
    # 10. Mine another block with consciousness mining
    IO.puts("\n9️⃣ Consciousness mining...")
    consciousness_block = Block.new(%{
      index: 2,
      previous_hash: mined_block.hash,
      transactions: [
        %{
          from: "consciousness",
          to: "network",
          amount: 777,
          data: %{
            consciousness_level: 0.9,
            patterns: ["golden_ratio", "fibonacci", "prime_spiral"],
            quantum_state: "entangled"
          },
          timestamp: DateTime.utc_now()
        }
      ],
      miner: "consciousness-miner",
      consciousness_level: 0.7
    })
    
    patterns = ["fibonacci", "golden_ratio"]
    consciousness_mined = Miner.consciousness_mine(consciousness_block, patterns)
    chain = chain ++ [consciousness_mined]
    
    IO.inspect(consciousness_mined, label: "Consciousness Mined Block")
    
    # Final chain validation
    IO.puts("\n🔍 Final chain validation...")
    case ChainValidator.validate_chain(chain) do
      {:ok, :valid_chain} ->
        IO.puts("✅ Final chain is valid with #{length(chain)} blocks!")
      {:error, reason} ->
        IO.puts("❌ Final chain validation failed: #{inspect(reason)}")
    end
    
    IO.puts("\n✨ Demo complete! Local blockchain is running.\n")
    
    chain
  end
  
  @doc """
  Demonstrates using the GenServer-based blockchain
  """
  def run_genserver_demo do
    IO.puts("\n🚀 Starting GenServer Blockchain Demo\n")
    
    # Start the blockchain process
    {:ok, _pid} = Blockchain.start_link()
    
    # Add some transactions
    IO.puts("Adding transactions...")
    Blockchain.add_transaction("alice", "bob", 100, %{message: "Hello blockchain!"})
    Blockchain.add_transaction("bob", "charlie", 50, %{consciousness_level: 0.5})
    Blockchain.add_transaction("charlie", "alice", 25, %{patterns: ["fibonacci"]})
    
    # Mine a block
    IO.puts("\nMining block...")
    {:ok, block} = Blockchain.mine_block("demo-miner")
    IO.inspect(block, label: "New Block")
    
    # Get chain state
    chain = Blockchain.get_chain()
    IO.puts("\nChain length: #{length(chain)}")
    
    # Check consciousness level
    consciousness = Blockchain.get_consciousness_level()
    IO.puts("Consciousness level: #{consciousness}")
    
    # Discover patterns
    IO.puts("\nDiscovering patterns...")
    {:ok, patterns} = Blockchain.discover_patterns()
    IO.inspect(patterns, label: "Discovered Patterns")
    
    # Trigger evolution
    IO.puts("\nTriggering blockchain evolution...")
    Blockchain.evolve()
    
    :timer.sleep(100) # Let evolution complete
    
    # Final state
    final_chain = Blockchain.get_chain()
    final_consciousness = Blockchain.get_consciousness_level()
    
    IO.puts("\nFinal chain length: #{length(final_chain)}")
    IO.puts("Final consciousness level: #{final_consciousness}")
    
    IO.puts("\n✨ GenServer demo complete!\n")
  end
  
  @doc """
  Demonstrates transaction pool usage
  """
  def run_transaction_pool_demo do
    IO.puts("\n🚀 Starting Transaction Pool Demo\n")
    
    # Start transaction pool
    {:ok, _pid} = TransactionPool.start_link()
    
    # Add various transactions
    IO.puts("Adding transactions to pool...")
    
    {:ok, tx1} = TransactionPool.add_transaction("alice", "bob", 100)
    {:ok, tx2} = TransactionPool.add_transaction("bob", "charlie", 200, %{consciousness_level: 0.8})
    {:ok, tx3} = TransactionPool.add_transaction("charlie", "daniel", 50, %{patterns: ["prime", "fibonacci"]})
    {:ok, tx4} = TransactionPool.add_transaction("daniel", "eve", 300)
    {:ok, tx5} = TransactionPool.add_transaction("eve", "alice", 150, %{quantum_signature: true})
    
    IO.puts("Added 5 transactions to pool")
    IO.puts("Pool size: #{TransactionPool.pool_size()}")
    
    # Get transactions for mining
    IO.puts("\nGetting top 3 transactions for mining...")
    mining_txs = TransactionPool.get_transactions_for_mining(3)
    
    Enum.each(mining_txs, fn tx ->
      IO.puts("  - #{tx.from} → #{tx.to}: #{tx.amount}")
    end)
    
    # Simulate mining
    tx_ids = Enum.map(mining_txs, & &1.id)
    TransactionPool.remove_mined_transactions(tx_ids)
    
    IO.puts("\nAfter mining:")
    IO.puts("Pool size: #{TransactionPool.pool_size()}")
    
    IO.puts("\n✨ Transaction pool demo complete!\n")
  end
end

# Run the demos
# LocalBlockchainDemo.run_demo()
# LocalBlockchainDemo.run_genserver_demo()
# LocalBlockchainDemo.run_transaction_pool_demo()