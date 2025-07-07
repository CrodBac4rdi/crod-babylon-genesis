defmodule PhoenixRathaus.Application do
  @moduledoc false
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # NATS Connection
      {Gnat.ConnectionSupervisor, %{
        name: :gnat,
        connection_settings: [
          %{host: System.get_env("NATS_HOST", "nats"), port: 4222}
        ]
      }},
      # Redis Connection Pool
      {Redix, host: System.get_env("REDIS_HOST", "redis"), name: :redix},
      # NATS Connection Handler
      PhoenixRathaus.NatsConnection,
      # District Registry
      PhoenixRathaus.DistrictRegistry,
      # Pattern Coordinator
      PhoenixRathaus.PatternCoordinator,
      # Memory Manager
      PhoenixRathaus.MemoryManager,
      # Telemetry
      PhoenixRathausWeb.Telemetry,
      # PubSub
      {Phoenix.PubSub, name: PhoenixRathaus.PubSub},
      # Endpoint
      PhoenixRathausWeb.Endpoint,
      # Task Scheduler
      PhoenixRathaus.Scheduler
    ]

    opts = [strategy: :one_for_one, name: PhoenixRathaus.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    PhoenixRathausWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end