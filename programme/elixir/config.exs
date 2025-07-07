# This file is responsible for configuring your application
import Config

config :crod,
  ecto_repos: [Crod.Repo],
  generators: [binary_id: true]

# Configures the endpoint
config :crod, CrodWeb.Endpoint,
  url: [host: "localhost"],
  render_errors: [
    formats: [html: CrodWeb.ErrorHTML, json: CrodWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: Crod.PubSub,
  live_view: [signing_salt: "polygon_city_secret"]

# Configure NATS
config :crod, Crod.Services.NatsClient,
  connection_settings: %{
    host: "localhost",
    port: 4222,
    tls: false
  }

# Configure Event Store
config :crod, Crod.EventStore,
  serializer: Commanded.Serialization.JsonSerializer,
  username: "postgres",
  password: "postgres",
  database: "crod_eventstore",
  hostname: "localhost",
  pool_size: 10

# Configure commanded
config :commanded,
  event_store_adapter: Commanded.EventStore.Adapters.EventStore

config :commanded_eventstore_adapter,
  event_store: Crod.EventStore

# Neural network paths
config :crod, :neural,
  master_config: "priv/neural/crod-master.json",
  neural_network: "priv/neural/crod-neural-network.js"

# Polygon City districts
config :crod, :polygon_city,
  districts: [
    :parasite,
    :neural,
    :memory,
    :orchestrator,
    :interface
  ]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config
import_config "#{config_env()}.exs"