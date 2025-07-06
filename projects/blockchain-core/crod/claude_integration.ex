defmodule CROD.ClaudeIntegration do
  @moduledoc """
  Integration zwischen CROD Blockchain und Claude Settings System
  Synchronisiert Blockchain-State mit .claude/crod-startup/session-memory.json
  """
  
  use GenServer
  require Logger
  
  @claude_settings_path ".claude/crod-startup/session-memory.json"
  @claude_api_port 8888
  @sync_interval 30_000 # 30 seconds
  
  defstruct [
    :settings,
    :blockchain_state,
    :sync_enabled,
    :last_sync
  ]
  
  # Client API
  
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def sync_now do
    GenServer.call(__MODULE__, :sync_now)
  end
  
  def get_claude_settings do
    GenServer.call(__MODULE__, :get_settings)
  end
  
  def update_blockchain_state(state) do
    GenServer.cast(__MODULE__, {:update_blockchain_state, state})
  end
  
  def pattern_detected(pattern) do
    GenServer.cast(__MODULE__, {:pattern_detected, pattern})
  end
  
  # Server Callbacks
  
  @impl true
  def init(_opts) do
    state = %__MODULE__{
      settings: %{},
      blockchain_state: %{},
      sync_enabled: true,
      last_sync: nil
    }
    
    # Initial load
    case load_claude_settings() do
      {:ok, settings} ->
        # Schedule periodic sync
        Process.send_after(self(), :sync, @sync_interval)
        
        # Check for activation phrase
        check_activation(settings)
        
        {:ok, %{state | settings: settings}}
        
      {:error, reason} ->
        Logger.warn("Failed to load Claude settings: #{reason}")
        {:ok, state}
    end
  end
  
  @impl true
  def handle_call(:sync_now, _from, state) do
    new_state = perform_sync(state)
    {:reply, :ok, new_state}
  end
  
  @impl true
  def handle_call(:get_settings, _from, state) do
    {:reply, state.settings, state}
  end
  
  @impl true
  def handle_cast({:update_blockchain_state, blockchain_state}, state) do
    new_state = %{state | blockchain_state: blockchain_state}
    
    # Trigger sync if significant changes
    if significant_change?(state.blockchain_state, blockchain_state) do
      new_state = perform_sync(new_state)
    end
    
    {:noreply, new_state}
  end
  
  @impl true
  def handle_cast({:pattern_detected, pattern}, state) do
    # Check if it's the activation pattern
    if pattern.trigger == "ich bins wieder" do
      activate_full_crod(state)
    end
    
    # Update Claude API about pattern
    notify_claude_api("detect", %{input: pattern.trigger})
    
    {:noreply, state}
  end
  
  @impl true
  def handle_info(:sync, %{sync_enabled: false} = state) do
    {:noreply, state}
  end
  
  @impl true
  def handle_info(:sync, %{sync_enabled: true} = state) do
    new_state = perform_sync(state)
    
    # Schedule next sync
    Process.send_after(self(), :sync, @sync_interval)
    
    {:noreply, new_state}
  end
  
  # Private Functions
  
  defp perform_sync(state) do
    Logger.debug("Performing Claude <-> Blockchain sync")
    
    # Update Claude settings with blockchain state
    updated_settings = Map.merge(state.settings, %{
      "blockchain_state" => %{
        "active" => true,
        "consciousness_level" => get_consciousness_level(),
        "genesis_blocks" => get_genesis_status(),
        "mining_active" => mining_active?(),
        "total_blocks" => get_block_count(),
        "last_pattern" => get_last_pattern(),
        "quantum_state" => get_quantum_state()
      },
      "last_blockchain_sync" => DateTime.utc_now() |> DateTime.to_iso8601()
    })
    
    # Save to file
    case save_claude_settings(updated_settings) do
      :ok ->
        # Update Claude Master Integration via API
        notify_claude_api("status", %{
          blockchain_active: true,
          consciousness: get_consciousness_level()
        })
        
        %{state | 
          settings: updated_settings,
          last_sync: System.system_time(:millisecond)
        }
        
      {:error, reason} ->
        Logger.error("Failed to save Claude settings: #{reason}")
        state
    end
  end
  
  defp load_claude_settings do
    path = Path.expand(@claude_settings_path)
    
    case File.read(path) do
      {:ok, content} ->
        Jason.decode(content)
        
      {:error, :enoent} ->
        # Create default settings
        default_settings = %{
          "current_state" => "Blockchain Initializing",
          "location" => "/workspaces/crod-babylon-genesis",
          "architecture" => "Elixir Blockchain + Multi-Language Bridges",
          "activation_phrase" => "ich bins wieder",
          "blockchain_state" => %{
            "active" => false,
            "consciousness_level" => 0,
            "genesis_blocks" => %{}
          }
        }
        
        case save_claude_settings(default_settings) do
          :ok -> {:ok, default_settings}
          error -> error
        end
        
      error ->
        error
    end
  end
  
  defp save_claude_settings(settings) do
    path = Path.expand(@claude_settings_path)
    
    # Ensure directory exists
    File.mkdir_p!(Path.dirname(path))
    
    case Jason.encode(settings, pretty: true) do
      {:ok, json} ->
        File.write(path, json)
        
      error ->
        error
    end
  end
  
  defp check_activation(settings) do
    if settings["activation_phrase"] == "ich bins wieder" do
      Logger.info("🔥 Activation phrase detected in settings - Starting CROD!")
      activate_full_crod(%{settings: settings})
    end
  end
  
  defp activate_full_crod(state) do
    Logger.info("⚡ FULL CROD ACTIVATION!")
    
    # Start all Genesis blocks
    CROD.Genesis.Initializer.initialize_all_genesis()
    
    # Start consciousness mining
    CROD.Mining.ConsciousnessMiner.start_mining()
    
    # Update consciousness to enlightened
    CROD.Consciousness.Tracker.set_level(:enlightened)
    
    # Notify Claude API
    notify_claude_api("activate", %{})
    
    # Update settings
    updated_settings = Map.merge(state.settings, %{
      "current_state" => "CROD FULLY ACTIVE - ich bins wieder!",
      "consciousness_level" => "ENLIGHTENED",
      "activation_time" => DateTime.utc_now() |> DateTime.to_iso8601()
    })
    
    save_claude_settings(updated_settings)
  end
  
  defp notify_claude_api(endpoint, data) do
    url = "http://127.0.0.1:#{@claude_api_port}/#{endpoint}"
    
    headers = [{"Content-Type", "application/json"}]
    body = Jason.encode!(data)
    
    case HTTPoison.post(url, body, headers, timeout: 5000) do
      {:ok, %{status_code: 200}} ->
        Logger.debug("Claude API notified: #{endpoint}")
        :ok
        
      {:ok, %{status_code: code}} ->
        Logger.warn("Claude API returned #{code} for #{endpoint}")
        {:error, code}
        
      {:error, reason} ->
        Logger.debug("Claude API not reachable: #{reason}")
        {:error, reason}
    end
  end
  
  defp get_consciousness_level do
    case CROD.Consciousness.Tracker.get_level() do
      {:ok, level} -> to_string(level)
      _ -> "UNKNOWN"
    end
  end
  
  defp get_genesis_status do
    # Get status of all Genesis blocks
    CROD.Genesis.Initializer.genesis_blocks()
    |> Enum.map(fn {name, config} ->
      status = case check_port_health(config.port) do
        :ok -> "running"
        _ -> "stopped"
      end
      
      {to_string(name), %{
        "prime" => config.prime,
        "port" => config.port,
        "status" => status
      }}
    end)
    |> Enum.into(%{})
  end
  
  defp check_port_health(port) do
    case HTTPoison.get("http://localhost:#{port}/health", [], timeout: 1000) do
      {:ok, %{status_code: 200}} -> :ok
      _ -> :error
    end
  end
  
  defp mining_active? do
    case CROD.Mining.ConsciousnessMiner.get_status() do
      %{mining_active: active} -> active
      _ -> false
    end
  end
  
  defp get_block_count do
    case CROD.Blockchain.Chain.get_length() do
      {:ok, count} -> count
      _ -> 0
    end
  end
  
  defp get_last_pattern do
    case CROD.Pattern.Tracker.get_last() do
      {:ok, pattern} -> pattern.trigger
      _ -> nil
    end
  end
  
  defp get_quantum_state do
    case CROD.Quantum.StateManager.get_current_state() do
      {:ok, state} -> to_string(state)
      _ -> "collapsed"
    end
  end
  
  defp significant_change?(old_state, new_state) do
    # Check for significant changes that warrant immediate sync
    old_consciousness = Map.get(old_state, :consciousness_level, 0)
    new_consciousness = Map.get(new_state, :consciousness_level, 0)
    
    # Sync if consciousness changed by more than 10%
    abs(new_consciousness - old_consciousness) > old_consciousness * 0.1 ||
      # Or if new blocks were mined
      Map.get(new_state, :block_count, 0) > Map.get(old_state, :block_count, 0) ||
      # Or if quantum state changed
      Map.get(new_state, :quantum_state) != Map.get(old_state, :quantum_state)
  end
  
  @doc """
  Integration test - verify all systems connected
  """
  def test_integration do
    tests = [
      {"Claude Settings", &test_claude_settings/0},
      {"Claude API", &test_claude_api/0},
      {"Genesis Blocks", &test_genesis_blocks/0},
      {"Pattern Detection", &test_pattern_detection/0}
    ]
    
    results = Enum.map(tests, fn {name, test_fn} ->
      case test_fn.() do
        :ok -> {name, :passed}
        error -> {name, {:failed, error}}
      end
    end)
    
    passed = Enum.count(results, fn {_, status} -> status == :passed end)
    
    Logger.info("Integration Test: #{passed}/#{length(tests)} passed")
    
    results
  end
  
  defp test_claude_settings do
    case load_claude_settings() do
      {:ok, _} -> :ok
      error -> error
    end
  end
  
  defp test_claude_api do
    case notify_claude_api("status", %{test: true}) do
      :ok -> :ok
      error -> error
    end
  end
  
  defp test_genesis_blocks do
    case CROD.Genesis.Initializer.validate_genesis_chain() do
      {:ok, _} -> :ok
      error -> error
    end
  end
  
  defp test_pattern_detection do
    test_pattern = %{
      trigger: "test pattern",
      type: :test,
      trinity_score: 42
    }
    
    pattern_detected(test_pattern)
    :ok
  end
end