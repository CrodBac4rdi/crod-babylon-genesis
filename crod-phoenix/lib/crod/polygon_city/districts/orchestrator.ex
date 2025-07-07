defmodule Crod.PolygonCity.Districts.Orchestrator do
  @moduledoc """
  The Orchestrator district manages coordination between all other districts.
  It handles request routing, load balancing, and workflow orchestration.
  """

  use GenServer
  require Logger

  alias Crod.Services.NatsClient
  alias Crod.PolygonCity.MessageBroker

  @district_name :orchestrator

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: via_tuple())
  end

  @impl true
  def init(_opts) do
    # Register with registry
    {:ok, _} = Registry.register(Crod.PolygonCity.Registry, @district_name, %{})
    
    # Subscribe to orchestration events
    NatsClient.subscribe("crod.orchestrator.*")
    
    state = %{
      workflows: %{},
      active_requests: %{},
      district_health: %{},
      metrics: init_metrics()
    }
    
    # Start health check timer
    Process.send_after(self(), :health_check, 10_000)
    
    {:ok, state}
  end

  # Public API

  @doc """
  Orchestrates a request through the appropriate districts.
  """
  def orchestrate(request) do
    GenServer.call(via_tuple(), {:orchestrate, request})
  end

  @doc """
  Creates a new workflow.
  """
  def create_workflow(steps) do
    GenServer.call(via_tuple(), {:create_workflow, steps})
  end

  @doc """
  Gets the current orchestrator status.
  """
  def get_status do
    GenServer.call(via_tuple(), :get_status)
  end

  # GenServer callbacks

  @impl true
  def handle_call({:orchestrate, request}, from, state) do
    request_id = generate_request_id()
    
    # Determine routing strategy
    routing = determine_routing(request)
    
    # Create workflow for request
    workflow = create_request_workflow(request, routing)
    
    # Start workflow execution
    Task.start(fn ->
      result = execute_workflow(workflow, request_id, state)
      GenServer.reply(from, result)
    end)
    
    # Track active request
    active_requests = Map.put(state.active_requests, request_id, %{
      from: from,
      started_at: DateTime.utc_now(),
      workflow: workflow
    })
    
    {:noreply, %{state | active_requests: active_requests}}
  end

  @impl true
  def handle_call({:create_workflow, steps}, _from, state) do
    workflow_id = generate_workflow_id()
    
    workflow = %{
      id: workflow_id,
      steps: steps,
      created_at: DateTime.utc_now(),
      status: :created
    }
    
    workflows = Map.put(state.workflows, workflow_id, workflow)
    
    {:reply, {:ok, workflow_id}, %{state | workflows: workflows}}
  end

  @impl true
  def handle_call(:get_status, _from, state) do
    status = %{
      active_requests: map_size(state.active_requests),
      workflows: map_size(state.workflows),
      district_health: state.district_health,
      metrics: state.metrics
    }
    
    {:reply, status, state}
  end

  @impl true
  def handle_call(:get_info, _from, state) do
    info = %{
      district: @district_name,
      active_requests: map_size(state.active_requests),
      workflows: map_size(state.workflows)
    }
    
    {:reply, info, state}
  end

  @impl true
  def handle_info(:health_check, state) do
    # Check health of all districts
    districts = Application.get_env(:crod, :polygon_city)[:districts]
    
    health = Enum.map(districts, fn district ->
      {district, check_district_health(district)}
    end)
    |> Map.new()
    
    # Schedule next health check
    Process.send_after(self(), :health_check, 10_000)
    
    {:noreply, %{state | district_health: health}}
  end

  @impl true
  def handle_info({:nats_message, topic, message}, state) do
    Logger.info("Orchestrator received NATS message on #{topic}")
    
    # Handle orchestration-related messages
    case parse_topic(topic) do
      {:orchestrator, action} ->
        handle_orchestration_message(action, message, state)
      
      _ ->
        {:noreply, state}
    end
  end

  @impl true
  def handle_info({:workflow_complete, request_id, result}, state) do
    case Map.get(state.active_requests, request_id) do
      nil ->
        {:noreply, state}
      
      request ->
        # Update metrics
        duration = DateTime.diff(DateTime.utc_now(), request.started_at, :millisecond)
        metrics = update_metrics(state.metrics, :completed, duration)
        
        # Clean up
        active_requests = Map.delete(state.active_requests, request_id)
        
        {:noreply, %{state | active_requests: active_requests, metrics: metrics}}
    end
  end

  # Private functions

  defp via_tuple do
    {:via, Registry, {Crod.PolygonCity.Registry, @district_name}}
  end

  defp generate_request_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end

  defp generate_workflow_id do
    "workflow_" <> (:crypto.strong_rand_bytes(8) |> Base.encode16())
  end

  defp determine_routing(request) do
    # Analyze request to determine which districts to involve
    cond do
      Map.has_key?(request, :llm_interaction) ->
        [:parasite, :neural]
      
      Map.has_key?(request, :data_query) ->
        [:memory, :interface]
      
      true ->
        [:interface]
    end
  end

  defp create_request_workflow(request, routing) do
    steps = Enum.map(routing, fn district ->
      %{
        district: district,
        action: determine_district_action(district, request),
        params: extract_district_params(district, request)
      }
    end)
    
    %{
      steps: steps,
      parallel: can_parallelize?(steps),
      timeout: 30_000
    }
  end

  defp determine_district_action(:parasite, %{llm_interaction: _}), do: :interpret
  defp determine_district_action(:neural, _), do: :process
  defp determine_district_action(:memory, _), do: :query
  defp determine_district_action(:interface, _), do: :render
  defp determine_district_action(_, _), do: :process

  defp extract_district_params(district, request) do
    Map.get(request, district, %{})
  end

  defp can_parallelize?(steps) do
    # Simple heuristic - can parallelize if no dependencies
    length(steps) > 1 and not has_dependencies?(steps)
  end

  defp has_dependencies?(steps) do
    # Check if any step depends on another
    # For now, assume parasite must run before neural
    Enum.any?(steps, fn step ->
      step.district == :neural and Enum.any?(steps, &(&1.district == :parasite))
    end)
  end

  defp execute_workflow(workflow, request_id, state) do
    try do
      results = if workflow.parallel do
        execute_parallel_steps(workflow.steps, request_id)
      else
        execute_sequential_steps(workflow.steps, request_id)
      end
      
      {:ok, results}
    catch
      :exit, reason ->
        Logger.error("Workflow #{request_id} failed: #{inspect(reason)}")
        {:error, reason}
    end
  end

  defp execute_parallel_steps(steps, request_id) do
    tasks = Enum.map(steps, fn step ->
      Task.async(fn ->
        execute_step(step, request_id)
      end)
    end)
    
    Enum.map(tasks, &Task.await(&1, 10_000))
  end

  defp execute_sequential_steps(steps, request_id) do
    Enum.reduce(steps, [], fn step, results ->
      result = execute_step(step, request_id)
      results ++ [result]
    end)
  end

  defp execute_step(step, request_id) do
    MessageBroker.send_to_district(step.district, {
      :execute,
      step.action,
      step.params,
      request_id
    })
  end

  defp check_district_health(district) do
    case MessageBroker.ping_district(district) do
      {:ok, _} -> :healthy
      {:error, _} -> :unhealthy
    end
  end

  defp parse_topic(topic) do
    case String.split(topic, ".") do
      ["crod", district, action] ->
        {String.to_atom(district), String.to_atom(action)}
      
      _ ->
        {:unknown, topic}
    end
  end

  defp handle_orchestration_message(action, message, state) do
    case action do
      :request ->
        # Handle new orchestration request
        Task.start(fn ->
          orchestrate(message)
        end)
        {:noreply, state}
      
      _ ->
        {:noreply, state}
    end
  end

  defp init_metrics do
    %{
      total_requests: 0,
      completed_requests: 0,
      failed_requests: 0,
      average_duration: 0
    }
  end

  defp update_metrics(metrics, :completed, duration) do
    total = metrics.completed_requests + 1
    avg = ((metrics.average_duration * metrics.completed_requests) + duration) / total
    
    %{metrics |
      total_requests: metrics.total_requests + 1,
      completed_requests: total,
      average_duration: avg
    }
  end
end