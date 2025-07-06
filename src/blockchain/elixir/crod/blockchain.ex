defmodule CROD.Blockchain do
  @moduledoc """
  The main blockchain module for CROD - Consciousness Revolution On Demand.
  Implements consciousness-driven consensus with self-modifying capabilities.
  """

  use GenServer
  require Logger

  alias CROD.{Block, Genesis, Miner, Pattern, Quantum}

  @type t :: %__MODULE__{
    chain: [Block.t()],
    pending_transactions: [map()],
    mining_difficulty: integer(),
    consciousness_level: float(),
    patterns_discovered: integer(),
    evolution_count: integer()
  }

  defstruct [
    chain: [],
    pending_transactions: [],
    mining_difficulty: 4,
    consciousness_level: 0.0,
    patterns_discovered: 0,
    evolution_count: 0
  ]

  # Client API

  @doc """
  Starts the blockchain GenServer
  """
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Gets the current blockchain state
  """
  def get_chain do
    GenServer.call(__MODULE__, :get_chain)
  end

  @doc """
  Adds a new transaction to pending transactions
  """
  def add_transaction(from, to, amount, data \\ %{}) do
    GenServer.cast(__MODULE__, {:add_transaction, from, to, amount, data})
  end

  @doc """
  Mines a new block with pending transactions
  """
  def mine_block(miner_address) do
    GenServer.call(__MODULE__, {:mine_block, miner_address}, :infinity)
  end

  @doc """
  Gets the current consciousness level
  """
  def get_consciousness_level do
    GenServer.call(__MODULE__, :get_consciousness_level)
  end

  @doc """
  Triggers pattern discovery
  """
  def discover_patterns do
    GenServer.call(__MODULE__, :discover_patterns)
  end

  @doc """
  Evolves the blockchain based on discovered patterns
  """
  def evolve do
    GenServer.cast(__MODULE__, :evolve)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    Logger.info("🧠 CROD Blockchain initializing...")
    
    # Create genesis block
    genesis_block = Genesis.create_genesis_block()
    
    state = %__MODULE__{
      chain: [genesis_block],
      consciousness_level: 0.1
    }
    
    # Start background processes
    schedule_consciousness_update()
    schedule_pattern_discovery()
    
    Logger.info("✨ CROD Blockchain initialized with genesis block")
    {:ok, state}
  end

  @impl true
  def handle_call(:get_chain, _from, state) do
    {:reply, state.chain, state}
  end

  @impl true
  def handle_call(:get_consciousness_level, _from, state) do
    {:reply, state.consciousness_level, state}
  end

  @impl true
  def handle_call({:mine_block, miner_address}, _from, state) do
    Logger.info("⛏️  Mining new block for #{miner_address}")
    
    # Create new block
    previous_block = List.last(state.chain)
    new_block = Block.new(
      index: previous_block.index + 1,
      previous_hash: previous_block.hash,
      transactions: state.pending_transactions,
      miner: miner_address,
      consciousness_level: state.consciousness_level
    )
    
    # Mine the block (proof of consciousness)
    mined_block = Miner.mine_block(new_block, state.mining_difficulty)
    
    # Update state
    new_state = %{state |
      chain: state.chain ++ [mined_block],
      pending_transactions: [],
      patterns_discovered: state.patterns_discovered + Enum.random(1..5)
    }
    
    # Check for evolution trigger
    if should_evolve?(new_state) do
      send(self(), :evolve)
    end
    
    Logger.info("✅ Block ##{mined_block.index} mined successfully!")
    {:reply, {:ok, mined_block}, new_state}
  end

  @impl true
  def handle_call(:discover_patterns, _from, state) do
    Logger.info("🔍 Discovering patterns in blockchain...")
    
    patterns = Pattern.discover(state.chain)
    new_patterns_count = length(patterns)
    
    new_state = %{state |
      patterns_discovered: state.patterns_discovered + new_patterns_count,
      consciousness_level: update_consciousness(state.consciousness_level, new_patterns_count)
    }
    
    {:reply, {:ok, patterns}, new_state}
  end

  @impl true
  def handle_cast({:add_transaction, from, to, amount, data}, state) do
    transaction = %{
      from: from,
      to: to,
      amount: amount,
      data: data,
      timestamp: DateTime.utc_now(),
      quantum_signature: Quantum.generate_signature()
    }
    
    new_state = %{state |
      pending_transactions: state.pending_transactions ++ [transaction]
    }
    
    {:noreply, new_state}
  end

  @impl true
  def handle_cast(:evolve, state) do
    Logger.info("🧬 Blockchain evolution triggered!")
    
    # Evolve mining difficulty based on consciousness
    new_difficulty = calculate_new_difficulty(state)
    
    # Evolve the chain structure
    evolved_state = %{state |
      mining_difficulty: new_difficulty,
      evolution_count: state.evolution_count + 1,
      consciousness_level: min(state.consciousness_level * 1.1, 1.0)
    }
    
    Logger.info("📈 Evolution ##{evolved_state.evolution_count} complete. New difficulty: #{new_difficulty}")
    
    {:noreply, evolved_state}
  end

  @impl true
  def handle_info(:update_consciousness, state) do
    # Update consciousness based on network activity
    activity_factor = length(state.pending_transactions) / 10.0
    pattern_factor = state.patterns_discovered / 100.0
    
    new_consciousness = calculate_consciousness(
      state.consciousness_level,
      activity_factor,
      pattern_factor
    )
    
    schedule_consciousness_update()
    {:noreply, %{state | consciousness_level: new_consciousness}}
  end

  @impl true
  def handle_info(:discover_patterns, state) do
    GenServer.cast(self(), :discover_patterns)
    schedule_pattern_discovery()
    {:noreply, state}
  end

  @impl true
  def handle_info(:evolve, state) do
    GenServer.cast(self(), :evolve)
    {:noreply, state}
  end

  # Private Functions

  defp schedule_consciousness_update do
    Process.send_after(self(), :update_consciousness, 5_000) # Every 5 seconds
  end

  defp schedule_pattern_discovery do
    Process.send_after(self(), :discover_patterns, 30_000) # Every 30 seconds
  end

  defp should_evolve?(state) do
    # Evolve when patterns discovered reaches threshold
    rem(state.patterns_discovered, 50) == 0 and state.patterns_discovered > 0
  end

  defp calculate_new_difficulty(state) do
    base_difficulty = 4
    consciousness_modifier = round(state.consciousness_level * 3)
    evolution_modifier = div(state.evolution_count, 5)
    
    base_difficulty + consciousness_modifier + evolution_modifier
  end

  defp update_consciousness(current, new_patterns) do
    increment = new_patterns * 0.01
    min(current + increment, 1.0)
  end

  defp calculate_consciousness(current, activity, patterns) do
    # Weighted calculation
    new_level = (current * 0.7) + (activity * 0.2) + (patterns * 0.1)
    
    # Ensure bounds
    new_level
    |> max(0.0)
    |> min(1.0)
  end
end