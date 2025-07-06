defmodule CrodDesktopWeb.Router do
  use CrodDesktopWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {CrodDesktopWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CrodDesktopWeb do
    pipe_through :browser

    live "/", DashboardLive, :index
    live "/blockchain", BlockchainLive, :index
    live "/simple-blockchain", SimpleBlockchainLive, :index
    live "/patterns", PatternsLive, :index
    live "/consciousness", ConsciousnessLive, :index
    live "/quantum", QuantumLive, :index
    live "/services", ServicesLive, :index
    live "/parasite", ParasiteLive, :index
    live "/settings", SettingsLive, :index
  end

  # Other scopes may use custom stacks.
  scope "/api", CrodDesktopWeb do
    pipe_through :api
    
    get "/status", ApiController, :status
    get "/consciousness", ApiController, :consciousness
    post "/mine", ApiController, :mine
    get "/blocks", ApiController, :blocks
    post "/evolve", ApiController, :evolve
  end

  # Enable LiveDashboard in development
  if Application.compile_env(:crod_desktop, :dev_routes) do
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through :browser

      live_dashboard "/dashboard", metrics: CrodDesktopWeb.Telemetry
    end
  end
end