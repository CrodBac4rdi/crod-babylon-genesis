defmodule CROD.EventStore do
  @moduledoc """
  Event sourcing for immutable history of all CROD actions.
  
  Every action CROD takes is recorded here, creating an
  immutable audit trail and enabling time-travel debugging.
  """

  use GenServer
  require Logger

  @table_name :crod_events
  @snapshot_interval 1000  # Create snapshot every 1000 events

  defstruct [
    :events,
    :snapshots,
    :event_count,
    :last_snapshot_at,
    :subscribers
  ]

  # Client API

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def record_event(event_type, payload) do
    GenServer.call(__MODULE__, {:record_event, event_type, payload})
  end

  def get_events(from_id \\ 0, limit \\ 100) do
    GenServer.call(__MODULE__, {:get_events, from_id, limit})
  end

  def get_events_by_type(event_type, limit \\ 100) do
    GenServer.call(__MODULE__, {:get_events_by_type, event_type, limit})
  end

  def replay_events(from_id, to_id, callback) do
    GenServer.call(__MODULE__, {:replay_events, from_id, to_id, callback})
  end

  def create_snapshot do
    GenServer.call(__MODULE__, :create_snapshot)
  end

  def get_latest_snapshot do
    GenServer.call(__MODULE__, :get_latest_snapshot)
  end

  def subscribe(subscriber_pid) do
    GenServer.call(__MODULE__, {:subscribe, subscriber_pid})
  end

  def unsubscribe(subscriber_pid) do
    GenServer.call(__MODULE__, {:unsubscribe, subscriber_pid})
  end

  def get_statistics do
    GenServer.call(__MODULE__, :get_statistics)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    # Create ETS table for fast event access
    :ets.new(@table_name, [:ordered_set, :named_table, :public])
    
    {:ok, %__MODULE__{
      events: [],
      snapshots: %{},
      event_count: 0,
      last_snapshot_at: 0,
      subscribers: []
    }}
  end

  @impl true
  def handle_call({:record_event, event_type, payload}, _from, state) do
    event_id = state.event_count + 1
    
    event = %{
      id: event_id,
      type: event_type,
      payload: payload,
      timestamp: DateTime.utc_now(),
      actor: get_actor(),
      metadata: %{
        node: node(),
        version: "1.0.0"
      }
    }
    
    # Store in ETS for fast access
    :ets.insert(@table_name, {event_id, event})
    
    # Notify subscribers
    notify_subscribers(event, state.subscribers)
    
    # Check if we need a snapshot
    new_state = %{state | 
      events: [event | state.events],
      event_count: event_id
    }
    
    new_state = maybe_create_snapshot(new_state)
    
    Logger.debug("Event recorded: #{event_type} ##{event_id}")
    
    {:reply, {:ok, event_id}, new_state}
  end

  @impl true
  def handle_call({:get_events, from_id, limit}, _from, state) do
    events = :ets.select(@table_name, [
      {{:"$1", :"$2"}, [{:>=, :"$1", from_id}], [:"$2"]}
    ])
    |> Enum.take(limit)
    
    {:reply, {:ok, events}, state}
  end

  @impl true
  def handle_call({:get_events_by_type, event_type, limit}, _from, state) do
    events = :ets.select(@table_name, [
      {{:"$1", :"$2"}, [{:==, {:map_get, :type, :"$2"}, event_type}], [:"$2"]}
    ])
    |> Enum.take(limit)
    |> Enum.reverse()
    
    {:reply, {:ok, events}, state}
  end

  @impl true
  def handle_call({:replay_events, from_id, to_id, callback}, _from, state) do
    Task.start(fn ->
      replay_range(from_id, to_id, callback)
    end)
    
    {:reply, :ok, state}
  end

  @impl true
  def handle_call(:create_snapshot, _from, state) do
    snapshot = create_snapshot_data(state)
    snapshot_id = state.event_count
    
    new_snapshots = Map.put(state.snapshots, snapshot_id, snapshot)
    new_state = %{state | 
      snapshots: new_snapshots,
      last_snapshot_at: snapshot_id
    }
    
    Logger.info("Snapshot created at event ##{snapshot_id}")
    
    {:reply, {:ok, snapshot_id}, new_state}
  end

  @impl true
  def handle_call(:get_latest_snapshot, _from, state) do
    if state.last_snapshot_at > 0 do
      snapshot = Map.get(state.snapshots, state.last_snapshot_at)
      {:reply, {:ok, snapshot}, state}
    else
      {:reply, {:error, :no_snapshots}, state}
    end
  end

  @impl true
  def handle_call({:subscribe, pid}, _from, state) do
    Process.monitor(pid)
    new_subscribers = [pid | state.subscribers] |> Enum.uniq()
    {:reply, :ok, %{state | subscribers: new_subscribers}}
  end

  @impl true
  def handle_call({:unsubscribe, pid}, _from, state) do
    new_subscribers = List.delete(state.subscribers, pid)
    {:reply, :ok, %{state | subscribers: new_subscribers}}
  end

  @impl true
  def handle_call(:get_statistics, _from, state) do
    stats = %{
      total_events: state.event_count,
      snapshot_count: map_size(state.snapshots),
      last_snapshot_at: state.last_snapshot_at,
      subscribers: length(state.subscribers),
      events_since_snapshot: state.event_count - state.last_snapshot_at,
      event_types: count_event_types()
    }
    
    {:reply, {:ok, stats}, state}
  end

  @impl true
  def handle_info({:DOWN, _ref, :process, pid, _reason}, state) do
    new_subscribers = List.delete(state.subscribers, pid)
    {:noreply, %{state | subscribers: new_subscribers}}
  end

  # Private Functions

  defp get_actor do
    # In a real system, this would identify the actual actor
    "CROD.System"
  end

  defp notify_subscribers(event, subscribers) do
    Enum.each(subscribers, fn pid ->
      send(pid, {:crod_event, event})
    end)
  end

  defp maybe_create_snapshot(state) do
    events_since_snapshot = state.event_count - state.last_snapshot_at
    
    if events_since_snapshot >= @snapshot_interval do
      snapshot = create_snapshot_data(state)
      new_snapshots = Map.put(state.snapshots, state.event_count, snapshot)
      
      Logger.info("Auto-snapshot created at event ##{state.event_count}")
      
      %{state | 
        snapshots: new_snapshots,
        last_snapshot_at: state.event_count,
        events: []  # Clear in-memory events after snapshot
      }
    else
      state
    end
  end

  defp create_snapshot_data(state) do
    # Get current system state from all components
    {:ok, city_resources} = CROD.City.calculate_resources()
    {:ok, orchestrator_status} = CROD.Orchestrator.status()
    
    %{
      event_id: state.event_count,
      timestamp: DateTime.utc_now(),
      city_state: city_resources,
      orchestrator_state: orchestrator_status,
      metadata: %{
        events_included: state.event_count,
        snapshot_size: calculate_snapshot_size(city_resources, orchestrator_status)
      }
    }
  end

  defp calculate_snapshot_size(city_resources, orchestrator_status) do
    # Simplified size calculation
    city_size = map_size(city_resources) * 100
    orch_size = map_size(orchestrator_status) * 50
    city_size + orch_size
  end

  defp replay_range(from_id, to_id, callback) do
    :ets.select(@table_name, [
      {{:"$1", :"$2"}, 
       [{:>=, :"$1", from_id}, {:"<=", :"$1", to_id}], 
       [:"$2"]}
    ])
    |> Enum.each(fn event ->
      callback.(event)
      Process.sleep(10)  # Simulate replay timing
    end)
  end

  defp count_event_types do
    :ets.foldl(fn {_id, event}, acc ->
      Map.update(acc, event.type, 1, &(&1 + 1))
    end, %{}, @table_name)
  end

  # Public helper module for event analysis

  defmodule Analyzer do
    @moduledoc """
    Tools for analyzing the event stream and finding patterns.
    """

    def find_patterns(event_type, time_window \\ 3600) do
      {:ok, events} = CROD.EventStore.get_events_by_type(event_type, 1000)
      
      events
      |> group_by_time_window(time_window)
      |> analyze_frequency()
      |> detect_anomalies()
    end

    def generate_timeline(from_time, to_time) do
      # Generate a visual timeline of events
      {:ok, all_events} = CROD.EventStore.get_events(0, 10000)
      
      all_events
      |> filter_by_time_range(from_time, to_time)
      |> group_by_type()
      |> format_timeline()
    end

    defp group_by_time_window(events, window_seconds) do
      Enum.group_by(events, fn event ->
        div(DateTime.to_unix(event.timestamp), window_seconds)
      end)
    end

    defp analyze_frequency(grouped_events) do
      Enum.map(grouped_events, fn {window, events} ->
        %{
          window: window,
          count: length(events),
          types: Enum.frequencies_by(events, & &1.type)
        }
      end)
    end

    defp detect_anomalies(frequency_data) do
      avg_count = Enum.sum(Enum.map(frequency_data, & &1.count)) / length(frequency_data)
      
      anomalies = Enum.filter(frequency_data, fn data ->
        data.count > avg_count * 2 or data.count < avg_count * 0.5
      end)
      
      %{
        patterns: frequency_data,
        anomalies: anomalies,
        average_frequency: avg_count
      }
    end

    defp filter_by_time_range(events, from_time, to_time) do
      Enum.filter(events, fn event ->
        DateTime.compare(event.timestamp, from_time) != :lt and
        DateTime.compare(event.timestamp, to_time) != :gt
      end)
    end

    defp group_by_type(events) do
      Enum.group_by(events, & &1.type)
    end

    defp format_timeline(grouped_events) do
      timeline = Enum.map(grouped_events, fn {type, events} ->
        %{
          type: type,
          events: Enum.map(events, &summarize_event/1),
          count: length(events)
        }
      end)
      
      %{
        timeline: timeline,
        total_events: Enum.sum(Enum.map(timeline, & &1.count)),
        event_types: length(timeline)
      }
    end

    defp summarize_event(event) do
      %{
        id: event.id,
        timestamp: event.timestamp,
        summary: generate_event_summary(event)
      }
    end

    defp generate_event_summary(event) do
      case event.type do
        :district_created ->
          "Created district '#{event.payload.name}'"
        :building_created ->
          "Built #{event.payload.type} in district"
        :permission_requested ->
          "Requested permission for #{event.payload.action}"
        _ ->
          "#{event.type} occurred"
      end
    end
  end
end