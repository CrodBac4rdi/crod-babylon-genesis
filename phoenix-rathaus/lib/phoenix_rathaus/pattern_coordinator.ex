defmodule PhoenixRathaus.PatternCoordinator do
  use GenServer
  require Logger

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  @impl true
  def init(_) do
    Logger.info("🧠 Pattern Coordinator initializing...")
    
    # Subscribe to pattern-related NATS topics
    {:ok, _} = Gnat.sub(:gnat, self(), "pattern.request")
    {:ok, _} = Gnat.sub(:gnat, self(), "pattern.result")
    
    {:ok, %{
      active_patterns: %{},
      pattern_cache: %{},
      request_queue: :queue.new()
    }}
  end

  @impl true
  def handle_info({:msg, %{body: body, topic: "pattern.request", reply_to: reply_to}}, state) do
    case Jason.decode(body) do
      {:ok, request} ->
        # Forward to Rust Pattern District
        case process_pattern_request(request, reply_to) do
          {:ok, result} ->
            {:noreply, update_pattern_cache(state, request, result)}
          {:error, _reason} ->
            {:noreply, state}
        end
      _ ->
        {:noreply, state}
    end
  end

  @impl true
  def handle_info({:msg, %{body: body, topic: "pattern.result"}}, state) do
    case Jason.decode(body) do
      {:ok, %{"pattern_id" => id, "result" => result}} ->
        broadcast_pattern_result(id, result)
        {:noreply, state}
      _ ->
        {:noreply, state}
    end
  end

  @impl true
  def handle_call({:analyze_pattern, text}, _from, state) do
    request_id = generate_request_id()
    request = %{
      id: request_id,
      text: text,
      timestamp: System.system_time(:millisecond)
    }
    
    # Check cache first
    case Map.get(state.pattern_cache, text) do
      nil ->
        # Send to Rust Pattern District via NATS
        Gnat.pub(:gnat, "pattern.analyze", Jason.encode!(request))
        {:reply, {:pending, request_id}, state}
      
      cached_result ->
        {:reply, {:ok, cached_result}, state}
    end
  end

  defp process_pattern_request(request, reply_to) do
    # Coordinate with Rust Pattern District
    enriched_request = Map.merge(request, %{
      coordinator: "phoenix_rathaus",
      priority: calculate_priority(request)
    })
    
    response = Jason.encode!(%{status: "processing", request_id: request["id"]})
    Gnat.pub(:gnat, reply_to, response)
    
    {:ok, enriched_request}
  end

  defp update_pattern_cache(state, request, result) do
    new_cache = Map.put(state.pattern_cache, request["text"], result)
    
    # Limit cache size
    if map_size(new_cache) > 1000 do
      %{state | pattern_cache: Map.drop(new_cache, [oldest_cache_key(new_cache)])}
    else
      %{state | pattern_cache: new_cache}
    end
  end

  defp calculate_priority(%{"urgent" => true}), do: :high
  defp calculate_priority(%{"source" => "python_parasit"}), do: :high
  defp calculate_priority(_), do: :normal

  defp generate_request_id do
    :crypto.strong_rand_bytes(16) |> Base.encode16()
  end

  defp oldest_cache_key(cache) do
    cache
    |> Map.keys()
    |> List.first()
  end

  defp broadcast_pattern_result(pattern_id, result) do
    Phoenix.PubSub.broadcast(
      PhoenixRathaus.PubSub,
      "patterns",
      {:pattern_result, pattern_id, result}
    )
  end

  # Public API
  def analyze_pattern(text) do
    GenServer.call(__MODULE__, {:analyze_pattern, text})
  end
end