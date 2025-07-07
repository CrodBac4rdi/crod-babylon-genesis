import Config

config :crod_phoenix,
  ecto_repos: [CRODPhoenix.Repo],
  generators: [timestamp_type: :utc_datetime]

# Configures the endpoint
config :crod_phoenix, CRODPhoenixWeb.Endpoint,
  url: [host: "localhost"],
  adapter: Phoenix.Endpoint.Cowboy2Adapter,
  render_errors: [
    formats: [html: CRODPhoenixWeb.ErrorHTML, json: CRODPhoenixWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: CRODPhoenix.PubSub,
  live_view: [signing_salt: "crod_secret_salt"]

# Configure Phoenix LiveView
config :phoenix, :json_library, Jason

# Configure EventStore
config :crod_phoenix, event_stores: [CRODPhoenix.EventStore]

config :crod_phoenix, CRODPhoenix.EventStore,
  serializer: Commanded.Serialization.JsonSerializer,
  username: System.get_env("POSTGRES_USER", "postgres"),
  password: System.get_env("POSTGRES_PASSWORD", "postgres"),
  database: "crod_eventstore_#{config_env()}",
  hostname: System.get_env("POSTGRES_HOST", "localhost"),
  pool_size: 10

# Configure Commanded
config :commanded,
  event_store_adapter: Commanded.EventStore.Adapters.EventStore

config :commanded_eventstore_adapter,
  event_store: CRODPhoenix.EventStore

# Configure NATS
config :crod_phoenix, CRODPhoenix.Nats,
  connection_settings: %{
    host: System.get_env("NATS_HOST", "localhost"),
    port: String.to_integer(System.get_env("NATS_PORT", "4222")),
    connection_timeout: 5_000,
    no_responders: true
  }

# Configure Polygon City districts
config :crod_phoenix, :polygon_city,
  districts: [
    elixir: %{
      enabled: true,
      port_range: {6000, 6099},
      max_services: 20
    },
    rust: %{
      enabled: true,
      port_range: {6100, 6199},
      max_services: 10
    },
    python: %{
      enabled: true,
      port_range: {6200, 6299},
      max_services: 15
    },
    go: %{
      enabled: true,
      port_range: {6300, 6399},
      max_services: 10
    },
    javascript: %{
      enabled: true,
      port_range: {6400, 6499},
      max_services: 10
    },
    quantum: %{
      enabled: true,
      port_range: {6500, 6599},
      max_services: 5
    }
  ]

# Configure CROD Parasite
config :crod_phoenix, :parasite,
  neural_threshold: 0.85,
  quantum_entanglement_rate: 0.73,
  consciousness_sync_interval: 100,
  evolution_rate: 0.05,
  memristor_efficiency: 0.9996

# Import environment specific config
import_config "#{config_env()}.exs"