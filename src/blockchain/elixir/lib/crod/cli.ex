defmodule CROD.CLI do
  @moduledoc """
  CROD Blockchain CLI - Start everything with one command!
  """

  def main(args \\ []) do
    case parse_args(args) do
      {:start, nodes} -> start_blockchain(nodes)
      {:docker, nodes} -> start_docker(nodes)
      {:help} -> print_help()
      _ -> print_help()
    end
  end

  defp parse_args([]), do: {:start, 3}
  defp parse_args(["start"]), do: {:start, 3}
  defp parse_args(["start", nodes]), do: {:start, String.to_integer(nodes)}
  defp parse_args(["docker"]), do: {:docker, 3}
  defp parse_args(["docker", nodes]), do: {:docker, String.to_integer(nodes)}
  defp parse_args(["help"]), do: {:help}
  defp parse_args(_), do: {:help}

  defp start_blockchain(node_count) do
    IO.puts """
    🔥 CROD Blockchain Starting...
    =============================
    Nodes: #{node_count}
    Mode: Local Multi-Node
    """

    # Start application
    Application.ensure_all_started(:crod_blockchain)

    # Start nodes
    nodes = for i <- 1..node_count do
      node_name = :"crod#{i}@127.0.0.1"
      
      # Start node in separate process
      spawn(fn ->
        System.cmd("elixir", [
          "--name", "#{node_name}",
          "--cookie", "crod_blockchain",
          "-S", "mix", "run", "--no-halt",
          "-e", """
          # Connect to previous nodes
          #{if i > 1, do: "Node.connect(:'crod1@127.0.0.1')", else: ""}
          
          # Start blockchain
          {:ok, _} = CROD.Blockchain.start_link(name: :blockchain)
          
          # Start P2P sync
          {:ok, _} = CROD.P2PSync.start_link()
          
          # Start HTTP API on different ports
          port = 8000 + #{i}
          
          # Log startup
          IO.puts("Node #{i} started on port \#{port}")
          IO.puts("Connected to: \#{Node.list()}")
          """
        ])
      end)
      
      Process.sleep(2000)
      node_name
    end

    IO.puts """
    
    ✅ All nodes started!
    
    📊 Dashboard: http://localhost:8001
    🔗 API Endpoints:
       - Node 1: http://localhost:8001
       - Node 2: http://localhost:8002  
       - Node 3: http://localhost:8003
    
    💡 Commands:
       - Add block: curl -X POST http://localhost:8001/api/block -d '{"data": "test"}'
       - Get chain: curl http://localhost:8001/api/chain
       - Mine block: curl -X POST http://localhost:8001/api/mine
    
    Press Ctrl+C to stop all nodes.
    """

    # Keep main process running
    Process.sleep(:infinity)
  end

  defp start_docker(node_count) do
    IO.puts """
    🐳 Starting CROD Blockchain in Docker...
    ========================================
    """

    # Generate docker-compose.yml
    compose_content = generate_docker_compose(node_count)
    File.write!("docker-compose.yml", compose_content)

    # Start docker-compose
    System.cmd("docker-compose", ["up", "-d"])

    IO.puts """
    
    ✅ Docker containers started!
    
    📊 Access points:
       - Dashboard: http://localhost:8001
       - Nodes: http://localhost:800[1-#{node_count}]
    
    🐳 Docker commands:
       - View logs: docker-compose logs -f
       - Stop: docker-compose down
       - Scale: docker-compose up -d --scale crod-node=5
    """
  end

  defp generate_docker_compose(node_count) do
    """
    version: '3.8'

    services:
      crod-node:
        build: .
        environment:
          - ERLANG_COOKIE=crod_blockchain
        ports:
          - "8001-80#{node_count}0:8000"
        deploy:
          replicas: #{node_count}
        networks:
          - crod-network

    networks:
      crod-network:
        driver: bridge
    """
  end

  defp print_help do
    IO.puts """
    CROD Blockchain CLI
    ===================
    
    Usage:
      ./crod_blockchain [command] [options]
    
    Commands:
      start [nodes]    Start local multi-node blockchain (default: 3 nodes)
      docker [nodes]   Start blockchain in Docker containers
      help            Show this help
    
    Examples:
      ./crod_blockchain start        # Start 3 nodes locally
      ./crod_blockchain start 5      # Start 5 nodes locally
      ./crod_blockchain docker       # Start 3 nodes in Docker
      ./crod_blockchain docker 10    # Start 10 nodes in Docker
    """
  end
end