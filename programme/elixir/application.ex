defmodule CRODPhoenix.Application do
  @moduledoc """
  CROD Phoenix Orchestrator - The brain of the polygon city architecture
  """
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # PostgreSQL connection
      CRODPhoenix.Repo,
      # NATS connection
      {Gnat.ConnectionSupervisor, CRODPhoenix.Nats.connection_settings()},
      # Event Store for event sourcing
      CRODPhoenix.EventStore,
      # Commanded application
      CRODPhoenix.App,
      # Phoenix PubSub
      {Phoenix.PubSub, name: CRODPhoenix.PubSub},
      # Finch HTTP client
      {Finch, name: CRODPhoenix.Finch},
      # Phoenix Endpoint
      CRODPhoenixWeb.Endpoint,
      # District supervisors
      {CRODPhoenix.Districts.Supervisor, []},
      # CROD Parasite Core
      {CRODPhoenix.Parasite.Core, []},
      # Polygon City Manager
      {CRODPhoenix.PolygonCity.Manager, []},
      # Inter-service communication registry
      {CRODPhoenix.ServiceRegistry, []},
      # Telemetry and monitoring
      CRODPhoenixWeb.Telemetry
    ]

    opts = [strategy: :one_for_one, name: CRODPhoenix.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    CRODPhoenixWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end