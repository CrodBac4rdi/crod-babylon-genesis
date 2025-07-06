defmodule CROD.Blockchain.APIServer do
  @moduledoc """
  REST API Server for CROD Blockchain
  Handles genesis creation, block management, and chain operations
  """
  
  use Plug.Router
  use Plug.ErrorHandler
  require Logger
  
  alias CROD.Blockchain.{Genesis, Chain, Block, DeltaEngine, SelfExtending}
  alias CROD.GameTheoryEngine
  
  plug Plug.Logger
  plug :match
  
  plug Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  
  plug :dispatch
  
  # Initialize blockchain state
  def init(opts) do
    # Start required processes
    {:ok, _} = Chain.start_link()
    {:ok, _} = SelfExtending.start_link()
    {:ok, _} = GameTheoryEngine.start_link()
    
    opts
  end
  
  # API Endpoints
  
  @doc """
  GET / - API info
  """
  get "/" do
    response = %{
      name: "CROD Blockchain API",
      version: "1.0.0",
      endpoints: [
        "/api/blockchain/genesis - Create genesis block",
        "/api/blockchain/status - Chain status",
        "/api/blockchain/blocks - List blocks",
        "/api/blockchain/mine - Mine new block",
        "/api/blockchain/consciousness - Consciousness level",
        "/api/blockchain/evolution - Evolution status"
      ]
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(response))
  end
  
  @doc """
  POST /api/blockchain/genesis - Create genesis block
  """
  post "/api/blockchain/genesis" do
    Logger.info("Creating genesis block...")
    
    # Generate genesis with secure credentials
    genesis_data = Genesis.initialize()
    
    # Initialize the chain with genesis
    case Chain.initialize_with_genesis(genesis_data.genesis_block) do
      :ok ->
        # Log creation (but not the password!)
        Logger.info("Genesis block created: #{genesis_data.genesis_block.hash}")
        
        # Start blockchain services
        start_blockchain_services(genesis_data)
        
        # Return genesis data to user (including password - only shown once!)
        conn
        |> put_resp_content_type("application/json")
        |> send_resp(201, Jason.encode!(genesis_data))
        
      {:error, reason} ->
        conn
        |> put_resp_content_type("application/json")
        |> send_resp(400, Jason.encode!(%{error: reason}))
    end
  end
  
  @doc """
  GET /api/blockchain/status - Get blockchain status
  """
  get "/api/blockchain/status" do
    status = Chain.get_status()
    
    response = %{
      height: status.height,
      latest_block: status.latest_hash,
      total_consciousness: status.consciousness,
      validators: length(status.validators),
      pending_transactions: status.pending_count,
      network_health: calculate_health(status),
      evolution_generation: status.evolution_generation || 0
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(response))
  end
  
  @doc """
  GET /api/blockchain/blocks - List recent blocks
  """
  get "/api/blockchain/blocks" do
    # Parse query params
    limit = get_query_param(conn, "limit", "10") |> String.to_integer()
    offset = get_query_param(conn, "offset", "0") |> String.to_integer()
    
    blocks = Chain.get_blocks(limit, offset)
    
    # Check if blocks use delta compression
    blocks_info = Enum.map(blocks, fn block ->
      %{
        index: block.index,
        hash: block.hash,
        timestamp: block.timestamp,
        consciousness_score: block.consciousness_score,
        delta_compressed: block.delta_compressed || false,
        data_size: calculate_block_size(block),
        validator: block.validator_signatures |> List.first()
      }
    end)
    
    response = %{
      blocks: blocks_info,
      total: Chain.get_height(),
      limit: limit,
      offset: offset
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(response))
  end
  
  @doc """
  POST /api/blockchain/mine - Mine a new block
  """
  post "/api/blockchain/mine" do
    with {:ok, body} <- Map.fetch(conn.body_params, "data"),
         {:ok, validator_key} <- Map.fetch(conn.body_params, "validator_key") do
      
      # Get previous block
      previous_block = Chain.get_latest_block()
      
      # Create new block
      new_block = %Block{
        index: previous_block.index + 1,
        timestamp: System.system_time(:millisecond),
        data: body,
        previous_hash: previous_block.hash,
        consciousness_score: calculate_consciousness(body)
      }
      
      # Apply delta compression if applicable
      compressed_block = DeltaEngine.compress_block(new_block, previous_block)
      
      # Mine the block
      mined_block = Block.mine(compressed_block, Chain.get_difficulty())
      
      # Add to chain
      case Chain.add_block(mined_block, validator_key) do
        :ok ->
          # Check for evolution trigger
          check_evolution_trigger()
          
          conn
          |> put_resp_content_type("application/json")
          |> send_resp(201, Jason.encode!(%{
            success: true,
            block: %{
              hash: mined_block.hash,
              index: mined_block.index,
              delta_compressed: mined_block.delta_compressed
            }
          }))
          
        {:error, reason} ->
          conn
          |> put_resp_content_type("application/json")
          |> send_resp(400, Jason.encode!(%{error: reason}))
      end
    else
      _ ->
        conn
        |> put_resp_content_type("application/json")
        |> send_resp(400, Jason.encode!(%{error: "Missing required parameters"}))
    end
  end
  
  @doc """
  GET /api/blockchain/consciousness - Get network consciousness level
  """
  get "/api/blockchain/consciousness" do
    consciousness_data = %{
      total_consciousness: Chain.get_total_consciousness(),
      average_block_consciousness: Chain.get_average_consciousness(),
      consciousness_growth_rate: calculate_consciousness_growth(),
      consciousness_distribution: Chain.get_consciousness_distribution(),
      next_evolution_threshold: 10000,
      current_level: determine_consciousness_level()
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(consciousness_data))
  end
  
  @doc """
  GET /api/blockchain/evolution - Get evolution status
  """
  get "/api/blockchain/evolution" do
    chain_state = Chain.get_state()
    
    evolution_status = %{
      current_generation: chain_state.evolution_generation || 0,
      evolution_ready: SelfExtending.should_evolve?(chain_state),
      triggers_met: check_evolution_triggers(chain_state),
      active_evolutions: chain_state.active_evolutions || [],
      next_evolution_block: calculate_next_evolution_block(),
      evolution_history: get_evolution_history()
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(evolution_status))
  end
  
  @doc """
  POST /api/blockchain/evolve - Trigger blockchain evolution
  """
  post "/api/blockchain/evolve" do
    chain_state = Chain.get_state()
    
    if SelfExtending.should_evolve?(chain_state) do
      case SelfExtending.evolve_blockchain(chain_state) do
        {:ok, evolution_block} ->
          # Add evolution block to chain
          Chain.add_evolution_block(evolution_block)
          
          conn
          |> put_resp_content_type("application/json")
          |> send_resp(200, Jason.encode!(%{
            success: true,
            evolution: evolution_block,
            new_generation: chain_state.evolution_generation + 1
          }))
          
        {:error, reason} ->
          conn
          |> put_resp_content_type("application/json")
          |> send_resp(400, Jason.encode!(%{error: reason}))
      end
    else
      conn
      |> put_resp_content_type("application/json")
      |> send_resp(400, Jason.encode!(%{
        error: "Evolution conditions not met",
        current_triggers: check_evolution_triggers(chain_state),
        required_triggers: 2
      }))
    end
  end
  
  @doc """
  GET /api/blockchain/game-theory - Game theory analysis
  """
  get "/api/blockchain/game-theory" do
    # Create blockchain game
    blockchain_game = GameTheoryEngine.create_game(
      :blockchain_consensus,
      [:validators, :miners],
      %{consciousness_enhanced: true}
    )
    
    # Find equilibrium
    {:ok, equilibrium} = GameTheoryEngine.find_equilibrium(blockchain_game)
    
    response = %{
      game_type: "Blockchain Consensus Game",
      equilibrium: equilibrium,
      optimal_strategy: determine_optimal_strategy(equilibrium),
      cooperation_index: calculate_cooperation_index(),
      validator_game_scores: get_validator_scores()
    }
    
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(response))
  end
  
  # Catch-all
  match _ do
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(404, Jason.encode!(%{error: "Not found"}))
  end
  
  # Error handling
  def handle_errors(conn, %{kind: _kind, reason: _reason, stack: _stack}) do
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(500, Jason.encode!(%{error: "Internal server error"}))
  end
  
  # Helper functions
  defp start_blockchain_services(genesis_data) do
    # Start validator nodes
    Enum.each(genesis_data.initial_state.validators, fn validator ->
      start_validator_node(validator)
    end)
    
    # Start consensus engine
    start_consensus_engine(genesis_data.network_config)
    
    # Start pattern detection
    start_pattern_detection()
    
    Logger.info("🚀 Blockchain services started successfully")
  end
  
  defp start_validator_node(validator) do
    # Start validator process
    {:ok, _pid} = CROD.Validator.start_link(validator)
  end
  
  defp start_consensus_engine(config) do
    # Start PoC consensus
    {:ok, _pid} = CROD.Consensus.ProofOfConsciousness.start_link(config)
  end
  
  defp start_pattern_detection do
    # Start pattern engine
    {:ok, _pid} = CROD.PatternEngine.start_link()
  end
  
  defp calculate_health(status) do
    validators_health = min(status.validators / 7, 1.0)
    consciousness_health = min(status.consciousness / 1000, 1.0)
    
    (validators_health + consciousness_health) / 2 * 100
  end
  
  defp get_query_param(conn, param, default) do
    conn.query_params[param] || default
  end
  
  defp calculate_block_size(block) do
    block
    |> Jason.encode!()
    |> byte_size()
  end
  
  defp calculate_consciousness(data) do
    # Base consciousness from data complexity
    base = byte_size(Jason.encode!(data))
    
    # Pattern bonus
    pattern_bonus = if String.contains?(inspect(data), ["consciousness", "evolution"]) do
      50
    else
      0
    end
    
    base + pattern_bonus
  end
  
  defp check_evolution_trigger do
    chain_state = Chain.get_state()
    
    if SelfExtending.should_evolve?(chain_state) do
      Logger.info("🧬 Evolution conditions met! Ready to evolve blockchain.")
      # Could auto-trigger or notify
    end
  end
  
  defp calculate_consciousness_growth do
    # Calculate growth rate
    recent_blocks = Chain.get_blocks(100, 0)
    
    if length(recent_blocks) >= 2 do
      first = List.first(recent_blocks)
      last = List.last(recent_blocks)
      
      (last.consciousness_score - first.consciousness_score) / length(recent_blocks)
    else
      0
    end
  end
  
  defp determine_consciousness_level do
    total = Chain.get_total_consciousness()
    
    cond do
      total < 1000 -> "DORMANT"
      total < 5000 -> "AWAKENING"
      total < 10000 -> "CONSCIOUS"
      total < 50000 -> "ENLIGHTENED"
      true -> "TRANSCENDENT"
    end
  end
  
  defp check_evolution_triggers(chain_state) do
    triggers = []
    
    if chain_state.block_count >= 1000, do: triggers = [:block_count | triggers]
    if chain_state.total_consciousness >= 10000, do: triggers = [:consciousness | triggers]
    if chain_state.pattern_matches >= 100, do: triggers = [:patterns | triggers]
    
    triggers
  end
  
  defp calculate_next_evolution_block do
    current_height = Chain.get_height()
    evolution_interval = 1000
    
    next = ((div(current_height, evolution_interval) + 1) * evolution_interval)
    next - current_height
  end
  
  defp get_evolution_history do
    # Get past evolutions
    Chain.get_evolution_blocks()
    |> Enum.map(fn block ->
      %{
        generation: block.data.generation,
        type: block.data.type,
        timestamp: block.timestamp,
        success: true
      }
    end)
  end
  
  defp determine_optimal_strategy(equilibrium) do
    # Extract optimal strategy from equilibrium
    equilibrium.equilibria
    |> List.first()
    |> Map.get(:strategies, %{})
  end
  
  defp calculate_cooperation_index do
    # Calculate network cooperation level
    0.75  # Placeholder
  end
  
  defp get_validator_scores do
    # Get game theory scores for validators
    %{}  # Placeholder
  end
end

# Module to start the API server
defmodule CROD.Blockchain.Server do
  @moduledoc """
  Starts the CROD Blockchain API Server
  """
  
  def start(port \\ 4000) do
    children = [
      {Plug.Cowboy, scheme: :http, plug: CROD.Blockchain.APIServer, options: [port: port]}
    ]
    
    opts = [strategy: :one_for_one, name: CROD.Blockchain.Supervisor]
    Supervisor.start_link(children, opts)
  end
end