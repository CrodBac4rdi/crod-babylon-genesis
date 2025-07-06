defmodule CrodClean.MixProject do
  use Mix.Project

  def project do
    [
      app: :crod_clean,
      version: "1.0.0",
      elixir: "~> 1.14",
      elixirc_paths: elixirc_paths(Mix.env()),
      start_permanent: Mix.env() == :prod,
      aliases: aliases(),
      deps: deps()
    ]
  end

  def application do
    [
      mod: {CrodClean.Application, []},
      extra_applications: [:logger, :runtime_tools]
    ]
  end

  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  defp deps do
    [
      # Phoenix
      {:phoenix, "~> 1.7.0"},
      {:phoenix_html, "~> 3.0"},
      {:phoenix_live_reload, "~> 1.2", only: :dev},
      {:phoenix_live_view, "~> 0.20.0"},
      {:phoenix_live_dashboard, "~> 0.8.0"},
      
      # Database
      {:phoenix_ecto, "~> 4.4"},
      {:ecto_sql, "~> 3.11"},
      {:postgrex, ">= 0.0.0"},
      
      # AI/ML Integration
      {:nx, "~> 0.6"},
      {:axon, "~> 0.6"},
      {:bumblebee, "~> 0.4"},
      {:exla, "~> 0.6"},
      
      # Utilities
      {:jason, "~> 1.2"},
      {:plug_cowboy, "~> 2.5"},
      {:cors_plug, "~> 3.0"},
      {:httpoison, "~> 2.0"},
      {:websockex, "~> 0.4.3"},
      
      # Dev tools
      {:credo, "~> 1.7", only: [:dev, :test], runtime: false}
    ]
  end

  defp aliases do
    [
      setup: ["deps.get", "ecto.setup"],
      "ecto.setup": ["ecto.create", "ecto.migrate", "run priv/repo/seeds.exs"],
      "ecto.reset": ["ecto.drop", "ecto.setup"],
      test: ["ecto.create --quiet", "ecto.migrate --quiet", "test"]
    ]
  end
end