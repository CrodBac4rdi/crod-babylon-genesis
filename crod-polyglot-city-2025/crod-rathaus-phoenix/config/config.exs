import Config

config :crod_rathaus, CrodRathausWeb.Endpoint,
  url: [host: "localhost"],
  render_errors: [view: CrodRathausWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: CrodRathaus.PubSub,
  live_view: [signing_salt: "crod2025"]

config :phoenix, :json_library, Jason

# Configure your database
config :crod_rathaus, CrodRathaus.Repo,
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  database: "crod_rathaus_dev",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

config :crod_rathaus, ecto_repos: [CrodRathaus.Repo]

# Quantum Scheduler configuration
config :crod_rathaus, CrodRathaus.Scheduler,
  jobs: [
    # Every 30 seconds: Check district health
    {"*/30 * * * * *", {CrodRathaus.DistrictMonitor, :check_health, []}},
    # Every minute: Create event snapshots
    {"* * * * *", {CrodRathaus.EventStore, :create_snapshots, []}},
    # Every 5 minutes: Clean old events
    {"*/5 * * * *", {CrodRathaus.EventStore, :cleanup_old_events, []}}
  ]

if config_env() == :dev do
  config :crod_rathaus, CrodRathausWeb.Endpoint,
    http: [ip: {0, 0, 0, 0}, port: 4000],
    check_origin: false,
    code_reloader: true,
    debug_errors: true,
    secret_key_base: "crod2025secretkeycrod2025secretkeycrod2025secretkeycrod2025secretkey",
    watchers: []
end
