defmodule CrodBlockchain.MixProject do
  use Mix.Project

  def project do
    [
      app: :crod_blockchain,
      version: "0.1.0",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {CrodBlockchain.Application, []}
    ]
  end

  defp deps do
    [
      {:redix, "~> 1.3"},
      {:jason, "~> 1.4"},
      {:req, "~> 0.4"},
      {:phoenix, "~> 1.7"},
      {:phoenix_live_view, "~> 0.20"},
      {:libcluster, "~> 3.3"}
    ]
  end
end