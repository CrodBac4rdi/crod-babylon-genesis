defmodule CrodRathaus.DistrictMonitor do
  use GenServer
  require Logger

  @check_interval 10_000

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def init(_) do
    schedule_check()
    {:ok, %{districts: %{}, stats: %{}}}
  end

  def handle_info(:check_districts, state) do
    districts = [
      %{name: :parasit, url: "http://localhost:6666/health"},
      %{name: :pattern, url: "http://localhost:7007/health"},
      %{name: :memory, url: "http://localhost:7031/health"},
      %{name: :gateway, url: "http://localhost:7888/health"}
    ]

    new_state = 
      districts
      |> Enum.map(&check_district/1)
      |> Enum.reduce(state, fn {name, status}, acc ->
        put_in(acc, [:districts, name], status)
      end)

    broadcast_update(new_state.districts)
    schedule_check()
    {:noreply, new_state}
  end

  defp check_district(%{name: name, url: url}) do
    status = 
      case HTTPoison.get(url, [], timeout: 2000, recv_timeout: 2000) do
        {:ok, %{status_code: 200, body: body}} ->
          %{status: :online, data: Jason.decode!(body), last_seen: DateTime.utc_now()}
        _ ->
          %{status: :offline, data: nil, last_seen: nil}
      end
    
    {name, status}
  end

  defp broadcast_update(districts) do
    Phoenix.PubSub.broadcast(
      CrodRathaus.PubSub,
      "districts:monitor",
      {:districts_update, districts}
    )
  end

  defp schedule_check do
    Process.send_after(self(), :check_districts, @check_interval)
  end

  def get_status do
    GenServer.call(__MODULE__, :get_status)
  end

  def handle_call(:get_status, _from, state) do
    {:reply, state.districts, state}
  end
end