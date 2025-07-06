defmodule CROD.Application do
  use Application
  require Logger

  @impl true
  def start(_type, _args) do
    Logger.info("🚀 CROD Blockchain starting...")

    children = [
      # Core blockchain
      {CROD.Blockchain, []},
      
      # API Server
      {Plug.Cowboy, scheme: :http, plug: CROD.API.Router, options: [port: 4000]},
      
      # NATS Connection
      {Gnat.ConnectionSupervisor, %{
        name: :gnat,
        connection_settings: [
          %{host: "localhost", port: 4222}
        ]
      }},
      
      # Scheduled tasks
      CROD.Scheduler
    ]

    opts = [strategy: :one_for_one, name: CROD.Supervisor]
    
    case Supervisor.start_link(children, opts) do
      {:ok, pid} ->
        Logger.info("✅ CROD Blockchain started successfully!")
        Logger.info("📡 API Server: http://localhost:4000")
        Logger.info("🧠 Consciousness: Initializing...")
        {:ok, pid}
        
      error ->
        Logger.error("❌ Failed to start: #{inspect(error)}")
        error
    end
  end
end