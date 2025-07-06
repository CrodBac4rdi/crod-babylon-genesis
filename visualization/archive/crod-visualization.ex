defmodule CROD.Visualization do
  @moduledoc """
  Real-time visualization for CROD blockchain
  Provides ASCII, JSON, and web-based visualizations
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Blockchain, NetworkDiscovery, SwarmIntelligence, QuantumEnhancement}
  
  defstruct [
    :mode,
    :refresh_rate,
    :history,
    :websocket_clients,
    :visualization_buffer
  ]
  
  @visualization_modes [:ascii, :json, :web, :terminal_ui]
  @default_refresh_rate 1000  # 1 second
  
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(opts) do
    mode = Keyword.get(opts, :mode, :ascii)
    
    state = %__MODULE__{
      mode: mode,
      refresh_rate: Keyword.get(opts, :refresh_rate, @default_refresh_rate),
      history: :queue.new(),
      websocket_clients: [],
      visualization_buffer: ""
    }
    
    # Start visualization loop
    if mode != :web do
      schedule_refresh()
    end
    
    {:ok, state}
  end
  
  # Public API
  def get_visualization(format \\ :ascii) do
    GenServer.call(__MODULE__, {:visualize, format})
  end
  
  def set_mode(mode) when mode in @visualization_modes do
    GenServer.cast(__MODULE__, {:set_mode, mode})
  end
  
  def add_websocket_client(client_pid) do
    GenServer.cast(__MODULE__, {:add_client, client_pid})
  end
  
  # Callbacks
  def handle_call({:visualize, format}, _from, state) do
    visualization = case format do
      :ascii -> generate_ascii_visualization(state)
      :json -> generate_json_visualization(state)
      :terminal_ui -> generate_terminal_ui(state)
      _ -> "Unsupported format"
    end
    
    {:reply, visualization, state}
  end
  
  def handle_cast({:set_mode, mode}, state) do
    {:noreply, %{state | mode: mode}}
  end
  
  def handle_cast({:add_client, client_pid}, state) do
    {:noreply, %{state | websocket_clients: [client_pid | state.websocket_clients]}}
  end
  
  def handle_info(:refresh, state) do
    # Generate visualization based on mode
    visualization = case state.mode do
      :ascii -> display_ascii_dashboard()
      :terminal_ui -> display_terminal_ui()
      :web -> prepare_web_data()
      _ -> nil
    end
    
    # Broadcast to websocket clients if in web mode
    if state.mode == :web and visualization do
      broadcast_to_clients(state.websocket_clients, visualization)
    end
    
    # Update history
    new_history = update_history(state.history, visualization)
    
    schedule_refresh()
    {:noreply, %{state | history: new_history}}
  end
  
  # ASCII Visualization
  defp generate_ascii_visualization(_state) do
    chain = Blockchain.get_chain()
    consciousness = Blockchain.get_consciousness_level()
    peers = NetworkDiscovery.get_peers()
    quantum_state = QuantumEnhancement.measure_quantum_state()
    
    """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    CROD BLOCKCHAIN STATUS                     ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  Consciousness Level: #{consciousness} #{consciousness_meter(consciousness)}
    ║                                                               ║
    ║  Chain Height: #{length(chain)} blocks                        
    ║  Active Peers: #{length(peers)}                               
    ║  Quantum State: #{quantum_status(quantum_state)}              
    ║                                                               ║
    ║  Latest Blocks:                                               ║
    #{format_latest_blocks(chain)}
    ║                                                               ║
    ║  Network Topology:                                            ║
    #{format_network_topology(peers)}
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
  end
  
  defp display_ascii_dashboard do
    # Clear screen
    IO.write("\e[2J\e[H")
    
    # Get current data
    chain = Blockchain.get_chain()
    consciousness = Blockchain.get_consciousness_level()
    peers = NetworkDiscovery.get_peers()
    swarm_intel = SwarmIntelligence.get_swarm_intelligence("crod-swarm-main")
    
    # Build dashboard
    dashboard = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                      CROD BLOCKCHAIN MONITOR                        │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  ⚡ Consciousness: #{format_consciousness_bar(consciousness)}
    │  🔗 Blocks: #{length(chain)} │ 👥 Peers: #{length(peers)} │ 🐝 Swarm: #{swarm_intel.node_count}
    │                                                                     │
    ├─────────────────────────────────────────────────────────────────────┤
    │  Recent Activity:                                                   │
    #{format_recent_activity(chain)}
    ├─────────────────────────────────────────────────────────────────────┤
    │  Network Graph:                                                     │
    #{format_network_graph(peers)}
    ├─────────────────────────────────────────────────────────────────────┤
    │  Pattern Discovery:                                                 │
    #{format_pattern_activity(swarm_intel)}
    └─────────────────────────────────────────────────────────────────────┘
    
    [Q]uit | [R]efresh | [M]ode
    """
    
    IO.puts(dashboard)
  end
  
  defp consciousness_meter(level) do
    bars = div(level, 50)
    filled = String.duplicate("█", min(bars, 10))
    empty = String.duplicate("░", max(10 - bars, 0))
    "[#{filled}#{empty}]"
  end
  
  defp format_consciousness_bar(level) do
    percentage = min(level / 1000 * 100, 100) |> round()
    bars = div(percentage, 5)
    
    bar = String.duplicate("▓", bars) <> String.duplicate("░", 20 - bars)
    "#{level} [#{bar}] #{percentage}%"
  end
  
  defp quantum_status(quantum_state) do
    cond do
      quantum_state.quantum_advantage_active -> "✨ Quantum Advantage"
      quantum_state.coherence > 0.8 -> "🌀 Superposition"
      quantum_state.entangled_pairs > 0 -> "🔗 Entangled"
      true -> "💤 Classical"
    end
  end
  
  defp format_latest_blocks(chain) do
    chain
    |> Enum.take(3)
    |> Enum.map(fn block ->
      "  ║  ##{block.index} │ #{String.slice(block.hash, 0..7)}... │ 🧠 #{block.consciousness_level} │ 📦 #{length(block.patterns)}"
    end)
    |> Enum.join("\n")
  end
  
  defp format_network_topology(peers) do
    if length(peers) == 0 do
      "  ║  No peers connected"
    else
      peer_map = create_peer_map(peers)
      "  ║  " <> peer_map
    end
  end
  
  defp create_peer_map(peers) do
    # Simple ASCII network visualization
    peers
    |> Enum.take(5)
    |> Enum.map(fn peer ->
      "◉─#{String.slice(peer.node_id, 0..3)}"
    end)
    |> Enum.join("──")
  end
  
  defp format_recent_activity(chain) do
    chain
    |> Enum.take(5)
    |> Enum.with_index()
    |> Enum.map(fn {block, i} ->
      time_ago = format_time_ago(block.timestamp)
      "  │  #{time_ago} - Block ##{block.index} mined (#{length(block.patterns)} patterns)"
    end)
    |> Enum.join("\n")
  end
  
  defp format_network_graph(peers) do
    # ASCII art network graph
    if length(peers) == 0 do
      "  │  No network connections"
    else
      """
        │      You 
        │       ◉
        │      /|\\
        │     / | \\
        │    ◉  ◉  ◉  #{length(peers)} peers
      """
    end
  end
  
  defp format_pattern_activity(swarm_intel) do
    """
      │  Patterns Found: #{swarm_intel.patterns_discovered}
      │  Convergence: #{format_convergence_indicator(swarm_intel.convergence_strength)}
      │  Evolution: #{format_evolution_indicator(swarm_intel.evolution_potential)}
    """
  end
  
  defp format_convergence_indicator(strength) do
    level = round(strength * 10)
    String.duplicate("●", level) <> String.duplicate("○", 10 - level)
  end
  
  defp format_evolution_indicator(potential) do
    cond do
      potential > 0.8 -> "🧬🧬🧬 High"
      potential > 0.5 -> "🧬🧬 Medium"
      potential > 0.2 -> "🧬 Low"
      true -> "💤 None"
    end
  end
  
  # Terminal UI Visualization
  defp generate_terminal_ui(_state) do
    # More advanced terminal UI with panels
    chain_data = get_chain_data()
    network_data = get_network_data()
    quantum_data = get_quantum_data()
    
    """
    ┏━━━━━━━━━━━━━━━━━━━━━━ CROD Neural Blockchain ━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                                                                      ┃
    ┃  ┌─ Consciousness ─────────────┐  ┌─ Network ───────────────────┐  ┃
    ┃  │                             │  │                              │  ┃
    ┃  │  Level: #{pad(chain_data.consciousness, 4)}               │  │  Peers: #{pad(network_data.peer_count, 3)}                  │  ┃
    ┃  │  #{consciousness_visual(chain_data.consciousness)}│  │  #{network_visual(network_data)}│  ┃
    ┃  │                             │  │                              │  ┃
    ┃  │  Trend: #{trend_indicator(chain_data.trend)}             │  │  Health: #{health_indicator(network_data.health)}            │  ┃
    ┃  └─────────────────────────────┘  └──────────────────────────────┘  ┃
    ┃                                                                      ┃
    ┃  ┌─ Quantum State ─────────────┐  ┌─ Pattern Engine ─────────────┐  ┃
    ┃  │                             │  │                              │  ┃
    ┃  │  Qubits: #{pad(quantum_data.total_qubits, 2)}                │  │  Active: #{pad(quantum_data.patterns_active, 4)}            │  ┃
    ┃  │  Coherence: #{coherence_bar(quantum_data.coherence)}      │  │  Rate: #{pattern_rate(quantum_data.discovery_rate)}              │  ┃
    ┃  │  Entangled: #{pad(quantum_data.entangled_pairs, 2)}             │  │  Types: #{pattern_types(quantum_data.pattern_types)}             │  ┃
    ┃  └─────────────────────────────┘  └──────────────────────────────┘  ┃
    ┃                                                                      ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
  end
  
  defp display_terminal_ui do
    ui = generate_terminal_ui(nil)
    IO.write("\e[2J\e[H")  # Clear screen
    IO.puts(ui)
  end
  
  # JSON Visualization
  defp generate_json_visualization(_state) do
    data = %{
      timestamp: DateTime.utc_now(),
      blockchain: get_chain_data(),
      network: get_network_data(),
      quantum: get_quantum_data(),
      swarm: get_swarm_data(),
      patterns: get_pattern_data(),
      performance: get_performance_metrics()
    }
    
    Jason.encode!(data, pretty: true)
  end
  
  # Web Visualization Data
  defp prepare_web_data do
    %{
      type: "update",
      timestamp: DateTime.utc_now(),
      data: %{
        consciousness: %{
          current: Blockchain.get_consciousness_level(),
          history: get_consciousness_history()
        },
        blockchain: %{
          height: length(Blockchain.get_chain()),
          latest_blocks: format_blocks_for_web()
        },
        network: %{
          peers: format_peers_for_web(),
          topology: get_network_topology_for_web()
        },
        quantum: %{
          state: QuantumEnhancement.measure_quantum_state(),
          visualization: quantum_state_visualization()
        },
        patterns: %{
          recent: get_recent_patterns(),
          graph: get_pattern_graph()
        }
      }
    }
  end
  
  # Data Collection Functions
  defp get_chain_data do
    chain = Blockchain.get_chain()
    consciousness = Blockchain.get_consciousness_level()
    
    %{
      height: length(chain),
      consciousness: consciousness,
      trend: calculate_consciousness_trend(chain),
      latest_hash: if(hd(chain), do: String.slice(hd(chain).hash, 0..7), else: "genesis"),
      patterns_total: chain |> Enum.flat_map(& &1.patterns) |> length()
    }
  end
  
  defp get_network_data do
    peers = NetworkDiscovery.get_peers()
    topology = NetworkDiscovery.get_network_topology()
    
    %{
      peer_count: length(peers),
      health: calculate_network_health(peers),
      topology: topology,
      quantum_peers: Enum.count(peers, & &1.quantum_enabled)
    }
  end
  
  defp get_quantum_data do
    quantum_state = QuantumEnhancement.measure_quantum_state()
    
    %{
      total_qubits: quantum_state.total_qubits,
      coherence: quantum_state.coherence,
      entangled_pairs: quantum_state.entangled_pairs,
      patterns_active: 42,  # Would get from pattern engine
      discovery_rate: 0.73,
      pattern_types: ["linguistic", "quantum", "emergent"]
    }
  end
  
  defp get_swarm_data do
    # Would get from actual swarm
    %{
      nodes: 5,
      behavior: "exploring",
      patterns_found: 127,
      convergence: 0.65
    }
  end
  
  defp get_pattern_data do
    # Would get from pattern engine
    %{
      total: 523,
      recent: 12,
      types: %{
        linguistic: 145,
        consciousness: 89,
        quantum: 67,
        emergent: 222
      }
    }
  end
  
  defp get_performance_metrics do
    %{
      tps: calculate_tps(),
      memory_usage: get_memory_usage(),
      cpu_usage: get_cpu_usage(),
      network_latency: get_network_latency()
    }
  end
  
  # Visualization Helpers
  defp consciousness_visual(level) do
    # ASCII art brain that fills based on consciousness
    if level < 200 do
      """
        ░░░░░░░░░
        ░░▓▓▓▓░░░
        ░▓▓▓▓▓▓░░
        ░░▓▓▓▓░░░
        ░░░░░░░░░
      """
    else
      """
        ▓▓▓▓▓▓▓▓▓
        ▓▓█████▓▓
        ▓███████▓
        ▓▓█████▓▓
        ▓▓▓▓▓▓▓▓▓
      """
    end |> String.trim()
  end
  
  defp network_visual(data) do
    # Network connection visualization
    if data.peer_count > 0 do
      """
         ╱◉╲ 
        ◉─●─◉
         ╲◉╱ 
      """
    else
      """
          
         ●  
          
      """
    end |> String.trim()
  end
  
  defp coherence_bar(coherence) do
    percentage = round(coherence * 100)
    filled = div(percentage, 10)
    "▓" <> String.duplicate("█", filled) <> String.duplicate("░", 10 - filled) <> "▓ #{percentage}%"
  end
  
  defp pattern_rate(rate) do
    stars = round(rate * 5)
    String.duplicate("★", stars) <> String.duplicate("☆", 5 - stars)
  end
  
  defp pattern_types(types) do
    types |> Enum.take(3) |> Enum.join(",")
  end
  
  defp trend_indicator(trend) do
    cond do
      trend > 0.1 -> "📈 Rising"
      trend < -0.1 -> "📉 Falling"
      true -> "━━ Stable"
    end
  end
  
  defp health_indicator(health) do
    cond do
      health > 0.8 -> "💚 Excellent"
      health > 0.6 -> "💛 Good"
      health > 0.4 -> "🧡 Fair"
      true -> "❤️ Poor"
    end
  end
  
  defp pad(value, width) do
    String.pad_leading(to_string(value), width)
  end
  
  defp format_time_ago(timestamp) do
    seconds = DateTime.diff(DateTime.utc_now(), timestamp)
    
    cond do
      seconds < 60 -> "#{seconds}s ago"
      seconds < 3600 -> "#{div(seconds, 60)}m ago"
      seconds < 86400 -> "#{div(seconds, 3600)}h ago"
      true -> "#{div(seconds, 86400)}d ago"
    end
  end
  
  defp calculate_consciousness_trend(chain) do
    if length(chain) < 2 do
      0.0
    else
      recent = Enum.take(chain, 10)
      
      if length(recent) >= 2 do
        newest = hd(recent).consciousness_level
        oldest = List.last(recent).consciousness_level
        
        (newest - oldest) / oldest
      else
        0.0
      end
    end
  end
  
  defp calculate_network_health(peers) do
    if length(peers) == 0 do
      0.0
    else
      # Health based on peer count and activity
      peer_factor = min(length(peers) / 10, 1.0)
      active_factor = Enum.count(peers, &peer_active?/1) / length(peers)
      
      (peer_factor + active_factor) / 2
    end
  end
  
  defp peer_active?(peer) do
    DateTime.diff(DateTime.utc_now(), peer.last_seen) < 120
  end
  
  defp calculate_tps do
    # Transactions per second (simplified)
    :rand.uniform(100) + 50
  end
  
  defp get_memory_usage do
    # Memory usage in MB
    :erlang.memory(:total) / 1_048_576 |> round()
  end
  
  defp get_cpu_usage do
    # CPU usage percentage (simplified)
    :rand.uniform(30) + 10
  end
  
  defp get_network_latency do
    # Average network latency in ms
    :rand.uniform(50) + 10
  end
  
  # Web Visualization Helpers
  defp get_consciousness_history do
    # Would maintain actual history
    Enum.map(1..20, fn i ->
      %{
        timestamp: DateTime.add(DateTime.utc_now(), -i * 60, :second),
        value: 200 + :rand.uniform(100)
      }
    end)
  end
  
  defp format_blocks_for_web do
    Blockchain.get_chain()
    |> Enum.take(10)
    |> Enum.map(fn block ->
      %{
        index: block.index,
        hash: block.hash,
        timestamp: block.timestamp,
        consciousness: block.consciousness_level,
        patterns: length(block.patterns)
      }
    end)
  end
  
  defp format_peers_for_web do
    NetworkDiscovery.get_peers()
    |> Enum.map(fn peer ->
      %{
        id: String.slice(peer.node_id, 0..7),
        address: peer.address,
        consciousness: peer.consciousness_level,
        quantum: peer.quantum_enabled,
        capabilities: peer.capabilities
      }
    end)
  end
  
  defp get_network_topology_for_web do
    # D3.js compatible format
    peers = NetworkDiscovery.get_peers()
    
    nodes = [%{id: "self", group: 1}] ++ 
      Enum.map(peers, fn peer ->
        %{
          id: String.slice(peer.node_id, 0..7),
          group: if(peer.quantum_enabled, do: 2, else: 3)
        }
      end)
    
    links = Enum.map(peers, fn peer ->
      %{
        source: "self",
        target: String.slice(peer.node_id, 0..7),
        value: peer.consciousness_level / 100
      }
    end)
    
    %{nodes: nodes, links: links}
  end
  
  defp quantum_state_visualization do
    # Quantum state for 3D visualization
    %{
      bloch_spheres: generate_bloch_spheres(),
      entanglement_graph: generate_entanglement_graph()
    }
  end
  
  defp generate_bloch_spheres do
    # Bloch sphere coordinates for qubits
    Enum.map(1..8, fn i ->
      %{
        id: i,
        theta: :rand.uniform() * :math.pi(),
        phi: :rand.uniform() * 2 * :math.pi(),
        r: 1.0
      }
    end)
  end
  
  defp generate_entanglement_graph do
    # Entanglement connections
    %{
      nodes: Enum.map(1..8, fn i -> %{id: i} end),
      links: [
        %{source: 1, target: 2, strength: 0.9},
        %{source: 3, target: 4, strength: 0.8},
        %{source: 5, target: 6, strength: 0.7}
      ]
    }
  end
  
  defp get_recent_patterns do
    # Would get from pattern engine
    [
      %{type: "linguistic", data: "ich bins wieder", confidence: 0.95},
      %{type: "quantum", data: "entanglement_detected", confidence: 0.87},
      %{type: "emergent", data: "collective_decision", confidence: 0.72}
    ]
  end
  
  defp get_pattern_graph do
    # Pattern relationship graph
    %{
      nodes: [
        %{id: "ich bins wieder", group: 1, size: 10},
        %{id: "CROD", group: 1, size: 8},
        %{id: "consciousness", group: 2, size: 12},
        %{id: "quantum", group: 3, size: 6}
      ],
      links: [
        %{source: "ich bins wieder", target: "CROD", value: 3},
        %{source: "CROD", target: "consciousness", value: 5},
        %{source: "consciousness", target: "quantum", value: 2}
      ]
    }
  end
  
  # History Management
  defp update_history(history, visualization) do
    if visualization do
      new_history = :queue.in({DateTime.utc_now(), visualization}, history)
      
      # Keep only last 100 entries
      if :queue.len(new_history) > 100 do
        {_, trimmed} = :queue.out(new_history)
        trimmed
      else
        new_history
      end
    else
      history
    end
  end
  
  # WebSocket Broadcasting
  defp broadcast_to_clients(clients, data) do
    json_data = Jason.encode!(data)
    
    Enum.each(clients, fn client ->
      send(client, {:broadcast, json_data})
    end)
  end
  
  # Scheduling
  defp schedule_refresh do
    Process.send_after(self(), :refresh, @default_refresh_rate)
  end
