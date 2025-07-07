defmodule CrodRathausWeb.DashboardLive do
  use CrodRathausWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Phoenix.PubSub.subscribe(CrodRathaus.PubSub, "crod:events")
    end

    {:ok, assign(socket, events: [], districts: %{
      "pattern" => %{status: :connecting, port: 7007},
      "memory" => %{status: :connecting, port: 7031},
      "gateway" => %{status: :connecting, port: 7888},
      "parasit" => %{status: :connecting, port: 6666}
    })}
  end

  @impl true
  def handle_info({:nats_event, topic, body}, socket) do
    event = %{topic: topic, body: body, timestamp: DateTime.utc_now()}
    {:noreply, update(socket, :events, fn events -> [event | Enum.take(events, 99)] end)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="container mx-auto p-4">
      <h1 class="text-4xl font-bold mb-8">CROD Polyglot City 2025 - Rathaus</h1>
      
      <div class="grid grid-cols-2 gap-6">
        <div>
          <h2 class="text-2xl font-semibold mb-4">Districts Status</h2>
          <div class="space-y-2">
            <%= for {name, info} <- @districts do %>
              <div class="p-3 border rounded flex justify-between">
                <span class="font-medium"><%= name %></span>
                <span class={"px-2 py-1 rounded text-sm " <> status_class(info.status)}>
                  <%= info.status %> (:<%= info.port %>)
                </span>
              </div>
            <% end %>
          </div>
        </div>
        
        <div>
          <h2 class="text-2xl font-semibold mb-4">Recent Events</h2>
          <div class="space-y-1 max-h-96 overflow-y-auto">
            <%= for event <- @events do %>
              <div class="p-2 bg-gray-100 rounded text-sm">
                <div class="font-mono"><%= event.topic %></div>
                <div class="text-gray-600"><%= event.body %></div>
              </div>
            <% end %>
          </div>
        </div>
      </div>
    </div>
    """
  end

  defp status_class(:online), do: "bg-green-500 text-white"
  defp status_class(:connecting), do: "bg-yellow-500 text-white"
  defp status_class(:offline), do: "bg-red-500 text-white"
end
