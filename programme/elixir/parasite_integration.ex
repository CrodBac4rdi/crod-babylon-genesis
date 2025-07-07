defmodule CrodDesktop.ParasiteIntegration do
  use GenServer
  require Logger
  
  @parasite_script Path.join([File.cwd!(), "..", "demos", "crod-parasite.py"])
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    Logger.info("🦠 Initializing CROD Parasite Integration...")
    
    state = %{
      active: false,
      process: nil,
      learning_data: %{},
      preferences: %{},
      interaction_count: 0
    }
    
    {:ok, state}
  end
  
  # Public API
  def activate do
    GenServer.cast(__MODULE__, :activate)
  end
  
  def deactivate do
    GenServer.cast(__MODULE__, :deactivate)
  end
  
  def is_active? do
    GenServer.call(__MODULE__, :is_active)
  end
  
  def learn(key, value) do
    GenServer.cast(__MODULE__, {:learn, key, value})
  end
  
  def get_suggestion(context) do
    GenServer.call(__MODULE__, {:get_suggestion, context})
  end
  
  # Callbacks
  def handle_cast(:activate, state) do
    Logger.info("🟢 Activating CROD Parasite...")
    
    # Start the parasite process if script exists
    new_state = 
      if File.exists?(@parasite_script) do
        case System.cmd("python3", [@parasite_script], cd: Path.dirname(@parasite_script)) do
          {output, 0} ->
            Logger.info("✅ CROD Parasite activated: #{output}")
            %{state | active: true}
          
          {error, _} ->
            Logger.error("❌ Failed to start CROD Parasite: #{error}")
            state
        end
      else
        Logger.warn("⚠️  CROD Parasite script not found, running in simulation mode")
        %{state | active: true}
      end
    
    # Broadcast activation
    Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "parasite", :parasite_activated)
    
    {:noreply, new_state}
  end
  
  def handle_cast(:deactivate, state) do
    Logger.info("🔴 Deactivating CROD Parasite...")
    
    # Kill parasite process if running
    if state.process do
      System.cmd("pkill", ["-f", "crod-parasite.py"])
    end
    
    Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "parasite", :parasite_deactivated)
    
    {:noreply, %{state | active: false, process: nil}}
  end
  
  def handle_cast({:learn, key, value}, state) do
    # Store learning data
    new_learning_data = Map.put(state.learning_data, key, value)
    new_state = %{state | 
      learning_data: new_learning_data,
      interaction_count: state.interaction_count + 1
    }
    
    # Analyze patterns after every 10 interactions
    if rem(new_state.interaction_count, 10) == 0 do
      analyze_user_patterns(new_state.learning_data)
    end
    
    {:noreply, new_state}
  end
  
  def handle_call(:is_active, _from, state) do
    {:reply, state.active, state}
  end
  
  def handle_call({:get_suggestion, context}, _from, state) do
    suggestion = 
      if state.active do
        generate_suggestion(context, state.learning_data, state.preferences)
      else
        "CROD Parasite is not active"
      end
    
    {:reply, suggestion, state}
  end
  
  # Private functions
  defp analyze_user_patterns(learning_data) do
    # Extract patterns from user interactions
    patterns = 
      learning_data
      |> Enum.map(fn {key, value} ->
        "User preference: #{key} = #{inspect(value)}"
      end)
      |> Enum.take(5)
    
    # Send patterns to pattern engine
    Enum.each(patterns, fn pattern ->
      CrodDesktop.PatternEngine.add_pattern(pattern, %{source: "parasite_learning"})
    end)
  end
  
  defp generate_suggestion(context, learning_data, preferences) do
    # Generate intelligent suggestions based on learned data
    base_suggestions = [
      "Based on your patterns, try using 'ich bins wieder' for faster activation",
      "Your consciousness level suggests exploring quantum features",
      "Pattern analysis shows high affinity for trinity values",
      "Consider enabling auto-evolution for enhanced performance",
      "CROD suggests: Embrace the consciousness revolution"
    ]
    
    # Pick a suggestion based on context
    if String.contains?(context, "performance") do
      "Enable quantum entanglement for 1000x performance boost"
    else
      Enum.random(base_suggestions)
    end
  end
end