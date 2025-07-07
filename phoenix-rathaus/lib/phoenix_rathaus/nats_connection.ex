defmodule PhoenixRathaus.NatsConnection do
  use GenServer
  require Logger

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def init(_state) do
    {:ok, %{}, {:continue, :connect}}
  end

  def handle_continue(:connect, state) do
    case Gnat.sub(:gnat, self(), "crod.>") do
      {:ok, _sub} ->
        Logger.info("Phoenix Rathaus connected to NATS")
        publish("crod.district.online", %{district: "phoenix-rathaus", port: 4000})
        {:noreply, state}
      {:error, reason} ->
        Logger.error("Failed to connect to NATS: #{inspect(reason)}")
        Process.send_after(self(), :reconnect, 5000)
        {:noreply, state}
    end
  end

  def handle_info({:msg, %{topic: topic, body: body}}, state) do
    Logger.info("Received message on #{topic}: #{body}")
    handle_message(topic, Jason.decode!(body))
    {:noreply, state}
  end

  def handle_info(:reconnect, state) do
    {:noreply, state, {:continue, :connect}}
  end

  def publish(topic, message) do
    case Jason.encode(message) do
      {:ok, json} ->
        Gnat.pub(:gnat, topic, json)
      {:error, reason} ->
        Logger.error("Failed to encode message: #{inspect(reason)}")
    end
  end

  defp handle_message("crod.district.online", %{"district" => district}) do
    PhoenixRathaus.DistrictRegistry.register_district(district)
  end

  defp handle_message("crod.pattern.match", %{"pattern" => pattern, "data" => data}) do
    result = PhoenixRathaus.PatternCoordinator.process_pattern(pattern, data)
    publish("crod.pattern.result", result)
  end

  defp handle_message(_, _), do: :ok
end