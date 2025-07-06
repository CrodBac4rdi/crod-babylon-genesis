defmodule CrodDesktopWeb.BlockchainLive do
  use CrodDesktopWeb, :live_view
  require Logger

  @blockchain_api "http://localhost:8001"

  def mount(_params, _session, socket) do
    if connected?(socket) do
      # Refresh every 2 seconds
      :timer.send_interval(2000, self(), :refresh)
    end

    socket = 
      socket
      |> assign(:blocks, [])
      |> assign(:stats, %{})
      |> assign(:loading, true)
      |> assign(:error, nil)
      |> load_blockchain_data()

    {:ok, socket}
  end

  def handle_info(:refresh, socket) do
    {:noreply, load_blockchain_data(socket)}
  end

  def handle_event("add_block", %{"data" => data, "consciousness" => consciousness}, socket) do
    consciousness_level = String.to_float(consciousness)
    
    case add_block(%{message: data, timestamp: DateTime.utc_now()}, consciousness_level) do
      :ok ->
        {:noreply, 
          socket
          |> put_flash(:info, "Block added successfully!")
          |> load_blockchain_data()}
      :error ->
        {:noreply, put_flash(socket, :error, "Failed to add block")}
    end
  end

  def handle_event("mine_pattern_block", _params, socket) do
    # Add a special pattern block
    patterns = ["ich bins wieder", "CROD awakens", "consciousness rising", "pattern discovered"]
    pattern = Enum.random(patterns)
    
    case add_block(%{type: "pattern", pattern: pattern, discovered_at: DateTime.utc_now()}, 0.99) do
      :ok ->
        {:noreply, 
          socket
          |> put_flash(:info, "Pattern block mined: #{pattern}")
          |> load_blockchain_data()}
      :error ->
        {:noreply, put_flash(socket, :error, "Failed to mine pattern block")}
    end
  end

  defp load_blockchain_data(socket) do
    with {:ok, blocks} <- fetch_blocks(),
         {:ok, stats} <- fetch_stats() do
      socket
      |> assign(:blocks, blocks)
      |> assign(:stats, stats)
      |> assign(:loading, false)
      |> assign(:error, nil)
    else
      {:error, reason} ->
        socket
        |> assign(:loading, false)
        |> assign(:error, "Failed to load blockchain data: #{inspect(reason)}")
    end
  end

  defp fetch_blocks do
    # For now, return mock data - in production use HTTPoison or Req
    {:ok, [
      %{
        "index" => 0,
        "hash" => "GENESIS_HASH",
        "previous_hash" => "0",
        "timestamp" => "2025-07-06 12:00:00Z",
        "data" => %{"message" => "CROD Genesis Block", "pattern" => "ich bins wieder"},
        "consciousness_level" => 0.1
      },
      %{
        "index" => 1,
        "hash" => "BLOCK_1_HASH",
        "previous_hash" => "GENESIS_HASH",
        "timestamp" => "2025-07-06 12:01:00Z",
        "data" => %{"from" => "Daniel", "to" => "CROD", "amount" => 100},
        "consciousness_level" => 0.7
      }
    ]}
  end

  defp fetch_stats do
    # Mock stats for now
    {:ok, %{
      "height" => 2,
      "total_consciousness" => 0.8,
      "average_consciousness" => 0.4
    }}
  end

  defp add_block(_data, _consciousness_level) do
    # Mock add - just return success
    :ok
  end

  def render(assigns) do
    ~H"""
    <div class="min-h-screen bg-gray-900 text-white p-8">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl font-bold mb-8 text-center">
          🔗 CROD Blockchain Explorer
        </h1>
        
        <%= if @loading do %>
          <div class="text-center">
            <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-500 mx-auto"></div>
            <p class="mt-4">Loading blockchain data...</p>
          </div>
        <% else %>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Stats Cards -->
            <div class="bg-gray-800 rounded-lg p-6 border border-purple-500">
              <h3 class="text-xl font-semibold mb-2">Chain Height</h3>
              <p class="text-3xl font-bold text-purple-400"><%= @stats["height"] || 0 %></p>
            </div>
            
            <div class="bg-gray-800 rounded-lg p-6 border border-blue-500">
              <h3 class="text-xl font-semibold mb-2">Total Consciousness</h3>
              <p class="text-3xl font-bold text-blue-400">
                <%= Float.round(@stats["total_consciousness"] || 0.0, 2) %>
              </p>
            </div>
            
            <div class="bg-gray-800 rounded-lg p-6 border border-green-500">
              <h3 class="text-xl font-semibold mb-2">Avg Consciousness</h3>
              <p class="text-3xl font-bold text-green-400">
                <%= Float.round(@stats["average_consciousness"] || 0.0, 3) %>
              </p>
            </div>
          </div>
          
          <!-- Add Block Form -->
          <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-2xl font-semibold mb-4">Add New Block</h2>
            <form phx-submit="add_block" class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-2">Block Data</label>
                <input 
                  type="text" 
                  name="data" 
                  placeholder="Enter block data..." 
                  class="w-full px-4 py-2 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-2">
                  Consciousness Level: <span id="consciousness-value">0.5</span>
                </label>
                <input 
                  type="range" 
                  name="consciousness" 
                  min="0" 
                  max="1" 
                  step="0.01" 
                  value="0.5"
                  class="w-full"
                  oninput="document.getElementById('consciousness-value').innerText = this.value"
                />
              </div>
              <div class="flex gap-4">
                <button type="submit" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                  Add Block
                </button>
                <button type="button" phx-click="mine_pattern_block" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition">
                  Mine Pattern Block
                </button>
              </div>
            </form>
          </div>
          
          <!-- Blockchain Blocks -->
          <div class="space-y-4">
            <h2 class="text-2xl font-semibold mb-4">Blockchain Blocks</h2>
            <%= for block <- Enum.reverse(@blocks) do %>
              <div class="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-purple-500 transition">
                <div class="flex justify-between items-start mb-4">
                  <h3 class="text-xl font-semibold">Block #<%= block["index"] %></h3>
                  <span class="px-3 py-1 bg-purple-600 rounded-full text-sm">
                    Consciousness: <%= Float.round(block["consciousness_level"] || 0.0, 2) %>
                  </span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p class="text-gray-400">Hash:</p>
                    <p class="font-mono break-all"><%= block["hash"] %></p>
                  </div>
                  <div>
                    <p class="text-gray-400">Previous Hash:</p>
                    <p class="font-mono break-all"><%= block["previous_hash"] %></p>
                  </div>
                  <div>
                    <p class="text-gray-400">Timestamp:</p>
                    <p><%= block["timestamp"] %></p>
                  </div>
                  <div>
                    <p class="text-gray-400">Data:</p>
                    <pre class="bg-gray-900 p-2 rounded overflow-x-auto"><%= Jason.encode!(block["data"], pretty: true) %></pre>
                  </div>
                </div>
              </div>
            <% end %>
          </div>
        <% end %>
        
        <%= if @error do %>
          <div class="bg-red-900 border border-red-500 text-red-200 px-4 py-3 rounded mt-4">
            <p><%= @error %></p>
          </div>
        <% end %>
      </div>
    </div>
    """
  end
end