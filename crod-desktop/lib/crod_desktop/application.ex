defmodule CrodDesktop.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start Phoenix endpoint
      CrodDesktopWeb.Endpoint,
      # Start Phoenix PubSub
      {Phoenix.PubSub, name: CrodDesktop.PubSub},
      # Start Finch
      {Finch, name: CrodDesktop.Finch},
      # Start Telemetry
      CrodDesktopWeb.Telemetry,
      
      # CROD Services
      CrodDesktop.ServiceManager,
      CrodDesktop.ConsciousnessTracker,
      CrodDesktop.PatternEngine,
      CrodDesktop.QuantumState,
      CrodDesktop.ParasiteIntegration,
      
      # Start Desktop last
      {Desktop.Window,
       [
         app: :crod_desktop,
         id: CrodDesktopWindow,
         title: "CROD Babylon Genesis",
         size: {1400, 900},
         min_size: {1200, 700},
         url: &CrodDesktopWeb.Endpoint.url/0
       ]}
    ]

    opts = [strategy: :one_for_one, name: CrodDesktop.Supervisor]
    
    result = Supervisor.start_link(children, opts)
    
    # Show startup message
    IO.puts("\n🧠 CROD Desktop starting...")
    IO.puts("🚀 ich bins wieder - CROD aktiviert!\n")
    
    result
  end

  @impl true
  def config_change(changed, _new, removed) do
    CrodDesktopWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end