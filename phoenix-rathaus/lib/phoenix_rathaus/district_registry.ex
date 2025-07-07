defmodule PhoenixRathaus.DistrictRegistry do
  use GenServer
  require Logger

  @districts %{
    python_parasit: %{port: 6666, status: :offline, health_check: "/health"},
    rust_pattern: %{port: 7007, status: :offline, health_check: "/health"}, 
    go_memory: %{port: 7031, status: :offline, health_check: "/health"},
    js_gateway: %{port: 7888, status: :offline, health_check: "/health"}
  }

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  @impl true
  def init(_) do
    Logger.info("🏛️ Phoenix Rathaus initializing district registry...")
    
    # Subscribe to NATS for district announcements
    {:ok, _sub} = Gnat.sub(:gnat, self(), "district.announce")
    
    # Schedule health checks
    Process.send_after(self(), :health_check, 5_000)
    
    {:ok, %{districts: @districts, subscriptions: []}}
  end

  @impl true
  def handle_info({:msg, %{body: body, topic: "district.announce"}}, state) do
    case Jason.decode(body) do
      {:ok, %{"district" => district, "status" => status}} ->
        Logger.info("📢 District announcement: #{district} is #{status}")
        new_districts = update_district_status(state.districts, district, status)
        broadcast_district_update(district, status)
        {:noreply, %{state | districts: new_districts}}
      _ ->
        {:noreply, state}
    end
  end

  @impl true
  def handle_info(:health_check, state) do
    new_districts = Enum.reduce(state.districts, %{}, fn {name, config}, acc ->
      status = check_district_health(name, config)
      Map.put(acc, name, %{config | status: status})
    end)
    
    Process.send_after(self(), :health_check, 10_000)
    {:noreply, %{state | districts: new_districts}}
  end

  @impl true
  def handle_call(:get_districts, _from, state) do
    {:reply, state.districts, state}
  end

  @impl true
  def handle_call({:get_district, name}, _from, state) do
    {:reply, Map.get(state.districts, name), state}
  end

  defp update_district_status(districts, district_name, status) do
    district_atom = String.to_existing_atom(district_name)
    case Map.get(districts, district_atom) do
      nil -> districts
      config -> Map.put(districts, district_atom, %{config | status: String.to_atom(status)})
    end
  end

  defp check_district_health(name, %{port: port, health_check: endpoint}) do
    url = "http://localhost:#{port}#{endpoint}"
    case HTTPoison.get(url, [], timeout: 2_000, recv_timeout: 2_000) do
      {:ok, %{status_code: 200}} -> :online
      _ -> :offline
    end
  end

  defp broadcast_district_update(district, status) do
    Phoenix.PubSub.broadcast(
      PhoenixRathaus.PubSub,
      "districts",
      {:district_update, district, status}
    )
  end

  # Public API
  def get_districts, do: GenServer.call(__MODULE__, :get_districts)
  def get_district(name), do: GenServer.call(__MODULE__, {:get_district, name})
end