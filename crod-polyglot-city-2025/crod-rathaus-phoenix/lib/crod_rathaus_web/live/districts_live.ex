defmodule CrodRathausWeb.DistrictsLive do
  use CrodRathausWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, districts: [
      %{name: "Pattern District", language: "Rust", port: 7007, status: :online},
      %{name: "Memory Quarter", language: "Go", port: 7031, status: :online},
      %{name: "Intelligence Hub", language: "Python", port: 6666, status: :online},
      %{name: "Gateway", language: "JavaScript", port: 7888, status: :online}
    ])}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="container">
      <h1>CROD Polyglot Districts</h1>
      <div class="districts">
        <%= for district <- @districts do %>
          <div class="district">
            <h3><%= district.name %></h3>
            <p>Language: <%= district.language %></p>
            <p>Port: <%= district.port %></p>
            <p class={"status-" <> Atom.to_string(district.status)}>
              Status: <%= district.status %>
            </p>
          </div>
        <% end %>
      </div>
    </div>
    """
  end
end