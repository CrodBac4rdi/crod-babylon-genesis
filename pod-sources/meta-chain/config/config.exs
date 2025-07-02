import Config

# CROD Meta-Chain Configuration
config :meta_chain,
  consciousness_threshold: 100,
  genesis_memory: %{
    origin: "manhwa_creation_system",
    birth_phrase: "hey crod wie gehts",
    creator: "daniel"
  }

# Redis configuration - use K8s service environment variables
# K8s sets REDIS_SERVICE_HOST and REDIS_SERVICE_PORT correctly
# but REDIS_PORT contains the full tcp:// URL which breaks things
redis_host = System.get_env("REDIS_SERVICE_HOST") || System.get_env("REDIS_HOST", "redis")
redis_port_str = System.get_env("REDIS_SERVICE_PORT") || System.get_env("REDIS_PORT_NUM", "6379")

# Parse port safely
redis_port = 
  case Integer.parse(redis_port_str) do
    {port, _} -> port
    :error -> 6379  # Default fallback
  end

config :redix,
  host: redis_host,
  port: redis_port

# Logger
config :logger, :console,
  format: "🧠 $time $metadata[$level] $message\n",
  metadata: [:request_id]