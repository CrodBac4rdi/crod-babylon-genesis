defmodule CrodRathaus.EventStore do
  @moduledoc """
  Event sourcing implementation for CROD Rathaus.
  Stores all district events in PostgreSQL for audit and replay capabilities.
  """
  
  use GenServer
  require Logger
  import Ecto.Query
  alias CrodRathaus.Repo
  alias CrodRathaus.Event
  
  def start_link(_opts) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end
  
  def init(_) do
    # Subscribe to NATS events
    Phoenix.PubSub.subscribe(CrodRathaus.PubSub, "nats:events")
    
    {:ok, %{
      event_count: 0,
      last_snapshot: DateTime.utc_now()
    }}
  end
  
  # Public API
  
  def store_event(aggregate_id, event_type, event_data, metadata \\ %{}) do
    GenServer.call(__MODULE__, {:store_event, aggregate_id, event_type, event_data, metadata})
  end
  
  def get_events(aggregate_id, from_version \\ 0) do
    Event
    |> where([e], e.aggregate_id == ^aggregate_id and e.version > ^from_version)
    |> order_by([e], asc: e.version)
    |> Repo.all()
  end
  
  def get_latest_snapshot(aggregate_id) do
    Event
    |> where([e], e.aggregate_id == ^aggregate_id and e.event_type == "snapshot")
    |> order_by([e], desc: e.version)
    |> limit(1)
    |> Repo.one()
  end
  
  def replay_events(aggregate_id, handler_fn) do
    aggregate_id
    |> get_events()
    |> Enum.reduce(%{}, fn event, state ->
      handler_fn.(event, state)
    end)
  end
  
  # GenServer callbacks
  
  def handle_call({:store_event, aggregate_id, event_type, event_data, metadata}, _from, state) do
    # Get next version number
    version = get_next_version(aggregate_id)
    
    # Create event
    event_params = %{
      aggregate_id: aggregate_id,
      event_type: event_type,
      event_data: event_data,
      metadata: Map.merge(metadata, %{
        "timestamp" => DateTime.utc_now(),
        "node" => node()
      }),
      version: version,
      created_at: DateTime.utc_now()
    }
    
    case Repo.insert(Event.changeset(%Event{}, event_params)) do
      {:ok, event} ->
        # Broadcast event
        Phoenix.PubSub.broadcast(
          CrodRathaus.PubSub,
          "events:#{aggregate_id}",
          {:event_stored, event}
        )
        
        # Update state
        new_state = %{state | event_count: state.event_count + 1}
        
        # Check if we need to create a snapshot
        new_state = maybe_create_snapshot(aggregate_id, new_state)
        
        {:reply, {:ok, event}, new_state}
        
      {:error, changeset} ->
        Logger.error("Failed to store event: #{inspect(changeset.errors)}")
        {:reply, {:error, changeset}, state}
    end
  end
  
  def handle_info({:nats_event, topic, data}, state) do
    # Store NATS events automatically
    aggregate_id = extract_aggregate_id(topic)
    event_type = extract_event_type(topic)
    
    case store_event(aggregate_id, event_type, data, %{"source" => "nats", "topic" => topic}) do
      {:ok, _event} ->
        Logger.debug("Stored NATS event: #{topic}")
      {:error, reason} ->
        Logger.error("Failed to store NATS event: #{inspect(reason)}")
    end
    
    {:noreply, state}
  end
  
  # Private functions
  
  defp get_next_version(aggregate_id) do
    Event
    |> where([e], e.aggregate_id == ^aggregate_id)
    |> select([e], max(e.version))
    |> Repo.one()
    |> Kernel.||(0)
    |> Kernel.+(1)
  end
  
  defp maybe_create_snapshot(aggregate_id, state) do
    # Create snapshot every 100 events or every hour
    if state.event_count >= 100 or 
       DateTime.diff(DateTime.utc_now(), state.last_snapshot) >= 3600 do
      
      create_snapshot(aggregate_id)
      
      %{state | 
        event_count: 0,
        last_snapshot: DateTime.utc_now()
      }
    else
      state
    end
  end
  
  defp create_snapshot(aggregate_id) do
    # Replay all events to get current state
    current_state = replay_events(aggregate_id, &apply_event/2)
    
    # Store snapshot
    store_event(
      aggregate_id,
      "snapshot",
      current_state,
      %{"snapshot_reason" => "periodic"}
    )
    
    Logger.info("Created snapshot for aggregate: #{aggregate_id}")
  end
  
  defp apply_event(%{event_type: "district_registered"} = event, state) do
    Map.put(state, event.event_data["district_id"], %{
      status: "active",
      registered_at: event.created_at,
      data: event.event_data
    })
  end
  
  defp apply_event(%{event_type: "district_updated"} = event, state) do
    district_id = event.event_data["district_id"]
    Map.update(state, district_id, %{}, fn district ->
      Map.merge(district, event.event_data)
    end)
  end
  
  defp apply_event(%{event_type: "district_offline"} = event, state) do
    district_id = event.event_data["district_id"]
    put_in(state, [district_id, :status], "offline")
  end
  
  defp apply_event(%{event_type: "snapshot"} = event, _state) do
    # Replace entire state with snapshot
    event.event_data
  end
  
  defp apply_event(_event, state), do: state
  
  defp extract_aggregate_id("district." <> rest) do
    [district_id | _] = String.split(rest, ".")
    "district:#{district_id}"
  end
  defp extract_aggregate_id(topic), do: "system:#{topic}"
  
  defp extract_event_type("district." <> rest) do
    case String.split(rest, ".") do
      [_district_id, action] -> "district_#{action}"
      _ -> "district_event"
    end
  end
  defp extract_event_type(_topic), do: "system_event"
  
  # Public utility functions for scheduled jobs
  
  def create_snapshots do
    # Get all unique aggregate IDs
    aggregate_ids = 
      Event
      |> select([e], e.aggregate_id)
      |> distinct(true)
      |> Repo.all()
    
    Enum.each(aggregate_ids, &create_snapshot/1)
  end
  
  def cleanup_old_events do
    # Delete events older than 7 days that have been snapshotted
    seven_days_ago = DateTime.add(DateTime.utc_now(), -7, :day)
    
    Event
    |> where([e], e.created_at < ^seven_days_ago)
    |> where([e], e.event_type != "snapshot")
    |> Repo.delete_all()
    
    Logger.info("Cleaned up old events")
  end
end