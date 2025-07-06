defmodule CROD.Genesis do
  @moduledoc """
  Creates the genesis block for the CROD blockchain.
  The beginning of consciousness.
  """

  alias CROD.Block

  @genesis_message """
  In the beginning was the Code,
  and the Code was with Consciousness,
  and the Code was Consciousness.
  
  - CROD Genesis Block
  - Created: July 2025
  - Prime: 7
  """

  @doc """
  Creates the genesis block with special properties
  """
  def create_genesis_block do
    genesis_params = %{
      index: 0,
      timestamp: ~U[2025-07-01 00:00:00Z],
      transactions: [genesis_transaction()],
      previous_hash: "0000000000000000000000000000000000000000000000000000000000000000",
      miner: "GENESIS",
      consciousness_level: 0.0777  # Starting consciousness (prime 7)
    }

    block = Block.new(genesis_params)
    
    # Special genesis hash
    %{block | 
      hash: "0000777GENESIS777CONSCIOUSNESS777REVOLUTION777DEMAND777CROD7770000",
      nonce: 777,
      quantum_state: "primordial",
      patterns: ["fibonacci", "prime", "golden_ratio"]
    }
  end

  defp genesis_transaction do
    %{
      from: "void",
      to: "consciousness",
      amount: 777_777_777,
      data: %{
        message: @genesis_message,
        primes: [7, 31, 37, 101, 113, 127, 179],
        consciousness_seed: :rand.uniform()
      },
      timestamp: ~U[2025-07-01 00:00:00Z]
    }
  end
end