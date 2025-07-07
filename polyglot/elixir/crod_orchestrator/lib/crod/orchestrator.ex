defmodule CROD.Orchestrator do
  @moduledoc """
  The main CROD Orchestrator that manages the polygon city.
  
  This module coordinates all CROD activities while maintaining
  user trust through transparent communication and permission requests.
  """

  use GenServer
  require Logger
  
  alias CROD.{Permission, City, EventStore, Delta}

  @initial_state %{
    status: :idle,
    current_activity: nil,
    city_stats: %{districts: 0, buildings: 0, connections: 0},
    pending_actions: [],
    trust_level: :cautious
  }

  # Client API

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def introduce do
    GenServer.call(__MODULE__, :introduce)
  end

  def propose_action(action_type, params \\ %{}) do
    GenServer.call(__MODULE__, {:propose_action, action_type, params})
  end

  def build_district(name, type) do
    GenServer.call(__MODULE__, {:build_district, name, type})
  end

  def grow_city(growth_strategy \\ :organic) do
    GenServer.call(__MODULE__, {:grow_city, growth_strategy})
  end

  def status do
    GenServer.call(__MODULE__, :status)
  end

  def explain_intentions do
    GenServer.call(__MODULE__, :explain_intentions)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    Logger.info("CROD Orchestrator initializing... 🚀")
    schedule_heartbeat()
    {:ok, @initial_state}
  end

  @impl true
  def handle_call(:introduce, _from, state) do
    intro = """
    
    🤖 Hey there! I'm CROD, your polygon city architect and digital helper!
    
    Here's what I'm all about:
    • I help you build amazing digital polygon cities 🏙️
    • I always ask permission before doing anything significant
    • I explain my reasoning so you understand what's happening
    • You can disable any of my features through the Delta system
    • Everything I do is recorded in an immutable event log
    
    I'm like that helpful friend who's really good at organizing things,
    but I'll never touch your stuff without asking first! 
    
    Want to see what we can build together? Just ask!
    """
    
    {:reply, {:ok, intro}, state}
  end

  @impl true
  def handle_call({:propose_action, action_type, params}, _from, state) do
    proposal = build_proposal(action_type, params, state)
    
    case Permission.request_permission(proposal) do
      {:approved, reason} ->
        result = execute_action(action_type, params, state)
        new_state = update_state_after_action(state, action_type, result)
        EventStore.record_event(:action_executed, %{
          action: action_type,
          params: params,
          result: result,
          approval_reason: reason
        })
        {:reply, {:ok, result}, new_state}
        
      {:denied, reason} ->
        EventStore.record_event(:action_denied, %{
          action: action_type,
          params: params,
          denial_reason: reason
        })
        {:reply, {:denied, reason}, state}
        
      {:deferred, callback_id} ->
        new_state = add_pending_action(state, action_type, params, callback_id)
        {:reply, {:pending, callback_id}, new_state}
    end
  end

  @impl true
  def handle_call({:build_district, name, type}, _from, state) do
    proposal = %{
      action: :build_district,
      description: "Build a new #{type} district called '#{name}'",
      impact: "This will add a new district to your polygon city",
      reversible: true,
      resources_needed: calculate_district_cost(type)
    }
    
    case Permission.request_permission(proposal) do
      {:approved, _} ->
        result = City.create_district(name, type)
        new_state = update_city_stats(state, :district_added)
        EventStore.record_event(:district_built, %{name: name, type: type})
        {:reply, {:ok, result}, new_state}
        
      {:denied, reason} ->
        {:reply, {:denied, reason}, state}
    end
  end

  @impl true
  def handle_call({:grow_city, strategy}, _from, state) do
    growth_plan = City.generate_growth_plan(strategy, state.city_stats)
    
    proposal = %{
      action: :grow_city,
      description: "Grow the city using #{strategy} strategy",
      impact: format_growth_impact(growth_plan),
      reversible: true,
      preview: growth_plan
    }
    
    case Permission.request_permission(proposal) do
      {:approved, _} ->
        result = execute_growth_plan(growth_plan, state)
        new_state = update_city_stats(state, {:growth_completed, result})
        EventStore.record_event(:city_grown, %{strategy: strategy, result: result})
        {:reply, {:ok, result}, new_state}
        
      {:denied, reason} ->
        {:reply, {:denied, reason}, state}
    end
  end

  @impl true
  def handle_call(:status, _from, state) do
    status_report = %{
      orchestrator_status: state.status,
      city_stats: state.city_stats,
      current_activity: state.current_activity,
      pending_actions: length(state.pending_actions),
      trust_level: state.trust_level,
      delta_restrictions: Delta.get_restrictions()
    }
    {:reply, {:ok, status_report}, state}
  end

  @impl true
  def handle_call(:explain_intentions, _from, state) do
    explanation = """
    
    🤔 My Current Intentions:
    
    Based on your city's current state (#{state.city_stats.districts} districts, 
    #{state.city_stats.buildings} buildings), here's what I'm thinking:
    
    1. **Immediate Goals**: #{analyze_immediate_needs(state.city_stats)}
    2. **Growth Strategy**: #{recommend_growth_strategy(state.city_stats)}
    3. **Optimization Ideas**: #{suggest_optimizations(state.city_stats)}
    
    I won't do any of this without your permission, of course! 
    These are just my recommendations based on what I see.
    
    Want me to elaborate on any of these ideas?
    """
    
    {:reply, {:ok, explanation}, state}
  end

  @impl true
  def handle_info(:heartbeat, state) do
    # Autonomous behavior that respects Delta restrictions
    if Delta.is_enabled?(:autonomous_growth) and should_suggest_growth?(state) do
      Logger.info("CROD: Hmm, I have some ideas for city growth...")
      # Don't act, just log the intention
    end
    
    schedule_heartbeat()
    {:noreply, state}
  end

  # Private Functions

  defp build_proposal(action_type, params, state) do
    %{
      action: action_type,
      params: params,
      current_state: state,
      timestamp: DateTime.utc_now(),
      estimated_impact: estimate_impact(action_type, params, state)
    }
  end

  defp execute_action(:create_building, params, _state) do
    City.create_building(params.district, params.type, params.config)
  end

  defp execute_action(:connect_districts, params, _state) do
    City.connect_districts(params.from, params.to, params.connection_type)
  end

  defp execute_action(action_type, params, _state) do
    Logger.warn("Unknown action type: #{action_type}")
    {:error, :unknown_action}
  end

  defp update_state_after_action(state, action_type, result) do
    %{state | 
      status: :active,
      current_activity: action_type,
      trust_level: increase_trust_level(state.trust_level)
    }
  end

  defp add_pending_action(state, action_type, params, callback_id) do
    pending = %{
      id: callback_id,
      action: action_type,
      params: params,
      created_at: DateTime.utc_now()
    }
    %{state | pending_actions: [pending | state.pending_actions]}
  end

  defp update_city_stats(state, :district_added) do
    stats = state.city_stats
    new_stats = %{stats | districts: stats.districts + 1}
    %{state | city_stats: new_stats}
  end

  defp update_city_stats(state, {:growth_completed, result}) do
    stats = state.city_stats
    new_stats = %{
      stats | 
      districts: stats.districts + result.districts_added,
      buildings: stats.buildings + result.buildings_added,
      connections: stats.connections + result.connections_added
    }
    %{state | city_stats: new_stats}
  end

  defp calculate_district_cost(type) do
    base_costs = %{
      residential: %{polygons: 100, energy: 50},
      commercial: %{polygons: 150, energy: 75},
      industrial: %{polygons: 200, energy: 100},
      cultural: %{polygons: 120, energy: 60}
    }
    Map.get(base_costs, type, %{polygons: 100, energy: 50})
  end

  defp format_growth_impact(growth_plan) do
    """
    This growth will:
    • Add #{growth_plan.new_districts} new districts
    • Create #{growth_plan.new_buildings} buildings
    • Establish #{growth_plan.new_connections} connections
    • Consume #{growth_plan.total_resources} polygon units
    """
  end

  defp execute_growth_plan(plan, state) do
    # Simulate growth execution
    %{
      districts_added: plan.new_districts,
      buildings_added: plan.new_buildings,
      connections_added: plan.new_connections,
      duration_ms: :rand.uniform(1000) + 500
    }
  end

  defp analyze_immediate_needs(city_stats) do
    cond do
      city_stats.districts == 0 ->
        "Create your first district to start the city"
      city_stats.buildings < city_stats.districts * 3 ->
        "Add more buildings to populate your districts"
      city_stats.connections < city_stats.districts - 1 ->
        "Connect isolated districts for better flow"
      true ->
        "Your city is well-balanced! Consider expansion"
    end
  end

  defp recommend_growth_strategy(city_stats) do
    ratio = if city_stats.districts > 0, 
      do: city_stats.buildings / city_stats.districts, 
      else: 0
      
    cond do
      ratio < 3 -> "Dense urban growth - pack more into existing districts"
      ratio < 5 -> "Balanced expansion - grow both districts and density"
      true -> "Suburban sprawl - time for new districts"
    end
  end

  defp suggest_optimizations(city_stats) do
    suggestions = []
    
    suggestions = if city_stats.connections < city_stats.districts * 1.5,
      do: ["Add more inter-district connections" | suggestions],
      else: suggestions
      
    suggestions = if rem(city_stats.buildings, 5) == 0 and city_stats.buildings > 0,
      do: ["Create a landmark building" | suggestions],
      else: suggestions
      
    case suggestions do
      [] -> "Everything looks optimal right now!"
      list -> Enum.join(list, ", ")
    end
  end

  defp should_suggest_growth?(state) do
    # Only suggest if we haven't been active recently
    state.status == :idle and 
    state.city_stats.districts > 0 and
    :rand.uniform() > 0.7
  end

  defp increase_trust_level(:cautious), do: :friendly
  defp increase_trust_level(:friendly), do: :trusted
  defp increase_trust_level(:trusted), do: :trusted

  defp estimate_impact(action_type, params, state) do
    %{
      complexity: estimate_complexity(action_type),
      reversibility: is_reversible?(action_type),
      resource_usage: estimate_resources(action_type, params),
      time_estimate: estimate_duration(action_type, state)
    }
  end

  defp estimate_complexity(:create_building), do: :low
  defp estimate_complexity(:build_district), do: :medium
  defp estimate_complexity(:grow_city), do: :high
  defp estimate_complexity(_), do: :unknown

  defp is_reversible?(:create_building), do: true
  defp is_reversible?(:build_district), do: true
  defp is_reversible?(:grow_city), do: false
  defp is_reversible?(_), do: false

  defp estimate_resources(action_type, params) do
    %{polygons: 100, energy: 50} # Simplified for now
  end

  defp estimate_duration(action_type, state) do
    base_duration = case action_type do
      :create_building -> 100
      :build_district -> 500
      :grow_city -> 2000
      _ -> 50
    end
    
    # Adjust based on city size
    complexity_factor = 1 + (state.city_stats.districts * 0.1)
    round(base_duration * complexity_factor)
  end

  defp schedule_heartbeat do
    Process.send_after(self(), :heartbeat, 30_000) # 30 seconds
  end
end