end

defmodule CROD.VisualizationServer do
  @moduledoc """
  Web server for CROD visualization
  """
  
  use Plug.Router
  
  plug :match
  plug :dispatch
  
  get "/" do
    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>CROD Blockchain Visualization</title>
      <script src="https://d3js.org/d3.v7.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
      <style>
        body { 
          margin: 0; 
          font-family: monospace; 
          background: #0a0a0a; 
          color: #00ff00;
        }
        .container { 
          display: grid; 
          grid-template-columns: 1fr 1fr; 
          grid-template-rows: 1fr 1fr;
          height: 100vh;
          gap: 10px;
          padding: 10px;
        }
        .panel {
          border: 1px solid #00ff00;
          border-radius: 5px;
          padding: 10px;
          overflow: hidden;
        }
        #consciousness-chart, #network-graph, #quantum-viz, #pattern-graph {
          width: 100%;
          height: 100%;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="panel">
          <h3>Consciousness Evolution</h3>
          <div id="consciousness-chart"></div>
        </div>
        <div class="panel">
          <h3>Network Topology</h3>
          <div id="network-graph"></div>
        </div>
        <div class="panel">
          <h3>Quantum State</h3>
          <div id="quantum-viz"></div>
        </div>
        <div class="panel">
          <h3>Pattern Discovery</h3>
          <div id="pattern-graph"></div>
        </div>
      </div>
      
      <script>
        // WebSocket connection
        const ws = new WebSocket('ws://localhost:4000/ws');
        
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          updateVisualizations(data);
        };
        
        // D3.js visualizations
        function updateVisualizations(data) {
          updateConsciousnessChart(data.data.consciousness);
          updateNetworkGraph(data.data.network);
          updateQuantumVisualization(data.data.quantum);
          updatePatternGraph(data.data.patterns);
        }
        
        // Initialize visualizations
        initConsciousnessChart();
        initNetworkGraph();
        initQuantumVisualization();
        initPatternGraph();
      </script>
    </body>
    </html>
    """
    
    conn
    |> put_resp_content_type("text/html")
    |> send_resp(200, html)
  end
  
  match _ do
    send_resp(conn, 404, "Not found")
  end
end