import Config

# For development, we disable any cache and enable
# debugging and code reloading.
config :crod_rathaus, CrodRathausWeb.Endpoint,
  # Binding to loopback ipv4 address prevents access from other machines.
  # Change to `ip: {0, 0, 0, 0}` to allow access from other machines.
  http: [ip: {0, 0, 0, 0}, port: 4000],
  check_origin: false,
  code_reloader: true,
  debug_errors: true,
  secret_key_base: "crod2025secretkeycrod2025secretkeycrod2025secretkeycrod2025secretkey",
  watchers: []

# Enable dev routes for dashboard and mailbox
config :crod_rathaus, dev_routes: true

# Set a higher stacktrace during development.
config :phoenix, :stacktrace_depth, 20

# Initialize plugs at runtime for faster development compilation
config :phoenix, :plug_init_mode, :runtime