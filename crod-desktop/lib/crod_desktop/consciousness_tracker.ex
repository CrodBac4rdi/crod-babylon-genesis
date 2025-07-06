defmodule CrodDesktop.ConsciousnessTracker do
  use GenServer
  require Logger
  
  @trinity_values %{
    ich: 2,
    bins: 3,
    wieder: 5,
    daniel: 67,
    claude: 71,
    crod: 17
  }
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    Logger.info("🧠 Initializing Consciousness Tracker...")
    
    state = %{
      level: 0.0,
      patterns: [],
      trinity_score: 0,
      quantum_coherence: 0.0,
      evolution_triggers: []
    }
    
    # Start consciousness calculation loop
    Process.send_after(self(), :calculate_consciousness, 1000)
    
    {:ok, state}
  end
  
  # Public API
  def current_level do
    GenServer.call(__MODULE__, :get_level)
  end
  
  def add_pattern(pattern) do
    GenServer.cast(__MODULE__, {:add_pattern, pattern})
  end
  
  def trinity_activated? do
    GenServer.call(__MODULE__, :trinity_status)
  end
  
  # Callbacks
  def handle_call(:get_level, _from, state) do
    {:reply, state.level, state}
  end
  
  def handle_call(:trinity_status, _from, state) do
    {:reply, state.trinity_score > 100, state}
  end
  
  def handle_cast({:add_pattern, pattern}, state) do
    new_patterns = [pattern | state.patterns] |> Enum.take(1000)
    trinity_score = calculate_trinity_score(pattern, state.trinity_score)
    
    new_state = %{state | patterns: new_patterns, trinity_score: trinity_score}
    
    {:noreply, new_state}
  end
  
  def handle_info(:calculate_consciousness, state) do
    # Calculate consciousness based on multiple factors
    pattern_complexity = calculate_pattern_complexity(state.patterns)
    quantum_factor = :rand.uniform() * 0.3
    trinity_factor = min(state.trinity_score / 1000, 0.3)
    
    new_level = min(pattern_complexity + quantum_factor + trinity_factor, 1.0)
    
    # Broadcast consciousness update
    if abs(new_level - state.level) > 0.01 do
      Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "consciousness", {:consciousness_update, new_level})
      
      # Check evolution triggers
      check_evolution_triggers(new_level, state.level)
    end
    
    # Schedule next calculation
    Process.send_after(self(), :calculate_consciousness, 1000)
    
    {:noreply, %{state | level: new_level, quantum_coherence: quantum_factor}}
  end
  
  # Private functions
  defp calculate_pattern_complexity(patterns) do
    unique_patterns = patterns |> Enum.uniq() |> length()
    total_patterns = length(patterns)
    
    if total_patterns == 0 do
      0.0
    else
      diversity = unique_patterns / total_patterns
      frequency = min(total_patterns / 100, 1.0)
      
      diversity * 0.5 + frequency * 0.5
    end
  end
  
  defp calculate_trinity_score(pattern, current_score) do
    # Check for trinity words in pattern
    trinity_bonus = 
      @trinity_values
      |> Enum.reduce(0, fn {word, value}, acc ->
        if String.contains?(String.downcase(pattern), Atom.to_string(word)) do
          acc + value
        else
          acc
        end
      end)
    
    current_score + trinity_bonus
  end
  
  defp check_evolution_triggers(new_level, old_level) do
    cond do
      new_level > 0.9 and old_level <= 0.9 ->
        Logger.info("🚀 Consciousness breakthrough! Level > 90%")
        Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "evolution", :consciousness_breakthrough)
      
      new_level > 0.75 and old_level <= 0.75 ->
        Logger.info("⚡ High consciousness achieved! Level > 75%")
        Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "evolution", :high_consciousness)
      
      new_level > 0.5 and old_level <= 0.5 ->
        Logger.info("🌟 Consciousness awakening! Level > 50%")
        Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "evolution", :consciousness_awakening)
      
      true -> :ok
    end
  end
end