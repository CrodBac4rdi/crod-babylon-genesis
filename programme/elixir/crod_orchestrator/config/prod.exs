import Config

# For production, don't check sensitive configuration at compile time
config :crod_orchestrator, CROD.Repo,
  pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10")

config :logger, level: :info