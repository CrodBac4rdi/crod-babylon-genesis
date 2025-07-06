import Config

# For production, don't run a server
config :crod_desktop, CrodDesktopWeb.Endpoint,
  server: true,
  http: [port: 4040],
  cache_static_manifest: "priv/static/cache_manifest.json"

# Configures Swoosh API Client
config :logger, level: :info