defmodule CROD.MessageBroker do
  @moduledoc """
  High-performance message broker for CROD network
  Replaces Python NATS with native Elixir implementation
  """
  
  use GenServer
  require Logger
  
  alias CROD.{Message, Subscription, MessageStore}
  
  defstruct [
    :node_id,
    :topics,          # Map of topic -> subscribers
    :subscriptions,   # Map of subscriber -> topics
    :message_store,   # Persistent message storage
    :metrics,
    :compression_enabled,
    :max_message_size
  ]
  
  @default_max_message_size 1_048_576  # 1MB
  @compression_threshold 1024          # Compress if > 1KB
  
  # Message Types
  defmodule Message do
    @enforce_keys [:id, :topic, :payload, :timestamp]
    defstruct [
      :id,
      :topic,
      :payload,
      :headers,
      :timestamp,
      :ttl,
      :priority,
      :compressed
    ]
    
    def new(topic, payload, opts \\ []) do
      %__MODULE__{
        id: generate_id(),
        topic: topic,
        payload: payload,
        headers: Keyword.get(opts, :headers, %{}),
        timestamp: System.system_time(:millisecond),
        ttl: Keyword.get(opts, :ttl),
        priority: Keyword.get(opts, :priority, 5),
        compressed: false
      }
    end
    
    def is_expired?(%__MODULE__{ttl: nil}), do: false
    def is_expired?(%__MODULE__{ttl: ttl, timestamp: ts}) do
      System.system_time(:millisecond) - ts > ttl
    end
    
    defp generate_id do
      :crypto.strong_rand_bytes(16) |> Base.encode16(case: :lower)
    end
  end
  
  # Public API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def publish(topic, payload, opts \\ []) do
    GenServer.call(__MODULE__, {:publish, topic, payload, opts})
  end
  
  def subscribe(topic_pattern, callback) when is_function(callback, 2) do
    GenServer.call(__MODULE__, {:subscribe, topic_pattern, callback, self()})
  end
  
  def unsubscribe(subscription_id) do
    GenServer.call(__MODULE__, {:unsubscribe, subscription_id})
  end
  
  def request_reply(topic, payload, timeout \\ 5000) do
    GenServer.call(__MODULE__, {:request_reply, topic, payload, timeout})
  end
  
  # Callbacks
  def init(opts) do
    node_id = Keyword.get(opts, :node_id, generate_node_id())
    
    state = %__MODULE__{
      node_id: node_id,
      topics: %{},
      subscriptions: %{},
      message_store: MessageStore.new(),
      metrics: init_metrics(),
      compression_enabled: Keyword.get(opts, :compression, true),
      max_message_size: Keyword.get(opts, :max_size, @default_max_message_size)
    }
    
    # Setup message cleanup
    schedule_cleanup()
    
    Logger.info("🚀 CROD Message Broker started on node: #{node_id}")
    
    {:ok, state}
  end
  
  def handle_call({:publish, topic, payload, opts}, _from, state) do
    # Create message
    message = Message.new(topic, payload, opts)
    
    # Compress if needed
    message = maybe_compress(message, state)
    
    # Validate size
    case validate_message_size(message, state.max_message_size) do
      :ok ->
        # Store message
        new_store = MessageStore.add(state.message_store, message)
        
        # Deliver to subscribers
        delivered = deliver_message(message, state.topics)
        
        # Update metrics
        new_metrics = update_metrics(state.metrics, :published, message)
        
        new_state = %{state | 
          message_store: new_store,
          metrics: new_metrics
        }
        
        {:reply, {:ok, message.id, delivered}, new_state}
        
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end
  
  def handle_call({:subscribe, pattern, callback, pid}, _from, state) do
    subscription_id = generate_subscription_id()
    
    # Create subscription
    subscription = %{
      id: subscription_id,
      pattern: pattern,
      callback: callback,
      pid: pid,
      created_at: System.system_time(:millisecond)
    }
    
    # Update topics mapping
    new_topics = add_subscription_to_topics(state.topics, pattern, subscription)
    
    # Update subscriptions mapping
    new_subscriptions = Map.put(state.subscriptions, subscription_id, subscription)
    
    # Monitor subscriber process
    Process.monitor(pid)
    
    Logger.info("📥 New subscription: #{pattern} -> #{subscription_id}")
    
    new_state = %{state | 
      topics: new_topics,
      subscriptions: new_subscriptions
    }
    
    {:reply, {:ok, subscription_id}, new_state}
  end
  
  def handle_call({:unsubscribe, subscription_id}, _from, state) do
    case Map.get(state.subscriptions, subscription_id) do
      nil ->
        {:reply, {:error, :not_found}, state}
        
      subscription ->
        # Remove from topics
        new_topics = remove_subscription_from_topics(state.topics, subscription)
        
        # Remove from subscriptions
        new_subscriptions = Map.delete(state.subscriptions, subscription_id)
        
        new_state = %{state |
          topics: new_topics,
          subscriptions: new_subscriptions
        }
        
        {:reply, :ok, new_state}
    end
  end
  
  def handle_call({:request_reply, topic, payload, timeout}, from, state) do
    # Create inbox for reply
    inbox = "crod.inbox.#{generate_id()}"
    
    # Subscribe to inbox
    reply_handler = fn _topic, reply_payload ->
      GenServer.reply(from, {:ok, reply_payload})
    end
    
    {:ok, inbox_sub} = subscribe(inbox, reply_handler)
    
    # Publish request with reply-to
    opts = [headers: %{"reply-to" => inbox}]
    {:ok, msg_id, _} = publish(topic, payload, opts)
    
    # Schedule timeout
    Process.send_after(self(), {:reply_timeout, from, inbox_sub}, timeout)
    
    {:noreply, state}
  end
  
  def handle_info({:DOWN, _ref, :process, pid, _reason}, state) do
    # Remove all subscriptions for dead process
    dead_subs = state.subscriptions
    |> Enum.filter(fn {_, sub} -> sub.pid == pid end)
    |> Enum.map(fn {id, _} -> id end)
    
    new_state = Enum.reduce(dead_subs, state, fn sub_id, acc ->
      case Map.get(acc.subscriptions, sub_id) do
        nil -> acc
        sub ->
          %{acc |
            topics: remove_subscription_from_topics(acc.topics, sub),
            subscriptions: Map.delete(acc.subscriptions, sub_id)
          }
      end
    end)
    
    {:noreply, new_state}
  end
  
  def handle_info({:reply_timeout, from, inbox_sub}, state) do
    # Clean up inbox subscription
    unsubscribe(inbox_sub)
    
    # Reply with timeout
    GenServer.reply(from, {:error, :timeout})
    
    {:noreply, state}
  end
  
  def handle_info(:cleanup, state) do
    # Remove expired messages
    new_store = MessageStore.cleanup_expired(state.message_store)
    
    # Update metrics
    cleaned = MessageStore.size(state.message_store) - MessageStore.size(new_store)
    
    if cleaned > 0 do
      Logger.info("🧹 Cleaned up #{cleaned} expired messages")
    end
    
    schedule_cleanup()
    
    {:noreply, %{state | message_store: new_store}}
  end
  
  # Private functions
  defp maybe_compress(message, state) do
    if state.compression_enabled and byte_size(message.payload) > @compression_threshold do
      compressed = :zlib.compress(message.payload)
      
      if byte_size(compressed) < byte_size(message.payload) * 0.9 do
        %{message | 
          payload: compressed,
          compressed: true,
          headers: Map.put(message.headers, "compression", "zlib")
        }
      else
        message
      end
    else
      message
    end
  end
  
  defp validate_message_size(message, max_size) do
    if byte_size(message.payload) <= max_size do
      :ok
    else
      {:error, :message_too_large}
    end
  end
  
  defp deliver_message(message, topics) do
    # Find matching subscribers
    matching_subs = topics
    |> Enum.filter(fn {pattern, _subs} -> 
      topic_matches?(message.topic, pattern)
    end)
    |> Enum.flat_map(fn {_pattern, subs} -> subs end)
    |> Enum.uniq_by(& &1.id)
    
    # Deliver to each subscriber
    delivered = Enum.map(matching_subs, fn sub ->
      try do
        # Decompress if needed
        payload = if message.compressed do
          :zlib.uncompress(message.payload)
        else
          message.payload
        end
        
        # Call callback
        sub.callback.(message.topic, payload)
        
        {:ok, sub.id}
      rescue
        e ->
          Logger.error("Failed to deliver to #{sub.id}: #{inspect(e)}")
          {:error, sub.id}
      end
    end)
    
    # Count successful deliveries
    Enum.count(delivered, fn {status, _} -> status == :ok end)
  end
  
  defp topic_matches?(topic, pattern) do
    topic_parts = String.split(topic, ".")
    pattern_parts = String.split(pattern, ".")
    
    match_parts?(topic_parts, pattern_parts)
  end
  
  defp match_parts?([], []), do: true
  defp match_parts?(_, [">" | _]), do: true
  defp match_parts?([_ | t_rest], ["*" | p_rest]), do: match_parts?(t_rest, p_rest)
  defp match_parts?([same | t_rest], [same | p_rest]), do: match_parts?(t_rest, p_rest)
  defp match_parts?(_, _), do: false
  
  defp add_subscription_to_topics(topics, pattern, subscription) do
    Map.update(topics, pattern, [subscription], fn subs ->
      [subscription | subs]
    end)
  end
  
  defp remove_subscription_from_topics(topics, subscription) do
    topics
    |> Enum.map(fn {pattern, subs} ->
      new_subs = Enum.reject(subs, & &1.id == subscription.id)
      {pattern, new_subs}
    end)
    |> Enum.reject(fn {_pattern, subs} -> Enum.empty?(subs) end)
    |> Map.new()
  end
  
  defp generate_node_id do
    :crypto.strong_rand_bytes(8) |> Base.encode16(case: :lower)
  end
  
  defp generate_subscription_id do
    "sub_#{System.unique_integer([:positive])}"
  end
  
  defp generate_id do
    :crypto.strong_rand_bytes(8) |> Base.encode16(case: :lower)
  end
  
  defp init_metrics do
    %{
      messages_published: 0,
      messages_delivered: 0,
      bytes_sent: 0,
      compression_ratio: 1.0,
      subscriptions_active: 0
    }
  end
  
  defp update_metrics(metrics, :published, message) do
    %{metrics |
      messages_published: metrics.messages_published + 1,
      bytes_sent: metrics.bytes_sent + byte_size(message.payload)
    }
  end
  
  defp schedule_cleanup do
    Process.send_after(self(), :cleanup, 60_000)  # Every minute
  end
