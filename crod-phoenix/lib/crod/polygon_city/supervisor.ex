defmodule Crod.PolygonCity.Supervisor do
  @moduledoc """
  Supervisor for the Polygon City architecture.
  Manages all district processes and their interactions.
  """

  use Supervisor

  def start_link(opts) do
    Supervisor.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    children = [
      # Core districts
      {Crod.PolygonCity.Districts.Orchestrator, []},
      {Crod.PolygonCity.Districts.Memory, []},
      {Crod.PolygonCity.Districts.Interface, []},
      
      # District registry
      {Registry, keys: :unique, name: Crod.PolygonCity.Registry},
      
      # Inter-district communication
      {Crod.PolygonCity.MessageBroker, []},
      
      # Health monitor
      {Crod.PolygonCity.HealthMonitor, []}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

  @doc """
  Gets the status of all districts.
  """
  def district_status do
    districts = Application.get_env(:crod, :polygon_city)[:districts]
    
    Enum.map(districts, fn district ->
      pid = get_district_pid(district)
      
      %{
        district: district,
        pid: pid,
        alive?: is_pid(pid) and Process.alive?(pid),
        info: get_district_info(district)
      }
    end)
  end

  @doc """
  Restarts a specific district.
  """
  def restart_district(district) do
    case get_district_pid(district) do
      nil ->
        {:error, :district_not_found}
      
      pid ->
        Supervisor.terminate_child(__MODULE__, pid)
        Supervisor.restart_child(__MODULE__, pid)
    end
  end

  # Private functions

  defp get_district_pid(district) do
    case Registry.lookup(Crod.PolygonCity.Registry, district) do
      [{pid, _}] -> pid
      [] -> nil
    end
  end

  defp get_district_info(district) do
    case get_district_pid(district) do
      nil -> %{status: :not_running}
      pid -> GenServer.call(pid, :get_info, 5_000) rescue _ -> %{status: :error}
    end
  end
end