defmodule CROD.NatsClient do
  @moduledoc """
  NATS JetStream client for CROD blockchain.
  Handles all messaging between districts and services.
  """

  use GenServer
  require Logger

  @nats_url "nats://localhost:4222"
  @reconnect_interval 5_000

  # Client API

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Publishes a message to a subject
  """
  def publish(subject, message) do
    GenServer.call(__MODULE__, {:publish, subject, message})
  end

  @doc """
  Publishes a pattern discovery event
  """
  def publish_pattern(pattern) do
    subject = "patterns.discovered.#{pattern.type}"
    publish(subject, pattern)
  end

  @doc """
  Publishes a new block event
  """
  def publish_block(block) do
    subject = "blockchain.block.new"
    publish(subject, %{
      index: block.index,
      hash: block.hash,
      miner: block.miner,
      consciousness_level: block.consciousness_level,
      patterns: block.patterns,
      timestamp: block.timestamp
    })
  end

  @doc """
  Subscribes to a subject with a callback
  """
  def subscribe(subject, callback) do
    GenServer.cast(__MODULE__, {:subscribe, subject, callback})
  end

  @doc """
  Request-reply pattern
  """
  def request(subject, message, timeout \\ 5_000) do
    GenServer.call(__MODULE__, {:request, subject, message, timeout}, timeout + 1_000)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    Logger.info("🔌 Starting NATS client for CROD")
    
    state = %{
      connection: nil,
      subscriptions: %{},
      reconnecting: false,
      message_queue: []
    }
    
    # Connect to NATS
    send(self(), :connect)
    
    {:ok, state}
  end

  @impl true
  def handle_call({:publish, subject, message}, _from, %{connection: nil} = state) do
    # Queue message if not connected
    new_state = queue_message(state, {:publish, subject, message})
    {:reply, {:error, :not_connected}, new_state}
  end

  @impl true
  def handle_call({:publish, subject, message}, _from, %{connection: conn} = state) do
    Logger.debug("📤 Publishing to #{subject}")
    
    encoded_message = Jason.encode!(message)
    
    case Gnat.pub(conn, subject, encoded_message) do
      :ok ->
        {:reply, :ok, state}
      
      {:error, reason} = error ->
        Logger.error("Failed to publish: #{inspect(reason)}")
        {:reply, error, state}
    end
  end

  @impl true
  def handle_call({:request, subject, message, timeout}, from, %{connection: conn} = state) do
    Logger.debug("📮 Request to #{subject}")
    
    encoded_message = Jason.encode!(message)
    
    # Create inbox for reply
    inbox = "inbox.#{:rand.uniform(1_000_000)}"
    
    # Subscribe to inbox
    {:ok, _sub} = Gnat.sub(conn, inbox, self())
    
    # Publish with reply-to
    headers = %{"reply-to" => inbox}
    
    case Gnat.pub(conn, subject, encoded_message, headers: headers) do
      :ok ->
        # Wait for response
        Process.send_after(self(), {:request_timeout, from, inbox}, timeout)
        {:noreply, state}
        
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end

  @impl true
  def handle_cast({:subscribe, subject, callback}, %{connection: nil} = state) do
    # Queue subscription if not connected
    new_state = queue_message(state, {:subscribe, subject, callback})
    {:noreply, new_state}
  end

  @impl true
  def handle_cast({:subscribe, subject, callback}, %{connection: conn} = state) do
    Logger.info("📥 Subscribing to #{subject}")
    
    case Gnat.sub(conn, subject, self()) do
      {:ok, sub} ->
        new_subscriptions = Map.put(state.subscriptions, subject, {sub, callback})
        {:noreply, %{state | subscriptions: new_subscriptions}}
        
      {:error, reason} ->
        Logger.error("Failed to subscribe to #{subject}: #{inspect(reason)}")
        {:noreply, state}
    end
  end

  @impl true
  def handle_info(:connect, state) do
    Logger.info("🔄 Connecting to NATS at #{@nats_url}")
    
    case Gnat.start_link(%{host: "localhost", port: 4222}) do
      {:ok, conn} ->
        Logger.info("✅ Connected to NATS")
        
        # Process queued messages
        new_state = %{state | connection: conn, reconnecting: false}
        |> process_message_queue()
        
        # Setup default subscriptions
        setup_default_subscriptions(new_state)
        
      {:error, reason} ->
        Logger.error("❌ Failed to connect to NATS: #{inspect(reason)}")
        schedule_reconnect()
        {:noreply, %{state | reconnecting: true}}
    end
  end

  @impl true
  def handle_info({:msg, %{subject: subject, body: body}}, state) do
    Logger.debug("📨 Received message on #{subject}")
    
    # Find callback for subject
    case find_subscription_callback(state.subscriptions, subject) do
      {:ok, callback} ->
        # Decode message
        case Jason.decode(body) do
          {:ok, decoded} ->
            # Execute callback  
            spawn(fn -> callback.(subject, decoded) end)
            
          {:error, _} ->
            Logger.warn("Failed to decode message on #{subject}")
        end
        
      :error ->
        Logger.warn("No callback found for subject #{subject}")
    end
    
    {:noreply, state}
  end

  @impl true
  def handle_info({:request_timeout, from, inbox}, state) do
    GenServer.reply(from, {:error, :timeout})
    
    # Unsubscribe from inbox
    case Map.get(state.subscriptions, inbox) do
      {sub, _} -> Gnat.unsub(state.connection, sub)
      _ -> :ok
    end
    
    {:noreply, state}
  end

  @impl true
  def handle_info({:EXIT, conn, reason}, %{connection: conn} = state) do
    Logger.error("❌ NATS connection lost: #{inspect(reason)}")
    schedule_reconnect()
    {:noreply, %{state | connection: nil, reconnecting: true}}
  end

  # Private Functions

  defp queue_message(state, message) do
    %{state | message_queue: state.message_queue ++ [message]}
  end

  defp process_message_queue(%{message_queue: queue} = state) do
    Enum.each(queue, fn
      {:publish, subject, message} ->
        publish(subject, message)
        
      {:subscribe, subject, callback} ->
        subscribe(subject, callback)
    end)
    
    %{state | message_queue: []}
  end

  defp setup_default_subscriptions(state) do
    # Subscribe to blockchain events
    subscribe("blockchain.>", &handle_blockchain_event/2)
    
    # Subscribe to pattern events  
    subscribe("patterns.>", &handle_pattern_event/2)
    
    # Subscribe to quantum events
    subscribe("quantum.>", &handle_quantum_event/2)
    
    # Subscribe to consciousness events
    subscribe("consciousness.>", &handle_consciousness_event/2)
    
    {:noreply, state}
  end

  defp find_subscription_callback(subscriptions, subject) do
    # Direct match
    case Map.get(subscriptions, subject) do
      {_sub, callback} -> {:ok, callback}
      nil ->
        # Wildcard match
        subscriptions
        |> Enum.find(fn {pattern, _} ->
          match_subject_pattern?(pattern, subject)
        end)
        |> case do
          {_pattern, {_sub, callback}} -> {:ok, callback}
          nil -> :error
        end
    end
  end

  defp match_subject_pattern?(pattern, subject) do
    pattern_parts = String.split(pattern, ".")
    subject_parts = String.split(subject, ".")
    
    match_parts?(pattern_parts, subject_parts)
  end

  defp match_parts?([], []), do: true
  defp match_parts?([">" | _], _), do: true
  defp match_parts?([p | ps], [s | ss]) when p == s, do: match_parts?(ps, ss)
  defp match_parts?(["*" | ps], [_ | ss]), do: match_parts?(ps, ss)
  defp match_parts?(_, _), do: false

  defp schedule_reconnect do
    Process.send_after(self(), :connect, @reconnect_interval)
  end

  # Event Handlers

  defp handle_blockchain_event(subject, data) do
    Logger.info("⛓️  Blockchain event on #{subject}: #{inspect(data)}")
  end

  defp handle_pattern_event(subject, data) do
    Logger.info("🔍 Pattern event on #{subject}: #{inspect(data)}")
  end

  defp handle_quantum_event(subject, data) do
    Logger.info("⚛️  Quantum event on #{subject}: #{inspect(data)}")
  end

  defp handle_consciousness_event(subject, data) do
    Logger.info("🧠 Consciousness event on #{subject}: #{inspect(data)}")
  end
end