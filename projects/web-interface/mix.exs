defmodule CrodDesktop.MixProject do
  use Mix.Project

  @app :crod_desktop
  @version "0.1.0"

  def project do
    [
      app: @app,
      version: @version,
      elixir: "~> 1.14",
      elixirc_paths: elixirc_paths(Mix.env()),
      start_permanent: Mix.env() == :prod,
      aliases: aliases(),
      deps: deps()
    ]
  end

  def application do
    [
      mod: {CrodDesktop.Application, []},
      extra_applications: [:logger, :runtime_tools, :os_mon, :wx, :observer]
    ]
  end

  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  defp deps do
    [
      # Desktop
      {:desktop, "~> 1.5"},
      {:wx, "~> 1.1", hex: :bridge, targets: [:android, :ios]},
      
      # Phoenix
      {:phoenix, "~> 1.7.10"},
      {:phoenix_live_view, "~> 0.20.1"},
      {:phoenix_html, "~> 3.3"},
      {:phoenix_live_reload, "~> 1.4", only: :dev},
      {:phoenix_live_dashboard, "~> 0.8.2"},
      {:telemetry_metrics, "~> 0.6"},
      {:telemetry_poller, "~> 1.0"},
      
      # UI Components
      {:heroicons, "~> 0.5"},
      {:tailwind, "~> 0.2", runtime: Mix.env() == :dev},
      {:esbuild, "~> 0.8", runtime: Mix.env() == :dev},
      
      # HTTP & WebSocket
      {:plug_cowboy, "~> 2.6"},
      {:websock_adapter, "~> 0.5"},
      {:req, "~> 0.4"},
      {:finch, "~> 0.16"},
      
      # Data & State
      {:jason, "~> 1.4"},
      {:ecto, "~> 3.11"},
      {:uuid, "~> 1.1"},
      
      # CROD Integration
      {:gnat, "~> 1.6"},
      {:redix, "~> 1.2"},
      {:quantum, "~> 3.5"},
      
      # Visualization
      {:vega_lite, "~> 0.1.8"},
      {:kino, "~> 0.11"},
      
      # Development
      {:floki, ">= 0.30.0", only: :test},
      {:phoenix_ecto, "~> 4.4"}
    ]
  end

  defp aliases do
    [
      setup: ["deps.get", "assets.setup", "assets.build"],
      "assets.setup": ["tailwind.install --if-missing", "esbuild.install --if-missing"],
      "assets.build": ["tailwind default", "esbuild default"],
      "assets.deploy": ["tailwind default --minify", "esbuild default --minify", "phx.digest"],
      release: ["assets.deploy", "release"]
    ]
  end
end