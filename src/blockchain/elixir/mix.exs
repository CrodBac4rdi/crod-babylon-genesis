defmodule CROD.MixProject do
  use Mix.Project

  def project do
    [
      app: :crod_blockchain,
      version: "0.4.0",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger, :crypto],
      mod: {CROD.Application, []}
    ]
  end

  defp deps do
    [
      {:jason, "~> 1.4"},
      {:plug_cowboy, "~> 2.6"},
      {:gnat, "~> 1.7"},
      {:uuid, "~> 1.1"},
      {:quantum, "~> 3.5"},
      {:httpoison, "~> 2.1"}
    ]
  end
end