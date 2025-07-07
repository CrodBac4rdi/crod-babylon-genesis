defmodule CrodRathaus.NATS do
  use GenServer
  require Logger

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end

  def init(_) do
    # Get NATS host from environment
    nats_host = System.get_env("NATS_HOST", "localhost")
    
    # Subscribe to all district topics
    {:ok, _sid1} = Gnat.sub(:gnat, self(), "district.>")
    {:ok, _sid2} = Gnat.sub(:gnat, self(), "pattern.>")
    {:ok, _sid3} = Gnat.sub(:gnat, self(), "trinity.>")
    {:ok, _sid4} = Gnat.sub(:gnat, self(), "city.>")
    
    Logger.info("NATS subscriptions created successfully to #{nats_host}")
    {:ok, %{metrics: %{}, subscriptions: []}}
  end

  def handle_info({:msg, %{topic: topic, body: body}}, state) do
    # Parse message
    data = Jason.decode!(body)
    
    # Broadcast to LiveView
    CrodRathausWeb.Endpoint.broadcast("dashboard:lobby", "district_update", %{
      topic: topic,
      data: data,
      timestamp: System.system_time(:millisecond)
    })
    
    # Update metrics
    metrics = Map.update(state.metrics, topic, 1, &(&1 + 1))
    
    {:noreply, %{state | metrics: metrics}}
  end

  def handle_info(:retry_connect, state) do
    # Retry NATS connection
    init([])
  end

  # Public API
  def publish(topic, data) do
    GenServer.call(__MODULE__, {:publish, topic, data})
  end

  def handle_call({:publish, topic, data}, _from, state) do
    body = Jason.encode!(data)
    case Gnat.pub(:gnat, topic, body) do
      :ok ->
        {:reply, :ok, state}
      error ->
        {:reply, error, state}
    end
  end
end