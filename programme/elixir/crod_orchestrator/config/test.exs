import Config

# Configure your database
config :crod_orchestrator, CROD.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_orchestrator_test#{System.get_env("MIX_TEST_PARTITION")}",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 10

# Print only warnings and errors during test
config :logger, level: :warn

# NATS Configuration for test
config :gnat,
  connection_settings: [
    %{
      host: "localhost",
      port: 4222
    }
  ]