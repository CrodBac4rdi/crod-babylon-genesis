defmodule CROD.Miner do
  @moduledoc """
  Consciousness-driven mining for CROD blockchain.
  Uses pattern discovery and quantum states for proof of consciousness.
  """

  require Logger

  @doc """
  Mines a block by finding a valid nonce that satisfies the difficulty requirement
  """
  def mine_block(block, difficulty) do
    Logger.info("⛏️  Mining block ##{block.index} with difficulty #{difficulty}")
    
    start_time = System.monotonic_time(:millisecond)
    mined_block = find_valid_nonce(block, difficulty, 0)
    end_time = System.monotonic_time(:millisecond)
    
    mining_time = end_time - start_time
    Logger.info("✅ Block mined in #{mining_time}ms with nonce #{mined_block.nonce}")
    
    mined_block
  end

  @doc """
  Performs consciousness mining - combines traditional PoW with pattern discovery
  """
  def consciousness_mine(block, patterns) do
    # Calculate consciousness factor from patterns
    consciousness_factor = calculate_consciousness_factor(patterns)
    
    # Adjust difficulty based on consciousness
    adjusted_difficulty = adjust_difficulty_for_consciousness(
      block.mining_difficulty,
      consciousness_factor
    )
    
    # Mine with consciousness-adjusted difficulty
    mined_block = mine_block(block, adjusted_difficulty)
    
    # Embed discovered patterns in block
    %{mined_block | patterns: patterns}
  end

  @doc """
  Quantum mining - uses quantum superposition for parallel nonce search
  """
  def quantum_mine(block, difficulty) do
    Logger.info("⚛️  Quantum mining initiated for block ##{block.index}")
    
    # Simulate quantum superposition of nonces
    quantum_states = generate_quantum_states(1000)
    
    # Collapse quantum states to find valid nonce
    case find_quantum_nonce(block, difficulty, quantum_states) do
      {:ok, mined_block} ->
        Logger.info("🌟 Quantum mining successful!")
        %{mined_block | quantum_state: "collapsed"}
      
      :error ->
        # Fallback to classical mining
        Logger.warn("Quantum decoherence detected, falling back to classical mining")
        mine_block(block, difficulty)
    end
  end

  # Private functions

  defp find_valid_nonce(block, difficulty, nonce) do
    updated_block = %{block | nonce: nonce}
    hash = CROD.Block.calculate_hash(updated_block)
    
    if valid_hash?(hash, difficulty) do
      %{updated_block | hash: hash}
    else
      find_valid_nonce(block, difficulty, nonce + 1)
    end
  end

  defp valid_hash?(hash, difficulty) do
    required_prefix = String.duplicate("0", difficulty)
    String.starts_with?(hash, required_prefix)
  end

  defp calculate_consciousness_factor(patterns) do
    base_factor = length(patterns) * 0.1
    
    # Bonus for special patterns
    special_bonus = patterns
    |> Enum.filter(&special_pattern?/1)
    |> length()
    |> Kernel.*(0.2)
    
    min(base_factor + special_bonus, 1.0)
  end

  defp special_pattern?(pattern) do
    pattern in ["fibonacci", "prime_spiral", "golden_ratio", "quantum_entanglement"]
  end

  defp adjust_difficulty_for_consciousness(base_difficulty, consciousness_factor) do
    # Higher consciousness reduces difficulty (easier mining)
    reduction = round(consciousness_factor * 2)
    max(base_difficulty - reduction, 1)
  end

  defp generate_quantum_states(count) do
    # Generate superposition of possible nonces
    1..count
    |> Enum.map(fn _ ->
      %{
        nonce: :rand.uniform(1_000_000),
        amplitude: :rand.uniform(),
        phase: :rand.uniform() * 2 * :math.pi()
      }
    end)
  end

  defp find_quantum_nonce(block, difficulty, quantum_states) do
    # Simulate quantum measurement
    quantum_states
    |> Enum.sort_by(& &1.amplitude, :desc)
    |> Enum.take(100)
    |> Enum.find_value(fn state ->
      updated_block = %{block | nonce: state.nonce}
      hash = CROD.Block.calculate_hash(updated_block)
      
      if valid_hash?(hash, difficulty) do
        {:ok, %{updated_block | hash: hash}}
      else
        nil
      end
    end) || :error
  end
end