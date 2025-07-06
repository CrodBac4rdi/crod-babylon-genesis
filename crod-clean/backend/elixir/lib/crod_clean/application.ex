defmodule CrodClean.Application do
  @moduledoc """
  CROD Clean Application - Pure AI/ML Focus ohne Blockchain
  """
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      CrodCleanWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: CrodClean.PubSub},
      # Start the Endpoint (http/https)
      CrodCleanWeb.Endpoint,
      # Start AI Services
      CrodClean.AIService,
      CrodClean.NeuralNetwork,
      CrodClean.PatternRecognition,
      # Start WebSocket handler
      CrodClean.WebSocketHandler
    ]

    opts = [strategy: :one_for_one, name: CrodClean.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    CrodCleanWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end