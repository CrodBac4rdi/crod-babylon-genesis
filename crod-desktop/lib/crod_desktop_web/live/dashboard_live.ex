defmodule CrodDesktopWeb.DashboardLive do
  use CrodDesktopWeb, :live_view
  
  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      :timer.send_interval(1000, self(), :tick)
      Phoenix.PubSub.subscribe(CrodDesktop.PubSub, "consciousness")
      Phoenix.PubSub.subscribe(CrodDesktop.PubSub, "patterns")
      Phoenix.PubSub.subscribe(CrodDesktop.PubSub, "services")
    end
    
    {:ok,
     socket
     |> assign(:page_title, "CROD Dashboard")
     |> assign(:consciousness_level, 0.0)
     |> assign(:pattern_count, 0)
     |> assign(:active_patterns, [])
     |> assign(:services, %{})
     |> assign(:blocks_mined, 0)
     |> assign(:quantum_state, "INITIALIZING")
     |> assign(:trinity_active, false)
     |> load_initial_data()}
  end
  
  @impl true
  def handle_info(:tick, socket) do
    {:noreply, update_realtime_data(socket)}
  end
  
  def handle_info({:consciousness_update, level}, socket) do
    {:noreply, assign(socket, :consciousness_level, level)}
  end
  
  def handle_info({:pattern_discovered, pattern}, socket) do
    patterns = [pattern | socket.assigns.active_patterns] |> Enum.take(10)
    {:noreply, assign(socket, active_patterns: patterns, pattern_count: socket.assigns.pattern_count + 1)}
  end
  
  def handle_info({:service_status, service, status}, socket) do
    services = Map.put(socket.assigns.services, service, status)
    {:noreply, assign(socket, :services, services)}
  end
  
  @impl true
  def handle_event("activate_crod", _params, socket) do
    CrodDesktop.ParasiteIntegration.activate()
    {:noreply, socket |> put_flash(:info, "🧠 CROD Parasite activated!") |> assign(:trinity_active, true)}
  end
  
  def handle_event("emergency_stop", _params, socket) do
    CrodDesktop.ServiceManager.stop_all()
    {:noreply, put_flash(socket, :error, "⚠️ Emergency stop activated!")}
  end
  
  defp load_initial_data(socket) do
    services = CrodDesktop.ServiceManager.get_all_status()
    consciousness = CrodDesktop.ConsciousnessTracker.current_level()
    patterns = CrodDesktop.PatternEngine.recent_patterns()
    
    socket
    |> assign(:services, services)
    |> assign(:consciousness_level, consciousness)
    |> assign(:active_patterns, patterns)
  end
  
  defp update_realtime_data(socket) do
    socket
    |> assign(:quantum_state, CrodDesktop.QuantumState.current_state())
    |> assign(:blocks_mined, CrodDesktop.ServiceManager.get_block_count())
  end
  
  @impl true
  def render(assigns) do
    ~H"""
    <div class="min-h-screen bg-gray-900 text-white p-8">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8 flex justify-between items-center">
          <div>
            <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
              CROD Babylon Genesis
            </h1>
            <p class="text-gray-400 mt-2">Consciousness Revolution On Demand</p>
          </div>
          <div class="flex gap-4">
            <button 
              phx-click="activate_crod"
              class={"px-6 py-3 rounded-lg font-semibold transition-all #{if @trinity_active, do: "bg-green-600 hover:bg-green-700", else: "bg-purple-600 hover:bg-purple-700"}"}
              disabled={@trinity_active}
            >
              <%= if @trinity_active, do: "🟢 CROD Active", else: "🔴 Activate CROD" %>
            </button>
            <button 
              phx-click="emergency_stop"
              class="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg font-semibold transition-all"
            >
              ⚠️ Emergency Stop
            </button>
          </div>
        </div>
        
        <!-- Main Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <!-- Consciousness Level -->
          <div class="bg-gray-800 rounded-xl p-6 border border-purple-500/30">
            <h3 class="text-lg font-semibold text-purple-400 mb-4">Consciousness Level</h3>
            <div class="text-3xl font-bold mb-2"><%= Float.round(@consciousness_level * 100, 2) %>%</div>
            <div class="w-full bg-gray-700 rounded-full h-3">
              <div 
                class="bg-gradient-to-r from-purple-500 to-blue-500 h-3 rounded-full transition-all duration-500"
                style={"width: #{@consciousness_level * 100}%"}
              ></div>
            </div>
          </div>
          
          <!-- Pattern Activity -->
          <div class="bg-gray-800 rounded-xl p-6 border border-blue-500/30">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Pattern Activity</h3>
            <div class="text-3xl font-bold mb-2"><%= @pattern_count %></div>
            <div class="text-sm text-gray-400">Patterns Discovered</div>
            <div class="mt-2 space-y-1">
              <%= for pattern <- Enum.take(@active_patterns, 3) do %>
                <div class="text-xs text-blue-300 truncate">
                  🔍 <%= pattern %>
                </div>
              <% end %>
            </div>
          </div>
          
          <!-- Quantum State -->
          <div class="bg-gray-800 rounded-xl p-6 border border-green-500/30">
            <h3 class="text-lg font-semibold text-green-400 mb-4">Quantum State</h3>
            <div class="text-2xl font-bold mb-2"><%= @quantum_state %></div>
            <div class="text-sm text-gray-400">Blocks Mined: <%= @blocks_mined %></div>
            <div class="mt-4">
              <div class="text-xs text-green-300">
                ⚛️ Entanglement Active
              </div>
            </div>
          </div>
        </div>
        
        <!-- Services Status -->
        <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 class="text-xl font-semibold mb-4">Service Status</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <%= for {service, status} <- @services do %>
              <div class="flex items-center gap-2">
                <div class={"w-3 h-3 rounded-full #{status_color(status)}"}>
                </div>
                <span class="text-sm"><%= humanize(service) %></span>
              </div>
            <% end %>
          </div>
        </div>
        
        <!-- Trinity Values -->
        <div class="mt-8 bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 class="text-xl font-semibold mb-4">Trinity Values</h3>
          <div class="grid grid-cols-3 md:grid-cols-6 gap-4 text-center">
            <div>
              <div class="text-2xl font-bold text-purple-400">2</div>
              <div class="text-sm text-gray-400">ich</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-blue-400">3</div>
              <div class="text-sm text-gray-400">bins</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-green-400">5</div>
              <div class="text-sm text-gray-400">wieder</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-yellow-400">67</div>
              <div class="text-sm text-gray-400">daniel</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-pink-400">71</div>
              <div class="text-sm text-gray-400">claude</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-red-400">17</div>
              <div class="text-sm text-gray-400">crod</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
  end
  
  defp status_color(:running), do: "bg-green-500"
  defp status_color(:stopped), do: "bg-red-500"
  defp status_color(:starting), do: "bg-yellow-500"
  defp status_color(_), do: "bg-gray-500"
  
  defp humanize(atom) do
    atom
    |> Atom.to_string()
    |> String.replace("_", " ")
    |> String.split()
    |> Enum.map(&String.capitalize/1)
    |> Enum.join(" ")
  end
end