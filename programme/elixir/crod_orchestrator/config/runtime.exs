import Config

# Runtime configuration for production deployments

if config_env() == :prod do
  database_url =
    System.get_env("DATABASE_URL") ||
      raise """
      environment variable DATABASE_URL is missing.
      For example: ecto://USER:PASS@HOST/DATABASE
      """

  config :crod_orchestrator, CROD.Repo,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10")

  # NATS Configuration
  nats_host = System.get_env("NATS_HOST") || "localhost"
  nats_port = String.to_integer(System.get_env("NATS_PORT") || "4222")

  config :gnat,
    connection_settings: [
      %{
        host: nats_host,
        port: nats_port
      }
    ]
end