end

defmodule CROD.MessageStore do
  @moduledoc "Persistent message storage with TTL support"
  
  defstruct messages: %{}, by_topic: %{}, by_timestamp: []
  
  def new, do: %__MODULE__{}
  
  def add(store, message) do
    %{store |
      messages: Map.put(store.messages, message.id, message),
      by_topic: Map.update(store.by_topic, message.topic, [message.id], &[message.id | &1]),
      by_timestamp: [{message.timestamp, message.id} | store.by_timestamp]
    }
  end
  
  def get(store, message_id) do
    Map.get(store.messages, message_id)
  end
  
  def get_by_topic(store, topic, limit \\ 100) do
    store.by_topic
    |> Map.get(topic, [])
    |> Enum.take(limit)
    |> Enum.map(&Map.get(store.messages, &1))
    |> Enum.reject(&is_nil/1)
  end
  
  def cleanup_expired(store) do
    # Find expired messages
    expired_ids = store.messages
    |> Enum.filter(fn {_id, msg} -> CROD.MessageBroker.Message.is_expired?(msg) end)
    |> Enum.map(fn {id, _} -> id end)
    
    # Remove from all indices
    new_messages = Map.drop(store.messages, expired_ids)
    
    new_by_topic = store.by_topic
    |> Enum.map(fn {topic, ids} ->
      {topic, Enum.reject(ids, &(&1 in expired_ids))}
    end)
    |> Enum.reject(fn {_topic, ids} -> Enum.empty?(ids) end)
    |> Map.new()
    
    new_by_timestamp = store.by_timestamp
    |> Enum.reject(fn {_ts, id} -> id in expired_ids end)
    
    %{store |
      messages: new_messages,
      by_topic: new_by_topic,
      by_timestamp: new_by_timestamp
    }
  end
  
  def size(store), do: map_size(store.messages)
end

defmodule CROD.EventBus do
  @moduledoc """
  High-level event bus built on message broker
  """
  
  def emit(event_type, data, metadata \\ %{}) do
    event = %{
      type: event_type,
      data: data,
      metadata: metadata,
      timestamp: System.system_time(:millisecond),
      source: node()
    }
    
    CROD.MessageBroker.publish(
      "crod.events.#{event_type}",
      :erlang.term_to_binary(event)
    )
  end
  
  def on(event_type, handler) when is_function(handler, 2) do
    callback = fn _topic, payload ->
      event = :erlang.binary_to_term(payload)
      if event.type == event_type do
        handler.(event.data, event.metadata)
      end
    end
    
    CROD.MessageBroker.subscribe("crod.events.#{event_type}", callback)
  end
  
  def request(service, method, params) do
    request = %{
      method: method,
      params: params,
      id: System.unique_integer([:positive])
    }
    
    CROD.MessageBroker.request_reply(
      "crod.rpc.#{service}",
      :erlang.term_to_binary(request)
    )
  end
end