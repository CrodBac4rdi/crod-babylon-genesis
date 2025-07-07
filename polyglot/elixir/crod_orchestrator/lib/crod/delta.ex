defmodule CROD.Delta do
  @moduledoc """
  User control system for disabling/enabling CROD features.
  
  Delta is your control panel - the emergency brake, the fine-tuning knobs,
  and the trust settings all in one. You're always in charge!
  """

  use GenServer
  require Logger

  alias CROD.{EventStore, Permission}

  defstruct [
    :enabled_features,
    :disabled_features,
    :feature_limits,
    :override_rules,
    :emergency_stop,
    :control_history
  ]

  @default_features %{
    autonomous_growth: true,
    permission_system: true,
    event_logging: true,
    sandbox_mode: true,
    ai_suggestions: true,
    pattern_learning: true,
    resource_optimization: true,
    auto_connections: true,
    predictive_planning: true,
    self_modification: false  # Disabled by default for safety
  }

  # Client API

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: opts[:name] || __MODULE__)
  end

  def enable_feature(feature) do
    GenServer.call(__MODULE__, {:enable_feature, feature})
  end

  def disable_feature(feature) do
    GenServer.call(__MODULE__, {:disable_feature, feature})
  end

  def is_enabled?(feature) do
    GenServer.call(__MODULE__, {:is_enabled, feature})
  end

  def set_limit(feature, limit_type, value) do
    GenServer.call(__MODULE__, {:set_limit, feature, limit_type, value})
  end

  def emergency_stop! do
    GenServer.call(__MODULE__, :emergency_stop)
  end

  def resume do
    GenServer.call(__MODULE__, :resume)
  end

  def get_status do
    GenServer.call(__MODULE__, :get_status)
  end

  def get_restrictions do
    GenServer.call(__MODULE__, :get_restrictions)
  end

  def set_override(pattern, rule) do
    GenServer.call(__MODULE__, {:set_override, pattern, rule})
  end

  def clear_override(pattern) do
    GenServer.call(__MODULE__, {:clear_override, pattern})
  end

  def review_control_history(limit \\ 50) do
    GenServer.call(__MODULE__, {:review_history, limit})
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    Logger.info("CROD Delta Control System initializing...")
    
    {:ok, %__MODULE__{
      enabled_features: @default_features,
      disabled_features: %{},
      feature_limits: initialize_default_limits(),
      override_rules: %{},
      emergency_stop: false,
      control_history: []
    }}
  end

  @impl true
  def handle_call({:enable_feature, feature}, _from, state) do
    if state.emergency_stop do
      {:reply, {:error, :emergency_stop_active}, state}
    else
      new_enabled = Map.put(state.enabled_features, feature, true)
      new_disabled = Map.delete(state.disabled_features, feature)
      
      new_state = %{state | 
        enabled_features: new_enabled,
        disabled_features: new_disabled
      }
      
      log_control_change(:enable, feature, new_state)
      EventStore.record_event(:delta_feature_enabled, %{feature: feature})
      
      Logger.info("Delta: Feature '#{feature}' enabled")
      
      {:reply, :ok, new_state}
    end
  end

  @impl true
  def handle_call({:disable_feature, feature}, _from, state) do
    # Some features cannot be disabled for safety
    if feature in [:permission_system, :event_logging] do
      {:reply, {:error, :cannot_disable_safety_feature}, state}
    else
      new_enabled = Map.put(state.enabled_features, feature, false)
      new_disabled = Map.put(state.disabled_features, feature, DateTime.utc_now())
      
      new_state = %{state | 
        enabled_features: new_enabled,
        disabled_features: new_disabled
      }
      
      log_control_change(:disable, feature, new_state)
      EventStore.record_event(:delta_feature_disabled, %{feature: feature})
      
      Logger.info("Delta: Feature '#{feature}' disabled")
      
      {:reply, :ok, new_state}
    end
  end

  @impl true
  def handle_call({:is_enabled, feature}, _from, state) do
    if state.emergency_stop do
      {:reply, false, state}
    else
      enabled = Map.get(state.enabled_features, feature, false)
      {:reply, enabled, state}
    end
  end

  @impl true
  def handle_call({:set_limit, feature, limit_type, value}, _from, state) do
    if state.emergency_stop do
      {:reply, {:error, :emergency_stop_active}, state}
    else
      current_limits = Map.get(state.feature_limits, feature, %{})
      new_limits = Map.put(current_limits, limit_type, value)
      
      new_feature_limits = Map.put(state.feature_limits, feature, new_limits)
      new_state = %{state | feature_limits: new_feature_limits}
      
      log_control_change(:set_limit, {feature, limit_type, value}, new_state)
      EventStore.record_event(:delta_limit_set, %{
        feature: feature,
        limit_type: limit_type,
        value: value
      })
      
      Logger.info("Delta: Set limit for #{feature}.#{limit_type} = #{value}")
      
      {:reply, :ok, new_state}
    end
  end

  @impl true
  def handle_call(:emergency_stop, _from, state) do
    Logger.warn("DELTA EMERGENCY STOP ACTIVATED! All CROD features suspended.")
    
    new_state = %{state | emergency_stop: true}
    
    log_control_change(:emergency_stop, true, new_state)
    EventStore.record_event(:delta_emergency_stop, %{timestamp: DateTime.utc_now()})
    
    # Notify all components
    broadcast_emergency_stop()
    
    {:reply, :ok, new_state}
  end

  @impl true
  def handle_call(:resume, _from, state) do
    if state.emergency_stop do
      Logger.info("Delta: Resuming normal operations...")
      
      new_state = %{state | emergency_stop: false}
      
      log_control_change(:resume, true, new_state)
      EventStore.record_event(:delta_resumed, %{timestamp: DateTime.utc_now()})
      
      # Notify all components
      broadcast_resume()
      
      {:reply, :ok, new_state}
    else
      {:reply, {:error, :not_in_emergency_stop}, state}
    end
  end

  @impl true
  def handle_call(:get_status, _from, state) do
    status = %{
      emergency_stop: state.emergency_stop,
      enabled_features: Map.keys(state.enabled_features) |> Enum.filter(&Map.get(state.enabled_features, &1)),
      disabled_features: Map.keys(state.disabled_features),
      active_limits: summarize_limits(state.feature_limits),
      override_count: map_size(state.override_rules),
      control_summary: generate_control_summary(state)
    }
    
    {:reply, {:ok, status}, state}
  end

  @impl true
  def handle_call(:get_restrictions, _from, state) do
    restrictions = %{
      emergency_stop: state.emergency_stop,
      disabled_features: Map.keys(state.disabled_features),
      limits: state.feature_limits,
      overrides: state.override_rules
    }
    
    {:reply, restrictions, state}
  end

  @impl true
  def handle_call({:set_override, pattern, rule}, _from, state) do
    new_overrides = Map.put(state.override_rules, pattern, rule)
    new_state = %{state | override_rules: new_overrides}
    
    log_control_change(:set_override, {pattern, rule}, new_state)
    EventStore.record_event(:delta_override_set, %{pattern: pattern, rule: rule})
    
    Logger.info("Delta: Override set for pattern '#{pattern}'")
    
    {:reply, :ok, new_state}
  end

  @impl true
  def handle_call({:clear_override, pattern}, _from, state) do
    new_overrides = Map.delete(state.override_rules, pattern)
    new_state = %{state | override_rules: new_overrides}
    
    log_control_change(:clear_override, pattern, new_state)
    EventStore.record_event(:delta_override_cleared, %{pattern: pattern})
    
    {:reply, :ok, new_state}
  end

  @impl true
  def handle_call({:review_history, limit}, _from, state) do
    recent_history = Enum.take(state.control_history, limit)
    {:reply, {:ok, recent_history}, state}
  end

  # Private Functions

  defp initialize_default_limits do
    %{
      autonomous_growth: %{
        max_districts_per_hour: 10,
        max_buildings_per_district: 50,
        max_connections_per_district: 20
      },
      resource_optimization: %{
        max_polygon_usage_percent: 80,
        min_efficiency_threshold: 0.6
      },
      ai_suggestions: %{
        max_suggestions_per_hour: 20,
        complexity_limit: :medium
      },
      pattern_learning: %{
        max_patterns_stored: 1000,
        learning_rate: 0.1
      }
    }
  end

  defp log_control_change(action, details, state) do
    entry = %{
      timestamp: DateTime.utc_now(),
      action: action,
      details: details,
      resulting_state: summarize_state(state)
    }
    
    history = [entry | state.control_history] |> Enum.take(1000)
    
    %{state | control_history: history}
  end

  defp summarize_state(state) do
    %{
      emergency_stop: state.emergency_stop,
      enabled_count: Enum.count(state.enabled_features, fn {_, v} -> v end),
      disabled_count: map_size(state.disabled_features),
      limit_count: map_size(state.feature_limits),
      override_count: map_size(state.override_rules)
    }
  end

  defp broadcast_emergency_stop do
    # In a real system, this would notify all CROD components
    Logger.warn("Broadcasting emergency stop to all CROD components...")
    :ok
  end

  defp broadcast_resume do
    # In a real system, this would notify all CROD components
    Logger.info("Broadcasting resume signal to all CROD components...")
    :ok
  end

  defp summarize_limits(feature_limits) do
    Enum.map(feature_limits, fn {feature, limits} ->
      {feature, map_size(limits)}
    end)
    |> Enum.into(%{})
  end

  defp generate_control_summary(state) do
    total_features = map_size(@default_features)
    enabled_count = Enum.count(state.enabled_features, fn {_, v} -> v end)
    
    cond do
      state.emergency_stop ->
        "🛑 EMERGENCY STOP ACTIVE - All features suspended"
      
      enabled_count == total_features ->
        "✅ All features enabled - CROD fully operational"
      
      enabled_count > total_features * 0.7 ->
        "🟢 Most features enabled - CROD operating normally"
      
      enabled_count > total_features * 0.3 ->
        "🟡 Limited features enabled - CROD in restricted mode"
      
      true ->
        "🔴 Minimal features enabled - CROD heavily restricted"
    end
  end

  # Public helper functions for common control patterns

  def safe_mode! do
    Logger.info("Activating CROD Safe Mode...")
    
    # Disable potentially risky features
    disable_feature(:self_modification)
    disable_feature(:predictive_planning)
    disable_feature(:auto_connections)
    
    # Set conservative limits
    set_limit(:autonomous_growth, :max_districts_per_hour, 1)
    set_limit(:ai_suggestions, :complexity_limit, :low)
    
    # Enable all safety features
    enable_feature(:permission_system)
    enable_feature(:event_logging)
    enable_feature(:sandbox_mode)
    
    :ok
  end

  def unrestricted_mode! do
    Logger.warn("Activating CROD Unrestricted Mode - Use with caution!")
    
    # Enable all features
    Enum.each(Map.keys(@default_features), &enable_feature/1)
    
    # Remove limits
    set_limit(:autonomous_growth, :max_districts_per_hour, 1000)
    set_limit(:resource_optimization, :max_polygon_usage_percent, 100)
    
    :ok
  end

  def learning_mode! do
    Logger.info("Activating CROD Learning Mode...")
    
    # Enable learning features
    enable_feature(:pattern_learning)
    enable_feature(:ai_suggestions)
    enable_feature(:sandbox_mode)
    
    # Disable autonomous actions
    disable_feature(:autonomous_growth)
    disable_feature(:auto_connections)
    
    # Set learning-friendly limits
    set_limit(:pattern_learning, :learning_rate, 0.3)
    set_limit(:ai_suggestions, :max_suggestions_per_hour, 50)
    
    :ok
  end

  # Query functions for feature checking

  def can_grow_autonomously? do
    is_enabled?(:autonomous_growth) and 
    not emergency_stop_active?() and
    within_growth_limits?()
  end

  def can_make_suggestions? do
    is_enabled?(:ai_suggestions) and
    not emergency_stop_active?()
  end

  def can_learn_patterns? do
    is_enabled?(:pattern_learning) and
    not emergency_stop_active?()
  end

  def emergency_stop_active? do
    GenServer.call(__MODULE__, :get_emergency_stop_status)
  end

  @impl true
  def handle_call(:get_emergency_stop_status, _from, state) do
    {:reply, state.emergency_stop, state}
  end

  defp within_growth_limits? do
    # Check if current growth rate is within limits
    # This would check actual metrics in a real implementation
    true
  end

  # Control validation functions

  def validate_action(action_type, params) do
    GenServer.call(__MODULE__, {:validate_action, action_type, params})
  end

  @impl true
  def handle_call({:validate_action, action_type, params}, _from, state) do
    validation = %{
      allowed: not state.emergency_stop,
      feature_enabled: is_feature_enabled_for_action?(action_type, state),
      within_limits: check_action_limits(action_type, params, state),
      override_applied: check_overrides(action_type, state.override_rules)
    }
    
    result = if Enum.all?(Map.values(validation), & &1) do
      {:ok, :approved}
    else
      {:error, build_denial_reason(validation)}
    end
    
    {:reply, result, state}
  end

  defp is_feature_enabled_for_action?(action_type, state) do
    feature = map_action_to_feature(action_type)
    Map.get(state.enabled_features, feature, false)
  end

  defp map_action_to_feature(:grow_city), do: :autonomous_growth
  defp map_action_to_feature(:suggest_improvement), do: :ai_suggestions
  defp map_action_to_feature(:learn_pattern), do: :pattern_learning
  defp map_action_to_feature(:optimize_resources), do: :resource_optimization
  defp map_action_to_feature(_), do: :general

  defp check_action_limits(action_type, params, state) do
    feature = map_action_to_feature(action_type)
    limits = Map.get(state.feature_limits, feature, %{})
    
    # Simplified limit checking
    case action_type do
      :grow_city ->
        max_allowed = Map.get(limits, :max_districts_per_hour, 10)
        requested = Map.get(params, :districts_to_add, 1)
        requested <= max_allowed
      
      _ ->
        true
    end
  end

  defp check_overrides(action_type, override_rules) do
    # Check if any override rules apply
    not Enum.any?(override_rules, fn {pattern, rule} ->
      matches_pattern?(action_type, pattern) and rule == :deny
    end)
  end

  defp matches_pattern?(action, pattern) when is_atom(pattern) do
    action == pattern
  end

  defp matches_pattern?(action, pattern) when is_binary(pattern) do
    String.contains?(to_string(action), pattern)
  end

  defp build_denial_reason(validation) do
    reasons = []
    
    reasons = if not validation.allowed,
      do: ["Emergency stop is active" | reasons],
      else: reasons
    
    reasons = if not validation.feature_enabled,
      do: ["Feature is disabled" | reasons],
      else: reasons
    
    reasons = if not validation.within_limits,
      do: ["Action exceeds configured limits" | reasons],
      else: reasons
    
    reasons = if not validation.override_applied,
      do: ["Override rule prevents this action" | reasons],
      else: reasons
    
    Enum.join(reasons, "; ")
  end
end