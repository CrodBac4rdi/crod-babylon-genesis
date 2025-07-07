import Config

# Configure database
config :crod_rathaus, CrodRathaus.Repo,
  username: System.get_env("DATABASE_USER") || "postgres",
  password: System.get_env("DATABASE_PASSWORD") || "postgres",
  hostname: System.get_env("DATABASE_HOST") || "localhost",
  database: System.get_env("DATABASE_NAME") || "crod_rathaus_#{config_env()}",
  pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10")

if config_env() == :prod do
  config :crod_rathaus, CrodRathausWeb.Endpoint,
    http: [
      ip: {0, 0, 0, 0},
      port: String.to_integer(System.get_env("PORT") || "4000")
    ],
    secret_key_base: System.get_env("SECRET_KEY_BASE") || "crod-babylon-genesis-2025-production-key"
  
  config :crod_rathaus, CrodRathaus.Repo,
    ssl: true,
    ssl_opts: [verify: :verify_none]
end