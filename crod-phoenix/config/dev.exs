import Config

# Configure your database
config :crod_phoenix, CRODPhoenix.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_phoenix_dev",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

# For development, we disable any cache and enable debugging
config :crod_phoenix, CRODPhoenixWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4000],
  check_origin: false,
  code_reloader: true,
  debug_errors: true,
  secret_key_base: "crod_dev_secret_key_base_at_least_64_chars_long_for_security_123456789",
  watchers: []

# Enable dev routes for dashboard and mailbox
config :crod_phoenix, dev_routes: true

# Do not include metadata nor timestamps in development logs
config :logger, :console, format: "[$level] $message\n"

# Set a higher stacktrace during development
config :phoenix, :stacktrace_depth, 20

# Initialize plugs at runtime for faster development compilation
config :phoenix, :plug_init_mode, :runtime