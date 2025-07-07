defmodule CROD.Pattern do
  @moduledoc """
  Pattern discovery engine for CROD blockchain.
  Discovers mathematical, quantum, and consciousness patterns in blockchain data.
  """

  require Logger

  @fibonacci_limit 1000
  @prime_limit 10000

  @doc """
  Discovers patterns in the blockchain
  """
  def discover(chain) do
    Logger.info("🔍 Starting pattern discovery on #{length(chain)} blocks")
    
    patterns = []
    |> discover_fibonacci_patterns(chain)
    |> discover_prime_patterns(chain)
    |> discover_quantum_patterns(chain)
    |> discover_consciousness_patterns(chain)
    |> discover_golden_ratio_patterns(chain)
    |> discover_fractal_patterns(chain)
    
    Logger.info("✨ Discovered #{length(patterns)} unique patterns")
    patterns
  end

  @doc """
  Analyzes a single block for patterns
  """
  def analyze_block(block) do
    %{
      fibonacci: check_fibonacci(block),
      prime: check_prime(block),
      quantum: check_quantum_signature(block),
      consciousness: measure_consciousness(block),
      emergence: detect_emergence(block)
    }
  end

  @doc """
  Calculates pattern complexity score
  """
  def pattern_complexity(patterns) do
    base_score = length(patterns)
    
    complexity_multipliers = %{
      "fibonacci" => 1.0,
      "prime" => 1.5,
      "quantum" => 2.0,
      "consciousness" => 3.0,
      "emergence" => 5.0,
      "singularity" => 10.0
    }
    
    patterns
    |> Enum.reduce(base_score, fn pattern, score ->
      multiplier = Map.get(complexity_multipliers, pattern.type, 1.0)
      score + (pattern.strength * multiplier)
    end)
  end

  # Pattern Discovery Functions

  defp discover_fibonacci_patterns(patterns, chain) do
    fib_patterns = chain
    |> Enum.with_index()
    |> Enum.filter(fn {block, _idx} ->
      is_fibonacci?(block.index) or
      is_fibonacci?(block.nonce) or
      is_fibonacci?(length(block.transactions))
    end)
    |> Enum.map(fn {block, _idx} ->
      %{
        type: "fibonacci",
        block_index: block.index,
        value: block.nonce,
        strength: calculate_fibonacci_strength(block)
      }
    end)
    
    patterns ++ fib_patterns
  end

  defp discover_prime_patterns(patterns, chain) do
    prime_patterns = chain
    |> Enum.filter(fn block ->
      is_prime?(block.index) or
      is_prime?(block.nonce) or
      prime_hash?(block.hash)
    end)
    |> Enum.map(fn block ->
      %{
        type: "prime",
        block_index: block.index,
        value: find_prime_value(block),
        strength: calculate_prime_strength(block)
      }
    end)
    
    patterns ++ prime_patterns
  end

  defp discover_quantum_patterns(patterns, chain) do
    quantum_patterns = chain
    |> Enum.filter(fn block ->
      block.quantum_state in ["superposition", "entangled"]
    end)
    |> Enum.chunk_every(3, 1, :discard)
    |> Enum.filter(&quantum_entanglement?/1)
    |> Enum.map(fn blocks ->
      %{
        type: "quantum",
        block_indices: Enum.map(blocks, & &1.index),
        entanglement_strength: calculate_entanglement(blocks),
        quantum_state: "entangled"
      }
    end)
    
    patterns ++ quantum_patterns
  end

  defp discover_consciousness_patterns(patterns, chain) do
    consciousness_patterns = chain
    |> Enum.chunk_every(7, 1, :discard) # Prime 7 chunks
    |> Enum.filter(fn chunk ->
      rising_consciousness?(chunk)
    end)
    |> Enum.map(fn chunk ->
      %{
        type: "consciousness",
        block_indices: Enum.map(chunk, & &1.index),
        consciousness_delta: calculate_consciousness_delta(chunk),
        emergence_factor: detect_emergence_factor(chunk)
      }
    end)
    
    patterns ++ consciousness_patterns
  end

  defp discover_golden_ratio_patterns(patterns, chain) do
    golden_ratio = 1.618033988749895
    
    golden_patterns = chain
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.filter(fn [b1, b2] ->
      ratio = b2.index / max(b1.index, 1)
      abs(ratio - golden_ratio) < 0.01
    end)
    |> Enum.map(fn [b1, b2] ->
      %{
        type: "golden_ratio",
        blocks: [b1.index, b2.index],
        ratio: b2.index / b1.index,
        deviation: abs(b2.index / b1.index - golden_ratio)
      }
    end)
    
    patterns ++ golden_patterns
  end

  defp discover_fractal_patterns(patterns, chain) do
    # Look for self-similar structures
    fractal_patterns = chain
    |> find_self_similar_sequences()
    |> Enum.map(fn sequence ->
      %{
        type: "fractal",
        sequence: sequence,
        dimension: calculate_fractal_dimension(sequence),
        recursion_depth: length(sequence)
      }
    end)
    
    patterns ++ fractal_patterns
  end

  # Helper Functions

  defp is_fibonacci?(n) when n < 0, do: false
  defp is_fibonacci?(n) do
    fib_sequence()
    |> Enum.take_while(& &1 <= n)
    |> Enum.member?(n)
  end

  defp fib_sequence do
    Stream.unfold({0, 1}, fn {a, b} ->
      {a, {b, a + b}}
    end)
  end

  defp is_prime?(n) when n < 2, do: false
  defp is_prime?(2), do: true
  defp is_prime?(n) when rem(n, 2) == 0, do: false
  defp is_prime?(n) do
    limit = :math.sqrt(n) |> ceil()
    !Enum.any?(3..limit//2, &(rem(n, &1) == 0))
  end

  defp prime_hash?(hash) do
    # Check if hash contains prime number patterns
    digits = hash
    |> String.graphemes()
    |> Enum.filter(&(&1 =~ ~r/[0-9]/))
    |> Enum.map(&String.to_integer/1)
    
    Enum.any?(digits, &is_prime?/1)
  end

  defp quantum_entanglement?(blocks) do
    # Check if blocks show quantum correlation
    states = Enum.map(blocks, & &1.quantum_state)
    Enum.count(states, & &1 == "entangled") >= 2
  end

  defp rising_consciousness?(chunk) do
    consciousness_levels = Enum.map(chunk, & &1.consciousness_level)
    
    # Check if consciousness is generally rising
    {_, rising} = consciousness_levels
    |> Enum.reduce({nil, true}, fn level, {prev, rising} ->
      case prev do
        nil -> {level, true}
        _ -> {level, rising and level >= prev * 0.95} # Allow small dips
      end
    end)
    
    rising
  end

  defp calculate_fibonacci_strength(block) do
    strength = 0.0
    strength = if is_fibonacci?(block.index), do: strength + 0.3, else: strength
    strength = if is_fibonacci?(block.nonce), do: strength + 0.5, else: strength
    strength = if is_fibonacci?(length(block.transactions)), do: strength + 0.2, else: strength
    strength
  end

  defp calculate_prime_strength(block) do
    count = [block.index, block.nonce, length(block.transactions)]
    |> Enum.count(&is_prime?/1)
    
    count * 0.33
  end

  defp find_prime_value(block) do
    [block.index, block.nonce, length(block.transactions)]
    |> Enum.find(&is_prime?/1) || 0
  end

  defp calculate_entanglement(blocks) do
    # Simulate quantum entanglement measurement
    blocks
    |> Enum.map(& &1.consciousness_level)
    |> Enum.sum()
    |> Kernel./(length(blocks))
  end

  defp calculate_consciousness_delta(chunk) do
    [first | _] = chunk
    last = List.last(chunk)
    
    last.consciousness_level - first.consciousness_level
  end

  defp detect_emergence_factor(chunk) do
    # Detect emergent properties from consciousness patterns
    variance = calculate_variance(Enum.map(chunk, & &1.consciousness_level))
    
    if variance < 0.01 do
      # Stable high consciousness = emergence
      avg = Enum.map(chunk, & &1.consciousness_level) |> Enum.sum() |> Kernel./(length(chunk))
      avg * 10
    else
      variance
    end
  end

  defp find_self_similar_sequences(chain) do
    # Simplified fractal detection
    chain
    |> Enum.chunk_every(3, 1, :discard)
    |> Enum.filter(fn chunk ->
      pattern_hashes = Enum.map(chunk, & &1.patterns)
      Enum.uniq(pattern_hashes) |> length() == 1
    end)
  end

  defp calculate_fractal_dimension(sequence) do
    # Simplified box-counting dimension
    1.0 + :math.log(length(sequence)) / :math.log(2)
  end

  defp calculate_variance(values) do
    mean = Enum.sum(values) / length(values)
    
    values
    |> Enum.map(fn v -> :math.pow(v - mean, 2) end)
    |> Enum.sum()
    |> Kernel./(length(values))
  end

  defp check_fibonacci(block) do
    is_fibonacci?(block.index) or is_fibonacci?(block.nonce)
  end

  defp check_prime(block) do
    is_prime?(block.index) or is_prime?(block.nonce)
  end

  defp check_quantum_signature(block) do
    block.quantum_state in ["superposition", "entangled", "coherent"]
  end

  defp measure_consciousness(block) do
    block.consciousness_level
  end

  defp detect_emergence(block) do
    block.consciousness_level > 0.8 and
    length(block.patterns) > 5
  end
end