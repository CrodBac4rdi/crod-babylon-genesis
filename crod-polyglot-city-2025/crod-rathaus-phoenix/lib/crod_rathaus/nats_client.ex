defmodule CrodRathaus.NatsClient do
  use GenServer
  require Logger

  def start_link(_) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end

  def init(_) do
    {:ok, conn} = Nats.Connection.start_link(host: "nats", port: 4222)
    Process.send_after(self(), :subscribe, 1000)
    {:ok, %{conn: conn}}
  end

  def handle_info(:subscribe, %{conn: conn} = state) do
    Nats.sub(conn, self(), "crod.>")
    Logger.info("CROD Rathaus subscribed to NATS")
    {:noreply, state}
  end

  def handle_info({:msg, %{topic: topic, body: body}}, state) do
    Logger.info("Received: #{topic} - #{body}")
    Phoenix.PubSub.broadcast(CrodRathaus.PubSub, "crod:events", {:nats_event, topic, body})
    {:noreply, state}
  end
end
