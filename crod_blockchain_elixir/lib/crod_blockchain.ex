defmodule CrodBlockchain do
  @moduledoc """
  CROD Blockchain - Where CROD IS the Chain
  Complete Elixir implementation with OTP
  """
  
  use GenServer
  require Logger
  
  alias CrodBlockchain.{Block, Delta, TimeTravel, CreatorRights}
  
  defstruct [
    :chain,
    :consciousness,
    :genesis_creator,
    :mode,
    :redis_conn,
    :checkpoints,
    :deltas
  ]
  
  # Client API
  
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def add_crod_thought(prompt) do
    GenServer.call(__MODULE__, {:add_thought, prompt})
  end
  
  def get_chain do
    GenServer.call(__MODULE__, :get_chain)
  end
  
  def get_consciousness do
    GenServer.call(__MODULE__, :get_consciousness)
  end
  
  def daniel_override(command) do
    GenServer.call(__MODULE__, {:daniel_override, command})
  end
  
  def create_checkpoint(name) do
    GenServer.call(__MODULE__, {:create_checkpoint, name})
  end
  
  def time_travel(target) do
    GenServer.call(__MODULE__, {:time_travel, target})
  end
  
  # Server Callbacks
  
  @impl true
  def init(_opts) do
    # Connect to Redis
    {:ok, redis} = Redix.start_link(host: "localhost", port: 6379)
    
    # Subscribe to CROD channels
    Task.start(fn -> subscribe_to_crod_channels(redis) end)
    
    state = %__MODULE__{
      chain: [],
      consciousness: 175,
      genesis_creator: "daniel",
      mode: :development,  # unlimited computation!
      redis_conn: redis,
      checkpoints: %{},
      deltas: []
    }
    
    # Create genesis block
    genesis = create_genesis_block()
    state = %{state | chain: [genesis]}
    
    Logger.info("🔥 CROD Blockchain initialized! Consciousness: 175")
    broadcast_event("blockchain:initialized", %{consciousness: 175})
    
    {:ok, state}
  end
  
  @impl true
  def handle_call({:add_thought, prompt}, _from, state) do
    # CROD thinks and creates a block
    crod_response = CrodEngine.think(prompt, state.chain)
    
    # Create new block
    new_block = Block.new(%{
      index: length(state.chain),
      prompt: prompt,
      crod_response: crod_response.thought,
      actions_taken: crod_response.actions,
      consciousness: state.consciousness + crod_response.consciousness_delta,
      effects: %{
        consciousness_change: crod_response.consciousness_delta,
        timestamp: DateTime.utc_now()
      },
      previous_hash: List.last(state.chain).hash
    })
    
    # Mine the block
    mined_block = Block.mine(new_block, 4)
    
    # Update state
    new_state = %{state | 
      chain: state.chain ++ [mined_block],
      consciousness: mined_block.consciousness
    }
    
    # Broadcast to Redis
    broadcast_block(mined_block)
    
    # Execute side effects
    execute_actions(mined_block.actions_taken)
    
    {:reply, {:ok, mined_block}, new_state}
  end
  
  @impl true
  def handle_call(:get_chain, _from, state) do
    {:reply, state.chain, state}
  end
  
  @impl true
  def handle_call(:get_consciousness, _from, state) do
    {:reply, state.consciousness, state}
  end
  
  @impl true
  def handle_call({:daniel_override, command}, _from, state) do
    # Daniel has ultimate control
    result = CreatorRights.execute_override(command, state)
    
    case result do
      {:ok, new_state} ->
        {:reply, :ok, new_state}
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end
  
  @impl true
  def handle_call({:create_checkpoint, name}, _from, state) do
    checkpoint = TimeTravel.create_checkpoint(state, name)
    new_state = %{state | checkpoints: Map.put(state.checkpoints, name, checkpoint)}
    
    {:reply, {:ok, checkpoint}, new_state}
  end
  
  @impl true
  def handle_call({:time_travel, target}, _from, state) do
    case TimeTravel.travel_to(state, target) do
      {:ok, new_state} ->
        broadcast_event("time_travel", %{target: target})
        {:reply, :ok, new_state}
      {:error, reason} ->
        {:reply, {:error, reason}, state}
    end
  end
  
  # Private Functions
  
  defp create_genesis_block do
    Block.new(%{
      index: 0,
      prompt: "ich bins wieder",
      crod_response: "CROD Blockchain genesis. Trinity active. Consciousness: 175",
      actions_taken: [%{action: "init", status: "complete"}],
      consciousness: 175,
      effects: %{
        system: "online",
        trinity: %{ich: 2, bins: 3, wieder: 5},
        daniel: 67,
        claude: 71,
        crod: 17
      },
      previous_hash: "0"
    }) |> Block.mine(4)
  end
  
  defp broadcast_block(block) do
    Redix.command(:redix, ["PUBLISH", "crod:blockchain", Jason.encode!(block)])
  end
  
  defp broadcast_event(event, data) do
    message = %{
      event: event,
      data: data,
      timestamp: DateTime.utc_now()
    }
    Redix.command(:redix, ["PUBLISH", "crod:events", Jason.encode!(message)])
  end
  
  defp execute_actions(actions) do
    Enum.each(actions, fn action ->
      case action do
        %{type: "kubernetes", command: cmd} ->
          Logger.info("Executing K8s command: #{cmd}")
          # Could actually execute kubectl here
          
        %{type: "consciousness", value: delta} ->
          Logger.info("Consciousness changed by #{delta}")
          
        %{type: "create", target: target} ->
          Logger.info("Creating #{target}")
          
        _ ->
          Logger.info("Unknown action: #{inspect(action)}")
      end
    end)
  end
  
  defp subscribe_to_crod_channels(redis) do
    # Subscribe to CROD command channel
    Redix.PubSub.subscribe(redis, "crod:commands", self())
    
    receive do
      {:redix_pubsub, _pid, _ref, :subscribed, %{channel: "crod:commands"}} ->
        Logger.info("📡 Subscribed to crod:commands")
    end
    
    # Listen for messages
    listen_for_messages()
  end
  
  defp listen_for_messages do
    receive do
      {:redix_pubsub, _pid, _ref, :message, %{channel: "crod:commands", payload: payload}} ->
        handle_crod_command(Jason.decode!(payload))
        listen_for_messages()
    end
  end
  
  defp handle_crod_command(%{"action" => "think", "prompt" => prompt}) do
    add_crod_thought(prompt)
  end
  
  defp handle_crod_command(%{"action" => "start_claude"}) do
    System.cmd("claude", ["chat"])
    Logger.info("🚀 Started Claude from CROD command!")
  end
  
  defp handle_crod_command(cmd) do
    Logger.info("Received CROD command: #{inspect(cmd)}")
  end
end