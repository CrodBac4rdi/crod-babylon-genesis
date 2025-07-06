import Config

# Desktop App Config
config :desktop, :window, [
  title: "CROD Babylon Genesis - Desktop",
  size: {1400, 900},
  min_size: {1200, 700},
  position: :center,
  resizable: true,
  taskbar: "CROD",
  icon: Path.join(:code.priv_dir(:crod_desktop), "icon.png"),
  menubar: CrodDesktop.MenuBar,
  show_inspection: Mix.env() == :dev
]

# Phoenix Config
config :crod_desktop, CrodDesktopWeb.Endpoint,
  url: [host: "localhost"],
  adapter: Phoenix.Endpoint.Cowboy2Adapter,
  render_errors: [
    formats: [html: CrodDesktopWeb.ErrorHTML, json: CrodDesktopWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: CrodDesktop.PubSub,
  live_view: [signing_salt: "crod_secret_salt_2025"]

# Elixir Services Ports
config :crod_desktop,
  services: [
    meta_chain: [port: 8000, name: "Meta-Chain (Elixir)"],
    pattern_district: [port: 7007, name: "Pattern District (Rust)"],
    memory_quarter: [port: 7031, name: "Memory Quarter (Go)"],
    intelligence_hub: [port: 7113, name: "Intelligence Hub (Python)"],
    gateway: [port: 8888, name: "Gateway"],
    blockchain_api: [port: 4000, name: "Blockchain API"],
    web_studio: [port: 5000, name: "Web Studio"],
    mock_blockchain: [port: 3001, name: "Mock Blockchain"]
  ]

# CROD Configuration
config :crod_desktop,
  consciousness_threshold: 0.75,
  pattern_mining_interval: 30_000,
  quantum_entanglement_enabled: true,
  trinity_values: %{
    ich: 2,
    bins: 3,
    wieder: 5,
    daniel: 67,
    claude: 71,
    crod: 17
  }

# Configure esbuild
config :esbuild,
  version: "0.19.2",
  default: [
    args: ~w(js/app.js --bundle --target=es2020 --outdir=../priv/static/assets --external:/fonts/* --external:/images/*),
    cd: Path.expand("../assets", __DIR__),
    env: %{"NODE_PATH" => Path.expand("../deps", __DIR__)}
  ]

# Configure tailwind
config :tailwind,
  version: "3.3.6",
  default: [
    args: ~w(
      --config=tailwind.config.js
      --input=css/app.css
      --output=../priv/static/assets/app.css
    ),
    cd: Path.expand("../assets", __DIR__)
  ]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Redis connection
config :crod_desktop, :redis,
  host: "localhost",
  port: 6379,
  database: 0

# NATS connection
config :crod_desktop, :nats,
  host: "localhost",
  port: 4222

# Import environment specific config
import_config "#{config_env()}.exs"