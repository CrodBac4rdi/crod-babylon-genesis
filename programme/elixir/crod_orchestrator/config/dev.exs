import Config

# Configure your database
config :crod_orchestrator, CROD.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_orchestrator_dev",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

# Enable debug logging
config :logger, :console,
  format: "[$level] $message\n",
  level: :debug

# NATS Configuration for development
config :gnat,
  connection_settings: [
    %{
      host: "localhost",
      port: 4222
    }
  ]