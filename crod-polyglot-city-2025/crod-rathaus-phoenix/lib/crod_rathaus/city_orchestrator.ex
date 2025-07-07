defmodule CrodRathaus.CityOrchestrator do
  use GenServer
  require Logger

  @districts %{
    parasit: %{name: "Python Parasit", port: 6666, subject: "crod.parasit.*"},
    pattern: %{name: "Rust Pattern", port: 7007, subject: "crod.pattern.*"},
    memory: %{name: "Go Memory", port: 7031, subject: "crod.memory.*"},
    gateway: %{name: "JS Gateway", port: 7888, subject: "crod.gateway.*"}
  }

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def init(_) do
    Logger.info("🔥 CROD City Orchestrator starting on port 4000...")
    schedule_health_check()
    {:ok, %{districts: @districts, status: %{}, last_check: nil}}
  end

  def handle_info(:check_districts, state) do
    status = check_all_districts()
    broadcast_status(status)
    schedule_health_check()
    {:noreply, %{state | status: status, last_check: DateTime.utc_now()}}
  end

  def handle_call(:get_status, _from, state) do
    {:reply, state.status, state}
  end

  defp check_all_districts do
    @districts
    |> Enum.map(fn {key, district} ->
      {key, check_district_health(district)}
    end)
    |> Enum.into(%{})
  end

  defp check_district_health(district) do
    case CrodRathaus.Nats.request(district.subject <> ".health", %{type: "ping", from: "rathaus"}, 1000) do
      {:ok, response} -> 
        %{status: :online, message: response, last_seen: DateTime.utc_now()}
      {:error, reason} -> 
        %{status: :offline, message: inspect(reason), last_seen: nil}
    end
  end

  def send_heartbeat do
    Logger.debug("Sending Rathaus heartbeat...")
    CrodRathaus.Nats.publish("crod.rathaus.heartbeat", %{
      district: "rathaus",
      type: "orchestrator",
      timestamp: DateTime.utc_now(),
      status: "healthy",
      trinity: Application.get_env(:crod_rathaus, :trinity_values)
    })
  end

  defp broadcast_status(status) do
    Phoenix.PubSub.broadcast(CrodRathaus.PubSub, "city:status", {:district_update, status})
  end

  defp schedule_health_check do
    Process.send_after(self(), :check_districts, 5_000)
  end
end