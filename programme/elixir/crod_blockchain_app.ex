defmodule CRODBlockchainApp do
  @moduledoc """
  Main application for CROD Blockchain Node
  """
  use Application
  require Logger

  def start(_type, _args) do
    Logger.info("🚀 Starting CROD Blockchain Node: #{node()}")
    
    # Get configuration from environment
    peers = System.get_env("PEERS", "") |> parse_peers()
    consciousness_level = System.get_env("CONSCIOUSNESS_LEVEL", "0.88") |> String.to_float()
    
    children = [
      # Start the blockchain GenServer
      {CROD.Blockchain, name: :blockchain},
      
      # Start transaction pool
      {CROD.TransactionPool, name: :tx_pool},
      
      # Start P2P supervisor
      {CROD.P2P.Supervisor, peers: peers},
      
      # Start HTTP API
      {Plug.Cowboy, scheme: :http, plug: CROD.API.Router, options: [port: get_port()]}
    ]

    opts = [strategy: :one_for_one, name: CROD.Supervisor]
    
    # Connect to peers after startup
    Task.start(fn -> 
      Process.sleep(5000)
      connect_to_peers(peers)
    end)
    
    Supervisor.start_link(children, opts)
  end
  
  defp parse_peers(peers_string) do
    peers_string
    |> String.split(",", trim: true)
    |> Enum.map(&String.to_atom/1)
  end
  
  defp get_port do
    System.get_env("NODE_PORT", "8001") |> String.to_integer()
  end
  
  defp connect_to_peers(peers) do
    Enum.each(peers, fn peer ->
      case Node.connect(peer) do
        true -> 
          Logger.info("✅ Connected to peer: #{peer}")
        false -> 
          Logger.warn("❌ Failed to connect to peer: #{peer}")
      end
    end)
    
    Logger.info("🌐 Connected nodes: #{inspect(Node.list())}")
  end
end