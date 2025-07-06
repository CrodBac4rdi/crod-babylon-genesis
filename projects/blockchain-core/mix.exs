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
      mod: {CRODBlockchainApp, []}
    ]
  end

  defp deps do
    [
      {:jason, "~> 1.4"},
      {:plug_cowboy, "~> 2.6"},
      {:uuid, "~> 1.1"}
    ]
  end
end