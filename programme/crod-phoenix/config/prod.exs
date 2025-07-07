import Config

# For production, don't forget to configure the url host
# to something meaningful, Phoenix uses this information
# when generating URLs.
config :crod_phoenix, CrodWeb.Endpoint,
  url: [host: "crod.phoenix.local", port: 80],
  cache_static_manifest: "priv/static/cache_manifest.json",
  server: true

# Configure NATS for production
config :crod_phoenix, :nats,
  connection_name: "crod_phoenix_prod",
  host: System.get_env("NATS_HOST", "localhost"),
  port: String.to_integer(System.get_env("NATS_PORT", "4222"))

# Event Store configuration for production
config :crod_phoenix, event_stores: [Crod.EventStore]

config :crod_phoenix, Crod.EventStore,
  serializer: Commanded.Serialization.JsonSerializer,
  username: System.get_env("DATABASE_USERNAME"),
  password: System.get_env("DATABASE_PASSWORD"),
  database: System.get_env("DATABASE_NAME", "crod_phoenix_eventstore_prod"),
  hostname: System.get_env("DATABASE_HOST", "localhost"),
  pool_size: 15

# Do not print debug messages in production
config :logger, level: :info

# Runtime production configuration, including reading
# of environment variables, is done on config/runtime.exs.