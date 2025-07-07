defmodule CrodRathaus.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      CrodRathausWeb.Telemetry,
      # Start the Ecto repository
      CrodRathaus.Repo,
      # Start the PubSub system
      {Phoenix.PubSub, name: CrodRathaus.PubSub},
      # Start NATS connection
      CrodRathaus.NATS,
      # Start Event Store
      CrodRathaus.EventStore,
      # Start the Endpoint (http/https) - must be last
      CrodRathausWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: CrodRathaus.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    CrodRathausWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
