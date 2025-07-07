defmodule CRODPhoenix.ServiceRegistry do
  @moduledoc """
  Service Registry for CROD inter-service communication
  Manages service discovery, health checks, and load balancing
  """
  use GenServer
  require Logger

  @table_name :crod_services
  @health_check_interval 5000
  @stale_service_timeout 30000

  defstruct [
    :services,
    :health_states,
    :load_balancer_state,
    :circuit_breakers
  ]

  # Client API

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def register(service_name, config) do
    GenServer.call(__MODULE__, {:register, service_name, config})
  end

  def unregister(service_name) do
    GenServer.call(__MODULE__, {:unregister, service_name})
  end

  def lookup(service_name) do
    GenServer.call(__MODULE__, {:lookup, service_name})
  end

  def lookup_district(district_name) do
    GenServer.call(__MODULE__, {:lookup_district, district_name})
  end

  def get_healthy_instance(service_name) do
    GenServer.call(__MODULE__, {:get_healthy_instance, service_name})
  end

  def report_health(service_name, health_status) do
    GenServer.cast(__MODULE__, {:report_health, service_name, health_status})
  end

  def get_service_mesh_status do
    GenServer.call(__MODULE__, :get_mesh_status)
  end

  # Server callbacks

  @impl true
  def init(_opts) do
    # Create ETS table for fast lookups
    :ets.new(@table_name, [:named_table, :public, read_concurrency: true])
    
    # Start health checking
    Process.send_after(self(), :health_check_round, @health_check_interval)
    
    state = %__MODULE__{
      services: %{},
      health_states: %{},
      load_balancer_state: %{},
      circuit_breakers: %{}
    }
    
    Logger.info("Service Registry initialized")
    
    {:ok, state}
  end

  @impl true
  def handle_call({:register, service_name, config}, _from, state) do
    service_id = generate_service_id(service_name)
    
    service_info = %{
      id: service_id,
      name: service_name,
      config: config,
      registered_at: DateTime.utc_now(),
      last_seen: DateTime.utc_now(),
      status: :healthy,
      metadata: extract_metadata(config)
    }
    
    # Store in ETS for fast lookup
    :ets.insert(@table_name, {service_name, service_info})
    
    # Initialize health state
    health_state = %{
      status: :healthy,
      last_check: DateTime.utc_now(),
      consecutive_failures: 0,
      response_times: []
    }
    
    # Initialize circuit breaker
    circuit_breaker = %{
      state: :closed,
      failure_count: 0,
      last_failure: nil,
      half_open_attempts: 0
    }
    
    new_state = %{state |
      services: Map.put(state.services, service_name, service_info),
      health_states: Map.put(state.health_states, service_name, health_state),
      circuit_breakers: Map.put(state.circuit_breakers, service_name, circuit_breaker)
    }
    
    broadcast_service_event(:registered, service_info)
    
    {:reply, {:ok, service_id}, new_state}
  end

  @impl true
  def handle_call({:unregister, service_name}, _from, state) do
    # Remove from ETS
    :ets.delete(@table_name, service_name)
    
    # Clean up state
    new_state = %{state |
      services: Map.delete(state.services, service_name),
      health_states: Map.delete(state.health_states, service_name),
      circuit_breakers: Map.delete(state.circuit_breakers, service_name)
    }
    
    broadcast_service_event(:unregistered, %{name: service_name})
    
    {:reply, :ok, new_state}
  end

  @impl true
  def handle_call({:lookup, service_name}, _from, state) do
    result = case :ets.lookup(@table_name, service_name) do
      [{^service_name, info}] -> {:ok, info}
      [] -> {:error, :not_found}
    end
    
    {:reply, result, state}
  end

  @impl true
  def handle_call({:lookup_district, district_name}, _from, state) do
    # Find all services belonging to a district
    district_services = :ets.match_object(@table_name, {:_, %{metadata: %{district: district_name}}})
    
    result = case district_services do
      [] -> {:error, :district_not_found}
      services -> {:ok, Enum.map(services, fn {_, info} -> info end)}
    end
    
    {:reply, result, state}
  end

  @impl true
  def handle_call({:get_healthy_instance, service_name}, _from, state) do
    # Check circuit breaker first
    case Map.get(state.circuit_breakers, service_name) do
      %{state: :open} ->
        {:reply, {:error, :circuit_open}, state}
      
      _ ->
        # Get healthy instances using load balancing
        case get_available_instances(service_name, state) do
          [] ->
            {:reply, {:error, :no_healthy_instances}, state}
          
          instances ->
            # Apply load balancing algorithm
            selected = select_instance(instances, state.load_balancer_state)
            update_load_balancer_state(service_name, selected, state)
            {:reply, {:ok, selected}, state}
        end
    end
  end

  @impl true
  def handle_call(:get_mesh_status, _from, state) do
    mesh_status = %{
      total_services: map_size(state.services),
      healthy_services: count_healthy_services(state.health_states),
      unhealthy_services: count_unhealthy_services(state.health_states),
      open_circuits: count_open_circuits(state.circuit_breakers),
      service_graph: build_service_graph(state.services),
      load_distribution: calculate_load_distribution(state.load_balancer_state)
    }
    
    {:reply, mesh_status, state}
  end

  @impl true
  def handle_cast({:report_health, service_name, health_status}, state) do
    case Map.get(state.health_states, service_name) do
      nil ->
        {:noreply, state}
      
      current_health ->
        updated_health = update_health_state(current_health, health_status)
        
        # Update circuit breaker based on health
        updated_breaker = update_circuit_breaker(
          Map.get(state.circuit_breakers, service_name),
          health_status
        )
        
        new_state = %{state |
          health_states: Map.put(state.health_states, service_name, updated_health),
          circuit_breakers: Map.put(state.circuit_breakers, service_name, updated_breaker)
        }
        
        # Broadcast significant health changes
        if current_health.status != updated_health.status do
          broadcast_health_change(service_name, updated_health.status)
        end
        
        {:noreply, new_state}
    end
  end

  @impl true
  def handle_info(:health_check_round, state) do
    # Perform health checks on all registered services
    health_results = perform_health_checks(state.services)
    
    # Update health states
    updated_health_states = Enum.reduce(health_results, state.health_states, fn {service, result}, acc ->
      Map.update(acc, service, default_health_state(), fn current ->
        update_health_from_check(current, result)
      end)
    end)
    
    # Remove stale services
    cleaned_services = remove_stale_services(state.services)
    
    # Schedule next round
    Process.send_after(self(), :health_check_round, @health_check_interval)
    
    new_state = %{state |
      services: cleaned_services,
      health_states: updated_health_states
    }
    
    {:noreply, new_state}
  end

  # Private functions

  defp generate_service_id(service_name) do
    "#{service_name}_#{:crypto.strong_rand_bytes(8) |> Base.encode16(case: :lower)}"
  end

  defp extract_metadata(config) do
    %{
      district: config[:district],
      capabilities: config[:capabilities] || [],
      version: config[:version] || "1.0.0",
      protocol: config[:protocol] || :nats
    }
  end

  defp broadcast_service_event(event_type, service_info) do
    Phoenix.PubSub.broadcast(
      CRODPhoenix.PubSub,
      "service_registry",
      {event_type, service_info}
    )
  end

  defp get_available_instances(service_name, state) do
    # In a real implementation, this would look up multiple instances
    # For now, return single instance if healthy
    case Map.get(state.health_states, service_name) do
      %{status: :healthy} = health ->
        case Map.get(state.services, service_name) do
          nil -> []
          service -> [service]
        end
      _ ->
        []
    end
  end

  defp select_instance(instances, load_balancer_state) do
    # Simple round-robin for now
    # In production, could use weighted round-robin, least connections, etc.
    Enum.random(instances)
  end

  defp update_load_balancer_state(service_name, selected_instance, state) do
    # Track load balancing decisions
    state
  end

  defp update_health_state(current, new_status) do
    %{current |
      status: new_status,
      last_check: DateTime.utc_now(),
      consecutive_failures: if(new_status == :healthy, do: 0, else: current.consecutive_failures + 1)
    }
  end

  defp update_circuit_breaker(breaker, health_status) do
    case {breaker.state, health_status} do
      {:closed, :unhealthy} ->
        failure_count = breaker.failure_count + 1
        if failure_count >= 5 do
          %{breaker | state: :open, failure_count: failure_count, last_failure: DateTime.utc_now()}
        else
          %{breaker | failure_count: failure_count}
        end
      
      {:open, _} ->
        # Check if enough time has passed to try half-open
        if DateTime.diff(DateTime.utc_now(), breaker.last_failure) > 30 do
          %{breaker | state: :half_open, half_open_attempts: 0}
        else
          breaker
        end
      
      {:half_open, :healthy} ->
        %{breaker | state: :closed, failure_count: 0, half_open_attempts: 0}
      
      {:half_open, :unhealthy} ->
        %{breaker | state: :open, last_failure: DateTime.utc_now(), half_open_attempts: breaker.half_open_attempts + 1}
      
      {_, :healthy} ->
        %{breaker | failure_count: 0}
      
      _ ->
        breaker
    end
  end

  defp perform_health_checks(services) do
    # Parallel health checks
    services
    |> Enum.map(fn {name, service} ->
      Task.async(fn -> {name, check_service_health(service)} end)
    end)
    |> Enum.map(&Task.await/1)
    |> Map.new()
  end

  defp check_service_health(service) do
    # Implement actual health check based on service protocol
    # For now, return random health status
    if :rand.uniform() > 0.1, do: :healthy, else: :unhealthy
  end

  defp remove_stale_services(services) do
    now = DateTime.utc_now()
    
    Enum.reduce(services, services, fn {name, service}, acc ->
      if DateTime.diff(now, service.last_seen) > @stale_service_timeout do
        Logger.warn("Removing stale service: #{name}")
        :ets.delete(@table_name, name)
        Map.delete(acc, name)
      else
        acc
      end
    end)
  end

  defp broadcast_health_change(service_name, new_status) do
    Phoenix.PubSub.broadcast(
      CRODPhoenix.PubSub,
      "service_health",
      {:health_changed, service_name, new_status}
    )
  end

  defp default_health_state do
    %{
      status: :unknown,
      last_check: DateTime.utc_now(),
      consecutive_failures: 0,
      response_times: []
    }
  end

  defp update_health_from_check(current, check_result) do
    %{current |
      status: check_result,
      last_check: DateTime.utc_now()
    }
  end

  defp count_healthy_services(health_states) do
    Enum.count(health_states, fn {_, %{status: status}} -> status == :healthy end)
  end

  defp count_unhealthy_services(health_states) do
    Enum.count(health_states, fn {_, %{status: status}} -> status != :healthy end)
  end

  defp count_open_circuits(circuit_breakers) do
    Enum.count(circuit_breakers, fn {_, %{state: state}} -> state == :open end)
  end

  defp build_service_graph(services) do
    # Build dependency graph between services
    # For now, return simplified structure
    %{nodes: Map.keys(services), edges: []}
  end

  defp calculate_load_distribution(load_balancer_state) do
    # Calculate how load is distributed across services
    %{algorithm: :round_robin, distribution: :even}
  end
end