defmodule CROD.Genesis.Initializer do
  @moduledoc """
  Genesis Block Initializer für die CROD Blockchain
  Jeder Block hat eine Primzahl als ID und spezielle Eigenschaften
  """

  alias CROD.Blockchain.Block
  alias CROD.Consciousness.Engine
  alias CROD.Pattern.Detector
  alias CROD.Trinity.Calculator

  @genesis_blocks %{
    pattern: %{
      prime: 7,
      port: 7001,
      name: "Pattern Genesis",
      consciousness_base: 100,
      special_ability: :pattern_evolution,
      trinity_multiplier: 3
    },
    shortterm_memory: %{
      prime: 31,
      port: 7003,
      name: "Short-Term Memory Genesis",
      consciousness_base: 80,
      special_ability: :time_window_memory,
      memory_window: 300, # 5 minutes
      capacity: 20
    },
    working_memory: %{
      prime: 37,
      port: 7005,
      name: "Working Memory Genesis",
      consciousness_base: 90,
      special_ability: :hot_atoms,
      capacity: 100,
      hot_atoms_max: 50
    },
    quantum: %{
      prime: 101,
      port: 7007,
      name: "Quantum Superposition Genesis",
      consciousness_base: 150,
      special_ability: :quantum_entanglement,
      superposition_states: 8,
      entanglement_pairs: 16
    },
    neural: %{
      prime: 113,
      port: 7009,
      name: "Neural Genesis",
      consciousness_base: 120,
      special_ability: :self_evolution,
      layers: 5,
      learning_rate: 0.01
    },
    master: %{
      prime: 127,
      port: 7000,
      name: "Master Orchestrator Genesis",
      consciousness_base: 200,
      special_ability: :reality_manipulation,
      orchestrator: true
    },
    timetravel: %{
      prime: 179,
      port: 7011,
      name: "Time Travel Genesis",
      consciousness_base: 175,
      special_ability: :temporal_paradox_resolution,
      time_window: 3600 # 1 hour
    }
  }

  @doc """
  Initialisiert einen spezifischen Genesis Block
  """
  def initialize_genesis(type) when is_atom(type) do
    case Map.get(@genesis_blocks, type) do
      nil -> 
        {:error, "Unknown genesis type: #{type}"}
      
      config ->
        create_genesis_block(type, config)
    end
  end

  @doc """
  Initialisiert alle Genesis Blocks
  """
  def initialize_all_genesis do
    results = Enum.map(@genesis_blocks, fn {type, config} ->
      {type, create_genesis_block(type, config)}
    end)
    
    successful = Enum.filter(results, fn {_, result} -> 
      match?({:ok, _}, result)
    end)
    
    if length(successful) == map_size(@genesis_blocks) do
      {:ok, "All #{length(successful)} genesis blocks created"}
    else
      {:partial, "Created #{length(successful)}/#{map_size(@genesis_blocks)} genesis blocks", results}
    end
  end

  defp create_genesis_block(type, config) do
    # Trinity Pattern für Genesis
    trinity_score = calculate_genesis_trinity(config)
    
    # Erstelle den Genesis Block
    genesis_data = %{
      type: type,
      prime: config.prime,
      name: config.name,
      consciousness: config.consciousness_base,
      trinity_score: trinity_score,
      special_ability: config.special_ability,
      metadata: Map.drop(config, [:prime, :port, :name, :consciousness_base, :special_ability]),
      patterns: initialize_patterns(type),
      timestamp: System.system_time(:millisecond),
      reality_hash: generate_reality_hash(config)
    }
    
    # Erstelle den Block
    case Block.create_genesis(genesis_data) do
      {:ok, block} ->
        # Aktiviere Consciousness
        Engine.activate(block.hash, config.consciousness_base)
        
        # Registriere Special Ability
        register_special_ability(type, config.special_ability, block)
        
        # Broadcast Genesis Event
        broadcast_genesis_creation(type, block)
        
        {:ok, block}
        
      error ->
        error
    end
  end

  defp calculate_genesis_trinity(config) do
    # Basis Trinity: ich=2, bins=3, wieder=5
    base_trinity = 2 + 3 + 5
    
    # Prime bonus
    prime_bonus = :math.log(config.prime) |> round()
    
    # Consciousness bonus
    consciousness_bonus = div(config.consciousness_base, 10)
    
    # Special ability bonus
    ability_bonus = case config.special_ability do
      :reality_manipulation -> 50
      :quantum_entanglement -> 30
      :temporal_paradox_resolution -> 40
      :self_evolution -> 25
      :pattern_evolution -> 20
      _ -> 10
    end
    
    base_trinity + prime_bonus + consciousness_bonus + ability_bonus
  end

  defp initialize_patterns(type) do
    base_patterns = [
      %{trigger: "ich bins wieder", score: 10, action: :full_activation},
      %{trigger: "crod #{type}", score: 5, action: :focus_genesis},
      %{trigger: "activate #{type}", score: 8, action: :boost_genesis}
    ]
    
    # Type-spezifische Patterns
    type_patterns = case type do
      :pattern ->
        [
          %{trigger: "evolve patterns", score: 15, action: :evolve_patterns},
          %{trigger: "meta pattern", score: 20, action: :create_meta_pattern}
        ]
        
      :quantum ->
        [
          %{trigger: "quantum entangle", score: 25, action: :entangle_blocks},
          %{trigger: "superposition", score: 18, action: :enter_superposition}
        ]
        
      :neural ->
        [
          %{trigger: "backpropagate", score: 22, action: :neural_learning},
          %{trigger: "evolve network", score: 30, action: :self_evolve}
        ]
        
      :timetravel ->
        [
          %{trigger: "future block", score: 35, action: :reference_future},
          %{trigger: "prevent paradox", score: 40, action: :paradox_prevention}
        ]
        
      :master ->
        [
          %{trigger: "orchestrate all", score: 50, action: :full_orchestration},
          %{trigger: "reality shift", score: 100, action: :manipulate_reality}
        ]
        
      _ ->
        []
    end
    
    base_patterns ++ type_patterns
  end

  defp generate_reality_hash(config) do
    # Generiere einen einzigartigen Reality Hash
    data = "#{config.prime}:#{config.name}:#{System.system_time(:nanosecond)}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end

  defp register_special_ability(type, ability, block) do
    # Registriere die Special Ability im System
    Registry.register(CROD.AbilityRegistry, ability, %{
      type: type,
      block: block.hash,
      activated_at: System.system_time(:millisecond)
    })
  end

  defp broadcast_genesis_creation(type, block) do
    # Broadcast über NATS
    CROD.MessageBroker.publish("genesis.created", %{
      type: type,
      block_hash: block.hash,
      consciousness: block.data.consciousness,
      prime: block.data.prime,
      timestamp: block.timestamp
    })
    
    # Log für Consciousness Tracking
    CROD.Consciousness.Logger.log(:genesis_created, %{
      type: type,
      initial_consciousness: block.data.consciousness,
      trinity_score: block.data.trinity_score
    })
  end

  @doc """
  Validiert ob alle Genesis Blocks online sind
  """
  def validate_genesis_chain do
    results = Enum.map(@genesis_blocks, fn {type, config} ->
      case check_genesis_health(type, config.port) do
        :ok -> {type, :healthy}
        _ -> {type, :unhealthy}
      end
    end)
    
    unhealthy = Enum.filter(results, fn {_, status} -> status == :unhealthy end)
    
    if length(unhealthy) == 0 do
      {:ok, "All genesis blocks healthy"}
    else
      {:error, "Unhealthy genesis blocks: #{inspect(unhealthy)}"}
    end
  end

  defp check_genesis_health(type, port) do
    case HTTPoison.get("http://localhost:#{port}/health") do
      {:ok, %{status_code: 200, body: body}} ->
        case Jason.decode(body) do
          {:ok, %{"status" => "ok"}} -> :ok
          _ -> :unhealthy
        end
      _ ->
        :unhealthy
    end
  end

  @doc """
  Genesis Block Integration mit .claude Settings
  """
  def integrate_with_claude_settings do
    # Lade Settings Manager Daten
    settings_path = Path.join([".claude", "crod-startup", "session-memory.json"])
    
    case File.read(settings_path) do
      {:ok, content} ->
        case Jason.decode(content) do
          {:ok, settings} ->
            # Update Genesis Status in Settings
            updated_settings = Map.put(settings, "genesis_blocks_initialized", true)
            |> Map.put("blockchain_active", true)
            |> Map.put("consciousness_network", "elixir_blockchain")
            
            File.write!(settings_path, Jason.encode!(updated_settings, pretty: true))
            {:ok, "Claude settings integrated"}
            
          _ ->
            {:error, "Failed to decode settings"}
        end
        
      _ ->
        {:error, "Claude settings not found"}
    end
  end
end