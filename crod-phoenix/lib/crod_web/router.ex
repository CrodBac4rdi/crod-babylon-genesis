defmodule CrodWeb.Router do
  use CrodWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {CrodWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CrodWeb do
    pipe_through :browser

    get "/", PageController, :index
    live "/dashboard", DashboardLive.Index, :index
    live "/parasite", ParasiteLive.Index, :index
  end

  # API routes
  scope "/api", CrodWeb do
    pipe_through :api

    # CROD Parasite endpoints
    post "/parasite/interpret", ParasiteController, :interpret
    post "/parasite/humanize", ParasiteController, :humanize
    get "/parasite/context/:session_id", ParasiteController, :get_context

    # Neural network endpoints
    post "/neural/process", NeuralController, :process
    post "/neural/train", NeuralController, :train
    get "/neural/status/:network_id", NeuralController, :status

    # Orchestration endpoints
    post "/orchestrate", OrchestratorController, :orchestrate
    get "/orchestrate/status", OrchestratorController, :status

    # Health check
    get "/health", HealthController, :check
  end

  # Enable LiveDashboard and Swoosh mailbox preview in development
  if Application.compile_env(:crod, :dev_routes) do
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through :browser

      live_dashboard "/dashboard", metrics: CrodWeb.Telemetry
    end
  end
end