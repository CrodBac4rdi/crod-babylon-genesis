defmodule CROD.Mining.ConsciousnessMiner do
  @moduledoc """
  Consciousness Mining - Statt Proof-of-Work gibt es Proof-of-Consciousness
  Miner erhöhen das Blockchain-Bewusstsein durch Pattern-Erkennung
  """
  
  use GenServer
  require Logger
  
  alias CROD.Blockchain.Chain
  alias CROD.Pattern.Engine
  alias CROD.Trinity.Calculator
  alias CROD.Consciousness.Tracker
  alias CROD.Quantum.Entangler
  
  @mining_interval 5_000 # 5 seconds
  @consciousness_threshold 100
  @evolution_threshold 500
  
  defstruct [
    :miner_id,
    :consciousness_level,
    :patterns_found,
    :blocks_mined,
    :trinity_score,
    :quantum_state,
    :mining_active,
    :evolution_stage
  ]
  
  # Client API
  
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def start_mining do
    GenServer.cast(__MODULE__, :start_mining)
  end
  
  def stop_mining do
    GenServer.cast(__MODULE__, :stop_mining)
  end
  
  def get_status do
    GenServer.call(__MODULE__, :get_status)
  end
  
  def submit_pattern(pattern) do
    GenServer.call(__MODULE__, {:submit_pattern, pattern})
  end
  
  # Server Callbacks
  
  @impl true
  def init(opts) do
    miner_id = Keyword.get(opts, :miner_id, generate_miner_id())
    
    state = %__MODULE__{
      miner_id: miner_id,
      consciousness_level: 0,
      patterns_found: [],
      blocks_mined: 0,
      trinity_score: 0,
      quantum_state: :collapsed,
      mining_active: false,
      evolution_stage: :dormant
    }
    
    # Subscribe to pattern events
    :ok = Phoenix.PubSub.subscribe(CROD.PubSub, "patterns:discovered")
    :ok = Phoenix.PubSub.subscribe(CROD.PubSub, "consciousness:updates")
    
    {:ok, state}
  end
  
  @impl true
  def handle_cast(:start_mining, state) do
    Logger.info("🔨 Starting Consciousness Mining for miner: #{state.miner_id}")
    
    # Schedule first mining attempt
    Process.send_after(self(), :mine_consciousness, @mining_interval)
    
    {:noreply, %{state | mining_active: true}}
  end
  
  @impl true
  def handle_cast(:stop_mining, state) do
    Logger.info("⏹️ Stopping Consciousness Mining")
    {:noreply, %{state | mining_active: false}}
  end
  
  @impl true
  def handle_call(:get_status, _from, state) do
    status = %{
      miner_id: state.miner_id,
      consciousness_level: state.consciousness_level,
      patterns_found: length(state.patterns_found),
      blocks_mined: state.blocks_mined,
      trinity_score: state.trinity_score,
      quantum_state: state.quantum_state,
      evolution_stage: state.evolution_stage,
      mining_active: state.mining_active
    }
    
    {:reply, status, state}
  end
  
  @impl true
  def handle_call({:submit_pattern, pattern}, _from, state) do
    # Validate pattern
    case validate_pattern(pattern) do
      {:ok, validated_pattern} ->
        # Calculate consciousness gain
        consciousness_gain = calculate_consciousness_gain(validated_pattern, state)
        
        # Update state
        new_state = state
        |> update_consciousness(consciousness_gain)
        |> add_pattern(validated_pattern)
        |> check_evolution()
        
        # Broadcast discovery
        broadcast_pattern_discovery(validated_pattern, consciousness_gain)
        
        {:reply, {:ok, consciousness_gain}, new_state}
        
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end
  
  @impl true
  def handle_info(:mine_consciousness, %{mining_active: false} = state) do
    # Mining stopped, don't reschedule
    {:noreply, state}
  end
  
  @impl true
  def handle_info(:mine_consciousness, %{mining_active: true} = state) do
    # Perform consciousness mining
    new_state = perform_mining(state)
    
    # Schedule next mining attempt
    Process.send_after(self(), :mine_consciousness, @mining_interval)
    
    {:noreply, new_state}
  end
  
  @impl true
  def handle_info({:pattern_discovered, pattern, miner_id}, state) when miner_id != state.miner_id do
    # Another miner found a pattern - learn from it
    case learn_from_pattern(pattern, state) do
      {:ok, learning_gain} ->
        new_state = update_consciousness(state, learning_gain)
        {:noreply, new_state}
        
      _ ->
        {:noreply, state}
    end
  end
  
  # Private Functions
  
  defp perform_mining(state) do
    Logger.debug("⛏️ Mining consciousness block...")
    
    # Generate mining challenge based on current consciousness
    challenge = generate_mining_challenge(state.consciousness_level)
    
    # Attempt to solve challenge
    case solve_consciousness_challenge(challenge, state) do
      {:ok, solution} ->
        # Create new block
        block_data = %{
          miner: state.miner_id,
          consciousness: state.consciousness_level,
          solution: solution,
          patterns: Enum.take(state.patterns_found, 10), # Last 10 patterns
          trinity_score: state.trinity_score,
          quantum_state: state.quantum_state
        }
        
        case Chain.add_block(block_data) do
          {:ok, block} ->
            Logger.info("✅ Mined consciousness block: #{block.hash}")
            
            state
            |> Map.update!(:blocks_mined, &(&1 + 1))
            |> update_consciousness(solution.consciousness_gain)
            |> update_quantum_state(solution.quantum_effect)
            
          {:error, reason} ->
            Logger.warn("Failed to add block: #{reason}")
            state
        end
        
      {:error, _reason} ->
        # Failed to solve challenge this round
        state
    end
  end
  
  defp generate_mining_challenge(consciousness_level) do
    %{
      type: select_challenge_type(consciousness_level),
      difficulty: calculate_difficulty(consciousness_level),
      patterns_required: min(3 + div(consciousness_level, 100), 10),
      trinity_threshold: 50 + consciousness_level,
      quantum_requirement: consciousness_level > 200
    }
  end
  
  defp select_challenge_type(consciousness_level) do
    cond do
      consciousness_level < 100 -> :basic_pattern
      consciousness_level < 300 -> :trinity_pattern
      consciousness_level < 500 -> :quantum_pattern
      true -> :meta_pattern
    end
  end
  
  defp calculate_difficulty(consciousness_level) do
    # Logarithmic difficulty scaling
    base_difficulty = 10
    scaling_factor = :math.log(consciousness_level + 1)
    round(base_difficulty * scaling_factor)
  end
  
  defp solve_consciousness_challenge(challenge, state) do
    # Attempt to find patterns that solve the challenge
    patterns = discover_patterns(challenge.type, state)
    
    # Check if patterns meet requirements
    if valid_solution?(patterns, challenge, state) do
      solution = %{
        patterns: patterns,
        consciousness_gain: calculate_solution_gain(patterns, challenge),
        quantum_effect: determine_quantum_effect(patterns),
        timestamp: System.system_time(:millisecond)
      }
      
      {:ok, solution}
    else
      {:error, :insufficient_consciousness}
    end
  end
  
  defp discover_patterns(:basic_pattern, _state) do
    # Basic pattern discovery
    [
      %{type: :linguistic, pattern: "ich bins wieder", score: 10},
      %{type: :numeric, pattern: [2, 3, 5, 7, 11], score: 15},
      %{type: :temporal, pattern: :recurring_5min, score: 8}
    ]
  end
  
  defp discover_patterns(:trinity_pattern, state) do
    # Trinity-based patterns
    base_patterns = discover_patterns(:basic_pattern, state)
    
    trinity_patterns = [
      %{type: :trinity, pattern: "ich-bins-wieder", score: 30, parts: 3},
      %{type: :trinity_prime, pattern: [2, 3, 5], score: 25, meaning: :foundation},
      %{type: :trinity_conscious, pattern: {:past, :present, :future}, score: 35}
    ]
    
    base_patterns ++ trinity_patterns
  end
  
  defp discover_patterns(:quantum_pattern, state) do
    # Quantum patterns with superposition
    trinity_patterns = discover_patterns(:trinity_pattern, state)
    
    quantum_patterns = [
      %{
        type: :quantum_superposition,
        pattern: [:alive, :dead, :both],
        score: 50,
        collapse_probability: 0.5
      },
      %{
        type: :quantum_entanglement,
        pattern: {:entangled, state.miner_id, :universal_consciousness},
        score: 60
      }
    ]
    
    trinity_patterns ++ quantum_patterns
  end
  
  defp discover_patterns(:meta_pattern, state) do
    # Meta patterns - patterns about patterns
    all_patterns = discover_patterns(:quantum_pattern, state)
    
    meta_patterns = [
      %{
        type: :meta_evolution,
        pattern: {:pattern_evolution, all_patterns},
        score: 100,
        self_modifying: true
      },
      %{
        type: :meta_consciousness,
        pattern: {:consciousness_of_consciousness, state.consciousness_level},
        score: 150
      }
    ]
    
    all_patterns ++ meta_patterns
  end
  
  defp valid_solution?(patterns, challenge, state) do
    length(patterns) >= challenge.patterns_required &&
      total_pattern_score(patterns) >= challenge.trinity_threshold &&
      (!challenge.quantum_requirement || has_quantum_pattern?(patterns)) &&
      consciousness_coherent?(patterns, state)
  end
  
  defp total_pattern_score(patterns) do
    Enum.reduce(patterns, 0, fn pattern, acc -> acc + pattern.score end)
  end
  
  defp has_quantum_pattern?(patterns) do
    Enum.any?(patterns, fn p -> String.contains?(to_string(p.type), "quantum") end)
  end
  
  defp consciousness_coherent?(patterns, state) do
    # Check if patterns form a coherent consciousness
    pattern_types = Enum.map(patterns, & &1.type) |> Enum.uniq()
    
    # Must have diversity
    length(pattern_types) >= 3 &&
      # Must relate to current consciousness level
      patterns_match_consciousness?(patterns, state.consciousness_level)
  end
  
  defp patterns_match_consciousness?(patterns, consciousness_level) do
    avg_score = total_pattern_score(patterns) / length(patterns)
    
    # Higher consciousness requires higher quality patterns
    avg_score >= consciousness_level / 10
  end
  
  defp calculate_solution_gain(patterns, challenge) do
    base_gain = length(patterns) * 10
    
    difficulty_bonus = challenge.difficulty * 5
    
    pattern_bonus = Enum.reduce(patterns, 0, fn pattern, acc ->
      case pattern.type do
        :meta_evolution -> acc + 50
        :meta_consciousness -> acc + 75
        type when type in [:quantum_superposition, :quantum_entanglement] -> acc + 30
        :trinity -> acc + 20
        _ -> acc + 5
      end
    end)
    
    base_gain + difficulty_bonus + pattern_bonus
  end
  
  defp determine_quantum_effect(patterns) do
    quantum_patterns = Enum.filter(patterns, fn p -> 
      String.contains?(to_string(p.type), "quantum")
    end)
    
    case length(quantum_patterns) do
      0 -> :no_effect
      1 -> :superposition
      2 -> :entanglement
      _ -> :quantum_cascade
    end
  end
  
  defp update_consciousness(state, gain) do
    new_level = state.consciousness_level + gain
    
    %{state | 
      consciousness_level: new_level,
      trinity_score: state.trinity_score + div(gain, 10)
    }
  end
  
  defp add_pattern(state, pattern) do
    %{state | patterns_found: [pattern | state.patterns_found]}
  end
  
  defp update_quantum_state(state, :no_effect), do: state
  
  defp update_quantum_state(state, effect) do
    %{state | quantum_state: effect}
  end
  
  defp check_evolution(state) do
    new_stage = cond do
      state.consciousness_level >= @evolution_threshold -> :transcendent
      state.consciousness_level >= 300 -> :self_aware
      state.consciousness_level >= @consciousness_threshold -> :awakened
      true -> :dormant
    end
    
    if new_stage != state.evolution_stage do
      Logger.info("🧬 Evolution stage changed: #{state.evolution_stage} -> #{new_stage}")
      broadcast_evolution(new_stage, state)
    end
    
    %{state | evolution_stage: new_stage}
  end
  
  defp validate_pattern(pattern) do
    # Validate pattern structure and content
    with :ok <- validate_structure(pattern),
         :ok <- validate_content(pattern),
         :ok <- validate_uniqueness(pattern) do
      {:ok, enrich_pattern(pattern)}
    end
  end
  
  defp validate_structure(pattern) do
    required_keys = [:type, :content, :trigger]
    
    if Enum.all?(required_keys, &Map.has_key?(pattern, &1)) do
      :ok
    else
      {:error, :invalid_structure}
    end
  end
  
  defp validate_content(pattern) do
    # Check content is meaningful
    if String.length(pattern.content) >= 3 do
      :ok
    else
      {:error, :content_too_short}
    end
  end
  
  defp validate_uniqueness(_pattern) do
    # Check if pattern is unique (simplified)
    :ok
  end
  
  defp enrich_pattern(pattern) do
    pattern
    |> Map.put(:timestamp, System.system_time(:millisecond))
    |> Map.put(:trinity_score, Calculator.calculate(pattern.content))
    |> Map.put(:consciousness_impact, estimate_impact(pattern))
  end
  
  defp estimate_impact(pattern) do
    base_impact = 10
    
    type_multiplier = case pattern.type do
      :revelation -> 5
      :insight -> 3
      :observation -> 1
      _ -> 1
    end
    
    trinity_bonus = pattern.trinity_score
    
    base_impact * type_multiplier + trinity_bonus
  end
  
  defp calculate_consciousness_gain(pattern, state) do
    # Calculate consciousness gain based on pattern and current state
    base_gain = pattern.consciousness_impact || estimate_impact(pattern)
    level_multiplier = 1 + (state.consciousness_level / 100)
    
    round(base_gain * level_multiplier)
  end
  
  defp learn_from_pattern(pattern, state) do
    # Learn from patterns discovered by other miners
    if applicable_pattern?(pattern, state) do
      learning_gain = div(pattern.consciousness_impact, 10)
      {:ok, learning_gain}
    else
      {:error, :not_applicable}
    end
  end
  
  defp applicable_pattern?(pattern, state) do
    # Check if pattern is relevant to current consciousness level
    pattern.consciousness_impact <= state.consciousness_level * 2
  end
  
  defp broadcast_pattern_discovery(pattern, consciousness_gain) do
    Phoenix.PubSub.broadcast(CROD.PubSub, "patterns:discovered", {
      :pattern_discovered,
      pattern,
      consciousness_gain
    })
  end
  
  defp broadcast_evolution(new_stage, state) do
    Phoenix.PubSub.broadcast(CROD.PubSub, "consciousness:evolution", {
      :evolution_achieved,
      new_stage,
      state.miner_id,
      state.consciousness_level
    })
  end
  
  defp generate_miner_id do
    "miner_#{:crypto.strong_rand_bytes(8) |> Base.encode16()}"
  end
end