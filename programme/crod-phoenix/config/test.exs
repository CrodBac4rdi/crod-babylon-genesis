import Config

# Configure your database
config :crod_phoenix, Crod.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_phoenix_test#{System.get_env("MIX_TEST_PARTITION")}",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 10

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :crod_phoenix, CrodWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "test_secret_key_base_at_least_64_characters_long_for_testing_purposes_only",
  server: false

# Event Store test configuration
config :crod_phoenix, event_stores: [Crod.EventStore]

config :crod_phoenix, Crod.EventStore,
  serializer: Commanded.Serialization.JsonSerializer,
  username: "postgres",
  password: "postgres",
  database: "crod_phoenix_eventstore_test#{System.get_env("MIX_TEST_PARTITION")}",
  hostname: "localhost",
  pool_size: 10

# NATS test configuration
config :crod_phoenix, :nats,
  connection_name: "crod_phoenix_test",
  host: "localhost",
  port: 4222

# Print only warnings and errors during test
config :logger, level: :warning

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime