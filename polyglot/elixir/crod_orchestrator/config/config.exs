import Config

config :crod_orchestrator,
  ecto_repos: [CROD.Repo]

# Configure your database
config :crod_orchestrator, CROD.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_orchestrator_#{config_env()}",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

# Configure Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{config_env()}.exs"