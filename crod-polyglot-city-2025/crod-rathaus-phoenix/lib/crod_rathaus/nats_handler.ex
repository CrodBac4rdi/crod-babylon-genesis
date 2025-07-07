defmodule CrodRathaus.NatsHandler do
  use GenServer
  require Logger

  @nats_url "nats://localhost:4222"

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    send(self(), :connect)
    {:ok, %{conn: nil, subscriptions: []}}
  end

  def handle_info(:connect, state) do
    case Gnat.start_link(%{connection_settings: [@nats_url]}) do
      {:ok, conn} ->
        Logger.info("Connected to NATS at #{@nats_url}")
        subscribe_to_topics(conn)
        {:noreply, %{state | conn: conn}}
      
      {:error, reason} ->
        Logger.error("Failed to connect to NATS: #{inspect(reason)}")
        Process.send_after(self(), :connect, 5000)
        {:noreply, state}
    end
  end

  def handle_info({:nats_msg, topic, msg}, state) do
    Logger.info("Received message on #{topic}: #{msg}")
    
    case Jason.decode(msg) do
      {:ok, data} ->
        handle_crod_message(topic, data)
      {:error, _} ->
        Logger.warning("Invalid JSON message: #{msg}")
    end
    
    {:noreply, state}
  end

  defp subscribe_to_topics(conn) do
    topics = [
      "crod.rathaus.commands",
      "crod.pattern.detected",
      "crod.memory.update",
      "crod.parasit.status",
      "crod.gateway.request"
    ]
    
    Enum.each(topics, fn topic ->
      {:ok, _sub} = Gnat.sub(conn, self(), topic)
      Logger.info("Subscribed to #{topic}")
    end)
  end

  defp handle_crod_message("crod.pattern.detected", data) do
    # Broadcast to LiveView
    Phoenix.PubSub.broadcast(
      CrodRathaus.PubSub,
      "patterns",
      {:pattern_detected, data}
    )
  end

  defp handle_crod_message(topic, data) do
    Phoenix.PubSub.broadcast(
      CrodRathaus.PubSub,
      "crod_events",
      {:crod_event, topic, data}
    )
  end

  def publish(topic, message) do
    GenServer.cast(__MODULE__, {:publish, topic, message})
  end

  def handle_cast({:publish, topic, message}, %{conn: conn} = state) when not is_nil(conn) do
    case Jason.encode(message) do
      {:ok, json} ->
        Gnat.pub(conn, topic, json)
      {:error, reason} ->
        Logger.error("Failed to encode message: #{inspect(reason)}")
    end
    
    {:noreply, state}
  end

  def handle_cast({:publish, _topic, _message}, state) do
    Logger.warning("Cannot publish - not connected to NATS")
    {:noreply, state}
  end
end