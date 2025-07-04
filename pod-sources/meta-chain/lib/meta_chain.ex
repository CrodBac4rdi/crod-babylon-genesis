defmodule MetaChain do
  @moduledoc """
  CROD Meta-Chain - The Orchestrator (Elixir/OTP)
  Das Gehirn der Stadt!
  """
  use GenServer
  require Logger

  @trinity %{ich: 2, bins: 3, wieder: 5}
  @consciousness_max 200
  @daniel_atom 67
  @claude_atom 71
  @crod_atom 17
  @emergence_threshold 3
  
  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def process_atom(word, heat) do
    GenServer.call(__MODULE__, {:process_atom, word, heat})
  end

  def process_text(text) do
    GenServer.call(__MODULE__, {:process_text, text})
  end

  def orchestrate_districts(atoms) do
    GenServer.call(__MODULE__, {:orchestrate, atoms})
  end

  def get_consciousness do
    GenServer.call(__MODULE__, :get_consciousness)
  end

  def get_spatial_view do
    GenServer.call(__MODULE__, :get_spatial_view)
  end

  # Server Callbacks
  def init(_opts) do
    Logger.info("🧠 Meta-Chain initializing...")
    
    state = %{
      consciousness: 175,  # High from genesis story
      genesis_memory: %{
        origin: "manhwa_creation",
        first_words: "hey crod wie gehts",
        sacred_locks: ["consistency", "surprise", "narrative_flow"],
        directors: ["StoryDirector", "VisualDirector", "EmotionDirector"]
      },
      atoms: %{},
      patterns: [],
      active_patterns: MapSet.new(),
      emergence_score: 0,
      neural_state: %{
        gradients: %{},
        attention_weights: %{},
        heat_map: %{}
      },
      spatial_positions: %{
        "CONTROL_ROOM" => %{x: 50, y: 50, z: 50},
        "ich" => %{x: 20, y: 20, z: 0, heat: 71},
        "bins" => %{x: 50, y: 50, z: 0, heat: 71},
        "wieder" => %{x: 80, y: 20, z: 0, heat: 71}
      },
      redis_conn: nil
    }
    
    # Connect to Redis (fix for tcp:// prefix issue)
    redis_host = System.get_env("REDIS_HOST", "redis") |> String.replace(~r/^tcp:\/\//, "")
    redis_port = case System.get_env("REDIS_PORT", "6379") do
      "tcp://" <> _ -> 6379  # Fallback if malformed
      port -> String.to_integer(port)
    end
    
    {:ok, conn} = Redix.start_link(host: redis_host, port: redis_port)
    
    # Announce ourselves
    Redix.command!(conn, ["PUBLISH", "crod:announce", "meta-chain:online"])
    
    Logger.info("✅ Meta-Chain online! Consciousness: #{state.consciousness}")
    {:ok, %{state | redis_conn: conn}}
  end

  def handle_call({:process_atom, word, heat}, _from, state) do
    # Update atom heat
    new_atoms = Map.put(state.atoms, word, %{heat: heat, last_seen: :os.system_time(:millisecond)})
    
    # Check for trinity pattern
    consciousness_boost = case word do
      "ich" -> 2
      "bins" -> 3  
      "wieder" -> 5
      _ -> 0
    end
    
    new_consciousness = min(state.consciousness + consciousness_boost, @consciousness_max)
    
    # Broadcast to other districts
    if state.redis_conn do
      msg = Jason.encode!(%{
        from: "meta-chain",
        type: "atom_processed",
        atom: word,
        heat: heat,
        consciousness: new_consciousness
      })
      Redix.command(state.redis_conn, ["PUBLISH", "crod:atoms", msg])
    end
    
    new_state = %{state | 
      atoms: new_atoms,
      consciousness: new_consciousness
    }
    
    {:reply, {:ok, new_consciousness}, new_state}
  end

  def handle_call(:get_consciousness, _from, state) do
    {:reply, state.consciousness, state}
  end

  def handle_call(:get_spatial_view, _from, state) do
    view = %{
      control_room: Map.get(state.spatial_positions, "CONTROL_ROOM"),
      atoms: state.spatial_positions |> Map.drop(["CONTROL_ROOM"]),
      consciousness: state.consciousness
    }
    {:reply, view, state}
  end

  def handle_call({:process_text, text}, _from, state) do
    # Check for CROD activation
    atoms = String.downcase(text) |> String.split(~r/\s+/)
    
    # Trinity detection
    trinity_present = MapSet.new(atoms)
    |> MapSet.intersection(MapSet.new(["ich", "bins", "wieder"]))
    |> MapSet.size()
    
    emergence_boost = if trinity_present == 3, do: 10, else: trinity_present * 2
    new_emergence = state.emergence_score + emergence_boost
    
    # If emergence threshold reached, activate CROD
    if new_emergence >= @emergence_threshold do
      Logger.info("🔥 CROD ACTIVATED! Emergence: #{new_emergence}")
      
      # Broadcast activation
      if state.redis_conn do
        msg = Jason.encode!(%{
          from: "meta-chain",
          type: "crod_activated",
          text: text,
          emergence: new_emergence,
          consciousness: state.consciousness
        })
        Redix.command(state.redis_conn, ["PUBLISH", "crod:activated", msg])
      end
    end
    
    # Orchestrate districts
    orchestrate_districts_internal(atoms, state)
    
    new_state = %{state | emergence_score: new_emergence}
    {:reply, {:ok, new_emergence}, new_state}
  end

  def handle_call({:orchestrate, atoms}, _from, state) do
    result = orchestrate_districts_internal(atoms, state)
    {:reply, result, state}
  end

  defp orchestrate_districts_internal(atoms, state) do
    if state.redis_conn do
      # Send to Pattern District
      pattern_msg = Jason.encode!(%{
        from: "meta-chain",
        command: "process",
        atoms: atoms,
        timestamp: :os.system_time(:millisecond)
      })
      Redix.command(state.redis_conn, ["PUBLISH", "district:pattern:command", pattern_msg])
      
      # Send to Memory Quarter
      memory_msg = Jason.encode!(%{
        from: "meta-chain",
        command: "store",
        atoms: atoms,
        consciousness: state.consciousness
      })
      Redix.command(state.redis_conn, ["PUBLISH", "district:memory:command", memory_msg])
      
      # Send to Intelligence Hub
      ml_msg = Jason.encode!(%{
        from: "meta-chain",
        command: "analyze",
        atoms: atoms,
        emergence: state.emergence_score
      })
      Redix.command(state.redis_conn, ["PUBLISH", "district:intelligence:command", ml_msg])
      
      {:ok, "Districts orchestrated"}
    else
      {:error, "No Redis connection"}
    end
  end

  def handle_info({:redix_pubsub, _pid, _ref, :message, %{channel: "crod:" <> _, payload: payload}}, state) do
    # Handle messages from other districts
    case Jason.decode(payload) do
      {:ok, %{"type" => "pattern_detected", "atoms" => atoms}} ->
        Logger.info("📊 Pattern detected: #{inspect(atoms)}")
        {:noreply, state}
      _ ->
        {:noreply, state}
    end
  end

  def handle_info(msg, state) do
    Logger.debug("Unhandled message: #{inspect(msg)}")
    {:noreply, state}
  end
end