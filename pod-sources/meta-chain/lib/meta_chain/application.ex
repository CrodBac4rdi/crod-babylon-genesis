defmodule MetaChain.Application do
  use Application
  require Logger

  @impl true
  def start(_type, _args) do
    port = String.to_integer(System.get_env("HTTP_PORT") || "8000")
    
    children = [
      MetaChain,
      {Plug.Cowboy, scheme: :http, plug: MetaChain.Router, options: [port: port]}
    ]

    opts = [strategy: :one_for_one, name: MetaChain.Supervisor]
    
    Logger.info("🏙️ CROD Meta-Chain starting on port #{port}...")
    Supervisor.start_link(children, opts)
  end
end