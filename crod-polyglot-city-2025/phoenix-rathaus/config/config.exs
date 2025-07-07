import Config

config :crod_rathaus, CrodRathausWeb.Endpoint,
  url: [host: "localhost"],
  render_errors: [
    formats: [json: CrodRathausWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: CrodRathaus.PubSub,
  live_view: [signing_salt: "aaaaaaaa"]

config :crod_rathaus,
  nats_url: System.get_env("NATS_URL") || "nats://localhost:4222",
  port: String.to_integer(System.get_env("PORT") || "4000")

config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

config :phoenix, :json_library, Jason

import_config "#{config_env()}.exs"