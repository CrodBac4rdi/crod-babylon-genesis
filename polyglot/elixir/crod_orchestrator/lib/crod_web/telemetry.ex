defmodule CRODWeb.Telemetry do
  use Supervisor
  import Telemetry.Metrics

  def start_link(arg) do
    Supervisor.start_link(__MODULE__, arg, name: __MODULE__)
  end

  @impl true
  def init(_arg) do
    children = [
      # Telemetry poller will execute the given period measurements
      # every 10_000ms. Learn more here: https://hexdocs.pm/telemetry_metrics
      {:telemetry_poller, measurements: periodic_measurements(), period: 10_000}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

  def metrics do
    [
      # CROD Metrics
      summary("crod.orchestrator.action.duration",
        unit: {:native, :millisecond},
        tags: [:action_type]
      ),
      counter("crod.orchestrator.action.count",
        tags: [:action_type, :status]
      ),
      
      # City Metrics
      last_value("crod.city.districts.count"),
      last_value("crod.city.buildings.count"),
      last_value("crod.city.connections.count"),
      last_value("crod.city.efficiency"),
      
      # Permission Metrics
      counter("crod.permission.requests.count",
        tags: [:decision]
      ),
      summary("crod.permission.response_time",
        unit: {:native, :millisecond}
      ),
      
      # EventStore Metrics
      counter("crod.events.count",
        tags: [:event_type]
      ),
      last_value("crod.events.total"),
      
      # Delta Control Metrics
      last_value("crod.delta.enabled_features.count"),
      counter("crod.delta.emergency_stops.count"),
      
      # Sandbox Metrics
      counter("crod.sandbox.experiments.count",
        tags: [:status]
      ),
      summary("crod.sandbox.simulation.duration",
        unit: {:native, :second}
      ),

      # Database Metrics
      summary("crod_orchestrator.repo.query.total_time",
        unit: {:native, :millisecond},
        description: "The sum of the other measurements"
      ),
      summary("crod_orchestrator.repo.query.decode_time",
        unit: {:native, :millisecond},
        description: "The time spent decoding the data received from the database"
      ),
      summary("crod_orchestrator.repo.query.query_time",
        unit: {:native, :millisecond},
        description: "The time spent executing the query"
      ),
      summary("crod_orchestrator.repo.query.queue_time",
        unit: {:native, :millisecond},
        description: "The time spent waiting for a database connection"
      ),
      summary("crod_orchestrator.repo.query.idle_time",
        unit: {:native, :millisecond},
        description: "The time the connection spent waiting before being checked out for the query"
      ),

      # VM Metrics
      summary("vm.memory.total", unit: {:byte, :kilobyte}),
      summary("vm.total_run_queue_lengths.total"),
      summary("vm.total_run_queue_lengths.cpu"),
      summary("vm.total_run_queue_lengths.io")
    ]
  end

  defp periodic_measurements do
    [
      # A module, function and arguments to be invoked periodically.
      {__MODULE__, :emit_city_metrics, []},
      {__MODULE__, :emit_orchestrator_metrics, []},
      {__MODULE__, :emit_delta_metrics, []}
    ]
  end

  def emit_city_metrics do
    case CROD.City.calculate_resources() do
      {:ok, resources} ->
        :telemetry.execute(
          [:crod, :city, :districts],
          %{count: resources.districts},
          %{}
        )
        :telemetry.execute(
          [:crod, :city, :buildings],
          %{count: resources.buildings},
          %{}
        )
        :telemetry.execute(
          [:crod, :city, :connections],
          %{count: resources.connections},
          %{}
        )
      _ ->
        :ok
    end
  end

  def emit_orchestrator_metrics do
    case CROD.Orchestrator.status() do
      {:ok, status} ->
        :telemetry.execute(
          [:crod, :orchestrator, :status],
          %{
            pending_actions: status.pending_actions,
            trust_level: trust_level_to_number(status.trust_level)
          },
          %{}
        )
      _ ->
        :ok
    end
  end

  def emit_delta_metrics do
    case CROD.Delta.get_status() do
      {:ok, status} ->
        :telemetry.execute(
          [:crod, :delta, :enabled_features],
          %{count: length(status.enabled_features)},
          %{}
        )
      _ ->
        :ok
    end
  end

  defp trust_level_to_number(:cautious), do: 1
  defp trust_level_to_number(:friendly), do: 2
  defp trust_level_to_number(:trusted), do: 3
  defp trust_level_to_number(_), do: 0
end