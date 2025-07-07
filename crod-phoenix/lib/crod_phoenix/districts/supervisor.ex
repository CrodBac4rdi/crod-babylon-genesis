defmodule CRODPhoenix.Districts.Supervisor do
  @moduledoc """
  Supervisor for all Polygon City districts
  Each district runs its own supervision tree with language-specific services
  """
  use DynamicSupervisor
  require Logger

  def start_link(init_arg) do
    DynamicSupervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end

  def start_district(name, config) do
    child_spec = build_district_spec(name, config)
    DynamicSupervisor.start_child(__MODULE__, child_spec)
  end

  def stop_district(name) do
    case Registry.lookup(CRODPhoenix.DistrictRegistry, name) do
      [{pid, _}] -> DynamicSupervisor.terminate_child(__MODULE__, pid)
      [] -> {:error, :not_found}
    end
  end

  def restart_district(name) do
    with :ok <- stop_district(name),
         config <- get_district_config(name),
         {:ok, _} <- start_district(name, config) do
      :ok
    end
  end

  defp build_district_spec(name, config) do
    case config.role do
      :orchestrator ->
        {CRODPhoenix.Districts.ElixirDistrict, name: name, config: config}
      
      :performance ->
        {CRODPhoenix.Districts.RustDistrict, name: name, config: config}
      
      :ai_intelligence ->
        {CRODPhoenix.Districts.PythonDistrict, name: name, config: config}
      
      :networking ->
        {CRODPhoenix.Districts.GoDistrict, name: name, config: config}
      
      :frontend ->
        {CRODPhoenix.Districts.JavaScriptDistrict, name: name, config: config}
      
      :computation ->
        {CRODPhoenix.Districts.QuantumDistrict, name: name, config: config}
      
      _ ->
        {CRODPhoenix.Districts.GenericDistrict, name: name, config: config}
    end
  end

  defp get_district_config(name) do
    # Retrieve district configuration from polygon city manager
    CRODPhoenix.PolygonCity.Manager.get_district_config(name)
  end
end