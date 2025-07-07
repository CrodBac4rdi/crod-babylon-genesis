defmodule Crod.Application do
  @moduledoc """
  The CROD application supervisor tree.
  Manages all polygon city districts and core services.
  """

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      CrodWeb.Telemetry,
      # Start the Ecto repository
      Crod.Repo,
      # Start the PubSub system
      {Phoenix.PubSub, name: Crod.PubSub},
      # Start Finch
      {Finch, name: Crod.Finch},
      # Start the Endpoint (http/https)
      CrodWeb.Endpoint,
      
      # CROD specific services
      # Start NATS client
      Crod.Services.NatsClient,
      # Start Event Store
      Crod.EventStore,
      # Start Polygon City supervisor
      Crod.PolygonCity.Supervisor,
      # Start CROD Parasite interpreter
      Crod.Parasite.Interpreter,
      # Start Neural Network manager
      Crod.Neural.Manager
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Crod.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    CrodWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end