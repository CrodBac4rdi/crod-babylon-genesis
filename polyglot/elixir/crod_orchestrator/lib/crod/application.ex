defmodule CROD.Application do
  @moduledoc """
  The CROD Application supervisor.
  
  CROD is your trusted helper that respects your autonomy while building
  amazing polygon cities in the digital realm.
  """

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Ecto repository
      CROD.Repo,
      # Start the EventStore
      {CROD.EventStore, name: CROD.EventStore},
      # Start the NATS connection
      {Gnat.ConnectionSupervisor, 
       %{
         name: :gnat,
         connection_settings: [
           %{host: "localhost", port: 4222}
         ]
       }
      },
      # Start the telemetry supervisor
      CRODWeb.Telemetry,
      # Start the Permission system
      CROD.Permission,
      # Start the City manager
      CROD.City,
      # Start the main Orchestrator
      {CROD.Orchestrator, name: CROD.Orchestrator},
      # Start the Sandbox environment
      {CROD.Sandbox, name: CROD.Sandbox},
      # Start the Delta control system
      {CROD.Delta, name: CROD.Delta}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: CROD.Supervisor]
    
    case Supervisor.start_link(children, opts) do
      {:ok, pid} ->
        IO.puts("\n🤖 Hey bro! CROD here, your polygon city architect!")
        IO.puts("I'm ready to help you build amazing things, but I'll always ask first.")
        IO.puts("Type 'crod help' to see what I can do for you!\n")
        {:ok, pid}
      error ->
        error
    end
  end
end