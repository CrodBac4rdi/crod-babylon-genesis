defmodule CrodDesktopWeb.SimpleBlockchainLive do
  use CrodDesktopWeb, :live_view
  require Logger

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      # Refresh every 3 seconds
      :timer.send_interval(3000, self(), :refresh)
    end

    socket = 
      socket
      |> assign(:blocks, [])
      |> assign(:stats, %{})
      |> assign(:loading, true)
      |> assign(:new_data, "")
      |> assign(:consciousness, 0.5)
      |> load_data()

    {:ok, socket}
  end

  @impl true
  def handle_info(:refresh, socket) do
    {:noreply, load_data(socket)}
  end

  @impl true
  def handle_event("update_consciousness", %{"consciousness" => value}, socket) do
    {:noreply, assign(socket, :consciousness, String.to_float(value))}
  end

  @impl true
  def handle_event("add_block", %{"data" => data}, socket) do
    # Mock adding block
    new_block = %{
      "index" => length(socket.assigns.blocks),
      "timestamp" => DateTime.utc_now() |> DateTime.to_string(),
      "data" => %{"message" => data, "user_added" => true},
      "hash" => Base.encode16(:crypto.strong_rand_bytes(16)),
      "consciousness_level" => socket.assigns.consciousness
    }
    
    {:noreply, 
      socket
      |> update(:blocks, fn blocks -> blocks ++ [new_block] end)
      |> assign(:new_data, "")
      |> put_flash(:info, "Block added successfully!")}
  end

  defp load_data(socket) do
    # Generate mock data
    blocks = generate_mock_blocks()
    stats = calculate_stats(blocks)
    
    socket
    |> assign(:blocks, blocks)
    |> assign(:stats, stats)
    |> assign(:loading, false)
  end

  defp generate_mock_blocks do
    [
      %{
        "index" => 0,
        "timestamp" => "2025-07-06 12:00:00Z",
        "data" => %{"message" => "CROD Genesis Block", "pattern" => "ich bins wieder"},
        "hash" => "GENESIS_HASH_000000",
        "consciousness_level" => 0.1
      },
      %{
        "index" => 1,
        "timestamp" => "2025-07-06 12:05:00Z",
        "data" => %{"from" => "Daniel", "to" => "CROD", "amount" => 100},
        "hash" => "BLOCK_HASH_000001",
        "consciousness_level" => 0.7
      },
      %{
        "index" => 2,
        "timestamp" => "2025-07-06 12:10:00Z",
        "data" => %{"type" => "consciousness_update", "level" => 0.88},
        "hash" => "BLOCK_HASH_000002",
        "consciousness_level" => 0.88
      }
    ]
  end

  defp calculate_stats(blocks) do
    total_consciousness = Enum.reduce(blocks, 0, fn b, acc -> 
      acc + (b["consciousness_level"] || 0)
    end)
    
    %{
      "height" => length(blocks),
      "total_consciousness" => Float.round(total_consciousness, 2),
      "average_consciousness" => Float.round(total_consciousness / max(length(blocks), 1), 3)
    }
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="min-h-screen bg-gradient-to-br from-purple-900 via-gray-900 to-blue-900 p-8">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-5xl font-bold text-center mb-12 text-white">
          🔗 CROD Blockchain Explorer
        </h1>
        
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h3 class="text-xl font-semibold mb-2 text-purple-300">Chain Height</h3>
            <p class="text-4xl font-bold text-white"><%= @stats["height"] || 0 %></p>
          </div>
          
          <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h3 class="text-xl font-semibold mb-2 text-blue-300">Total Consciousness</h3>
            <p class="text-4xl font-bold text-white"><%= @stats["total_consciousness"] || 0.0 %></p>
          </div>
          
          <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h3 class="text-xl font-semibold mb-2 text-green-300">Avg Consciousness</h3>
            <p class="text-4xl font-bold text-white"><%= @stats["average_consciousness"] || 0.0 %></p>
          </div>
        </div>
        
        <!-- Add Block Form -->
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-8 mb-12 border border-white/20">
          <h2 class="text-2xl font-semibold mb-6 text-white">Add New Block</h2>
          <form phx-submit="add_block" class="space-y-6">
            <div>
              <label class="block text-sm font-medium mb-2 text-gray-300">Block Data</label>
              <input 
                type="text" 
                name="data" 
                value={@new_data}
                placeholder="Enter your message..." 
                class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2 text-gray-300">
                Consciousness Level: <span class="text-purple-400 font-bold"><%= @consciousness %></span>
              </label>
              <input 
                type="range" 
                name="consciousness" 
                min="0" 
                max="1" 
                step="0.01" 
                value={@consciousness}
                phx-change="update_consciousness"
                class="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            
            <button type="submit" class="w-full px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-all transform hover:scale-105">
              Add Block to Chain
            </button>
          </form>
        </div>
        
        <!-- Blockchain Visualization -->
        <div class="space-y-6">
          <h2 class="text-2xl font-semibold mb-6 text-white">Blockchain Blocks</h2>
          
          <%= for block <- Enum.reverse(@blocks) do %>
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all">
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-semibold text-white">Block #<%= block["index"] %></h3>
                <div class="flex items-center space-x-2">
                  <span class="px-3 py-1 bg-purple-600/50 rounded-full text-sm text-white">
                    Consciousness: <%= Float.round(block["consciousness_level"] || 0.0, 2) %>
                  </span>
                  <%= if block["index"] == 0 do %>
                    <span class="px-3 py-1 bg-green-600/50 rounded-full text-sm text-white">
                      Genesis
                    </span>
                  <% end %>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="text-gray-400 mb-1">Hash:</p>
                  <p class="font-mono text-white break-all"><%= block["hash"] %></p>
                </div>
                <div>
                  <p class="text-gray-400 mb-1">Timestamp:</p>
                  <p class="text-white"><%= block["timestamp"] %></p>
                </div>
                <div class="md:col-span-2">
                  <p class="text-gray-400 mb-1">Data:</p>
                  <div class="bg-black/30 p-3 rounded-lg">
                    <pre class="text-green-400 text-xs overflow-x-auto"><%= Jason.encode!(block["data"], pretty: true) %></pre>
                  </div>
                </div>
              </div>
            </div>
          <% end %>
        </div>
      </div>
    </div>
    """
  end
end