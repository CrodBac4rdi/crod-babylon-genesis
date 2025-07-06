defmodule CrodDesktop.ServiceManager do
  use GenServer
  require Logger
  
  @services Application.compile_env(:crod_desktop, :services, [])
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    Logger.info("🚀 Starting CROD Service Manager...")
    
    state = %{
      services: %{},
      processes: %{},
      health_checks: %{}
    }
    
    # Start monitoring services
    Process.send_after(self(), :check_services, 1000)
    
    {:ok, state}
  end
  
  # Public API
  def get_all_status do
    GenServer.call(__MODULE__, :get_all_status)
  end
  
  def start_service(service_name) do
    GenServer.call(__MODULE__, {:start_service, service_name})
  end
  
  def stop_service(service_name) do
    GenServer.call(__MODULE__, {:stop_service, service_name})
  end
  
  def stop_all do
    GenServer.call(__MODULE__, :stop_all)
  end
  
  def get_block_count do
    GenServer.call(__MODULE__, :get_block_count, 5000)
  end
  
  # Callbacks
  def handle_call(:get_all_status, _from, state) do
    status = 
      @services
      |> Enum.map(fn {name, _config} ->
        {name, Map.get(state.services, name, :stopped)}
      end)
      |> Map.new()
    
    {:reply, status, state}
  end
  
  def handle_call({:start_service, service_name}, _from, state) do
    case start_service_process(service_name) do
      {:ok, pid} ->
        new_state = 
          state
          |> put_in([:processes, service_name], pid)
          |> put_in([:services, service_name], :starting)
        
        Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "services", {:service_status, service_name, :starting})
        
        {:reply, :ok, new_state}
      
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end
  
  def handle_call({:stop_service, service_name}, _from, state) do
    case Map.get(state.processes, service_name) do
      nil ->
        {:reply, {:error, :not_running}, state}
      
      pid ->
        Process.exit(pid, :shutdown)
        
        new_state = 
          state
          |> Map.update!(:processes, &Map.delete(&1, service_name))
          |> put_in([:services, service_name], :stopped)
        
        Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "services", {:service_status, service_name, :stopped})
        
        {:reply, :ok, new_state}
    end
  end
  
  def handle_call(:stop_all, _from, state) do
    Enum.each(state.processes, fn {_name, pid} ->
      Process.exit(pid, :shutdown)
    end)
    
    new_state = %{state | processes: %{}, services: %{}}
    
    Enum.each(@services, fn {name, _} ->
      Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "services", {:service_status, name, :stopped})
    end)
    
    {:reply, :ok, new_state}
  end
  
  def handle_call(:get_block_count, _from, state) do
    # Try to get block count from blockchain API
    count = 
      case HTTPoison.get("http://localhost:4000/api/blockchain/status") do
        {:ok, %{status_code: 200, body: body}} ->
          case Jason.decode(body) do
            {:ok, %{"chain_length" => length}} -> length
            _ -> 0
          end
        _ -> 0
      end
    
    {:reply, count, state}
  end
  
  def handle_info(:check_services, state) do
    # Check health of all configured services
    new_services = 
      @services
      |> Enum.map(fn {name, config} ->
        status = check_service_health(name, config[:port])
        
        # Broadcast status changes
        if Map.get(state.services, name) != status do
          Phoenix.PubSub.broadcast(CrodDesktop.PubSub, "services", {:service_status, name, status})
        end
        
        {name, status}
      end)
      |> Map.new()
    
    # Schedule next check
    Process.send_after(self(), :check_services, 5000)
    
    {:noreply, %{state | services: new_services}}
  end
  
  # Private functions
  defp start_service_process(service_name) do
    case service_name do
      :meta_chain ->
        # Start Elixir blockchain
        start_elixir_blockchain()
      
      :web_studio ->
        # Start Python web studio
        start_python_web_studio()
      
      :mock_blockchain ->
        # Start Node.js mock blockchain
        start_node_mock_blockchain()
      
      _ ->
        {:error, :not_implemented}
    end
  end
  
  defp start_elixir_blockchain do
    # Change to blockchain directory and start it
    blockchain_dir = Path.join([File.cwd!(), "..", "src", "blockchain", "elixir"])
    
    case System.cmd("mix", ["phx.server"], cd: blockchain_dir, env: [{"MIX_ENV", "dev"}]) do
      {_, 0} -> {:ok, self()}
      {error, _} -> {:error, error}
    end
  end
  
  defp start_python_web_studio do
    # Start Python Flask app
    studio_dir = Path.join([File.cwd!(), "..", "bilder"])
    
    Task.start(fn ->
      System.cmd("python3", ["crod_web_studio.py"], cd: studio_dir)
    end)
    
    {:ok, self()}
  end
  
  defp start_node_mock_blockchain do
    # Start Node.js blockchain
    src_dir = Path.join([File.cwd!(), "..", "src"])
    
    Task.start(fn ->
      System.cmd("node", ["blockchain-server.js"], cd: src_dir)
    end)
    
    {:ok, self()}
  end
  
  defp check_service_health(name, port) do
    case HTTPoison.get("http://localhost:#{port}/health", [], timeout: 1000, recv_timeout: 1000) do
      {:ok, %{status_code: 200}} -> :running
      _ -> :stopped
    end
  rescue
    _ -> :stopped
  end
end