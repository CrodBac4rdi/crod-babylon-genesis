defmodule Crod.Services.NatsClient do
  @moduledoc """
  NATS client for CROD's messaging infrastructure.
  Handles pub/sub communication between polygon city districts.
  """

  use GenServer
  require Logger

  @reconnect_interval 5_000

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    # Get connection settings from config
    settings = Application.get_env(:crod, __MODULE__)[:connection_settings]
    
    # Start connection process
    send(self(), :connect)
    
    {:ok, %{
      connection: nil,
      settings: settings,
      subscriptions: %{},
      pending_messages: :queue.new()
    }}
  end

  # Public API

  @doc """
  Publishes a message to a NATS topic.
  """
  def publish(topic, message) when is_binary(topic) do
    GenServer.cast(__MODULE__, {:publish, topic, message})
  end

  @doc """
  Subscribes to a NATS topic.
  """
  def subscribe(topic, pid \\ self()) when is_binary(topic) do
    GenServer.call(__MODULE__, {:subscribe, topic, pid})
  end

  @doc """
  Unsubscribes from a NATS topic.
  """
  def unsubscribe(topic, pid \\ self()) when is_binary(topic) do
    GenServer.call(__MODULE__, {:unsubscribe, topic, pid})
  end

  @doc """
  Performs a request-reply operation.
  """
  def request(topic, message, timeout \\ 5_000) do
    GenServer.call(__MODULE__, {:request, topic, message, timeout}, timeout + 1_000)
  end

  # GenServer callbacks

  @impl true
  def handle_call({:subscribe, topic, pid}, _from, state) do
    case state.connection do
      nil ->
        {:reply, {:error, :not_connected}, state}
      
      conn ->
        case Gnat.sub(conn, pid, topic) do
          {:ok, sid} ->
            subscriptions = Map.put(state.subscriptions, {topic, pid}, sid)
            {:reply, :ok, %{state | subscriptions: subscriptions}}
          
          {:error, reason} ->
            {:reply, {:error, reason}, state}
        end
    end
  end

  @impl true
  def handle_call({:unsubscribe, topic, pid}, _from, state) do
    case Map.get(state.subscriptions, {topic, pid}) do
      nil ->
        {:reply, {:error, :not_subscribed}, state}
      
      sid ->
        case state.connection do
          nil ->
            {:reply, {:error, :not_connected}, state}
          
          conn ->
            :ok = Gnat.unsub(conn, sid)
            subscriptions = Map.delete(state.subscriptions, {topic, pid})
            {:reply, :ok, %{state | subscriptions: subscriptions}}
        end
    end
  end

  @impl true
  def handle_call({:request, topic, message, timeout}, from, state) do
    case state.connection do
      nil ->
        {:reply, {:error, :not_connected}, state}
      
      conn ->
        Task.start(fn ->
          result = Gnat.request(conn, topic, encode_message(message), request_timeout: timeout)
          GenServer.reply(from, decode_response(result))
        end)
        
        {:noreply, state}
    end
  end

  @impl true
  def handle_cast({:publish, topic, message}, state) do
    encoded = encode_message(message)
    
    case state.connection do
      nil ->
        # Queue message for later
        pending = :queue.in({topic, encoded}, state.pending_messages)
        {:noreply, %{state | pending_messages: pending}}
      
      conn ->
        case Gnat.pub(conn, topic, encoded) do
          :ok ->
            {:noreply, state}
          
          {:error, reason} ->
            Logger.error("Failed to publish to #{topic}: #{inspect(reason)}")
            {:noreply, state}
        end
    end
  end

  @impl true
  def handle_info(:connect, state) do
    case connect_to_nats(state.settings) do
      {:ok, conn} ->
        Logger.info("Connected to NATS")
        
        # Resubscribe to all topics
        resubscribe_all(conn, state.subscriptions)
        
        # Publish pending messages
        state = publish_pending_messages(conn, state)
        
        {:noreply, %{state | connection: conn}}
      
      {:error, reason} ->
        Logger.error("Failed to connect to NATS: #{inspect(reason)}")
        Process.send_after(self(), :connect, @reconnect_interval)
        {:noreply, state}
    end
  end

  @impl true
  def handle_info({:msg, %{topic: topic, body: body}}, state) do
    # Decode and forward message to subscribers
    decoded = decode_message(body)
    
    state.subscriptions
    |> Enum.filter(fn {{t, _}, _} -> t == topic end)
    |> Enum.each(fn {{_, pid}, _} ->
      send(pid, {:nats_message, topic, decoded})
    end)
    
    {:noreply, state}
  end

  @impl true
  def handle_info({:DOWN, _ref, :process, pid, _reason}, state) do
    # Remove subscriptions for dead process
    subscriptions = state.subscriptions
    |> Enum.reject(fn {{_, p}, _} -> p == pid end)
    |> Map.new()
    
    {:noreply, %{state | subscriptions: subscriptions}}
  end

  # Private functions

  defp connect_to_nats(settings) do
    Gnat.start_link(settings)
  end

  defp encode_message(message) when is_binary(message), do: message
  defp encode_message(message), do: Jason.encode!(message)

  defp decode_message(body) do
    case Jason.decode(body) do
      {:ok, decoded} -> decoded
      {:error, _} -> body
    end
  end

  defp decode_response({:ok, %{body: body}}) do
    {:ok, decode_message(body)}
  end
  defp decode_response({:error, reason}) do
    {:error, reason}
  end

  defp resubscribe_all(conn, subscriptions) do
    Enum.each(subscriptions, fn {{topic, pid}, _old_sid} ->
      case Gnat.sub(conn, pid, topic) do
        {:ok, _new_sid} ->
          Logger.debug("Resubscribed to #{topic}")
        
        {:error, reason} ->
          Logger.error("Failed to resubscribe to #{topic}: #{inspect(reason)}")
      end
    end)
  end

  defp publish_pending_messages(conn, state) do
    case :queue.out(state.pending_messages) do
      {{:value, {topic, message}}, remaining} ->
        case Gnat.pub(conn, topic, message) do
          :ok ->
            publish_pending_messages(conn, %{state | pending_messages: remaining})
          
          {:error, _reason} ->
            # Put it back and stop
            state
        end
      
      {:empty, _} ->
        %{state | pending_messages: :queue.new()}
    end
  end
end