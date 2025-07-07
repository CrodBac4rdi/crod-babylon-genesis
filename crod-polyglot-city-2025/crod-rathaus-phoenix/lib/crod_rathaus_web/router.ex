defmodule CrodRathausWeb.Router do
  use CrodRathausWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, {CrodRathausWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CrodRathausWeb do
    pipe_through :browser

    live "/", DashboardLive, :index
    live "/districts", DistrictsLive, :index
  end

  if Mix.env() in [:dev, :test] do
    import Phoenix.LiveDashboard.Router

    scope "/" do
      pipe_through :browser
      live_dashboard "/dashboard", metrics: CrodRathausWeb.Telemetry
    end
  end
end
