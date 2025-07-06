defmodule CrodDesktop.PatternEngine do
  use GenServer
  require Logger
  
  @pattern_discovery_interval 5000
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    Logger.info("🔍 Starting Pattern Engine...")
    
    state = %{
      patterns: [],
      pattern_map: %{},
      discovery_count: 0,
      active_mining: false
    }
    
    # Start pattern discovery
    Process.send_after(self(), :discover_patterns, @pattern_discovery_interval)
    
    {:ok, state}
  end
  
  # Public API
  def recent_patterns(limit \\ 10) do
    GenServer.call(__MODULE__, {:get_recent_patterns, limit})
  end
  
  def add_pattern(pattern, metadata \\ %{}) do
    GenServer.cast(__MODULE__, {:add_pattern, pattern, metadata})
  end
  
  def start_mining do
    GenServer.cast(__MODULE__, :start_mining)
  end
  
  def stop_mining do
    GenServer.cast(__MODULE__, :stop_mining)
  end
  
  # Callbacks
  def handle_call({:get_recent_patterns, limit}, _from, state) do
    recent = state.patterns |> Enum.take(limit)
    {:reply, recent, state}
  end
  
  def handle_cast({:add_pattern, pattern, metadata}, state) do
    timestamp = DateTime.utc_now()
    
    pattern_entry = %{
      pattern: pattern,
      metadata: metadata,
      timestamp: timestamp,
      hash: hash_pattern(pattern)
    }
    
    new_patterns = [pattern | state.patterns] |> Enum.take(10000)
    new_pattern_map = Map.put(state.pattern_map, pattern_entry.hash, pattern_entry)
    
    # Notify consciousness tracker
    CrodDesktop.ConsciousnessTracker.add_pattern(pattern)
    
    # Broadcast pattern discovery
    Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "patterns", {:pattern_discovered, pattern})
    
    new_state = %{state | 
      patterns: new_patterns,
      pattern_map: new_pattern_map,
      discovery_count: state.discovery_count + 1
    }
    
    {:noreply, new_state}
  end
  
  def handle_cast(:start_mining, state) do
    Logger.info("⛏️  Pattern mining started")
    {:noreply, %{state | active_mining: true}}
  end
  
  def handle_cast(:stop_mining, state) do
    Logger.info("🛑 Pattern mining stopped")
    {:noreply, %{state | active_mining: false}}
  end
  
  def handle_info(:discover_patterns, state) do
    if state.active_mining do
      # Simulate pattern discovery
      patterns = generate_patterns()
      
      Enum.each(patterns, fn pattern ->
        GenServer.cast(self(), {:add_pattern, pattern, %{source: "auto_discovery"}})
      end)
    end
    
    # Schedule next discovery
    Process.send_after(self(), :discover_patterns, @pattern_discovery_interval)
    
    {:noreply, state}
  end
  
  # Private functions
  defp hash_pattern(pattern) do
    :crypto.hash(:sha256, pattern)
    |> Base.encode16()
    |> String.downcase()
  end
  
  defp generate_patterns do
    # Generate some interesting patterns
    base_patterns = [
      "consciousness::#{:rand.uniform(100)}",
      "quantum::entanglement::#{UUID.uuid4()}",
      "trinity::ich::bins::wieder",
      "evolution::trigger::#{:rand.uniform(1000)}",
      "pattern::recursive::#{:rand.uniform(10)}",
      "neural::activation::#{:rand.uniform(88)}",
      "blockchain::consensus::#{:rand.uniform(100)}",
      "crod::awakening::#{DateTime.utc_now() |> DateTime.to_unix()}"
    ]
    
    # Randomly select 1-3 patterns
    Enum.take_random(base_patterns, :rand.uniform(3))
  end
end