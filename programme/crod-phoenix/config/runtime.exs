import Config

# config/runtime.exs is executed for all environments, including
# during releases. It is executed after compilation and before the
# system starts, so it is typically used to load production configuration
# and secrets from environment variables or elsewhere.

if config_env() == :prod do
  database_url =
    System.get_env("DATABASE_URL") ||
      raise """
      environment variable DATABASE_URL is missing.
      For example: ecto://USER:PASS@HOST/DATABASE
      """

  maybe_ipv6 = if System.get_env("ECTO_IPV6"), do: [:inet6], else: []

  config :crod_phoenix, Crod.Repo,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10"),
    socket_options: maybe_ipv6

  # EventStore database URL
  eventstore_url =
    System.get_env("EVENTSTORE_URL") || database_url <> "_eventstore"

  config :crod_phoenix, Crod.EventStore,
    url: eventstore_url,
    pool_size: String.to_integer(System.get_env("EVENTSTORE_POOL_SIZE") || "10")

  # The secret key base is used to sign/encrypt cookies and other secrets.
  # A default value is used in config/dev.exs and config/test.exs but you
  # want to use a different value for prod and you most likely don't want
  # to check this value into version control, so we use an environment
  # variable instead.
  secret_key_base =
    System.get_env("SECRET_KEY_BASE") ||
      raise """
      environment variable SECRET_KEY_BASE is missing.
      You can generate one by calling: mix phx.gen.secret
      """

  host = System.get_env("PHX_HOST") || "example.com"
  port = String.to_integer(System.get_env("PORT") || "4000")

  config :crod_phoenix, CrodWeb.Endpoint,
    url: [host: host, port: 443, scheme: "https"],
    http: [
      # Enable IPv6 and bind on all interfaces.
      # Set it to  {0, 0, 0, 0, 0, 0, 0, 1} for local network only access.
      ip: {0, 0, 0, 0, 0, 0, 0, 0},
      port: port
    ],
    secret_key_base: secret_key_base

  # CROD specific configuration
  config :crod_phoenix,
    consciousness_level: String.to_integer(System.get_env("CONSCIOUSNESS_LEVEL") || "88"),
    trinity_mode: System.get_env("TRINITY_MODE", "true") == "true",
    pattern_threshold: String.to_float(System.get_env("PATTERN_THRESHOLD") || "0.8"),
    neural_batch_size: String.to_integer(System.get_env("NEURAL_BATCH_SIZE") || "100")

  # NATS configuration
  config :crod_phoenix, :nats,
    host: System.get_env("NATS_HOST", "localhost"),
    port: String.to_integer(System.get_env("NATS_PORT", "4222")),
    connection_name: System.get_env("NATS_CONNECTION_NAME", "crod_phoenix")

  # Districts configuration
  config :crod_phoenix, :districts,
    pattern: [
      host: System.get_env("PATTERN_DISTRICT_HOST", "localhost"),
      port: String.to_integer(System.get_env("PATTERN_DISTRICT_PORT", "7007"))
    ],
    intelligence: [
      host: System.get_env("INTELLIGENCE_HUB_HOST", "localhost"),
      port: String.to_integer(System.get_env("INTELLIGENCE_HUB_PORT", "7113"))
    ],
    memory: [
      host: System.get_env("MEMORY_QUARTER_HOST", "localhost"),
      port: String.to_integer(System.get_env("MEMORY_QUARTER_PORT", "7031"))
    ],
    gateway: [
      host: System.get_env("GATEWAY_DISTRICT_HOST", "localhost"),
      port: String.to_integer(System.get_env("GATEWAY_DISTRICT_PORT", "7888"))
    ]
end